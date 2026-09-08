"""Unified book-pipeline entrypoints (compat layer)."""

from __future__ import annotations

from pathlib import Path

from .book_schema import default_book_fixture_path, load_book_json
from .config import PipelineConfig
from .llm_roles import LlmRoleRegistry
from .portfolio_graph import run_book_pipeline
from ..graph.deps import GraphDeps


def run_book_from_fixture_path(
    book_path: Path | str | None = None,
    *,
    config: PipelineConfig | None = None,
    deps: GraphDeps | None = None,
    roles: LlmRoleRegistry | None = None,
) -> dict:
    cfg = config or PipelineConfig.from_env()
    path = Path(book_path) if book_path else default_book_fixture_path()
    book = load_book_json(path)
    state = run_book_pipeline(book, config=cfg, deps=deps, roles=roles)
    return {"report": state.get("report", ""), "leg_results": state.get("leg_results", [])}
