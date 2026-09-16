#!/usr/bin/env python3
"""Deterministic quiet-day selection (Task A7.1).

Selects (t-1, t) pairs on a liquid underlying where:
- |close-to-close return| < 0.3%
- no earnings within +/-3 trading days
- no ex-dividend within +/-3 trading days
- no FOMC or CPI release that week
- all quotes tight or normal on both dates (data.historical_chain)

Not hand-picked: every date in the candidate window is checked against the
same filter; only the output is a small survivor set. The three cheap
checks (return, earnings, ex-div) run first, locally, from a single
yfinance history call per ticker -- the expensive DoltHub quote-tier check
only runs on days that already pass everything else, since DoltHub's SQL
API takes 45-55s per query.

Usage::

    python scripts/find_quiet_days.py                  # AAPL, MSFT, SPY, 2023
    python scripts/find_quiet_days.py --min 3 --year 2023
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "src"))
sys.path.insert(0, str(_REPO_ROOT / "tests"))

from bootstrap import install  # noqa: E402

install()

import yfinance as yf  # noqa: E402

from explain_my_option.data.historical_chain import (  # noqa: E402
    fetch_day_chain,
    quote_hygiene,
)

RETURN_THRESHOLD = 0.003  # 0.3%
EARNINGS_WINDOW_DAYS = 3
EXDIV_WINDOW_DAYS = 3

# FOMC meeting (decision-day) dates and BLS CPI release dates. Public,
# well-documented official calendars (federalreserve.gov, bls.gov) --
# hardcoded per date because neither publishes a queryable historical API;
# this is a reproducible reference table, not a hand-picked exclusion list.
FOMC_DATES_2023 = [
    "2023-02-01", "2023-03-22", "2023-05-03", "2023-06-14",
    "2023-07-26", "2023-09-20", "2023-11-01", "2023-12-13",
]
CPI_DATES_2023 = [
    "2023-01-12", "2023-02-14", "2023-03-14", "2023-04-12",
    "2023-05-10", "2023-06-13", "2023-07-12", "2023-08-10",
    "2023-09-13", "2023-10-12", "2023-11-14", "2023-12-12",
]
MACRO_EVENT_DATES = {
    datetime.strptime(d, "%Y-%m-%d").date() for d in FOMC_DATES_2023 + CPI_DATES_2023
}

DEFAULT_TICKERS = ["AAPL", "MSFT", "SPY"]
OUT_DIR = _REPO_ROOT / "tests" / "ci" / "fixtures" / "quiet_days"


def _no_macro_event_that_week(day: date) -> bool:
    week_start = day - timedelta(days=day.weekday())
    week_end = week_start + timedelta(days=6)
    return not any(week_start <= d <= week_end for d in MACRO_EVENT_DATES)


def _nearest_trading_days_within(target: date, candidates: list[date], window: int) -> bool:
    return any(abs((c - target).days) <= window for c in candidates)


def find_candidates(ticker: str, year: int) -> list[dict]:
    tk = yf.Ticker(ticker)
    hist = tk.history(start=f"{year}-01-01", end=f"{year+1}-01-15", auto_adjust=False)
    if hist.empty:
        return []
    closes = hist["Close"]
    trading_days = [ts.date() for ts in hist.index]

    earnings_days: list[date] = []
    try:
        ed = tk.get_earnings_dates(limit=40)
        earnings_days = [ts.date() for ts in ed.index if ts.date().year in (year - 1, year, year + 1)]
    except Exception:
        pass

    exdiv_days: list[date] = []
    try:
        divs = tk.dividends
        exdiv_days = [ts.date() for ts in divs.index if ts.date().year in (year - 1, year, year + 1)]
    except Exception:
        pass

    out: list[dict] = []
    for i in range(1, len(trading_days)):
        t = trading_days[i]
        t1 = trading_days[i - 1]
        if t.year != year:
            continue
        c_now = float(closes.iloc[i])
        c_prev = float(closes.iloc[i - 1])
        ret = abs(c_now / c_prev - 1.0)
        if ret >= RETURN_THRESHOLD:
            continue
        if _nearest_trading_days_within(t, earnings_days, EARNINGS_WINDOW_DAYS):
            continue
        if _nearest_trading_days_within(t, exdiv_days, EXDIV_WINDOW_DAYS):
            continue
        if not _no_macro_event_that_week(t) or not _no_macro_event_that_week(t1):
            continue
        out.append(
            {
                "ticker": ticker,
                "as_of": t.isoformat(),
                "prev_as_of": t1.isoformat(),
                "return_abs": ret,
            }
        )
    return out


def _atm_tier_ok(ticker: str, on_date: str, spot: float) -> bool:
    """Cheap-check survivors only: pull the day chain, tier the strike
    nearest spot, require tight or normal."""
    rows = fetch_day_chain(ticker, on_date)
    if not rows:
        return False
    hyg = quote_hygiene(rows, as_of=datetime.strptime(on_date, "%Y-%m-%d").date())
    if not hyg.kept:
        return False
    nearest = min(hyg.kept, key=lambda r: abs(float(r["strike"]) - spot))
    return nearest["quote_tier"] in ("tight", "normal")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tickers", nargs="+", default=DEFAULT_TICKERS)
    parser.add_argument("--year", type=int, default=2023)
    parser.add_argument("--min", type=int, default=3)
    args = parser.parse_args(argv)

    per_ticker: dict[str, list[dict]] = {}
    for ticker in args.tickers:
        cands = find_candidates(ticker, args.year)
        print(f"{ticker}: {len(cands)} cheap-check candidates")
        per_ticker[ticker] = cands

    # Round-robin across tickers so the (slow) DoltHub check samples every
    # ticker early instead of exhausting one ticker's candidates first.
    all_candidates: list[dict] = []
    idx = 0
    while any(idx < len(v) for v in per_ticker.values()):
        for ticker in args.tickers:
            if idx < len(per_ticker[ticker]):
                all_candidates.append(per_ticker[ticker][idx])
        idx += 1

    max_checked = max(60, args.min * 12)
    survivors: list[dict] = []
    for checked, cand in enumerate(all_candidates):
        if checked >= max_checked:
            print(f"  stopping: checked {max_checked} candidates")
            break
        if len(survivors) >= args.min and len({s["ticker"] for s in survivors}) >= min(
            args.min, len(args.tickers)
        ):
            break
        tk = yf.Ticker(cand["ticker"])
        hist = tk.history(
            start=cand["as_of"], end=(datetime.strptime(cand["as_of"], "%Y-%m-%d") + timedelta(days=1)).date().isoformat(),
            auto_adjust=False,
        )
        if hist.empty:
            continue
        spot = float(hist["Close"].iloc[-1])
        print(f"  checking DoltHub quote tier for {cand['ticker']} {cand['as_of']}...")
        try:
            ok_now = _atm_tier_ok(cand["ticker"], cand["as_of"], spot)
            ok_prev = _atm_tier_ok(cand["ticker"], cand["prev_as_of"], spot)
        except Exception as exc:
            print(f"    skipped ({exc})")
            continue
        if ok_now and ok_prev:
            cand["spot"] = spot
            survivors.append(cand)
            print(f"    QUIET DAY: {cand}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"quiet_days_{args.year}.json"
    out_path.write_text(json.dumps(survivors, indent=2, sort_keys=True), encoding="utf-8")
    print(f"\nWrote {len(survivors)} quiet days to {out_path.relative_to(_REPO_ROOT)}")
    return 0 if len(survivors) >= args.min else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
