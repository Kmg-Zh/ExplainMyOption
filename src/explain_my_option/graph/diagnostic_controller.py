"""Deterministic diagnostic pass: which tools run, and what the run escalates to.

Free tools are arithmetic on already-priced facts and always run when their
inputs exist. One costly tool (a full revaluation or an early-exercise check)
may run per pass. The two revaluation audits need the PnL source's optional
``second_order`` / ``path_reprice`` hooks; without them they are skipped with
the reason recorded. No LLM is involved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from ..pricing.types import MarketSnapshot, PricingResult, VolSurfaceData
from ..report.reconciliation import build_reconciliation_facts
from . import diagnostic_tools as tools
from .deps import PnlSource

MAX_DIAGNOSTIC_TOOL_CALLS = 1

# "Free" means the tool does not use the costly-tool budget, not that it does
# no work: taylor_second_order bump-reprices around the already-priced T-1 point.
FREE_TOOLS = frozenset(
    {"taylor_second_order", "reconcile_mark_vs_model", "quote_quality_and_noise_band"}
)

# Above this severity (max of residual % and mark-gap %) the costly slot goes to
# a full revaluation; at or below it a day can count as having nothing to explain.
LOW_SEVERITY_THRESHOLD_PCT = 10.0
# Unless the day has nothing to explain, a residual above this gets a
# follow-up full revaluation when none ran yet. It audits the blotter and
# never escalates.
FOLLOW_UP_RESIDUAL_PCT = 5.0
# The costly audit ran (or the PnL source cannot run it) and the residual or
# mark gap is still above this: terminal break.
TERMINAL_BREAK_PCT = 15.0
_NO_REVALUATION = "the PnL source has no revaluation hook"
# Taylor is local: past this ratio of second- to first-order terms it diverges
# rather than converging slowly. Provisional; see the README "Regime rule".
TAYLOR_REGIME_THRESHOLD = 0.35

# A small escalation ratio alone also fits a dramatic move the Greeks happen to
# explain well (a vol crush with ~zero residual), so "nothing to explain"
# also requires a small move: under 5% of the option mid, or $0.50 without one.
# Provisional, calibrated on the committed quiet days ($0.03-$0.11 moves on
# $5-$13 premiums).
NO_ESCALATION_MATERIALITY_PCT_OF_MID = 0.05
NO_ESCALATION_MATERIALITY_ABS_USD = 0.50


@dataclass
class SkippedTool:
    name: str
    reason: str


@dataclass
class DiagnosticFindings:
    tools_run: list[str] = field(default_factory=list)
    results: dict[str, dict[str, Any]] = field(default_factory=dict)
    tool_calls_used: int = 0
    skipped_tools: list[SkippedTool] = field(default_factory=list)
    terminal_unexplained_break: bool = False
    terminal_cause: str | None = None
    suppress_vega_narrative: bool = False
    observation_reliable: bool = True
    ex_div_attribution: dict[str, Any] | None = None
    tool_costs: dict[str, str] = field(default_factory=dict)
    taylor_regime: str | None = None
    r_spot: float | None = None
    r_vol: float | None = None
    no_escalation: bool = False

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "tools_run": list(self.tools_run),
            "results": dict(self.results),
            "tool_calls_used": self.tool_calls_used,
            "skipped_tools": [{"name": s.name, "reason": s.reason} for s in self.skipped_tools],
            "terminal_unexplained_break": self.terminal_unexplained_break,
            "terminal_cause": self.terminal_cause,
            "suppress_vega_narrative": self.suppress_vega_narrative,
            "observation_reliable": self.observation_reliable,
            "tool_costs": dict(self.tool_costs),
            "taylor_regime": self.taylor_regime,
            "r_spot": self.r_spot,
            "r_vol": self.r_vol,
            "no_escalation": self.no_escalation,
        }
        if self.ex_div_attribution is not None:
            payload["ex_div_attribution"] = dict(self.ex_div_attribution)
        return payload


def residual_pct(pricing: PricingResult) -> float:
    """|Taylor residual| as a percentage of |model ΔP| (0 when ΔP is 0)."""
    total = pricing.pnl.total_pnl
    if abs(total) < 1e-12:
        return 0.0
    return abs(100.0 * pricing.pnl.residual_pnl / total)


def _gap_pct(rec: dict[str, Any]) -> float:
    gap = rec.get("model_vs_mark_gap_usd")
    model = rec.get("model_pnl_usd")
    if gap is None or model is None or abs(model) < 1e-9:
        return 0.0
    return abs(100.0 * float(gap) / float(model))


def _run_tool(findings: DiagnosticFindings, name: str, fn: Callable[[], dict[str, Any]], *, budgeted: bool = True) -> bool:
    """Run one tool. Free tools always run; a budgeted costly tool needs a slot."""
    cost = "free" if name in FREE_TOOLS else "costly"
    if cost == "costly" and budgeted and findings.tool_calls_used >= MAX_DIAGNOSTIC_TOOL_CALLS:
        return False
    findings.tools_run.append(name)
    findings.results[name] = fn()
    findings.tool_costs[name] = cost
    if cost == "costly":
        findings.tool_calls_used += 1
    return True


def _skip(findings: DiagnosticFindings, name: str, reason: str) -> None:
    findings.skipped_tools.append(SkippedTool(name=name, reason=reason))


def _pick_deep_tool(
    *,
    severity: float,
    flag_ex_div: bool,
) -> tuple[str | None, list[tuple[str, str]]]:
    """Choose the one costly tool for the budget slot, with skip reasons."""
    if severity > LOW_SEVERITY_THRESHOLD_PCT:
        skipped = [("compare_to_official", "path_reprice selected for severity >10%")]
        if flag_ex_div:
            skipped.append(("american_dividend_exercise_check", "path_reprice outranks ex-div window"))
        return "path_reprice", skipped
    if flag_ex_div:
        return "american_dividend_exercise_check", [
            ("compare_to_official", "american check outranks model-risk cross-check")
        ]
    return None, []


def run_diagnostic_pass(
    snap: MarketSnapshot,
    pricing: PricingResult,
    surface: Optional[VolSurfaceData] = None,
    *,
    pnl: PnlSource,
) -> DiagnosticFindings:
    """Run the deterministic tools; ``pnl`` is the PnL source that priced the leg."""
    findings = DiagnosticFindings()
    res_pct = residual_pct(pricing)
    can_second_order = hasattr(pnl, "second_order")
    can_reprice = hasattr(pnl, "path_reprice")

    if snap.option_price_now > 0 and snap.option_price_prev > 0:
        _run_tool(findings, "reconcile_mark_vs_model", lambda: tools.reconcile_mark_vs_model(snap, pricing))
    if snap.bid is not None and snap.ask is not None:
        _run_tool(findings, "quote_quality_and_noise_band", lambda: tools.quote_quality_and_noise_band(snap, pricing))
    quote = findings.results.get("quote_quality_and_noise_band")
    if quote:
        findings.suppress_vega_narrative = bool(quote.get("iv_move_within_noise"))
        findings.observation_reliable = bool(quote.get("observation_reliable", True))

    if can_second_order:
        _run_tool(findings, "taylor_second_order", lambda: tools.run_taylor_second_order(pnl, snap, pricing))
    else:
        _skip(findings, "taylor_second_order", _NO_REVALUATION)
    second = findings.results.get("taylor_second_order") or {}
    findings.r_spot = abs(pricing.pnl.gamma_pnl) / max(abs(pricing.pnl.delta_pnl), 1e-12)
    findings.r_vol = abs(float(second.get("volga_pnl", 0.0))) / max(abs(pricing.pnl.vega_pnl), 1e-12)
    findings.taylor_regime = "INVALID" if max(findings.r_spot, findings.r_vol) > TAYLOR_REGIME_THRESHOLD else "VALID"

    rec = findings.results.get("reconcile_mark_vs_model", {})
    gap_pct = _gap_pct(rec)
    calibrated_ok = rec.get("mark_calibrated") and gap_pct < 2.0

    am_check = tools.american_dividend_exercise_check(snap, pricing)
    flag_ex_div = bool(am_check.get("flag_ex_div_window"))
    if flag_ex_div:
        findings.ex_div_attribution = tools.ex_div_attribution_split(snap, pricing)

    deep_unavailable = False
    if calibrated_ok:
        _skip(findings, "deep_diagnostics", "mark calibrated and gap small")
    else:
        deep, skipped = _pick_deep_tool(severity=max(res_pct, gap_pct), flag_ex_div=flag_ex_div)
        for name, reason in skipped:
            _skip(findings, name, reason)
        if deep == "path_reprice" and can_reprice:
            _run_tool(findings, deep, lambda: tools.run_path_reprice(pnl, snap, pricing, surface))
        elif deep == "path_reprice":
            _skip(findings, deep, _NO_REVALUATION)
            deep_unavailable = True
        elif deep == "american_dividend_exercise_check":
            _run_tool(findings, deep, lambda: am_check)
    considered = {*findings.tools_run, *(s.name for s in findings.skipped_tools)}
    if flag_ex_div and "american_dividend_exercise_check" not in considered:
        _skip(findings, "american_dividend_exercise_check", "budget exhausted or lower priority")

    slot_used = findings.tool_calls_used >= MAX_DIAGNOSTIC_TOOL_CALLS or deep_unavailable
    if slot_used and max(res_pct, gap_pct) > TERMINAL_BREAK_PCT:
        findings.terminal_unexplained_break = True
        findings.terminal_cause = "unexplained_residual"
    findings.no_escalation = nothing_to_explain(snap, pricing, findings)

    if not findings.no_escalation and res_pct > FOLLOW_UP_RESIDUAL_PCT and "path_reprice" not in findings.tools_run:
        if can_reprice:
            _run_tool(
                findings,
                "path_reprice",
                lambda: tools.run_path_reprice(pnl, snap, pricing, surface),
                budgeted=False,
            )
        elif not deep_unavailable:
            _skip(findings, "path_reprice", _NO_REVALUATION)
    return findings


def nothing_to_explain(snap: MarketSnapshot, pricing: PricingResult, findings: DiagnosticFindings) -> bool:
    """Quiet day: no terminal break, a small escalation metric, and a small move."""
    if findings.terminal_unexplained_break:
        return False
    rec = build_reconciliation_facts(snap, pricing)
    mid = snap.mid or snap.option_price_prev
    if mid and mid > 0:
        floor = NO_ESCALATION_MATERIALITY_PCT_OF_MID * mid
    else:
        floor = NO_ESCALATION_MATERIALITY_ABS_USD
    floor *= snap.position_scale()  # rec.model_pnl_usd is position-scaled
    return rec.escalation_metric_pct <= LOW_SEVERITY_THRESHOLD_PCT and abs(rec.model_pnl_usd) < floor
