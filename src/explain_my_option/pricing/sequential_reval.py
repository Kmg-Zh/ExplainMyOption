"""Sequential full revaluation — locked order t → S → σ → r."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from .config import EngineConfig
from .registry import get_engine
from .types import EngineId, MarketSnapshot, PricingSpec, SequentialRevalResult, SequentialRevalStep, VolSurfaceData

_ORDER = ["time", "spot", "vol", "rate"]


def _eval_date(snapshot: MarketSnapshot) -> date:
    if snapshot.as_of:
        return datetime.strptime(snapshot.as_of, "%Y-%m-%d").date()
    return date.today()


def _prev_eval_date(snapshot: MarketSnapshot) -> date:
    if snapshot.prev_as_of:
        return datetime.strptime(snapshot.prev_as_of, "%Y-%m-%d").date()
    return _eval_date(snapshot) - timedelta(days=1)


def _spec(
    snapshot: MarketSnapshot,
    *,
    spot: float,
    vol: float,
    rate: float,
    eval_date: date,
) -> PricingSpec:
    return PricingSpec(
        spot=spot,
        strike=snapshot.strike,
        rate=rate,
        dividend_yield=snapshot.dividend_yield,
        vol=vol,
        expiry=snapshot.expiry,
        eval_date=eval_date,
        option_type=snapshot.option_type,  # type: ignore[arg-type]
        exercise_style=snapshot.exercise_style,
        discrete_dividends=snapshot.discrete_dividends,
        surface=None,
    )


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
    as_of = _eval_date(snapshot)
    prev_date = _prev_eval_date(snapshot)
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
        _spec(snapshot, spot=spot, vol=vol, rate=rate, eval_date=eval_d),
        config=cfg,
        engine_id=engine_id,
    )
    price = p_start
    steps: list[SequentialRevalStep] = []

    def _step_spec(spot_v: float, vol_v: float, rate_v: float, eval_v: date) -> PricingSpec:
        spec = _spec(snapshot, spot=spot_v, vol=vol_v, rate=rate_v, eval_date=eval_v)
        if engine_id == "fdm_local_vol":
            spec = PricingSpec(
                spot=spec.spot,
                strike=spec.strike,
                rate=spec.rate,
                dividend_yield=spec.dividend_yield,
                vol=spec.vol,
                expiry=spec.expiry,
                eval_date=spec.eval_date,
                option_type=spec.option_type,
                exercise_style=spec.exercise_style,
                discrete_dividends=spec.discrete_dividends,
                surface=surface,
            )
        return spec

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
