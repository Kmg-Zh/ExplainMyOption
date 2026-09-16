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


def _narrative_texts(synthesis: DiagnosticSynthesis) -> list[str]:
    return [
        synthesis.primary_driver,
        synthesis.verdict,
        synthesis.confidence_rationale,
        synthesis.american_commentary,
        *[e.relevance for e in synthesis.evidence],
        *synthesis.takeaways,
    ]


def validate_synthesis(synthesis: DiagnosticSynthesis) -> list[str]:
    """Return validation errors; empty list means safe to render."""
    errors: list[str] = []
    for text in _narrative_texts(synthesis):
        if not text:
            continue
        if _DOLLAR.search(text):
            errors.append("LLM prose must not contain dollar amounts.")
        if _PERCENT.search(text):
            errors.append("LLM prose must not contain percentage literals.")
        if _PNL_CLAIM.search(text):
            errors.append("LLM prose must not embed numeric PnL claims.")
    return list(dict.fromkeys(errors))


# A9.4: the borrow field (A9.3) makes "opportunity"/"mispricing"/
# "arbitrage"/"free money" newly likely -- a real elevated/extreme
# q_implied is easy to misdescribe as a tradeable edge instead of a cost
# now inside the model. "riskless", "should have", "cheap", "rich" are the
# project's pre-existing red line (no trade advice, no "should have
# exercised") made explicit and enforced, not new ground.
PROHIBITED_TRADE_ADVICE_PHRASES: tuple[str, ...] = (
    "arbitrage",
    "mispricing",
    "mispriced",
    "free money",
    "riskless",
    "opportunity",
    "should have",
    "cheap",
    "rich",
)
_PROHIBITED_PHRASE_RE = re.compile(
    r"\b(" + "|".join(re.escape(p) for p in PROHIBITED_TRADE_ADVICE_PHRASES) + r")\b",
    re.IGNORECASE,
)


def find_prohibited_phrases(synthesis: DiagnosticSynthesis) -> list[str]:
    """A9.4: trade-advice-adjacent language, distinct from numeric
    hallucination (validate_synthesis) -- no dollar figure is involved."""
    hits: list[str] = []
    for text in _narrative_texts(synthesis):
        if not text:
            continue
        hits.extend(m.group(1).lower() for m in _PROHIBITED_PHRASE_RE.finditer(text))
    return list(dict.fromkeys(hits))
