"""Deterministic terminal states never reach the LLM: Task A9.1.

no_escalation and terminal_no_comparable_observation render their fixed
report text and short-circuit before synthesize -- no narrator call, no
catalyst critic, no verifier. This is a routing guard in the existing
graph (route_after_diag_finalize / route_after_fetch), not a new node.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from ci.engine_config import engine_config_for_tests
from explain_my_option.data.historical_chain import load_historical_case
from explain_my_option.data.observation import NoComparableObservationError, ObservationStatus
from explain_my_option.data_loader import LoadedData
from explain_my_option.graph.deps import GraphDeps, OfficialFdmPnlSource
from explain_my_option.pipeline.book_schema import BookLegSpec
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.leg_graph import build_leg_diagnosis_subgraph
from explain_my_option.pipeline.llm_roles import LlmRoleRegistry


@dataclass
class _FailIfCalled:
    def structured_invoke(self, *, system, human, schema):
        raise AssertionError(f"LLM must not be called here ({schema.__name__})")


def _fail_roles() -> LlmRoleRegistry:
    return LlmRoleRegistry(
        narrator=_FailIfCalled(),
        verifier=_FailIfCalled(),
        challenger=_FailIfCalled(),
        digester=_FailIfCalled(),
    )


@dataclass
class _SnapshotLoader:
    name: str

    def load(self, *, ticker, option_type, strike, expiry):
        return LoadedData(
            snapshot=load_historical_case(self.name), news=[], surface=None, surface_prev=None
        )


def test_no_escalation_makes_zero_llm_calls():
    name = "quiet_aapl_2023-04-24"
    deps = GraphDeps(
        market=_SnapshotLoader(name), pnl=OfficialFdmPnlSource(config=engine_config_for_tests())
    )
    app = build_leg_diagnosis_subgraph(
        config=PipelineConfig(features={"a1", "a2", "a3"}, verify_budget=1),
        deps=deps,
        roles=_fail_roles(),
    )
    snap = load_historical_case(name)
    leg = BookLegSpec(leg_id="q", fixture=None, ticker=snap.ticker, strike=snap.strike, expiry=snap.expiry)
    out = app.invoke({"leg": leg})
    assert out.get("no_escalation") is True
    assert out.get("llm_calls", 0) == 0


@dataclass
class _NoComparableLoader:
    def load(self, *, ticker, option_type, strike, expiry):
        raise NoComparableObservationError(
            contract="X",
            status_t1=ObservationStatus.OK,
            status_t=ObservationStatus.DAY_MISSING,
            date_t1="t-1",
            date_t="t",
        )


def test_terminal_no_comparable_observation_makes_zero_llm_calls():
    deps = GraphDeps(market=_NoComparableLoader())
    app = build_leg_diagnosis_subgraph(
        config=PipelineConfig(features={"a1", "a2", "a3"}, verify_budget=1),
        deps=deps,
        roles=_fail_roles(),
    )
    leg = BookLegSpec(leg_id="q", fixture=None, ticker="X", strike=1.0, expiry="2027-01-01")
    out = app.invoke({"leg": leg})
    assert out.get("terminal_no_comparable_observation") is True
    assert out.get("llm_calls", 0) == 0


def test_normal_pass_run_counts_at_least_two_llm_calls():
    """Sanity check on the counter itself: a run that does reach the
    narrator/verifier should show it, so the zero above is meaningful."""

    @dataclass
    class _MockRole:
        def structured_invoke(self, *, system, human, schema):
            name = schema.__name__
            if name == "DiagnosticSynthesis":
                return schema(
                    primary_driver="Delta / spot move",
                    verdict="mock verdict",
                    confidence_level="medium",
                    confidence_rationale="r",
                    evidence=[],
                    takeaways=[],
                    american_commentary="",
                )
            if name == "DiagnosticVerifierResult":
                return schema(verdict="PASS", missing_evidence=[], policy_flags=[], rationale="mock llm rationale")
            return schema(relevant=[], discarded=[], mechanisms=[], brief="", reason="")

    roles = LlmRoleRegistry(
        narrator=_MockRole(), verifier=_MockRole(), challenger=_MockRole(), digester=_MockRole()
    )
    app = build_leg_diagnosis_subgraph(
        config=PipelineConfig(features={"a1", "a2", "a3"}, verify_budget=1), roles=roles
    )
    # vol_crush's residual is well below the ratio band but its |ΔP| is
    # well above the materiality floor (A7.2's second gate), so it still
    # reaches the narrator/verifier -- see the A5/A7 commit FINDINGS.
    leg = BookLegSpec(leg_id="demo", fixture="vol_crush", ticker="AAPL")
    out = app.invoke({"leg": leg})
    assert out.get("no_escalation") is not True
    assert out.get("llm_calls", 0) >= 2  # synthesize + verify, at minimum


if __name__ == "__main__":
    test_no_escalation_makes_zero_llm_calls()
    test_terminal_no_comparable_observation_makes_zero_llm_calls()
    test_normal_pass_run_counts_at_least_two_llm_calls()
    print("OK — LLM call budget tests passed")
