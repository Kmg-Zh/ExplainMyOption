"""Industrial Markdown template — quant sections are code-only."""

from __future__ import annotations

from typing import Any, Sequence

from ..intel.types import NewsItem, SearchPlan
from .facts import PositionBundle, PositionFacts, build_portfolio_facts, build_position_facts
from .formatting import is_reference_engine, official_model, pct
from .formatting import money as _money
from .reconciliation import ReconciliationFacts
from .schema import DiagnosticSynthesis
from .settlement import ExpirySettlement, render_settlements, settlement_total

# A factor counts as a headline driver when it is at least this share of the
# gross factor movement.
_DRIVER_MIN_GROSS_SHARE = 0.05


def _confidence_badge(level: str) -> str:
    return {"high": "**High**", "medium": "**Medium**", "low": "**Low**"}.get(
        level, level
    )


def _observation_lock_section(facts: PositionFacts) -> str:
    rec = facts.reconciliation
    lines = [
        "## 2. Observation Lock",
        "",
        f"* **As-of**: `{facts.eval_date}` | **Data**: `{facts.data_source}` | **IV prev**: `{facts.iv_prev_source}`",
    ]
    if rec is not None:
        lines.append(
            f"* **Quote tier**: `{rec.quote_tier}`"
            + (f" (spread/mid {rec.spread_pct_mid:.1%})" if rec.spread_pct_mid is not None else "")
        )
        if rec.iv_noise_band_pts is not None:
            within = (
                "inside noise band — **Vega story not falsifiable**"
                if rec.iv_move_within_noise
                else "exceeds noise band"
            )
            lines.append(
                f"* **IV move**: {rec.iv_move_pts:+.2f} vol pts vs noise band ±{rec.iv_noise_band_pts:.2f} pts ({within})"
            )
        if rec.deep_otm_itm:
            lines.append("* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.")
        if not rec.observation_reliable:
            lines.append(
                "* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news."
            )
    else:
        lines.append("* **Observation lock**: no live quote tier — model-only path.")
    if facts.prev_as_of_note:
        lines.append(f"* **Prior observation**: `{facts.prev_as_of_note}`")
    return "\n".join(lines)


def _reconciliation_section(facts: PositionFacts) -> str:
    rec = facts.reconciliation
    lines = [
        "## 3. Mark Reconciliation",
        "",
    ]
    if rec is None or rec.mark_pnl_usd is None:
        lines.append(f"* **Model ΔP (engine)**: `{_money(facts.model_pnl_usd)}`")
        lines.append("* **Mark ΔP**: unavailable — no valid marks on both dates.")
        explained = facts.model_pnl_usd - facts.attribution[-1].usd
        lines.append(f"* **Explained ΔP (Taylor ex-residual)**: `{_money(explained)}`")
        lines.extend(_two_residuals_lines(facts, rec))
        return "\n".join(lines)

    lines.append(f"* **Mark ΔP (MTM)**: `{_money(rec.mark_pnl_usd)}`")
    lines.append(f"* **Model ΔP (engine)**: `{_money(rec.model_pnl_usd)}`")
    if rec.model_vs_mark_gap_usd is not None:
        gap_note = (
            f" ({pct(rec.gap_pct_of_model)} of model)"
            if rec.gap_pct_of_model is not None
            else ""
        )
        lines.append(
            f"* **Model vs Mark gap**: `{_money(rec.model_vs_mark_gap_usd)}`{gap_note}"
        )
    explained = rec.model_pnl_usd - facts.attribution[-1].usd
    lines.append(f"* **Explained ΔP (Taylor ex-residual)**: `{_money(explained)}`")
    if rec.mark_calibrated:
        lines.append("* **Mark calibration**: active (`diagnostics.mark_calibrated`)")
    lines.extend(_two_residuals_lines(facts, rec))
    return "\n".join(lines)


