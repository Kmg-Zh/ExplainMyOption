"""A2 helper functions: deterministic tool choice and state updates."""

from __future__ import annotations

from typing import Any

from ..graph import diagnostic_tools as tools
from ..pricing.config import EngineConfig
from ..pricing.types import MarketSnapshot, PricingResult, VolSurfaceData
ALLOWED_TOOLS = {
    "reconcile_mark_vs_model": tools.reconcile_mark_vs_model,
    "quote_quality_and_noise_band": tools.quote_quality_and_noise_band,
    "taylor_second_order": tools.run_taylor_second_order,
    "path_reprice": tools.run_path_reprice,
    "compare_to_official": tools.run_compare_to_official,
    "american_dividend_exercise_check": tools.american_dividend_exercise_check,
}


def compute_residual_pct(pricing: PricingResult) -> float:
    total = pricing.pnl.total_pnl
    if abs(total) < 1e-12:
        return 0.0
    return abs(100.0 * pricing.pnl.residual_pnl / total)


def choose_a2_tool(
    *,
    residual_pct: float,
    tools_run: list[str],
) -> str | None:
    """A5.1: taylor_second_order is free and already ran upstream, before
    this react loop's first turn (graph.diagnostic_controller.run_diagnostic_pass
    runs it unconditionally) -- it is never a candidate here, so this loop
    no longer needs a severity band reserved for it ahead of a full reval.
    """
    if residual_pct <= 5.0:
        return None
    if "path_reprice" in tools_run:
        return None
    return "path_reprice"


def execute_diagnostic_tool(
    *,
    tool_name: str,
    snap: MarketSnapshot,
    pricing: PricingResult,
    surface: VolSurfaceData | None,
    engine_config: EngineConfig | None = None,
) -> dict[str, Any]:
    fn = ALLOWED_TOOLS[tool_name]
    if tool_name == "compare_to_official":
        return fn(snap, pricing, surface, config=engine_config)
    if tool_name == "taylor_second_order":
        return fn(snap, pricing, config=engine_config)
    if tool_name == "path_reprice":
        return fn(snap, pricing, surface, config=engine_config)
    if tool_name == "american_dividend_exercise_check":
        return fn(snap, pricing)
    return fn(snap, pricing)


def merge_iteration(
    *,
    findings: dict[str, Any],
    tool_name: str,
    payload: dict[str, Any],
    residual_before: float,
    budget_remaining: int,
    iterations: int,
) -> dict[str, Any]:
    merged = dict(findings)
    results = dict(merged.get("results") or {})
    tools_run = list(merged.get("tools_run") or [])
    history: list[dict[str, Any]] = list(merged.get("diag_tool_history") or [])
    tools_run.append(tool_name)
    results[tool_name] = payload
    history.append({"tool": tool_name, "residual_pct": residual_before})
    merged.update(
        {
            "tools_run": tools_run,
            "results": results,
            "tool_calls_used": len(tools_run),
            "diag_budget_remaining": budget_remaining,
            "diag_iterations": iterations,
            "diag_tool_history": history,
        }
    )
    return merged
