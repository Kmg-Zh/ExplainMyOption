"""Mark-vs-model reconciliation and quote-quality checks (desk conventions).

Shared by the product report, ``diagnostic_pass`` tools, and ``tests/live_book/desk_pnl.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..pricing.types import MarketSnapshot, PricingResult

# Desk thresholds — tune freely; not derived from the pricing engine.
WIDE_SPREAD_PCT_MID = 0.15
THIN_VOLUME = 10
THIN_OPEN_INTEREST = 50
MIN_TOTAL_USD_FOR_PCT = 5.0
VEGA_ZERO_EPS = 1e-9


@dataclass
class ReconciliationFacts:
    quote_tier: str
    spread: float | None
    spread_pct_mid: float | None
    iv_move_pts: float
    iv_noise_band_pts: float | None
    iv_move_within_noise: bool | None
    mark_pnl_usd: float | None
    model_pnl_usd: float
    model_vs_mark_gap_usd: float | None
    gap_pct_of_model: float | None
    mark_calibrated: bool
    observation_reliable: bool
    deep_otm_itm: bool
    pct_uses_abs_share: bool


def quote_tier(
    spread_pct_mid: float | None,
    volume: float | None,
    open_interest: float | None,
) -> str:
    if spread_pct_mid is None:
        return "unquoted"
    wide = spread_pct_mid > WIDE_SPREAD_PCT_MID
    thin = (volume or 0) < THIN_VOLUME or (open_interest or 0) < THIN_OPEN_INTEREST
    if wide and thin:
        return "wide+thin"
    if wide:
        return "wide"
    if thin:
        return "thin"
    return "reliable"


def iv_noise_band_pts(spread: float | None, vega_per_vol_point: float) -> float | None:
    if spread is None or abs(vega_per_vol_point) <= VEGA_ZERO_EPS:
        return None
    return (spread / 2.0) / abs(vega_per_vol_point)


def build_reconciliation_facts(
    snap: MarketSnapshot,
    pricing: PricingResult,
) -> ReconciliationFacts:
    """Derive mark reconciliation and quote-quality flags for one position."""
    scale = snap.position_scale()
    pnl = pricing.pnl
    g_now = pricing.greeks_now

    bid, ask = snap.bid, snap.ask
    mid = snap.mid
    if mid is None and bid is not None and ask is not None and bid > 0 and ask > 0:
        mid = 0.5 * (bid + ask)
    spread = (ask - bid) if (bid is not None and ask is not None) else None
    spread_pct_mid = (spread / mid) if (spread is not None and mid) else None
    tier = quote_tier(spread_pct_mid, snap.volume, snap.open_interest)

    iv_move_pts = (snap.iv_now - snap.iv_prev) * 100.0
    vega_now = float(g_now.vega)
    deep_otm_itm = abs(g_now.delta) >= 0.95 or abs(g_now.delta) <= 0.05
    noise_pts = iv_noise_band_pts(spread, vega_now)
    within_noise: bool | None = None
    if noise_pts is not None:
        within_noise = abs(iv_move_pts) <= noise_pts

    model_pnl = float(pnl.total_pnl) * scale
    mark_pnl: float | None = None
    gap: float | None = None
    gap_pct: float | None = None
    if snap.option_price_now > 0 and snap.option_price_prev > 0:
        mark_unit = float(snap.option_price_now) - float(snap.option_price_prev)
        mark_pnl = mark_unit * scale
        gap = model_pnl - mark_pnl
        if abs(model_pnl) > 1e-9:
            gap_pct = 100.0 * gap / model_pnl

    mark_cal = bool(pricing.diagnostics.mark_calibrated)
    reliable_tier = tier == "reliable"
    observation_reliable = reliable_tier and not (within_noise is True) and not deep_otm_itm

    total_abs = abs(model_pnl)
    pct_uses_abs_share = total_abs < MIN_TOTAL_USD_FOR_PCT

    return ReconciliationFacts(
        quote_tier=tier,
        spread=spread,
        spread_pct_mid=spread_pct_mid,
        iv_move_pts=iv_move_pts,
        iv_noise_band_pts=noise_pts,
        iv_move_within_noise=within_noise,
        mark_pnl_usd=mark_pnl,
        model_pnl_usd=model_pnl,
        model_vs_mark_gap_usd=gap,
        gap_pct_of_model=gap_pct,
        mark_calibrated=mark_cal,
        observation_reliable=observation_reliable,
        deep_otm_itm=deep_otm_itm,
        pct_uses_abs_share=pct_uses_abs_share,
    )
