"""Real historical option-chain adapter (Task A4).

Source: DoltHub `post-no-preference/options`, queried over its free HTTP SQL
API -- no `dolt` CLI, no auth, no bulk download. Schema, licence
(CC BY-SA 4.0) and coverage limits are recorded in `docs/dev/DATA_SOURCES.md`;
read that before trusting a new case built on this source.

Same port as ``YFinanceMarketLoader``/``FixtureMarketLoader``
(``graph.deps.MarketLoader``) -- the pricing layer, blotter and graph do not
know which source they are on. Unlike those two, a historical case needs an
explicit ``as_of`` (there is no "today" for a past date), so
``HistoricalChainMarketLoader`` takes ``as_of``/``prev_as_of`` at
construction, the same way ``FixtureMarketLoader`` takes a fixture name.
Set ``EMO_MARKET_SOURCE=historical`` to document that a run is on this path;
nothing reads that env var automatically because building the loader always
needs the two dates, which no generic env toggle can supply.

Known split/rename hazards for the symbols this source is actually used
with -- A3.5 itself asks for "a short cited comment block in the data
adapter (not a registry module)":

- **GME**: yfinance's historical ``Close`` is *always* split-adjusted, even
  with ``auto_adjust=False`` (that flag only toggles dividend adjustment,
  never split adjustment -- confirmed empirically, see
  `docs/dev/DATA_SOURCES.md`). GME did a 4-for-1 split on 2022-07-22
  (``yf.Ticker("GME").splits``). Any ``as_of`` before that split needs its
  yfinance close multiplied back up by the cumulative split ratio to match
  this source's as-traded strikes -- ``_as_traded_close()`` does this
  generically from yfinance's own split history, not a hardcoded GME
  constant. Verified: 19.1975 * 4 = 76.79, matching the independently
  confirmed as-traded close for 2021-01-25.
- **Meta/FB**: the 2022 chain here is stored under ticker ``FB``, but
  yfinance spot only resolves under ``META`` post-rename. Neither of the
  two verified cases (A4.5) touches this name; noted so a future case on
  it does not get silently mis-based.

A3.5's basis-consistency guard (``data.observation.check_basis_consistency``)
still runs on every case built here regardless of the above -- it is the
safety net for anything this comment block does not already know about.
"""

from __future__ import annotations

import json
import math
import ssl
import urllib.parse
import urllib.request
from dataclasses import dataclass, replace
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

from ..data_loader import LoadedData
from ..paths import CI_DIR as _CI_DIR
from ..pricing.config import EngineConfig
from ..pricing.calibrate import implied_vol_flat
from ..pricing.types import DiscreteDividend, MarketSnapshot, PricingSpec
from .observation import (
    NoComparableObservationError,
    ObservationStatus,
    check_basis_consistency,
    classify_observation_status,
)
from .rates import fetch_irx_rate_as_of

_API_BASE = "https://www.dolthub.com/api/v1alpha1/post-no-preference/options/master"
_REFERENCE_BASKET = ("SPY", "AAPL")  # + the case symbol itself, per A3.1
_HTTP_TIMEOUT_S = 75.0  # DoltHub's SQL API can take 50s+ for a full day's chain

_IV_CACHE_PATH = Path(".cache/explain-my-option/historical_iv.json")


def _ssl_context() -> ssl.SSLContext:
    # The stdlib urllib on this machine's Python.framework build has no CA
    # bundle wired in by default; certifi (already present transitively via
    # yfinance -> requests) supplies one without adding a new dependency.
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def _dolthub_query(sql: str) -> list[dict]:
    url = f"{_API_BASE}?q={urllib.parse.quote(sql)}"
    with urllib.request.urlopen(  # noqa: S310
        url, timeout=_HTTP_TIMEOUT_S, context=_ssl_context()
    ) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    status = payload.get("query_execution_status")
    if status != "Success":
        raise RuntimeError(
            f"DoltHub query failed ({status}): {payload.get('query_execution_message')}"
        )
    return payload.get("rows") or []


def _escape(s: str) -> str:
    return s.replace("'", "''")


def fetch_day_chain(ticker: str, on_date: str) -> list[dict]:
    """All rows for one symbol on one date -- every expiry/strike/right carried."""
    sql = (
        "SELECT date, act_symbol, expiration, strike, call_put, bid, ask, vol "
        f"FROM option_chain WHERE act_symbol='{_escape(ticker.upper())}' "
        f"AND date='{_escape(on_date)}'"
    )
    return _dolthub_query(sql)


