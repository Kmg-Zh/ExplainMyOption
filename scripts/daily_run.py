#!/usr/bin/env python3
"""The daily live-book run log.

Runs every leg of docs/runlog/book.json through the real graph, writes
docs/runlog/YYYY-MM-DD/{report.md,audit.json} and appends one row to
docs/runlog/metrics.jsonl.

Only today's entry is ever written: no backfill, no simulated days. A gap is
honest; a fabricated entry would destroy the log's value. The roll-up report
is the deterministic portfolio render, not an extra LLM call; legs that are
quiet days make no LLM call at all (legs_silent).

    python scripts/daily_run.py            # today, needs OPENAI_API_KEY
    python scripts/daily_run.py --dry-run  # price and diagnose, write nothing
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from collections import Counter
from datetime import date
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "src"))
sys.path.insert(0, str(_REPO_ROOT / "tests"))

from bootstrap import install  # noqa: E402

install()

from dotenv import load_dotenv  # noqa: E402

load_dotenv()

from live_book.portfolio_book import load_pinned_book  # noqa: E402
from explain_my_option.agent_graph import run_pipeline  # noqa: E402
from explain_my_option.data.cache import upsert_snapshot  # noqa: E402
from explain_my_option.graph.deps import default_deps  # noqa: E402
from explain_my_option.graph.prompts import PROMPT_VERSION  # noqa: E402
from explain_my_option.pipeline.llm_roles import default_openai_roles  # noqa: E402
from explain_my_option.report.facts import PositionBundle  # noqa: E402
from explain_my_option.report.reconciliation import build_reconciliation_facts  # noqa: E402
from explain_my_option.report.schema import DiagnosticSynthesis  # noqa: E402
from explain_my_option.report.template import render_portfolio_report  # noqa: E402

BOOK_PATH = _REPO_ROOT / "docs" / "runlog" / "book.json"
RUNLOG_DIR = _REPO_ROOT / "docs" / "runlog"
METRICS_PATH = RUNLOG_DIR / "metrics.jsonl"
# A leg whose |total PnL| is below this has no meaningful percent denominator
# (the residual / total ratio explodes); it is excluded from the median and
# counted in `residual_pct_excluded_legs`.
MIN_PCT_DENOMINATOR_USD = 0.005

# gpt-5.4-mini list price, as in docs/studies/agent_budget.md. Token counts
# are exact; the dollar figure is only as current as that price.
PRICE_PER_1M_INPUT_USD = 0.75
PRICE_PER_1M_OUTPUT_USD = 4.50


def _skew_proxy(bundles_by_id: dict[str, PositionBundle]) -> dict:
    """Skew proxy from the risk-reversal pair: two quoted points, no fitting."""
    put = bundles_by_id.get("spy_reversal_put")
    call = bundles_by_id.get("spy_reversal_call")
    if put is None or call is None:
        return {}
    iv_put_now = put.snapshot.iv_now
    iv_call_now = call.snapshot.iv_now
    iv_put_prev = put.snapshot.iv_prev
    iv_call_prev = call.snapshot.iv_prev
    skew_now = iv_put_now - iv_call_now
    level_now = 0.5 * (iv_put_now + iv_call_now)
    skew_prev = iv_put_prev - iv_call_prev
    level_prev = 0.5 * (iv_put_prev + iv_call_prev)
    return {
        "SPY": {
            "skew_proxy": skew_now,
            "level_proxy": level_now,
            "d_skew": skew_now - skew_prev,
            "d_level": level_now - level_prev,
            "put_strike": put.snapshot.strike,
            "call_strike": call.snapshot.strike,
            "put_delta": put.pricing.greeks_now.delta,
            "call_delta": call.pricing.greeks_now.delta,
            "note": (
                "Nearest-listed-strike approximation of 25-delta, not a fit or a "
                "surface -- actual deltas recorded above, not assumed."
            ),
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Price and diagnose every leg but do not write report.md/metrics.jsonl.",
    )
    args = parser.parse_args()

    today = date.today().isoformat()
    run_id = f"{today}-{int(time.time())}"
    t_start = time.perf_counter()

    have_key = bool(os.getenv("OPENAI_API_KEY"))
    roles = default_openai_roles() if have_key else None

    baseline_as_of, legs = load_pinned_book(BOOK_PATH)
    deps = default_deps()

    bundles_by_id: dict[str, PositionBundle] = {}
    syntheses: list[DiagnosticSynthesis] = []
    leg_findings: list[dict] = []
    errors: list[dict] = []
    legs_narrated = 0
    legs_silent = 0
    llm_calls_total = 0
    tools_run_all: list[str] = []
    skipped_tools_all: list[dict] = []
    quote_tier_counts: Counter = Counter()
    terminal_states_by_leg: dict[str, str] = {}
    taylor_regimes: list[str] = []
    residual_method_pcts: list[float] = []
    residual_pct_excluded_legs = 0
    residual_model_pcts: list[float] = []
    escalation_bases: list[str] = []
    verifier_verdicts: list[str] = []
    verifier_downgraded = 0
    audit_by_leg: dict[str, dict] = {}
    injection_observed_any = False
    usage_by_role: dict[str, Counter] = {}

    for leg in legs:
        leg_id = leg.leg_id or leg.ticker.lower()
        label = f"{leg.ticker} {leg.strike:g}{leg.option_type[0].upper()} {leg.expiry}"
        print(f"[{leg_id}] {label} ...", file=sys.stderr)
        try:
            state = run_pipeline(
                ticker=leg.ticker, option_type=leg.option_type,
                strike=leg.strike, expiry=leg.expiry,
                quantity=leg.quantity, multiplier=leg.multiplier,
                deps=deps, roles=roles,
            )
        except Exception as exc:
            print(f"  FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
            errors.append({"leg_id": leg_id, "ticker": leg.ticker, "error": f"{type(exc).__name__}: {exc}"})
            continue

        bundle = PositionBundle(
            snapshot=state["snapshot"], pricing=state["pricing"],
            news=state.get("news") or [], plan=state.get("search_plan"),
        )
        bundles_by_id[leg_id] = bundle
        if not args.dry_run:
            # Cache today's snapshot so tomorrow's run finds a real T-1 mark
            # instead of the HV20 proxy (t-1 lookup reads only the snapshot).
            if not upsert_snapshot(state["snapshot"], None):
                print(f"  not cached as t-1: {leg_id} has a sentinel IV "
                      f"({state['snapshot'].iv_now:g})", file=sys.stderr)
        synthesis = DiagnosticSynthesis.model_validate(state["diagnostic_synthesis"])
        syntheses.append(synthesis)
        findings = state.get("diagnostic_findings") or {}
        leg_findings.append(findings)

        n_calls = state.get("llm_calls") or 0
        llm_calls_total += n_calls
        if n_calls > 0:
            legs_narrated += 1
        else:
            legs_silent += 1

        tools_run_all.extend(findings.get("tools_run") or [])
        skipped_tools_all.extend(findings.get("skipped_tools") or [])
        # The same reconciliation facts the report prints (quote tier, basis).
        rec = build_reconciliation_facts(state["snapshot"], state["pricing"])
        quote_tier_counts[rec.quote_tier or "unknown"] += 1

        # The diagnostic pass flags a residual left unexplained after its tool
        # budget, but the leg still narrates and verifies; only a code-confirmed
        # verifier FAIL ends the leg in the terminal state.
        if findings.get("terminal_unexplained_break") and findings.get("verifier_status") == "FAIL":
            terminal_states_by_leg[leg_id] = "terminal_unexplained_break"
        elif state.get("terminal_no_comparable_observation"):
            terminal_states_by_leg[leg_id] = "terminal_no_comparable_observation"
        elif state.get("no_escalation"):
            terminal_states_by_leg[leg_id] = "no_escalation"
        else:
            terminal_states_by_leg[leg_id] = findings.get("verifier_status") or "completed"

        if findings.get("taylor_regime"):
            taylor_regimes.append(findings["taylor_regime"])
        rec_pnl = state["pricing"].pnl
        total = abs(rec_pnl.total_pnl)
        if total >= MIN_PCT_DENOMINATOR_USD:
            residual_method_pcts.append(100.0 * abs(rec_pnl.residual_pnl) / total)
        else:
            residual_pct_excluded_legs += 1
        escalation_bases.append(rec.escalation_basis)
        if findings.get("verifier_status"):
            verifier_verdicts.append(findings["verifier_status"])
        # A hard LLM FAIL that code could not confirm is downgraded to PARTIAL;
        # count it so a downgrade is never silently an "ordinary" PARTIAL.
        trace = (findings.get("verifier_audit") or {}).get("trace") or []
        if any(row.get("llm_verdict") == "FAIL" for row in trace):
            verifier_downgraded += 1
        audit_by_leg[leg_id] = {
            "terminal_state": terminal_states_by_leg[leg_id],
            "terminal_cause": findings.get("terminal_cause"),
            "final_synthesis": synthesis.model_dump(),
            "verifier_audit": findings.get("verifier_audit") or {},
            "verifier_trace": trace,
        }
        if synthesis.injection_observed:
            injection_observed_any = True

        if roles is not None:
            for role_name, role in (
                ("narrator", roles.narrator), ("verifier", roles.verifier),
                ("challenger", roles.challenger), ("digester", roles.digester),
            ):
                u = getattr(role, "last_usage", None)
                if u:
                    c = usage_by_role.setdefault(role_name, Counter())
                    c["input"] += u.get("input_tokens", 0)
                    c["output"] += u.get("output_tokens", 0)

    wall_clock_s = time.perf_counter() - t_start
    skew = _skew_proxy(bundles_by_id)

    prompt_tokens = sum(c["input"] for c in usage_by_role.values())
    completion_tokens = sum(c["output"] for c in usage_by_role.values())
    est_cost_usd = (
        prompt_tokens / 1_000_000 * PRICE_PER_1M_INPUT_USD
        + completion_tokens / 1_000_000 * PRICE_PER_1M_OUTPUT_USD
    )

    vol_input_quality = ",".join(sorted(quote_tier_counts.keys()))
    escalation_basis = Counter(escalation_bases).most_common(1)[0][0] if escalation_bases else ""
    taylor_regime = Counter(taylor_regimes).most_common(1)[0][0] if taylor_regimes else ""
    verifier_verdict = Counter(verifier_verdicts).most_common(1)[0][0] if verifier_verdicts else ""

    report = render_portfolio_report(
        list(bundles_by_id.values()), syntheses, leg_findings=leg_findings,
    )
    skew_lines = ""
    if skew:
        s = skew["SPY"]
        skew_lines = (
            f"\n\n## Skew proxy (SPY risk reversal)\n\n"
            f"* skew_proxy(t) = {s['skew_proxy']:+.4f} | level_proxy(t) = {s['level_proxy']:.4f}\n"
            f"* Δskew = {s['d_skew']:+.4f} | Δlevel = {s['d_level']:+.4f}\n"
            f"* Put {s['put_strike']:g} delta={s['put_delta']:.4f} | "
            f"Call {s['call_strike']:g} delta={s['call_delta']:.4f}\n"
            f"* {s['note']}\n"
        )
    any_real_t1 = any(
        b.snapshot.iv_prev_source == "chain_t1" for b in bundles_by_id.values()
    )
    day1_note = ""
    if not any_real_t1:
        day1_note = (
            "\n\n**No leg in this run has a cached t-1 snapshot yet** "
            "(`iv_prev_source` is `hv20_proxy` or `copied` for every leg below) "
            "-- this is the book's opening day, or the first run since a leg "
            "changed. Every `ΔP`/residual/terminal-state figure below is "
            "comparing today's quote against a statistically-derived proxy for "
            "yesterday, not a real prior trading day, and should be read as "
            "noisy. This run still caches each leg's snapshot "
            "(`data.cache.upsert_snapshot`), so tomorrow's run compares "
            "against today for real.\n"
        )
    report_full = (
        f"# Live book run — {today}\n\n"
        f"Run `{run_id}`. {len(bundles_by_id)}/{len(legs)} legs completed, "
        f"{len(errors)} failed. `legs_narrated={legs_narrated}` `legs_silent={legs_silent}` "
        f"`llm_calls={llm_calls_total}`."
        + day1_note
        + "\n\n" + report + skew_lines
    )
    if errors:
        report_full += "\n\n## Errors\n\n" + "\n".join(
            f"- **{e['leg_id']}** ({e['ticker']}): {e['error']}" for e in errors
        )

    metrics_line = {
        "date": today,
        "run_id": run_id,
        # So a discontinuity in later behavior (e.g. a terminal_unexplained_break
        # rate that drops after a given date) is legible as "the prompt changed
        # here," not a silent gap -- bump PROMPT_VERSION whenever
        # VERIFIER_SYSTEM_PROMPT or the diagnose system prompt changes (see its
        # own comment in graph/prompts.py).
        "prompt_version": PROMPT_VERSION,
        "n_legs": len(legs),
        "wall_clock_s": round(wall_clock_s, 3),
        "llm_calls": llm_calls_total,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "est_cost_usd": round(est_cost_usd, 6),
        "legs_narrated": legs_narrated,
        "legs_silent": legs_silent,
        "tools_run": tools_run_all,
        "skipped_tools": skipped_tools_all,
        "vol_input_quality": vol_input_quality,
        "escalation_basis": escalation_basis,
        "residual_method_pct": round(statistics.median(residual_method_pcts), 4) if residual_method_pcts else 0.0,
        "residual_pct_excluded_legs": residual_pct_excluded_legs,
        "residual_model_pct": round(statistics.median(residual_model_pcts), 4) if residual_model_pcts else 0.0,
        "taylor_regime": taylor_regime,
        "verifier_verdict": verifier_verdict,
        "verifier_downgraded": verifier_downgraded,
        "terminal_states_by_leg": terminal_states_by_leg,
        "injection_observed": injection_observed_any,
        "quote_tier_counts": dict(quote_tier_counts),
        "skew_proxy_by_underlying": {k: {kk: vv for kk, vv in v.items() if kk != "note"} for k, v in skew.items()},
        "errors": errors,
    }

    print(json.dumps(metrics_line, indent=2))

    if not bundles_by_id:
        # Every leg failed: there is no run to record. Writing an all-errors
        # entry (and exiting 0, so the launchd wrapper commits it) would put
        # a failed day into the permanent log as if it were a real one.
        # A gap is honest (docs/runlog/README.md); a failed-run row isn't
        # information the summary can use. The errors are in the stderr log.
        print(
            f"\nAll {len(legs)} legs failed -- writing nothing and exiting 1.",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print("\n--dry-run: not writing report.md or metrics.jsonl", file=sys.stderr)
        return 0

    day_dir = RUNLOG_DIR / today
    day_dir.mkdir(parents=True, exist_ok=True)
    (day_dir / "report.md").write_text(report_full.rstrip() + "\n", encoding="utf-8")
    (day_dir / "audit.json").write_text(
        json.dumps(audit_by_leg, indent=2, default=str) + "\n", encoding="utf-8"
    )
    with METRICS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(metrics_line) + "\n")
    print(f"\nWrote docs/runlog/{today}/report.md and appended to docs/runlog/metrics.jsonl", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
