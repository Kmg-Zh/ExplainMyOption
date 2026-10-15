"""Sequential full revaluation — locked order t → S → σ → r."""

from __future__ import annotations

from datetime import date

from .config import EngineConfig
from .registry import get_engine
from .types import EngineId, MarketSnapshot, PricingSpec, SequentialRevalResult, SequentialRevalStep, VolSurfaceData

_ORDER = ["time", "spot", "vol", "rate"]


def _npv(
    spec: PricingSpec,
    *,
    config: EngineConfig,
    engine_id: EngineId,
) -> float:
    engine = get_engine(engine_id, config)
    g, _ = engine.price(spec)
    return float(g.price)


def sequential_full_revaluation(
    snapshot: MarketSnapshot,
    *,
    model_total_pnl: float,
    config: EngineConfig | None = None,
    iv_now: float | None = None,
    iv_prev: float | None = None,
    engine_id: EngineId = "fdm_flat",
    surface: VolSurfaceData | None = None,
) -> SequentialRevalResult:
    """Reprice official FDM along t → S → σ → r; step sum telescopes to model ΔP."""
    cfg = config or EngineConfig.from_env()
    limitations: list[str] = []
    as_of = snapshot.as_of_date()
    prev_date = snapshot.prev_date()
    rate_prev = snapshot.risk_free_rate_prev
    if rate_prev is None:
        rate_prev = snapshot.risk_free_rate
        limitations.append("rate_prev_unavailable")

    vol_prev = iv_prev if iv_prev is not None else snapshot.iv_prev
    vol_now = iv_now if iv_now is not None else snapshot.iv_now

    # Initial state at T-1
    spot = snapshot.spot_prev
    vol = vol_prev
    rate = rate_prev
    eval_d = prev_date

    p_start = _npv(
        snapshot.spec(spot=spot, vol=vol, rate=rate, eval_date=eval_d),
        config=cfg,
        engine_id=engine_id,
    )
    price = p_start
    steps: list[SequentialRevalStep] = []

    def _step_spec(spot_v: float, vol_v: float, rate_v: float, eval_v: date) -> PricingSpec:
        return snapshot.spec(
            spot=spot_v,
            vol=vol_v,
            rate=rate_v,
            eval_date=eval_v,
            surface=surface if engine_id == "fdm_local_vol" else None,
        )

    # 1. time
    eval_d = as_of
    p_after = _npv(_step_spec(spot, vol, rate, eval_d), config=cfg, engine_id=engine_id)
    steps.append(
        SequentialRevalStep(
            factor="time",
            pnl_usd=p_after - price,
            price_before=price,
            price_after=p_after,
        )
    )
    price = p_after

    # 2. spot
    spot = snapshot.spot_now
    p_after = _npv(_step_spec(spot, vol, rate, eval_d), config=cfg, engine_id=engine_id)
    steps.append(
        SequentialRevalStep(
            factor="spot",
            pnl_usd=p_after - price,
            price_before=price,
            price_after=p_after,
        )
    )
    price = p_after

    # 3. vol
    vol = vol_now
    p_after = _npv(_step_spec(spot, vol, rate, eval_d), config=cfg, engine_id=engine_id)
    steps.append(
        SequentialRevalStep(
            factor="vol",
            pnl_usd=p_after - price,
            price_before=price,
            price_after=p_after,
        )
    )
    price = p_after

    # 4. rate (skip bucket if no prior rate move)
    rate_now = snapshot.risk_free_rate
    if (
        snapshot.risk_free_rate_prev is not None
        and abs(rate_now - snapshot.risk_free_rate_prev) > 1e-12
    ):
        rate = rate_now
        p_after = _npv(_step_spec(spot, vol, rate, eval_d), config=cfg, engine_id=engine_id)
        steps.append(
            SequentialRevalStep(
                factor="rate",
                pnl_usd=p_after - price,
                price_before=price,
                price_after=p_after,
            )
        )
        price = p_after
    else:
        limitations.append("rate_step_skipped")

    step_sum = sum(s.pnl_usd for s in steps)
    residual = model_total_pnl - step_sum
    return SequentialRevalResult(
        steps=steps,
        model_total_pnl=float(model_total_pnl),
        step_sum=float(step_sum),
        residual_vs_model=float(residual),
        order=list(_ORDER),
        limitations=limitations,
    )
