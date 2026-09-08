"""Reject numeric hallucinations in LLM narrative fields."""

from __future__ import annotations

import re

from .schema import DiagnosticSynthesis

# Dollar amounts and bare percentages are forbidden in LLM-*authored* prose —
# numbers belong only in the code-rendered quant sections, never as the
# model's own claim about this report's PnL.
#
# `evidence.headline` / `evidence.source` are exempt: the system prompt tells
# the LLM to quote real news hits close to verbatim ("do NOT invent
# headlines"), so a number there is a fact about the world (e.g. "stock down
# 26%" from a real headline) rather than a number the model asserted about
# this report's attribution. `evidence.relevance` is the LLM's own sentence
# and stays checked.
_DOLLAR = re.compile(r"\$\s*[\d,]+(?:\.\d+)?")
_PERCENT = re.compile(r"(?<!\w)[+-]?\d+(?:\.\d+)?\s*%")
_PNL_CLAIM = re.compile(
    r"\b(pnl|profit|loss|gained|lost|rose|fell|up|down)\s+[\d$]",
    re.IGNORECASE,
)


def validate_synthesis(synthesis: DiagnosticSynthesis) -> list[str]:
    """Return validation errors; empty list means safe to render."""
    errors: list[str] = []
    narrative_texts = [
        synthesis.primary_driver,
        synthesis.verdict,
        synthesis.confidence_rationale,
        synthesis.american_commentary,
        *[e.relevance for e in synthesis.evidence],
        *synthesis.takeaways,
    ]
    for text in narrative_texts:
        if not text:
            continue
        if _DOLLAR.search(text):
            errors.append("LLM prose must not contain dollar amounts.")
        if _PERCENT.search(text):
            errors.append("LLM prose must not contain percentage literals.")
        if _PNL_CLAIM.search(text):
            errors.append("LLM prose must not embed numeric PnL claims.")
    return list(dict.fromkeys(errors))