def _two_residuals_lines(facts: PositionFacts, rec: ReconciliationFacts | None) -> list[str]:
    """The method and model residuals, always as separate lines."""
    method = rec.residual_method_usd if rec is not None else facts.attribution[-1].usd
    lines = [
        "",
        f"* **Method residual (ε_method)**: `{_money(method)}` — arithmetic, "
        "not news (ΔP_model minus the Taylor components).",
    ]
    if rec is None or rec.residual_model_usd is None:
        lines.append(
            "* **Model residual (ε_model)**: n/a (no reliable marks) — "
            "the gap between the market's price change and the model's."
        )
    else:
        lines.append(
            f"* **Model residual (ε_model)**: `{_money(rec.residual_model_usd)}` — "
            "ΔP_market − ΔP_model; the only residual a catalyst may explain."
        )
    basis = rec.escalation_basis if rec is not None else "method"
    metric = rec.escalation_metric_pct if rec is not None else None
    metric_note = f" ({pct(metric, signed=False)})" if metric is not None else ""
    lines.append(f"* **Escalation basis**: `{basis}`{metric_note}")
    if basis == "method":
        dates = f"{facts.eval_date}" if not facts.prev_as_of_note else f"{facts.prev_as_of_note} and/or {facts.eval_date}"
        if facts.iv_prev_source in ("hv20_proxy", "copied"):
            cause = (
                f"prior-day vol is a `{facts.iv_prev_source}` stand-in, not a chain mark, "
                "so the market-vs-model gap cannot be measured"
            )
        elif rec is not None and not rec.marks_reliable_now:
            cause = f"today's option quote tier is `{rec.quote_tier}`, not reliable"
        elif rec is not None and not rec.marks_reliable_prev:
            cause = "the prior-day option quote is not reliable"
        else:
            cause = f"reliable option marks were unavailable on {dates}"
        lines.append(
            f"  Escalation basis: method residual — {cause}; this run explains a "
            "model price change, not a market price change."
        )
    return lines


def _attribution_table(facts: PositionFacts) -> str:
    share_note = (
        " (the components largely offset, so % Share is of the gross movement Σ|component|)"
        if facts.shares_of_gross
        else ""
    )
    lines = [
        f"Greek-based (Taylor) attribution (official {official_model(facts.engine)} Greeks, "
        f"T-1 sensitivities){share_note}:",
        "",
        "| Attribution Component | Value ($) | % Share | Quant Driver |",
        "| :--- | ---: | ---: | :--- |",
    ]
    for row in facts.attribution:
        lines.append(
            f"| **{row.label}** | `{_money(row.usd)}` | {pct(row.share_pct)} | {row.driver_note} |"
        )
    lines.append(
        f"| **Total Model PnL** | **{_money(facts.model_pnl_usd)}** | **{pct(facts.total_share_pct)}** | "
        f"ΔP = P₁ − P₀ (model) |"
    )
    return "\n".join(lines)


