"""Industrial Markdown template — quant sections are code-only."""

from __future__ import annotations

from typing import Any

from ..data_loader import NewsItem
from ..intel.types import SearchPlan
from .facts import PositionBundle, PositionFacts, build_portfolio_facts, build_position_facts
from .schema import DiagnosticSynthesis


def _money(x: float) -> str:
    sign = "+" if x >= 0 else "-"
    return f"{sign}${abs(x):,.4f}"


def _pct(x: float) -> str:
    sign = "+" if x >= 0 else ""
    return f"{sign}{x:.1f}%"


def _abs_share(part: float, parts: list[float]) -> float:
    denom = sum(abs(x) for x in parts)
    if denom < 1e-12:
        return 0.0
    return 100.0 * abs(part) / denom


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
        return "\n".join(lines)

    lines.append(f"* **Mark ΔP (MTM)**: `{_money(rec.mark_pnl_usd)}`")
    lines.append(f"* **Model ΔP (engine)**: `{_money(rec.model_pnl_usd)}`")
    if rec.model_vs_mark_gap_usd is not None:
        gap_note = (
            f" ({rec.gap_pct_of_model:+.1f}% of model)"
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
    return "\n".join(lines)


def _attribution_table(facts: PositionFacts) -> str:
    pct_note = (
        " (% shares use sum-of-|components| because |total PnL| is near zero)"
        if facts.pct_uses_abs_share
        else ""
    )
    lines = [
        f"Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities){pct_note}:",
        "",
        "| Attribution Component | Value ($) | % Share | Quant Driver |",
        "| :--- | ---: | ---: | :--- |",
    ]
    for row in facts.attribution:
        lines.append(
            f"| **{row.label}** | `{_money(row.usd)}` | {_pct(row.pct_of_total)} | {row.driver_note} |"
        )
    lines.append(
        f"| **Total Model PnL** | **{_money(facts.model_pnl_usd)}** | **100.0%** | "
        f"ΔP = P₁ − P₀ (model) |"
    )
    return "\n".join(lines)


def _residual_drill_section(
    facts: PositionFacts,
    diagnostic_findings: dict[str, Any] | None,
) -> str:
    findings = diagnostic_findings or {}
    results = findings.get("results") or {}
    lines = [
        "## 5. Residual Drill",
        "",
        f"* **Taylor residual**: `{_money(facts.attribution[-1].usd)}` "
        f"({facts.residual_pct:.1f}% of |model|)",
    ]
    if findings.get("terminal_unexplained_break"):
        lines.append(
            "* **Terminal break**: diagnostic budget exhausted with large unexplained "
            "residual/gap — escalate to human review before trading on factor stories."
        )
    second = results.get("taylor_second_order")
    if second:
        lines.extend(
            [
                "",
                "### Second-order Taylor (Layer 3)",
                f"* Vanna PnL: `{_money(second.get('vanna_pnl', 0.0))}` | "
                f"Volga PnL: `{_money(second.get('volga_pnl', 0.0))}`",
                f"* Combined: `{_money(second.get('combined_pnl', 0.0))}` | "
                f"Residual after: `{_money(second.get('residual_after', 0.0))}`",
            ]
        )
    path = results.get("path_reprice")
    if path:
        lines.extend(["", "### Sequential full revaluation (Layer 4, t → S → σ → r)"])
        for step in path.get("steps") or []:
            lines.append(
                f"* **{step.get('factor', '?')}**: `{_money(step.get('pnl_usd', 0.0))}`"
            )
        lines.append(
            f"* Step sum: `{_money(path.get('step_sum', 0.0))}` | "
            f"Model ΔP: `{_money(path.get('model_total_pnl', 0.0))}` | "
            f"Audit residual: `{_money(path.get('residual_vs_model', 0.0))}`"
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
                "### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)",
                f"* **Spot drop vs dividend**: spot `{_money(float(split.get('spot_drop') or 0.0))}` "
                f"vs next cash dividend `{_money(float(split.get('dividend_amount') or 0.0))}` "
                f"(gap `{_money(float(split.get('spot_drop_vs_dividend') or 0.0))}`)",
                f"* **American FDM vs European analytic (no cash div)**: "
                f"`{_money(float(split.get('american_price') or 0.0))}` vs "
                f"`{_money(float(split.get('european_analytic_no_div') or 0.0))}` "
                f"(gap `{_money(float(split.get('am_minus_eu') or 0.0))}`)",
                f"* **Early-exercise premium** (floored at 0 in diagnostics): "
                f"`{_money(float(split.get('ee_premium_now') or 0.0))}`"
                + (
                    " — material"
                    if split.get("ee_premium_material")
                    else " — not material"
                ),
                f"* **Vol (Taylor Vega PnL)**: `{_money(float(split.get('vega_pnl') or 0.0))}`",
                f"* **Residual (Taylor ε)**: `{_money(float(split.get('residual_pnl') or 0.0))}`",
                "* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._",
            ]
        )
    return "\n".join(lines)


