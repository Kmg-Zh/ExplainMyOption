"""Markdown report formatter for the diagnostic output."""

from __future__ import annotations

from .data_loader import NewsItem
from .intel.types import SearchPlan
from .pricing.types import Greeks, MarketSnapshot, PnLAttribution, PricingResult


def _fmt(x: float, dp: int = 4) -> str:
    return f"{x:,.{dp}f}"


def _money(x: float) -> str:
    sign = "+" if x >= 0 else "-"
    return f"{sign}${abs(x):,.4f}"


def contract_id(snap: MarketSnapshot) -> str:
    right = "C" if snap.option_type.lower().startswith("c") else "P"
    return f"{snap.ticker} {snap.strike:g}{right} {snap.expiry}"


def scale_pnl(pnl: PnLAttribution, scale: float) -> PnLAttribution:
    """Scale factor PnL; market deltas (d_spot, d_vol) stay unscaled."""
    if scale == 1.0:
        return pnl
    return PnLAttribution(
        total_pnl=pnl.total_pnl * scale,
        delta_pnl=pnl.delta_pnl * scale,
        gamma_pnl=pnl.gamma_pnl * scale,
        vega_pnl=pnl.vega_pnl * scale,
        theta_pnl=pnl.theta_pnl * scale,
        residual_pnl=pnl.residual_pnl * scale,
        d_spot=pnl.d_spot,
        d_vol=pnl.d_vol,
    )


def scale_greeks(greeks: Greeks, scale: float) -> Greeks:
    if scale == 1.0:
        return greeks
    return Greeks(
        price=greeks.price * scale,
        delta=greeks.delta * scale,
        gamma=greeks.gamma * scale,
        vega=greeks.vega * scale,
        theta=greeks.theta * scale,
    )


def _md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def build_quant_section(snap: MarketSnapshot, pricing: PricingResult) -> str:
    """Render the deterministic single-position blotter as Markdown."""
    greeks = pricing.greeks_prev
    pnl = pricing.pnl
    diag = pricing.diagnostics
    scale = snap.position_scale()
    pos_greeks = scale_greeks(greeks, scale)
    pos_pnl = scale_pnl(pnl, scale)
    now_price = pricing.greeks_now.price
    qty_s = _fmt(snap.quantity, 4).rstrip("0").rstrip(".")
    mult_s = _fmt(snap.multiplier, 4).rstrip("0").rstrip(".")
    contract_rows = [
        ["Ticker", snap.ticker],
        ["Right", snap.option_type.upper()],
        ["Strike", f"{snap.strike:g}"],
        ["Expiry", snap.expiry],
        ["Style", f"`{diag.exercise_style}`"],
        ["Quantity", qty_s],
        [
            "Multiplier",
            f"{mult_s} (engine PnL is per 1 option; display = qty × multiplier)",
        ],
        ["As-of", snap.as_of or "—"],
        ["Data source", f"`{diag.data_source}`"],
        ["Engine", f"`{diag.engine}`"],
        ["Local vol used", f"`{diag.local_vol_used}`"],
        ["IV prev source", f"`{diag.iv_prev_source or snap.iv_prev_source}`"],
    ]
    if diag.ql_version:
        contract_rows.append(["QuantLib", f"`{diag.ql_version}`"])
    lines = [
        f"## Position — {contract_id(snap)}",
        "",
        "### Contract",
    ]
    lines.extend(_md_table(["Field", "Value"], contract_rows))
    lines.extend(
        [
            "",
            "### Market move (T-1 → T)",
        ]
    )
    hv_row: list[list[str]] = []
    if snap.hv20_now is not None and snap.hv20_prev is not None:
        hv_row = [
            [
                "HV20 (realized)",
                f"{_fmt(snap.hv20_prev * 100, 2)}%",
                f"{_fmt(snap.hv20_now * 100, 2)}%",
                f"{(snap.hv20_now - snap.hv20_prev) * 100:+.2f} pts",
            ]
        ]
    lines.extend(
        _md_table(
            ["", "T-1", "T", "Change"],
            [
                [
                    "Spot",
                    _fmt(snap.spot_prev, 2),
                    _fmt(snap.spot_now, 2),
                    _money(pnl.d_spot),
                ],
                [
                    "IV",
                    f"{_fmt(snap.iv_prev * 100, 2)}%",
                    f"{_fmt(snap.iv_now * 100, 2)}%",
                    f"{pnl.d_vol * 100:+.2f} pts",
                ],
                [
                    "Model price (per option)",
                    _fmt(greeks.price),
                    _fmt(now_price),
                    _money(now_price - greeks.price),
                ],
                *hv_row,
            ],
        )
    )
    lines.extend(
        [
            "",
            f"- Time to expiry: {_fmt(snap.time_to_expiry_years, 3)} yr",
            "",
            "### Greeks (previous close, official engine)",
        ]
    )
    lines.extend(
        _md_table(
            ["", "Per option", "Position"],
            [
                ["Delta", _fmt(greeks.delta), _fmt(pos_greeks.delta)],
                ["Gamma", _fmt(greeks.gamma), _fmt(pos_greeks.gamma)],
                ["Vega (per 1 vol pt)", _fmt(greeks.vega), _fmt(pos_greeks.vega)],
                ["Theta (per day)", _fmt(greeks.theta), _fmt(pos_greeks.theta)],
            ],
        )
    )
    lines.extend(
        [
            "",
            "### 1-day factor PnL (official FDM, position-scaled)",
        ]
    )
    lines.extend(
        _md_table(
            ["Factor", "USD"],
            [
                ["**Total**", f"**{_money(pos_pnl.total_pnl)}**"],
                ["Delta (ΔS)", _money(pos_pnl.delta_pnl)],
                ["Gamma (½(ΔS)²·Γ)", _money(pos_pnl.gamma_pnl)],
                ["Vega (Δσ)", _money(pos_pnl.vega_pnl)],
                ["Theta (decay)", _money(pos_pnl.theta_pnl)],
                ["Residual (ε)", _money(pos_pnl.residual_pnl)],
            ],
        )
    )
    if diag.early_exercise_premium is not None:
        lines.extend(
            [
                "",
                "### Early exercise (flat FDM vs European analytic)",
                f"- Official American price: {_fmt(diag.american_price or 0.0)}",
                f"- European analytic (flat): {_fmt(diag.european_price or 0.0)}",
                f"- Early-exercise premium (flat FDM − EU): {_money(diag.early_exercise_premium)}",
            ]
        )
    if diag.limitations:
        lines.extend(
            [
                "",
                f"_Limitations: {', '.join(diag.limitations)}_",
            ]
        )

    sd = pricing.surface_diagnostics
    if sd is not None:
        lines.extend(["", "### Surface / Heston diagnostics"])
        if sd.skew_proxy is not None:
            lines.append(f"- Skew proxy: {_fmt(sd.skew_proxy)}")
        if sd.term_slope is not None:
            lines.append(f"- Term slope: {_fmt(sd.term_slope)}")
        if sd.heston_params is not None:
            lines.append(f"- Heston params: `{sd.heston_params}`")
            lines.append(f"- Heston RMSE: {_fmt(sd.heston_rmse or 0.0)}")
        if sd.american_surface_price is not None:
            lines.append(
                f"- American FD under surface: {_fmt(sd.american_surface_price)}"
            )
        if sd.american_heston_price is not None:
            lines.append(
                f"- American FD under Heston: {_fmt(sd.american_heston_price)}"
            )
        if sd.limitations:
            lines.append(f"- Surface limitations: {', '.join(sd.limitations)}")

    return "\n".join(lines)