def _residual_drill_section(
    facts: PositionFacts,
    diagnostic_findings: dict[str, Any] | None,
) -> str:
    findings = diagnostic_findings or {}
    results = findings.get("results") or {}
    # Tool payloads are per option; PnL figures below are position-scaled
    # like the attribution table.
    scale = facts.position_scale
    lines = [
        "## 5. Residual Drill",
        "",
        f"* **Taylor residual**: `{_money(facts.attribution[-1].usd)}` "
        f"({pct(facts.residual_pct, signed=False)} of |model|)",
    ]
    if findings.get("terminal_cause") == "verifier_hard_fail":
        lines.append(
            "* **Terminal break**: the verifier's hard failure was confirmed by code (see Headline); "
            "the narrative is not reliable and needs human review."
        )
    elif findings.get("terminal_unexplained_break"):
        lines.append(
            "* **Terminal break**: diagnostic budget exhausted with large unexplained "
            "residual/gap; the factor story is not reliable and needs human review."
        )
    taylor_regime = findings.get("taylor_regime")
    if taylor_regime == "INVALID":
        r_spot = findings.get("r_spot")
        lines.append(
            "* **Regime**: the move this day is outside the range where a Taylor "
            f"expansion is valid (r_spot = {r_spot:.2f})." if r_spot is not None
            else "* **Regime**: the move this day is outside the range where a "
            "Taylor expansion is valid."
        )
        lines.append(
            "  The Greek decomposition below is shown for reference; the headline "
            "attribution comes from full revaluation."
        )
    second = results.get("taylor_second_order")
    if second:
        # A term earns its own line only if |term| >= max(1% of |ΔP|, $0.01);
        # smaller terms fold into one line.
        materiality_floor = max(0.01 * abs(facts.model_pnl_usd), 0.01)
        vanna_pnl = scale * float(second.get("vanna_pnl", 0.0))
        volga_pnl = scale * float(second.get("volga_pnl", 0.0))
        term_lines: list[str] = []
        folded = 0.0
        if abs(vanna_pnl) >= materiality_floor:
            term_lines.append(f"Vanna PnL: `{_money(vanna_pnl)}`")
        else:
            folded += vanna_pnl
        if abs(volga_pnl) >= materiality_floor:
            term_lines.append(f"Volga PnL: `{_money(volga_pnl)}`")
        else:
            folded += volga_pnl
        if abs(folded) > 1e-12:
            term_lines.append(f"other second-order: `{_money(folded)}`")
        lines.extend(
            [
                "",
                "### Second-order Taylor (vanna, volga)"
                + (" — reference only, see Regime above" if taylor_regime == "INVALID" else ""),
                "* " + " | ".join(term_lines),
                f"* Combined: `{_money(scale * float(second.get('combined_pnl', 0.0)))}` | "
                f"Residual after: `{_money(scale * float(second.get('residual_after', 0.0)))}`",
            ]
        )
    path = results.get("path_reprice")
    if path:
        lines.extend(["", "### Sequential full revaluation (t → S → σ → r)"])
        for step in path.get("steps") or []:
            lines.append(
                f"* **{step.get('factor', '?')}**: `{_money(scale * float(step.get('pnl_usd', 0.0)))}`"
            )
        lines.append(
            f"* Step sum: `{_money(scale * float(path.get('step_sum', 0.0)))}` | "
            f"Model ΔP: `{_money(scale * float(path.get('model_total_pnl', 0.0)))}` | "
            f"Audit residual: `{_money(scale * float(path.get('residual_vs_model', 0.0)))}`"
        )
    if not second and not path:
        lines.append(
            "* _No deep diagnostic tools ran — residual may reflect truncation, American effects, or data gaps._"
        )
    split = findings.get("ex_div_attribution")
    if isinstance(split, dict) and split.get("flag_ex_div_window"):
        lines.extend(
            [
                "",
                "### Ex-div attribution overlay (official PnL stays the American FDM Taylor blotter)",
                f"* **Spot drop vs dividend** (per share): spot `{_money(float(split.get('spot_drop') or 0.0))}` "
                f"vs next cash dividend `{_money(float(split.get('dividend_amount') or 0.0))}` "
                f"(gap `{_money(float(split.get('spot_drop_vs_dividend') or 0.0))}`)",
                f"* **American FDM vs European analytic (no cash div, cross-check, per option)**: "
                f"`{_money(float(split.get('american_price') or 0.0))}` vs "
                f"`{_money(float(split.get('european_analytic_no_div') or 0.0))}` "
                f"(gap `{_money(float(split.get('am_minus_eu') or 0.0))}`)",
                f"* **Early-exercise premium** (American vs European, same dividend "
                f"schedule, signed, not floored, per option): "
                f"`{_money(float(split.get('ee_premium_now') or 0.0))}`"
                + (
                    " — material"
                    if split.get("ee_premium_material")
                    else " — not material"
                ),
                f"* **Dividend PV effect** (European, same divs − no divs, per option): "
                f"`{_money(float(split.get('dividend_pv_effect') or 0.0))}`",
                (
                    f"* **Dividend coverage** (dividend / time value): "
                    f"`{float(split.get('dividend_coverage')):.2f}` — "
                    + (
                        "early exercise is economically relevant"
                        if split.get("ee_relevant")
                        else "carry/theta case, not an early-exercise case"
                    )
                    if split.get("dividend_coverage") is not None
                    and split.get("ee_relevant") is not None
                    else "* **Dividend coverage**: n/a (no upcoming dividend or expiry data)"
                ),
                f"* **Vol (Taylor Vega PnL)**: `{_money(scale * float(split.get('vega_pnl') or 0.0))}`",
                f"* **Residual (Taylor ε)**: `{_money(scale * float(split.get('residual_pnl') or 0.0))}`",
                "* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._",
            ]
            + (
                [
                    f"* early exercise premium: {float(split.get('ee_premium_now') or 0.0):.4f} "
                    "(NEGATIVE — numerical anomaly from an engine/grid inconsistency, "
                    "not an exercise signal)"
                ]
                if split.get("ee_premium_anomaly")
                else []
            )
        )
    return "\n".join(lines)


