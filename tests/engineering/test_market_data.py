"""Inputs: market-data hygiene, real-chain quotes, input guards, news sources."""

from __future__ import annotations

import json
import math
import sqlite3
from dataclasses import asdict, replace
from datetime import date

import numpy as np
import pandas as pd
import pytest
from scipy.stats import norm
from support import FAST, aapl_nov20_call, jpm_oct23_straddle

from explain_my_option.data.cache import MIN_PLAUSIBLE_IV, load_t1, upsert_snapshot
from explain_my_option.data.dividends import normalize_dividend_yield
from explain_my_option.data.historical_chain import imply_borrow_rate, quote_hygiene
from explain_my_option.data.observation import (
    DataBreakError,
    NoComparableObservationError,
    ObservationStatus,
    check_basis_consistency,
    check_calibrated_iv,
    check_mark_bounds,
    classify_observation_status,
    continuity_gate,
)
from explain_my_option.data.realized import hv20_from_closes, iv_prev_from_hv20
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.data_loader import (
    _clean_iv,
    prior_close,
    quote_session,
    session_close,
    session_closed,
    settlement_snapshot,
)
from explain_my_option.intel.sec_edgar import SecEdgar8KSource, reset_ticker_cache
from explain_my_option.intel.sources import IntelRegistry, TavilyNewsSource
from explain_my_option.intel.types import SearchPlan, SearchQuery
from explain_my_option.pricing.facade import price_and_attribute
from explain_my_option.pricing.surface import parallel_shift_surface
from explain_my_option.pricing.types import MarketSnapshot

# --- Live market data ---------------------------------------------------------------------


def _bars(closes: dict[str, float]) -> pd.DataFrame:
    index = pd.DatetimeIndex(list(closes)).tz_localize("America/New_York")
    return pd.DataFrame({"Close": list(closes.values())}, index=index)


# Yahoo at 21:15 ET on 2026-11-04: the session's daily bar is listed with no close yet.
EVENING_BARS = {"2026-10-30": 344.63, "2026-11-02": 338.32, "2026-11-03": 331.90, "2026-11-04": np.nan}
EVENING_META = {
    "regularMarketPrice": 349.51,
    "regularMarketTime": pd.Timestamp("2026-11-04 16:00:01", tz="America/New_York"),
    "exchangeTimezoneName": "America/New_York",
}


def test_spot_is_the_close_of_the_session_the_quotes_belong_to():
    hist = _bars(EVENING_BARS)
    session = quote_session(hist, EVENING_META)
    assert session == date(2026, 11, 4)
    # The bar's close is NaN: the regular-market price stamped with the session stands in.
    assert session_close(hist, session, market_price=349.51, market_price_session=session) == 349.51
    assert prior_close(hist, session) == (331.90, date(2026, 11, 3))
    # Epoch seconds, as older yfinance returns them, give the same session.
    epoch = {**EVENING_META, "regularMarketTime": int(EVENING_META["regularMarketTime"].timestamp())}
    assert quote_session(hist, epoch) == session


def test_a_session_without_a_close_is_a_data_break_not_yesterdays_spot():
    """The old rule took the last two *valid* closes: 331.90 and 338.32, one session late."""
    hist = _bars(EVENING_BARS)
    assert quote_session(hist) == date(2026, 11, 4)  # no metadata: the newest bar, NaN close or not
    with pytest.raises(DataBreakError, match="no 2026-11-04 close yet"):
        session_close(hist, date(2026, 11, 4))
    with pytest.raises(DataBreakError, match="no 2026-11-04 close yet"):
        session_close(hist, date(2026, 11, 4), market_price=331.90, market_price_session=date(2026, 11, 3))


def test_the_prior_spot_is_dated_to_the_prior_mark():
    hist = _bars({**EVENING_BARS, "2026-11-04": 349.51})
    # A missed run: the newest cached mark is from 10-30, so is its spot.
    assert prior_close(hist, date(2026, 11, 4), prior_mark_date=date(2026, 10, 30)) == (344.63, date(2026, 10, 30))
    # A weekend run captured Friday's quotes under Saturday's date.
    assert prior_close(hist, date(2026, 11, 4), prior_mark_date=date(2026, 10, 31)) == (344.63, date(2026, 10, 30))
    with pytest.raises(DataBreakError, match="no close on or before 2026-10-01"):
        prior_close(hist, date(2026, 11, 4), prior_mark_date=date(2026, 10, 1))


