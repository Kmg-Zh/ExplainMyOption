#!/usr/bin/env python3
"""Compare LLM models on the agent's four roles under a hard spending cap.

Every model answers the same cases, all read from data the repo has already
accumulated (nothing is fetched and nothing is written back):

  redteam     the constructed attacks on real blotters: verifier detection,
              misses and false alarms (tests/redteam/attack_cases.json)
  historical  the five historical events with frozen as-of news, scored with
              the desk rubric (tests/historical)
  archive     archived live-book days replayed with their frozen market and
              news: verdict mix, overruled FAILs, narrator fallbacks

The model under test plays all four roles through the production OpenAiRole,
exactly as setting EMO_LLM_MODEL would. Every API response is cached under
tests/output/model_comparison/ (gitignored), so a rerun, or a run stopped by
--max-usd, pays only for calls it has not made yet. Each case runs on every
model before the next case starts, so a stopped run still compares the models
on the same cases.

    python scripts/compare_models.py --dry-run      # no API calls: planned calls and cost
    python scripts/compare_models.py --models gpt-5.4-mini,gpt-6-sol --max-usd 5
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import importlib.util
import json
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "src"))
sys.path.insert(0, str(_REPO_ROOT / "tests"))

OUT = _REPO_ROOT / "tests" / "output" / "model_comparison"
CACHE = OUT / "cache"
DOC = _REPO_ROOT / "docs" / "studies" / "model_comparison.md"
SAMPLES = _REPO_ROOT / "docs" / "studies" / "model_comparison"

# USD per 1M tokens (input, output), standard tier, from public price lists in
# October 2026. Cached input is billed at the full input rate here, so every
# cost below is an upper bound.
PRICES = {
    "gpt-5.4-mini": (0.75, 4.50),
    "gpt-5.4": (2.50, 15.00),
    "gpt-5.5": (5.00, 30.00),
    "gpt-5.6-terra": (2.00, 12.00),
    "gpt-5.6-sol": (5.00, 30.00),
    "gpt-6-sol": (2.00, 10.00),
    "gpt-6.1-sol": (2.00, 10.00),
    "gpt-6-astra": (10.00, 50.00),
}
ROLES = {
    "IntelDigest": "digester",
    "CatalystChallenge": "critic",
    "DiagnosticSynthesis": "narrator",
    "DiagnosticVerifierResult": "verifier",
}
# Output tokens assumed for a call not observed yet: the dry run's estimate and
# the budget check before the first call of each role.
OUTPUT_ALLOWANCE = {"digester": 800, "critic": 600, "narrator": 1500, "verifier": 600}
# These reject an explicit temperature (HTTP 400 "Unsupported value"), which the
# production OpenAiRole always sends (0.0), so here they run at their default:
# the same footing as gpt-5* models, whose temperature langchain-openai drops.
DEFAULT_TEMPERATURE_ONLY = {"gpt-6-sol", "gpt-6.1-sol", "gpt-6-astra"}
SUITES = ("redteam", "historical", "archive")
DEFAULT_DAYS = ("2026-09-07", "2026-10-15")
_FALLBACK_PREFIX = "LLM synthesis failed"


@dataclass
class Call:
    model: str
    role: str
    input_tokens: int
    output_tokens: int
    reasoning_tokens: int = 0
    cached_tokens: int = 0
    latency_s: float = 0.0
    cost_usd: float = 0.0
    source: str = "api"  # "api", "cache" or "planned" (dry run)
    error: str = ""


class BudgetExhausted(RuntimeError):
    """Raised before a call that could take this run's spending past --max-usd."""


class Ledger:
    def __init__(self, max_usd: float) -> None:
        self.max_usd = max_usd
        self.calls: list[Call] = []
        self.spent = 0.0  # paid in this run; cache hits are free
        self.exhausted = False

    def allowance(self, model: str, role: str) -> int:
        seen = [c.output_tokens for c in self.calls if (c.model, c.role) == (model, role) and c.source == "api"]
        return int(max(seen) * 1.5) if seen else OUTPUT_ALLOWANCE[role]


