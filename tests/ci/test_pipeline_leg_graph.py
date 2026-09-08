"""Leg-subgraph routing tests for A2/A3."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import os
from dataclasses import dataclass

import bootstrap

bootstrap.install()

from explain_my_option.pipeline.book_schema import BookLegSpec
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.leg_graph import (
    _apply_observation_lock_to_synthesis,
    build_leg_diagnosis_subgraph,
)
from explain_my_option.pipeline.llm_roles import LlmRoleRegistry
from explain_my_option.pipeline.verifier_schema import DiagnosticVerifierResult
from explain_my_option.report.schema import DiagnosticSynthesis, EvidenceItem


@dataclass
class _MockNarrator:
    verdict: str = "Mock synthesis."

    def structured_invoke(self, *, system, human, schema):
        return schema(
            primary_driver="Delta / spot move",
            verdict=self.verdict,
            confidence_level="medium",
            confidence_rationale="mock narrator",
            evidence=[],
            takeaways=["watch residual"],
            american_commentary="",
        )


@dataclass
class _MockVerifier:
    verdicts: tuple[str, ...] = ("PASS",)
    policy_flags: tuple[tuple[str, ...], ...] = ()
    idx: int = 0

    def structured_invoke(self, *, system, human, schema):
        verdict = self.verdicts[min(self.idx, len(self.verdicts) - 1)]
        flags: tuple[str, ...] = ()
        if self.policy_flags:
            flags = self.policy_flags[min(self.idx, len(self.policy_flags) - 1)]
        self.idx += 1
        return DiagnosticVerifierResult(
            verdict=verdict,
            missing_evidence=[],
            policy_flags=list(flags),
            rationale="mock",
        )


class _MockDigesterEmpty:
    def structured_invoke(self, *, system, human, schema):
        del system, human
        return schema(relevant=[], discarded=[], mechanisms=[], brief="", reason="mock-empty")


class _FailIfCalledChallenger:
    def structured_invoke(self, *, system, human, schema):
        raise AssertionError("challenger should be short-circuited")


def _leg() -> BookLegSpec:
    return BookLegSpec(leg_id="demo", fixture="vol_crush", ticker="AAPL")


def _base_config(*, verify_budget: int = 1) -> PipelineConfig:
    return PipelineConfig(
        features={"a1", "a2", "a3"},
        diag_budget=3,
        diag_iterations=2,
        verify_budget=verify_budget,
        require_openai=True,
    )


def test_leg_graph_compiles_with_explicit_loop_nodes():
    graph = build_leg_diagnosis_subgraph(
        config=_base_config(),
        roles=LlmRoleRegistry(narrator=_MockNarrator(), verifier=_MockVerifier()),
    )
    xray_nodes = set(graph.get_graph(xray=True).nodes.keys())
    assert any("residual_gate" in node for node in xray_nodes)
    assert any("react_tool_exec" in node for node in xray_nodes)
    assert any("verify" in node for node in xray_nodes)
    assert any("digest_news" in node for node in xray_nodes)
    assert any("challenge_catalyst" in node for node in xray_nodes)
    assert any("reconcile_debate" in node for node in xray_nodes)
    assert any("reflect_verifier" in node for node in xray_nodes)


def test_a3_fail_exhausted_escalates_terminal_break():
    old = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-test-not-real"
    try:
        roles = LlmRoleRegistry(
            narrator=_MockNarrator(),
            verifier=_MockVerifier(
                verdicts=("FAIL",),
                policy_flags=(("numeric_hallucination",),),
            ),
        )
        app = build_leg_diagnosis_subgraph(config=_base_config(verify_budget=1), roles=roles)
        out = app.invoke({"leg": _leg()})
    finally:
        if old is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = old

    assert out["diagnostic_findings"].get("terminal_unexplained_break") is True
    assert "terminal break escalation" in out["diagnostic_synthesis"]["verdict"].lower()


def test_a3_partial_reflects_without_terminal_break():
    old = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-test-not-real"
    try:
        roles = LlmRoleRegistry(
            narrator=_MockNarrator(),
            verifier=_MockVerifier(verdicts=("PARTIAL",)),
        )
        app = build_leg_diagnosis_subgraph(config=_base_config(verify_budget=1), roles=roles)
        out = app.invoke({"leg": _leg()})
    finally:
        if old is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = old

    assert out["diagnostic_findings"].get("terminal_unexplained_break") is not True
    assert out["diagnostic_findings"].get("verifier_status") == "PARTIAL"
    assert out["diagnostic_synthesis"]["verdict"].startswith("Reflect (PARTIAL):")


def test_a3_soft_fail_reflects_without_terminal_break():
    old = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-test-not-real"
    try:
        roles = LlmRoleRegistry(
            narrator=_MockNarrator(),
            verifier=_MockVerifier(verdicts=("FAIL",)),
        )
        app = build_leg_diagnosis_subgraph(config=_base_config(verify_budget=1), roles=roles)
        out = app.invoke({"leg": _leg()})
    finally:
        if old is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = old

    assert out["diagnostic_findings"].get("terminal_unexplained_break") is not True
    assert out["diagnostic_findings"].get("verifier_status") == "PARTIAL"
    assert "Reflect (PARTIAL):" in out["diagnostic_synthesis"]["verdict"]


def test_reconcile_with_challenge_injects_missing_mechanism():
    from explain_my_option.pipeline.challenger import reconcile_with_challenge
    from explain_my_option.report.schema import DiagnosticSynthesis

    syn = DiagnosticSynthesis(
        primary_driver="Delta / spot move",
        verdict="Spot move dominated via higher-order convexity.",
        confidence_level="medium",
        confidence_rationale="Truncation after an extreme gap.",
        evidence=[],
        takeaways=["Re-price on the full surface."],
    )
    out = reconcile_with_challenge(
        syn,
        {"layer_b_required": True, "mechanisms": ["borrow", "squeeze"]},
    )
    blob = (out.verdict + " " + " ".join(out.takeaways)).lower()
    assert "borrow" in blob
    assert "squeeze" in blob


def test_observation_lock_strips_evidence_from_synthesis():
    syn = DiagnosticSynthesis(
        primary_driver="Delta / spot move",
        verdict="Spot move dominated.",
        confidence_level="medium",
        confidence_rationale="mock narrator",
        evidence=[EvidenceItem(headline="h1", source="s1", relevance="r1")],
        takeaways=["watch residual"],
        american_commentary="",
    )
    out = _apply_observation_lock_to_synthesis(
        syn, {"observation_reliable": False}
    )
    assert out.evidence == []


def test_run_catalyst_challenge_skips_on_observation_lock():
    from explain_my_option.data_loader import NewsItem
    from explain_my_option.pipeline.challenger import run_catalyst_challenge
    from explain_my_option.pipeline.digest import IntelDigest
    from explain_my_option.pricing.types import (
        Greeks,
        MarketSnapshot,
        PnLAttribution,
        PricingDiagnostics,
        PricingResult,
    )

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
    )
    pricing = PricingResult(
        greeks_prev=Greeks(price=4.0, delta=0.5, gamma=0.02, vega=0.1, theta=-0.04),
        greeks_now=Greeks(price=5.0, delta=0.52, gamma=0.02, vega=0.1, theta=-0.04),
        pnl=PnLAttribution(
            total_pnl=1.0,
            delta_pnl=0.8,
            gamma_pnl=0.05,
            vega_pnl=0.1,
            theta_pnl=-0.01,
            residual_pnl=0.06,
            d_spot=5.0,
            d_vol=0.02,
        ),
        diagnostics=PricingDiagnostics(data_source="synthetic", exercise_style="american"),
    )
    digest = IntelDigest(
        relevant=[
            {
                "title": "Apple reports earnings",
                "publisher": "Reuters",
                "mechanisms": ["earnings"],
                "one_line_fact": "Earnings print named.",
            }
        ],
        discarded=[],
        mechanisms=["earnings"],
        brief="Earnings headline is relevant.",
    )
    out = run_catalyst_challenge(
        role=_FailIfCalledChallenger(),
        snap=snap,
        pricing=pricing,
        news=[NewsItem(title="Apple reports earnings")],
        intel_digest=digest,
        diagnostic_findings={"observation_reliable": False},
    )
    assert out.layer_b_required is False
    assert out.suppress_reason == "observation lock"


def test_leg_graph_short_circuits_challenger_when_digest_empty():
    old = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-test-not-real"
    try:
        roles = LlmRoleRegistry(
            narrator=_MockNarrator(),
            verifier=_MockVerifier(verdicts=("PASS",)),
            challenger=_FailIfCalledChallenger(),
            digester=_MockDigesterEmpty(),
        )
        app = build_leg_diagnosis_subgraph(config=_base_config(verify_budget=1), roles=roles)
        out = app.invoke({"leg": _leg()})
    finally:
        if old is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = old
    challenge = out["diagnostic_findings"].get("catalyst_challenge", {})
    assert challenge.get("layer_b_required") is False
    assert challenge.get("suppress_reason") == "no relevant catalysts"


if __name__ == "__main__":
    test_leg_graph_compiles_with_explicit_loop_nodes()
    test_a3_fail_exhausted_escalates_terminal_break()
    test_a3_partial_reflects_without_terminal_break()
    test_a3_soft_fail_reflects_without_terminal_break()
    test_reconcile_with_challenge_injects_missing_mechanism()
    test_observation_lock_strips_evidence_from_synthesis()
    test_run_catalyst_challenge_skips_on_observation_lock()
    test_leg_graph_short_circuits_challenger_when_digest_empty()
    print("OK — pipeline leg graph tests passed")
