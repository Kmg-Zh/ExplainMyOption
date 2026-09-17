"""Test-only portfolio e2e: fetch → quant → blotter → search → diagnose.

Not a product API. Default live mode uses a **pinned** contract book so
day-over-day marks stay comparable. Archives under ``tests/live_book/output/``.

    python tests/live_book/portfolio_e2e.py --offline
    python tests/live_book/portfolio_e2e.py --live --compare-to-baseline
    ./scripts/run-portfolio-e2e.sh
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Optional

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from dotenv import load_dotenv

load_dotenv()  # same as app.py — .env is not auto-exported into the process

from live_book.portfolio_book import (
    DEFAULT_PINNED_BOOK,
    LIVE_LEGS,
    OFFLINE_AS_OF,
    OFFLINE_LEGS,
    LiveLeg,
    OfflineLeg,
    PinnedLeg,
    load_pinned_book,
)
from live_book.compare_runs import compare_run_dirs, find_latest_run
from live_book.strikes import pick_strike
from explain_my_option.agent_graph import run_pipeline
from explain_my_option.data.cache import (
    DEFAULT_CACHE,
    count_snapshots,
    list_as_of_dates,
    upsert_snapshot,
)
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.data_loader import LoadedData
from explain_my_option.graph.deps import (
    FixtureMarketLoader,
    GraphDeps,
    MarketLoader,
    OfficialFdmPnlSource,
    YFinanceMarketLoader,
    default_deps,
)
from explain_my_option.graph.prompts import PROMPT_VERSION
from explain_my_option.intel.sources import IntelRegistry, StubIntelSource
from explain_my_option.pipeline.llm_roles import default_openai_roles, llm_run_metadata
from explain_my_option.paths import LIVE_BOOK_OUTPUT_DIR, TESTS_DIR
from ci.engine_config import engine_config_for_tests
from explain_my_option.pricing.config import EngineConfig
from explain_my_option.pricing.facade import price_and_attribute
from explain_my_option.pricing.types import MarketSnapshot, PricingResult, VolSurfaceData
from explain_my_option.report.facts import PositionBundle, build_portfolio_facts, build_position_facts
from explain_my_option.report.schema import DiagnosticSynthesis
from explain_my_option.report.synthesis import fallback_synthesis, synthesize_diagnosis
from explain_my_option.report.template import render_portfolio_report

# Test artifacts only (gitignored via tests/live_book/output/).
RUNS_ROOT = LIVE_BOOK_OUTPUT_DIR


@dataclass
class ResolvedLiveContract:
    leg: LiveLeg
    strike: float
    expiry: str
    spot: float


class PatchingMarketLoader:
    """Wrap a market loader and apply per-ticker snapshot field patches after fetch."""

    def __init__(
        self,
        base: MarketLoader,
        patches: dict[str, dict[str, Any]],
    ) -> None:
        self.base = base
        self.patches = {k.upper(): dict(v) for k, v in patches.items()}

    def load(
        self,
        *,
        ticker: str,
        option_type: str,
        strike: Optional[float],
        expiry: Optional[str],
    ) -> LoadedData:
        data = self.base.load(
            ticker=ticker,
            option_type=option_type,
            strike=strike,
            expiry=expiry,
        )
        patch = self.patches.get(data.snapshot.ticker.upper()) or self.patches.get(
            ticker.upper()
        )
        if patch:
            for key, val in patch.items():
                setattr(data.snapshot, key, val)
        return data


def _apply_offline_overrides(snap: MarketSnapshot, overrides: dict[str, Any]) -> None:
    for key, val in overrides.items():
        setattr(snap, key, val)


def build_offline_bundles(
    *,
    config: EngineConfig | None = None,
) -> tuple[list[PositionBundle], list[DiagnosticSynthesis]]:
    cfg = config or engine_config_for_tests()
    bundles: list[PositionBundle] = []
    syntheses: list[DiagnosticSynthesis] = []
    for leg in OFFLINE_LEGS:
        snap, surf = load_fixture(leg.fixture)
        snap.ticker = leg.ticker
        _apply_offline_overrides(snap, leg.overrides)
        pricing = price_and_attribute(snap, surf, config=cfg)
        bundles.append(PositionBundle(snapshot=snap, pricing=pricing))
        facts = build_position_facts(snap, pricing)
        syntheses.append(fallback_synthesis(facts, llm_unavailable=True))
    return bundles, syntheses


def resolve_live_contract(leg: LiveLeg) -> ResolvedLiveContract:
    """Peek the live chain once to lock strike + expiry for this run."""
    import yfinance as yf

    from explain_my_option.data_loader import _pick_nearest_expiry

    tk = yf.Ticker(leg.ticker)
    hist = tk.history(period="5d", auto_adjust=False)
    if hist.empty:
        raise ValueError(f"No spot history for {leg.ticker}")
    spot = float(hist["Close"].iloc[-1])
    expiry = _pick_nearest_expiry(tk)
    chain = tk.option_chain(expiry)
    table = chain.calls if leg.option_type == "call" else chain.puts
    strike = pick_strike(
        table,
        spot,
        leg.option_type,
        leg.moneyness,
        distance_pct=leg.distance_pct,
    )
    return ResolvedLiveContract(leg=leg, strike=strike, expiry=expiry, spot=spot)


def _style_patches_from_pinned(
    legs: tuple[PinnedLeg, ...],
) -> dict[str, dict[str, Any]]:
    return {
        leg.ticker.upper(): {"exercise_style": leg.exercise_style}
        for leg in legs
        if leg.exercise_style != "american"
    }


def _style_patches() -> dict[str, dict[str, Any]]:
    return {
        leg.ticker.upper(): {"exercise_style": leg.exercise_style}
        for leg in LIVE_LEGS
        if leg.exercise_style != "american"
    }


def _live_deps(patches: dict[str, dict[str, Any]] | None = None) -> GraphDeps:
    base = default_deps()
    return GraphDeps(
        market=PatchingMarketLoader(
            YFinanceMarketLoader(), patches if patches is not None else _style_patches()
        ),
        pnl=base.pnl,
        planner=base.planner,
        intel=base.intel,
        diagnose_system_prompt=base.diagnose_system_prompt,
        diagnose_system_extra=base.diagnose_system_extra,
    )


def _offline_fixture_deps_for_leg(leg: OfflineLeg) -> GraphDeps:
    patches = dict(leg.overrides)
    patches.setdefault("ticker", leg.ticker)
    return GraphDeps(
        market=PatchingMarketLoader(
            FixtureMarketLoader(leg.fixture), {leg.ticker: patches}
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


def _run_dir(as_of: str, *, label: str) -> Path:
    """Live runs are stamped. Offline overwrites one slot so CI does not grow folders."""
    if label == "offline":
        path = RUNS_ROOT / "offline"
        if path.exists():
            shutil.rmtree(path)
        return path
    stamp = datetime.now().strftime("%H%M%S")
    return RUNS_ROOT / as_of / f"{label}_{stamp}"


def _write_leg_artifact(
    run_dir: Path,
    *,
    ticker: str,
    snapshot: MarketSnapshot,
    surface: Optional[VolSurfaceData],
    pricing: PricingResult,
    synthesis: DiagnosticSynthesis,
    news: list[Any] | None = None,
    search_plan: Any | None = None,
    diagnostic_findings: dict[str, Any] | None = None,
) -> None:
    leg_dir = run_dir / "legs"
    leg_dir.mkdir(parents=True, exist_ok=True)
    news_rows = []
    for item in news or []:
        if hasattr(item, "__dataclass_fields__"):
            news_rows.append(asdict(item))
        elif isinstance(item, dict):
            news_rows.append(item)
        else:
            news_rows.append({"title": str(item)})
    plan_payload = None
    if search_plan is not None:
        plan_payload = (
            search_plan.model_dump()
            if hasattr(search_plan, "model_dump")
            else dict(search_plan)
        )
    payload = {
        "snapshot": asdict(snapshot),
        "surface": asdict(surface) if surface is not None else None,
        "pricing": pricing.as_dict(),
        "synthesis": synthesis.model_dump(),
        "news": news_rows,
        "search_plan": plan_payload,
        "diagnostic_findings": diagnostic_findings or {},
    }
    (leg_dir / f"{ticker}.json").write_text(
        json.dumps(payload, indent=2, default=str),
        encoding="utf-8",
    )


def _persist_run(
    *,
    as_of: str,
    label: str,
    bundles: list[PositionBundle],
    syntheses: list[DiagnosticSynthesis],
    extra_manifest: dict[str, Any],
    surfaces: dict[str, Optional[VolSurfaceData]] | None = None,
    leg_findings: list[dict[str, Any] | None] | None = None,
) -> Path:
    run_dir = _run_dir(as_of, label=label)
    run_dir.mkdir(parents=True, exist_ok=True)
    surf_map = surfaces or {}
    findings_list = leg_findings or [None] * len(bundles)

    for bundle, synthesis, findings in zip(bundles, syntheses, findings_list):
        ticker = bundle.snapshot.ticker
        _write_leg_artifact(
            run_dir,
            ticker=ticker,
            snapshot=bundle.snapshot,
            surface=surf_map.get(ticker),
            pricing=bundle.pricing,
            synthesis=synthesis,
            news=bundle.news,
            search_plan=bundle.plan,
            diagnostic_findings=findings,
        )

    report = render_portfolio_report(
        bundles, syntheses, leg_findings=findings_list
    )
    (run_dir / "portfolio_report.md").write_text(report, encoding="utf-8")

    pf = build_portfolio_facts(bundles)
    manifest = {
        "as_of": as_of,
        "label": label,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "position_count": pf.position_count,
        "tickers": pf.tickers,
        "total_pnl": pf.total_pnl,
        "cache_path": str(DEFAULT_CACHE),
        "cache_as_of_dates": list_as_of_dates(),
        "cache_snapshot_count": count_snapshots(),
        "prompt_version": PROMPT_VERSION,
        "llm_run_metadata": extra_manifest.pop("llm_run_metadata", None),
        **extra_manifest,
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, default=str),
        encoding="utf-8",
    )
    return run_dir


def run_offline_portfolio_e2e(*, through_graph: bool = False) -> Path:
    """Offline portfolio experiment. Default: price + fallback synthesis (fast CI)."""
    bundles: list[PositionBundle] = []
    syntheses: list[DiagnosticSynthesis] = []

    roles = default_openai_roles() if through_graph else None
    if through_graph:
        for leg in OFFLINE_LEGS:
            snap0, _ = load_fixture(leg.fixture)
            deps = _offline_fixture_deps_for_leg(leg)
            state = run_pipeline(
                ticker=leg.ticker,
                option_type=snap0.option_type,
                strike=snap0.strike,
                expiry=snap0.expiry,
                quantity=float(leg.overrides.get("quantity", snap0.quantity)),
                multiplier=float(
                    leg.overrides.get("multiplier", snap0.multiplier)
                ),
                deps=deps,
                roles=roles,
            )
            snap = state["snapshot"]
            pricing = state["pricing"]
            syn_raw = state.get("diagnostic_synthesis")
            synthesis = (
                DiagnosticSynthesis.model_validate(syn_raw)
                if syn_raw
                else fallback_synthesis(
                    build_position_facts(snap, pricing), llm_unavailable=True
                )
            )
            bundles.append(
                PositionBundle(
                    snapshot=snap,
                    pricing=pricing,
                    news=state.get("news") or [],
                    plan=state.get("search_plan"),
                )
            )
            syntheses.append(synthesis)
    else:
        bundles, syntheses = build_offline_bundles()

    surfaces: dict[str, Optional[VolSurfaceData]] = {}
    for leg in OFFLINE_LEGS:
        _, surf = load_fixture(leg.fixture)
        surfaces[leg.ticker] = surf

    return _persist_run(
        as_of=OFFLINE_AS_OF,
        label="offline",
        bundles=bundles,
        syntheses=syntheses,
        surfaces=surfaces,
        extra_manifest={
            "mode": "offline",
            "through_graph": through_graph,
            "legs": [
                {
                    "ticker": leg.ticker,
                    "fixture": leg.fixture,
                    "moneyness": leg.moneyness,
                    "overrides": leg.overrides,
                }
                for leg in OFFLINE_LEGS
            ],
            "llm_run_metadata": llm_run_metadata(roles) if roles is not None else None,
        },
    )


def run_live_portfolio_e2e(
    *,
    resolve_moneyness: bool = False,
    pinned_book: Path | str | None = None,
) -> Path:
    """Live multi-leg e2e.

    Default: **pinned** contracts from ``pinned_books/book_2026-09-02.json`` so
    tomorrow's marks are comparable to today's (same strike/expiry/style/qty).

    Pass ``resolve_moneyness=True`` only to discover a new book (not for DoD).
    """
    bundles: list[PositionBundle] = []
    syntheses: list[DiagnosticSynthesis] = []
    leg_findings: list[dict[str, Any]] = []
    surfaces: dict[str, Optional[VolSurfaceData]] = {}
    errors: list[dict[str, str]] = []
    resolved_rows: list[dict[str, Any]] = []
    baseline_as_of: str | None = None
    mode = "live_resolve" if resolve_moneyness else "live_pinned"
    roles = default_openai_roles()

    if resolve_moneyness:
        deps = _live_deps()
        work: list[tuple[str, str, float | None, str | None, float, float, str]] = []
        # ticker, option_type, strike, expiry, qty, mult, style_label
        for leg in LIVE_LEGS:
            try:
                contract = resolve_live_contract(leg)
                work.append(
                    (
                        leg.ticker,
                        leg.option_type,
                        contract.strike,
                        contract.expiry,
                        leg.quantity,
                        leg.multiplier,
                        leg.exercise_style,
                    )
                )
                resolved_rows.append(
                    {
                        "ticker": leg.ticker,
                        "option_type": leg.option_type,
                        "moneyness": leg.moneyness,
                        "strike": contract.strike,
                        "expiry": contract.expiry,
                        "spot": contract.spot,
                        "exercise_style": leg.exercise_style,
                        "quantity": leg.quantity,
                        "multiplier": leg.multiplier,
                        "notes": leg.notes,
                    }
                )
            except Exception as exc:
                errors.append(
                    {"ticker": leg.ticker, "error": f"{type(exc).__name__}: {exc}"}
                )
                print(f"FAIL resolve {leg.ticker}: {exc}", file=sys.stderr)
    else:
        baseline_as_of, pinned = load_pinned_book(pinned_book)
        deps = _live_deps(_style_patches_from_pinned(pinned))
        work = [
            (
                leg.ticker,
                leg.option_type,
                leg.strike,
                leg.expiry,
                leg.quantity,
                leg.multiplier,
                leg.exercise_style,
            )
            for leg in pinned
        ]
        resolved_rows = [
            {
                "ticker": leg.ticker,
                "option_type": leg.option_type,
                "moneyness": leg.moneyness_at_pin,
                "strike": leg.strike,
                "expiry": leg.expiry,
                "spot": None,
                "exercise_style": leg.exercise_style,
                "quantity": leg.quantity,
                "multiplier": leg.multiplier,
                "notes": leg.notes,
                "pinned": True,
                "baseline_as_of": baseline_as_of,
            }
            for leg in pinned
        ]
        print(
            f"Pinned book ({baseline_as_of}): {len(pinned)} fixed contracts "
            f"from {Path(pinned_book) if pinned_book else DEFAULT_PINNED_BOOK}",
            file=sys.stderr,
        )

    for ticker, option_type, strike, expiry, quantity, multiplier, style in work:
        try:
            state = run_pipeline(
                ticker=ticker,
                option_type=option_type,
                strike=strike,
                expiry=expiry,
                quantity=quantity,
                multiplier=multiplier,
                deps=deps,
                roles=roles,
            )
            snap = state["snapshot"]
            pricing = state["pricing"]
            surf = state.get("surface")
            surfaces[snap.ticker] = surf
            upsert_snapshot(snap, surf)
            syn_raw = state.get("diagnostic_synthesis")
            synthesis = (
                DiagnosticSynthesis.model_validate(syn_raw)
                if syn_raw
                else synthesize_diagnosis(
                    snap, pricing, state.get("news") or [], ports=deps, role=roles.narrator
                )
            )
            bundles.append(
                PositionBundle(
                    snapshot=snap,
                    pricing=pricing,
                    news=state.get("news") or [],
                    plan=state.get("search_plan"),
                )
            )
            syntheses.append(synthesis)
            leg_findings.append(dict(state.get("diagnostic_findings") or {}))
            # Fill spot on pinned rows for the manifest.
            for row in resolved_rows:
                if row["ticker"] == snap.ticker and row.get("spot") is None:
                    row["spot"] = snap.spot_now
            print(
                f"OK {ticker} {option_type} K={strike:g} exp={expiry} "
                f"iv_prev={snap.iv_prev_source} style={snap.exercise_style}",
                file=sys.stderr,
            )
        except Exception as exc:
            errors.append({"ticker": ticker, "error": f"{type(exc).__name__}: {exc}"})
            print(f"FAIL {ticker}: {exc}", file=sys.stderr)

    if not bundles:
        raise RuntimeError(f"No legs succeeded: {errors}")

    as_of = bundles[0].snapshot.as_of or date.today().isoformat()
    return _persist_run(
        as_of=as_of,
        label="live",
        bundles=bundles,
        syntheses=syntheses,
        surfaces=surfaces,
        leg_findings=leg_findings,
        extra_manifest={
            "mode": mode,
            "baseline_as_of": baseline_as_of,
            "pinned_book": str(
                Path(pinned_book) if pinned_book else DEFAULT_PINNED_BOOK
            )
            if not resolve_moneyness
            else None,
            "resolved": resolved_rows,
            "errors": errors,
            "llm_run_metadata": llm_run_metadata(roles),
        },
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Test-only portfolio e2e (offline synthetic or live yfinance)"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--offline",
        action="store_true",
        help="Synthetic fixtures; no network",
    )
    mode.add_argument(
        "--live",
        action="store_true",
        help="Live book using pinned contracts (comparable day-over-day)",
    )
    mode.add_argument(
        "--compare",
        nargs=2,
        metavar=("BASELINE_RUN", "CURRENT_RUN"),
        help="Compare two archived run dirs (Markdown to stdout)",
    )
    parser.add_argument(
        "--through-graph",
        action="store_true",
        help="Offline only: run each leg through LangGraph (frozen news)",
    )
    parser.add_argument(
        "--resolve-moneyness",
        action="store_true",
        help="Live only: re-pick ITM/OTM/ATM (breaks day-over-day comparability)",
    )
    parser.add_argument(
        "--pinned-book",
        default=None,
        help=f"Pinned book JSON (default: {DEFAULT_PINNED_BOOK.name})",
    )
    parser.add_argument(
        "--compare-to-baseline",
        action="store_true",
        help="After --live, compare this run to the pinned baseline as_of archive",
    )
    args = parser.parse_args(argv)

    if args.compare:
        baseline_dir = Path(args.compare[0])
        current_dir = Path(args.compare[1])
        print(compare_run_dirs(baseline_dir, current_dir))
        return 0

    if args.live:
        run_dir = run_live_portfolio_e2e(
            resolve_moneyness=args.resolve_moneyness,
            pinned_book=args.pinned_book,
        )
    else:
        run_dir = run_offline_portfolio_e2e(through_graph=args.through_graph)

    dates = list_as_of_dates()
    print(f"Run archived → {run_dir}")
    print(
        f"Cache: {count_snapshots()} snapshots across {len(dates)} as_of day(s): "
        f"{', '.join(dates) if dates else '(empty)'}"
    )

    if args.live and args.compare_to_baseline and not args.resolve_moneyness:
        baseline_as_of, _ = load_pinned_book(args.pinned_book)
        # Prefer the earliest archive on the baseline day (pin discovery), never this run.
        search_roots = [
            RUNS_ROOT,
            TESTS_DIR / "output" / "live_book",  # pre-2026-09-03 layout
            TESTS_DIR / "output" / "portfolio_runs",  # pre-2026-09-02 name
            Path(".cache/explain-my-option/runs"),
        ]
        baseline_dir = None
        for root in search_roots:
            day = root / baseline_as_of
            if not day.is_dir():
                continue
            candidates = sorted(
                [
                    p
                    for p in day.iterdir()
                    if p.is_dir()
                    and p.name.startswith("live")
                    and p.resolve() != run_dir.resolve()
                ],
                key=lambda p: p.name,
            )
            if candidates:
                baseline_dir = candidates[0]
                break
        if baseline_dir is None:
            print(
                f"No prior baseline archive for {baseline_as_of}; skip compare.",
                file=sys.stderr,
            )
        else:
            md = compare_run_dirs(baseline_dir, run_dir)
            out = run_dir / "compare.md"
            out.write_text(md, encoding="utf-8")
            print(md)
            print(f"Compare → {out}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())