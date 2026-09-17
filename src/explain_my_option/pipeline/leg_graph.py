"""Unified leg pipeline with explicit A2/A3 control-flow nodes."""

from __future__ import annotations

import time
from typing import Any, Callable, Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from ..data.observation import NoComparableObservationError, check_basis_consistency
from ..graph.deps import FixtureMarketLoader, GraphDeps, default_deps, fixture_deps
from ..graph.diagnostic_controller import (
    LOW_SEVERITY_THRESHOLD_PCT,
    NO_ESCALATION_MATERIALITY_ABS_USD,
    NO_ESCALATION_MATERIALITY_PCT_OF_MID,
    run_diagnostic_pass,
)
from ..graph.state import OptionState
from ..intel.types import SearchPlan
from ..report import PositionBundle, render_portfolio_report, synthesize_diagnosis
from ..report.facts import build_position_facts
from ..report.reconciliation import build_reconciliation_facts
from ..report.schema import DiagnosticSynthesis
from ..report_generator import build_quant_section
from ..report.synthesis import fallback_synthesis, synthesis_to_legacy_diagnosis
from .challenger import reconcile_with_challenge, run_catalyst_challenge
from .digest import IntelDigest, coarse_kept_news, run_intel_digest
from .book_schema import BookLegSpec
from .config import PipelineConfig
from .diagnostic_loop import (
    choose_a2_tool,
    compute_residual_pct,
    execute_diagnostic_tool,
    merge_iteration,
)
from .llm_roles import LlmRole, LlmRoleRegistry, OpenAiRole, default_openai_roles
from .types import LegResult
from .verifier import (
    DETERMINISTIC_PRECHECK_RATIONALES,
    apply_verifier_reflection,
    is_hard_verifier_fail,
    verify_synthesis,
)


def _timed_node(name: str, fn: Callable[["LegState"], dict]) -> Callable[["LegState"], dict]:
    """B4: wrap a node with wall-clock timing into ``state["stage_timings"]``.

    Pure observability -- times the node's own body, merges the elapsed
    seconds into whatever dict the node already returns, and changes no
    routing/decision. See docs/studies/agent_budget.md.
    """

    def wrapped(state: "LegState") -> dict:
        t0 = time.perf_counter()
        result = fn(state) or {}
        elapsed = time.perf_counter() - t0
        timings = dict(state.get("stage_timings") or {})
        timings[name] = timings.get(name, 0.0) + elapsed
        return {**result, "stage_timings": timings}

    return wrapped


# A7.3: verbatim, terminal no_escalation report text.
NO_ESCALATION_TEXT = (
    "Nothing to explain. The move is accounted for by carry and a small "
    "spot move; the unexplained portion is within tolerance. No news "
    "search was performed."
)


class LegState(OptionState, total=False):
    leg: BookLegSpec
    leg_error: str | None
    leg_ok: bool
    terminal_no_comparable_observation: bool
    observation_status_t1: str
    observation_status_t: str
    basis_mismatch_suspected: bool
    no_escalation: bool
    llm_calls: int
    diag_budget_remaining: int
    diag_iterations: int
    diag_tool_history: list[dict[str, Any]]
    diag_residual_pct: float
    diag_next_tool: str
    catalyst_challenge: dict[str, Any]
    verifier_trace: list[dict[str, Any]]
    verify_budget_remaining: int
    # B4: wall-clock per node, keyed by graph node name -- pure observability,
    # no effect on routing/decisions. See docs/studies/agent_budget.md.
    stage_timings: dict[str, float]


class LegBranchState(LegState, total=False):
    leg_results: list[LegResult]


def _resolve_ports(leg: BookLegSpec, deps: GraphDeps | None) -> GraphDeps:
    if leg.fixture:
        base = deps or fixture_deps(leg.fixture)
        return GraphDeps(
            market=FixtureMarketLoader(leg.fixture),
            pnl=base.pnl,
            planner=base.planner,
            intel=base.intel,
            diagnose_system_prompt=base.diagnose_system_prompt,
            diagnose_system_extra=base.diagnose_system_extra,
        )
    return deps or default_deps()


