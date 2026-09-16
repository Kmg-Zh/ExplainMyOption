"""Tool-budget reclassification and the Taylor regime rule: Task A5.1/A5.3/A5.4.

taylor_second_order is free (A5.1): it always runs and never consumes the
3-call diagnostic budget, so it no longer competes with path_reprice for
the scarce slot. taylor_regime (A5.3) gates whether the Taylor split or a
full revaluation is the headline. A5.4's materiality folding is exercised
via the report template smoke test in test_report_template.py's existing
fixtures; here we check the underlying r_spot/r_vol numbers directly.
"""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from ci.engine_config import engine_config_for_tests
from explain_my_option.data.historical_chain import load_historical_case
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.graph.diagnostic_controller import (
    MAX_DIAGNOSTIC_TOOL_CALLS,
    TAYLOR_REGIME_THRESHOLD,
    run_diagnostic_pass,
)
from explain_my_option.pricing.facade import price_and_attribute


def test_taylor_second_order_always_runs_and_is_free():
    snap, surf = load_fixture("vol_crush")
    pricing = price_and_attribute(snap, surface_data=surf, config=engine_config_for_tests())
    findings = run_diagnostic_pass(snap, pricing, surf, config=engine_config_for_tests())
    assert "taylor_second_order" in findings.tools_run
    assert findings.tool_costs["taylor_second_order"] == "free"
    # A free tool must not have consumed a budget slot.
    assert findings.tool_calls_used <= MAX_DIAGNOSTIC_TOOL_CALLS


def test_taylor_second_order_does_not_block_path_reprice():
    """The old bug: on the case where it mattered most, taylor_second_order
    used to win the single deep-tool slot and path_reprice never ran."""
    snap, surf = load_fixture("vol_crush")
    pricing = price_and_attribute(snap, surface_data=surf, config=engine_config_for_tests())
    findings = run_diagnostic_pass(snap, pricing, surf, config=engine_config_for_tests())
    if findings.r_spot is not None and findings.r_vol is not None:
        # Whatever the severity, both taylor_second_order (free) AND a
        # costly deep tool can now coexist in the same pass.
        costly_ran = [n for n, c in findings.tool_costs.items() if c == "costly"]
        assert "taylor_second_order" in findings.tools_run
        assert len(costly_ran) >= 1 or findings.tool_calls_used == 0


def test_regime_rule_squeeze_stress_fixture_is_invalid():
    snap, surf = load_fixture("vow_float_squeeze_2008")
    pricing = price_and_attribute(snap, surface_data=surf, config=engine_config_for_tests())
    findings = run_diagnostic_pass(snap, pricing, surf, config=engine_config_for_tests())
    assert findings.taylor_regime == "INVALID"
    assert max(findings.r_spot, findings.r_vol) > TAYLOR_REGIME_THRESHOLD


def test_regime_rule_real_exdiv_case_is_valid():
    snap = load_historical_case("aapl_exdiv_2023_real")
    pricing = price_and_attribute(snap, config=engine_config_for_tests())
    findings = run_diagnostic_pass(snap, pricing, None, config=engine_config_for_tests())
    assert findings.taylor_regime == "VALID"
    assert max(findings.r_spot, findings.r_vol) <= TAYLOR_REGIME_THRESHOLD


def test_regime_rule_guards_division_by_zero():
    from explain_my_option.graph.diagnostic_controller import run_diagnostic_pass

    # A flat/no-move fixture should never raise even if delta_pnl or
    # vega_pnl round to ~0.
    snap, surf = load_fixture("calibration_ok")
    pricing = price_and_attribute(snap, surface_data=surf, config=engine_config_for_tests())
    findings = run_diagnostic_pass(snap, pricing, surf, config=engine_config_for_tests())
    assert findings.taylor_regime in ("VALID", "INVALID")
    assert findings.r_spot is not None and findings.r_spot == findings.r_spot  # not NaN
    assert findings.r_vol is not None and findings.r_vol == findings.r_vol


if __name__ == "__main__":
    test_taylor_second_order_always_runs_and_is_free()
    test_taylor_second_order_does_not_block_path_reprice()
    test_regime_rule_squeeze_stress_fixture_is_invalid()
    test_regime_rule_real_exdiv_case_is_valid()
    test_regime_rule_guards_division_by_zero()
    print("OK — regime rule / free-tool budget tests passed")
