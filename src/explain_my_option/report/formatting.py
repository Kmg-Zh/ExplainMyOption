"""Number and label formatting shared by every report section."""

from __future__ import annotations

from ..pricing.types import MarketSnapshot

# A percentage over a near-zero denominator (a residual over a ~$0 move) would
# print as an absurd figure. Only the displayed text is clamped; routing and
# escalation use the raw numbers.
PCT_DISPLAY_CAP = 1000.0


def money(x: float) -> str:
    """Signed dollars to four decimals, e.g. ``+$1.2345`` or ``-$0.0100``."""
    sign = "+" if x >= 0 else "-"
    return f"{sign}${abs(x):,.4f}"


def pct(x: float, *, signed: bool = True) -> str:
    """One-decimal percent; ``>1000%`` when the denominator was near zero."""
    if abs(x) > PCT_DISPLAY_CAP:
        sign = "-" if x < 0 else ("+" if signed else "")
        return f"{sign}>{PCT_DISPLAY_CAP:.0f}%"
    return f"{x:+.1f}%" if signed else f"{x:.1f}%"


def num(x: float, dp: int = 4) -> str:
    return f"{x:,.{dp}f}"


def contract_id(snap: MarketSnapshot) -> str:
    right = "C" if snap.option_type.lower().startswith("c") else "P"
    return f"{snap.ticker} {snap.strike:g}{right} {snap.expiry}"
