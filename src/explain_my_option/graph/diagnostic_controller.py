"""Bounded tool Controller for ``diagnostic_pass`` — deterministic, max 1 costly call.

A7.1 widened ``FREE_TOOLS`` to include ``reconcile_mark_vs_model`` and
``quote_quality_and_noise_band`` (both are pure arithmetic on
already-computed facts, and a quiet day can only be recognized as quiet
by running them, so A7.2's "zero costly tools" requirement needs them to
not consume the budget). That leaves exactly one costly slot per pass --
the single deep tool ``_pick_deep_tool`` selects -- so the budget shrank
from 3 to 1 to match, not merely to relabel the same ceiling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from ..pricing.config import EngineConfig
from ..pricing.types import MarketSnapshot, PricingResult, VolSurfaceData
from . import diagnostic_tools as tools

MAX_DIAGNOSTIC_TOOL_CALLS = 1

# A5.1: pure arithmetic on already-computed Greeks/facts -- no repricing
# path, no network, no LLM -- always runs when its precondition holds and
# never competes with path_reprice/compare_to_official for the scarce
# budget slot. (taylor_second_order does bump-and-revalue a handful of
# small perturbations around the single already-priced t-1 point, which
# is why it is cheap relative to path_reprice's full multi-factor
# sequential reval -- "free" here means "does not consume the tool
# budget", not "zero computation".)
#
# reconcile_mark_vs_model and quote_quality_and_noise_band fit the same
# definition (both just read already-computed pricing/snapshot fields,
# no repricing) and, unlike taylor_second_order, they are not optional --
# every diagnostic pass needs them to even compute the severity/
# escalation metric that decides whether anything else should run. A7.2
# requires a quiet day to run *zero costly tools*; that is only
# achievable if the tools that establish quietness are themselves free.
FREE_TOOLS = frozenset(
    {"taylor_second_order", "reconcile_mark_vs_model", "quote_quality_and_noise_band"}
)

# A5.3: the Taylor expansion is local -- on a large move it does not
# converge slowly, it diverges. Provisional threshold; see README "Regime
# rule" (added once the case table backing it exists).
TAYLOR_REGIME_THRESHOLD = 0.35

# A7.2: escalation_metric at or below this band means "nothing to
# explain" -- the same cutoff _pick_deep_tool already uses to skip the
# deep-tool slot entirely, reused here so "no deep tool ran" and
# "no_escalation" agree by construction rather than by coincidence.
LOW_SEVERITY_THRESHOLD_PCT = 10.0

# A7.2, second half of the same gate: a small *ratio* is not sufficient on
# its own -- it is also true of a large, dramatic move the Taylor
# decomposition happens to explain well (e.g. a vol crush with residual
# near zero), which is not "nothing to explain." A7.1's selection
# criteria (|return| < 0.3%, no earnings/ex-div/macro that week) pick days
# where the *absolute* move is tiny in the first place; the three
# verified quiet-day cases (A7.1) show total_pnl of $0.03-$0.11 against
# option_price_prev of $5-13 (0.4%-1.4% of premium). Provisional, like
# TAYLOR_REGIME_THRESHOLD -- would benefit from a larger case table.
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
    suppress_vega_narrative: bool = False
    observation_reliable: bool = True
    ex_div_attribution: dict[str, Any] | None = None
    tool_costs: dict[str, str] = field(default_factory=dict)
    taylor_regime: str | None = None
    r_spot: float | None = None
    r_vol: float | None = None

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "tools_run": list(self.tools_run),
            "results": dict(self.results),
            "tool_calls_used": self.tool_calls_used,
            "skipped_tools": [{"name": s.name, "reason": s.reason} for s in self.skipped_tools],
            "terminal_unexplained_break": self.terminal_unexplained_break,
            "suppress_vega_narrative": self.suppress_vega_narrative,
            "observation_reliable": self.observation_reliable,
            "tool_costs": dict(self.tool_costs),
            "taylor_regime": self.taylor_regime,
            "r_spot": self.r_spot,
            "r_vol": self.r_vol,
        }
        if self.ex_div_attribution is not None:
            payload["ex_div_attribution"] = dict(self.ex_div_attribution)
        return payload


def _residual_pct(pricing: PricingResult) -> float:
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


def _run_tool(
    findings: DiagnosticFindings,
    name: str,
    fn: Callable[[], dict[str, Any]],
) -> bool:
    """Run one tool. Free tools (A5.1) always run; costly ones need budget."""
    cost = "free" if name in FREE_TOOLS else "costly"
    if cost == "costly" and findings.tool_calls_used >= MAX_DIAGNOSTIC_TOOL_CALLS:
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
    residual_pct: float,
    gap_pct: float,
    flag_ex_div: bool,
) -> tuple[str | None, list[tuple[str, str]]]:
    """Select one *costly* tool for the final budget slot.

    taylor_second_order no longer competes here (A5.1: it is free and
    already ran unconditionally before this is called) -- the old
    10-20% band that reserved the slot for it ahead of a full reval is
    gone, folded into the path_reprice threshold below.
    """
    severity = max(residual_pct, gap_pct)
    skipped: list[tuple[str, str]] = []

    if severity <= LOW_SEVERITY_THRESHOLD_PCT and not flag_ex_div:
        return None, skipped

    if severity > LOW_SEVERITY_THRESHOLD_PCT:
        skipped.append(("compare_to_official", "path_reprice selected for severity >10%"))
        if flag_ex_div:
            skipped.append(
                ("american_dividend_exercise_check", "path_reprice outranks ex-div window")
            )
        return "path_reprice", skipped

    if flag_ex_div:
        skipped.append(("compare_to_official", "american check outranks model-risk cross-check"))
        return "american_dividend_exercise_check", skipped

    return "compare_to_official", skipped


def run_diagnostic_pass(
    snap: MarketSnapshot,
    pricing: PricingResult,
    surface: Optional[VolSurfaceData] = None,
    *,
    config: Optional[EngineConfig] = None,
) -> DiagnosticFindings:
    findings = DiagnosticFindings()
    residual_pct = _residual_pct(pricing)

    if snap.option_price_now > 0 and snap.option_price_prev > 0:
        _run_tool(
            findings,
            "reconcile_mark_vs_model",
            lambda: tools.reconcile_mark_vs_model(snap, pricing),
        )

    if snap.bid is not None and snap.ask is not None:
        _run_tool(
            findings,
            "quote_quality_and_noise_band",
            lambda: tools.quote_quality_and_noise_band(snap, pricing),
        )

    q = findings.results.get("quote_quality_and_noise_band")
    if q:
        if q.get("iv_move_within_noise"):
            findings.suppress_vega_narrative = True
        findings.observation_reliable = bool(q.get("observation_reliable", True))

    # A5.1: free -- always runs, never competes for the budget slot below.
    _run_tool(
        findings,
        "taylor_second_order",
        lambda: tools.run_taylor_second_order(snap, pricing, config=config),
    )
    second = findings.results.get("taylor_second_order") or {}
    r_spot = abs(pricing.pnl.gamma_pnl) / max(abs(pricing.pnl.delta_pnl), 1e-12)
    r_vol = abs(float(second.get("volga_pnl", 0.0))) / max(abs(pricing.pnl.vega_pnl), 1e-12)
    findings.r_spot = r_spot
    findings.r_vol = r_vol
    findings.taylor_regime = "INVALID" if max(r_spot, r_vol) > TAYLOR_REGIME_THRESHOLD else "VALID"

    rec = findings.results.get("reconcile_mark_vs_model", {})
    gap_pct = _gap_pct(rec)
    calibrated_ok = rec.get("mark_calibrated") and gap_pct < 2.0

    am_preview = tools.american_dividend_exercise_check(snap, pricing)
    if am_preview.get("flag_ex_div_window"):
        findings.ex_div_attribution = tools.ex_div_attribution_split(snap, pricing)

    if findings.tool_calls_used < MAX_DIAGNOSTIC_TOOL_CALLS and not calibrated_ok:
        deep, skip_list = _pick_deep_tool(
            residual_pct=residual_pct,
            gap_pct=gap_pct,
            flag_ex_div=bool(am_preview.get("flag_ex_div_window")),
        )
        for name, reason in skip_list:
            _skip(findings, name, reason)

        if deep == "path_reprice":
            _run_tool(
                findings,
                "path_reprice",
                lambda: tools.run_path_reprice(snap, pricing, surface, config=config),
            )
        elif deep == "american_dividend_exercise_check":
            _run_tool(
                findings,
                "american_dividend_exercise_check",
                lambda: am_preview,
            )
        elif deep == "compare_to_official":
            _run_tool(
                findings,
                "compare_to_official",
                lambda: tools.run_compare_to_official(
                    snap, pricing, surface, config=config
                ),
            )
    elif calibrated_ok:
        _skip(findings, "deep_diagnostics", "mark calibrated and gap small")

    if (
        am_preview.get("flag_ex_div_window")
        and "american_dividend_exercise_check" not in findings.tools_run
    ):
        _skip(
            findings,
            "american_dividend_exercise_check",
            "budget exhausted or lower priority",
        )

    if findings.tool_calls_used >= MAX_DIAGNOSTIC_TOOL_CALLS and (
        residual_pct > 15.0 or gap_pct > 15.0
    ):
        findings.terminal_unexplained_break = True

    return findings