def test_a_first_live_day_never_calibrates_to_a_copied_prior_mark():
    """No t-1 in the cache: a prior mark copied from today forced ΔP_model to 0."""
    snap = replace(aapl_nov20_call(350.0, stale_spot=False), option_price_prev=6.925, iv_prev_source="hv20_proxy")
    result = price_and_attribute(snap, config=FAST)
    assert not result.diagnostics.mark_calibrated
    assert result.pnl.total_pnl > 3.0 and result.pnl.delta_pnl > 0  # the +17.61 spot move survives


def test_an_expired_contract_settles_from_its_expiry_close_and_last_mark(tmp_path, monkeypatch):
    """JPM 350P, expired 10-23, first run since on 11-05: no chain read, the 10-22 mark."""
    monkeypatch.chdir(tmp_path)  # the T-1 cache path is relative
    upsert_snapshot(replace(jpm_oct23_straddle("put"), as_of="2026-10-22", option_price_now=14.10, time_to_expiry_years=1 / 365), None)
    hist = _bars({"2026-10-21": 335.19, "2026-10-22": 336.54, "2026-10-23": 331.58, "2026-10-26": 334.04, "2026-11-05": np.nan})
    snap = settlement_snapshot(hist, {}, ticker="JPM", option_type="put", strike=350.0, expiry="2026-10-23", session=date(2026, 11, 5))
    assert (snap.as_of, snap.spot_now, snap.option_price_now) == ("2026-10-23", 331.58, pytest.approx(18.42))
    assert (snap.prev_as_of, snap.spot_prev, snap.option_price_prev) == ("2026-10-22", 336.54, 14.10)
    assert snap.time_to_expiry_years == 0.0 and snap.iv_prev_source == "chain_t1"
    # No cached mark for the call: settled, but with no prior mark to compute PnL from.
    call = settlement_snapshot(hist, {}, ticker="JPM", option_type="call", strike=350.0, expiry="2026-10-23", session=date(2026, 11, 5))
    assert (call.option_price_now, call.option_price_prev, call.iv_prev_source) == (0.0, 0.0, "copied")


def test_an_option_expiring_today_settles_only_once_the_session_has_closed():
    hist = _bars(EVENING_BARS)
    snap = settlement_snapshot(hist, EVENING_META, ticker="AAPL", option_type="call", strike=325.0, expiry="2026-11-04", session=date(2026, 11, 4))
    assert (snap.as_of, snap.spot_now, snap.option_price_now) == ("2026-11-04", 349.51, pytest.approx(24.51))
    intraday = {**EVENING_META, "regularMarketTime": pd.Timestamp("2026-11-04 13:00", tz="America/New_York")}
    assert not session_closed(hist, date(2026, 11, 4), intraday)
    with pytest.raises(ValueError, match="rerun after the close"):
        settlement_snapshot(hist, intraday, ticker="AAPL", option_type="call", strike=325.0, expiry="2026-11-04", session=date(2026, 11, 4))
    # A 13:00 early close is final at 13:00.
    half_day = {**intraday, "currentTradingPeriod": {"regular": {"end": pd.Timestamp("2026-11-04 13:00", tz="America/New_York")}}}
    assert session_closed(hist, date(2026, 11, 4), half_day)


def test_yahoo_sentinel_iv_is_not_a_reading():
    assert [_clean_iv(x) for x in (1e-05, 0.0, float("nan"), MIN_PLAUSIBLE_IV, 0.30)] == [None, None, None, MIN_PLAUSIBLE_IV, 0.30]


def test_t1_cache_returns_the_latest_good_prior_snapshot(tmp_path):
    db = tmp_path / "market.sqlite"
    snap, surf = load_fixture("flat_only")
    assert upsert_snapshot(replace(snap, as_of="2026-09-16"), surf, path=db)
    assert not upsert_snapshot(replace(snap, as_of="2026-09-17", iv_now=1e-05), surf, path=db)  # sentinel never cached
    # A sentinel row written by an older run is skipped on read too.
    bad = asdict(replace(snap, as_of="2026-09-17", iv_now=1e-05))
    with sqlite3.connect(db) as conn:
        conn.execute(
            "INSERT INTO snapshots VALUES (?,?,?,?,?,?,NULL)",
            (snap.ticker.upper(), snap.expiry, float(snap.strike), snap.option_type, "2026-09-17", json.dumps(bad)),
        )
    loaded, _ = load_t1(snap.ticker, snap.expiry, snap.strike, snap.option_type, "2026-09-18", path=db)
    assert loaded is not None and loaded.as_of == "2026-09-16" and loaded.iv_now == snap.iv_now
    same_day, _ = load_t1(snap.ticker, snap.expiry, snap.strike, snap.option_type, "2026-09-16", path=db)
    assert same_day is None


