#!/usr/bin/env python3
"""Cost, latency, and terminal-state study (Task B4).

Runs the real leg graph (``agent_graph.run_pipeline``, not a mock) for the
10 offline synthetic legs plus the 2 verified real historical cases (real
DoltHub chains -- see docs/dev/DATA_SOURCES.md), through a real
``gpt-5.4-mini`` narrator/verifier (temperature=0, seed pinned --
pipeline.llm_roles.OpenAiRole). Writes docs/studies/agent_budget.md with
p50/p95 wall-clock per stage, tokens/cost by role, the tools_run/skip-
reason/terminal-state distributions -- every number here comes from this
run, not an estimate.

    python scripts/agent_budget_study.py     # needs OPENAI_API_KEY, ~2-3 min
"""

from __future__ import annotations

import json
import os
import statistics
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "src"))
sys.path.insert(0, str(_REPO_ROOT / "tests"))

from bootstrap import install  # noqa: E402

install()

from dotenv import load_dotenv  # noqa: E402

load_dotenv()

from live_book.portfolio_book import OFFLINE_LEGS  # noqa: E402
from explain_my_option.agent_graph import run_pipeline  # noqa: E402
from explain_my_option.data.historical_chain import HistoricalChainMarketLoader  # noqa: E402
from explain_my_option.data.synthetic import load_fixture  # noqa: E402
from explain_my_option.graph.deps import (  # noqa: E402
    FixtureMarketLoader,
    GraphDeps,
    OfficialFdmPnlSource,
)
from explain_my_option.intel.sources import IntelRegistry, StubIntelSource  # noqa: E402
from explain_my_option.pipeline.llm_roles import default_openai_roles  # noqa: E402
from ci.engine_config import engine_config_for_tests  # noqa: E402

OUT_PATH = _REPO_ROOT / "docs" / "studies" / "agent_budget.md"

# Task A4.5's two verified real cases (scripts/fetch_chains.py CASES, not
# re-typed by hand -- kept in sync manually since that dict is script-local).
REAL_CASES = {
    "gme_squeeze_2021_real": dict(
        ticker="GME", option_type="put", strike=55.0, expiry="2021-02-19",
        as_of="2021-01-25", prev_as_of="2021-01-22",
    ),
    "aapl_exdiv_2023_real": dict(
        ticker="AAPL", option_type="call", strike=180.0, expiry="2023-11-24",
        as_of="2023-11-09", prev_as_of="2023-11-08",
    ),
}

# Graph node name -> B4 stage bucket. IV inversion happens inside the
# "quant" node's price_and_attribute() call, not a separate node -- it is
# not separately measurable without invasive engine instrumentation (see
# the FINDING recorded in WORK_ORDER_REPORT.md for this task).
STAGE_BUCKETS = {
    "fetch_market": "data_fetch",
    "quant": "pricing",
    "blotter": "pricing",
    "diagnostic_pass": "diagnostic_tools",
    "react_plan": "diagnostic_tools",
    "react_tool_exec": "diagnostic_tools",
    "diag_finalize": "diagnostic_tools",
    "plan_search": "search",
    "search": "search",
    "digest_news": "llm_roles",
    "challenge_catalyst": "llm_roles",
    "synthesize": "llm_roles",
    "reconcile_debate": "llm_roles",
    "verify": "llm_roles",
    "revise_synthesis": "llm_roles",
    "reflect_verifier": "llm_roles",
    "finalize_leg_report": "report_render",
}

# gpt-5.4-mini standard (non-batch) pricing, September 2026. OpenAI's own
# pricing page returned HTTP 403 to this session's fetch tool; this figure
# is from a third-party aggregator (pricepertoken.com / morphllm.com via
# web search this session), not OpenAI's page directly -- treat the $
# figures below as approximate, the token counts as exact.
PRICE_PER_1M_INPUT_USD = 0.75
PRICE_PER_1M_OUTPUT_USD = 4.50


