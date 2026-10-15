"""Deterministic position blotter: contract, market move, Greeks, factor PnL."""

from __future__ import annotations

from ..pricing.types import MarketSnapshot, PricingResult
from .formatting import contract_id, money, num


def _md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def build_quant_section(snap: MarketSnapshot, pricing: PricingResult) -> str:
    """Render the single-position blotter as Markdown (no LLM)."""
    greeks = pricing.greeks_prev
    pnl = pricing.pnl
    diag = pricing.diagnostics
    scale = snap.position_scale()
    pos_greeks = greeks.scaled(scale)
    pos_pnl = pnl.scaled(scale)
    now_price = pricing.greeks_now.price
    qty_s = num(snap.quantity).rstrip("0").rstrip(".")
    mult_s = num(snap.multiplier).rstrip("0").rstrip(".")
    contract_rows = [
        ["Ticker", snap.ticker],
        ["Right", snap.option_type.upper()],
        ["Strike", f"{snap.strike:g}"],
        ["Expiry", snap.expiry],
        ["Style", f"`{diag.exercise_style}`"],
        ["Quantity", qty_s],
        ["Multiplier", f"{mult_s} (engine PnL is per 1 option; display = qty × multiplier)"],
        ["As-of", snap.as_of or "—"],
        ["Data source", f"`{diag.data_source}`"],
        ["Engine", f"`{diag.engine}`"],
        ["Local vol used", f"`{diag.local_vol_used}`"],
        ["IV prev source", f"`{diag.iv_prev_source or snap.iv_prev_source}`"],
    ]
    if diag.ql_version:
        contract_rows.append(["QuantLib", f"`{diag.ql_version}`"])
    lines = [f"## Position — {contract_id(snap)}", "", "### Contract"]
    lines.extend(_md_table(["Field", "Value"], contract_rows))
    lines.extend(["", "### Market move (T-1 → T)"])
    # The vols the official PnL used: mark-calibrated when marks exist.
    iv_prev = snap.iv_prev if diag.effective_iv_prev is None else diag.effective_iv_prev
    iv_now = snap.iv_now if diag.effective_iv_now is None else diag.effective_iv_now
    move_rows = [
        ["Spot", num(snap.spot_prev, 2), num(snap.spot_now, 2), money(pnl.d_spot)],
        ["IV", f"{num(iv_prev * 100, 2)}%", f"{num(iv_now * 100, 2)}%", f"{pnl.d_vol * 100:+.2f} pts"],
        ["Model price (per option)", num(greeks.price), num(now_price), money(now_price - greeks.price)],
    ]
    if snap.hv20_now is not None and snap.hv20_prev is not None:
        move_rows.append(
            [
                "HV20 (realized)",
                f"{num(snap.hv20_prev * 100, 2)}%",
                f"{num(snap.hv20_now * 100, 2)}%",
                f"{(snap.hv20_now - snap.hv20_prev) * 100:+.2f} pts",
            ]
        )
    lines.extend(_md_table(["", "T-1", "T", "Change"], move_rows))
    lines.extend(
        [
            "",
            f"- Time to expiry: {num(snap.time_to_expiry_years, 3)} yr",
            "",
            "### Greeks (previous close, official engine)",
        ]
    )
    lines.extend(
        _md_table(
            ["", "Per option", "Position"],
            [
                ["Delta", num(greeks.delta), num(pos_greeks.delta)],
                ["Gamma", num(greeks.gamma), num(pos_greeks.gamma)],
                ["Vega (per 1 vol pt)", num(greeks.vega), num(pos_greeks.vega)],
                ["Theta (per day)", num(greeks.theta), num(pos_greeks.theta)],
            ],
        )
    )
    lines.extend(["", "### 1-day factor PnL (official FDM, position-scaled)"])
    lines.extend(
        _md_table(
            ["Factor", "USD"],
            [
                ["**Total**", f"**{money(pos_pnl.total_pnl)}**"],
                ["Delta (ΔS)", money(pos_pnl.delta_pnl)],
                ["Gamma (½(ΔS)²·Γ)", money(pos_pnl.gamma_pnl)],
                ["Vega (Δσ)", money(pos_pnl.vega_pnl)],
                ["Theta (decay)", money(pos_pnl.theta_pnl)],
                ["Residual (ε)", money(pos_pnl.residual_pnl)],
            ],
        )
    )
    if diag.early_exercise_premium is not None:
        lines.extend(
            [
                "",
                "### Early exercise (flat FDM, American vs European, same dividend schedule)",
                f"- Official American price: {num(diag.american_price or 0.0)}",
                f"- European analytic (no cash div, cross-check): {num(diag.european_price or 0.0)}",
                f"- Early-exercise premium (American − European, same divs): {money(diag.early_exercise_premium)}",
            ]
        )
        if diag.dividend_pv_effect is not None:
            lines.append(
                f"- Dividend PV effect (European, same divs − no divs): {money(diag.dividend_pv_effect)}"
            )
        if diag.ee_premium_anomaly:
            lines.append(
                f"- early exercise premium: {diag.early_exercise_premium:.4f} "
                "(NEGATIVE — numerical anomaly from an engine/grid inconsistency, "
                "not an exercise signal)"
            )
    if diag.limitations:
        lines.extend(["", f"_Limitations: {', '.join(diag.limitations)}_"])

    sd = pricing.surface_diagnostics
    if sd is not None:
        lines.extend(["", "### Surface / Heston diagnostics"])
        if sd.skew_proxy is not None:
            lines.append(f"- Skew proxy: {num(sd.skew_proxy)}")
        if sd.term_slope is not None:
            lines.append(f"- Term slope: {num(sd.term_slope)}")
        if sd.heston_params is not None:
            # Optimizer output is only stable to ~4dp across machines; the full
            # float repr would make the golden files platform-dependent.
            hp = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in sd.heston_params.items()}
            lines.append(f"- Heston params: `{hp}`")
            lines.append(f"- Heston RMSE: {num(sd.heston_rmse or 0.0)}")
        if sd.american_surface_price is not None:
            lines.append(f"- American FD under surface: {num(sd.american_surface_price)}")
        if sd.american_heston_price is not None:
            lines.append(f"- American FD under Heston: {num(sd.american_heston_price)}")
        if sd.limitations:
            lines.append(f"- Surface limitations: {', '.join(sd.limitations)}")

    return "\n".join(lines)