def row_count(ticker: str, on_date: str) -> int:
    sql = (
        "SELECT COUNT(*) AS n FROM option_chain "
        f"WHERE act_symbol='{_escape(ticker.upper())}' AND date='{_escape(on_date)}'"
    )
    rows = _dolthub_query(sql)
    return int(rows[0]["n"]) if rows else 0


def classify_day(
    ticker: str, on_date: str, *, contract_rows: Optional[int] = None
) -> ObservationStatus:
    """A3.1: classify one date via a real reference-basket query against this source."""
    ticker_u = ticker.upper()
    basket = {
        sym: row_count(sym, on_date) for sym in _REFERENCE_BASKET if sym != ticker_u
    }
    basket[ticker_u] = row_count(ticker, on_date) if contract_rows is None else contract_rows
    return classify_observation_status(reference_row_counts=basket, contract_rows=basket[ticker_u])


def _as_traded_close(ticker: str, as_of: date, *, yf_module=None) -> float:
    """yfinance close, corrected for any split between ``as_of`` and today.

    See the module docstring's GME note for why this correction exists.
    """
    yf = yf_module
    if yf is None:
        import yfinance as yf  # type: ignore

    tk = yf.Ticker(ticker)
    hist = tk.history(
        start=(as_of - timedelta(days=7)).isoformat(),
        end=(as_of + timedelta(days=1)).isoformat(),
        auto_adjust=False,
    )
    if hist is None or hist.empty:
        raise ValueError(f"No yfinance price history for {ticker!r} around {as_of}.")
    close = float(hist["Close"].dropna().iloc[-1])

    factor = 1.0
    try:
        splits = tk.splits
    except Exception:
        splits = None
    if splits is not None and len(splits) > 0:
        for ex_ts, ratio in splits.items():
            try:
                ex_date = ex_ts.to_pydatetime().date()
            except Exception:
                continue
            if ex_date > as_of:
                factor *= float(ratio)
    return close * factor


def _historical_dividends(
    ticker: str, as_of: date, expiry: date, *, yf_module=None
) -> list[DiscreteDividend]:
    """Real dividends actually paid in (as_of, expiry] -- not a projection.

    Unlike ``data.dividends.project_dividends`` (which guesses forward from
    "today"), every date here is already in the past relative to "today",
    so yfinance's own recorded ``dividends`` series is exact history.
    """
    yf = yf_module
    if yf is None:
        import yfinance as yf  # type: ignore
    try:
        series = yf.Ticker(ticker).dividends
    except Exception:
        return []
    if series is None or len(series) == 0:
        return []
    out: list[DiscreteDividend] = []
    for ts, amt in series.items():
        try:
            ex_date = ts.to_pydatetime().date()
        except Exception:
            continue
        if as_of < ex_date <= expiry:
            out.append(DiscreteDividend(ex_date=ex_date.isoformat(), amount=float(amt)))
    return out


@dataclass
class HygieneResult:
    kept: list[dict]
    rejected: list[tuple[dict, str]]
    # DoltHub's option_chain has no volume/open_interest columns at all (its
    # "vol" column is implied volatility) -- A4.2's volume/OI check cannot
    # be evaluated against this source. Recorded, not silently skipped.
    volume_oi_check_applicable: bool = False


def quote_hygiene(
    rows: list[dict], *, as_of: date, min_dte: int = 7, max_dte: int = 180
) -> HygieneResult:
    """A4.2: reject with a logged reason code; tier the survivors."""
    kept: list[dict] = []
    rejected: list[tuple[dict, str]] = []
    for raw in rows:
        row = dict(raw)
        try:
            bid, ask = float(row["bid"]), float(row["ask"])
        except (TypeError, ValueError, KeyError):
            rejected.append((row, "unparseable bid/ask"))
            continue
        if not (bid > 0):
            rejected.append((row, "bid<=0"))
            continue
        if not (ask > bid):
            rejected.append((row, "ask<=bid"))
            continue
        mid = 0.5 * (bid + ask)
        if not (mid >= 0.05):
            rejected.append((row, "mid<0.05"))
            continue
        rel_spread = (ask - bid) / mid
        if not (rel_spread <= 0.25):
            rejected.append((row, "relative_spread>0.25"))
            continue
        try:
            exp_d = datetime.strptime(str(row["expiration"]), "%Y-%m-%d").date()
        except ValueError:
            rejected.append((row, "bad expiration"))
            continue
        dte = (exp_d - as_of).days
        if not (min_dte <= dte <= max_dte):
            rejected.append((row, f"DTE {dte} outside [{min_dte},{max_dte}]"))
            continue
        row["mid"] = mid
        row["rel_spread"] = rel_spread
        row["dte"] = dte
        row["quote_tier"] = (
            "tight" if rel_spread <= 0.05 else "normal" if rel_spread <= 0.15 else "wide"
        )
        kept.append(row)
    return HygieneResult(kept=kept, rejected=rejected)