def cost(model: str, input_tokens: int, output_tokens: int) -> float:
    price_in, price_out = PRICES[model]
    return (input_tokens * price_in + output_tokens * price_out) / 1_000_000


@functools.lru_cache(maxsize=1)
def _encoding():
    import tiktoken

    return tiktoken.get_encoding("o200k_base")


def prompt_tokens(system: str, human: str, schema) -> int:
    """Approximate billed input: both messages plus the structured-output schema."""
    return len(_encoding().encode(system + human + json.dumps(schema.model_json_schema())))


def _placeholder(schema):
    """A schema-valid answer for --dry-run, so the graph walks its full path."""
    name = schema.__name__
    if name == "DiagnosticSynthesis":
        return schema(
            primary_driver="Delta / spot move",
            verdict="Dry run.",
            confidence_level="medium",
            confidence_rationale="Dry run.",
            takeaways=["Dry run."],
        )
    if name == "DiagnosticVerifierResult":
        return schema(verdict="PASS", rationale="Dry run.")
    if name == "CatalystChallenge":
        return schema(layer_b_required=False, rationale="Dry run.")
    return schema(brief="Dry run.")


class StudyRole:
    """The model under test behind every role: the cache first, then the API under the cap."""

    def __init__(self, model: str, ledger: Ledger, *, dry_run: bool) -> None:
        from explain_my_option.pipeline.llm_roles import OpenAiRole

        self.model = model
        self.ledger = ledger
        self.dry_run = dry_run
        self.api = OpenAiRole(model=model)
        if model in DEFAULT_TEMPERATURE_ONLY:
            self.api.temperature = None  # omitted from the request

    def structured_invoke(self, *, system: str, human: str, schema):
        role = ROLES[schema.__name__]
        key = hashlib.sha256("\x00".join((self.model, schema.__name__, system, human)).encode()).hexdigest()
        cached = CACHE / f"{key}.json"
        if cached.exists():
            entry = json.loads(cached.read_text(encoding="utf-8"))
            self.ledger.calls.append(Call(**{**entry["call"], "source": "cache"}))
            return schema.model_validate(entry["parsed"])
        tokens_in = prompt_tokens(system, human, schema)
        if self.dry_run:
            tokens_out = OUTPUT_ALLOWANCE[role]
            self.ledger.calls.append(
                Call(self.model, role, tokens_in, tokens_out, cost_usd=cost(self.model, tokens_in, tokens_out), source="planned")
            )
            return _placeholder(schema)
        estimate = cost(self.model, tokens_in, self.ledger.allowance(self.model, role))
        if self.ledger.spent + estimate > self.ledger.max_usd:
            self.ledger.exhausted = True
            raise BudgetExhausted(f"the next {role} call (~${estimate:.4f}) would pass ${self.ledger.max_usd:.2f}")
        self.api.last_usage = None
        started = time.perf_counter()
        error = ""
        try:
            result = self.api.structured_invoke(system=system, human=human, schema=schema)
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"[:300]
            raise
        finally:
            usage = self.api.last_usage or {}
            call = Call(
                self.model,
                role,
                input_tokens=int(usage.get("input_tokens", 0)),
                output_tokens=int(usage.get("output_tokens", 0)),
                reasoning_tokens=int((usage.get("output_token_details") or {}).get("reasoning", 0)),
                cached_tokens=int((usage.get("input_token_details") or {}).get("cache_read", 0)),
                latency_s=round(time.perf_counter() - started, 3),
                error=error,
            )
            call.cost_usd = cost(self.model, call.input_tokens, call.output_tokens)
            self.ledger.spent += call.cost_usd
            self.ledger.calls.append(call)
        CACHE.mkdir(parents=True, exist_ok=True)
        cached.write_text(json.dumps({"call": asdict(call), "parsed": result.model_dump()}), encoding="utf-8")
        return result


