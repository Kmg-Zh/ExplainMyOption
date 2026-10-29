#!/usr/bin/env python3
"""Does the terminal-break playbook record reach the Headline verdict?

Replays every archived live-run leg whose diagnostic pass ended in a terminal
break, twice on the same code: with the playbook off (``playbook=()``) and on.
Only the narrator is a real model. The digester and the catalyst critic return
what they returned on the archived day, and the verifier is off, so the two
arms differ by the record alone and the verdict scored is the narrator's (after
the deterministic reconcile step), as it would reach the Headline.

API responses are cached with ``scripts/compare_models.py``'s cache, so a rerun
pays nothing for calls already made.

    python evals/live_book/playbook_replay.py --dry-run
    python evals/live_book/playbook_replay.py --archive-root ../tests/live_book/output --max-usd 2
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(_REPO_ROOT / "src"), str(_REPO_ROOT / "evals")]

OUT = _REPO_ROOT / "evals" / "output" / "playbook_replay"
DOC = _REPO_ROOT / "docs" / "studies" / "playbook_replay.md"

# The verdict says the attribution does not explain the move, or that a person
# must look, in any of these words.
_FLAGS_BREAK = re.compile(
    r"unexplained|not explain|n't explain|unattributed|not attributed|cannot be attributed"
    r"|human review|not reliable|unreliable|needs review|manual review",
    re.IGNORECASE,
)


def _compare_models():
    spec = importlib.util.spec_from_file_location("compare_models", _REPO_ROOT / "scripts" / "compare_models.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # its dataclasses look themselves up here
    spec.loader.exec_module(module)
    return module


def terminal_break_legs(root: Path) -> list[Path]:
    """Diagnostic-pass terminal breaks in each day's live run (replays excluded)."""
    legs = []
    for day in sorted(p for p in root.iterdir() if p.is_dir() and p.name[:2] == "20"):
        lives = sorted(p for p in day.iterdir() if p.is_dir() and p.name.startswith("live"))
        if not lives:
            continue
        for path in sorted((lives[-1] / "legs").glob("*.json")):
            findings = json.loads(path.read_text(encoding="utf-8")).get("diagnostic_findings") or {}
            if findings.get("terminal_unexplained_break") and findings.get("terminal_cause") != "verifier_hard_fail":
                legs.append(path)
    return legs