@pytest.mark.parametrize("raw, expected, rescaled", [(0.35, 0.0035, True), (4.5, 0.045, True), (0.0101, 0.0101, False), (0.0, 0.0, False), (-1.0, 0.0, None)])
def test_yahoo_percent_dividend_yields_are_rescaled(raw, expected, rescaled):
    q, was_rescaled = normalize_dividend_yield(raw)
    assert q == pytest.approx(expected)
    if rescaled is not None:
        assert was_rescaled is rescaled


def test_hv20_proxy_shifts_prior_iv_by_the_realized_vol_change():
    rng = np.random.default_rng(0)
    returns = np.concatenate([rng.normal(0, 0.01, 20), rng.normal(0, 0.03, 19)])
    hv_now, hv_prev = hv20_from_closes(100.0 * np.exp(np.cumsum(np.concatenate([[0.0], returns]))))
    assert hv_now > hv_prev
    iv_prev, shift = iv_prev_from_hv20(0.25, hv_now, hv_prev)
    assert iv_prev > 0 and shift == pytest.approx(hv_now - hv_prev)


def test_a_shifted_surface_never_goes_below_the_vol_floor():
    _, surface = load_fixture("calibration_ok")
    assert min(min(row) for row in parallel_shift_surface(surface, -0.50).matrix) >= 1e-4


# --- Real historical chains -----------------------------------------------------------------

AS_OF = date(2026, 1, 15)


@pytest.mark.parametrize(
    "bid, ask, expiration, outcome",
    [
        (4.99, 5.01, "2026-06-15", "tight"),
        (4.8, 5.2, "2026-06-15", "normal"),
        (4.5, 5.5, "2026-06-15", "wide"),
        (0.0, 1.0, "2026-06-15", "bid<=0"),
        (5.0, 5.0, "2026-06-15", "ask<=bid"),
        (0.01, 0.03, "2026-06-15", "mid<0.05"),
        (4.0, 7.0, "2026-06-15", "relative_spread>0.25"),
        (4.9, 5.1, "2026-01-18", "DTE 3 outside [7,180]"),
        (4.9, 5.1, "2026-08-15", "DTE 212 outside [7,180]"),
    ],
)
def test_chain_quotes_are_tiered_or_rejected_with_a_reason(bid, ask, expiration, outcome):
    row = {"expiration": expiration, "strike": 100.0, "call_put": "Call", "bid": bid, "ask": ask}
    result = quote_hygiene([row], as_of=AS_OF)
    got = result.kept[0]["quote_tier"] if result.kept else result.rejected[0][1]
    assert got == outcome
    assert result.volume_oi_check_applicable is False  # the source has no volume/OI columns


