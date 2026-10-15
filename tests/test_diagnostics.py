"""Deterministic diagnostic pass: tool budget, escalation rules, regime rule, quiet days."""

from __future__ import annotations

import pytest
from support import FAST

from explain_my_option.data.historical_chain import load_historical_case
from explain_my_option.data.synthetic import list_fixtures, load_fixture
from explain_my_option.graph.deps import OfficialFdmPnlSource
from explain_my_option.graph.diagnostic_controller import (
    FREE_TOOLS,
    MAX_DIAGNOSTIC_TOOL_CALLS,
    TAYLOR_REGIME_THRESHOLD,
    run_diagnostic_pass,
)
from explain_my_option.pricing import price_and_attribute


def _diagnose(name: str):
    if name.endswith("_real") or name.startswith("quiet_"):
        snap, surf = load_historical_case(name), None
    else:
        snap, surf = load_fixture(name)
    return run_diagnostic_pass(snap, price_and_attribute(snap, surf, config=FAST), surf, pnl=OfficialFdmPnlSource(config=FAST))


def _costly(findings) -> list[str]:
    return [tool for tool in findings.tools_run if tool not in FREE_TOOLS]


@pytest.mark.parametrize("name", list_fixtures())
def test_free_tools_always_run_and_the_budget_holds(name):
    findings = _diagnose(name)
    assert "taylor_second_order" in findings.tools_run
    assert all(findings.tool_costs[t] == "free" for t in FREE_TOOLS if t in findings.tools_run)
    # At most one budgeted costly tool, plus at most one follow-up full revaluation.
    assert len(_costly(findings)) <= MAX_DIAGNOSTIC_TOOL_CALLS + 1


def test_severity_above_ten_percent_spends_the_slot_on_a_full_revaluation():
    findings = _diagnose("put_skew")  # residual ~174% of the model move
    assert _costly(findings) == ["path_reprice"]
    assert {"name": "compare_to_official", "reason": "path_reprice selected for severity >10%"} in findings.as_dict()["skipped_tools"]


def test_an_in_the_money_ex_div_window_spends_the_slot_on_the_exercise_check():
    findings = _diagnose("american_put_div")
    assert _costly(findings) == ["american_dividend_exercise_check"]
    assert findings.ex_div_attribution is not None and findings.ex_div_attribution["flag_ex_div_window"]


def test_a_large_residual_left_after_the_slot_is_spent_is_a_terminal_break():
    assert _diagnose("vow_float_squeeze_2008").terminal_unexplained_break
    assert not _diagnose("vol_crush").terminal_unexplained_break


def test_a_moderate_residual_gets_a_follow_up_revaluation_that_never_escalates():
    findings = _diagnose("spot_gap")  # residual ~8%: below the slot's 10% band
    assert "path_reprice" in findings.tools_run
    assert not findings.terminal_unexplained_break


def test_skipped_tools_are_listed_once_with_the_reason():
    names = [s.name for s in _diagnose("aapl_exdiv_2023").skipped_tools]
    assert len(names) == len(set(names))


def test_reconciled_marks_skip_deep_diagnostics_but_a_large_residual_is_still_audited():
    findings = _diagnose("gme_squeeze_2021_real")  # mark calibrated, residual ~18%
    assert "deep_diagnostics" in [s.name for s in findings.skipped_tools]
    assert "path_reprice" in findings.tools_run


def test_a_large_move_the_greeks_explain_is_not_a_quiet_day():
    """A small residual ratio alone is not enough: vol_crush loses 35% of the option."""
    assert not _diagnose("vol_crush").no_escalation


def test_regime_rule_flags_moves_where_taylor_diverges():
    """r_spot = |½Γ(ΔS)²| / |ΔS·Δ|; past 0.35 the full revaluation is the headline."""
    squeeze = _diagnose("vow_float_squeeze_2008")
    assert squeeze.taylor_regime == "INVALID" and max(squeeze.r_spot, squeeze.r_vol) > TAYLOR_REGIME_THRESHOLD
    exdiv = _diagnose("aapl_exdiv_2023_real")
    assert exdiv.taylor_regime == "VALID" and max(exdiv.r_spot, exdiv.r_vol) <= TAYLOR_REGIME_THRESHOLD
    flat = _diagnose("calibration_ok")  # near-zero first-order terms must not divide by zero
    assert flat.r_spot == flat.r_spot and flat.r_vol == flat.r_vol
