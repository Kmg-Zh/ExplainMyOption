"""Engine registry. Official PnL is FDM; CRR / LSM remain selectable."""

from __future__ import annotations

from typing import Optional

from .config import EngineConfig
from .engines.crr import CrrEngine
from .engines.fdm import FdmFlatEngine, FdmLocalVolEngine
from .types import EngineId, VolSurfaceData


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