def _parity_rows(strikes, *, expiry="2026-07-15", q=0.10, S=100.0, r=0.04, T=0.5, sigma=0.30):
    rows = []
    for k in strikes:
        d1 = (math.log(S / k) + (r - q + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        call = S * math.exp(-q * T) * norm.cdf(d1) - k * math.exp(-r * T) * norm.cdf(d2)
        put = k * math.exp(-r * T) * norm.cdf(-d2) - S * math.exp(-q * T) * norm.cdf(-d1)
        rows += [{"expiration": expiry, "strike": k, "call_put": "Call", "mid": call}, {"expiration": expiry, "strike": k, "call_put": "Put", "mid": put}]
    return rows


def test_implied_borrow_is_recovered_from_put_call_parity():
    rows = _parity_rows([80.0, 90.0, 100.0, 110.0, 120.0]) + _parity_rows([90.0], expiry="2099-01-01")
    result = imply_borrow_rate(rows, spot=100.0, rate=0.04, expiry="2026-07-15", as_of=AS_OF)
    assert result.n_pairs_used == 5 and result.q_implied == pytest.approx(0.10, abs=1e-3)
    assert result.borrow_regime == "elevated"
    thin = imply_borrow_rate(_parity_rows([95.0, 100.0]), spot=100.0, rate=0.04, expiry="2026-07-15", as_of=AS_OF, fallback_dividend_yield=0.015)
    assert thin.borrow_unavailable and thin.q_implied == 0.015 and thin.borrow_regime == "normal"


# --- Input guards -----------------------------------------------------------------------------


def test_observation_continuity_is_a_precondition():
    assert classify_observation_status(reference_row_counts={"SPY": 0, "AAPL": 0}, contract_rows=0) is ObservationStatus.DAY_MISSING
    assert classify_observation_status(reference_row_counts={"SPY": 900}, contract_rows=0) is ObservationStatus.CONTRACT_MISSING
    assert classify_observation_status(reference_row_counts={"SPY": 900}, contract_rows=12) is ObservationStatus.OK
    continuity_gate(contract="X", status_t1=ObservationStatus.OK, status_t=ObservationStatus.OK, date_t1="a", date_t="b")
    with pytest.raises(NoComparableObservationError, match="No comparable observation. X was OK on a and CONTRACT_MISSING on b"):
        continuity_gate(contract="X", status_t1=ObservationStatus.OK, status_t=ObservationStatus.CONTRACT_MISSING, date_t1="a", date_t="b")


@pytest.mark.parametrize(
    "quote, failing",
    [
        ({"call_mid": 105.0, "call_strike": 90.0}, "call_mid <= spot * 1.01"),
        ({"put_mid": 100.0, "put_strike": 90.0}, "put_mid <= strike * exp(-r*T) * 1.01"),
        ({"call_mid": 8.0, "call_strike": 95.0}, None),
    ],
)
def test_single_contract_basis_bounds(quote, failing):
    result = check_basis_consistency(spot=100.0, rate=0.04, time_to_expiry_years=0.5, **quote)
    assert result.failing_invariant == failing and result.basis_mismatch_suspected == (failing is not None)


def test_a_prior_mark_under_its_lower_bound_is_a_data_break():
    """2026-11-04 AAPL 325C: the 11-03 mark met the 11-02 close."""
    stale = check_mark_bounds(aapl_nov20_call(325.0, stale_spot=True))
    assert stale.failing_check == "T-1 mark >= no-arbitrage lower bound"
    assert "mark 11.9500 on 2026-11-03" in stale.detail and "spot 338.32" in stale.detail
    assert check_mark_bounds(aapl_nov20_call(325.0, stale_spot=False)).ok


@pytest.mark.parametrize(
    "change, failing",
    [
        ({"option_price_now": 102.0}, "T mark <= no-arbitrage upper bound"),  # call above spot
        ({"option_type": "put", "option_price_now": 10.6, "option_price_prev": 0.5}, "T-1 mark >= no-arbitrage lower bound"),
        ({"option_type": "put", "option_price_now": 9.6, "option_price_prev": 10.6}, None),  # within half a spread of K - S
        ({"option_price_now": 0.0, "option_price_prev": 0.0}, None),  # no marks: nothing to check
    ],
)
def test_mark_bounds_both_sides(change, failing):
    snap = MarketSnapshot(
        ticker="X", option_type="call", strike=110.0, expiry="2027-01-15", spot_now=100.0, spot_prev=100.0,
        iv_now=0.30, iv_prev=0.30, option_price_now=2.0, option_price_prev=2.0, time_to_expiry_years=0.2,
        bid=10.5, ask=11.5, as_of="2026-11-04", prev_as_of="2026-11-03",
    )
    assert check_mark_bounds(replace(snap, **change)).failing_check == failing


def test_a_mark_calibrated_far_from_the_source_iv_is_a_data_break():
    """2026-11-04 AAPL 350C: inside its bounds, but the stale spot calibrates to 49% vs Yahoo's 25%."""
    for stale, failing in ((True, "T calibrated IV ~= quote-source IV"), (False, None)):
        snap = aapl_nov20_call(350.0, stale_spot=stale)
        assert check_mark_bounds(snap).ok
        diag = price_and_attribute(snap, config=FAST).diagnostics
        assert diag.mark_calibrated
        check = check_calibrated_iv(snap, iv_cal_now=diag.effective_iv_now, iv_cal_prev=diag.effective_iv_prev)
        assert check.failing_check == failing


def test_the_iv_cross_check_skips_what_carries_no_vol_information():
    snap = aapl_nov20_call(350.0, stale_spot=False)
    # Deep ITM: time value under 30% of the mark.
    deep = replace(snap, strike=300.0, option_price_now=50.0, option_price_prev=32.5)
    assert check_calibrated_iv(deep, iv_cal_now=0.60, iv_cal_prev=0.25).ok
    # A proxied prior IV is not a reading to compare against.
    proxy = replace(snap, iv_prev_source="hv20_proxy")
    assert check_calibrated_iv(proxy, iv_cal_now=snap.iv_now, iv_cal_prev=0.60).ok
    assert not check_calibrated_iv(snap, iv_cal_now=snap.iv_now, iv_cal_prev=0.60).ok


def test_chain_basis_bounds_catch_an_unadjusted_split():
    strikes = (17.5, 20, 22.5, 25, 27.5, 30, 32.5)
    four_x = check_basis_consistency(spot=25.0, rate=0.0, time_to_expiry_years=0.5, carried_strikes=[k * 4 for k in strikes], forward=25.0)
    eight_x = check_basis_consistency(spot=25.0, rate=0.0, time_to_expiry_years=0.5, carried_strikes=[k * 8 for k in strikes], forward=25.0)
    assert four_x.ok  # a 4-for-1 mis-basing sits inside the stated bounds (documented limit)
    assert eight_x.basis_mismatch_suspected


# --- News sources -------------------------------------------------------------------------------


def _execute(sources: dict, query: SearchQuery):
    return IntelRegistry(sources).execute(SearchPlan(queries=[query]), ticker="AAPL")


def test_news_sources_fail_soft():
    class Down:
        source_id = "yfinance_news"

        def search(self, query, *, ticker):
            raise RuntimeError("yahoo down")

    yahoo = SearchQuery(q="AAPL", source_id="yfinance_news")
    assert _execute({}, yahoo) == ([], ["yfinance_news"], [])  # unregistered: skipped
    assert _execute({"yfinance_news": Down()}, yahoo) == ([], [], ["yfinance_news"])  # raised: failed
    tavily = SearchQuery(q="AAPL IV", source_id="tavily", cue="vega")
    assert _execute({"tavily": TavilyNewsSource(api_key="")}, tavily) == ([], ["tavily"], [])  # no key
    reset_ticker_cache()
    sec = SearchQuery(q="AAPL 8-K", source_id="sec_8k", cue="residual")
    assert _execute({"sec_8k": SecEdgar8KSource(user_agent="")}, sec) == ([], ["sec_8k"], [])  # no User-Agent


def test_tavily_and_sec_parse_their_responses():
    class Client:
        def search(self, **kwargs):
            assert kwargs["topic"] == "news"
            return {"results": [{"title": "AAPL IV into earnings", "url": "https://example.com/iv", "source": "Reuters", "published_date": "2026-08-18"}]}

    hits, _, _ = _execute({"tavily": TavilyNewsSource(api_key="tvly-test", client=Client())}, SearchQuery(q="AAPL IV", source_id="tavily"))
    assert (hits[0].title, hits[0].publisher, hits[0].published) == ("AAPL IV into earnings", "Reuters", "2026-08-18")

    def fetch(url, headers):
        assert headers.get("User-Agent")
        if "company_tickers.json" in url:
            return {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}}
        return {
            "filings": {
                "recent": {
                    "form": ["10-Q", "8-K", "8-K/A"],
                    "filingDate": ["2026-08-01", "2026-08-15", "2026-08-10"],
                    "accessionNumber": ["0000320193-26-000001", "0000320193-26-000050", "0000320193-26-000040"],
                    "primaryDocDescription": ["Quarterly report", "Results of operations", "Amended current report"],
                    "primaryDocument": ["a.htm", "b.htm", "c.htm"],
                }
            }
        }

    reset_ticker_cache()
    sec = SecEdgar8KSource(user_agent="ExplainMyOption test@example.com", fetch_json=fetch)
    hits, skipped, failed = _execute({"sec_8k": sec}, SearchQuery(q="AAPL 8-K", source_id="sec_8k", limit=2))
    reset_ticker_cache()
    assert (skipped, failed, len(hits)) == ([], [], 2)
    assert hits[0].title == "Results of operations" and "sec.gov/Archives/edgar/data" in hits[0].link
