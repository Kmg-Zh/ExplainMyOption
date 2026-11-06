"""One option leg, as a LangGraph subgraph.

fetch_market → quant → blotter → diagnostic_pass → plan_search → search →
digest_news → challenge_catalyst → synthesize → reconcile_debate → verify →
finalize_leg_report. Market, pricing, blotter and diagnostics use no LLM. A
quiet day ends after ``diagnostic_pass`` with a fixed report; a data or basis
failure ends at ``leg_failure_finalize`` before any pricing. A leg whose
session is on or after its expiry ends at ``settle_expiry``: intrinsic value
at the expiry close, with no pricing, LLM or search.
"""

from __future__ import annotations

import time
from dataclasses import replace
from typing import Any, Callable, Literal

from langgraph.graph import END, START, StateGraph

from ..data.observation import (
    DataBreakError,
    NoComparableObservationError,
    check_basis_consistency,
    check_calibrated_iv,
    check_mark_bounds,
)
from ..graph.deps import FixtureMarketLoader, GraphDeps, default_deps, fixture_deps
from ..graph.diagnostic_controller import run_diagnostic_pass
from ..graph.playbook import select_records
from ..graph.state import OptionState
from ..intel.types import SearchPlan
from ..report import PositionBundle, render_portfolio_report, synthesize_diagnosis
from ..report.blotter import build_quant_section
from ..report.facts import build_position_facts
from ..report.schema import DiagnosticSynthesis
from ..report.settlement import ExpirySettlement, is_settlement, render_settlement, settle
from .book_schema import BookLegSpec
from .challenger import reconcile_with_challenge, run_catalyst_challenge
from .config import PipelineConfig
from .digest import IntelDigest, run_intel_digest
from .llm_roles import LlmRoleRegistry, default_openai_roles
from .types import LegResult
from .verifier import (
    DETERMINISTIC_PRECHECK_RATIONALES,
    HARD_FAIL_POLICY_FLAGS,
    apply_verifier_reflection,
    is_hard_verifier_fail,
    verify_synthesis,
    violation_sentence,
)
from .verifier_schema import DiagnosticVerifierResult

NO_ESCALATION_TEXT = (
    "Nothing to explain. The move is accounted for by carry and a small "
    "spot move; the unexplained portion is within tolerance. No news "
    "search was performed."
)


class LegState(OptionState, total=False):
    leg: BookLegSpec
    leg_error: str | None
    terminal_no_comparable_observation: bool
    basis_mismatch_suspected: bool
    data_break: bool
    settlement: ExpirySettlement
    no_escalation: bool
    llm_calls: int
    verifier_trace: list[dict[str, Any]]
    # Wall-clock seconds per node; observability only, never read by routing.
    stage_timings: dict[str, float]


class LegBranchState(LegState, total=False):
    leg_results: list[LegResult]


def _timed_node(name: str, fn: Callable[[LegState], dict]) -> Callable[[LegState], dict]:
    def wrapped(state: LegState) -> dict:
        t0 = time.perf_counter()
        result = fn(state) or {}
        timings = dict(state.get("stage_timings") or {})
        timings[name] = timings.get(name, 0.0) + time.perf_counter() - t0
        return {**result, "stage_timings": timings}

    return wrapped


def _resolve_ports(leg: BookLegSpec, deps: GraphDeps | None) -> GraphDeps:
    if leg.fixture:
        return replace(deps or fixture_deps(leg.fixture), market=FixtureMarketLoader(leg.fixture))
    return deps or default_deps()


def _apply_leg_overrides(snap, leg: BookLegSpec) -> None:
    snap.ticker = leg.ticker
    for key, val in leg.overrides.items():
        setattr(snap, key, val)
    if leg.strike is not None:
        snap.strike = float(leg.strike)
    if leg.expiry is not None:
        snap.expiry = leg.expiry
    snap.option_type = leg.option_type
    snap.quantity = leg.quantity
    snap.multiplier = leg.multiplier
    snap.exercise_style = leg.exercise_style