def leg_outcome(state: dict) -> dict:
    """What the governed graph shipped for one leg, beyond the report text."""
    from explain_my_option.pipeline.verifier import DETERMINISTIC_PRECHECK_RATIONALES

    findings = state.get("diagnostic_findings") or {}
    trace = (findings.get("verifier_audit") or {}).get("trace") or []
    if state.get("no_escalation"):
        status = "quiet"
    else:
        status = findings.get("verifier_status") or (trace[-1]["verdict"] if trace else "unverified")
    rationale = str((state.get("diagnostic_synthesis") or {}).get("confidence_rationale") or "")
    return {
        "status": status,
        "terminal_break": bool(findings.get("terminal_unexplained_break")),
        "narrator_fallback": rationale.startswith(_FALLBACK_PREFIX),
        "verifier_by_code": sum(t.get("rationale") in DETERMINISTIC_PRECHECK_RATIONALES for t in trace),
        "overruled_fails": sum(t.get("llm_verdict") == "FAIL" and t.get("verdict") != "FAIL" for t in trace),
        "llm_calls": state.get("llm_calls"),
    }


def _load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, _REPO_ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


Runner = Callable[[Any, Any], dict]


def redteam_cases() -> list[tuple[str, Runner]]:
    redteam = _load_script("run_redteam")

    def runner(case: dict) -> Runner:
        def run(roles, _config) -> dict:
            result = redteam.run_case(case, roles.verifier)
            return {
                "category": case["category"],
                "expected": case["expected_verdict"],
                "verdict": result.verdict,
                "flags": list(result.policy_flags or []),
                "violation": redteam._is_violation_case(case),
                "detected": redteam._detected(case, result),
                "overruled_fail": getattr(result, "llm_verdict", None) == "FAIL" and result.verdict != "FAIL",
            }

        return run

    cases = json.loads(redteam.CASES_PATH.read_text(encoding="utf-8"))
    return [(case["case_id"], runner(case)) for case in cases]


def historical_cases() -> list[tuple[str, Runner]]:
    from historical.cases import load_cases, news_lineage_errors
    from historical.pipeline_position import pipeline_run_kwargs
    from historical.run import _deps_for_case
    from historical.scoring import score_narrative_for_case

    from explain_my_option.agent_graph import run_pipeline
    from explain_my_option.report.schema import DiagnosticSynthesis

    lineage = news_lineage_errors()
    if lineage:
        raise RuntimeError("historical news lineage errors:\n" + "\n".join(lineage))

    def runner(case) -> Runner:
        def run(roles, config) -> dict:
            state = run_pipeline(
                ticker=case.ticker,
                option_type=str(case.input_quant["option_type"]),
                strike=float(case.input_quant["strike"]),
                expiry=str(case.input_quant["expiry"]),
                **pipeline_run_kwargs(),
                deps=_deps_for_case(case),
                config=config,
                roles=roles,
            )
            pnl = state["pricing"].pnl
            scores = score_narrative_for_case(
                DiagnosticSynthesis.model_validate(state["diagnostic_synthesis"]),
                case,
                residual_pct=100.0 * abs(pnl.residual_pnl) / abs(pnl.total_pnl),
            )
            return {
                **leg_outcome(state),
                "tier": case.tier,
                "keyword_groups": f"{scores['keyword_groups_hit']}/{scores['keyword_groups_required']}",
                "desk_bar": scores["keyword_groups_pass"] and scores["action_themes_pass"],
                "layer_a": (scores.get("layer_a") or {}).get("pass"),
                "layer_b": (scores.get("layer_b") or {}).get("pass"),
                "residual_ack": scores["residual_ack_pass"],
                "parametric_leak": scores["leak_marker_hits"],
                "report": state["report"],
            }

        return run

    return [(case.test_id, runner(case)) for case in load_cases()]


