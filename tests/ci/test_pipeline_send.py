"""Book-level Send fan-out and failure isolation."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import os

import bootstrap

bootstrap.install()

from explain_my_option.pipeline.book_schema import load_book_json
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.portfolio_graph import run_book_pipeline
from explain_my_option.paths import FIXTURES_DIR

BOOK_FIXTURE = FIXTURES_DIR / "books" / "demo_book.json"


def test_book_fanout_continues_on_leg_failure():
    old = os.environ.pop("OPENAI_API_KEY", None)
    try:
        book = load_book_json(BOOK_FIXTURE)
        cfg = PipelineConfig(
            features={"a1", "a2", "a3"},
            verify_budget=0,
            require_openai=False,
        )
        state = run_book_pipeline(book, config=cfg)
        results = state.get("leg_results") or []
        assert len(results) == 3
        ok = [r for r in results if r.get("ok")]
        failed = [r for r in results if not r.get("ok")]
        assert len(ok) == 2
        assert len(failed) == 1
        report = state.get("report", "")
        assert "# Portfolio Option Diagnostic Report" in report
        assert "Failed legs" in report
        assert "Aggregate factor attribution" in report or "Portfolio Executive Summary" in report
    finally:
        if old is not None:
            os.environ["OPENAI_API_KEY"] = old


if __name__ == "__main__":
    test_book_fanout_continues_on_leg_failure()
    print("OK — pipeline send tests passed")
