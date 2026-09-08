"""Desk blotter text for LLM diagnosis (read-only context)."""

from __future__ import annotations

from ..data_loader import NewsItem
from ..pricing.types import MarketSnapshot, PricingResult
from ..report_generator import build_quant_section
from .facts import build_position_facts


def format_desk_packet(
    snap: MarketSnapshot,
    pricing: PricingResult,
    news: list[NewsItem],
    *,
    desk_color: str | None = None,
) -> str:
    """Human-readable desk view — Greeks, factor PnL, residual, headlines."""
    facts = build_position_facts(snap, pricing, news_count=len(news))
    blotter = build_quant_section(snap, pricing)
    lines = [
        "## Desk blotter (read-only)",
        "",
        f"Contract: {facts.contract_label}",
        f"As-of: {facts.eval_date}",
        f"Engine: {facts.engine}",
        f"IV prev source: {facts.iv_prev_source}",
        "",
        "### Market moves",
        f"- Spot: {facts.spot_prev:.4f} → {facts.spot_now:.4f} ({facts.spot_pct:+.2f}%)",
        f"- IV: {facts.iv_prev:.2%} → {facts.iv_now:.2%} ({facts.d_vol_pts:+.2f} vol pts)",
        f"- Model ΔP (position-scaled): {facts.model_pnl_usd:+.4f}",
        "",
        "### T-1 Greeks (position-scaled in blotter)",
        f"- Delta: {facts.greeks_delta:.6f}",
        f"- Gamma: {facts.greeks_gamma:.6f}",
        f"- Vega: {facts.greeks_vega:.6f}",
        f"- Theta: {facts.greeks_theta:.6f}",
        "",
        "### Factor PnL (Greek-based Taylor, position-scaled)",
    ]
    for row in facts.attribution:
        lines.append(f"- {row.label}: {row.usd:+.4f} ({row.pct_of_total:+.1f}% of total)")
    lines.extend(
        [
            "",
            f"Primary driver (code): {facts.primary_driver}",
            f"Residual share of |model| (code): {facts.residual_pct:.1f}%",
            f"Confidence hint (code): {facts.confidence}",
            f"American assessment (code): {facts.american.early_exercise_assessment}",
            "",
            "### Full quant blotter (engine output)",
            "",
            blotter,
            "",
            "### News headlines",
        ]
    )
    if not news:
        lines.append("- (none)")
    else:
        for hit in news[:5]:
            pub = hit.publisher or "?"
            lines.append(f"- {hit.title} ({pub})")
    if desk_color:
        lines.extend(["", "### Desk color (context only)", desk_color.strip()])
    return "\n".join(lines)
