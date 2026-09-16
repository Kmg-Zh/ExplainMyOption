"""Deterministic diagnostic tools for ``diagnostic_pass`` (no LLM)."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from ..pricing.analysis_api import compare_to_official, path_reprice, taylor_second_order
from ..pricing.config import EngineConfig
from ..pricing.types import MarketSnapshot, PricingResult, VolSurfaceData
from ..report.facts import _american_facts, _intrinsic
from ..report.reconciliation import build_reconciliation_facts


def reconcile_mark_vs_model(
    snap: MarketSnapshot,
    pricing: PricingResult,
) -> dict[str, Any]:
    rec = build_reconciliation_facts(snap, pricing)
    return {
        "mark_pnl_usd": rec.mark_pnl_usd,
        "model_pnl_usd": rec.model_pnl_usd,
        "model_vs_mark_gap_usd": rec.model_vs_mark_gap_usd,
        "gap_pct_of_model": rec.gap_pct_of_model,
        "mark_calibrated": rec.mark_calibrated,
    }


def quote_quality_and_noise_band(
    snap: MarketSnapshot,
    pricing: PricingResult,
) -> dict[str, Any]:
    rec = build_reconciliation_facts(snap, pricing)
    return {
        "quote_tier": rec.quote_tier,
        "spread_pct_mid": rec.spread_pct_mid,
        "iv_move_pts": rec.iv_move_pts,
        "iv_noise_band_pts": rec.iv_noise_band_pts,
        "iv_move_within_noise": rec.iv_move_within_noise,
        "observation_reliable": rec.observation_reliable,
        "deep_otm_itm": rec.deep_otm_itm,
    }


def run_compare_to_official(
    snap: MarketSnapshot,
    pricing: PricingResult,
    surface: Optional[VolSurfaceData],
    *,
    config: Optional[EngineConfig] = None,
) -> dict[str, Any]:
    cross = compare_to_official(snap, surface, config=config)
    return {
        "official_price": cross.official_price,
        "engine_used": cross.engine_used_for_official,
        "lsm_bs": cross.lsm_bs,
        "lsm_merton": cross.lsm_merton,
        "rel_diff_lsm_bs": cross.rel_diff,
        "limitations": cross.limitations,
    }


def run_taylor_second_order(
    snap: MarketSnapshot,
    pricing: PricingResult,
    *,
    config: Optional[EngineConfig] = None,
) -> dict[str, Any]:
    result = taylor_second_order(snap, pricing, config=config)
    return {
        "vanna": result.vanna,
        "volga": result.volga,
        "vanna_pnl": result.vanna_pnl,
        "volga_pnl": result.volga_pnl,
        "combined_pnl": result.combined_pnl,
        "residual_after": result.residual_after,
        "limitations": result.limitations,
    }


def run_path_reprice(
    snap: MarketSnapshot,
    pricing: PricingResult,
    surface: Optional[VolSurfaceData],
    *,
    config: Optional[EngineConfig] = None,
) -> dict[str, Any]:
    result = path_reprice(snap, pricing, surface=surface, config=config)
    return result.as_dict()


def american_dividend_exercise_check(
    snap: MarketSnapshot,
    pricing: PricingResult,
) -> dict[str, Any]:
    am = _american_facts(snap, pricing)
    intrinsic = _intrinsic(snap)
    itm = intrinsic > 0
    days_to_ex: int | None = None
    if am.next_ex_div and snap.as_of:
        try:
            ex = datetime.strptime(am.next_ex_div, "%Y-%m-%d").date()
            as_of = datetime.strptime(snap.as_of, "%Y-%m-%d").date()
            days_to_ex = (ex - as_of).days
        except ValueError:
            days_to_ex = None
    flag_window = days_to_ex is not None and 0 <= days_to_ex <= 30 and itm
    return {
        "exercise_style": am.exercise_style,
        "intrinsic": am.intrinsic,
        "time_value": am.time_value,
        "next_ex_div": am.next_ex_div,
        "next_div_amount": am.next_div_amount,
        "early_exercise_premium": am.early_exercise_premium,
        "dividend_pv_effect": am.dividend_pv_effect,
        "ee_premium_anomaly": am.ee_premium_anomaly,
        "early_exercise_assessment": am.early_exercise_assessment,
        "days_to_ex_div": days_to_ex,
        "flag_ex_div_window": flag_window,
        "dividend_coverage": am.dividend_coverage,
        "days_to_expiry": am.days_to_expiry,
        "ee_relevant": am.ee_relevant,
    }


_EE_MATERIAL_USD = 0.01


def ex_div_attribution_split(
    snap: MarketSnapshot,
    pricing: PricingResult,
) -> dict[str, Any]:
    """FO overlay: spot≈div, American−European premium, vol, residual.

    Does not change official American FDM Taylor PnL.
    """
    am = american_dividend_exercise_check(snap, pricing)
    d_spot = float(snap.spot_now - snap.spot_prev)
    div = am.get("next_div_amount")
    ee = am.get("early_exercise_premium")
    div_pv = am.get("dividend_pv_effect")
    div_f = float(div) if div is not None else None
    ee_f = float(ee) if ee is not None else None
    div_pv_f = float(div_pv) if div_pv is not None else None
    spot_vs_div = None
    if div_f is not None:
        spot_vs_div = d_spot + div_f
    am_price = float(pricing.greeks_now.price)
    eu_price = pricing.diagnostics.european_price
    eu_f = float(eu_price) if eu_price is not None else None
    am_minus_eu = (am_price - eu_f) if eu_f is not None else None
    return {
        "flag_ex_div_window": bool(am.get("flag_ex_div_window")),
        "spot_drop": d_spot,
        "dividend_amount": div_f,
        "spot_drop_vs_dividend": spot_vs_div,
        "american_price": am_price,
        "european_analytic_no_div": eu_f,
        "am_minus_eu": am_minus_eu,
        "ee_premium_now": ee_f,
        "dividend_pv_effect": div_pv_f,
        "ee_premium_anomaly": bool(am.get("ee_premium_anomaly")),
        "ee_premium_material": (
            ee_f is not None
            and ee_f >= _EE_MATERIAL_USD
            and not am.get("ee_premium_anomaly")
        ),
        "dividend_coverage": am.get("dividend_coverage"),
        "ee_relevant": am.get("ee_relevant"),
        "vega_pnl": float(pricing.pnl.vega_pnl),
        "residual_pnl": float(pricing.pnl.residual_pnl),
        "note": (
            "FO overlay on official American FDM Taylor — not a trading edge. "
            "LSM/Heston stay diagnostic-only."
        ),
    }