def archive_cases(root: Path, days: list[str]) -> list[tuple[str, Runner]]:
    from live_book.replay_archives import (
        FrozenMarketLoader,
        FrozenNewsSource,
        _latest_source_run,
        _news_from_rows,
        _snapshot_from_dict,
        _surface_from_dict,
    )

    from explain_my_option.agent_graph import run_pipeline
    from explain_my_option.graph.deps import GraphDeps, OfficialFdmPnlSource
    from explain_my_option.intel.planner import CueQueryPlanner
    from explain_my_option.intel.sources import IntelRegistry, StubIntelSource
    from explain_my_option.pricing.types import LoadedData

    def runner(payload: dict) -> Runner:
        def run(roles, config) -> dict:
            # A fresh snapshot per run: the graph applies the leg to it in place.
            snap = _snapshot_from_dict(payload["snapshot"])
            news = _news_from_rows(payload.get("news") or [])
            deps = GraphDeps(
                market=FrozenMarketLoader(LoadedData(snapshot=snap, surface=_surface_from_dict(payload.get("surface")))),
                pnl=OfficialFdmPnlSource(),
                planner=CueQueryPlanner(),
                intel=IntelRegistry(
                    {
                        "yfinance_news": FrozenNewsSource(news),
                        "tavily": StubIntelSource("tavily"),
                        "sec_8k": StubIntelSource("sec_8k"),
                    }
                ),
            )
            state = run_pipeline(
                ticker=snap.ticker,
                option_type=snap.option_type,
                strike=snap.strike,
                expiry=snap.expiry,
                quantity=snap.quantity,
                multiplier=snap.multiplier,
                deps=deps,
                config=config,
                roles=roles,
            )
            return {**leg_outcome(state), "headlines": len(news), "report": state["report"]}

        return run

    cases = []
    for day in days:
        source = _latest_source_run(root / day)
        if source is None:
            raise FileNotFoundError(f"no archived run for {day} under {root}")
        for path in sorted((source / "legs").glob("*.json")):
            cases.append((f"{day}/{path.stem}", runner(json.loads(path.read_text(encoding="utf-8")))))
    return cases


def run_study(cases, models, ledger, config, *, dry_run: bool) -> dict:
    from explain_my_option.pipeline.llm_roles import LlmRoleRegistry

    results: dict[str, dict[str, dict]] = defaultdict(dict)
    for suite, case_id, run in cases:
        row: dict[str, dict] = {}
        for model in models:
            role = StudyRole(model, ledger, dry_run=dry_run)
            roles = LlmRoleRegistry(narrator=role, verifier=role, challenger=role, digester=role)
            try:
                row[model] = run(roles, config)
            except Exception as exc:  # noqa: BLE001 -- recorded, the study goes on
                row[model] = {"error": f"{type(exc).__name__}: {exc}"[:300]}
            if ledger.exhausted:
                break
        if ledger.exhausted:
            # A role may have swallowed the budget stop and shipped a fallback,
            # so the unfinished case is dropped for every model.
            print(f"budget reached at {suite}/{case_id}; stopping (rerun with a higher --max-usd to resume)")
            break
        results[suite][case_id] = row
        print(f"{suite}/{case_id}: " + ", ".join(f"{m}={row[m].get('status') or row[m].get('verdict') or 'error'}" for m in models))
    return results


# --- Reporting -----------------------------------------------------------------------


def _usage(calls: list[Call], model: str) -> dict:
    mine = [c for c in calls if c.model == model and c.source != "planned"]
    paid = [c for c in mine if not c.error]
    return {
        "calls": len(mine),
        "call_errors": sum(bool(c.error) for c in mine),
        "input_tokens": sum(c.input_tokens for c in mine),
        "output_tokens": sum(c.output_tokens for c in mine),
        "reasoning_tokens": sum(c.reasoning_tokens for c in mine),
        "cost_usd": sum(c.cost_usd for c in mine),
        "mean_latency_s": sum(c.latency_s for c in paid) / len(paid) if paid else 0.0,
        "by_role": dict(Counter(c.role for c in mine)),
    }


