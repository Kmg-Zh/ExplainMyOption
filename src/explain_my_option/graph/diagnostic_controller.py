"""Bounded tool Controller for ``diagnostic_pass`` — deterministic, max 3 calls."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from ..pricing.config import EngineConfig
from ..pricing.types import MarketSnapshot, PricingResult, VolSurfaceData
from . import diagnostic_tools as tools

MAX_DIAGNOSTIC_TOOL_CALLS = 3


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

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "tools_run": list(self.tools_run),
            "results": dict(self.results),
            "tool_calls_used": self.tool_calls_used,
            "skipped_tools": [{"name": s.name, "reason": s.reason} for s in self.skipped_tools],
            "terminal_unexplained_break": self.terminal_unexplained_break,
            "suppress_vega_narrative": self.suppress_vega_narrative,
            "observation_reliable": self.observation_reliable,
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
    """Run one tool if budget allows. Returns False if budget exhausted."""
    if findings.tool_calls_used >= MAX_DIAGNOSTIC_TOOL_CALLS:
        return False
    findings.tools_run.append(name)
    findings.results[name] = fn()
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
    """Select one deep tool for the final slot; record skipped alternatives."""
    severity = max(residual_pct, gap_pct)
    skipped: list[tuple[str, str]] = []

    if severity <= 10.0 and not flag_ex_div:
        return None, skipped

    if severity > 20.0:
        skipped.extend(
            [
                ("taylor_second_order", "path_reprice selected for severity >20%"),
                ("compare_to_official", "path_reprice selected for severity >20%"),
            ]
        )
        if flag_ex_div:
            skipped.append(
                ("american_dividend_exercise_check", "path_reprice outranks ex-div window")
            )
        return "path_reprice", skipped

    if 10.0 < severity <= 20.0:
        skipped.extend(
            [
                ("path_reprice", "severity in 10–20% band — second-order Taylor first"),
                ("compare_to_official", "taylor_second_order selected for 10–20% band"),
            ]
        )
        if flag_ex_div:
            skipped.append(
                ("american_dividend_exercise_check", "taylor_second_order outranks ex-div")
            )
        return "taylor_second_order", skipped

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
        elif deep == "taylor_second_order":
            _run_tool(
                findings,
                "taylor_second_order",
                lambda: tools.run_taylor_second_order(snap, pricing, config=config),
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
