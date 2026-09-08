"""Live LangGraph topology — Mermaid from compiled graphs (not hand-drawn)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..pipeline.config import PipelineConfig
    from ..pipeline.llm_roles import LlmRoleRegistry
    from .deps import GraphDeps


def pipeline_mermaid(deps: GraphDeps | None = None, *, xray: bool = False) -> str:
    """Mermaid for the product entry graph (``build_graph`` / book parent)."""
    from ..agent_graph import build_graph

    return build_graph(deps).get_graph(xray=xray).draw_mermaid()


def leg_mermaid(
    deps: GraphDeps | None = None,
    *,
    config: PipelineConfig | None = None,
    roles: LlmRoleRegistry | None = None,
    xray: bool = False,
) -> str:
    """Mermaid for one leg diagnosis subgraph (A2 loop + A3 verifier edges)."""
    from ..pipeline.config import PipelineConfig
    from ..pipeline.leg_graph import build_leg_diagnosis_subgraph

    cfg = config or PipelineConfig(require_openai=False)
    return (
        build_leg_diagnosis_subgraph(config=cfg, deps=deps, roles=roles)
        .get_graph(xray=xray)
        .draw_mermaid()
    )


def book_mermaid(
    deps: GraphDeps | None = None,
    *,
    config: PipelineConfig | None = None,
    roles: LlmRoleRegistry | None = None,
    xray: bool = False,
) -> str:
    """Mermaid for the book parent graph (``Send`` fan-out + aggregate)."""
    from ..pipeline.portfolio_graph import build_book_graph

    return (
        build_book_graph(config=config, deps=deps, roles=roles)
        .get_graph(xray=xray)
        .draw_mermaid()
    )