def _observation_reliable(state: LegState) -> bool:
    return bool((state.get("diagnostic_findings") or {}).get("observation_reliable", True))


def _apply_observation_lock(synthesis: DiagnosticSynthesis, *, observation_reliable: bool) -> DiagnosticSynthesis:
    """Drop catalyst evidence when the quote is too unreliable to support it."""
    if observation_reliable or not synthesis.evidence:
        return synthesis
    return synthesis.model_copy(update={"evidence": []})


def _no_escalation_synthesis() -> DiagnosticSynthesis:
    return DiagnosticSynthesis(
        primary_driver="Theta / carry",
        verdict=NO_ESCALATION_TEXT,
        confidence_level="high",
        confidence_rationale=(
            "Escalation metric is at or below the quiet-day threshold; see the "
            "Mark Reconciliation section for the exact figures."
        ),
        evidence=[],
        takeaways=["No action needed; move is within theta/carry tolerance."],
        american_commentary="",
    )


def _last_verdict(state: LegState) -> DiagnosticVerifierResult:
    trace = state.get("verifier_trace") or []
    return DiagnosticVerifierResult.model_validate(trace[-1] if trace else {"verdict": "PARTIAL"})


def build_leg_diagnosis_subgraph(
    *,
    config: PipelineConfig,
    deps: GraphDeps | None = None,
    roles: LlmRoleRegistry | None = None,
):
    roles = roles or default_openai_roles()

    def fetch_market_node(state: LegState) -> LegState:
        leg = state["leg"]
        ports = _resolve_ports(leg, deps)
        try:
            data = ports.market.load(
                ticker=state.get("ticker") or leg.ticker,
                option_type=state.get("option_type", leg.option_type),
                strike=state.get("strike") or leg.strike,
                expiry=state.get("expiry") or leg.expiry,
            )
        except NoComparableObservationError as exc:
            # A data coverage gap, never an unexplained break: nothing is priced.
            return {"leg_error": exc.report_text(), "terminal_no_comparable_observation": True}
        except DataBreakError as exc:
            return {"leg_error": exc.report_text(), "data_break": True}
        except Exception as exc:
            return {"leg_error": str(exc)}

        snap = data.snapshot
        if is_settlement(snap):
            _apply_leg_overrides(snap, leg)
            return {"snapshot": snap, "ticker": snap.ticker, "option_type": snap.option_type, "leg_error": None}
        is_call, is_put = snap.option_type == "call", snap.option_type == "put"
        basis = check_basis_consistency(
            spot=snap.spot_now,
            rate=snap.risk_free_rate,
            time_to_expiry_years=snap.time_to_expiry_years,
            call_mid=snap.mid if is_call else None,
            call_strike=snap.strike if is_call else None,
            put_mid=snap.mid if is_put else None,
            put_strike=snap.strike if is_put else None,
        )
        if basis.basis_mismatch_suspected:
            # Never apply a correction factor: report and stop.
            return {
                "leg_error": (
                    f"Basis mismatch suspected: {basis.failing_invariant} failed "
                    f"({basis.detail}). No correction applied; case aborted."
                ),
                "basis_mismatch_suspected": True,
            }
        _apply_leg_overrides(snap, leg)
        marks = check_mark_bounds(snap)
        if not marks.ok:
            return {"leg_error": marks.error().report_text(), "data_break": True}
        return {
            "snapshot": snap,
            "surface": data.surface,
            "surface_prev": data.surface_prev,
            "ticker": snap.ticker,
            "option_type": snap.option_type,
            "leg_error": None,
        }

    def route_after_fetch(state: LegState) -> Literal["quant", "settle_expiry", "leg_failure_finalize"]:
        if state.get("leg_error"):
            return "leg_failure_finalize"
        return "settle_expiry" if is_settlement(state["snapshot"]) else "quant"

    def settle_expiry_node(state: LegState) -> LegState:
        # Intrinsic value at the expiry close: no pricer, LLM or news search.
        settlement = settle(state["snapshot"])
        verdict = f"Expired at the {settlement.session} close and settled at intrinsic value ({settlement.outcome})."
        synthesis = DiagnosticSynthesis(
            primary_driver="Expiry settlement",
            verdict=verdict,
            confidence_level="high",
            confidence_rationale="Settlement is intrinsic value at the expiry close; no model is involved.",
            takeaways=[settlement.delivery()],
        )
        return {
            "settlement": settlement,
            "diagnosis": verdict,
            "diagnostic_synthesis": synthesis.model_dump(),
            "report": render_settlement(settlement),
        }

    def quant_node(state: LegState) -> LegState:
        ports = _resolve_ports(state["leg"], deps)
        try:
            pricing = ports.pnl.attribute(state["snapshot"], state.get("surface"), state.get("surface_prev"))
        except Exception as exc:
            return {"leg_error": str(exc)}
        diag = pricing.diagnostics
        if diag.mark_calibrated:
            # Calibration fits any mark it can; a mark that does not belong to
            # its spot would otherwise reach the blotter as a vol move.
            iv_check = check_calibrated_iv(
                state["snapshot"], iv_cal_now=diag.effective_iv_now, iv_cal_prev=diag.effective_iv_prev
            )
            if not iv_check.ok:
                return {"leg_error": iv_check.error().report_text(), "data_break": True}
        return {"pricing": pricing}

    def blotter_node(state: LegState) -> LegState:
        try:
            return {"blotter": build_quant_section(state["snapshot"], state["pricing"])}
        except Exception as exc:
            return {"leg_error": str(exc)}

    def diagnostic_pass_node(state: LegState) -> LegState:
        ports = _resolve_ports(state["leg"], deps)
        snap, pricing = state["snapshot"], state["pricing"]
        result = run_diagnostic_pass(snap, pricing, state.get("surface"), pnl=ports.pnl)
        out: LegState = {"diagnostic_findings": result.as_dict(), "verifier_trace": []}
        if result.no_escalation:
            out["no_escalation"] = True
            out["diagnostic_synthesis"] = _no_escalation_synthesis().model_dump()
        return out

    def plan_search_node(state: LegState) -> LegState:
        ports = _resolve_ports(state["leg"], deps)
        plan = ports.planner.plan(
            state["snapshot"], state["pricing"], observation_reliable=_observation_reliable(state)
        )
        return {"search_plan": plan}

    def search_node(state: LegState) -> LegState:
        ports = _resolve_ports(state["leg"], deps)
        plan = state.get("search_plan") or SearchPlan()
        news, skipped, failed = ports.intel.execute(plan, ticker=state.get("ticker") or state["snapshot"].ticker)
        plan = plan.model_copy(update={"skipped_sources": list(skipped), "failed_sources": list(failed)})
        return {"news": news, "search_plan": plan}

    def digest_news_node(state: LegState) -> LegState:
        digest = run_intel_digest(
            role=roles.digester,
            ticker=state.get("ticker") or state["snapshot"].ticker,
            news=state.get("news", []),
        )
        findings = {**(state.get("diagnostic_findings") or {}), "intel_digest": digest.model_dump()}
        calls = int(state.get("llm_calls", 0)) + (0 if digest.reason else 1)  # reason set = no LLM call
        return {"intel_digest": digest.model_dump(), "diagnostic_findings": findings, "llm_calls": calls}

    def challenge_catalyst_node(state: LegState) -> LegState:
        challenge = run_catalyst_challenge(
            role=roles.challenger,
            snap=state["snapshot"],
            pricing=state["pricing"],
            news=state.get("news", []),
            intel_digest=state.get("intel_digest"),
            diagnostic_findings=state.get("diagnostic_findings"),
        )
        payload = challenge.model_dump()
        findings = {**(state.get("diagnostic_findings") or {}), "catalyst_challenge": payload}
        calls = int(state.get("llm_calls", 0)) + (0 if challenge.suppress_reason else 1)
        return {"catalyst_challenge": payload, "diagnostic_findings": findings, "llm_calls": calls}

    def synthesize_node(state: LegState) -> LegState:
        ports = _resolve_ports(state["leg"], deps)
        findings = state.get("diagnostic_findings") or {}
        records = select_records(findings, ports.playbook)
        synthesis = synthesize_diagnosis(
            state["snapshot"],
            state["pricing"],
            state.get("news", []),
            plan=state.get("search_plan"),
            ports=ports,
            diagnostic_findings=findings,
            role=roles.narrator,
            playbook=records,
        )
        synthesis = _apply_observation_lock(synthesis, observation_reliable=_observation_reliable(state))
        out: LegState = {"diagnostic_synthesis": synthesis.model_dump(), "llm_calls": int(state.get("llm_calls", 0)) + 1}
        if records:
            out["diagnostic_findings"] = {
                **findings,
                "playbook_records": [{"id": r.record_id, "when": r.when} for r in records],
            }
        return out

    def reconcile_debate_node(state: LegState) -> LegState:
        synthesis = DiagnosticSynthesis.model_validate(state.get("diagnostic_synthesis") or {})
        merged = reconcile_with_challenge(synthesis, state.get("catalyst_challenge"))
        return {"diagnostic_synthesis": merged.model_dump()}

    def route_verify_gate(state: LegState) -> Literal["verify", "finalize_leg_report"]:
        return "verify" if config.verify else "finalize_leg_report"

    def verify_node(state: LegState) -> LegState:
        synthesis = DiagnosticSynthesis.model_validate(state.get("diagnostic_synthesis") or {})
        findings = state.get("diagnostic_findings") or {}
        digest = IntelDigest.model_validate(state.get("intel_digest") or {})
        facts = build_position_facts(state["snapshot"], state["pricing"], news_count=len(state.get("news", [])))
        verdict = verify_synthesis(
            synthesis,
            facts,
            role=roles.verifier,
            suppress_vega=bool(findings.get("suppress_vega_narrative")),
            observation_reliable=bool(findings.get("observation_reliable", True)),
            news_titles=[item.title for item in digest.relevant if item.title],
            catalyst_challenge=state.get("catalyst_challenge"),
            no_escalation=bool(findings.get("no_escalation")),
            news=list(state.get("news") or []),
            as_of=state["snapshot"].as_of,
        )
        trace = [*(state.get("verifier_trace") or []), verdict.model_dump()]
        # Precheck verdicts carry fixed, code-authored rationales; only the
        # others came from an LLM call.
        calls = int(state.get("llm_calls", 0)) + (verdict.rationale not in DETERMINISTIC_PRECHECK_RATIONALES)
        # Audit trail: the candidate the verifier saw plus every verdict.
        audit = dict(findings.get("verifier_audit") or {})
        audit.setdefault("candidates", []).append(synthesis.model_dump())
        audit["trace"] = trace
        return {
            "verifier_trace": trace,
            "llm_calls": calls,
            "diagnostic_findings": {**findings, "verifier_audit": audit},
        }

    def route_verify_result(
        state: LegState,
    ) -> Literal["finalize_leg_report", "reflect_verifier", "terminal_unexplained_break"]:
        verdict = _last_verdict(state)
        if verdict.verdict == "PASS":
            return "finalize_leg_report"
        if verdict.verdict == "FAIL" and is_hard_verifier_fail(verdict):
            return "terminal_unexplained_break"
        return "reflect_verifier"

    def reflect_verifier_node(state: LegState) -> LegState:
        verdict = _last_verdict(state)
        synthesis = apply_verifier_reflection(
            DiagnosticSynthesis.model_validate(state.get("diagnostic_synthesis") or {}),
            verdict,
            observation_reliable=_observation_reliable(state),
        )
        findings = {
            **(state.get("diagnostic_findings") or {}),
            "verifier_status": "PARTIAL",
            "verifier_reflect": verdict.model_dump(),
        }
        return {"diagnostic_findings": findings, "diagnostic_synthesis": synthesis.model_dump()}

    def terminal_unexplained_break_node(state: LegState) -> LegState:
        verdict = _last_verdict(state)
        flags = [f for f in verdict.policy_flags if f in HARD_FAIL_POLICY_FLAGS]
        sentence = violation_sentence(verdict)
        flag_text = ", ".join(flags) or "policy"
        missing = list(verdict.missing_evidence or [])
        synthesis = DiagnosticSynthesis.model_validate(state.get("diagnostic_synthesis") or {})
        synthesis = synthesis.model_copy(
            update={
                "verdict": f"Verifier FAIL — terminal break escalation ({flag_text})."
                + (f" {sentence}" if sentence else ""),
                "takeaways": [
                    f"Verifier flags: {flag_text}"
                    + (f"; missing evidence: {', '.join(missing)}" if missing else ""),
                    *synthesis.takeaways,
                ],
            }
        )
        findings = {
            **(state.get("diagnostic_findings") or {}),
            "terminal_unexplained_break": True,
            "verifier_status": "FAIL",
            "terminal_cause": "verifier_hard_fail",
            "terminal_verifier_flags": flags,
            "terminal_violation": sentence,
        }
        return {"diagnostic_findings": findings, "diagnostic_synthesis": synthesis.model_dump()}

    def finalize_leg_report_node(state: LegState) -> LegState:
        synthesis = DiagnosticSynthesis.model_validate(state.get("diagnostic_synthesis") or {})
        bundle = PositionBundle(
            snapshot=state["snapshot"],
            pricing=state["pricing"],
            news=state.get("news", []),
            plan=state.get("search_plan"),
        )
        report = render_portfolio_report([bundle], [synthesis], leg_findings=[state.get("diagnostic_findings") or {}])
        return {"diagnosis": synthesis.verdict.strip(), "report": report}

    def leg_failure_finalize_node(state: LegState) -> LegState:
        msg = state.get("leg_error") or "Leg failed before report finalization."
        if state.get("terminal_no_comparable_observation"):
            heading = "## No Comparable Observation"
            takeaway = "No pricing or news search was performed; this is a data coverage limitation."
        elif state.get("basis_mismatch_suspected"):
            heading = "## Basis Mismatch Suspected"
            takeaway = "No pricing was performed; the raw quotes failed a basis-consistency check."
        elif state.get("data_break"):
            heading = "## Data Break"
            takeaway = "No narrative or news search; fix the market data for this leg and rerun."
        else:
            heading = "## Leg Failure"
            takeaway = "Inspect fixture or market input for this leg."
        synthesis = DiagnosticSynthesis(
            primary_driver="Unresolved",
            verdict=msg,
            confidence_level="low",
            confidence_rationale=msg,
            takeaways=[takeaway],
        )
        return {"diagnosis": msg, "diagnostic_synthesis": synthesis.model_dump(), "report": f"{heading}\n\n{msg}\n"}

    def on_error(next_node: str) -> Callable[[LegState], str]:
        return lambda state: "leg_failure_finalize" if state.get("leg_error") else next_node

    graph = StateGraph(LegState)
    for name, fn in (
        ("fetch_market", fetch_market_node),
        ("settle_expiry", settle_expiry_node),
        ("quant", quant_node),
        ("blotter", blotter_node),
        ("diagnostic_pass", diagnostic_pass_node),
        ("plan_search", plan_search_node),
        ("search", search_node),
        ("digest_news", digest_news_node),
        ("challenge_catalyst", challenge_catalyst_node),
        ("synthesize", synthesize_node),
        ("reconcile_debate", reconcile_debate_node),
        ("verify", verify_node),
        ("reflect_verifier", reflect_verifier_node),
        ("terminal_unexplained_break", terminal_unexplained_break_node),
        ("finalize_leg_report", finalize_leg_report_node),
        ("leg_failure_finalize", leg_failure_finalize_node),
    ):
        graph.add_node(name, _timed_node(name, fn))

    graph.add_edge(START, "fetch_market")
    graph.add_conditional_edges(
        "fetch_market", route_after_fetch, ["quant", "settle_expiry", "leg_failure_finalize"]
    )
    graph.add_edge("settle_expiry", END)
    graph.add_conditional_edges("quant", on_error("blotter"), ["blotter", "leg_failure_finalize"])
    graph.add_conditional_edges("blotter", on_error("diagnostic_pass"), ["diagnostic_pass", "leg_failure_finalize"])
    graph.add_conditional_edges(
        "diagnostic_pass",
        lambda state: "finalize_leg_report" if state.get("no_escalation") else "plan_search",
        ["plan_search", "finalize_leg_report"],
    )
    graph.add_edge("plan_search", "search")
    graph.add_edge("search", "digest_news")
    graph.add_edge("digest_news", "challenge_catalyst")
    graph.add_edge("challenge_catalyst", "synthesize")
    graph.add_edge("synthesize", "reconcile_debate")
    graph.add_conditional_edges("reconcile_debate", route_verify_gate, ["verify", "finalize_leg_report"])
    graph.add_conditional_edges(
        "verify",
        route_verify_result,
        ["finalize_leg_report", "reflect_verifier", "terminal_unexplained_break"],
    )
    graph.add_edge("reflect_verifier", "finalize_leg_report")
    graph.add_edge("terminal_unexplained_break", "finalize_leg_report")
    graph.add_edge("finalize_leg_report", END)
    graph.add_edge("leg_failure_finalize", END)
    return graph.compile()