def _apply_leg_overrides(state: LegState, leg: BookLegSpec) -> None:
    snap = state["snapshot"]
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


def _synthesize_with_role(
    *,
    role: LlmRole,
    state: LegState,
    ports: GraphDeps,
) -> DiagnosticSynthesis:
    if isinstance(role, OpenAiRole):
        return synthesize_diagnosis(
            state["snapshot"],
            state["pricing"],
            state.get("news", []),
            plan=state.get("search_plan"),
            ports=ports,
            diagnostic_findings=state.get("diagnostic_findings"),
            role=role,
        )
    facts = build_position_facts(
        state["snapshot"], state["pricing"], news_count=len(state.get("news", []))
    )
    system = (
        "Return DiagnosticSynthesis JSON only. Cover Layer A (dominant Taylor driver) "
        "and Layer B (headline catalysts). Residual truncation does not replace the tape."
    )
    findings = state.get("diagnostic_findings") or {}
    digest = IntelDigest.model_validate(
        state.get("intel_digest") or findings.get("intel_digest") or {}
    )
    titles = [n.title for n in coarse_kept_news(state.get("news", [])) if n.title]
    if not titles:
        titles = [item.title for item in digest.relevant if item.title]
    human = (
        f"Contract: {facts.contract_label}\n"
        f"Primary driver: {facts.primary_driver}\n"
        f"Confidence: {facts.confidence}\n"
        f"Observation reliable: {bool(findings.get('observation_reliable', True))}\n"
        f"Tools run: {', '.join(findings.get('tools_run', [])) or 'none'}\n"
        f"Digest brief: {digest.brief or 'none'}\n"
        f"News titles: {titles[:5]}\n"
        "Cover Layer A (dominant Taylor driver) and any named headline catalysts "
        "(IV crush, borrow, squeeze, float, ex-div) in verdict and takeaways.\n"
    )
    try:
        syn = role.structured_invoke(
            system=system,
            human=human,
            schema=DiagnosticSynthesis,
        )
        if isinstance(syn, DiagnosticSynthesis):
            return syn
        return DiagnosticSynthesis.model_validate(syn)
    except Exception:
        layer_b = coarse_kept_news(state.get("news", []))
        if not layer_b:
            layer_b = state.get("news", [])
        return fallback_synthesis(
            facts,
            llm_failed=True,
            diagnostic_findings=findings,
            news=layer_b,
        )


