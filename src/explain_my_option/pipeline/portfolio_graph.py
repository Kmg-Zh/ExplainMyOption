"""Book parent graph: ``Send`` fan-out into one leg subgraph per position, then roll-up."""

from __future__ import annotations

import operator
import os
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send

from ..graph.deps import GraphDeps
from ..report import render_portfolio_report
from ..report.facts import build_position_facts
from ..report.schema import DiagnosticSynthesis
from ..report.synthesis import fallback_synthesis
from .book_schema import BookSpec
from .config import PipelineConfig
from .leg_graph import build_leg_branch_subgraph
from .llm_roles import LlmRoleRegistry, default_openai_roles
from .types import LegResult


class PortfolioState(TypedDict, total=False):
    book: BookSpec
    leg_results: Annotated[list[LegResult], operator.add]
    # Not "report": every leg subgraph writes its own "report" key, and parallel
    # legs may not write one shared parent key in the same step.
    book_report: str


def _fanout(state: PortfolioState):
    legs = state["book"].legs
    if not legs:
        return "aggregate_book"
    return [Send("leg_branch", {"leg": leg}) for leg in legs]


def _aggregate(state: PortfolioState) -> PortfolioState:
    results = state.get("leg_results") or []
    ok = [r for r in results if r.get("ok") and r.get("bundle")]
    syntheses = [
        DiagnosticSynthesis.model_validate(r["synthesis"])
        if r.get("synthesis")
        else fallback_synthesis(build_position_facts(r["bundle"].snapshot, r["bundle"].pricing), llm_unavailable=True)
        for r in ok
    ]
    report = render_portfolio_report(
        [r["bundle"] for r in ok],
        syntheses,
        leg_findings=[r.get("diagnostic_findings") for r in ok],
    )
    failed = [r for r in results if not r.get("ok")]
    if failed:
        report += "\n\n## Failed legs\n\n" + "".join(f"* `{r.get('leg_id')}`: {r.get('error')}\n" for r in failed)
    return {"book_report": report}


def build_book_graph(
    *,
    config: PipelineConfig | None = None,
    deps: GraphDeps | None = None,
    roles: LlmRoleRegistry | None = None,
):
    cfg = config or PipelineConfig.from_env()

    def require_openai(_state: PortfolioState) -> PortfolioState:
        if cfg.require_openai and not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("The pipeline requires OPENAI_API_KEY (set EMO_PIPELINE_REQUIRE_KEY=0 to skip).")
        return {}

    graph = StateGraph(PortfolioState)
    graph.add_node("require_openai", require_openai)
    graph.add_node("leg_branch", build_leg_branch_subgraph(config=cfg, deps=deps, roles=roles or default_openai_roles()))
    graph.add_node("aggregate_book", _aggregate)
    graph.add_edge(START, "require_openai")
    graph.add_conditional_edges("require_openai", _fanout, ["leg_branch", "aggregate_book"])
    graph.add_edge("leg_branch", "aggregate_book")
    graph.add_edge("aggregate_book", END)
    return graph.compile()


def run_book_pipeline(
    book: BookSpec,
    *,
    config: PipelineConfig | None = None,
    deps: GraphDeps | None = None,
    roles: LlmRoleRegistry | None = None,
) -> PortfolioState:
    """Run the book graph; the roll-up report is returned under ``report``."""
    state = build_book_graph(config=config, deps=deps, roles=roles).invoke({"book": book, "leg_results": []})
    return {**state, "report": state.get("book_report", "")}