def build_leg_branch_subgraph(
    *,
    config: PipelineConfig,
    deps: GraphDeps | None = None,
    roles: LlmRoleRegistry | None = None,
):
    """The leg subgraph plus a packing node that emits one ``LegResult`` for the book."""
    leg_graph = build_leg_diagnosis_subgraph(config=config, deps=deps, roles=roles)

    def pack_leg_result_node(state: LegBranchState) -> LegBranchState:
        settlement = state.get("settlement")
        diagnosed = bool(state.get("pricing")) and settlement is None
        ok = not state.get("leg_error") and bool(state.get("snapshot")) and (diagnosed or settlement is not None)
        error = None if ok else (state.get("leg_error") or "leg pipeline failed")
        bundle = (
            PositionBundle(
                snapshot=state["snapshot"],
                pricing=state["pricing"],
                news=state.get("news", []),
                plan=state.get("search_plan"),
            )
            if ok and diagnosed
            else None
        )
        result: LegResult = {
            "leg_id": state["leg"].leg_id,
            "ok": ok,
            "error": error,
            "bundle": bundle,
            "settlement": settlement,
            "synthesis": state.get("diagnostic_synthesis"),
            "diagnostic_findings": state.get("diagnostic_findings") or {},
            "report": state.get("report", ""),
            "blotter": state.get("blotter", ""),
            "diagnosis": state.get("diagnosis", error or ""),
            "stage_timings": state.get("stage_timings") or {},
            "llm_calls": state.get("llm_calls"),
            "no_escalation": bool(state.get("no_escalation")),
            "terminal_no_comparable_observation": bool(state.get("terminal_no_comparable_observation")),
        }
        return {"leg_results": [result]}

    graph = StateGraph(LegBranchState)
    graph.add_node("leg_pipeline", leg_graph)
    graph.add_node("pack_leg_result", pack_leg_result_node)
    graph.add_edge(START, "leg_pipeline")
    graph.add_edge("leg_pipeline", "pack_leg_result")
    graph.add_edge("pack_leg_result", END)
    return graph.compile()