def replay(payload: dict, narrator, *, playbook, require_openai: bool = True) -> dict:
    from live_book.replay_archives import (
        FrozenMarketLoader,
        FrozenNewsSource,
        _news_from_rows,
        _snapshot_from_dict,
        _surface_from_dict,
    )

    from explain_my_option.agent_graph import run_pipeline
    from explain_my_option.graph.deps import GraphDeps, OfficialFdmPnlSource
    from explain_my_option.intel.planner import CueQueryPlanner
    from explain_my_option.intel.sources import IntelRegistry, StubIntelSource
    from explain_my_option.pipeline.config import PipelineConfig
    from explain_my_option.pipeline.llm_roles import LlmRoleRegistry
    from explain_my_option.pricing.types import LoadedData
    from explain_my_option.testing import NoLlm, ScriptedRole

    archived = payload.get("diagnostic_findings") or {}
    snap = _snapshot_from_dict(payload["snapshot"])
    news = _news_from_rows(payload.get("news") or [])
    deps = GraphDeps(
        market=FrozenMarketLoader(LoadedData(snapshot=snap, surface=_surface_from_dict(payload.get("surface")))),
        pnl=OfficialFdmPnlSource(),
        planner=CueQueryPlanner(),
        intel=IntelRegistry(
            {"yfinance_news": FrozenNewsSource(news), "tavily": StubIntelSource("tavily"), "sec_8k": StubIntelSource("sec_8k")}
        ),
        playbook=playbook,
    )
    roles = LlmRoleRegistry(
        narrator=narrator,
        verifier=NoLlm(),
        digester=ScriptedRole(archived["intel_digest"]) if "intel_digest" in archived else NoLlm(),
        challenger=ScriptedRole(archived["catalyst_challenge"]) if archived.get("catalyst_challenge") else NoLlm(),
    )
    state = run_pipeline(
        ticker=snap.ticker,
        option_type=snap.option_type,
        strike=snap.strike,
        expiry=snap.expiry,
        quantity=snap.quantity,
        multiplier=snap.multiplier,
        deps=deps,
        config=PipelineConfig(verify=False, require_openai=require_openai),
        roles=roles,
    )
    findings = state.get("diagnostic_findings") or {}
    synthesis = state.get("diagnostic_synthesis") or {}
    return {
        "terminal_break": bool(findings.get("terminal_unexplained_break")),
        "fallback": str(synthesis.get("confidence_rationale", "")).startswith("LLM synthesis failed"),
        "verdict": synthesis.get("verdict", ""),
        "confidence_rationale": synthesis.get("confidence_rationale", ""),
        "verdict_flags_break": bool(_FLAGS_BREAK.search(synthesis.get("verdict", ""))),
        "rationale_flags_break": bool(_FLAGS_BREAK.search(synthesis.get("confidence_rationale", ""))),
        "playbook_records": [r["id"] for r in findings.get("playbook_records") or []],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--archive-root", type=Path, default=_REPO_ROOT / "evals" / "live_book" / "output")
    parser.add_argument("--model", default="gpt-5.4-mini")
    parser.add_argument("--max-usd", type=float, default=2.0, help="hard cap on what this run may spend")
    parser.add_argument("--env-file", type=Path, default=_REPO_ROOT / ".env", help="where OPENAI_API_KEY lives")
    parser.add_argument("--dry-run", action="store_true", help="count planned calls and cost; call no API")
    args = parser.parse_args(argv)

    from dotenv import load_dotenv

    load_dotenv(args.env_file)
    if not args.dry_run and not os.getenv("OPENAI_API_KEY"):
        parser.error(f"OPENAI_API_KEY is not set (looked in the environment and {args.env_file})")

    from explain_my_option.graph.playbook import DEFAULT_PLAYBOOK
    from explain_my_option.graph.prompts import PROMPT_VERSION

    cm = _compare_models()
    ledger = cm.Ledger(args.max_usd)
    narrator = cm.StudyRole(args.model, ledger, dry_run=args.dry_run)
    legs = terminal_break_legs(args.archive_root)
    rows = []
    for path in legs:
        payload = json.loads(path.read_text(encoding="utf-8"))
        row = {"leg": str(path.relative_to(args.archive_root))}
        try:
            for arm, playbook in (("off", ()), ("on", DEFAULT_PLAYBOOK)):
                row[arm] = replay(payload, narrator, playbook=playbook, require_openai=not args.dry_run)
        except cm.BudgetExhausted as exc:
            print(f"stopped: {exc}")
            break
        rows.append(row)
        if not args.dry_run:
            print(row["leg"], {arm: row[arm]["verdict_flags_break"] for arm in ("off", "on")})

    spent = sum(c.cost_usd for c in ledger.calls if c.source != "cache")
    if args.dry_run:
        still = sum(r["off"]["terminal_break"] and r["on"]["terminal_break"] for r in rows)
        print(f"{len(legs)} legs ({still} still terminal breaks), {len(ledger.calls)} narrator calls planned, about ${spent:.2f} at most")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    DOC.write_text(_markdown(rows, args, PROMPT_VERSION, ledger), encoding="utf-8")
    print(f"spent this run: ${ledger.spent:.4f} of ${args.max_usd:.2f}; wrote {DOC.relative_to(_REPO_ROOT)}")
    return 0


def _markdown(rows: list[dict], args, prompt_version: str, ledger) -> str:
    scored = [r for r in rows if r["off"]["terminal_break"] and r["on"]["terminal_break"]]

    def count(arm: str, key: str) -> str:
        n = sum(bool(r[arm][key]) for r in scored)
        return f"{n}/{len(scored)}"

    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    paid = sum(c.cost_usd for c in ledger.calls if c.source == "api")
    lines = [
        "# Playbook replay: the terminal-break record",
        "",
        f"Generated {generated} by `evals/live_book/playbook_replay.py`, prompt `{prompt_version}`, "
        f"narrator `{args.model}`, cost ${paid:.2f}.",
        "",
        f"Every archived live-run leg whose diagnostic pass ended in a terminal break ({len(rows)} legs) "
        "was replayed twice on the same code: playbook off and on. Only the narrator is a real model; "
        "the digester and the critic return their archived answers and the verifier is off, so the arms "
        "differ by the record alone. "
        f"{len(scored)} legs are still terminal breaks under the current code and are scored.",
        "",
        "A verdict \"flags the break\" if it says, in any wording, that the move is unexplained, "
        "or that it needs human review or is not reliable.",
        "",
        "| | Playbook off | Playbook on |",
        "|---|---|---|",
        f"| Verdict flags the break | {count('off', 'verdict_flags_break')} | {count('on', 'verdict_flags_break')} |",
        f"| Confidence rationale flags the break | {count('off', 'rationale_flags_break')} | {count('on', 'rationale_flags_break')} |",
        f"| Narrator fell back to the rule-based summary | {count('off', 'fallback')} | {count('on', 'fallback')} |",
        "",
        "## Verdicts, leg by leg",
        "",
    ]
    for r in scored:
        lines.extend(
            [
                f"### {r['leg']}",
                "",
                f"- **Off**{' (flags it)' if r['off']['verdict_flags_break'] else ''}: {r['off']['verdict']}",
                f"- **On**{' (flags it)' if r['on']['verdict_flags_break'] else ''}: {r['on']['verdict']}",
                "",
            ]
        )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
