"""Unified topology and Send reducer guard tests."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import os

import bootstrap

bootstrap.install()

from explain_my_option.agent_graph import build_graph
from explain_my_option.pipeline.book_schema import load_book_json
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.portfolio_graph import build_book_graph, run_book_pipeline
from explain_my_option.paths import FIXTURES_DIR

BOOK_FIXTURE = FIXTURES_DIR / "books" / "demo_book.json"


def test_imports_compile_without_cycles():
    from explain_my_option.pipeline.leg_graph import build_leg_branch_subgraph, build_leg_diagnosis_subgraph

    assert callable(build_graph)
    assert callable(build_book_graph)
    assert callable(build_leg_diagnosis_subgraph)
    assert callable(build_leg_branch_subgraph)


def test_unified_graph_xray_shows_nested_leg_nodes():
    app = build_graph()
    xray_nodes = set(app.get_graph(xray=True).nodes.keys())
    assert "leg_branch" in app.get_graph().nodes
    assert any("leg_pipeline" in node for node in xray_nodes)
    assert any("diagnostic_pass" in node for node in xray_nodes)


def test_send_fanout_uses_reducer_without_invalid_update():
    old = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-test-not-real"
    try:
        cfg = PipelineConfig(
            features={"a1", "a2", "a3"},
            diag_budget=3,
            diag_iterations=2,
            verify_budget=0,
            require_openai=True,
        )
        book = load_book_json(BOOK_FIXTURE)
        state = run_book_pipeline(book, config=cfg)
    finally:
        if old is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = old
    assert len(state.get("leg_results") or []) == 3
    assert "report" in state


if __name__ == "__main__":
    test_imports_compile_without_cycles()
    test_unified_graph_xray_shows_nested_leg_nodes()
    test_send_fanout_uses_reducer_without_invalid_update()
    print("OK — pipeline topology tests passed")