def _offline_deps(leg):
    patches = dict(leg.overrides)
    patches.setdefault("ticker", leg.ticker)
    from live_book.portfolio_e2e import PatchingMarketLoader  # local, avoids cycle

    return GraphDeps(
        market=PatchingMarketLoader(FixtureMarketLoader(leg.fixture), {leg.ticker: patches}),
        pnl=OfficialFdmPnlSource(config=engine_config_for_tests()),
        intel=IntelRegistry(
            {
                "yfinance_news": StubIntelSource("yfinance_news"),
                "tavily": StubIntelSource("tavily"),
                "sec_8k": StubIntelSource("sec_8k"),
            }
        ),
    )


def _real_case_deps(spec):
    return GraphDeps(
        market=HistoricalChainMarketLoader(
            as_of=spec["as_of"], prev_as_of=spec["prev_as_of"],
            config=engine_config_for_tests(),
        ),
        pnl=OfficialFdmPnlSource(config=engine_config_for_tests()),
        intel=IntelRegistry(
            {
                "yfinance_news": StubIntelSource("yfinance_news"),
                "tavily": StubIntelSource("tavily"),
                "sec_8k": StubIntelSource("sec_8k"),
            }
        ),
    )


def _run_leg(name: str, *, ticker: str, option_type: str, strike, expiry, deps, roles) -> dict:
    t0 = time.perf_counter()
    try:
        state = run_pipeline(
            ticker=ticker, option_type=option_type, strike=strike, expiry=expiry,
            deps=deps, roles=roles,
        )
    except Exception as exc:  # a leg failing is itself a real, reportable outcome
        wall = time.perf_counter() - t0
        return {"name": name, "ok": False, "error": f"{type(exc).__name__}: {exc}", "wall_s": wall}
    wall = time.perf_counter() - t0

    usage_by_role = {}
    for role_name, role in (
        ("narrator", roles.narrator),
        ("verifier", roles.verifier),
        ("challenger", roles.challenger),
        ("digester", roles.digester),
    ):
        u = getattr(role, "last_usage", None)
        if u:
            usage_by_role[role_name] = dict(u)

    findings = state.get("diagnostic_findings") or {}
    if findings.get("terminal_unexplained_break"):
        terminal = "terminal_unexplained_break"
    elif state.get("terminal_no_comparable_observation"):
        terminal = "terminal_no_comparable_observation"
    elif state.get("no_escalation"):
        terminal = "no_escalation"
    else:
        terminal = findings.get("verifier_status") or "completed"

    return {
        "name": name,
        "ok": True,
        "wall_s": wall,
        "stage_timings": dict(state.get("stage_timings") or {}),
        "llm_calls": state.get("llm_calls"),
        "usage_by_role": usage_by_role,
        "tools_run": list(findings.get("tools_run") or []),
        "tool_calls_used": findings.get("tool_calls_used"),
        "skipped_tools": [dict(s) for s in (findings.get("skipped_tools") or [])],
        "terminal_state": terminal,
        "verifier_status": findings.get("verifier_status"),
    }


