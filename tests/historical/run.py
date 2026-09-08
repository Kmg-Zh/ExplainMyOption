"""Historical anomaly benchmark — live LLM only (OPENAI_API_KEY required).

Five stress cases with as-of frozen news + synthetic fixtures. Post-event
papers and the scenario note are eval ground truth only (not graph input).
"""

from __future__ import annotations

import argparse
from datetime import date
import json
import os
import sys
from pathlib import Path
from typing import Any

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from dotenv import load_dotenv

load_dotenv()

from historical.pipeline_position import apply_pipeline_position, pipeline_run_kwargs
from historical.scoring import score_narrative_for_case
from historical.cases import (
    PARAMETRIC_KNOWLEDGE_CAVEAT,
    BenchmarkCase,
    format_ground_truth_markdown,
    frozen_news_for_case,
    load_cases,
    news_lineage_errors,
)
from explain_my_option.agent_graph import run_pipeline
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.data_loader import NewsItem
from explain_my_option.graph.deps import FixtureMarketLoader, GraphDeps, OfficialFdmPnlSource
from explain_my_option.intel.planner import CueQueryPlanner
from explain_my_option.intel.sources import IntelRegistry, StubIntelSource
from explain_my_option.intel.types import SearchQuery
from explain_my_option.paths import (
    HISTORICAL_OUTPUT_DIR,
    HISTORICAL_SUMMARY_PATH,
    historical_case_dir,
)
from explain_my_option.pricing import price_and_attribute
from ci.engine_config import engine_config_for_tests
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.report.schema import DiagnosticSynthesis

CFG = engine_config_for_tests()
GOLDEN_SUMMARY = HISTORICAL_SUMMARY_PATH


def _report_path_relative(test_id: str) -> str:
    return f"tests/historical/output/{test_id}/report.md"


def _require_openai_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is required for historical benchmark runs "
            "(mock/offline narrator removed)."
        )


class FixedNewsSource:
    source_id = "yfinance_news"

    def __init__(self, news: list[NewsItem]) -> None:
        self._news = list(news)

    def search(self, query: SearchQuery, *, ticker: str) -> list[NewsItem]:
        del query, ticker
        return list(self._news)


def _deps_for_case(case: BenchmarkCase) -> GraphDeps:
    news = frozen_news_for_case(case)
    return GraphDeps(
        market=FixtureMarketLoader(case.fixture),
        pnl=OfficialFdmPnlSource(config=CFG),
        planner=CueQueryPlanner(),
        intel=IntelRegistry(
            {
                "yfinance_news": FixedNewsSource(news),
                "tavily": StubIntelSource("tavily"),
                "sec_8k": StubIntelSource("sec_8k"),
            }
        ),
    )


def _pipeline_config() -> PipelineConfig:
    return PipelineConfig(
        features={"a1", "a2", "a3"},
        diag_budget=1,
        diag_iterations=0,
        verify_budget=0,
        require_openai=True,
    )


def _assert_case_narrative(case: BenchmarkCase, scores: dict[str, Any]) -> None:
    assert scores["keyword_groups_pass"], (
        f"{case.test_id}: keyword groups {scores['keyword_groups_hit']}/"
        f"{scores['keyword_groups_required']} (missing: {scores['missing_keyword_groups']})"
    )
    assert scores["action_themes_pass"], (
        f"{case.test_id}: action themes {scores['action_themes_hit']}/"
        f"{scores['action_themes_required']} (missing: {scores['missing_action_themes']})"
    )


def run_diagnose_node(case: BenchmarkCase) -> dict[str, Any]:
    _require_openai_api_key()
    return run_pipeline(
        ticker=case.ticker,
        option_type=str(case.input_quant["option_type"]),
        strike=float(case.input_quant["strike"]),
        expiry=str(case.input_quant["expiry"]),
        **pipeline_run_kwargs(),
        deps=_deps_for_case(case),
        config=_pipeline_config(),
    )


