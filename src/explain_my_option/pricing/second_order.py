"""Second-order cross-Greeks via bump-and-revalue on official FDM."""

from __future__ import annotations

from datetime import date, datetime

from .config import EngineConfig
from .engines.fdm import FdmFlatEngine
from .types import Greeks, MarketSnapshot, PricingSpec, SecondOrderTaylorResult, VolSurfaceData

_SPOT_BUMP = 0.01  # 1% relative bump
_VOL_BUMP = 0.01  # 1 vol point in decimal


def _eval_date(snapshot: MarketSnapshot) -> date:
    if snapshot.as_of:
        return datetime.strptime(snapshot.as_of, "%Y-%m-%d").date()
    return date.today()


def _prev_eval_date(snapshot: MarketSnapshot) -> date:
    if snapshot.prev_as_of:
        return datetime.strptime(snapshot.prev_as_of, "%Y-%m-%d").date()
    as_of = _eval_date(snapshot)
    from datetime import timedelta

    return as_of - timedelta(days=1)


def _spec_at(
    snapshot: MarketSnapshot,
    *,
    spot: float,
    vol: float,
    eval_date: date,
    surface: VolSurfaceData | None = None,
) -> PricingSpec:
    return PricingSpec(
        spot=spot,
        strike=snapshot.strike,
        rate=snapshot.risk_free_rate,
        dividend_yield=snapshot.dividend_yield,
        vol=vol,
        expiry=snapshot.expiry,
        eval_date=eval_date,
        option_type=snapshot.option_type,  # type: ignore[arg-type]
        exercise_style=snapshot.exercise_style,
        discrete_dividends=snapshot.discrete_dividends,
        surface=surface,
    )


def _price_flat(
    spec: PricingSpec,
    *,
    config: EngineConfig | None = None,
) -> Greeks:
    engine = FdmFlatEngine(config or EngineConfig.from_env())
    g, _ = engine.price(spec)
    return g


def compute_second_order_taylor(
    snapshot: MarketSnapshot,
    *,
    price_prev: float,
    price_now: float,
    d_spot: float,
    d_vol: float,
    config: EngineConfig | None = None,
) -> SecondOrderTaylorResult:
    """Vanna/Volga PnL from T-1 cross sensitivities (official flat FDM bumps)."""
    cfg = config or EngineConfig.from_env()
    limitations: list[str] = []
    prev_date = _prev_eval_date(snapshot)
    base = _spec_at(
        snapshot,
        spot=snapshot.spot_prev,
        vol=snapshot.iv_prev,
        eval_date=prev_date,
    )
    try:
        p0 = _price_flat(base, config=cfg).price
        ds = max(abs(snapshot.spot_prev) * _SPOT_BUMP, 0.01)
        dv = _VOL_BUMP
        p_sp = _price_flat(
            _spec_at(snapshot, spot=snapshot.spot_prev + ds, vol=snapshot.iv_prev, eval_date=prev_date),
            config=cfg,
        ).price
        p_vm = _price_flat(
            _spec_at(snapshot, spot=snapshot.spot_prev, vol=snapshot.iv_prev + dv, eval_date=prev_date),
            config=cfg,
        ).price
        p_sp_vm = _price_flat(
            _spec_at(
                snapshot,
                spot=snapshot.spot_prev + ds,
                vol=snapshot.iv_prev + dv,
                eval_date=prev_date,
            ),
            config=cfg,
        ).price
        vanna = (p_sp_vm - p_sp - p_vm + p0) / (ds * dv)
        p_vm_down = _price_flat(
            _spec_at(
                snapshot,
                spot=snapshot.spot_prev,
                vol=max(snapshot.iv_prev - dv, 1e-6),
                eval_date=prev_date,
            ),
            config=cfg,
        ).price
        volga = (p_vm - 2.0 * p0 + p_vm_down) / (dv * dv)
    except Exception:
        limitations.append("second_order_bump_failed")
        return SecondOrderTaylorResult(
            vanna=0.0,
            volga=0.0,
            vanna_pnl=0.0,
            volga_pnl=0.0,
            combined_pnl=0.0,
            residual_after=float(price_now - price_prev),
            limitations=limitations,
        )

    vanna_pnl = vanna * d_spot * d_vol
    volga_pnl = 0.5 * volga * d_vol * d_vol
    combined = vanna_pnl + volga_pnl
    first_order = price_now - price_prev
    residual_after = first_order - combined
    return SecondOrderTaylorResult(
        vanna=float(vanna),
        volga=float(volga),
        vanna_pnl=float(vanna_pnl),
        volga_pnl=float(volga_pnl),
        combined_pnl=float(combined),
        residual_after=float(residual_after),
        limitations=limitations,
    )
