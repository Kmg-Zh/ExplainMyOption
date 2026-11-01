"""Second-order cross-Greeks via bump-and-revalue on official FDM."""

from __future__ import annotations

from .config import EngineConfig
from .engines.fdm import FdmFlatEngine
from .types import Greeks, MarketSnapshot, PricingSpec, SecondOrderTaylorResult

_SPOT_BUMP = 0.01  # 1% relative bump
_VOL_BUMP = 0.01  # 1 vol point in decimal


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
    d_spot: float,
    d_vol: float,
    residual_pnl: float = 0.0,
    config: EngineConfig | None = None,
) -> SecondOrderTaylorResult:
    """Vanna/Volga PnL from T-1 cross sensitivities (official flat FDM bumps).

    ``residual_after`` is the first-order Taylor residual left once the
    second-order terms are added back.
    """
    cfg = config or EngineConfig.from_env()
    limitations: list[str] = []
    prev_date = snapshot.prev_date()
    base = snapshot.spec(
        spot=snapshot.spot_prev,
        vol=snapshot.iv_prev,
        eval_date=prev_date,
    )
    try:
        p0 = _price_flat(base, config=cfg).price
        ds = max(abs(snapshot.spot_prev) * _SPOT_BUMP, 0.01)
        dv = _VOL_BUMP
        p_sp = _price_flat(
            snapshot.spec(spot=snapshot.spot_prev + ds, vol=snapshot.iv_prev, eval_date=prev_date),
            config=cfg,
        ).price
        p_vm = _price_flat(
            snapshot.spec(spot=snapshot.spot_prev, vol=snapshot.iv_prev + dv, eval_date=prev_date),
            config=cfg,
        ).price
        p_sp_vm = _price_flat(
            snapshot.spec(
                spot=snapshot.spot_prev + ds,
                vol=snapshot.iv_prev + dv,
                eval_date=prev_date,
            ),
            config=cfg,
        ).price
        vanna = (p_sp_vm - p_sp - p_vm + p0) / (ds * dv)
        p_vm_down = _price_flat(
            snapshot.spec(
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
            residual_after=float(residual_pnl),
            limitations=limitations,
        )

    vanna_pnl = vanna * d_spot * d_vol
    volga_pnl = 0.5 * volga * d_vol * d_vol
    combined = vanna_pnl + volga_pnl
    return SecondOrderTaylorResult(
        vanna=float(vanna),
        volga=float(volga),
        vanna_pnl=float(vanna_pnl),
        volga_pnl=float(volga_pnl),
        combined_pnl=float(combined),
        residual_after=float(residual_pnl - combined),
        limitations=limitations,
    )