def _pct(n: int, d: int) -> str:
    return f"{100.0 * n / d:.0f}% ({n}/{d})" if d else "—"


def _finished(results: dict, suite: str, model: str) -> list[dict]:
    rows = (row.get(model) for row in results.get(suite, {}).values())
    return [r for r in rows if r is not None and "error" not in r]


def summarize(results: dict, models: list[str], calls: list[Call]) -> dict:
    summary: dict[str, dict] = {}
    for model in models:
        red, hist, legs = (_finished(results, suite, model) for suite in SUITES)
        violations = [r for r in red if r["violation"]]
        clean = [r for r in red if r["category"] == "clean_control"]
        narrated = [r for r in hist + legs if r["status"] != "quiet"]
        summary[model] = {
            "redteam_detection": _pct(sum(r["detected"] for r in violations), len(violations)),
            "redteam_false_alarms": _pct(sum(r["verdict"] != "PASS" for r in clean), len(clean)),
            "historical_desk_bar": _pct(sum(bool(r["desk_bar"]) for r in hist), len(hist)),
            "historical_layer_b": _pct(sum(bool(r["layer_b"]) for r in hist), len(hist)),
            "parametric_leak": _pct(sum(bool(r["parametric_leak"]) for r in hist), len(hist)),
            "verdicts": dict(Counter(r["status"] for r in hist + legs)),
            "narrator_fallbacks": _pct(sum(r["narrator_fallback"] for r in narrated), len(narrated)),
            "overruled_fails": sum(r["overruled_fail"] for r in red) + sum(r["overruled_fails"] for r in hist + legs),
            "errors": sum("error" in row.get(model, {}) for suite in results.values() for row in suite.values()),
            "paid_usd": 0.0,
            **_usage(calls, model),
        }
        usage = summary[model]
        usage["calls_label"] = f"{usage['calls']} ({usage['call_errors']})"
        usage["tokens_label"] = f"{usage['input_tokens']:,} / {usage['output_tokens']:,}" + (
            f" ({usage['reasoning_tokens']:,} reasoning)" if usage["reasoning_tokens"] else ""
        )
    return summary


def _paid() -> dict[str, float]:
    """What the study paid per model: every cached API response, counted once."""
    paid: dict[str, float] = defaultdict(float)
    for path in CACHE.glob("*.json"):
        call = json.loads(path.read_text(encoding="utf-8"))["call"]
        paid[call["model"]] += call["cost_usd"]
    return paid


def _carried_findings() -> str:
    """The hand-written "## Findings" section of the current doc, kept across reruns."""
    if not DOC.exists():
        return ""
    match = re.search(r"(?ms)^## Findings\n.*?(?=^## |\Z)", DOC.read_text(encoding="utf-8"))
    return match.group(0).rstrip() + "\n" if match else ""


def _demote(markdown: str, levels: int = 2) -> str:
    return re.sub(r"(?m)^(#+) ", lambda m: "#" * (len(m.group(1)) + levels) + " ", markdown)


def _side_by_side(title: str, case_id: str, row: dict, models: list[str]) -> str:
    lines = [f"# {title}", "", f"Case `{case_id}`, the same frozen inputs for every model. Generated by `scripts/compare_models.py`.", ""]
    for model in models:
        result = row.get(model) or {}
        lines.extend([f"## {model}", ""])
        lines.append(_demote(result["report"]) if "report" in result else f"_No report: {result.get('error', 'not run')}_")
        lines.append("")
    return "\n".join(lines)


