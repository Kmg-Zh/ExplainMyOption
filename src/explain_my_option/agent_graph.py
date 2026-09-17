"""Unified product entrypoints.

The product now runs a book-first parent graph with Send fan-out into leg
subgraphs. ``run_pipeline`` remains as a single-leg convenience wrapper.
"""

from __future__ import annotations

from typing import Optional

from .graph.deps import GraphDeps
from .graph.state import OptionState
from .pipeline.book_schema import BookLegSpec, BookSpec
from .pipeline.config import PipelineConfig
from .pipeline.llm_roles import LlmRoleRegistry
from .pipeline.portfolio_graph import build_book_graph, run_book_pipeline


def run_pipeline(
    ticker: str,
    option_type: str = "call",
    strike: Optional[float] = None,
    expiry: Optional[str] = None,
    quantity: float = 1.0,
    multiplier: float = 1.0,
    *,
    deps: GraphDeps | None = None,
    config: PipelineConfig | None = None,
    roles: LlmRoleRegistry | None = None,
) -> OptionState:
    """Run one leg via the unified book graph and return compatibility fields."""
    leg = BookLegSpec(
        leg_id=ticker,
        fixture=None,
        ticker=ticker,
        option_type=option_type,
        strike=strike,
        expiry=expiry,
        quantity=float(quantity),
        multiplier=float(multiplier),
    )
    book = BookSpec(version="1", as_of="", legs=(leg,))
    out = run_book_pipeline(book, config=config, deps=deps, roles=roles)
    legs = out.get("leg_results") or []
    if not legs:
        raise RuntimeError("Unified pipeline returned no leg results.")
    leg_state = legs[0]
    if not leg_state.get("ok"):
        raise RuntimeError(str(leg_state.get("error") or "Single-leg pipeline failed."))
    bundle = leg_state.get("bundle")
    if bundle is None:
        raise RuntimeError("Missing successful leg bundle in unified result.")
    synthesis = leg_state.get("synthesis") or {}
    return {
        "ticker": ticker,
        "option_type": option_type,
        "strike": strike,
        "expiry": expiry,
        "quantity": quantity,
        "multiplier": multiplier,
        "snapshot": bundle.snapshot,
        "pricing": bundle.pricing,
        "news": bundle.news,
        "search_plan": bundle.plan,
        "diagnostic_findings": leg_state.get("diagnostic_findings") or {},
        "diagnostic_synthesis": synthesis,
        "diagnosis": str(synthesis.get("verdict", leg_state.get("diagnosis", ""))).strip(),
        "report": leg_state.get("report", ""),
        "blotter": leg_state.get("blotter", ""),
        "stage_timings": leg_state.get("stage_timings") or {},
        "llm_calls": leg_state.get("llm_calls"),
        "no_escalation": leg_state.get("no_escalation", False),
        "terminal_no_comparable_observation": leg_state.get(
            "terminal_no_comparable_observation", False
        ),
    }


def build_graph(
    deps: GraphDeps | None = None,
    *,
    config: PipelineConfig | None = None,
    roles: LlmRoleRegistry | None = None,
):
    """Canonical compiled graph (book-first parent with Send fan-out)."""
    return build_book_graph(config=config, deps=deps, roles=roles)
