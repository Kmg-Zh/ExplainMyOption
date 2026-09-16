"""Quiet-day non-escalation: Task A7.2/A7.4.

Real quiet-day cases from scripts/find_quiet_days.py's deterministic
selection (tests/ci/fixtures/quiet_days/quiet_days_2023.json), fetched as
frozen slices by scripts/fetch_chains.py -- offline, no network in CI.

Every clause of A7.2 must hold: escalation_metric below the lower severity
band, zero costly tools, no search, no catalyst claim, terminal state
no_escalation. A quiet day that triggers a search is a FAIL.
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
from explain_my_option.data_loader import LoadedData
from explain_my_option.graph.deps import GraphDeps, OfficialFdmPnlSource
from explain_my_option.graph.diagnostic_controller import LOW_SEVERITY_THRESHOLD_PCT
from explain_my_option.pipeline.book_schema import BookLegSpec
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.leg_graph import NO_ESCALATION_TEXT, build_leg_diagnosis_subgraph
from explain_my_option.pipeline.llm_roles import LlmRoleRegistry
from explain_my_option.pricing.facade import price_and_attribute
from explain_my_option.report.reconciliation import build_reconciliation_facts

QUIET_CASES = [
    "quiet_aapl_2023-04-24",
    "quiet_spy_2023-03-06",
    "quiet_spy_2023-04-24",
]


@dataclass
class _SnapshotLoader:
    name: str

    def load(self, *, ticker, option_type, strike, expiry):
        snap = load_historical_case(self.name)
        return LoadedData(snapshot=snap, news=[], surface=None, surface_prev=None)


@dataclass
class _FailIfCalled:
    def structured_invoke(self, *, system, human, schema):
        raise AssertionError(f"LLM must not be called on a no_escalation day ({schema.__name__})")


def _run_quiet_case(name: str) -> dict:
    deps = GraphDeps(
        market=_SnapshotLoader(name), pnl=OfficialFdmPnlSource(config=engine_config_for_tests())
    )
    roles = LlmRoleRegistry(
        narrator=_FailIfCalled(),
        verifier=_FailIfCalled(),
        challenger=_FailIfCalled(),
        digester=_FailIfCalled(),
    )
    app = build_leg_diagnosis_subgraph(
        config=PipelineConfig(features={"a1", "a2", "a3"}, verify_budget=1),
        deps=deps,
        roles=roles,
    )
    snap = load_historical_case(name)
    leg = BookLegSpec(leg_id=name, fixture=None, ticker=snap.ticker, strike=snap.strike, expiry=snap.expiry)
    return app.invoke({"leg": leg})


def test_all_three_quiet_cases_reach_no_escalation():
    for name in QUIET_CASES:
        out = _run_quiet_case(name)
        assert out.get("no_escalation") is True, name
        findings = out.get("diagnostic_findings") or {}
        assert findings.get("no_escalation") is True, name


def test_quiet_case_runs_zero_costly_tools():
    for name in QUIET_CASES:
        out = _run_quiet_case(name)
        findings = out.get("diagnostic_findings") or {}
        costs = findings.get("tool_costs") or {}
        costly = [tool for tool, cost in costs.items() if cost == "costly"]
        assert costly == [], (name, costly)


def test_quiet_case_performs_no_search():
    for name in QUIET_CASES:
        out = _run_quiet_case(name)
        assert out.get("search_plan") is None, name
        assert not out.get("news"), name


def test_quiet_case_makes_no_catalyst_claim():
    for name in QUIET_CASES:
        out = _run_quiet_case(name)
        synthesis = out["diagnostic_synthesis"]
        assert synthesis["verdict"] == NO_ESCALATION_TEXT, name
        assert synthesis["evidence"] == [], name


def test_quiet_case_escalation_metric_below_lower_band():
    for name in QUIET_CASES:
        snap = load_historical_case(name)
        pricing = price_and_attribute(snap, config=engine_config_for_tests())
        rec = build_reconciliation_facts(snap, pricing)
        assert rec.escalation_metric_pct <= LOW_SEVERITY_THRESHOLD_PCT, (
            name,
            rec.escalation_metric_pct,
        )


def test_quiet_case_never_reports_terminal_unexplained_break():
    for name in QUIET_CASES:
        out = _run_quiet_case(name)
        findings = out.get("diagnostic_findings") or {}
        assert findings.get("terminal_unexplained_break") is not True, name


if __name__ == "__main__":
    test_all_three_quiet_cases_reach_no_escalation()
    test_quiet_case_runs_zero_costly_tools()
    test_quiet_case_performs_no_search()
    test_quiet_case_makes_no_catalyst_claim()
    test_quiet_case_escalation_metric_below_lower_band()
    test_quiet_case_never_reports_terminal_unexplained_break()
    print("OK — quiet-day non-escalation tests passed")