def _borrow_regime(q: float) -> str:
    if q < 0.02:
        return "normal"
    if q <= 0.20:
        return "elevated"
    return "extreme"


@dataclass
class BorrowResult:
    q_implied: float
    n_pairs_used: int
    iqr: Optional[float]
    borrow_regime: str
    borrow_unavailable: bool


def imply_borrow_rate(
    rows: list[dict],
    *,
    spot: float,
    rate: float,
    expiry: str,
    as_of: date,
    fallback_dividend_yield: float = 0.0,
) -> BorrowResult:
    """A4.3: imply the borrow rate from put-call parity, BEFORE any arbitrage
    filter (a static filter with q=0 misreads an omitted borrow cost as bad
    data on a hard-to-borrow name).

    ``q_implied(K) = -(1/T) * ln[(C_mid - P_mid + K*exp(-r*T)) / S]``,
    median across strikes with both sides quoted.
    """
    exp_d = datetime.strptime(expiry, "%Y-%m-%d").date()
    T = max((exp_d - as_of).days, 1) / 365.0

    by_strike: dict[float, dict[str, float]] = {}
    for row in rows:
        if str(row["expiration"]) != expiry:
            continue
        try:
            k = float(row["strike"])
        except (TypeError, ValueError):
            continue
        mid = row.get("mid")
        if mid is None:
            try:
                bid, ask = float(row["bid"]), float(row["ask"])
            except (TypeError, ValueError):
                continue
            if not (bid > 0 and ask > bid):
                continue
            mid = 0.5 * (bid + ask)
        side = "call" if str(row["call_put"]).lower().startswith("c") else "put"
        by_strike.setdefault(k, {})[side] = float(mid)

    q_vals: list[float] = []
    for k, sides in by_strike.items():
        if "call" not in sides or "put" not in sides or k <= 0 or spot <= 0:
            continue
        c, p = sides["call"], sides["put"]
        inner = (c - p + k * math.exp(-rate * T)) / spot
        if inner <= 0:
            continue
        q_vals.append(-(1.0 / T) * math.log(inner))

    if len(q_vals) < 3:
        q = float(fallback_dividend_yield)
        return BorrowResult(
            q_implied=q,
            n_pairs_used=len(q_vals),
            iqr=None,
            borrow_regime=_borrow_regime(q),
            borrow_unavailable=True,
        )

    q_vals.sort()
    n = len(q_vals)
    median = q_vals[n // 2] if n % 2 else 0.5 * (q_vals[n // 2 - 1] + q_vals[n // 2])
    q1 = q_vals[n // 4]
    q3 = q_vals[(3 * n) // 4]
    return BorrowResult(
        q_implied=median,
        n_pairs_used=n,
        iqr=q3 - q1,
        borrow_regime=_borrow_regime(median),
        borrow_unavailable=False,
    )


def _load_iv_cache() -> dict:
    if not _IV_CACHE_PATH.is_file():
        return {}
    try:
        return json.loads(_IV_CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_iv_cache(cache: dict) -> None:
    _IV_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    _IV_CACHE_PATH.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")


def invert_iv_cached(
    *,
    ticker: str,
    on_date: str,
    expiry: str,
    strike: float,
    option_type: str,
    spec: PricingSpec,
    target_price: float,
    config: Optional[EngineConfig] = None,
) -> tuple[Optional[float], list[str]]:
    """A4.4: invert ``mid`` with the shipped American FDM engine via Brent,
    disk-cached by ``(ticker, date, expiry, strike, right)`` -- the
    expensive step; a bad cache key dominates runtime.

    Reuses ``pricing.calibrate.implied_vol_flat`` (the same Brent-on-FDM
    solver the product already ships for mark-to-model calibration) rather
    than a second, parallel implementation.
    """
    key = f"{ticker.upper()}|{on_date}|{expiry}|{strike}|{option_type}"
    cache = _load_iv_cache()
    if key in cache:
        entry = cache[key]
        return entry.get("vol"), list(entry.get("limitations") or [])

    vol, limitations = implied_vol_flat(spec, target_price, config=config)
    cache[key] = {"vol": vol, "limitations": limitations}
    _save_iv_cache(cache)
    return vol, limitations


@dataclass
class HistoricalChainMarketLoader:
    """A4.1: the historical-chain ``MarketLoader``.

    Constructed with the two dates a case needs (there is no "today" for a
    past contract) -- the same pattern ``FixtureMarketLoader`` uses for its
    fixture name. ``.load()`` still matches the shared ``MarketLoader``
    protocol so the pricing layer, blotter and graph don't know which
    source they're on.
    """

    as_of: str
    prev_as_of: str
    config: Optional[EngineConfig] = None

    def load(
        self,
        *,
        ticker: str,
        option_type: str,
        strike: Optional[float],
        expiry: Optional[str],
    ) -> LoadedData:
        if strike is None or expiry is None:
            raise ValueError(
                "HistoricalChainMarketLoader requires an explicit strike and "
                "expiry -- there is no 'nearest ATM' concept on a past date."
            )
        as_of_d = datetime.strptime(self.as_of, "%Y-%m-%d").date()
        prev_d = datetime.strptime(self.prev_as_of, "%Y-%m-%d").date()
        expiry_d = datetime.strptime(expiry, "%Y-%m-%d").date()

        rows_t1 = fetch_day_chain(ticker, self.prev_as_of)
        rows_t = fetch_day_chain(ticker, self.as_of)

        def _contract_row(rows: list[dict]) -> Optional[dict]:
            wanted_side = "Call" if option_type == "call" else "Put"
            for r in rows:
                if (
                    str(r["expiration"]) == expiry
                    and abs(float(r["strike"]) - float(strike)) < 1e-6
                    and str(r["call_put"]) == wanted_side
                ):
                    return r
            return None

        status_t1 = classify_day(
            ticker, self.prev_as_of, contract_rows=len(rows_t1)
        )
        status_t = classify_day(ticker, self.as_of, contract_rows=len(rows_t))
        contract_t1 = _contract_row(rows_t1) if status_t1 is ObservationStatus.OK else None
        contract_t = _contract_row(rows_t) if status_t is ObservationStatus.OK else None
        if contract_t1 is None and status_t1 is ObservationStatus.OK:
            status_t1 = ObservationStatus.CONTRACT_MISSING
        if contract_t is None and status_t is ObservationStatus.OK:
            status_t = ObservationStatus.CONTRACT_MISSING

        if status_t1 is not ObservationStatus.OK or status_t is not ObservationStatus.OK:
            raise NoComparableObservationError(
                contract=f"{ticker} {expiry} {strike}{option_type[0].upper()}",
                status_t1=status_t1,
                status_t=status_t,
                date_t1=self.prev_as_of,
                date_t=self.as_of,
            )

        spot_now = _as_traded_close(ticker, as_of_d)
        spot_prev = _as_traded_close(ticker, prev_d)

        rate_now, rate_now_src = fetch_irx_rate_as_of(as_of_d)
        rate_prev, _ = fetch_irx_rate_as_of(prev_d)

        hyg_t = quote_hygiene(rows_t, as_of=as_of_d)
        hyg_t1 = quote_hygiene(rows_t1, as_of=prev_d)

        div_now = _historical_dividends(ticker, as_of_d, expiry_d)

        borrow_now = imply_borrow_rate(
            hyg_t.kept, spot=spot_now, rate=rate_now, expiry=expiry, as_of=as_of_d
        )
        borrow_prev = imply_borrow_rate(
            hyg_t1.kept, spot=spot_prev, rate=rate_prev, expiry=expiry, as_of=prev_d
        )

        c_now = dict(contract_t)
        c_prev = dict(contract_t1)
        mid_now = 0.5 * (float(c_now["bid"]) + float(c_now["ask"]))
        mid_prev = 0.5 * (float(c_prev["bid"]) + float(c_prev["ask"]))

        # A3.5 runs on both dates -- a mis-based day is not guaranteed to be
        # t rather than t-1.
        T_now = max((expiry_d - as_of_d).days, 1) / 365.0
        T_prev = max((expiry_d - prev_d).days, 1) / 365.0
        for label, spot_i, rate_i, mid_i, T_i in (
            ("t", spot_now, rate_now, mid_now, T_now),
            ("t-1", spot_prev, rate_prev, mid_prev, T_prev),
        ):
            basis = check_basis_consistency(
                spot=spot_i,
                rate=rate_i,
                time_to_expiry_years=T_i,
                call_mid=mid_i if option_type == "call" else None,
                call_strike=strike if option_type == "call" else None,
                put_mid=mid_i if option_type == "put" else None,
                put_strike=strike if option_type == "put" else None,
            )
            if basis.basis_mismatch_suspected:
                raise ValueError(
                    f"Basis mismatch suspected for {ticker} {expiry} {strike} "
                    f"on {label}: {basis.failing_invariant} failed "
                    f"({basis.detail}). No correction applied; case aborted."
                )

        spec_now = PricingSpec(
            spot=spot_now,
            strike=float(strike),
            rate=rate_now,
            dividend_yield=borrow_now.q_implied,
            vol=0.5,
            expiry=expiry,
            eval_date=as_of_d,
            option_type=option_type,  # type: ignore[arg-type]
            exercise_style="american",
        )
        iv_now, lim_now = invert_iv_cached(
            ticker=ticker,
            on_date=self.as_of,
            expiry=expiry,
            strike=float(strike),
            option_type=option_type,
            spec=spec_now,
            target_price=mid_now,
            config=self.config,
        )

        spec_prev = replace(
            spec_now, eval_date=prev_d, rate=rate_prev, dividend_yield=borrow_prev.q_implied
        )
        iv_prev, lim_prev = invert_iv_cached(
            ticker=ticker,
            on_date=self.prev_as_of,
            expiry=expiry,
            strike=float(strike),
            option_type=option_type,
            spec=spec_prev,
            target_price=mid_prev,
            config=self.config,
        )

        if iv_now is None or iv_prev is None:
            raise ValueError(
                f"IV inversion failed for {ticker} {expiry} {strike}: "
                f"now={lim_now} prev={lim_prev}"
            )

        snapshot = MarketSnapshot(
            ticker=ticker.upper(),
            option_type=option_type,
            strike=float(strike),
            expiry=expiry,
            spot_now=spot_now,
            spot_prev=spot_prev,
            iv_now=iv_now,
            iv_prev=iv_prev,
            option_price_now=mid_now,
            option_price_prev=mid_prev,
            time_to_expiry_years=T_now,
            risk_free_rate=rate_now,
            dividend_yield=borrow_now.q_implied,
            discrete_dividends=div_now,
            exercise_style="american",
            data_source="historical",
            as_of=self.as_of,
            prev_as_of=self.prev_as_of,
            risk_free_rate_prev=rate_prev,
            iv_prev_source="chain_t1",
            bid=float(c_now["bid"]),
            ask=float(c_now["ask"]),
            mid=mid_now,
            risk_free_rate_source=rate_now_src,  # type: ignore[arg-type]
        )
        return LoadedData(snapshot=snapshot, news=[], surface=None, surface_prev=None)


_HISTORICAL_CASE_DIR = _CI_DIR / "fixtures" / "historical"


def load_historical_case(name: str, *, cases_root: Optional[Path] = None) -> MarketSnapshot:
    """Load a committed real-case slice written by ``scripts/fetch_chains.py``.

    Unlike ``data.synthetic.load_fixture`` (which always forces
    ``data_source="synthetic"``), this preserves whatever the slice's own
    JSON says -- these are real snapshots, not synthetic fixtures, and
    should keep reading as ``data_source="historical"``.
    """
    root = cases_root or _HISTORICAL_CASE_DIR
    path = root / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"Historical case slice not found: {path}. Run "
            f"'python scripts/fetch_chains.py {name}' to fetch it."
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    d = dict(payload["snapshot"])
    divs = [DiscreteDividend(ex_date=x["ex_date"], amount=float(x["amount"])) for x in d.get("discrete_dividends") or []]
    d["discrete_dividends"] = divs
    return MarketSnapshot(**d)
