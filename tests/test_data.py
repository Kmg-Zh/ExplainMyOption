"""Inputs: market-data hygiene, real-chain quotes, input guards, search planning, news sources."""

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

from explain_my_option.data.cache import MIN_PLAUSIBLE_IV, load_t1, upsert_snapshot
from explain_my_option.data.dividends import normalize_dividend_yield
from explain_my_option.data.historical_chain import imply_borrow_rate, quote_hygiene
from explain_my_option.data.observation import (
    NoComparableObservationError,
    ObservationStatus,
    check_basis_consistency,
    classify_observation_status,
    continuity_gate,
)
from explain_my_option.data.realized import hv20_from_closes, iv_prev_from_hv20
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.data_loader import _clean_iv, latest_two_closes
from explain_my_option.intel.planner import CueQueryPlanner
from explain_my_option.intel.sec_edgar import SecEdgar8KSource, reset_ticker_cache
from explain_my_option.intel.sources import IntelRegistry, TavilyNewsSource
from explain_my_option.intel.types import SearchPlan, SearchQuery
from explain_my_option.pricing.surface import parallel_shift_surface
from explain_my_option.pricing.types import Greeks, MarketSnapshot, PnLAttribution, PricingDiagnostics, PricingResult

# --- Live market data ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "closes, expected",
    [([330.0, 331.5, 336.13, np.nan], (336.13, 331.5)), ([100.0, np.nan, 0.0, -1.0, 102.0, 103.0], (103.0, 102.0))],
    ids=["trailing NaN bar", "interior bad bars"],
)
def test_spot_comes_from_the_last_two_valid_closes(closes, expected):
    assert latest_two_closes(pd.DataFrame({"Close": closes})) == expected


def test_too_few_valid_closes_fails_with_the_real_cause():
    with pytest.raises(RuntimeError, match="fewer than 2 valid daily closes"):
        latest_two_closes(pd.DataFrame({"Close": [np.nan, 336.13, np.nan]}))


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


def test_chain_basis_bounds_catch_an_unadjusted_split():
    strikes = (17.5, 20, 22.5, 25, 27.5, 30, 32.5)
    four_x = check_basis_consistency(spot=25.0, rate=0.0, time_to_expiry_years=0.5, carried_strikes=[k * 4 for k in strikes], forward=25.0)
    eight_x = check_basis_consistency(spot=25.0, rate=0.0, time_to_expiry_years=0.5, carried_strikes=[k * 8 for k in strikes], forward=25.0)
    assert four_x.ok  # a 4-for-1 mis-basing sits inside the stated bounds (documented limit)
    assert eight_x.basis_mismatch_suspected


# --- Search planning ----------------------------------------------------------------------------


def _priced(*, delta=1.0, gamma=0.0, vega=0.1, theta=0.1, residual=0.1, d_spot=1.0, d_vol=0.0, prices=(5.0, 4.5)):
    snap = MarketSnapshot(
        ticker="AAPL", option_type="call", strike=100.0, expiry="2026-12-18", spot_now=100.0 + d_spot, spot_prev=100.0,
        iv_now=0.30, iv_prev=0.30, option_price_now=prices[0], option_price_prev=prices[1], time_to_expiry_years=0.25,
        data_source="synthetic",
    )
    greeks = Greeks(price=4.5, delta=0.5, gamma=0.02, vega=0.1, theta=-0.04)
    pnl = PnLAttribution(
        total_pnl=delta + gamma + vega + theta + residual, delta_pnl=delta, gamma_pnl=gamma, vega_pnl=vega,
        theta_pnl=theta, residual_pnl=residual, d_spot=d_spot, d_vol=d_vol,
    )
    return snap, PricingResult(greeks, greeks, pnl, PricingDiagnostics(data_source="synthetic", exercise_style="american"))


def _cues(**kwargs) -> list[str]:
    return [q.cue for q in CueQueryPlanner().plan(*_priced(**kwargs)).queries]


def test_planner_searches_only_material_reliable_moves():
    plan = CueQueryPlanner().plan(*_priced())
    assert [(q.source_id, q.cue) for q in plan.queries] == [("yfinance_news", "material")]
    quiet = CueQueryPlanner().plan(*_priced(delta=0.05, vega=0.02, theta=0.04, residual=0.01, prices=(4.52, 4.50)))
    assert quiet.queries == [] and quiet.skip_reason == "below_materiality"
    locked = CueQueryPlanner().plan(*_priced(delta=2.0), observation_reliable=False)
    assert locked.queries == [] and locked.skip_reason == "observation_lock"


@pytest.mark.parametrize(
    "factors, cue",
    [
        ({"vega": 2.0, "delta": 0.1}, "vega"),
        ({"delta": 5.0, "d_vol": -0.20}, "vega"),  # a large IV move even when vega is not the biggest share
        ({"residual": 2.0, "delta": 0.1}, "residual"),  # 8-K
        ({"delta": 5.0, "residual": 2.0, "d_spot": -30.0}, "microstructure"),
    ],
)
def test_planner_adds_bounded_cue_queries(factors, cue):
    cues = _cues(**factors)
    assert cues[0] == "material" and cue in cues and len(cues) <= 3


def test_planner_respects_the_query_cap():
    plan = CueQueryPlanner(max_queries=1).plan(*_priced(delta=0.1, vega=2.0, residual=2.0))
    assert [q.cue for q in plan.queries] == ["material"]


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
