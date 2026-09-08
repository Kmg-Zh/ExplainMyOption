"""Desk-quality verification of live portfolio e2e runs (test-only).

Reads archived leg JSON under tests/live_book/output/<as_of>/<run>/legs/.
Reconciliation math lives in ``src.report.reconciliation`` (shared with product).
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from explain_my_option.paths import LIVE_BOOK_OUTPUT_DIR
from explain_my_option.pricing.types import Greeks, MarketSnapshot, PnLAttribution, PricingDiagnostics, PricingResult
from explain_my_option.report.reconciliation import (
    THIN_OPEN_INTEREST,
    THIN_VOLUME,
    WIDE_SPREAD_PCT_MID,
    build_reconciliation_facts,
    quote_tier,
)

RUNS_ROOT = LIVE_BOOK_OUTPUT_DIR

_tier = quote_tier  # backward compat for tests


@dataclass
class LegVerdict:
    ticker: str
    option_type: str
    strike: float
    expiry: str
    qty_mult: float

    bid: Optional[float]
    ask: Optional[float]
    mid: Optional[float]
    spread: Optional[float]
    spread_pct_mid: Optional[float]
    volume: Optional[float]
    open_interest: Optional[float]
    tier: str

    mark_pnl_per_unit: float
    model_pnl_per_unit: float
    mark_pnl_book: float
    model_pnl_book: float
    gap_book: float

    iv_prev: float
    iv_now: float
    iv_move_pts: float
    vega_now: float
    iv_noise_band_pts: Optional[float]
    iv_move_within_noise: Optional[bool]

    mark_calibrated: bool
    limitations: list[str]


def _snapshot_from_dict(d: dict) -> MarketSnapshot:
    return MarketSnapshot(
        ticker=d["ticker"],
        option_type=d["option_type"],
        strike=float(d["strike"]),
        expiry=d["expiry"],
        spot_now=float(d.get("spot_now", 0)),
        spot_prev=float(d.get("spot_prev", 0)),
        iv_now=float(d["iv_now"]),
        iv_prev=float(d["iv_prev"]),
        option_price_now=float(d["option_price_now"]),
        option_price_prev=float(d["option_price_prev"]),
        time_to_expiry_years=float(d.get("time_to_expiry_years", 0.25)),
        bid=d.get("bid"),
        ask=d.get("ask"),
        mid=d.get("mid"),
        volume=d.get("volume"),
        open_interest=d.get("open_interest"),
        quantity=float(d.get("quantity", 1.0)),
        multiplier=float(d.get("multiplier", 1.0)),
        data_source=d.get("data_source", "yfinance"),
        as_of=d.get("as_of"),
    )


def _pricing_from_dict(d: dict) -> PricingResult:
    pnl_d = d["pnl"]
    g_now = d["greeks_now"]
    g_prev = d.get("greeks_prev", g_now)
    diag_d = d.get("diagnostics", {})
    return PricingResult(
        greeks_prev=Greeks(
            price=float(g_prev.get("price", 0)),
            delta=float(g_prev.get("delta", 0)),
            gamma=float(g_prev.get("gamma", 0)),
            vega=float(g_prev.get("vega", 0)),
            theta=float(g_prev.get("theta", 0)),
        ),
        greeks_now=Greeks(
            price=float(g_now.get("price", 0)),
            delta=float(g_now.get("delta", 0)),
            gamma=float(g_now.get("gamma", 0)),
            vega=float(g_now.get("vega", 0)),
            theta=float(g_now.get("theta", 0)),
        ),
        pnl=PnLAttribution(
            total_pnl=float(pnl_d["total_pnl"]),
            delta_pnl=float(pnl_d.get("delta_pnl", 0)),
            gamma_pnl=float(pnl_d.get("gamma_pnl", 0)),
            vega_pnl=float(pnl_d.get("vega_pnl", 0)),
            theta_pnl=float(pnl_d.get("theta_pnl", 0)),
            residual_pnl=float(pnl_d.get("residual_pnl", 0)),
            d_spot=float(pnl_d.get("d_spot", 0)),
            d_vol=float(pnl_d.get("d_vol", 0)),
        ),
        diagnostics=PricingDiagnostics(
            data_source=diag_d.get("data_source", "yfinance"),
            exercise_style=diag_d.get("exercise_style", "american"),
            engine=diag_d.get("engine", "fdm_flat"),
            mark_calibrated=bool(diag_d.get("mark_calibrated", False)),
            limitations=list(diag_d.get("limitations", [])),
        ),
    )


def evaluate_leg(payload: dict) -> LegVerdict:
    snap = _snapshot_from_dict(payload["snapshot"])
    pricing = _pricing_from_dict(payload["pricing"])
    rec = build_reconciliation_facts(snap, pricing)
    qty_mult = snap.position_scale()

    mark_pnl_unit = (
        float(snap.option_price_now) - float(snap.option_price_prev)
        if snap.option_price_now > 0 and snap.option_price_prev > 0
        else 0.0
    )
    model_pnl_unit = float(pricing.pnl.total_pnl)

    return LegVerdict(
        ticker=snap.ticker,
        option_type=snap.option_type,
        strike=snap.strike,
        expiry=snap.expiry,
        qty_mult=qty_mult,
        bid=snap.bid,
        ask=snap.ask,
        mid=snap.mid,
        spread=rec.spread,
        spread_pct_mid=rec.spread_pct_mid,
        volume=snap.volume,
        open_interest=snap.open_interest,
        tier=rec.quote_tier,
        mark_pnl_per_unit=mark_pnl_unit,
        model_pnl_per_unit=model_pnl_unit,
        mark_pnl_book=rec.mark_pnl_usd or mark_pnl_unit * qty_mult,
        model_pnl_book=rec.model_pnl_usd,
        gap_book=rec.model_vs_mark_gap_usd or (model_pnl_unit - mark_pnl_unit) * qty_mult,
        iv_prev=snap.iv_prev,
        iv_now=snap.iv_now,
        iv_move_pts=rec.iv_move_pts,
        vega_now=float(pricing.greeks_now.vega),
        iv_noise_band_pts=rec.iv_noise_band_pts,
        iv_move_within_noise=rec.iv_move_within_noise,
        mark_calibrated=rec.mark_calibrated,
        limitations=list(pricing.diagnostics.limitations),
    )


def load_run_legs(run_dir: Path) -> list[LegVerdict]:
    legs_dir = run_dir / "legs"
    out = []
    for path in sorted(legs_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        out.append(evaluate_leg(payload))
    return out


def find_latest_run_for_as_of(as_of: str) -> Optional[Path]:
    day = RUNS_ROOT / as_of
    if not day.is_dir():
        return None
    candidates = sorted(p for p in day.iterdir() if p.is_dir() and p.name.startswith("live"))
    return candidates[-1] if candidates else None


def check_daycount(as_of: str, run_dir: Path) -> str:
    prior_days = sorted(
        p.name for p in RUNS_ROOT.iterdir() if p.is_dir() and p.name < as_of
    )
    if not prior_days:
        return f"No prior archived as_of before {as_of}; cannot check day-count."
    prior_as_of = prior_days[-1]
    d0 = date.fromisoformat(prior_as_of)
    d1 = date.fromisoformat(as_of)
    actual_days = (d1 - d0).days
    verdict = "OK (1 day, matches engine assumption)" if actual_days == 1 else (
        f"MISMATCH — engine assumes dt_days=1.0 but actual gap to prior "
        f"archived as_of ({prior_as_of}) is {actual_days} calendar day(s). "
        f"Theta PnL for every leg is understated by ~{actual_days}x if the "
        f"prior day was the true observation point."
    )
    return f"{prior_as_of} -> {as_of}: {actual_days} calendar day(s). {verdict}"


def render_report(as_of: str, run_dir: Path, legs: list[LegVerdict]) -> str:
    lines = [
        f"# Desk P&L verification — {as_of}",
        "",
        f"*Run*: `{run_dir}`",
        "",
        "## 1. Day-count check",
        "",
        check_daycount(as_of, run_dir),
        "",
        "## 2. Mark-quality tiers",
        "",
        f"Thresholds: spread/mid > {WIDE_SPREAD_PCT_MID:.0%} -> wide; "
        f"volume < {THIN_VOLUME} or OI < {THIN_OPEN_INTEREST} -> thin.",
        "",
        "| Ticker | Tier | Spread | Spread/Mid | Volume | OI | IV move (pts) | Noise band (pts) | Attributable? |",
        "| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | :--- |",
    ]
    for leg in legs:
        noise_str = f"{leg.iv_noise_band_pts:.2f}" if leg.iv_noise_band_pts is not None else "—"
        if leg.iv_move_within_noise is None:
            attributable = "n/a (unquoted)"
        elif leg.iv_move_within_noise:
            attributable = "**NO — within noise**"
        else:
            attributable = "yes"
        lines.append(
            "| {t} | {tier} | {spr} | {sm} | {vol:.0f} | {oi:.0f} | {ivm:+.2f} | {nb} | {attr} |".format(
                t=leg.ticker,
                tier=leg.tier,
                spr=f"{leg.spread:.3f}" if leg.spread is not None else "—",
                sm=f"{leg.spread_pct_mid:.1%}" if leg.spread_pct_mid is not None else "—",
                vol=leg.volume or 0,
                oi=leg.open_interest or 0,
                ivm=leg.iv_move_pts,
                nb=noise_str,
                attr=attributable,
            )
        )

    flagged = [leg for leg in legs if leg.iv_move_within_noise]
    lines.extend(["", "### Legs where vega narrative is not falsifiable from the quote", ""])
    if flagged:
        for leg in flagged:
            lines.append(
                f"* **{leg.ticker}**: IV moved {leg.iv_move_pts:+.2f} pts, but the "
                f"bid-ask spread alone implies ±{leg.iv_noise_band_pts:.2f} pts of "
                f"price noise. A vega story here is not distinguishable from a stale "
                f"or noisy quote (tier: {leg.tier}, volume={leg.volume:.0f})."
            )
    else:
        lines.append("_None — every leg's IV move exceeds its bid-ask noise band._")

    lines.extend(["", "## 3. Model P&L vs mark-to-market P&L", ""])
    lines.append(
        "After product mark-calibration (`diagnostics.mark_calibrated`), model ΔP "
        "should match mark ΔP within solver tolerance. Remaining gap is calibration "
        "failure or missing marks — not something the diagnose narrative should invent."
    )
    lines.append("")
    lines.extend(
        [
            "| Ticker | Calibrated? | Mark ΔP (book) | Model ΔP (book) | Gap | Gap as % of \\|mark\\| |",
            "| :--- | :---: | ---: | ---: | ---: | ---: |",
        ]
    )
    tot_mark = tot_model = 0.0
    for leg in legs:
        tot_mark += leg.mark_pnl_book
        tot_model += leg.model_pnl_book
        pct = (leg.gap_book / abs(leg.mark_pnl_book) * 100.0) if abs(leg.mark_pnl_book) > 1e-9 else float("inf")
        pct_str = f"{pct:+.0f}%" if pct != float("inf") else "n/a (mark≈0)"
        cal = "yes" if leg.mark_calibrated else "no"
        lines.append(
            f"| {leg.ticker} | {cal} | {leg.mark_pnl_book:+.3f} | {leg.model_pnl_book:+.3f} | "
            f"{leg.gap_book:+.3f} | {pct_str} |"
        )
    tot_gap = tot_model - tot_mark
    tot_pct = (tot_gap / abs(tot_mark) * 100.0) if abs(tot_mark) > 1e-9 else float("inf")
    n_cal = sum(1 for leg in legs if leg.mark_calibrated)
    lines.extend(
        [
            f"| **Book total** | **{n_cal}/{len(legs)}** | **{tot_mark:+.2f}** | **{tot_model:+.2f}** | "
            f"**{tot_gap:+.2f}** | **{tot_pct:+.1f}%** |",
        ]
    )

    lines.extend(["", "## 4. Engine limitations flagged per leg", ""])
    any_lim = False
    for leg in legs:
        if leg.limitations:
            any_lim = True
            lines.append(f"* **{leg.ticker}**: {', '.join(leg.limitations)}")
    if not any_lim:
        lines.append("_No engine limitations flagged._")

    return "\n".join(lines) + "\n"


def run_for_as_of(as_of: str) -> Path:
    run_dir = find_latest_run_for_as_of(as_of)
    if run_dir is None:
        raise FileNotFoundError(f"No archived live run for {as_of} under {RUNS_ROOT}")
    legs = load_run_legs(run_dir)
    report = render_report(as_of, run_dir, legs)
    out = run_dir / "desk_pnl.md"
    out.write_text(report, encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Desk P&L verification over archived runs")
    parser.add_argument(
        "--as-of",
        action="append",
        default=None,
        help="as_of date(s) to verify (default: all archived live_* days)",
    )
    args = parser.parse_args(argv)

    if args.as_of:
        as_of_days = args.as_of
    else:
        as_of_days = sorted(
            p.name
            for p in RUNS_ROOT.iterdir()
            if p.is_dir() and any(c.name.startswith("live") for c in p.iterdir())
        )

    if not as_of_days:
        print("No archived live runs found.", file=sys.stderr)
        return 1

    for as_of in as_of_days:
        try:
            out = run_for_as_of(as_of)
            print(f"{as_of}: {out}")
        except FileNotFoundError as exc:
            print(f"{as_of}: SKIP ({exc})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
