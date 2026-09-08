"""Book-level parent graph with Send fan-out into compiled leg subgraphs."""

from __future__ import annotations

import operator
import os
from typing import Annotated, TypedDict

from langgraph.types import Send
from langgraph.graph import END, START, StateGraph

from ..graph.deps import GraphDeps
from ..report import render_portfolio_report
from ..report.synthesis import fallback_synthesis
from ..report.facts import PositionBundle, build_position_facts
from .book_schema import BookSpec
from .config import PipelineConfig
from .leg_graph import build_leg_branch_subgraph
from .llm_roles import LlmRoleRegistry, default_openai_roles
from .types import LegResult


class PortfolioState(TypedDict, total=False):
    book: BookSpec
    leg_results: Annotated[list[LegResult], operator.add]
    book_report: str


def _require_openai_node(_state: PortfolioState, config: PipelineConfig) -> PortfolioState:
    if config.require_openai and not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Unified pipeline requires OPENAI_API_KEY.")
    return {}


def _fanout(state: PortfolioState):
    book = state["book"]
    if not book.legs:
        return "aggregate_book"
    return [Send("leg_branch", {"leg": leg}) for leg in book.legs]


def _aggregate(state: PortfolioState) -> PortfolioState:
    results = state.get("leg_results") or []
    ok_results = [r for r in results if r.get("ok") and r.get("bundle")]
    bundles: list[PositionBundle] = [r["bundle"] for r in ok_results]  # type: ignore[misc]
    syntheses = []
    findings_list = []
    for r in ok_results:
        syn_dict = r.get("synthesis")
        if syn_dict:
            from ..report.schema import DiagnosticSynthesis

            syntheses.append(DiagnosticSynthesis.model_validate(syn_dict))
        else:
            facts = build_position_facts(r["bundle"].snapshot, r["bundle"].pricing)  # type: ignore[union-attr]
            syntheses.append(fallback_synthesis(facts, llm_unavailable=True))
        findings_list.append(r.get("diagnostic_findings"))

    report = render_portfolio_report(bundles, syntheses, leg_findings=findings_list)
    failed = [r for r in results if not r.get("ok")]
    if failed:
        report += "\n\n## Failed legs\n\n"
        for r in failed:
            report += f"* `{r.get('leg_id')}`: {r.get('error')}\n"
    return {"book_report": report}


def build_book_graph(
    *,
    config: PipelineConfig | None = None,
    deps: GraphDeps | None = None,
    roles: LlmRoleRegistry | None = None,
):
    cfg = config or PipelineConfig.from_env()
    role_registry = roles or default_openai_roles()
    leg_branch = build_leg_branch_subgraph(config=cfg, deps=deps, roles=role_registry)

    graph = StateGraph(PortfolioState)
    graph.add_node("require_openai", lambda state: _require_openai_node(state, cfg))
    graph.add_node("leg_branch", leg_branch)
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
    app = build_book_graph(config=config, deps=deps, roles=roles)
    state = app.invoke({"book": book, "leg_results": []})
    # Backward compatibility: keep `report` key for callers.
    if "book_report" in state:
        state["report"] = state["book_report"]  # type: ignore[index]
    return state
