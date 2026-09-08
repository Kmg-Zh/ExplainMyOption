"""LSM / Merton analysis API (seeded, small path counts)."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


from bootstrap import install

install()

from explain_my_option.data.synthetic import load_fixture
from explain_my_option.pricing.analysis_api import _spec_now, calibrate_merton
from ci.engine_config import engine_config_for_tests
from explain_my_option.pricing.config import default_merton_params
from explain_my_option.pricing.engines.lsm import price_lsm_merton
from explain_my_option.pricing.engines.merton import price_merton_european

CFG = engine_config_for_tests()


def test_european_merton_vs_lsm_terminal_only():
    snap, _ = load_fixture("flat_only")
    snap.exercise_style = "european"
    spec = _spec_now(snap, None)
    params = default_merton_params()
    eu, _ = price_merton_european(spec, params=params)
    lsm, _ = price_lsm_merton(spec, params=params, config=CFG, european=True)
    rel = abs(lsm.price - eu.price) / max(abs(eu.price), 1e-8)
    assert eu.price > 0
    assert rel < 0.25


def test_calibrate_merton_defaults_without_surface():
    snap, _ = load_fixture("flat_only")
    params, lim = calibrate_merton(snap, None)
    assert "merton_params_defaulted" in lim
    assert params.jump_intensity == default_merton_params().jump_intensity


if __name__ == "__main__":
    test_european_merton_vs_lsm_terminal_only()
    test_calibrate_merton_defaults_without_surface()
    print("OK — LSM/Merton checks passed")
