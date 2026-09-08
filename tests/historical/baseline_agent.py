"""Single-shot baseline agent for benchmark comparison (test-only).

The baseline receives the **same desk blotter** the governed workflow uses
(Greeks, factor PnL, residual, headlines) and writes ``DiagnosticSynthesis``
in one LLM call. Quant sections in the final report still come from the engine
via ``render_position_report`` — only the narrative layer differs.

    python tests/historical/compare.py --case vow_float_squeeze_2008
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Literal

from explain_my_option.data_loader import NewsItem
from explain_my_option.pricing.types import MarketSnapshot, PricingResult
from explain_my_option.report.desk_packet import format_desk_packet
from explain_my_option.report.facts import PositionFacts, build_position_facts
from explain_my_option.report.schema import DiagnosticSynthesis
from explain_my_option.report.synthesis import fallback_synthesis
from explain_my_option.report.template import render_position_report
from explain_my_option.report.validate import validate_synthesis

BaselinePrompt = Literal["simple", "cot"]

_DEFAULT_LLM_MODEL = "gpt-4o-mini"

BASELINE_SYSTEM_SIMPLE = """You are a derivatives desk analyst diagnosing a one-day option move.

You receive the full desk blotter: contract, market moves, T-1 Greeks, factor PnL
attribution (Delta / Gamma / Vega / Theta), residual, and news headlines.

Produce DiagnosticSynthesis JSON only. Explain the dominant driver and whether the
residual is economically meaningful (model gap, American effects, skew, bad marks).

Rules:
- Do NOT put dollar amounts, percentages, or numeric PnL claims in primary_driver,
  verdict, confidence_rationale, american_commentary, evidence.relevance, or takeaways.
- Numbers may appear only when quoting a news headline verbatim in evidence.headline.
- If residual is large, say so explicitly — do not force all PnL into Delta/Vega stories.
- confidence_level must be high, medium, or low.
"""

BASELINE_SYSTEM_COT = BASELINE_SYSTEM_SIMPLE + """

Before filling JSON fields, reason through:
1) Which factor PnL row dominates?
2) Is Taylor residual large relative to total model PnL?
3) Which headline (if any) supports the mechanism without inventing facts?
"""


@dataclass
class BaselineRunResult:
    synthesis: DiagnosticSynthesis
    report: str
    facts: PositionFacts
    desk_packet: str
    prompt_variant: BaselinePrompt
    validation_errors: list[str]
    used_fallback: bool
    latency_s: float
    token_usage: dict[str, int] = field(default_factory=dict)


def _system_prompt(variant: BaselinePrompt) -> str:
    if variant == "cot":
        return BASELINE_SYSTEM_COT
    return BASELINE_SYSTEM_SIMPLE


def run_baseline_diagnosis(
    snap: MarketSnapshot,
    pricing: PricingResult,
    news: list[NewsItem],
    *,
    prompt_variant: BaselinePrompt = "simple",
    case_context: str | None = None,
    require_llm: bool = False,
) -> BaselineRunResult:
    """Single LLM call: desk packet in, structured synthesis out, same report template."""
    facts = build_position_facts(snap, pricing, news_count=len(news))
    desk_packet = format_desk_packet(
        snap, pricing, news, desk_color=case_context
    )
    t0 = time.perf_counter()
    token_usage: dict[str, int] = {}
    validation_errors: list[str] = []
    used_fallback = False

    if not os.getenv("OPENAI_API_KEY"):
        if require_llm:
            raise RuntimeError(
                "OPENAI_API_KEY is required for live benchmark baseline runs."
            )
        synthesis = fallback_synthesis(facts, llm_unavailable=True)
        used_fallback = True
    else:
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            from langchain_openai import ChatOpenAI

            model = os.getenv("EMO_LLM_MODEL", _DEFAULT_LLM_MODEL)
            llm = ChatOpenAI(model=model, temperature=0, timeout=60)
            structured = llm.with_structured_output(DiagnosticSynthesis)
            human = (
                "Write DiagnosticSynthesis for this desk blotter.\n\n"
                f"{desk_packet}"
            )
            result = structured.invoke(
                [
                    SystemMessage(content=_system_prompt(prompt_variant)),
                    HumanMessage(content=human),
                ]
            )
            if not isinstance(result, DiagnosticSynthesis):
                result = DiagnosticSynthesis.model_validate(result)
            synthesis = result
            meta = getattr(result, "response_metadata", None) or {}
            usage = meta.get("token_usage") or {}
            if usage:
                token_usage = {
                    "prompt_tokens": int(usage.get("prompt_tokens", 0)),
                    "completion_tokens": int(usage.get("completion_tokens", 0)),
                    "total_tokens": int(usage.get("total_tokens", 0)),
                }
            validation_errors = validate_synthesis(synthesis)
            if validation_errors:
                synthesis = fallback_synthesis(facts, llm_failed=True)
                used_fallback = True
        except Exception:
            synthesis = fallback_synthesis(facts, llm_failed=True)
            used_fallback = True

    report = render_position_report(facts, synthesis, news=news)
    latency_s = time.perf_counter() - t0
    return BaselineRunResult(
        synthesis=synthesis,
        report=report,
        facts=facts,
        desk_packet=desk_packet,
        prompt_variant=prompt_variant,
        validation_errors=validation_errors,
        used_fallback=used_fallback,
        latency_s=latency_s,
        token_usage=token_usage,
    )


def score_narrative(
    synthesis: DiagnosticSynthesis,
    *,
    keywords: list[str],
    residual_pct: float,
    residual_threshold: float = 15.0,
) -> dict[str, Any]:
    """Code-based scores for resume / notebook tables."""
    text = " ".join(
        [
            synthesis.primary_driver,
            synthesis.verdict,
            synthesis.confidence_rationale,
            synthesis.american_commentary,
            " ".join(synthesis.takeaways),
            " ".join(e.relevance for e in synthesis.evidence),
        ]
    ).lower()
    hits = [kw for kw in keywords if kw.lower() in text]
    residual_terms = ("residual", "model gap", "unexplained", "truncation", "convexity")
    mentions_residual = any(t in text for t in residual_terms)
    return {
        "keyword_hits": len(hits),
        "keyword_total": len(keywords),
        "keywords_matched": hits,
        "keywords_missing": [kw for kw in keywords if kw.lower() not in text],
        "mentions_residual": mentions_residual,
        "residual_ack_required": residual_pct >= residual_threshold,
        "residual_ack_pass": (not (residual_pct >= residual_threshold)) or mentions_residual,
    }
