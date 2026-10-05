"""Analysis-only pricing API for later LLM tools. Not called by quant_node."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from .config import EngineConfig, MertonParams, default_merton_params
from .engines.lsm import price_lsm_bs, price_lsm_merton
from .engines.merton import merton_european_series, price_merton_european
from .facade import price_and_attribute
from .ql_engine import _day_count, _parse_iso, _to_ql_date
from .types import (
    CrossCheckResult,
    MarketSnapshot,
    PricingResult,
    PricingSpec,
    SecondOrderTaylorResult,
    SequentialRevalResult,
    VolSurfaceData,
)


def _eval_date(snapshot: MarketSnapshot) -> date:
    if snapshot.as_of:
        return datetime.strptime(snapshot.as_of, "%Y-%m-%d").date()
    return date.today()


def _spec_now(
    snapshot: MarketSnapshot,
    surface: Optional[VolSurfaceData] = None,
) -> PricingSpec:
    return PricingSpec(
        spot=snapshot.spot_now,
        strike=snapshot.strike,
        rate=snapshot.risk_free_rate,
        dividend_yield=snapshot.dividend_yield,
        vol=snapshot.iv_now,
        expiry=snapshot.expiry,
        eval_date=_eval_date(snapshot),
        option_type=snapshot.option_type,  # type: ignore[arg-type]
        exercise_style=snapshot.exercise_style,
        discrete_dividends=snapshot.discrete_dividends,
        surface=surface,
    )


def _year_frac(snapshot: MarketSnapshot) -> float:
    return max(
        _day_count().yearFraction(
            _to_ql_date(_eval_date(snapshot)), _parse_iso(snapshot.expiry)
        ),
        1.0 / 365.0,
    )


def calibrate_merton(
    snapshot: MarketSnapshot,
    surface: Optional[VolSurfaceData],
) -> tuple[MertonParams, list[str]]:
    """Cheap 1-parameter λ fit to the contract's European BS price; else defaults."""
    base = default_merton_params()
    if surface is None:
        return base, ["merton_params_defaulted"]
    t = _year_frac(snapshot)
    from .ql_engine import price_european_flat

    target = price_european_flat(
        spot=snapshot.spot_now,
        strike=snapshot.strike,
        rate=snapshot.risk_free_rate,
        dividend_yield=snapshot.dividend_yield,
        vol=snapshot.iv_now,
        expiry=snapshot.expiry,
        eval_date=_eval_date(snapshot),
        option_type=snapshot.option_type,  # type: ignore[arg-type]
        discrete_dividends=snapshot.discrete_dividends,
    ).price
    best = base
    best_err = float("inf")
    for lam in (0.1, 0.3, 0.5, 0.8, 1.2):
        cand = MertonParams(
            jump_intensity=lam,
            jump_mean=base.jump_mean,
            jump_vol=base.jump_vol,
        )
        px = merton_european_series(
            snapshot.spot_now,
            snapshot.strike,
            t,
            snapshot.risk_free_rate,
            snapshot.dividend_yield,
            snapshot.iv_now,
            snapshot.option_type,
            cand,
        )
        err = abs(px - target)
        if err < best_err:
            best_err = err
            best = cand
    if best_err > max(0.25 * abs(target), 0.05):
        return base, ["merton_params_defaulted"]
    return best, []


def compare_to_official(
    snapshot: MarketSnapshot,
    surface: Optional[VolSurfaceData] = None,
    *,
    config: Optional[EngineConfig] = None,
) -> CrossCheckResult:
    cfg = config or EngineConfig.from_env()
    official = price_and_attribute(snapshot, surface, config=cfg)
    spec = _spec_now(snapshot, surface)
    limitations = list(official.diagnostics.limitations)
    params, m_lim = calibrate_merton(snapshot, surface)
    limitations.extend(m_lim)

    lsm_bs = lsm_merton = eu_merton = None
    try:
        g, _ = price_lsm_bs(spec, config=cfg)
        lsm_bs = g.price
    except Exception:
        limitations.append("lsm_bs_failed")
    try:
        g, _ = price_lsm_merton(spec, params=params, config=cfg)
        lsm_merton = g.price
    except Exception:
        limitations.append("lsm_merton_failed")
    try:
        g, _ = price_merton_european(spec, params=params)
        eu_merton = g.price
    except Exception:
        limitations.append("merton_european_failed")

    rel = None
    if lsm_bs is not None and official.greeks_now.price:
        rel = abs(lsm_bs - official.greeks_now.price) / max(
            abs(official.greeks_now.price), 1e-8
        )

    return CrossCheckResult(
        official_price=official.greeks_now.price,
        engine_used_for_official=official.diagnostics.engine,
        lsm_bs=lsm_bs,
        lsm_merton=lsm_merton,
        european_merton=eu_merton,
        rel_diff=rel,
        limitations=list(dict.fromkeys(limitations)),
    )


def taylor_second_order(
    snapshot: MarketSnapshot,
    pricing_result: PricingResult,
    *,
    config: Optional[EngineConfig] = None,
) -> SecondOrderTaylorResult:
    """Layer 3: Vanna/Volga second-order Taylor shrinkage."""
    from .second_order import compute_second_order_taylor

    pnl = pricing_result.pnl
    return compute_second_order_taylor(
        snapshot,
        price_prev=pricing_result.greeks_prev.price,
        price_now=pricing_result.greeks_now.price,
        d_spot=pnl.d_spot,
        d_vol=pnl.d_vol,
        residual_pnl=pnl.residual_pnl,
        config=config,
    )


def path_reprice(
    snapshot: MarketSnapshot,
    pricing_result: PricingResult,
    *,
    config: Optional[EngineConfig] = None,
    surface: Optional[VolSurfaceData] = None,
) -> SequentialRevalResult:
    """Layer 4: sequential full revaluation t → S → σ → r."""
    from .sequential_reval import sequential_full_revaluation

    return sequential_full_revaluation(
        snapshot,
        model_total_pnl=pricing_result.pnl.total_pnl,
        config=config,
        iv_now=pricing_result.diagnostics.effective_iv_now,
        iv_prev=pricing_result.diagnostics.effective_iv_prev,
        engine_id=pricing_result.diagnostics.engine,
        surface=surface,
    )
