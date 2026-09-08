"""Replay archived live-book days through the current graph.

Uses frozen snapshots + archived news (no live Yahoo). LLM digest / challenge /
synthesize / verify still run. Writes under tests/live_book/output/<as_of>/replay_*.

    python tests/live_book/replay_archives.py
    python tests/live_book/replay_archives.py --days 2026-09-01,2026-09-02
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import fields
from pathlib import Path
from typing import Any

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from explain_my_option.agent_graph import run_pipeline
from explain_my_option.data_loader import LoadedData, NewsItem
from explain_my_option.graph.deps import GraphDeps, OfficialFdmPnlSource
from explain_my_option.intel.planner import CueQueryPlanner
from explain_my_option.intel.sources import IntelRegistry, StubIntelSource
from explain_my_option.intel.types import SearchQuery
from explain_my_option.pricing.types import DiscreteDividend, MarketSnapshot, VolSurfaceData
from explain_my_option.report.schema import DiagnosticSynthesis
from live_book.portfolio_e2e import _persist_run
from explain_my_option.report.facts import PositionBundle

ARCHIVE_ROOTS = (
    _TESTS_DIR / "output" / "live_book",
    _TESTS_DIR / "live_book" / "output",
)


class FrozenMarketLoader:
    def __init__(self, data: LoadedData) -> None:
        self.data = data

    def load(self, **kwargs) -> LoadedData:
        del kwargs
        return self.data


class FrozenNewsSource:
    source_id = "yfinance_news"

    def __init__(self, news: list[NewsItem]) -> None:
        self.news = list(news)

    def search(self, query: SearchQuery, *, ticker: str) -> list[NewsItem]:
        del query, ticker
        return list(self.news)


def _snapshot_from_dict(raw: dict[str, Any]) -> MarketSnapshot:
    payload = dict(raw)
    divs: list[DiscreteDividend] = []
    for item in payload.get("discrete_dividends") or []:
        if isinstance(item, dict):
            divs.append(DiscreteDividend(**item))
        elif isinstance(item, DiscreteDividend):
            divs.append(item)
    payload["discrete_dividends"] = divs
    allowed = {f.name for f in fields(MarketSnapshot)}
    return MarketSnapshot(**{k: v for k, v in payload.items() if k in allowed})


def _surface_from_dict(raw: dict[str, Any] | None) -> VolSurfaceData | None:
    if not raw:
        return None
    allowed = {f.name for f in fields(VolSurfaceData)}
    return VolSurfaceData(**{k: v for k, v in raw.items() if k in allowed})


def _news_from_rows(rows: list[Any]) -> list[NewsItem]:
    items: list[NewsItem] = []
    for row in rows or []:
        if isinstance(row, dict):
            title = str(row.get("title") or "").strip()
            if not title:
                continue
            items.append(
                NewsItem(
                    title=title,
                    publisher=str(row.get("publisher") or ""),
                    link=str(row.get("link") or ""),
                    published=str(row.get("published") or ""),
                )
            )
    return items


def _latest_source_run(day_dir: Path) -> Path | None:
    """Prefer original live_* archives; fall back to prior replay_* snapshots."""
    lives = sorted(
        [p for p in day_dir.iterdir() if p.is_dir() and p.name.startswith("live")],
        key=lambda p: p.name,
    )
    if lives:
        return lives[-1]
    replays = sorted(
        [p for p in day_dir.iterdir() if p.is_dir() and p.name.startswith("replay")],
        key=lambda p: p.name,
    )
    return replays[-1] if replays else None


def discover_days() -> list[tuple[str, Path]]:
    found: dict[str, Path] = {}
    for root in ARCHIVE_ROOTS:
        if not root.is_dir():
            continue
        for day in sorted(p for p in root.iterdir() if p.is_dir() and p.name[:4].isdigit()):
            run = _latest_source_run(day)
            if run is None:
                continue
            found[day.name] = run
    return [(as_of, found[as_of]) for as_of in sorted(found)]


def replay_day(as_of: str, src_run: Path) -> Path:
    legs_dir = src_run / "legs"
    if not legs_dir.is_dir():
        raise FileNotFoundError(f"No legs/ under {src_run}")
    bundles: list[PositionBundle] = []
    syntheses: list[DiagnosticSynthesis] = []
    findings: list[dict[str, Any]] = []
    surfaces: dict[str, VolSurfaceData | None] = {}
    errors: list[dict[str, str]] = []

    for path in sorted(legs_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        snap = _snapshot_from_dict(payload["snapshot"])
        surf = _surface_from_dict(payload.get("surface"))
        news = _news_from_rows(payload.get("news") or [])
        deps = GraphDeps(
            market=FrozenMarketLoader(LoadedData(snapshot=snap, surface=surf)),
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
        try:
            state = run_pipeline(
                ticker=snap.ticker,
                option_type=snap.option_type,
                strike=snap.strike,
                expiry=snap.expiry,
                quantity=snap.quantity,
                multiplier=snap.multiplier,
                deps=deps,
            )
            out_snap = state["snapshot"]
            pricing = state["pricing"]
            syn = DiagnosticSynthesis.model_validate(state.get("diagnostic_synthesis") or {})
            bundles.append(
                PositionBundle(
                    snapshot=out_snap,
                    pricing=pricing,
                    news=state.get("news") or [],
                    plan=state.get("search_plan"),
                )
            )
            syntheses.append(syn)
            findings.append(dict(state.get("diagnostic_findings") or {}))
            surfaces[out_snap.ticker] = surf
            fd = state.get("diagnostic_findings") or {}
            print(
                f"OK {as_of} {snap.ticker} verifier={fd.get('verifier_status')} "
                f"obs={fd.get('observation_reliable')} "
                f"digest_rel={len((fd.get('intel_digest') or {}).get('relevant') or [])} "
                f"challenge={((fd.get('catalyst_challenge') or {}).get('suppress_reason') or 'ran')}",
                file=sys.stderr,
            )
        except Exception as exc:
            errors.append({"ticker": snap.ticker, "error": f"{type(exc).__name__}: {exc}"})
            print(f"FAIL {as_of} {snap.ticker}: {exc}", file=sys.stderr)

    if not bundles:
        raise RuntimeError(f"{as_of}: no legs succeeded ({errors})")

    return _persist_run(
        as_of=as_of,
        label="replay",
        bundles=bundles,
        syntheses=syntheses,
        surfaces=surfaces,
        leg_findings=findings,
        extra_manifest={
            "mode": "archive_replay",
            "source_run": str(src_run),
            "errors": errors,
        },
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Replay archived live-book days")
    parser.add_argument(
        "--days",
        default="",
        help="Comma-separated as_of dates (default: every archived live day)",
    )
    args = parser.parse_args(argv)
    wanted = {d.strip() for d in args.days.split(",") if d.strip()}
    days = discover_days()
    if wanted:
        days = [(as_of, run) for as_of, run in days if as_of in wanted]
    if not days:
        print("No archived live days found.", file=sys.stderr)
        return 1
    print(f"Replaying {len(days)} day(s): {', '.join(a for a, _ in days)}", file=sys.stderr)
    for as_of, src in days:
        out = replay_day(as_of, src)
        print(f"{as_of}: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