def _diagnostic_summary_section(findings: dict[str, Any] | None) -> str:
    if not findings:
        return ""
    tools = findings.get("tools_run") or []
    skipped = findings.get("skipped_tools") or []
    from ..graph.diagnostic_controller import FREE_TOOLS, MAX_DIAGNOSTIC_TOOL_CALLS

    costly = sum(1 for t in tools if t not in FREE_TOOLS)
    lines = [
        "### Diagnostic tool summary",
        "",
        f"* **Tools run** ({len(tools)} total; costly {costly}/{MAX_DIAGNOSTIC_TOOL_CALLS}, "
        "free tools do not use the budget): "
        + (", ".join(f"`{t}`" for t in tools) if tools else "none"),
    ]
    if skipped:
        lines.append("* **Skipped candidates**:")
        for item in skipped:
            if isinstance(item, dict):
                lines.append(f"  * `{item.get('name', '?')}` — {item.get('reason', '')}")
    records = findings.get("playbook_records") or []
    if records:
        lines.append(
            "* **Playbook records** (selected by code for the narrator): "
            + ", ".join(f"`{r.get('id', '?')}` (`{r.get('when', '?')}`)" for r in records)
        )
    return "\n".join(lines)


def _digest_item_lines(items: list[dict[str, Any]], start: int) -> tuple[list[str], int]:
    lines: list[str] = []
    idx = start
    for item in items[:5]:
        title = str(item.get("title") or "").strip()
        if not title:
            continue
        pub = str(item.get("publisher") or "").strip()
        fact = str(item.get("one_line_fact") or "").strip()
        src = f" _(Source: {pub})_" if pub else ""
        lines.append(f"{idx}. **{title}**{src}")
        if fact:
            lines.append(f"   {fact}")
        idx += 1
    return lines, idx


def _news_lines(news: list[NewsItem]) -> list[str]:
    lines = []
    for i, item in enumerate(news, 1):
        pub = f" — _{item.publisher}_" if item.publisher else ""
        lines.append(f"{i}. [{item.title}]({item.link}){pub}" if item.link else f"{i}. {item.title}{pub}")
    return lines


def _evidence_section(
    synthesis: DiagnosticSynthesis,
    news: list[NewsItem],
    plan: SearchPlan | None,
    facts: PositionFacts,
    diagnostic_findings: dict[str, Any] | None = None,
    *,
    section: int = 6,
) -> str:
    reliable = facts.reconciliation.observation_reliable if facts.reconciliation else True
    digest = (diagnostic_findings or {}).get("intel_digest")
    if not isinstance(digest, dict):
        digest = None
    digest_relevant = list(digest.get("relevant") or []) if digest else []
    digest_background = list(digest.get("background") or []) if digest else []
    digest_brief = str(digest.get("brief") or "").strip() if digest else ""
    digest_discarded_count = len(digest.get("discarded") or []) if digest else 0
    lines = [
        f"## {section}. Root-Cause Market Intelligence",
        "",
    ]
    if plan is not None and plan.skip_reason:
        lines.append(
            "_No catalyst search — move below materiality / observation lock._"
        )
        lines.append("")
        return "\n".join(lines)
    if not reliable:
        lines.append(
            "_Observation unreliable — event linkage suppressed; reconcile marks before catalyst stories._"
        )
        lines.append("")
        return "\n".join(lines)
    lines.append(
        f"_Targeted retrieval for dominant driver: **{synthesis.primary_driver}**._"
    )
    lines.append("")
    if digest_brief:
        lines.append(f"_Intel note: {digest_brief}_")
    if digest_discarded_count:
        lines.append(f"_Intel triage discarded {digest_discarded_count} low-relevance headline(s)._")
    if digest_brief or digest_discarded_count:
        lines.append("")
    notes = plan.honesty_notes() if plan is not None else []
    lines.extend(f"_{note}_" for note in notes)
    if notes:
        lines.append("")

    if digest is not None:
        item_lines, idx = _digest_item_lines(digest_relevant, 1)
        lines.extend(item_lines)
        if digest_background:
            if digest_relevant:
                lines.append("")
            lines.append("_Peer / sector background (indirect context, not a required catalyst):_")
            lines.append("")
            item_lines, idx = _digest_item_lines(digest_background, idx)
            lines.extend(item_lines)
        if idx == 1:
            lines.extend(_news_lines(news[:5]) or ["_No corroborating headlines retrieved for this window._"])
        return "\n".join(lines)
    if synthesis.evidence:
        for i, item in enumerate(synthesis.evidence, 1):
            lines.append(
                f"{i}. **[{item.headline}]** _(Source: {item.source})_  \n"
                f"   {item.relevance}"
            )
    else:
        lines.extend(_news_lines(news) or ["_No corroborating headlines retrieved for this window._"])
    return "\n".join(lines)


