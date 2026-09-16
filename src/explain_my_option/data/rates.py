"""Risk-free rate from Yahoo ^IRX (13-week T-bill). Fail soft to 4.5%."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

DEFAULT_RATE = 0.045


def fetch_irx_rate(yf_module=None) -> tuple[float, str]:
    """Return ``(rate_decimal, source)`` with ``source`` in {irx, default}."""
    try:
        yf = yf_module
        if yf is None:
            import yfinance as yf  # type: ignore
        hist = yf.Ticker("^IRX").history(period="10d", auto_adjust=False)
        if hist is None or hist.empty:
            return DEFAULT_RATE, "default"
        last = float(hist["Close"].dropna().iloc[-1])
        if not (last == last) or last <= 0:
            return DEFAULT_RATE, "default"
        # ^IRX is always quoted in percent (e.g. 5.15 -> 0.0515), including
        # during near-zero-rate regimes where the index itself prints below
        # 1.0 (e.g. 0.07 -> 0.0007, not 0.07). Found via fetch_irx_rate_as_of
        # returning 7% for GME 2021-01-25 instead of the correct ~0.08%
        # (docs/dev/DATA_SOURCES.md's independently-verified r=0.0008) --
        # the old "only divide if last > 1.0" guard was wrong, not defensive.
        rate = last / 100.0
        if rate > 0.25:
            return DEFAULT_RATE, "default"
        return float(rate), "irx"
    except Exception:
        return DEFAULT_RATE, "default"


def fetch_irx_rate_as_of(as_of: date, yf_module=None) -> tuple[float, str]:
    """``^IRX`` close on or just before ``as_of`` (Task A4: historical rate).

    Widens the window backward up to 10 trading days to survive holidays;
    fails soft to the default the same way ``fetch_irx_rate`` does.
    """
    try:
        yf = yf_module
        if yf is None:
            import yfinance as yf  # type: ignore
        start = (as_of - timedelta(days=14)).isoformat()
        end = (as_of + timedelta(days=1)).isoformat()
        hist = yf.Ticker("^IRX").history(start=start, end=end, auto_adjust=False)
        if hist is None or hist.empty:
            return DEFAULT_RATE, "default"
        closes = hist["Close"].dropna()
        if closes.empty:
            return DEFAULT_RATE, "default"
        as_of_dt = datetime(as_of.year, as_of.month, as_of.day)
        idx = closes.index
        try:
            idx_naive = idx.tz_localize(None)
        except TypeError:
            idx_naive = idx
        mask = idx_naive <= as_of_dt
        eligible = closes[mask] if mask.any() else closes
        last = float(eligible.iloc[-1])
        if not (last == last) or last <= 0:
            return DEFAULT_RATE, "default"
        rate = last / 100.0
        if rate > 0.25:
            return DEFAULT_RATE, "default"
        return float(rate), "irx"
    except Exception:
        return DEFAULT_RATE, "default"