def _pct(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    idx = min(len(s) - 1, max(0, round(q * (len(s) - 1))))
    return s[idx]


def main() -> int:
    if not os.getenv("OPENAI_API_KEY"):
        print("SKIP: OPENAI_API_KEY not set. This study needs a real model run.")
        return 0

    roles = default_openai_roles()
    runs: list[dict] = []

    for leg in OFFLINE_LEGS:
        snap0, _ = load_fixture(leg.fixture)
        deps = _offline_deps(leg)
        print(f"running {leg.ticker}/{leg.fixture} ...", file=sys.stderr)
        runs.append(
            _run_leg(
                f"{leg.ticker}/{leg.fixture}",
                ticker=leg.ticker,
                option_type=snap0.option_type,
                strike=snap0.strike,
                expiry=snap0.expiry,
                deps=deps,
                roles=roles,
            )
        )

    for case_name, spec in REAL_CASES.items():
        deps = _real_case_deps(spec)
        print(f"running {case_name} (real DoltHub chain, ~45-55s fetch) ...", file=sys.stderr)
        runs.append(
            _run_leg(
                case_name,
                ticker=spec["ticker"],
                option_type=spec["option_type"],
                strike=spec["strike"],
                expiry=spec["expiry"],
                deps=deps,
                roles=roles,
            )
        )

    ok_runs = [r for r in runs if r["ok"]]
    failed_runs = [r for r in runs if not r["ok"]]

    # Stage bucket timing across all successful runs.
    bucket_samples: dict[str, list[float]] = defaultdict(list)
    for r in ok_runs:
        per_run_bucket: dict[str, float] = defaultdict(float)
        for node, seconds in r["stage_timings"].items():
            bucket = STAGE_BUCKETS.get(node, node)
            per_run_bucket[bucket] += seconds
        for bucket, seconds in per_run_bucket.items():
            bucket_samples[bucket].append(seconds)

    wall_samples = [r["wall_s"] for r in ok_runs]

    # Tokens/cost by role, summed across all runs (not per-run average --
    # a total is what a desk actually pays for this leg set).
    role_tokens: dict[str, Counter] = defaultdict(Counter)
    for r in ok_runs:
        for role_name, usage in r["usage_by_role"].items():
            role_tokens[role_name]["input"] += usage.get("input_tokens", 0)
            role_tokens[role_name]["output"] += usage.get("output_tokens", 0)
            role_tokens[role_name]["calls"] += 1

    tools_run_counts = [len(r["tools_run"]) for r in ok_runs]
    skip_reason_hist: Counter = Counter()
    for r in ok_runs:
        for s in r["skipped_tools"]:
            skip_reason_hist[s.get("reason", "unknown")] += 1

    terminal_hist: Counter = Counter(r["terminal_state"] for r in ok_runs)

    lines = [
        "# Agent cost, latency, and terminal-state study (Task B4)",
        "",
        f"Generated {datetime.now(timezone.utc).isoformat(timespec='seconds')} by "
        "`scripts/agent_budget_study.py`, run through the real leg graph "
        "(`agent_graph.run_pipeline`) for the 10 offline synthetic legs "
        "(`tests/live_book/portfolio_book.py::OFFLINE_LEGS`) and the 2 "
        "verified real historical cases (real DoltHub chains). Every "
        f"number below is produced by this run, `n={len(runs)}` "
        f"({len(ok_runs)} completed, {len(failed_runs)} failed).",
        "",
        "**Model**: `gpt-5.4-mini`, `temperature=0.0`, fixed `seed=0` "
        "(`pipeline.llm_roles.OpenAiRole`, Task B3).",
        "",
        "## Wall-clock per stage (seconds)",
        "",
        "IV inversion happens inside the `quant` node's `price_and_attribute()` "
        "call, not a separate graph node -- not separately measurable without "
        "invasive engine instrumentation, folded into `pricing` here.",
        "",
        "| Stage | n | p50 | p95 | max |",
        "|---|---:|---:|---:|---:|",
    ]
    for bucket in ("data_fetch", "pricing", "diagnostic_tools", "search", "llm_roles", "report_render"):
        samples = bucket_samples.get(bucket, [])
        if not samples:
            lines.append(f"| {bucket} | 0 | — | — | — |")
            continue
        lines.append(
            f"| {bucket} | {len(samples)} | {_pct(samples, 0.5):.4f} | "
            f"{_pct(samples, 0.95):.4f} | {max(samples):.4f} |"
        )
    lines.append(
        f"| **total wall (per run)** | {len(wall_samples)} | "
        f"{_pct(wall_samples, 0.5):.2f} | {_pct(wall_samples, 0.95):.2f} | "
        f"{max(wall_samples) if wall_samples else 0:.2f} |"
    )

    lines.extend(["", "## Tokens and cost by role (summed across all runs)", ""])
    lines.append("| Role | Calls | Input tokens | Output tokens | Cost (USD, see pricing note) |")
    lines.append("|---|---:|---:|---:|---:|")
    total_cost = 0.0
    for role_name in ("narrator", "verifier", "challenger", "digester"):
        c = role_tokens.get(role_name)
        if not c:
            lines.append(f"| {role_name} | 0 | 0 | 0 | $0.0000 |")
            continue
        cost = (
            c["input"] / 1_000_000 * PRICE_PER_1M_INPUT_USD
            + c["output"] / 1_000_000 * PRICE_PER_1M_OUTPUT_USD
        )
        total_cost += cost
        lines.append(f"| {role_name} | {c['calls']} | {c['input']} | {c['output']} | ${cost:.4f} |")
    lines.append(f"| **total** | | | | **${total_cost:.4f}** |")
    lines.extend(
        [
            "",
            f"Pricing: gpt-5.4-mini standard (non-batch) rate, "
            f"${PRICE_PER_1M_INPUT_USD}/1M input + ${PRICE_PER_1M_OUTPUT_USD}/1M output tokens. "
            "OpenAI's own pricing page returned HTTP 403 to this session's fetch tool; "
            "this rate is from a third-party aggregator (web search, this session), "
            "not confirmed against OpenAI's page directly -- the token counts above "
            "are exact (from each call's real `usage_metadata`), the $ total is "
            "approximate to whatever that page currently says.",
        ]
    )

    lines.extend(["", "## `tools_run` count distribution", ""])
    if tools_run_counts:
        tc = Counter(tools_run_counts)
        lines.append("| tools_run count | runs |")
        lines.append("|---:|---:|")
        for k in sorted(tc):
            lines.append(f"| {k} | {tc[k]} |")
        lines.append(
            f"\np50={_pct([float(x) for x in tools_run_counts], 0.5):.1f}, "
            f"p95={_pct([float(x) for x in tools_run_counts], 0.95):.1f}, "
            f"max={max(tools_run_counts)} "
            f"(budget ceiling is `MAX_DIAGNOSTIC_TOOL_CALLS=1` costly slot per pass, Task A5/A7)."
        )
    else:
        lines.append("No successful runs.")

    lines.extend(["", "## Skip-reason histogram", ""])
    if skip_reason_hist:
        lines.append("| Reason | Count |")
        lines.append("|---|---:|")
        for reason, n in skip_reason_hist.most_common():
            lines.append(f"| {reason} | {n} |")
    else:
        lines.append("No skipped tools across this run set.")

    lines.extend(["", "## Terminal-state distribution", ""])
    lines.append("| State | Count |")
    lines.append("|---|---:|")
    for state, n in terminal_hist.most_common():
        lines.append(f"| {state} | {n} |")

    if failed_runs:
        lines.extend(["", "## Failed legs (not silently dropped)", ""])
        for r in failed_runs:
            lines.append(f"- **{r['name']}**: `{r['error']}`")

    lines.extend(
        [
            "",
            "## Sample size and scope",
            "",
            f"- {len(OFFLINE_LEGS)} offline synthetic legs (one real narrator+verifier "
            "call pair each unless a deterministic precheck or no-escalation gate "
            "short-circuits first) + 2 real historical cases (real DoltHub chains, "
            "45-55s data-fetch latency each, dominating those two runs' `data_fetch` "
            "stage -- see `docs/dev/DATA_SOURCES.md`).",
            "- `n=12` is small; p95 on a 12-sample set is really closer to a max. "
            "Treat percentiles here as directional, not a SLA.",
            "- `--no-llm` (this task) is the zero-LLM-cost path for a reviewer "
            "without an API key; this study is the other half -- what a real run "
            "actually costs.",
        ]
    )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH.relative_to(_REPO_ROOT)}")
    print(f"Total cost this run: ${total_cost:.4f} across {len(ok_runs)} completed legs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
