"""Engine registry. Official PnL is FDM; CRR / LSM remain selectable."""

from __future__ import annotations

from typing import Optional

from .config import EngineConfig
from .engines.crr import CrrEngine
from .engines.fdm import FdmFlatEngine, FdmLocalVolEngine
from .types import EngineId, PricingSpec, VolSurfaceData


def get_engine(name: EngineId, config: Optional[EngineConfig] = None):
    cfg = config or EngineConfig.from_env()
    if name == "fdm_flat":
        return FdmFlatEngine(cfg)
    if name == "fdm_local_vol":
        return FdmLocalVolEngine(cfg)
    if name == "crr":
        return CrrEngine(cfg)
    raise KeyError(f"Unknown or analysis-only engine {name!r} — use analysis_api for LSM/Merton")


def resolve_official_engine(
    *,
    surface: Optional[VolSurfaceData],
    local_vol_ok: bool,
    config: Optional[EngineConfig] = None,
) -> EngineId:
    cfg = config or EngineConfig.from_env()
    if cfg.engine_override in ("fdm_local_vol", "fdm_flat", "crr"):
        return cfg.engine_override  # type: ignore[return-value]
    if surface is not None and local_vol_ok:
        return "fdm_local_vol"
    return "fdm_flat"


def spec_from_snapshot_now(snapshot, surface: Optional[VolSurfaceData] = None) -> PricingSpec:
    from datetime import date, datetime

    as_of = snapshot.as_of or date.today().isoformat()
    eval_date = datetime.strptime(as_of, "%Y-%m-%d").date()
    return PricingSpec(
        spot=snapshot.spot_now,
        strike=snapshot.strike,
        rate=snapshot.risk_free_rate,
        dividend_yield=snapshot.dividend_yield,
        vol=snapshot.iv_now,
        expiry=snapshot.expiry,
        eval_date=eval_date,
        option_type=snapshot.option_type,  # type: ignore[arg-type]
        exercise_style=snapshot.exercise_style,
        discrete_dividends=snapshot.discrete_dividends,
        surface=surface,
    )