def _run_suite(
    *,
    strict: bool,
    only_case: str | None = None,
) -> list[dict[str, Any]]:
    _require_openai_api_key()
    lineage = news_lineage_errors()
    if lineage:
        raise RuntimeError("historical news lineage errors:\n" + "\n".join(lineage))
    cases = load_cases()
    assert len(cases) == 5
    if only_case:
        cases = [c for c in cases if c.test_id == only_case]
        if not cases:
            raise ValueError(f"Unknown case id: {only_case}")

    HISTORICAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    for case in cases:
        print(f"[run] {case.test_id} (live)")
        snap, surf = load_fixture(case.fixture)
        apply_pipeline_position(snap)
        assert snap.as_of == case.date
        assert snap.ticker.upper() == case.ticker.upper()

        pricing = price_and_attribute(snap, surf, None, config=CFG)
        total = pricing.pnl.total_pnl
        assert abs(total) > 0.01, f"{case.test_id}: total pnl too small"
        ratio = abs(pricing.pnl.residual_pnl) / abs(total)
        assert ratio >= case.min_residual_ratio, (
            f"{case.test_id}: expected residual ratio >= {case.min_residual_ratio:.1%}, "
            f"got {ratio:.1%}"
        )

        state = run_diagnose_node(case)
        report = state["report"]
        syn = state["diagnostic_synthesis"]

        path = historical_case_dir(case.test_id) / "report.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")
        (path.parent / "ground_truth.md").write_text(
            format_ground_truth_markdown(case), encoding="utf-8"
        )

        assert "Root-Cause Market Intelligence" in report
        assert "Trading Desk Watchlist" in report

        model = DiagnosticSynthesis.model_validate(syn)
        scores = score_narrative_for_case(
            model, case, residual_pct=ratio * 100.0
        )
        if strict:
            _assert_case_narrative(case, scores)

        rows.append(
            {
                "test_id": case.test_id,
                "tier": case.tier,
                "residual_ratio": round(ratio, 4),
                "keyword_groups_hit": scores["keyword_groups_hit"],
                "keyword_groups_required": scores["keyword_groups_required"],
                "missing_keyword_groups": scores["missing_keyword_groups"],
                "as_of_keyword_groups": scores["as_of_keyword_groups"],
                "post_hoc_keyword_groups": scores["post_hoc_keyword_groups"],
                "hindsight_keyword_groups": scores["hindsight_keyword_groups"],
                "hindsight_groups_hit": scores["hindsight_groups_hit"],
                "possible_parametric_leak": scores["possible_parametric_leak"],
                "leak_marker_hits": scores["leak_marker_hits"],
                "layer_a_pass": (scores.get("layer_a") or {}).get("pass"),
                "layer_b_pass": (scores.get("layer_b") or {}).get("pass"),
                "failure_hints": scores["failure_hints"],
                "action_themes_hit": scores["action_themes_hit"],
                "action_themes_required": scores["action_themes_required"],
                "missing_action_themes": scores["missing_action_themes"],
                "references": case.references,
                "report_path": _report_path_relative(case.test_id),
            }
        )
    return rows


def _write_summary(
    rows: list[dict[str, Any]],
    *,
    strict: bool,
    pin: bool,
) -> Path:
    payload: dict[str, Any] = {
        "mode": "live_llm",
        "news_lineage": "as_of_only",
        "parametric_knowledge_caveat": PARAMETRIC_KNOWLEDGE_CAVEAT,
        "strict": strict,
        "llm_model": os.getenv("EMO_LLM_MODEL", "gpt-5.4-mini"),
        "results": rows,
    }
    if pin:
        payload["pinned_at"] = date.today().isoformat()
    HISTORICAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = HISTORICAL_OUTPUT_DIR / "summary.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if pin:
        GOLDEN_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
        GOLDEN_SUMMARY.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def test_historical_benchmark_live():
    """Opt-in live benchmark (skipped in default CI). Set EMO_BENCHMARK_LIVE=1."""
    if os.getenv("EMO_BENCHMARK_LIVE", "0") != "1":
        return
    _run_suite(strict=False)


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run historical benchmark cases (live LLM only)."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on missing expected keywords/actions.",
    )
    parser.add_argument(
        "--case",
        default=None,
        help="Run only one case by test_id.",
    )
    parser.add_argument(
        "--pin",
        action="store_true",
        help="Also write a local gitignored snapshot at tests/historical/historical_benchmark_summary.json.",
    )
    args = parser.parse_args(argv)

    lineage = news_lineage_errors()
    if lineage:
        raise RuntimeError("historical news lineage errors:\n" + "\n".join(lineage))
    rows = _run_suite(strict=args.strict, only_case=args.case)
    out = _write_summary(rows, strict=args.strict, pin=args.pin)
    print(f"summary -> {out}")
    if args.pin:
        print(f"pinned  -> {GOLDEN_SUMMARY}")
    for row in rows:
        print(
            f"{row['test_id']} [tier {row['tier']}]: residual={row['residual_ratio']:.2%}, "
            f"kw_groups={row['keyword_groups_hit']}/{row['keyword_groups_required']}, "
            f"hindsight={len(row['hindsight_groups_hit'])}/{len(row['hindsight_keyword_groups'])}, "
            f"leak={row['possible_parametric_leak']}, "
            f"hints={','.join(row['failure_hints'])}, "
            f"actions={row['action_themes_hit']}/{row['action_themes_required']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