def _apply_observation_lock_to_synthesis(
    synthesis: DiagnosticSynthesis, findings: dict[str, Any] | None
) -> DiagnosticSynthesis:
    """Drop catalyst evidence when quote reliability is locked."""
    if bool((findings or {}).get("observation_reliable", True)):
        return synthesis
    if not synthesis.evidence:
        return synthesis
    return synthesis.model_copy(update={"evidence": []})


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
            # A3.2: a data coverage gap, never reported as an unexplained
            # break. No pricing call below this point.
            return {
                "leg_ok": False,
                "leg_error": exc.report_text(),
                "terminal_no_comparable_observation": True,
                "observation_status_t1": exc.status_t1.value,
                "observation_status_t": exc.status_t.value,
            }
        except Exception as exc:
            return {"leg_ok": False, "leg_error": str(exc)}

        snap = data.snapshot
        basis = check_basis_consistency(
            spot=snap.spot_now,
            rate=snap.risk_free_rate,
            time_to_expiry_years=snap.time_to_expiry_years,
            call_mid=snap.mid if snap.option_type == "call" else None,
            call_strike=snap.strike if snap.option_type == "call" else None,
            put_mid=snap.mid if snap.option_type == "put" else None,
            put_strike=snap.strike if snap.option_type == "put" else None,
        )
        if basis.basis_mismatch_suspected:
            # A3.5: never apply a correction factor -- report and stop.
            return {
                "leg_ok": False,
                "leg_error": (
                    f"Basis mismatch suspected: {basis.failing_invariant} failed "
                    f"({basis.detail}). No correction applied; case aborted."
                ),
                "basis_mismatch_suspected": True,
            }

        next_state: LegState = {
            "snapshot": data.snapshot,
            "surface": data.surface,
            "surface_prev": data.surface_prev,
            "ticker": data.snapshot.ticker,
            "option_type": data.snapshot.option_type,
            "leg_ok": True,
            "leg_error": None,
        }
        _apply_leg_overrides(next_state, leg)
        return next_state

    def route_after_fetch(state: LegState) -> Literal["quant", "leg_failure_finalize"]:
        if state.get("leg_error"):
            return "leg_failure_finalize"
        return "quant"

    def quant_node(state: LegState) -> LegState:
        leg = state["leg"]
        ports = _resolve_ports(leg, deps)
        try:
            return {
                "pricing": ports.pnl.attribute(
                    state["snapshot"],
                    state.get("surface"),
                    state.get("surface_prev"),
                )
            }
        except Exception as exc:
            return {"leg_ok": False, "leg_error": str(exc)}

    def route_after_quant(state: LegState) -> Literal["blotter", "leg_failure_finalize"]:
        if state.get("leg_error"):
            return "leg_failure_finalize"
        return "blotter"

    def blotter_node(state: LegState) -> LegState:
        try:
            return {
                "blotter": build_quant_section(state["snapshot"], state["pricing"])
            }
        except Exception as exc:
            return {"leg_ok": False, "leg_error": str(exc)}

    def diagnostic_pass_node(state: LegState) -> LegState:
        leg = state["leg"]
        ports = _resolve_ports(leg, deps)
        cfg = getattr(ports.pnl, "config", None)
        findings = run_diagnostic_pass(
            state["snapshot"],
            state["pricing"],
            state.get("surface"),
            config=cfg,
        )
        return {
            "diagnostic_findings": findings.as_dict(),
            "diag_budget_remaining": config.diag_budget,
            "diag_iterations": 0,
            "diag_tool_history": [],
            "diag_residual_pct": compute_residual_pct(state["pricing"]),
            "diag_next_tool": "",
            "verify_budget_remaining": config.verify_budget,
            "verifier_trace": [],
        }

    def route_residual_gate(
        state: LegState,
    ) -> Literal["react_plan", "diag_finalize"]:
        budget = int(state.get("diag_budget_remaining", 0))
        iterations = int(state.get("diag_iterations", 0))
        residual = float(state.get("diag_residual_pct", 0.0))
        if budget <= 0 or iterations >= config.diag_iterations:
            return "diag_finalize"
        next_tool = choose_a2_tool(
            residual_pct=residual,
            tools_run=list((state.get("diagnostic_findings") or {}).get("tools_run") or []),
        )
        if next_tool is None:
            return "diag_finalize"
        return "react_plan"

    def react_plan_node(state: LegState) -> LegState:
        residual = float(state.get("diag_residual_pct", 0.0))
        next_tool = choose_a2_tool(
            residual_pct=residual,
            tools_run=list((state.get("diagnostic_findings") or {}).get("tools_run") or []),
        )
        return {"diag_next_tool": next_tool or ""}

    def react_tool_exec_node(state: LegState) -> LegState:
        leg = state["leg"]
        ports = _resolve_ports(leg, deps)
        cfg = getattr(ports.pnl, "config", None)
        tool_name = state.get("diag_next_tool")
        if not tool_name:
            return {}
        residual_before = float(state.get("diag_residual_pct", 0.0))
        payload = execute_diagnostic_tool(
            tool_name=tool_name,
            snap=state["snapshot"],
            pricing=state["pricing"],
            surface=state.get("surface"),
            engine_config=cfg,
        )
        next_budget = int(state.get("diag_budget_remaining", config.diag_budget)) - 1
        next_iterations = int(state.get("diag_iterations", 0)) + 1
        next_residual = residual_before
        # path_reprice (A5.1: the only tool this loop can still pick --
        # taylor_second_order is free and already ran upstream) reports its
        # own audited residual; use it so the gate below sees progress
        # instead of looping on a stale pre-reprice number.
        if tool_name == "path_reprice" and "residual_vs_model" in payload:
            next_residual = abs(
                100.0
                * float(payload["residual_vs_model"])
                / max(abs(state["pricing"].pnl.total_pnl), 1e-12)
            )
        merged = merge_iteration(
            findings=state.get("diagnostic_findings") or {},
            tool_name=tool_name,
            payload=payload,
            residual_before=residual_before,
            budget_remaining=next_budget,
            iterations=next_iterations,
        )
        return {
            "diagnostic_findings": merged,
            "diag_budget_remaining": next_budget,
            "diag_iterations": next_iterations,
            "diag_residual_pct": next_residual,
            "diag_next_tool": "",
        }

    def route_budget_gate(
        state: LegState,
    ) -> Literal["residual_gate", "diag_finalize"]:
        budget = int(state.get("diag_budget_remaining", 0))
        iterations = int(state.get("diag_iterations", 0))
        if budget <= 0 or iterations >= config.diag_iterations:
            return "diag_finalize"
        return "residual_gate"

    def diag_finalize_node(state: LegState) -> LegState:
        findings = dict(state.get("diagnostic_findings") or {})
        if int(state.get("diag_budget_remaining", 0)) <= 0 and float(
            state.get("diag_residual_pct", 0.0)
        ) > 15.0:
            findings["terminal_unexplained_break"] = True

        # A7.2/A7.3: nothing to explain -- deterministic, no LLM call, no
        # search. Computed directly from build_reconciliation_facts (A6)
        # rather than read back off reconcile_mark_vs_model's tool-call
        # result: that tool only runs when snap.option_price_now/prev are
        # both positive (a pre-existing, unrelated gate in this function,
        # above), which most synthetic fixtures leave at 0 -- the metric
        # itself is always computable from state["snapshot"]/["pricing"].
        rec = build_reconciliation_facts(state["snapshot"], state["pricing"])
        metric = rec.escalation_metric_pct
        # A7.2's ratio gate alone would also fire on a large, dramatic
        # move the Taylor decomposition happens to explain well (e.g. a
        # vol crush with near-zero residual) -- not "nothing to explain."
        # Require the move itself to be small too.
        snap = state["snapshot"]
        mid = snap.mid or snap.option_price_prev
        if mid and mid > 0:
            materiality_floor = NO_ESCALATION_MATERIALITY_PCT_OF_MID * mid
        else:
            materiality_floor = NO_ESCALATION_MATERIALITY_ABS_USD
        materiality_floor *= snap.position_scale()  # rec.model_pnl_usd is position-scaled
        no_escalation = (
            not findings.get("terminal_unexplained_break")
            and metric <= LOW_SEVERITY_THRESHOLD_PCT
            and abs(rec.model_pnl_usd) < materiality_floor
        )
        out: LegState = {"diagnostic_findings": findings}
        if no_escalation:
            findings["no_escalation"] = True
            synthesis = DiagnosticSynthesis(
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
            out["diagnostic_synthesis"] = synthesis.model_dump()
            out["no_escalation"] = True
        return out

    def route_after_diag_finalize(
        state: LegState,
    ) -> Literal["plan_search", "finalize_leg_report"]:
        # A7.2: no search on a no_escalation day -- reuses the existing
        # finalize_leg_report node (no new node), skipping
        # plan_search/search/digest_news/challenge_catalyst/synthesize/
        # verify entirely.
        if bool(state.get("no_escalation")):
            return "finalize_leg_report"
        return "plan_search"

    def plan_search_node(state: LegState) -> LegState:
        leg = state["leg"]
        ports = _resolve_ports(leg, deps)
        findings = state.get("diagnostic_findings") or {}
        obs = bool(findings.get("observation_reliable", True))
        return {
            "search_plan": ports.planner.plan(
                state["snapshot"],
                state["pricing"],
                observation_reliable=obs,
            )
        }

    def search_node(state: LegState) -> LegState:
        leg = state["leg"]
        ports = _resolve_ports(leg, deps)
        ticker = state.get("ticker") or state["snapshot"].ticker
        plan = state.get("search_plan") or SearchPlan()
        news, skipped, failed = ports.intel.execute(plan, ticker=ticker)
        plan = plan.model_copy(
            update={"skipped_sources": list(skipped), "failed_sources": list(failed)}
        )
        return {"news": news, "search_plan": plan}

    def digest_news_node(state: LegState) -> LegState:
        ticker = state.get("ticker") or state["snapshot"].ticker
        digest = run_intel_digest(
            role=roles.digester,
            ticker=ticker,
            news=state.get("news", []),
        )
        findings = dict(state.get("diagnostic_findings") or {})
        findings["intel_digest"] = digest.model_dump()
        calls = int(state.get("llm_calls", 0))
        if not digest.reason:  # A9.1: only count an actual LLM invocation
            calls += 1
        return {
            "intel_digest": digest.model_dump(),
            "diagnostic_findings": findings,
            "llm_calls": calls,
        }

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
        findings = dict(state.get("diagnostic_findings") or {})
        findings["catalyst_challenge"] = payload
        calls = int(state.get("llm_calls", 0))
        if not challenge.suppress_reason:  # A9.1: only count an actual LLM invocation
            calls += 1
        return {"catalyst_challenge": payload, "diagnostic_findings": findings, "llm_calls": calls}

    def synthesize_node(state: LegState) -> LegState:
        leg = state["leg"]
        ports = _resolve_ports(leg, deps)
        findings = state.get("diagnostic_findings") or {}
        syn = _synthesize_with_role(role=roles.narrator, state=state, ports=ports)
        syn = _apply_observation_lock_to_synthesis(syn, findings)
        return {
            "diagnostic_synthesis": syn.model_dump(),
            "llm_calls": int(state.get("llm_calls", 0)) + 1,
        }

    def reconcile_debate_node(state: LegState) -> LegState:
        synthesis = DiagnosticSynthesis.model_validate(state.get("diagnostic_synthesis") or {})
        challenge = state.get("catalyst_challenge") or (
            (state.get("diagnostic_findings") or {}).get("catalyst_challenge")
        )
        merged = reconcile_with_challenge(synthesis, challenge)
        return {"diagnostic_synthesis": merged.model_dump()}

    def route_verify_gate(state: LegState) -> Literal["verify", "finalize_leg_report"]:
        if int(state.get("verify_budget_remaining", 0)) > 0:
            return "verify"
        return "finalize_leg_report"

    def verify_node(state: LegState) -> LegState:
        synthesis = DiagnosticSynthesis.model_validate(state.get("diagnostic_synthesis") or {})
        findings = state.get("diagnostic_findings") or {}
        synthesis = _apply_observation_lock_to_synthesis(synthesis, findings)
        digest = IntelDigest.model_validate(
            state.get("intel_digest") or findings.get("intel_digest") or {}
        )
        relevant_titles = [item.title for item in digest.relevant if item.title]
        facts = build_position_facts(
            state["snapshot"], state["pricing"], news_count=len(state.get("news", []))
        )
        verdict = verify_synthesis(
            synthesis,
            facts,
            role=roles.verifier,
            suppress_vega=bool(findings.get("suppress_vega_narrative")),
            observation_reliable=bool(findings.get("observation_reliable", True)),
            news_titles=relevant_titles,
            catalyst_challenge=state.get("catalyst_challenge") or findings.get("catalyst_challenge"),
            no_escalation=bool(findings.get("no_escalation")),
        )
        trace: list[dict[str, Any]] = list(state.get("verifier_trace") or [])
        trace.append(verdict.model_dump())
        remaining = int(state.get("verify_budget_remaining", config.verify_budget)) - 1
        # A9.1: deterministic_precheck (inside verify_synthesis) intercepts
        # most hard-rule violations before any LLM call; rationale strings
        # from that path are fixed, code-authored sentences, never the
        # LLM's own prose -- a cheap, if slightly indirect, "was this
        # deterministic" signal without changing verify_synthesis's return
        # type for two call sites over one counter.
        calls = int(state.get("llm_calls", 0))
        if verdict.rationale not in DETERMINISTIC_PRECHECK_RATIONALES:
            calls += 1
        return {"verifier_trace": trace, "verify_budget_remaining": remaining, "llm_calls": calls}

    def route_verify_result(
        state: LegState,
    ) -> Literal[
        "finalize_leg_report",
        "revise_synthesis",
        "reflect_verifier",
        "terminal_unexplained_break",
    ]:
        trace = list(state.get("verifier_trace") or [])
        if not trace:
            return "finalize_leg_report"
        last = trace[-1]
        verdict = last.get("verdict")
        remaining = int(state.get("verify_budget_remaining", 0))
        if verdict == "PASS":
            return "finalize_leg_report"
        if verdict == "PARTIAL":
            return "reflect_verifier"
        if verdict == "FAIL":
            if remaining > 0:
                return "revise_synthesis"
            from .verifier_schema import DiagnosticVerifierResult

            result = DiagnosticVerifierResult.model_validate(last)
            if is_hard_verifier_fail(result):
                return "terminal_unexplained_break"
            return "reflect_verifier"
        return "finalize_leg_report"

    def reflect_verifier_node(state: LegState) -> LegState:
        findings = dict(state.get("diagnostic_findings") or {})
        synthesis = DiagnosticSynthesis.model_validate(state.get("diagnostic_synthesis") or {})
        trace = list(state.get("verifier_trace") or [])
        last = trace[-1] if trace else {}
        from .verifier_schema import DiagnosticVerifierResult

        verdict = DiagnosticVerifierResult.model_validate(
            last
            or {
                "verdict": "PARTIAL",
                "missing_evidence": [],
                "policy_flags": [],
                "rationale": "",
            }
        )
        obs_reliable = bool(findings.get("observation_reliable", True))
        synthesis = apply_verifier_reflection(
            synthesis,
            verdict,
            observation_reliable=obs_reliable,
        )
        findings["verifier_status"] = "PARTIAL"
        findings["verifier_reflect"] = verdict.model_dump()
        return {
            "diagnostic_findings": findings,
            "diagnostic_synthesis": synthesis.model_dump(),
        }

    def revise_synthesis_node(state: LegState) -> LegState:
        leg = state["leg"]
        ports = _resolve_ports(leg, deps)
        findings = state.get("diagnostic_findings") or {}
        syn = _synthesize_with_role(role=roles.narrator, state=state, ports=ports)
        syn = _apply_observation_lock_to_synthesis(syn, findings)
        return {
            "diagnostic_synthesis": syn.model_dump(),
            "llm_calls": int(state.get("llm_calls", 0)) + 1,
        }

    def terminal_unexplained_break_node(state: LegState) -> LegState:
        findings = dict(state.get("diagnostic_findings") or {})
        findings["terminal_unexplained_break"] = True
        findings["verifier_status"] = "FAIL"
        synthesis = DiagnosticSynthesis.model_validate(state.get("diagnostic_synthesis") or {})
        trace = list(state.get("verifier_trace") or [])
        last = trace[-1] if trace else {}
        rationale = str(last.get("rationale", "")).strip()
        missing = list(last.get("missing_evidence") or [])
        synthesis = synthesis.model_copy(
            update={
                "verdict": "Verifier FAIL — terminal break escalation."
                + (f" {rationale}" if rationale else ""),
                "takeaways": [
                    f"Verifier missing evidence: {', '.join(missing) or 'policy'}",
                    *synthesis.takeaways,
                ],
            }
        )
        return {
            "diagnostic_findings": findings,
            "diagnostic_synthesis": synthesis.model_dump(),
        }

    def finalize_leg_report_node(state: LegState) -> LegState:
        synthesis = DiagnosticSynthesis.model_validate(state.get("diagnostic_synthesis") or {})
        diagnosis = synthesis_to_legacy_diagnosis(synthesis)
        bundle = PositionBundle(
            snapshot=state["snapshot"],
            pricing=state["pricing"],
            news=state.get("news", []),
            plan=state.get("search_plan"),
        )
        findings = state.get("diagnostic_findings") or {}
        report = render_portfolio_report(
            [bundle],
            [synthesis],
            leg_findings=[findings],
        )
        return {
            "diagnosis": diagnosis,
            "diagnostic_synthesis": synthesis.model_dump(),
            "report": report,
        }

    def leg_failure_finalize_node(state: LegState) -> LegState:
        msg = state.get("leg_error") or "Leg failed before report finalization."
        no_comparable = bool(state.get("terminal_no_comparable_observation"))
        basis_mismatch = bool(state.get("basis_mismatch_suspected"))
        if no_comparable:
            heading = "## No Comparable Observation"
            takeaways = ["No pricing or news search was performed; this is a data coverage limitation."]
        elif basis_mismatch:
            heading = "## Basis Mismatch Suspected"
            takeaways = ["No pricing was performed; the raw quotes failed a basis-consistency check."]
        else:
            heading = "## Leg Failure"
            takeaways = ["Inspect fixture or market input for this leg."]
        return {
            "diagnosis": msg,
            "diagnostic_synthesis": {
                "primary_driver": "Unresolved",
                "verdict": msg,
                "confidence_level": "low",
                "confidence_rationale": msg,
                "evidence": [],
                "takeaways": takeaways,
                "american_commentary": "",
            },
            "report": f"{heading}\n\n{msg}\n",
        }

    graph = StateGraph(LegState)
    for name, fn in (
        ("fetch_market", fetch_market_node),
        ("quant", quant_node),
        ("blotter", blotter_node),
        ("diagnostic_pass", diagnostic_pass_node),
        ("residual_gate", lambda state: {}),
        ("react_plan", react_plan_node),
        ("react_tool_exec", react_tool_exec_node),
        ("budget_gate", lambda state: {}),
        ("diag_finalize", diag_finalize_node),
        ("plan_search", plan_search_node),
        ("search", search_node),
        ("digest_news", digest_news_node),
        ("challenge_catalyst", challenge_catalyst_node),
        ("synthesize", synthesize_node),
        ("reconcile_debate", reconcile_debate_node),
        ("verify", verify_node),
        ("revise_synthesis", revise_synthesis_node),
        ("reflect_verifier", reflect_verifier_node),
        ("terminal_unexplained_break", terminal_unexplained_break_node),
        ("finalize_leg_report", finalize_leg_report_node),
        ("leg_failure_finalize", leg_failure_finalize_node),
    ):
        graph.add_node(name, _timed_node(name, fn))

    graph.add_edge(START, "fetch_market")
    graph.add_conditional_edges(
        "fetch_market",
        route_after_fetch,
        ["quant", "leg_failure_finalize"],
    )
    graph.add_conditional_edges(
        "quant",
        route_after_quant,
        ["blotter", "leg_failure_finalize"],
    )
    graph.add_edge("blotter", "diagnostic_pass")
    graph.add_conditional_edges(
        "diagnostic_pass",
        route_residual_gate,
        ["react_plan", "diag_finalize"],
    )
    graph.add_edge("react_plan", "react_tool_exec")
    graph.add_edge("react_tool_exec", "budget_gate")
    graph.add_conditional_edges(
        "budget_gate",
        route_budget_gate,
        ["residual_gate", "diag_finalize"],
    )
    graph.add_conditional_edges(
        "residual_gate",
        route_residual_gate,
        ["react_plan", "diag_finalize"],
    )
    graph.add_conditional_edges(
        "diag_finalize",
        route_after_diag_finalize,
        ["plan_search", "finalize_leg_report"],
    )
    graph.add_edge("plan_search", "search")
    graph.add_edge("search", "digest_news")
    graph.add_edge("digest_news", "challenge_catalyst")
    graph.add_edge("challenge_catalyst", "synthesize")
    graph.add_edge("synthesize", "reconcile_debate")
    graph.add_conditional_edges(
        "reconcile_debate",
        route_verify_gate,
        ["verify", "finalize_leg_report"],
    )
    graph.add_conditional_edges(
        "verify",
        route_verify_result,
        [
            "finalize_leg_report",
            "revise_synthesis",
            "reflect_verifier",
            "terminal_unexplained_break",
        ],
    )
    graph.add_edge("revise_synthesis", "reconcile_debate")
    graph.add_edge("reflect_verifier", "finalize_leg_report")
    graph.add_edge("terminal_unexplained_break", "finalize_leg_report")
    graph.add_edge("finalize_leg_report", END)
    graph.add_edge("leg_failure_finalize", END)
    return graph.compile()


def run_leg_pipeline(
    leg: BookLegSpec,
    *,
    config: PipelineConfig | None = None,
    deps: GraphDeps | None = None,
    roles: LlmRoleRegistry | None = None,
) -> LegState:
    cfg = config or PipelineConfig.from_env()
    app = build_leg_diagnosis_subgraph(config=cfg, deps=deps, roles=roles)
    initial: LegState = {
        "leg": leg,
        "ticker": leg.ticker,
        "option_type": leg.option_type,
        "strike": leg.strike,
        "expiry": leg.expiry,
        "quantity": leg.quantity,
        "multiplier": leg.multiplier,
        "verify_budget_remaining": cfg.verify_budget,
        "diag_budget_remaining": cfg.diag_budget,
    }
    return app.invoke(initial)


def build_leg_branch_subgraph(
    *,
    config: PipelineConfig,
    deps: GraphDeps | None = None,
    roles: LlmRoleRegistry | None = None,
):
    leg_graph = build_leg_diagnosis_subgraph(config=config, deps=deps, roles=roles)

    def pack_leg_result_node(state: LegBranchState) -> LegBranchState:
        leg = state["leg"]
        if state.get("leg_error") or not state.get("snapshot") or not state.get("pricing"):
            msg = state.get("leg_error") or "leg pipeline failed"
            return {
                "leg_results": [
                    {
                        "leg_id": leg.leg_id,
                        "ok": False,
                        "error": msg,
                        "bundle": None,
                        "synthesis": state.get("diagnostic_synthesis"),
                        "diagnostic_findings": state.get("diagnostic_findings") or {},
                        "report": state.get("report", ""),
                        "blotter": state.get("blotter", ""),
                        "diagnosis": state.get("diagnosis", msg),
                        "stage_timings": state.get("stage_timings") or {},
                        "llm_calls": state.get("llm_calls"),
                        "no_escalation": bool(state.get("no_escalation")),
                        "terminal_no_comparable_observation": bool(
                            state.get("terminal_no_comparable_observation")
                        ),
                    }
                ]
            }
        bundle = PositionBundle(
            snapshot=state["snapshot"],
            pricing=state["pricing"],
            news=state.get("news", []),
            plan=state.get("search_plan"),
        )
        return {
            "leg_results": [
                {
                    "leg_id": leg.leg_id,
                    "ok": True,
                    "error": None,
                    "bundle": bundle,
                    "synthesis": state.get("diagnostic_synthesis"),
                    "diagnostic_findings": state.get("diagnostic_findings") or {},
                    "report": state.get("report", ""),
                    "blotter": state.get("blotter", ""),
                    "diagnosis": state.get("diagnosis", ""),
                    "stage_timings": state.get("stage_timings") or {},
                    "llm_calls": state.get("llm_calls"),
                    "no_escalation": bool(state.get("no_escalation")),
                    "terminal_no_comparable_observation": bool(
                        state.get("terminal_no_comparable_observation")
                    ),
                }
            ]
        }

    graph = StateGraph(LegBranchState)
    graph.add_node("leg_pipeline", leg_graph)
    graph.add_node("pack_leg_result", pack_leg_result_node)
    graph.add_edge(START, "leg_pipeline")
    graph.add_edge("leg_pipeline", "pack_leg_result")
    graph.add_edge("pack_leg_result", END)
    return graph.compile()
