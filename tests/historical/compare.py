"""Governed vs single-shot baseline comparison — live LLM only (OPENAI_API_KEY required).

    python tests/historical/compare.py --case vow_float_squeeze_2008
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from dotenv import load_dotenv

load_dotenv()

from historical.baseline_agent import (
    BaselinePrompt,
    BaselineRunResult,
    run_baseline_diagnosis,
)
from historical.scoring import attribute_governed_vs_baseline, score_narrative_for_case
from historical.pipeline_position import apply_pipeline_position, pipeline_run_kwargs
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
from explain_my_option.paths import HISTORICAL_OUTPUT_DIR, historical_compare_dir
from ci.engine_config import engine_config_for_tests
from explain_my_option.pricing.facade import price_and_attribute
from explain_my_option.report.schema import DiagnosticSynthesis
from explain_my_option.report.validate import validate_synthesis
from explain_my_option.pipeline.config import PipelineConfig

CFG = engine_config_for_tests()


def _require_openai_api_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is required for benchmark comparison "
            "(mock/offline governed narrator removed)."
        )


class FixedNewsSource:
    source_id = "yfinance_news"

    def __init__(self, news: list[NewsItem]) -> None:
        self._news = list(news)

    def search(self, query: SearchQuery, *, ticker: str) -> list[NewsItem]:
        del query, ticker
        return list(self._news)


@dataclass
class GovernedRunResult:
    report: str
    synthesis: dict[str, Any]
    latency_s: float
    mode: str


@dataclass
class ComparisonRow:
    test_id: str
    residual_ratio: float
    governed: dict[str, Any]
    baseline: dict[str, Any]
    improvement_hint: dict[str, Any]
    governed_report_path: str
    baseline_report_path: str
    desk_packet_path: str


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


def run_governed_case(case: BenchmarkCase) -> GovernedRunResult:
    _require_openai_api_key()
    cfg = _pipeline_config()
    deps = _deps_for_case(case)
    t0 = time.perf_counter()
    state = run_pipeline(
        ticker=case.ticker,
        option_type=str(case.input_quant["option_type"]),
        strike=float(case.input_quant["strike"]),
        expiry=str(case.input_quant["expiry"]),
        **pipeline_run_kwargs(),
        deps=deps,
        config=cfg,
    )
    latency_s = time.perf_counter() - t0
    syn = state.get("diagnostic_synthesis") or {}
    return GovernedRunResult(
        report=str(state.get("report", "")),
        synthesis=syn if isinstance(syn, dict) else dict(syn),
        latency_s=latency_s,
        mode="governed_live",
    )


def _empty_narrative_scores(case: BenchmarkCase, *, error: str) -> dict[str, Any]:
    required_groups = case.required_keyword_groups()
    required_themes = case.required_action_themes()
    groups_required = min(case.min_keyword_groups_hit, len(required_groups)) if required_groups else 0
    themes_required = min(case.min_action_themes_hit, len(required_themes)) if required_themes else 0
    return {
        "keyword_groups_hit": 0,
        "keyword_groups_required": groups_required,
        "keyword_groups_pass": groups_required == 0,
        "missing_keyword_groups": [g[0] for g in required_groups],
        "action_themes_hit": 0,
        "action_themes_required": themes_required,
        "action_themes_pass": themes_required == 0,
        "missing_action_themes": list(required_themes),
        "residual_ack_pass": False,
        "mentions_residual": False,
        "hindsight_groups_hit": [],
        "hindsight_keyword_groups": [],
        "possible_parametric_leak": False,
        "layer_a": {"configured": False, "pass": True},
        "layer_b": {"configured": False, "pass": True},
        "validation_errors": [error],
        "used_fallback": False,
        "score_error": error,
    }


def _governed_scores(synthesis: dict[str, Any], case: BenchmarkCase, facts_residual_pct: float) -> dict[str, Any]:
    try:
        model = DiagnosticSynthesis.model_validate(synthesis)
    except Exception as exc:
        return _empty_narrative_scores(case, error=f"synthesis_invalid: {exc}")
    narrative = score_narrative_for_case(
        model,
        case,
        residual_pct=facts_residual_pct,
    )
    return {
        **narrative,
        "validation_errors": validate_synthesis(model),
        "used_fallback": False,
    }


def _baseline_scores(result: BaselineRunResult, case: BenchmarkCase) -> dict[str, Any]:
    narrative = score_narrative_for_case(
        result.synthesis,
        case,
        residual_pct=result.facts.residual_pct,
    )
    return {
        **narrative,
        "validation_errors": result.validation_errors,
        "used_fallback": result.used_fallback,
        "prompt_variant": result.prompt_variant,
        "latency_s": round(result.latency_s, 3),
        "token_usage": result.token_usage,
    }


def _write_compare_scorecard(
    case_dir: Path,
    *,
    case: BenchmarkCase,
    residual_ratio: float,
    gov_scores: dict[str, Any],
    base_scores: dict[str, Any],
    hint: dict[str, Any],
) -> None:
    """Always write residual + keyword/action scores, even when narrative fails."""
    lines = [
        f"# Compare pack — `{case.test_id}`",
        "",
        f"**Residual ratio (deterministic):** `{residual_ratio:.1%}` "
        f"(floor `{case.min_residual_ratio:.0%}`). Quant residual is the hard bar.",
        "",
        "Narrative keyword / action scores are **soft and model-dependent**.",
        "",
        "| Path | keyword groups | action themes | residual ack | validation |",
        "|------|----------------|---------------|--------------|------------|",
        (
            f"| governed | {gov_scores.get('keyword_groups_hit', 0)}/"
            f"{gov_scores.get('keyword_groups_required', 0)} | "
            f"{gov_scores.get('action_themes_hit', 0)}/"
            f"{gov_scores.get('action_themes_required', 0)} | "
            f"{gov_scores.get('residual_ack_pass')} | "
            f"{gov_scores.get('validation_errors') or 'clean'} |"
        ),
        (
            f"| baseline | {base_scores.get('keyword_groups_hit', 0)}/"
            f"{base_scores.get('keyword_groups_required', 0)} | "
            f"{base_scores.get('action_themes_hit', 0)}/"
            f"{base_scores.get('action_themes_required', 0)} | "
            f"{base_scores.get('residual_ack_pass')} | "
            f"{base_scores.get('validation_errors') or 'clean'} |"
        ),
        "",
        f"**Improvement hint:** `{hint.get('primary')}`",
        "",
        "Side-by-side reports: `governed_report.md` vs `baseline_report.md`.",
    ]
    (case_dir / "scorecard.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_comparison_case(
    case: BenchmarkCase,
    *,
    baseline_prompt: BaselinePrompt = "simple",
    out_dir: Path | None = None,
) -> ComparisonRow:
    _require_openai_api_key()
    snap, surf = load_fixture(case.fixture)
    apply_pipeline_position(snap)
    pricing = price_and_attribute(snap, surf, None, config=CFG)
    news = frozen_news_for_case(case)
    total = pricing.pnl.total_pnl
    residual_ratio = abs(pricing.pnl.residual_pnl) / abs(total) if abs(total) > 1e-12 else 0.0
    try:
        governed = run_governed_case(case)
    except Exception as exc:
        governed = GovernedRunResult(
            report=f"_Governed run failed: {exc}_\n",
            synthesis={},
            latency_s=0.0,
            mode="governed_error",
        )
    try:
        baseline = run_baseline_diagnosis(
            snap,
            pricing,
            news,
            prompt_variant=baseline_prompt,
            case_context=None,
            require_llm=True,
        )
        base_scores = _baseline_scores(baseline, case)
        baseline_report = baseline.report
        desk_packet = baseline.desk_packet
    except Exception as exc:
        base_scores = {
            **_empty_narrative_scores(case, error=f"baseline_failed: {exc}"),
            "latency_s": 0.0,
            "prompt_variant": baseline_prompt,
            "token_usage": {},
            "used_fallback": False,
        }
        baseline_report = f"_Baseline run failed: {exc}_\n"
        desk_packet = "_unavailable_\n"

    case_dir = out_dir or historical_compare_dir(case.test_id)
    case_dir.mkdir(parents=True, exist_ok=True)

    governed_path = case_dir / "governed_report.md"
    baseline_path = case_dir / "baseline_report.md"
    desk_path = case_dir / "desk_packet.md"
    governed_path.write_text(governed.report, encoding="utf-8")
    baseline_path.write_text(baseline_report, encoding="utf-8")
    desk_path.write_text(desk_packet, encoding="utf-8")
    (case_dir / "ground_truth.md").write_text(
        format_ground_truth_markdown(case), encoding="utf-8"
    )

    gov_syn = governed.synthesis
    facts_residual_pct = (
        abs(pricing.pnl.residual_pnl) / abs(total) * 100.0 if abs(total) > 1e-12 else 0.0
    )
    gov_scores = {
        "mode": governed.mode,
        "latency_s": round(governed.latency_s, 3),
        **_governed_scores(gov_syn, case, facts_residual_pct),
    }
    hint = attribute_governed_vs_baseline(gov_scores, base_scores, case)
    _write_compare_scorecard(
        case_dir,
        case=case,
        residual_ratio=residual_ratio,
        gov_scores=gov_scores,
        base_scores=base_scores,
        hint=hint,
    )
    return ComparisonRow(
        test_id=case.test_id,
        residual_ratio=round(residual_ratio, 4),
        governed=gov_scores,
        baseline=base_scores,
        improvement_hint=hint,
        governed_report_path=str(governed_path),
        baseline_report_path=str(baseline_path),
        desk_packet_path=str(desk_path),
    )


def run_comparison_suite(
    *,
    baseline_prompt: BaselinePrompt = "simple",
    only_case: str | None = None,
) -> list[ComparisonRow]:
    _require_openai_api_key()
    cases = load_cases()
    if only_case:
        cases = [c for c in cases if c.test_id == only_case]
        if not cases:
            raise ValueError(f"Unknown case id: {only_case}")
    return [
        run_comparison_case(case, baseline_prompt=baseline_prompt)
        for case in cases
    ]


def summarize_rows(rows: list[ComparisonRow]) -> dict[str, Any]:
    def _pass_rate(getter) -> float:
        if not rows:
            return 0.0
        return sum(1 for r in rows if getter(r)) / len(rows)

    return {
        "case_count": len(rows),
        "governed_keyword_groups_pass_rate": _pass_rate(
            lambda r: r.governed.get("keyword_groups_pass")
        ),
        "baseline_keyword_groups_pass_rate": _pass_rate(
            lambda r: r.baseline.get("keyword_groups_pass")
        ),
        "governed_action_themes_pass_rate": _pass_rate(
            lambda r: r.governed.get("action_themes_pass")
        ),
        "baseline_action_themes_pass_rate": _pass_rate(
            lambda r: r.baseline.get("action_themes_pass")
        ),
        "governed_residual_ack_rate": _pass_rate(lambda r: r.governed.get("residual_ack_pass")),
        "baseline_residual_ack_rate": _pass_rate(lambda r: r.baseline.get("residual_ack_pass")),
        "governed_validation_clean_rate": _pass_rate(
            lambda r: not r.governed.get("validation_errors")
        ),
        "baseline_validation_clean_rate": _pass_rate(
            lambda r: not r.baseline.get("validation_errors")
        ),
        "governed_parametric_leak_rate": _pass_rate(
            lambda r: r.governed.get("possible_parametric_leak")
        ),
        "baseline_parametric_leak_rate": _pass_rate(
            lambda r: r.baseline.get("possible_parametric_leak")
        ),
        "structure_helps_rate": _pass_rate(
            lambda r: str(r.improvement_hint.get("primary", "")).startswith(
                "structure_helps"
            )
        ),
        "both_miss_layer_b_rate": _pass_rate(
            lambda r: r.improvement_hint.get("primary")
            == "both_miss_layer_b_try_prompt_and_structure"
        ),
        "median_governed_latency_s": sorted(r.governed.get("latency_s", 0.0) for r in rows)[
            len(rows) // 2
        ]
        if rows
        else 0.0,
        "median_baseline_latency_s": sorted(r.baseline.get("latency_s", 0.0) for r in rows)[
            len(rows) // 2
        ]
        if rows
        else 0.0,
    }


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare governed graph vs baseline agent (live LLM only)."
    )
    parser.add_argument("--case", default=None, help="Run one case by test_id.")
    parser.add_argument(
        "--baseline-prompt",
        choices=("simple", "cot"),
        default="simple",
        help="Baseline prompt variant.",
    )
    args = parser.parse_args(argv)

    lineage = news_lineage_errors()
    if lineage:
        raise RuntimeError("historical news lineage errors:\n" + "\n".join(lineage))
    rows = run_comparison_suite(
        baseline_prompt=args.baseline_prompt,
        only_case=args.case,
    )
    summary = summarize_rows(rows)
    payload = {
        "mode": "live",
        "news_lineage": "as_of_only",
        "parametric_knowledge_caveat": PARAMETRIC_KNOWLEDGE_CAVEAT,
        "baseline_prompt": args.baseline_prompt,
        "summary": summary,
        "results": [asdict(r) for r in rows],
    }
    out = HISTORICAL_OUTPUT_DIR / "comparison_summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"summary -> {out}")
    for row in rows:
        print(
            f"{row.test_id}: residual={row.residual_ratio:.1%} | "
            f"gov_grp={row.governed.get('keyword_groups_hit', 0)}/{row.governed.get('keyword_groups_required', 0)} "
            f"base_grp={row.baseline.get('keyword_groups_hit', 0)}/{row.baseline.get('keyword_groups_required', 0)} | "
            f"gov_hindsight={len(row.governed.get('hindsight_groups_hit') or [])}/"
            f"{len(row.governed.get('hindsight_keyword_groups') or [])} "
            f"base_hindsight={len(row.baseline.get('hindsight_groups_hit') or [])}/"
            f"{len(row.baseline.get('hindsight_keyword_groups') or [])} | "
            f"gov_leak={row.governed.get('possible_parametric_leak')} "
            f"base_leak={row.baseline.get('possible_parametric_leak')} | "
            f"gov_theme={row.governed.get('action_themes_hit', 0)}/{row.governed.get('action_themes_required', 0)} "
            f"base_theme={row.baseline.get('action_themes_hit', 0)}/{row.baseline.get('action_themes_required', 0)} | "
            f"hint={row.improvement_hint.get('primary')}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
