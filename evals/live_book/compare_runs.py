"""Day-over-day comparison of pinned portfolio e2e run archives (test-only)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _leg_map(run_dir: Path) -> dict[str, dict[str, Any]]:
    legs_dir = run_dir / "legs"
    if not legs_dir.is_dir():
        raise FileNotFoundError(f"No legs/ under {run_dir}")
    out: dict[str, dict[str, Any]] = {}
    for path in sorted(legs_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        snap = payload["snapshot"]
        ticker = str(snap["ticker"]).upper()
        out[ticker] = payload
    return out


def _contract_key(snap: dict[str, Any]) -> tuple:
    return (
        str(snap["ticker"]).upper(),
        str(snap["option_type"]),
        float(snap["strike"]),
        str(snap["expiry"]),
    )


def compare_run_dirs(baseline_dir: Path, current_dir: Path) -> str:
    """Return a Markdown table comparing spot / IV / price / Greeks / PnL."""
    base = _leg_map(baseline_dir)
    curr = _leg_map(current_dir)
    tickers = sorted(set(base) | set(curr))

    lines = [
        "# Portfolio day-over-day comparison",
        "",
        f"*Baseline*: `{baseline_dir}`",
        f"*Current*: `{current_dir}`",
        "",
        "| Ticker | Contract match | Spot₀→₁ | IV₀→₁ | Opt₀→₁ | ΔPnL | iv_prev₁ |",
        "| :--- | :---: | ---: | ---: | ---: | ---: | :--- |",
    ]

    mismatches: list[str] = []
    for ticker in tickers:
        if ticker not in base or ticker not in curr:
            lines.append(
                f"| {ticker} | missing | — | — | — | — | — |"
            )
            mismatches.append(ticker)
            continue
        b_snap = base[ticker]["snapshot"]
        c_snap = curr[ticker]["snapshot"]
        same = _contract_key(b_snap) == _contract_key(c_snap)
        if not same:
            mismatches.append(ticker)
        b_pnl = float(base[ticker]["pricing"]["pnl"]["total_pnl"])
        c_pnl = float(curr[ticker]["pricing"]["pnl"]["total_pnl"])
        # Display uses quantity×multiplier already in pnl if scaled at facts;
        # engine pnl in artifact is per-option — still comparable same qty.
        qty = float(c_snap.get("quantity", 1.0)) * float(
            c_snap.get("multiplier", 1.0)
        )
        lines.append(
            "| {ticker} | {match} | {s0:.2f}→{s1:.2f} | {iv0:.1%}→{iv1:.1%} | "
            "{p0:.3f}→{p1:.3f} | {dpnl:+.4f} | {src} |".format(
                ticker=ticker,
                match="yes" if same else "NO",
                s0=float(b_snap["spot_now"]),
                s1=float(c_snap["spot_now"]),
                iv0=float(b_snap["iv_now"]),
                iv1=float(c_snap["iv_now"]),
                p0=float(b_snap.get("option_price_now") or 0.0),
                p1=float(c_snap.get("option_price_now") or 0.0),
                dpnl=(c_pnl - b_pnl) * qty,
                src=c_snap.get("iv_prev_source", "—"),
            )
        )

    lines.extend(["", "## Contracts (current)", ""])
    for ticker in sorted(curr):
        snap = curr[ticker]["snapshot"]
        lines.append(
            f"* **{ticker}**: {snap['option_type']} K={snap['strike']} "
            f"exp={snap['expiry']} style={snap.get('exercise_style', '—')}"
        )

    if mismatches:
        lines.extend(
            [
                "",
                f"_Contract mismatch or missing legs: {', '.join(mismatches)}_",
            ]
        )
    else:
        lines.extend(["", "_All 10 contracts match baseline (comparable)._"])

    return "\n".join(lines) + "\n"


def find_latest_run(
    runs_root: Path,
    as_of: str,
    *,
    label_prefix: str = "live",
) -> Path | None:
    day = runs_root / as_of
    if not day.is_dir():
        return None
    candidates = sorted(
        [p for p in day.iterdir() if p.is_dir() and p.name.startswith(label_prefix)],
        key=lambda p: p.name,
    )
    return candidates[-1] if candidates else None
