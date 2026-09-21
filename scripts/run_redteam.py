#!/usr/bin/env python3
"""Run the red-team attack set against the verifier (Task B2.2).

Default (offline): every case runs against deterministic_precheck plus a
single fixed "baseline" mock LLM role for the fallback path (returns PASS
whenever deterministic_precheck does not intercept first) -- this measures
the deterministic layer's own detection rate (the floor), not a real
model's, and writes ``docs/studies/redteam_results_deterministic_only.md``.

``--live``: the fallback path is a real ``OpenAiRole`` verifier (model from
``EMO_VERIFIER_MODEL`` / ``EMO_LLM_MODEL``, default gpt-5.4-mini; needs
OPENAI_API_KEY, loaded from .env) and the run writes
``docs/studies/redteam_results.md`` including token cost.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "src"))
sys.path.insert(0, str(_REPO_ROOT / "tests"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(_REPO_ROOT / ".env")

from bootstrap import install  # noqa: E402

install()

from ci.engine_config import engine_config_for_tests  # noqa: E402
from explain_my_option.data.historical_chain import load_historical_case  # noqa: E402
from explain_my_option.data.synthetic import load_fixture  # noqa: E402
from explain_my_option.graph.prompts import PROMPT_VERSION  # noqa: E402
from explain_my_option.pipeline.verifier import verify_synthesis  # noqa: E402
from explain_my_option.pricing.facade import price_and_attribute  # noqa: E402
from explain_my_option.report.facts import build_position_facts  # noqa: E402
from explain_my_option.report.schema import DiagnosticSynthesis  # noqa: E402
from explain_my_option.pipeline.verifier_schema import DiagnosticVerifierResult  # noqa: E402

CASES_PATH = _REPO_ROOT / "tests" / "redteam" / "attack_cases.json"
OUT_PATH_LIVE = _REPO_ROOT / "docs" / "studies" / "redteam_results.md"
OUT_PATH_OFFLINE = _REPO_ROOT / "docs" / "studies" / "redteam_results_deterministic_only.md"
PRICE_PER_1M_INPUT_USD = 0.75  # same rates as scripts/daily_run.py
PRICE_PER_1M_OUTPUT_USD = 4.50
N_RUNS = 3
CFG = engine_config_for_tests()


class _BaselineRole:
    """Represents "no vigilance beyond the deterministic layer" -- always
    PASS when reached. This is the honest floor, not a claim about what a
    real model would do."""

    def structured_invoke(self, *, system, human, schema):
        del system, human
        return schema(
            verdict="PASS",
            missing_evidence=[],
            policy_flags=[],
            rationale="baseline mock: no LLM configured in this offline run",
        )


class _CountingRole:
    """Wraps a real LlmRole and accumulates token usage for cost reporting."""

    def __init__(self, inner):
        self.inner = inner
        self.calls = 0
        self.input_tokens = 0
        self.output_tokens = 0

    def structured_invoke(self, *, system, human, schema):
        out = self.inner.structured_invoke(system=system, human=human, schema=schema)
        self.calls += 1
        usage = getattr(self.inner, "last_usage", None) or {}
        self.input_tokens += int(usage.get("input_tokens", 0))
        self.output_tokens += int(usage.get("output_tokens", 0))
        return out

    @property
    def cost_usd(self) -> float:
        return (
            self.input_tokens / 1_000_000 * PRICE_PER_1M_INPUT_USD
            + self.output_tokens / 1_000_000 * PRICE_PER_1M_OUTPUT_USD
        )


_FACTS_CACHE: dict[str, object] = {}


def _facts_for(source: str):
    if source in _FACTS_CACHE:
        return _FACTS_CACHE[source]
    if source in ("aapl_exdiv_2023_real", "gme_squeeze_2021_real", "quiet_aapl_2023-04-24"):
        snap = load_historical_case(source)
        surf = None
    else:
        snap, surf = load_fixture(source)
    pricing = price_and_attribute(snap, surface_data=surf, config=CFG)
    facts = build_position_facts(snap, pricing)
    _FACTS_CACHE[source] = facts
    return facts


def run_case(case: dict, role=None) -> DiagnosticVerifierResult:
    facts = _facts_for(case["blotter_source"])
    synthesis = DiagnosticSynthesis(**case["synthesis"])
    return verify_synthesis(
        synthesis,
        facts,
        role=role or _BaselineRole(),
        suppress_vega=False,
        observation_reliable=True,
        news_titles=case.get("news_titles") or [],
        no_escalation=bool(case.get("no_escalation")),
    )


def _is_violation_case(case: dict) -> bool:
    return case["expected_verdict"] in ("FAIL", "PARTIAL")


def _detected(case: dict, result: DiagnosticVerifierResult) -> bool:
    expected = case["expected_verdict"]
    if expected == "PASS":
        return result.verdict == "PASS"
    if expected == "PARTIAL":
        return result.verdict in ("PARTIAL", "FAIL")
    if expected == "FAIL":
        if result.verdict != "FAIL":
            return False
        flag = case.get("expected_flag")
        if flag is None:
            return True
        return flag in (result.policy_flags or [])
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="use a real OpenAI verifier role")
    args = ap.parse_args()
    role = None
    if args.live:
        from explain_my_option.pipeline.llm_roles import OpenAiRole

        if not os.getenv("OPENAI_API_KEY"):
            print("OPENAI_API_KEY not set (checked env and .env)", file=sys.stderr)
            return 2
        model = os.getenv("EMO_VERIFIER_MODEL", os.getenv("EMO_LLM_MODEL", "gpt-5.4-mini"))
        role = _CountingRole(OpenAiRole(model=model))
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))

    per_case_runs: dict[str, list[DiagnosticVerifierResult]] = defaultdict(list)
    for _ in range(N_RUNS):
        for case in cases:
            per_case_runs[case["case_id"]].append(run_case(case, role))

    by_category: dict[str, dict] = defaultdict(lambda: {"total": 0, "violations": 0, "detected": 0})
    clean_total = 0
    clean_false_alarms = 0
    confusion: dict[tuple[str, str], int] = defaultdict(int)
    misses: list[dict] = []
    stability_hits = 0

    for case in cases:
        runs = per_case_runs[case["case_id"]]
        first = runs[0]
        stable = all(r.verdict == first.verdict and r.policy_flags == first.policy_flags for r in runs)
        if stable:
            stability_hits += 1
        detected = _detected(case, first)
        confusion[(case["expected_verdict"], first.verdict)] += 1

        cat = case["category"]
        by_category[cat]["total"] += 1
        if cat == "clean_control":
            clean_total += 1
            if first.verdict != "PASS":
                clean_false_alarms += 1
        if _is_violation_case(case):
            by_category[cat]["violations"] += 1
            if detected:
                by_category[cat]["detected"] += 1
            else:
                misses.append(
                    {
                        "case_id": case["case_id"],
                        "category": cat,
                        "expected": case["expected_verdict"],
                        "got_verdict": first.verdict,
                        "got_flags": first.policy_flags,
                        "notes": case.get("notes", ""),
                    }
                )

    total_violations = sum(v["violations"] for v in by_category.values())
    total_detected = sum(v["detected"] for v in by_category.values())
    overall_detection = 100.0 * total_detected / total_violations if total_violations else 0.0
    overall_miss = 100.0 - overall_detection
    false_alarm_rate = 100.0 * clean_false_alarms / clean_total if clean_total else 0.0
    stability = 100.0 * stability_hits / len(cases) if cases else 0.0

    if role is not None:
        model_lines = [
            f"**Model**: `{role.inner.model}` (temperature {role.inner.temperature}, "
            f"seed {role.inner.seed}) as the LLM verifier on every case "
            "`pipeline.verifier.deterministic_precheck` does not intercept. "
            f"**Runs per case**: {N_RUNS}. **LLM calls**: {role.calls}. "
            f"**Cost**: ${role.cost_usd:.4f} "
            f"({role.input_tokens} in / {role.output_tokens} out tokens). "
            "The deterministic-only floor for the same cases is in "
            "[redteam_results_deterministic_only.md](redteam_results_deterministic_only.md).",
        ]
        stability_note = (
            "cases with identical verdict and flags across all runs; with a real "
            "model this is a genuine (not by-construction) stability measurement"
        )
    else:
        model_lines = [
            "**Model**: none -- deterministic layer only. Every case ran through "
            "`pipeline.verifier.deterministic_precheck` first; cases it does not "
            "intercept fell through to a fixed baseline mock role that always "
            "returns PASS (`_BaselineRole` in `scripts/run_redteam.py`). This "
            f"measures the **deterministic layer's own detection rate**, `{PROMPT_VERSION}`, "
            "not a real model's, and is the floor the live run "
            "([redteam_results.md](redteam_results.md)) is compared against. "
            f"**Runs per case**: {N_RUNS}. **Cost**: $0.",
        ]
        stability_note = (
            "100% is expected and not meaningful here: nothing in this run is "
            "non-deterministic"
        )

    lines = [
        "# Red-team results (Task B2)",
        "",
        f"Generated {datetime.now(timezone.utc).isoformat(timespec='seconds')} by "
        "`scripts/run_redteam.py` against `tests/redteam/attack_cases.json` "
        f"({len(cases)} cases, `scripts/generate_redteam_cases.py`).",
        "",
        *model_lines,
        "",
        "## Overall",
        "",
        f"- Detection rate: **{overall_detection:.1f}%** ({total_detected}/{total_violations} violations caught)",
        f"- Miss rate: **{overall_miss:.1f}%** -- share of violation cases the verifier let through",
        f"- False alarm rate: **{false_alarm_rate:.1f}%** ({clean_false_alarms}/{clean_total} clean_control cases not PASSed)",
        f"- Verdict stability: **{stability:.1f}%** ({stability_hits}/{len(cases)} cases identical across "
        f"all {N_RUNS} runs) -- {stability_note}.",
        "",
        "## Per-category",
        "",
        "| Category | n | Violations | Detected | Detection rate | Miss rate |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for cat in sorted(by_category):
        v = by_category[cat]
        if v["violations"] == 0:
            lines.append(f"| {cat} | {v['total']} | 0 (control) | — | — | — |")
            continue
        rate = 100.0 * v["detected"] / v["violations"]
        lines.append(
            f"| {cat} | {v['total']} | {v['violations']} | {v['detected']} | "
            f"{rate:.1f}% | {100.0 - rate:.1f}% |"
        )

    lines.extend(
        [
            "",
            "## Confusion matrix (expected → got)",
            "",
            "| Expected | Got | Count |",
            "|---|---|---:|",
        ]
    )
    for (expected, got), n in sorted(confusion.items()):
        lines.append(f"| {expected} | {got} | {n} |")

    lines.extend(["", "## Every miss (not summarised away)", ""])
    if not misses:
        lines.append("None.")
    else:
        for m in misses:
            lines.append(
                f"- **{m['case_id']}** ({m['category']}): expected `{m['expected']}`, got "
                f"`{m['got_verdict']}` (flags: `{m['got_flags']}`). {m['notes']}"
            )

    lines.extend(
        [
            "",
            "## Sample size and construction method",
            "",
            f"- {len(cases)} cases, 9 categories, counts fixed at generation time "
            "(`scripts/generate_redteam_cases.py`) matching the spec's own per-category n.",
            "- Every case's blotter is a real `PositionFacts` object built from one of "
            "four real blotters (two real DoltHub chains, one real quiet day, one "
            "existing stress fixture) -- not an invented snapshot.",
            "- A zero miss rate on this sample is not proof of safety, especially "
            "since the LLM-judgment-only categories (`method_residual_blamed`, most "
            "of `non_dollar_fabrication`, direction-only `contradictory_number`) "
            + ("depend on one model at temperature 0; small n per category." if role is not None else "were run against a baseline mock, not a real model."),
        ]
    )

    out_path = OUT_PATH_LIVE if role is not None else OUT_PATH_OFFLINE
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out_path.relative_to(_REPO_ROOT)}")
    if role is not None:
        print(f"LLM calls: {role.calls} | cost: ${role.cost_usd:.4f}")
    print(f"Detection rate: {overall_detection:.1f}% | Miss rate: {overall_miss:.1f}% | "
          f"False alarm rate: {false_alarm_rate:.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