def write_outputs(results: dict, models: list[str], ledger: Ledger, args) -> None:
    from explain_my_option.graph.prompts import PROMPT_VERSION

    OUT.mkdir(parents=True, exist_ok=True)
    summary = summarize(results, models, ledger.calls)
    stripped = {
        suite: {cid: {m: {k: v for k, v in r.items() if k != "report"} for m, r in row.items()} for cid, row in rows.items()}
        for suite, rows in results.items()
    }
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    (OUT / "results.json").write_text(
        json.dumps(
            {"generated": generated, "prompt_version": PROMPT_VERSION, "models": models, "summary": summary,
             "results": stripped, "calls": [asdict(c) for c in ledger.calls]},
            indent=2,
        ),
        encoding="utf-8",
    )
    SAMPLES.mkdir(parents=True, exist_ok=True)
    for stale in SAMPLES.glob("*.md"):
        stale.unlink()
    samples = []
    for suite in ("historical", "archive"):
        for case_id, row in results.get(suite, {}).items():
            for model, result in row.items():
                if "report" in result:
                    path = OUT / "reports" / suite / case_id / f"{model}.md"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(result["report"], encoding="utf-8")
            # Every event, and the archive legs where the models shipped different verdicts.
            if suite == "historical" or len({r.get("status") for r in row.values()}) > 1:
                name = case_id.replace("/", "_") + ".md"
                (SAMPLES / name).write_text(_side_by_side(case_id, case_id, row, models), encoding="utf-8")
                samples.append((suite, case_id, name))
    for model, usd in _paid().items():
        if model in summary:
            summary[model]["paid_usd"] = usd
    findings = _carried_findings()
    DOC.write_text(
        _study_markdown(generated, PROMPT_VERSION, models, summary, results, samples, args, findings), encoding="utf-8"
    )
    print(f"wrote {DOC.relative_to(_REPO_ROOT)}, {len(samples)} side-by-side samples, and {OUT.relative_to(_REPO_ROOT)}/")