def _diagnostic_summary_section(findings: dict[str, Any] | None) -> str:
    if not findings:
        return ""
    tools = findings.get("tools_run") or []
    skipped = findings.get("skipped_tools") or []
    lines = [
        "### Diagnostic tool summary",
        "",
        f"* **Tools run** ({findings.get('tool_calls_used', 0)}/3): "
        + (", ".join(f"`{t}`" for t in tools) if tools else "none"),
    ]
    if skipped:
        lines.append("* **Skipped candidates**:")
        for item in skipped:
            if isinstance(item, dict):
                lines.append(f"  * `{item.get('name', '?')}` — {item.get('reason', '')}")
    return "\n".join(lines)


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
    findings = diagnostic_findings or {}
    digest = findings.get("intel_digest") if isinstance(findings, dict) else None
    digest_relevant = (
        list(digest.get("relevant") or [])
        if isinstance(digest, dict)
        else []
    )
    digest_background = (
        list(digest.get("background") or [])
        if isinstance(digest, dict)
        else []
    )
    digest_brief = (
        str(digest.get("brief") or "").strip()
        if isinstance(digest, dict)
        else ""
    )
    digest_discarded_count = (
        len(digest.get("discarded") or [])
        if isinstance(digest, dict)
        else 0
    )
    lines = [
        f"## {section}. Root-Cause Market Intelligence",
        "",
    ]
    skip_reason = getattr(plan, "skip_reason", "") if plan is not None else ""
    if skip_reason:
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
    if plan is not None:
        for note in plan.honesty_notes():
            lines.append(f"_{note}_")
        if plan.honesty_notes():
            lines.append("")

    if isinstance(digest, dict):
        idx = 1
        for item in digest_relevant[:5]:
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
        if digest_background:
            if digest_relevant:
                lines.append("")
            lines.append("_Peer / sector background (indirect context, not a required catalyst):_")
            lines.append("")
            for item in digest_background[:5]:
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
        if idx == 1:
            if news:
                for i, item in enumerate(news[:5], 1):
                    pub = f" — _{item.publisher}_" if item.publisher else ""
                    if item.link:
                        lines.append(f"{i}. [{item.title}]({item.link}){pub}")
                    else:
                        lines.append(f"{i}. {item.title}{pub}")
            else:
                lines.append("_No corroborating headlines retrieved for this window._")
        return "\n".join(lines)
    if synthesis.evidence:
        for i, item in enumerate(synthesis.evidence, 1):
            lines.append(
                f"{i}. **[{item.headline}]** _(Source: {item.source})_  \n"
                f"   {item.relevance}"
            )
    elif news:
        for i, item in enumerate(news, 1):
            pub = f" — _{item.publisher}_" if item.publisher else ""
            if item.link:
                lines.append(f"{i}. [{item.title}]({item.link}){pub}")
            else:
                lines.append(f"{i}. {item.title}{pub}")
    else:
        lines.append("_No corroborating headlines retrieved for this window._")
    return "\n".join(lines)


def _watchlist_section(
    synthesis: DiagnosticSynthesis,
    facts: PositionFacts,
    diagnostic_findings: dict[str, Any] | None,
    *,
    section: int = 7,
) -> str:
    lines = [f"## {section}. Trading Desk Watchlist", ""]
    if diagnostic_findings and diagnostic_findings.get("terminal_unexplained_break"):
        lines.append(
            "* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock."
        )
    if synthesis.takeaways:
        for bullet in synthesis.takeaways:
            lines.append(f"* {bullet}")
    else:
        lines.append("* Monitor residual size and IV marks before sizing follow-on trades.")
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
    status = f"Verified by QuantLib ({facts.engine})"
    headline_label = "Mark MTM PnL" if facts.headline_is_mtm else "Model PnL (no mark)"
    driver_parts = [
        f"**{row.label.split('(')[0].strip()}** ({_abs_share(row.usd, [r.usd for r in facts.attribution]):.0f}%)"
        for row in sorted(facts.attribution, key=lambda r: abs(r.usd), reverse=True)
        if _abs_share(row.usd, [r.usd for r in facts.attribution]) >= 5.0 and row.key != "residual"
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
        f"* **{headline_label}**: `{_money(facts.headline_pnl_usd)}` "
        f"({ _pct(facts.pnl_pct) if facts.headline_is_mtm else _pct(facts.pnl_pct) })",
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
            sections.append(
                "* **Verifier**: FAIL — hard policy violation; escalate before trading on story."
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
) -> str:
    """Portfolio roll-up plus per-position reports."""
    if not bundles:
        return "_Empty portfolio — no positions to diagnose._"
    leg_findings = leg_findings or [None] * len(bundles)
    if len(bundles) == 1:
        facts = build_position_facts(bundles[0].snapshot, bundles[0].pricing, news_count=len(bundles[0].news))
        return render_position_report(
            facts,
            syntheses[0],
            news=bundles[0].news,
            plan=bundles[0].plan,
            diagnostic_findings=leg_findings[0],
        )

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

    return "\n".join(lines).rstrip() + "\n"