def build_news_section(
    news: list[NewsItem],
    *,
    plan: SearchPlan | None = None,
) -> str:
    lines = ["## Recent News", ""]
    if plan is not None:
        notes = plan.honesty_notes()
        for note in notes:
            lines.append(f"_{note}_")
        if notes:
            lines.append("")
    if not news:
        lines.append("_No recent headlines found._")
        return "\n".join(lines)
    for i, item in enumerate(news, 1):
        pub = f" — _{item.publisher}_" if item.publisher else ""
        if item.link:
            lines.append(f"{i}. [{item.title}]({item.link}){pub}")
        else:
            lines.append(f"{i}. {item.title}{pub}")
    return "\n".join(lines)


def build_report(
    snap: MarketSnapshot,
    pricing: PricingResult,
    news: list[NewsItem],
    diagnosis: str,
    *,
    blotter: str | None = None,
    plan: SearchPlan | None = None,
    synthesis: object | None = None,
) -> str:
    """Assemble the full Markdown diagnostic report.

    When ``synthesis`` is a ``DiagnosticSynthesis``, renders the industrial template.
    Otherwise falls back to legacy blotter + free-text diagnosis.
    """
    from .report.facts import build_position_facts
    from .report.schema import DiagnosticSynthesis
    from .report.template import render_position_report

    if isinstance(synthesis, DiagnosticSynthesis):
        facts = build_position_facts(snap, pricing, news_count=len(news))
        return render_position_report(facts, synthesis, news=news, plan=plan)

    quant = blotter if blotter is not None else build_quant_section(snap, pricing)
    return "\n\n".join(
        [
            f"# Explain My Option — {snap.ticker}",
            quant,
            build_news_section(news, plan=plan),
            "## Diagnosis",
            diagnosis.strip(),
        ]
    )
