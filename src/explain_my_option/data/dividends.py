"""Best-effort discrete dividend schedule from yfinance (inferred if needed)."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from ..pricing.types import DiscreteDividend

# Yahoo `info.dividendYield` is sometimes a percent-as-fraction (0.35 = 0.35%)
# rather than a decimal yield (0.0035). US mega-cap / ETF demo names are well
# below 15%; treat anything above that as the Yahoo percent form.
YIELD_PERCENT_AS_FRACTION_CUT = 0.15


def normalize_dividend_yield(raw: float) -> tuple[float, bool]:
    """Return ``(decimal_yield, rescaled)``.

    Rules, applied once:
    - non-finite / negative → ``(0.0, False)``
    - ``q > 1`` → divide by 100 (e.g. 4.5 → 4.5%)
    - then ``q > 0.15`` → divide by 100 (e.g. 0.35 → 0.35%)
    """
    try:
        q = float(raw)
    except (TypeError, ValueError):
        return 0.0, False
    if q != q or q < 0.0:
        return 0.0, False
    original = q
    if q > 1.0:
        q = q / 100.0
    if q > YIELD_PERCENT_AS_FRACTION_CUT:
        q = q / 100.0
    return float(q), q != original


def _to_date(val) -> Optional[date]:
    if val is None:
        return None
    if isinstance(val, date) and not isinstance(val, datetime):
        return val
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, (int, float)):
        try:
            return datetime.utcfromtimestamp(int(val)).date()
        except Exception:
            return None
    if isinstance(val, str) and val:
        try:
            return datetime.strptime(val[:10], "%Y-%m-%d").date()
        except Exception:
            return None
    # pandas Timestamp
    try:
        return val.to_pydatetime().date()  # type: ignore[union-attr]
    except Exception:
        return None


def project_dividends(
    ticker_obj,
    *,
    as_of: date,
    expiry: date,
    info: Optional[dict] = None,
) -> tuple[list[DiscreteDividend], bool]:
    """Return (schedule, inferred). At most the next two cash amounts before expiry."""
    inferred = False
    out: list[DiscreteDividend] = []
    hist_amt: Optional[float] = None
    last_ex: Optional[date] = None
    try:
        series = ticker_obj.dividends
        if series is not None and len(series) > 0:
            last = series.dropna().iloc[-1]
            hist_amt = float(last)
            last_ex = _to_date(series.dropna().index[-1])
    except Exception:
        pass

    info = info or {}
    try:
        last_amt = info.get("lastDividendValue")
        if last_amt is not None and float(last_amt) > 0:
            hist_amt = float(last_amt)
    except Exception:
        pass
    ex_info = _to_date(info.get("exDividendDate"))

    amount = hist_amt
    if amount is None or amount <= 0:
        return [], False

    # Next ex-date: info first, else +90d from last historical ex.
    next_ex = ex_info
    if next_ex is None or next_ex <= as_of:
        if last_ex is not None:
            next_ex = last_ex + timedelta(days=90)
            inferred = True
        else:
            next_ex = as_of + timedelta(days=30)
            inferred = True
    if next_ex <= as_of:
        next_ex = as_of + timedelta(days=30)
        inferred = True

    candidates = [next_ex, next_ex + timedelta(days=90)]
    for d in candidates:
        if as_of < d <= expiry:
            out.append(DiscreteDividend(ex_date=d.isoformat(), amount=float(amount)))
    if out and (ex_info is None or inferred):
        inferred = True
    return out[:2], inferred
