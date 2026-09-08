"""Risk-free rate from Yahoo ^IRX (13-week T-bill). Fail soft to 4.5%."""

from __future__ import annotations

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
        # ^IRX is quoted in percent (e.g. 5.15 → 0.0515).
        rate = last / 100.0 if last > 1.0 else last
        if rate > 0.25:
            return DEFAULT_RATE, "default"
        return float(rate), "irx"
    except Exception:
        return DEFAULT_RATE, "default"