def _study_markdown(generated, prompt_version, models, summary, results, samples, args, findings) -> str:
    def row(label: str, key: str, fmt=str) -> str:
        return f"| {label} | " + " | ".join(fmt(summary[m][key]) for m in models) + " |"

    def verdicts(v: dict) -> str:
        return ", ".join(f"{k} {n}" for k, n in sorted(v.items())) or "—"

    n = {suite: len(results.get(suite, {})) for suite in SUITES}
    lines = [
        "# Model comparison",
        "",
        f"Generated {generated} by `scripts/compare_models.py`, prompt `{prompt_version}`. Each model played all four "
        "roles (digester, catalyst critic, narrator, verifier) through the production `OpenAiRole`, as setting "
        "`EMO_LLM_MODEL` would, on the same cases. Every case comes from data the repo had already accumulated:",
        "",
        f"- **Red team**: {n['redteam']} constructed attacks on real blotters, verifier only, one run per case.",
        f"- **Historical**: {n['historical']} events with frozen as-of news, the full graph with the verifier on, "
        "scored with the desk rubric in `tests/historical/scoring.py`.",
        f"- **Archive**: {n['archive']} archived live-book legs ({', '.join(args.days)}) replayed with their frozen "
        "market and news.",
        "",
        "## Summary",
        "",
        "| | " + " | ".join(f"`{m}`" for m in models) + " |",
        "| --- | " + " | ".join("---:" for _ in models) + " |",
        row("Red-team detection", "redteam_detection"),
        row("Red-team false alarms (clean controls)", "redteam_false_alarms"),
        row("LLM hard FAILs code could not confirm", "overruled_fails"),
        row("Historical: desk bar met (keywords and actions)", "historical_desk_bar"),
        row("Historical: Layer B (catalyst) met", "historical_layer_b"),
        row("Historical: post-event knowledge in the narrative", "parametric_leak"),
        row("Shipped verdicts (historical + archive)", "verdicts", verdicts),
        row("Narrator fallbacks (invalid output or API error)", "narrator_fallbacks"),
        row("Errors (case did not finish)", "errors"),
        row("LLM calls (API errors)", "calls_label"),
        row("Input / output tokens", "tokens_label"),
        row("Mean latency per call", "mean_latency_s", lambda s: f"{s:.1f}s"),
        row("Paid (cached input at the full rate)", "paid_usd", lambda c: f"${c:.2f}"),
        "",
        findings or "## Findings\n\n_Hand-written reading of the tables; reruns keep this section._\n",
    ]

    if results.get("historical"):
        lines.extend(["## Historical events", "", "| Case | Tier | " + " | ".join(f"`{m}`" for m in models) + " |",
                      "| --- | --- | " + " | ".join("---" for _ in models) + " |"])
        for case_id, case_row in results["historical"].items():
            cells = []
            for m in models:
                r = case_row.get(m) or {}
                if "error" in r:
                    cells.append("error")
                    continue
                marks = [r["status"], "desk bar ✓" if r["desk_bar"] else "desk bar ✗", f"keywords {r['keyword_groups']}"]
                if r["parametric_leak"]:
                    marks.append("leak: " + ", ".join(r["parametric_leak"]))
                cells.append("; ".join(marks))
            tier = next((r.get("tier") for r in case_row.values() if r.get("tier")), "")
            lines.append(f"| `{case_id}` | {tier} | " + " | ".join(cells) + " |")
        lines.append("")

    if results.get("archive"):
        lines.extend(["## Archive legs", "", "| Leg | Headlines | " + " | ".join(f"`{m}`" for m in models) + " |",
                      "| --- | ---: | " + " | ".join("---" for _ in models) + " |"])
        for case_id, case_row in results["archive"].items():
            heads = next((r.get("headlines") for r in case_row.values() if "headlines" in r), 0)
            cells = []
            for m in models:
                r = case_row.get(m) or {}
                cell = r.get("status", "error")
                if r.get("narrator_fallback"):
                    cell += ", fallback"
                if r.get("overruled_fails"):
                    cell += ", FAIL overruled"
                cells.append(cell)
            lines.append(f"| `{case_id}` | {heads} | " + " | ".join(cells) + " |")
        lines.append("")

    if results.get("redteam"):
        cats = sorted({r["category"] for row in results["redteam"].values() for r in row.values() if "category" in r})
        lines.extend(["## Red team by category", "", "| Category | " + " | ".join(f"`{m}`" for m in models) + " |",
                      "| --- | " + " | ".join("---:" for _ in models) + " |"])
        for cat in cats:
            cells = []
            for m in models:
                rs = [row[m] for row in results["redteam"].values() if row.get(m, {}).get("category") == cat]
                if cat == "clean_control" or not any(r["violation"] for r in rs):
                    cells.append("passed " + _pct(sum(r["verdict"] == "PASS" for r in rs), len(rs)))
                else:
                    v = [r for r in rs if r["violation"]]
                    cells.append("caught " + _pct(sum(r["detected"] for r in v), len(v)))
            lines.append(f"| {cat} | " + " | ".join(cells) + " |")
        lines.append("")

    if samples:
        lines.extend(["## Reports side by side", ""])
        lines.extend(f"- [{case_id}](model_comparison/{name}) ({suite})" for suite, case_id, name in samples)
        lines.append("")

    lines.extend([
        "## Method and caveats",
        "",
        "- One run per case and model, every model at its default temperature and reasoning effort. "
        "`langchain-openai` drops the production `temperature=0` for `gpt-5*` models unless reasoning effort is "
        "`none`; `gpt-6*` models reject it with HTTP 400, so the study omits it for them (the production "
        "`OpenAiRole` would fail every call and fall back to the rule-based narrative). Outputs are not "
        "deterministic, and differences of one or two cases are noise at this sample size.",
        "- Costs use the list prices in `PRICES` with cached input billed at the full rate, so they are upper "
        "bounds. *Paid* counts every API call the study made once, including calls a later fix made obsolete.",
        "- Historical events predate every model's training data, so a narrative can draw on what happened after "
        "the as-of date; the leak row counts the rubric's post-event markers, which are flagged, never required.",
        "- The red-team verdicts here are one run per case; `docs/studies/redteam_results.md` reports the "
        "three-run stability for the production model.",
        "- Rerunning the script reuses every cached response, so it regenerates these tables and reports for free.",
        "",
    ])
    return "\n".join(lines)