def _watchlist_section(
    synthesis: DiagnosticSynthesis,
    facts: PositionFacts,
    diagnostic_findings: dict[str, Any] | None,
    *,
    section: int = 7,
) -> str:
    lines = [f"## {section}. Risk Watchlist", ""]
    if diagnostic_findings and diagnostic_findings.get("terminal_unexplained_break"):
        lines.append(
            "* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock."
        )
    if synthesis.takeaways:
        for bullet in synthesis.takeaways:
            lines.append(f"* {bullet}")
    else:
        lines.append("* Monitor residual size and IV marks.")
    if facts.american.next_ex_div:
        lines.append(
            f"* **Assignment watch**: ex-div `{facts.american.next_ex_div}` — "
            f"{facts.american.early_exercise_assessment}"
        )
    return "\n".join(lines)


def render_position_report(
    facts: PositionFacts,
    synthesis: DiagnosticSynthesis,
    *,
    news: list[NewsItem] | None = None,
    plan: SearchPlan | None = None,
    diagnostic_findings: dict[str, Any] | None = None,
) -> str:
    """Seven-section morning-pack diagnostic report for one position."""
    news = news or []
    if is_reference_engine(facts.engine):
        status = f"Verified by QuantLib ({facts.engine})"
    else:
        status = f"Priced by {facts.engine}"
    headline_label = "Mark MTM PnL" if facts.headline_is_mtm else "Model PnL (no mark)"
    gross = sum(abs(r.usd) for r in facts.attribution)
    driver_parts = [
        f"**{row.label.split('(')[0].strip()}** ({pct(row.share_pct)})"
        for row in sorted(facts.attribution, key=lambda r: abs(r.usd), reverse=True)
        if row.key != "residual" and gross > 1e-12 and abs(row.usd) >= _DRIVER_MIN_GROSS_SHARE * gross
    ][:3]
    driver_line = " and ".join(driver_parts) if driver_parts else synthesis.primary_driver

    diag_block = _diagnostic_summary_section(diagnostic_findings)
    sections = [
        "# Option Price Movement Diagnostic Report",
        "",
        f"**Contract**: `{facts.contract_label}`  ",
        f"**Analysis Date**: `{facts.eval_date}` | **Status**: {status}",
        "",
        "---",
        "",
        "## 1. Headline",
        "",
        f"* **{headline_label}**: `{_money(facts.headline_pnl_usd)}` ({pct(facts.pnl_pct)})",
        f"* **Model ΔP**: `{_money(facts.model_pnl_usd)}`",
        f"* **Primary drivers**: {driver_line}.",
    ]
    if diagnostic_findings:
        vstatus = diagnostic_findings.get("verifier_status")
        if vstatus == "PARTIAL":
            sections.append(
                "* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied)."
            )
        elif vstatus == "FAIL":
            flags = ", ".join(diagnostic_findings.get("terminal_verifier_flags") or [])
            violation = str(diagnostic_findings.get("terminal_violation") or "").strip()
            sections.append(
                "* **Verifier**: FAIL — hard policy violation"
                + (f" ({flags})" if flags else "")
                + "; the factor story is not reliable."
                + (f" {violation}" if violation else "")
            )
    sections.extend(
        [
            f"* **Verdict**: {synthesis.verdict.strip()}",
            f"* **Confidence**: {_confidence_badge(facts.confidence)} — "
            f"{synthesis.confidence_rationale.strip()}",
            "",
            "---",
            "",
            _observation_lock_section(facts),
            "",
            "---",
            "",
            _reconciliation_section(facts),
            "",
            "---",
            "",
            "## 4. Quantitative PnL Attribution",
            "",
            _attribution_table(facts),
            "",
            "---",
            "",
            _residual_drill_section(facts, diagnostic_findings),
        ]
    )
    if diag_block:
        sections.extend(["", diag_block])
    sections.extend(
        [
            "",
            "---",
            "",
            _evidence_section(
                synthesis,
                news,
                plan,
                facts,
                diagnostic_findings,
                section=6,
            ),
            "",
            "---",
            "",
            _watchlist_section(synthesis, facts, diagnostic_findings, section=7),
        ]
    )
    return "\n".join(sections)


