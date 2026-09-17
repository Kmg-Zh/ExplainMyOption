"""Structured LLM synthesis + deterministic fallback."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from ..data_loader import NewsItem, format_untrusted_source
from ..graph.prompts import compose_diagnose_system_prompt
from ..intel.types import SearchPlan
from ..pricing.types import MarketSnapshot, PricingResult
from .catalysts import tags_from_news, with_inferred_microstructure
from ..pipeline.digest import IntelDigest, coarse_kept_news
from .facts import PositionFacts, build_position_facts
from .desk_packet import format_desk_packet
from .schema import DiagnosticSynthesis, EvidenceItem
from .validate import validate_synthesis

if TYPE_CHECKING:
    from ..graph.deps import GraphDeps
    from ..pipeline.llm_roles import LlmRole

_DEFAULT_LLM_MODEL = "gpt-5.4-mini"

_DRIVER_LABELS = {
    "delta": "Delta / spot move",
    "gamma": "Gamma / convexity",
    "vega": "Vega / implied volatility",
    "theta": "Theta / time decay",
    "residual": "Unexplained residual",
}


def fallback_synthesis(
    facts: PositionFacts,
    *,
    llm_failed: bool = False,
    llm_unavailable: bool = False,
    diagnostic_findings: dict | None = None,
    news: list[NewsItem] | None = None,
) -> DiagnosticSynthesis:
    """Deterministic narrative when the LLM is off or validation fails."""
    driver = _DRIVER_LABELS.get(facts.primary_driver, facts.primary_driver_label)
    direction = "gained" if facts.total_pnl >= 0 else "lost"
    verdict = (
        f"The position {direction} value over the session; the largest attributed "
        f"component is {driver}. Residual and American effects are flagged when "
        f"Taylor coverage is below desk thresholds."
    )
    if llm_failed:
        rationale = (
            "LLM synthesis failed — using rule-based summary. Quant sections remain "
            "engine-verified."
        )
    elif llm_unavailable:
        rationale = (
            "No OPENAI_API_KEY — narrative is rule-based; all dollar amounts are "
            "in the quant tables only."
        )
    else:
        rationale = facts.confidence_reasons[0] if facts.confidence_reasons else (
            "Rule-based synthesis."
        )

    takeaways: list[str] = []
    findings = diagnostic_findings or {}

    if findings.get("terminal_unexplained_break"):
        takeaways.insert(
            0,
            "**Terminal break**: diagnostic budget exhausted with large unexplained residual — escalate to human review.",
        )

    # Vega: post-event crush risk (skip when quote noise suppresses Vega narrative)
    if facts.reconciliation and facts.reconciliation.iv_move_within_noise:
        takeaways.append(
            "**Quote quality**: IV move sits inside the bid-ask noise band — do not treat Vega as "
            "a falsifiable driver from this quote alone."
        )
    elif facts.primary_driver == "vega":
        takeaways.append(
            "**Vega risk**: If IV was the main driver, monitor for post-event crush (e.g., earnings release, "
            "Fed decision). Consider hedging vega or taking profits before catalysts."
        )

    # High residual: model gap or unmodeled effects
    if facts.residual_pct > 15.0:
        takeaways.append(
            "**Elevated residual (>{:.0f}%)**: Review American early-exercise boundary, discrete dividends, "
            "vol skew curvature, and mark quality. Model limitations flagged above.".format(facts.residual_pct)
        )
    elif facts.residual_pct > 10.0:
        takeaways.append(
            "**Moderate residual ({:.0f}%)**: Consider American option effects (especially near ex-div), "
            "higher-order Greeks, or data quality gaps.".format(facts.residual_pct)
        )

    # Gamma: rehedge if spot moved large
    if facts.primary_driver == "gamma" or abs(facts.spot_pct) > 3.0:
        takeaways.append(
            "**Gamma dynamics**: Large spot move detected. Rebalance delta hedges and review convexity "
            "exposure before the next trading session."
        )

    # Ex-dividend: early exercise & assignment
    if facts.american.next_ex_div:
        days_hint = " imminently" if "shortly" in facts.american.early_exercise_assessment.lower() else ""
        takeaways.append(
            f"**Ex-dividend window ({facts.american.next_ex_div}){days_hint}**: "
            f"Monitor ITM positions for early-exercise risk. Verify assignment protocols with operations."
        )

    tags = _prompt_layer_b_tags(news or [], findings)
    if "iv crush" in tags and not any("iv crush" in t.lower() or "implied vol" in t.lower() for t in takeaways):
        takeaways.append(
            "**IV crush**: Implied volatility collapsed with the event — monitor post-print vol "
            "and do not treat a Delta-led gap as the whole story."
        )
    if any(tag in tags for tag in ("borrow", "squeeze", "buy-in")):
        takeaways.append(
            "**Borrow / squeeze**: Stress borrow, buy-in, and quote liquidity; the official FDM "
            "path does not model hard-to-borrow."
        )
    if "float" in tags:
        takeaways.append(
            "**Float / liquidity**: Disable continuous-hedging assumptions and haircut marks in a "
            "cornered or squeeze tape."
        )
    if "conversion" in tags:
        takeaways.append(
            "**Conversion / parity**: Update borrow-curve assumptions and stress synthetic-dividend mismatch."
        )

    # Fallback: generic reconciliation
    if not takeaways:
        takeaways.append("Reconcile Greeks vs. book before the next session and confirm mark quality.")

    return DiagnosticSynthesis(
        primary_driver=driver,
        verdict=verdict,
        confidence_level=facts.confidence,
        confidence_rationale=rationale,
        evidence=[],
        takeaways=takeaways[:5],
        american_commentary=_american_commentary_for_facts(facts),
    )


def _news_to_evidence(news: list[NewsItem], driver: str) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for hit in news[:3]:
        pub = hit.publisher or "News"
        items.append(
            EvidenceItem(
                headline=hit.title[:200],
                source=pub,
                relevance=f"Possible context for {driver}; verify against the quant driver.",
            )
        )
    return items


def _should_attach_evidence(findings: dict | None) -> bool:
    return bool((findings or {}).get("observation_reliable", True))


def _digest_from_findings(findings: dict | None) -> IntelDigest:
    payload = (findings or {}).get("intel_digest") or {}
    return IntelDigest.model_validate(payload)


def _digest_ran(findings: dict | None) -> bool:
    return "intel_digest" in (findings or {})


def _layer_b_news(news: list[NewsItem], digest: IntelDigest, findings: dict | None) -> list[NewsItem]:
    """Desk-packet headlines: coarse-kept tape. Digest labels; it does not hide titles."""
    del digest
    if _digest_ran(findings):
        return coarse_kept_news(news)
    return news


def _digest_relevant_news(news: list[NewsItem], digest: IntelDigest) -> list[NewsItem]:
    if not digest.relevant:
        return []
    keep = {(row.title or "").strip().lower() for row in digest.relevant if row.title}
    return [hit for hit in news if hit.title.strip().lower() in keep]


def _catalyst_tags(news: list[NewsItem], findings: dict | None) -> list[str]:
    """Required Layer B tokens come from relevant titles only."""
    if not _digest_ran(findings):
        return with_inferred_microstructure(tags_from_news(news))
    digest = _digest_from_findings(findings)
    if digest.mechanisms:
        return with_inferred_microstructure(digest.mechanisms)
    return with_inferred_microstructure(
        tags_from_news(_digest_relevant_news(news, digest))
    )


def _prompt_layer_b_tags(news: list[NewsItem], findings: dict | None) -> list[str]:
    """Tags the narrator must name — relevant first, else microstructure in the tape.

    When digest.relevant is empty, do not forbid squeeze/float words that already
    appear in coarse-kept blotter headlines. Peer earnings are not promoted.
    """
    from ..report.catalysts import MICROSTRUCTURE_TAGS, tags_from_headlines

    tags = _catalyst_tags(news, findings)
    if tags:
        return tags
    if _digest_ran(findings):
        digest = _digest_from_findings(findings)
        if digest.relevant:
            return []
    present = [
        tag
        for tag in tags_from_headlines([hit.title for hit in news])
        if tag in MICROSTRUCTURE_TAGS
    ]
    return with_inferred_microstructure(present)


_EE_MATERIAL_USD = 0.01


def ee_premium_material(facts: PositionFacts) -> bool:
    prem = facts.american.early_exercise_premium
    if facts.american.ee_premium_anomaly:
        return False
    return prem is not None and prem >= _EE_MATERIAL_USD


def _american_commentary_for_facts(facts: PositionFacts) -> str:
    if not ee_premium_material(facts):
        return ""
    return (
        "Early-exercise premium versus European is material near the ex-div window; "
        "the Taylor blotter does not isolate that American-European gap."
    )


def apply_american_commentary_policy(
    synthesis: DiagnosticSynthesis,
    facts: PositionFacts,
) -> DiagnosticSynthesis:
    """Mention early exercise only when the American-European premium is material."""
    material = ee_premium_material(facts)
    text = (synthesis.american_commentary or "").strip()
    lowered = text.lower()
    ee_tokens = ("early exercise", "early-exercise", "assignment", "ex-div", "ex-dividend")
    mentions_ee = any(tok in lowered for tok in ee_tokens)
    if not material:
        if mentions_ee:
            return synthesis.model_copy(update={"american_commentary": ""})
        return synthesis
    if not mentions_ee:
        return synthesis.model_copy(
            update={"american_commentary": _american_commentary_for_facts(facts)}
        )
    return synthesis


def _evidence_for_synthesis(
    digest: IntelDigest,
    news: list[NewsItem],
    findings: dict | None,
    driver: str,
) -> list[EvidenceItem]:
    if digest.relevant:
        return _digest_to_evidence(digest, driver)
    if _digest_ran(findings):
        return []
    return _news_to_evidence(news, driver)


def _digest_to_evidence(digest: IntelDigest, driver: str) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for row in digest.relevant[:3]:
        source = row.publisher or "News"
        relevance = (row.one_line_fact or "").strip()
        if not relevance:
            relevance = f"Possible context for {driver}; verify against the quant driver."
        items.append(
            EvidenceItem(
                headline=row.title[:200],
                source=source,
                relevance=relevance,
            )
        )
    return items


def synthesize_diagnosis(
    snap: MarketSnapshot,
    pricing: PricingResult,
    news: list[NewsItem],
    *,
    plan: SearchPlan | None = None,
    ports: GraphDeps | None = None,
    diagnostic_findings: dict | None = None,
    role: "LlmRole | None" = None,
) -> DiagnosticSynthesis:
    """Return structured synthesis; falls back on missing key, errors, or validation."""
    facts = build_position_facts(snap, pricing, news_count=len(news))
    findings = diagnostic_findings or {}
    digest = _digest_from_findings(findings)
    layer_b_news = _layer_b_news(news, digest, findings)

    def _finish(syn: DiagnosticSynthesis) -> DiagnosticSynthesis:
        return apply_american_commentary_policy(syn, facts)

    if not os.getenv("OPENAI_API_KEY"):
        syn = fallback_synthesis(
            facts, llm_unavailable=True, diagnostic_findings=findings, news=layer_b_news
        )
        if _should_attach_evidence(findings):
            evidence = _evidence_for_synthesis(digest, layer_b_news, findings, syn.primary_driver)
            syn = syn.model_copy(update={"evidence": evidence})
        return _finish(syn)

    try:
        if ports is not None:
            system = compose_diagnose_system_prompt(
                base=ports.diagnose_system_prompt,
                extra=ports.diagnose_system_extra,
            )
        else:
            system = compose_diagnose_system_prompt(extra=None)

        human = _human_prompt(snap, pricing, facts, layer_b_news, plan, findings)

        if role is not None:
            # Go through the configured role so its model/temperature/seed
            # (Task B3) and token-usage capture (Task B4) actually apply --
            # this used to build its own ChatOpenAI straight from
            # EMO_LLM_MODEL, silently ignoring any role the caller passed
            # (WORK_ORDER_REPORT.md FINDING: real bug, not a naming choice).
            result = role.structured_invoke(system=system, human=human, schema=DiagnosticSynthesis)
        else:
            from langchain_core.messages import HumanMessage, SystemMessage
            from langchain_openai import ChatOpenAI

            model = os.getenv("EMO_LLM_MODEL", _DEFAULT_LLM_MODEL)
            llm = ChatOpenAI(model=model, temperature=0, timeout=45)
            structured = llm.with_structured_output(DiagnosticSynthesis)
            result = structured.invoke(
                [SystemMessage(content=system), HumanMessage(content=human)]
            )
        if not isinstance(result, DiagnosticSynthesis):
            result = DiagnosticSynthesis.model_validate(result)

        errors = validate_synthesis(result)
        if errors:
            syn = fallback_synthesis(
                facts, llm_failed=True, diagnostic_findings=findings, news=layer_b_news
            )
            if _should_attach_evidence(findings):
                evidence = _evidence_for_synthesis(
                    digest, layer_b_news, findings, syn.primary_driver
                )
                syn = syn.model_copy(update={"evidence": evidence})
            return _finish(syn)
        if _should_attach_evidence(findings) and digest.relevant:
            result = result.model_copy(
                update={
                    "evidence": _digest_to_evidence(digest, result.primary_driver),
                }
            )
        return _finish(result)
    except Exception:
        syn = fallback_synthesis(
            facts, llm_failed=True, diagnostic_findings=findings, news=layer_b_news
        )
        if _should_attach_evidence(findings):
            evidence = _evidence_for_synthesis(
                digest, layer_b_news, findings, syn.primary_driver
            )
            syn = syn.model_copy(update={"evidence": evidence})
        return _finish(syn)


def _coverage_band(explained_pct: float) -> str:
    if explained_pct >= 90.0:
        return "high"
    if explained_pct >= 75.0:
        return "medium"
    return "low"


def _residual_band(residual_pct: float) -> str:
    if residual_pct <= 5.0:
        return "low"
    if residual_pct <= 15.0:
        return "medium"
    return "high"


def _spot_move_band(spot_pct: float) -> str:
    """|ΔS/S| band — lets Step 2 of the diagnose prompt spot a Taylor-truncation case."""
    move = abs(spot_pct)
    if move >= 20.0:
        return "extreme"
    if move >= 10.0:
        return "large"
    if move >= 5.0:
        return "moderate"
    return "small"


def _vol_move_band(d_vol_pts: float) -> str:
    """|Δσ| band in vol points — pairs with residual to flag skew/Vanna-Volga cases."""
    move = abs(d_vol_pts)
    if move >= 15.0:
        return "extreme"
    if move >= 8.0:
        return "large"
    if move >= 3.0:
        return "moderate"
    return "small"


def _human_prompt(
    snap: MarketSnapshot,
    pricing: PricingResult,
    facts: PositionFacts,
    news: list[NewsItem],
    plan: SearchPlan | None,
    diagnostic_findings: dict | None = None,
) -> str:
    findings = diagnostic_findings or {}
    digest = _digest_from_findings(findings)
    lines = [
        "Produce DiagnosticSynthesis JSON only.",
        "Use the desk blotter below for reasoning. Do NOT copy dollar amounts, percentages, "
        "or numeric PnL into primary_driver, verdict, confidence_rationale, american_commentary, "
        "evidence.relevance, or takeaways.",
        "Write Layer A first (dominant Taylor driver). News is auxiliary background for "
        "that PnL story, not a replacement. Residual taxonomy is additive — truncation "
        "does not replace named relevant catalysts.",
        "",
        format_desk_packet(snap, pricing, news),
        "",
        "### Diagnostic signals (code-derived bands)",
        f"Dominant quant driver key: {facts.primary_driver}",
        f"Confidence hint (code): {facts.confidence}",
        f"Attribution coverage band (code): {_coverage_band(facts.explained_pct)}",
        f"Residual band (code): {_residual_band(facts.residual_pct)}",
        f"Spot move magnitude band (code): {_spot_move_band(facts.spot_pct)}",
        f"Vol move magnitude band (code): {_vol_move_band(facts.d_vol_pts)}",
        f"Observation reliable (code): {findings.get('observation_reliable', facts.reconciliation.observation_reliable if facts.reconciliation else True)}",
        f"Suppress Vega narrative (code): {findings.get('suppress_vega_narrative', False)}",
        f"Diagnostic tools run (code): {', '.join(findings.get('tools_run', [])) or 'none'}",
    ]
    split = findings.get("ex_div_attribution")
    if isinstance(split, dict) and split.get("flag_ex_div_window"):
        lines.append(
            "Ex-div window (code): true. American-versus-European premium is "
            + ("material" if split.get("ee_premium_material") else "not material")
            + ". Fill american_commentary with early-exercise language only if material; "
            "the dollar split lives in the blotter overlay, not in your prose."
        )
    tags = _prompt_layer_b_tags(news, findings)
    lines.extend(
        [
            "",
            "### Layer B — intel digest (labels; all kept headlines are in the blotter)",
        ]
    )
    # B1.1: headline text (and the digester's own brief, itself derived from
    # untrusted headlines) is external content, delimited here too.
    _src_idx = 0
    if digest.brief:
        _src_idx += 1
        lines.append(
            "Digest brief: " + format_untrusted_source(digest.brief, idx=_src_idx, origin="digester")
        )
    if digest.reason:
        lines.append(f"Digest note: {digest.reason}")
    if digest.relevant:
        _src_idx += 1
        lines.append(
            "Relevant (subject / related issuer): "
            + format_untrusted_source(
                "; ".join(row.title for row in digest.relevant if row.title),
                idx=_src_idx,
                origin="digester:relevant",
            )
        )
    if digest.background:
        _src_idx += 1
        lines.append(
            "Background (peer/sector; context only, not required Layer B): "
            + format_untrusted_source(
                "; ".join(row.title for row in digest.background if row.title),
                idx=_src_idx,
                origin="digester:background",
            )
        )
    if digest.discarded:
        _src_idx += 1
        lines.append(
            "Discarded: "
            + format_untrusted_source(
                "; ".join(
                    f"{row.title} ({row.reason})" for row in digest.discarded if row.title
                ),
                idx=_src_idx,
                origin="digester:discarded",
            )
        )
    if tags:
        lines.append("Present in relevant headlines / desk-inferable tape: " + "; ".join(tags))
        lines.append(
            "Name every listed tag in verdict AND in at least one takeaway. "
            "Truncation explains residual size; it does not replace these mechanisms. "
            "Squeeze / collapsed free float imply unmodeled borrow or squeeze stress "
            "(FDM does not model HTB or cornered float) — use those words, never fee numbers. "
            "Peer/background headlines may be mentioned as context only."
        )
    else:
        lines.append(
            "No named microstructure tokens in relevant or blotter headlines — do not invent "
            "a squeeze, borrow, or IV-crush story from peer/background tape or training memory. "
            "Words already in the blotter titles may be used."
        )
    challenge = findings.get("catalyst_challenge") or {}
    if challenge:
        lines.extend(
            [
                "",
                "### Independent catalyst critic (address this brief)",
                f"Layer B required: {challenge.get('layer_b_required')}",
                f"Mechanisms: {', '.join(challenge.get('mechanisms') or []) or 'none'}",
                f"Rationale: {challenge.get('rationale', '')}",
            ]
        )
        if challenge.get("suppress_reason"):
            lines.append(f"Suppress reason: {challenge['suppress_reason']}")
        lines.append(
            "If Layer B is required, those mechanisms must appear in verdict and takeaways. "
            "If you reject the critic, explain why in confidence_rationale (no numbers)."
        )
    if findings.get("terminal_unexplained_break"):
        lines.append("Terminal unexplained break (code): true — escalate in watchlist.")
    if plan is not None:
        lines.append("")
        lines.append("### Search plan notes")
        for note in plan.honesty_notes():
            lines.append(f"- [{note}]")
    return "\n".join(lines)


def synthesis_to_legacy_diagnosis(synthesis: DiagnosticSynthesis) -> str:
    """Short string for OptionState['diagnosis'] backward compatibility."""
    return synthesis.verdict.strip()
