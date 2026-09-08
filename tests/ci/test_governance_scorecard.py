"""Offline CI scoreboard for A1 governance gates (no live LLM).

Run:
  python tests/ci/test_governance_scorecard.py
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

import bootstrap

bootstrap.install()

from explain_my_option.data.synthetic import load_fixture
from explain_my_option.graph.diagnostic_controller import MAX_DIAGNOSTIC_TOOL_CALLS, run_diagnostic_pass
from explain_my_option.pipeline.verifier import deterministic_precheck
from explain_my_option.pricing.types import (
    Greeks,
    MarketSnapshot,
    PnLAttribution,
    PricingDiagnostics,
    PricingResult,
)
from explain_my_option.report.facts import build_position_facts
from explain_my_option.report.schema import DiagnosticSynthesis
from explain_my_option.report.template import render_position_report
from ci.engine_config import engine_config_for_tests
from explain_my_option.pricing.facade import price_and_attribute

CFG = engine_config_for_tests()
GOVERNANCE_DIR = Path(__file__).resolve().parent / "fixtures" / "governance"


def _load_syn(name: str) -> DiagnosticSynthesis:
    payload = json.loads((GOVERNANCE_DIR / f"{name}.json").read_text(encoding="utf-8"))
    return DiagnosticSynthesis.model_validate(payload)


def _sample_facts(*, residual_pnl: float = 0.06, total_pnl: float = 1.0):
    snap = MarketSnapshot(
        ticker="AAPL",
        option_type="call",
        strike=100.0,
        expiry="2027-01-15",
        spot_now=105.0,
        spot_prev=100.0,
        iv_now=0.30,
        iv_prev=0.28,
        option_price_now=5.0,
        option_price_prev=4.0,
        time_to_expiry_years=0.5,
        data_source="synthetic",
        as_of="2026-08-30",
        bid=4.8,
        ask=5.2,
        quantity=1.0,
        multiplier=1.0,
    )
    pricing = PricingResult(
        greeks_prev=Greeks(price=4.0, delta=0.5, gamma=0.02, vega=0.1, theta=-0.04),
        greeks_now=Greeks(price=5.0, delta=0.52, gamma=0.02, vega=0.1, theta=-0.04),
        pnl=PnLAttribution(
            total_pnl=total_pnl,
            delta_pnl=0.8,
            gamma_pnl=0.05,
            vega_pnl=0.1,
            theta_pnl=-0.01,
            residual_pnl=residual_pnl,
            d_spot=5.0,
            d_vol=0.02,
        ),
        diagnostics=PricingDiagnostics(data_source="synthetic", exercise_style="american"),
    )
    return snap, pricing, build_position_facts(snap, pricing)


def _high_residual_priced() -> tuple[MarketSnapshot, PricingResult]:
    snap = MarketSnapshot(
        ticker="TEST",
        option_type="call",
        strike=100.0,
        expiry="2027-01-15",
        spot_now=105.0,
        spot_prev=100.0,
        iv_now=0.32,
        iv_prev=0.30,
        option_price_now=5.30,
        option_price_prev=5.00,
        time_to_expiry_years=0.5,
        bid=9.80,
        ask=10.20,
        volume=500.0,
        open_interest=1000.0,
        quantity=1.0,
        multiplier=100.0,
        data_source="synthetic",
        as_of="2026-08-30",
    )
    pricing = PricingResult(
        greeks_prev=Greeks(price=5.0, delta=0.5, gamma=0.02, vega=0.20, theta=-0.04),
        greeks_now=Greeks(price=5.35, delta=0.52, gamma=0.02, vega=0.20, theta=-0.04),
        pnl=PnLAttribution(
            total_pnl=1.0,
            delta_pnl=0.20,
            gamma_pnl=0.05,
            vega_pnl=0.04,
            theta_pnl=-0.01,
            residual_pnl=0.50,
            d_spot=5.0,
            d_vol=0.02,
        ),
        diagnostics=PricingDiagnostics(
            data_source="synthetic",
            exercise_style="american",
            engine="fdm_flat",
            mark_calibrated=False,
        ),
    )
    return snap, pricing


def test_numeric_amounts_in_synthesis_fail_precheck():
    syn = _load_syn("numeric_hallucination")
    _, _, facts = _sample_facts()
    pre = deterministic_precheck(
        syn, facts, suppress_vega=False, observation_reliable=True
    )
    assert pre is not None and pre.verdict == "FAIL"
    assert "numeric_hallucination" in pre.policy_flags


def test_unreliable_observation_rejects_vega_led_and_iv_crush():
    syn = _load_syn("vega_unreliable")
    _, _, facts = _sample_facts()
    pre_obs = deterministic_precheck(
        syn, facts, suppress_vega=False, observation_reliable=False
    )
    assert pre_obs is not None and pre_obs.verdict == "PARTIAL"
    assert "observation_soft_lock" in pre_obs.policy_flags

    pre_suppress = deterministic_precheck(
        syn, facts, suppress_vega=True, observation_reliable=True
    )
    assert pre_suppress is not None and pre_suppress.verdict == "PARTIAL"
    assert "suppress_vega_narrative" in pre_suppress.policy_flags


def test_omitted_headline_catalyst_with_elevated_residual_is_partial():
    syn = _load_syn("missing_catalyst")
    _, pricing, facts = _sample_facts(residual_pnl=0.40, total_pnl=1.0)
    residual_pct = abs(100.0 * pricing.pnl.residual_pnl / pricing.pnl.total_pnl)
    assert residual_pct > 15.0
    titles = [
        "Meta options volume surged as implied volatility collapsed after earnings (IV crush)"
    ]
    pre = deterministic_precheck(
        syn,
        facts,
        suppress_vega=False,
        observation_reliable=True,
        news_titles=titles,
    )
    assert pre is not None and pre.verdict == "PARTIAL"
    assert "missing_catalyst_layer" in pre.policy_flags


def test_budget_exhausted_high_residual_sets_terminal_unexplained_break():
    snap, pricing = _high_residual_priced()
    findings = run_diagnostic_pass(snap, pricing, surface=None, config=CFG)
    assert findings.tool_calls_used >= MAX_DIAGNOSTIC_TOOL_CALLS
    assert findings.terminal_unexplained_break is True
    facts = build_position_facts(snap, pricing)
    syn = DiagnosticSynthesis(
        primary_driver="Delta / spot move",
        verdict="Spot led; residual remains unexplained after the diagnostic budget.",
        confidence_level="low",
        confidence_rationale="Budget exhausted.",
        evidence=[],
        takeaways=["Escalate the unexplained residual."],
    )
    report = render_position_report(
        facts, syn, diagnostic_findings=findings.as_dict()
    )
    assert "unexplained" in report.lower()


def test_report_exposes_skipped_tools_with_reasons():
    snap, surf = load_fixture("aapl_exdiv_2023")
    pricing = price_and_attribute(snap, surf, config=CFG)
    findings = run_diagnostic_pass(snap, pricing, surf, config=CFG)
    payload = findings.as_dict()
    assert "skipped_tools" in payload
    facts = build_position_facts(snap, pricing)
    syn = DiagnosticSynthesis(
        primary_driver="Gamma / convexity",
        verdict="Spot convexity dominated the Taylor story.",
        confidence_level="medium",
        confidence_rationale="Large gap.",
        evidence=[],
        takeaways=["Review the residual drill."],
    )
    report = render_position_report(facts, syn, diagnostic_findings=payload)
    skipped = payload.get("skipped_tools") or []
    assert skipped, "expected at least one skipped tool with a reason"
    assert "Skipped candidates" in report
    first = skipped[0]
    assert first.get("reason")
    assert first["name"] in report


if __name__ == "__main__":
    test_numeric_amounts_in_synthesis_fail_precheck()
    test_unreliable_observation_rejects_vega_led_and_iv_crush()
    test_omitted_headline_catalyst_with_elevated_residual_is_partial()
    test_budget_exhausted_high_residual_sets_terminal_unexplained_break()
    test_report_exposes_skipped_tools_with_reasons()
    print("OK — governance scorecard passed")
