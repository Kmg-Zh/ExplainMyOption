"""Test-only pricing engine budgets — not part of product defaults."""

from __future__ import annotations

from explain_my_option.pricing.config import EngineConfig

LSM_TEST_PATHS = 4096
LSM_TEST_STEPS = 50
LSM_TEST_SEED = 42


def engine_config_for_tests() -> EngineConfig:
    """Smaller grids / fixed LSM seed for offline CI."""
    return EngineConfig(
        t_grid=80,
        x_grid=160,
        lsm_paths=LSM_TEST_PATHS,
        lsm_steps=LSM_TEST_STEPS,
        lsm_seed=LSM_TEST_SEED,
    )