def render_portfolio_report(
    bundles: list[PositionBundle],
    syntheses: list[DiagnosticSynthesis],
    *,
    leg_findings: list[dict[str, Any] | None] | None = None,
    settlements: Sequence[ExpirySettlement] = (),
) -> str:
    """Portfolio roll-up plus per-position reports; legs settled at expiry last."""
    tail = "\n" + render_settlements(settlements) if settlements else ""
    if not bundles:
        return render_settlements(settlements) if settlements else "_Empty portfolio — no positions to diagnose._"
    leg_findings = leg_findings or [None] * len(bundles)
    if len(bundles) == 1:
        facts = build_position_facts(bundles[0].snapshot, bundles[0].pricing, news_count=len(bundles[0].news))
        report = render_position_report(
            facts,
            syntheses[0],
            news=bundles[0].news,
            plan=bundles[0].plan,
            diagnostic_findings=leg_findings[0],
        )
        return report.rstrip() + "\n" + tail if tail else report

    pf = build_portfolio_facts(bundles)
    lines = [
        "# Portfolio Option Diagnostic Report",
        "",
        f"**Analysis Date**: `{pf.eval_date}` | **Positions**: {pf.position_count} | "
        f"**Tickers**: {', '.join(pf.tickers)}",
        "",
        "---",
        "",
        "## Portfolio Executive Summary",
        "",
    ]
    if pf.total_mark_pnl is not None:
        lines.append(f"* **Total Mark MTM PnL**: `{_money(pf.total_mark_pnl)}`")
    lines.append(f"* **Total Model PnL**: `{_money(pf.total_model_pnl)}`")
    if pf.aggregate_mark_gap is not None:
        lines.append(f"* **Aggregate model vs mark gap**: `{_money(pf.aggregate_mark_gap)}`")
    if settlements:
        lines.append(
            f"* **Settled at expiry**: `{_money(settlement_total(settlements))}` across {len(settlements)} "
            "leg(s), not in the totals above (see Settled at expiry)"
        )
    lines.extend(
        [
            "",
            "| Rank | Contract | PnL ($) |",
            "| ---: | :--- | ---: |",
        ]
    )
    for i, (label, pnl) in enumerate(pf.top_by_abs_pnl, 1):
        lines.append(f"| {i} | `{label}` | `{_money(pnl)}` |")

    lines.extend(
        [
            "",
            "### Aggregate factor attribution",
            "",
            "| Factor | Portfolio ($) |",
            "| :--- | ---: |",
        ]
    )
    labels = {
        "delta": "Delta",
        "gamma": "Gamma",
        "vega": "Vega",
        "theta": "Theta",
        "residual": "Residual",
    }
    for key, usd in pf.aggregate_attribution.items():
        lines.append(f"| {labels[key]} | `{_money(usd)}` |")

    if pf.top_by_ticker:
        lines.extend(["", "### Notable underlyings", ""])
        for ticker, pnl in pf.top_by_ticker:
            lines.append(f"* **{ticker}**: `{_money(pnl)}` aggregate option PnL")

    lines.extend(["", "---", "", "## Position Detail", ""])

    for i, (bundle, synthesis, findings) in enumerate(
        zip(bundles, syntheses, leg_findings), 1
    ):
        facts = build_position_facts(
            bundle.snapshot, bundle.pricing, news_count=len(bundle.news)
        )
        lines.append(f"### Position {i} — `{facts.contract_label}`")
        lines.append("")
        lines.append(
            render_position_report(
                facts,
                synthesis,
                news=bundle.news,
                plan=bundle.plan,
                diagnostic_findings=findings,
            )
        )
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n" + tail
