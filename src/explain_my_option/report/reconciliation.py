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
    # A6.1: the two residuals, named separately.
    # residual_method = pnl.residual_pnl unchanged (ΔP_model - Taylor
    # components) -- arithmetic, never news. residual_model =
    # ΔP_market - ΔP_model, the only quantity a catalyst may explain; None
    # without reliable marks on both dates.
    residual_method_usd: float
    residual_model_usd: float | None
    marks_reliable_now: bool
    marks_reliable_prev: bool
    # A6.2: which residual actually drives escalation this run.
    escalation_basis: str  # "model" | "method"
    escalation_metric_pct: float


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


def marks_reliable(quote_tier: str | None) -> bool:
    """A6.2: quote tier in {tight, normal} -- data.historical_chain's
    vocabulary -- or this module's own "reliable" label, so both feed the
    same gate. None (unknown/never verified) is never reliable."""
    return quote_tier in ("tight", "normal", "reliable")


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

    # A6.1/A6.2: the two residuals, and which one drives escalation.
    # Scaled by position size (quantity * multiplier), matching model_pnl/
    # mark_pnl above -- residual_method_usd is a blotter dollar figure, not
    # the raw per-option pnl.residual_pnl.
    residual_method = float(pnl.residual_pnl) * scale
    residual_model = (mark_pnl - model_pnl) if mark_pnl is not None else None
    tier_now = snap.quote_tier_now if snap.quote_tier_now is not None else tier
    tier_prev = snap.quote_tier_prev
    reliable_now = marks_reliable(tier_now)
    reliable_prev = marks_reliable(tier_prev)
    if reliable_now and reliable_prev and mark_pnl is not None and abs(mark_pnl) > 1e-12:
        escalation_basis = "model"
        escalation_metric_pct = 100.0 * abs(residual_model or 0.0) / abs(mark_pnl)
    else:
        escalation_basis = "method"
        escalation_metric_pct = (
            100.0 * abs(residual_method) / abs(model_pnl) if abs(model_pnl) > 1e-12 else 0.0
        )

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
        residual_method_usd=residual_method,
        residual_model_usd=residual_model,
        marks_reliable_now=reliable_now,
        marks_reliable_prev=reliable_prev,
        escalation_basis=escalation_basis,
        escalation_metric_pct=escalation_metric_pct,
    )
