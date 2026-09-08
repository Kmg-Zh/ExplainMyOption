"""Tunable engine defaults. Swap methods via env without editing call sites."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from .types import EngineId

# Merton (1976) typical equity jump-diffusion defaults.
# λ ≈ 0.5 jumps/year, ln(1+k̄) ≈ −10%, jump-size vol ≈ 15%.
DEFAULT_JUMP_INTENSITY = 0.5
DEFAULT_JUMP_MEAN = -0.10
DEFAULT_JUMP_VOL = 0.15

LSM_CI_PATHS = 8192
LSM_CI_STEPS = 100
LSM_PROD_PATHS = 65536
LSM_PROD_STEPS = 252


@dataclass(frozen=True)
class MertonParams:
    """Merton (1976) jump-diffusion parameters.

    ``jump_mean`` is the mean of log jump size (μ_J). Jump-size std is
    ``jump_vol`` (δ). Intensity λ is jumps per year.
    """

    jump_intensity: float = DEFAULT_JUMP_INTENSITY
    jump_mean: float = DEFAULT_JUMP_MEAN
    jump_vol: float = DEFAULT_JUMP_VOL


@dataclass
class EngineConfig:
    """Numerical budgets for FDM / LSM. Env vars override selected fields."""

    t_grid: int = 200
    x_grid: int = 400
    damping_steps: int = 0
    crr_steps: int = 500
    min_ql_version: str = "1.30"
    lsm_paths: int = LSM_PROD_PATHS
    lsm_steps: int = LSM_PROD_STEPS
    lsm_seed: int = 0
    lsm_poly_order: int = 2
    engine_override: Optional[EngineId] = None

    @classmethod
    def from_env(cls) -> "EngineConfig":
        cfg = cls()
        t = os.getenv("EMO_FDM_TGRID")
        x = os.getenv("EMO_FDM_XGRID")
        if t:
            cfg.t_grid = int(t)
        if x:
            cfg.x_grid = int(x)
        override = os.getenv("EMO_PRICING_ENGINE")
        if override:
            cfg.engine_override = override  # type: ignore[assignment]
        paths = os.getenv("EMO_LSM_PATHS")
        steps = os.getenv("EMO_LSM_STEPS")
        seed = os.getenv("EMO_LSM_SEED")
        if paths:
            cfg.lsm_paths = int(paths)
        if steps:
            cfg.lsm_steps = int(steps)
        if seed is not None and seed != "":
            cfg.lsm_seed = int(seed)
        return cfg


def default_merton_params() -> MertonParams:
    return MertonParams()
