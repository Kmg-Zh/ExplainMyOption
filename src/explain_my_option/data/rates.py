"""Risk-free rate from Yahoo ^IRX (13-week T-bill). Fail soft to 4.5%."""

from __future__ import annotations

from datetime import date, datetime, timedelta

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
        # ^IRX is always quoted in percent (5.15 -> 0.0515), including in
        # near-zero regimes where it prints below 1.0 (0.07 -> 0.0007).
        rate = last / 100.0
        if rate > 0.25:
            return DEFAULT_RATE, "default"
        return float(rate), "irx"
    except Exception:
        return DEFAULT_RATE, "default"


def fetch_irx_rate_as_of(as_of: date, yf_module=None) -> tuple[float, str]:
    """``^IRX`` close on or just before ``as_of`` (the rate on a past date).

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