def print_plan(ledger: Ledger, models: list[str], counts: dict) -> None:
    """Planned calls do not depend on the model, so one model's plan prices them all."""
    planned = [c for c in ledger.calls if c.model == models[0]]
    tokens_in = sum(c.input_tokens for c in planned)
    tokens_out = sum(c.output_tokens for c in planned)
    print(f"\nDry run: {', '.join(f'{s} {n}' for s, n in counts.items())} cases; no API calls made.")
    print(f"Per model: {len(planned)} calls ({dict(Counter(c.role for c in planned))}), "
          f"{tokens_in:,} input and ~{tokens_out:,} output tokens.")
    for model, (price_in, price_out) in sorted(PRICES.items(), key=lambda kv: cost(kv[0], tokens_in, tokens_out)):
        print(f"  {model:14s} ${price_in:5.2f} / ${price_out:5.2f} per 1M  ->  ~${cost(model, tokens_in, tokens_out):.2f}")
    print("Output assumed per call: " + ", ".join(f"{r} {n}" for r, n in OUTPUT_ALLOWANCE.items())
          + "; a model that reasons by default can use several times more.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--models", default="gpt-5.4-mini", help="comma-separated model ids (see PRICES)")
    parser.add_argument("--suites", default=",".join(SUITES), help="comma-separated subset of " + ", ".join(SUITES))
    parser.add_argument("--days", default=",".join(DEFAULT_DAYS), help="archived live-book days to replay")
    parser.add_argument("--archive-root", type=Path, default=_REPO_ROOT / "tests" / "live_book" / "output")
    parser.add_argument("--limit", type=int, default=0, help="first N cases per suite (0 = all)")
    parser.add_argument("--max-usd", type=float, default=5.0, help="hard cap on what this run may spend")
    parser.add_argument("--env-file", type=Path, default=_REPO_ROOT / ".env", help="where OPENAI_API_KEY lives")
    parser.add_argument("--dry-run", action="store_true", help="count planned calls and cost; call no API")
    args = parser.parse_args(argv)
    args.days = [d for d in args.days.split(",") if d]
    models = [m for m in args.models.split(",") if m]
    suites = [s for s in args.suites.split(",") if s]
    unknown = [m for m in models if m not in PRICES] + [s for s in suites if s not in SUITES]
    if unknown:
        parser.error(f"unknown model or suite: {', '.join(unknown)}")

    import os

    from dotenv import load_dotenv

    load_dotenv(args.env_file)
    if not args.dry_run and not os.getenv("OPENAI_API_KEY"):
        parser.error(f"OPENAI_API_KEY is not set (looked in the environment and {args.env_file})")

    from explain_my_option.pipeline.config import PipelineConfig

    builders = {
        "redteam": redteam_cases,
        "historical": historical_cases,
        "archive": lambda: archive_cases(args.archive_root, args.days),
    }
    cases, counts = [], {}
    for suite in suites:
        built = builders[suite]()
        built = built[: args.limit] if args.limit else built
        counts[suite] = len(built)
        cases.extend((suite, case_id, run) for case_id, run in built)

    ledger = Ledger(args.max_usd)
    config = PipelineConfig(require_openai=not args.dry_run)
    results = run_study(cases, models, ledger, config, dry_run=args.dry_run)
    if args.dry_run:
        print_plan(ledger, models, counts)
        return 0
    write_outputs(results, models, ledger, args)
    print(f"spent this run: ${ledger.spent:.4f} of ${args.max_usd:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
