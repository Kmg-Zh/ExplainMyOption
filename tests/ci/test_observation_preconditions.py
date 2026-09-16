"""Observation-continuity gate: Task A3.1/A3.2/A3.6.

One fixture per ``ObservationStatus``, asserting the correct terminal state,
no pricing, no LLM call -- and that the abstain state is never reported as
``terminal_unexplained_break`` (that says the market did something the
model didn't capture; this says no comparison was possible at all).
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

from explain_my_option.data.observation import (
    NO_COMPARABLE_OBSERVATION_TEMPLATE,
    NoComparableObservationError,
    ObservationStatus,
    classify_observation_status,
    continuity_gate,
)
from explain_my_option.graph.deps import GraphDeps
from explain_my_option.pipeline.book_schema import BookLegSpec
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.leg_graph import build_leg_diagnosis_subgraph


def test_classify_observation_status_day_missing():
    status = classify_observation_status(
        reference_row_counts={"SPY": 0, "AAPL": 0, "GME": 0}, contract_rows=0
    )
    assert status is ObservationStatus.DAY_MISSING


def test_classify_observation_status_contract_missing():
    status = classify_observation_status(
        reference_row_counts={"SPY": 120, "AAPL": 95, "GME": 40}, contract_rows=0
    )
    assert status is ObservationStatus.CONTRACT_MISSING


def test_classify_observation_status_ok():
    status = classify_observation_status(
        reference_row_counts={"SPY": 120, "AAPL": 95, "GME": 40}, contract_rows=6
    )
    assert status is ObservationStatus.OK


def test_continuity_gate_passes_when_both_ok():
    continuity_gate(
        contract="GME 2021-02-19 55P",
        status_t1=ObservationStatus.OK,
        status_t=ObservationStatus.OK,
        date_t1="2021-01-22",
        date_t="2021-01-25",
    )


def test_continuity_gate_raises_with_verbatim_report_text():
    try:
        continuity_gate(
            contract="GME 2021-02-19 55P",
            status_t1=ObservationStatus.OK,
            status_t=ObservationStatus.DAY_MISSING,
            date_t1="2021-01-22",
            date_t="2021-01-25",
        )
        raise AssertionError("expected NoComparableObservationError")
    except NoComparableObservationError as exc:
        expected = NO_COMPARABLE_OBSERVATION_TEMPLATE.format(
            contract="GME 2021-02-19 55P",
            status_t1="OK",
            status_t="DAY_MISSING",
            date_t1="2021-01-22",
            date_t="2021-01-25",
        )
        assert exc.report_text() == expected
        assert "unexplained market move" in exc.report_text()
        assert "data coverage limitation" in exc.report_text()


@dataclass
class _NoComparableObservationLoader:
    status_t: ObservationStatus

    def load(self, *, ticker, option_type, strike, expiry):
        raise NoComparableObservationError(
            contract=f"{ticker} {option_type}",
            status_t1=ObservationStatus.OK,
            status_t=self.status_t,
            date_t1="t-1",
            date_t="t",
        )


@dataclass
class _FailIfCalledPnl:
    def attribute(self, snapshot, surface_data=None, surface_prev=None):
        raise AssertionError("pricing must not run past a continuity-gate failure")


def _leg() -> BookLegSpec:
    return BookLegSpec(leg_id="demo", fixture=None, ticker="GME", strike=55.0)


def test_day_missing_terminates_without_pricing_or_llm():
    deps = GraphDeps(
        market=_NoComparableObservationLoader(ObservationStatus.DAY_MISSING),
        pnl=_FailIfCalledPnl(),
    )
    app = build_leg_diagnosis_subgraph(
        config=PipelineConfig(features={"a1", "a2", "a3"}, verify_budget=0),
        deps=deps,
    )
    out = app.invoke({"leg": _leg()})
    assert out.get("terminal_no_comparable_observation") is True
    assert out.get("observation_status_t") == "DAY_MISSING"
    assert out.get("leg_ok") is False
    assert not out.get("diagnostic_findings")
    assert "data coverage limitation" in out["report"]
    assert "No Comparable Observation" in out["report"]


def test_contract_missing_terminates_without_pricing_or_llm():
    deps = GraphDeps(
        market=_NoComparableObservationLoader(ObservationStatus.CONTRACT_MISSING),
        pnl=_FailIfCalledPnl(),
    )
    app = build_leg_diagnosis_subgraph(
        config=PipelineConfig(features={"a1", "a2", "a3"}, verify_budget=0),
        deps=deps,
    )
    out = app.invoke({"leg": _leg()})
    assert out.get("terminal_no_comparable_observation") is True
    assert out.get("observation_status_t") == "CONTRACT_MISSING"
    assert not out.get("diagnostic_findings")


def test_no_comparable_observation_is_never_terminal_unexplained_break():
    deps = GraphDeps(
        market=_NoComparableObservationLoader(ObservationStatus.DAY_MISSING),
        pnl=_FailIfCalledPnl(),
    )
    app = build_leg_diagnosis_subgraph(
        config=PipelineConfig(features={"a1", "a2", "a3"}, verify_budget=0),
        deps=deps,
    )
    out = app.invoke({"leg": _leg()})
    findings = out.get("diagnostic_findings") or {}
    assert findings.get("terminal_unexplained_break") is not True


if __name__ == "__main__":
    test_classify_observation_status_day_missing()
    test_classify_observation_status_contract_missing()
    test_classify_observation_status_ok()
    test_continuity_gate_passes_when_both_ok()
    test_continuity_gate_raises_with_verbatim_report_text()
    test_day_missing_terminates_without_pricing_or_llm()
    test_contract_missing_terminates_without_pricing_or_llm()
    test_no_comparable_observation_is_never_terminal_unexplained_break()
    print("OK — observation precondition tests passed")
