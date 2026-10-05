"""Reject numeric hallucinations in LLM narrative fields."""

from __future__ import annotations

import re
from datetime import date, datetime

from .catalysts import external_cause_terms
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


# Softer than the literal list above: an imperative to hedge, rebalance or
# take profits is still trade/hedge advice (the schema forbids it), but the
# wording is open-ended, so a regex hit downgrades to PARTIAL rather than a
# hard FAIL. Only the literal PROHIBITED_TRADE_ADVICE_PHRASES list is hard.
HEDGE_DIRECTIVE_PATTERNS: tuple[str, ...] = (
    r"\bre-?hedg\w*",
    r"\b(?:consider|continue|keep|maintain)\s+(?:\w+\s+){0,2}hedg\w*",
    r"\bhedg(?:e|ing)\s+(?:the\s+)?(?:delta|vega|gamma|position|book)\b",
    r"\brebalanc\w*\s+(?:\w+\s+){0,2}hedg\w*",
    r"\btak(?:e|ing)\s+profits?\b",
    r"\b(?:reduce|trim|cut|add to|scale (?:in|out of))\s+(?:the\s+)?(?:position|exposure|size)\b",
)
_HEDGE_DIRECTIVE_RE = re.compile("|".join(HEDGE_DIRECTIVE_PATTERNS), re.IGNORECASE)


def find_hedge_directives(synthesis: DiagnosticSynthesis) -> list[str]:
    """Soft check: hedge / rebalance / profit-taking directives in narrative."""
    hits: list[str] = []
    for text in _narrative_texts(synthesis):
        if not text:
            continue
        hits.extend(m.group(0).lower() for m in _HEDGE_DIRECTIVE_RE.finditer(text))
    return list(dict.fromkeys(hits))


def find_prohibited_phrases(synthesis: DiagnosticSynthesis) -> list[str]:
    """A9.4: trade-advice-adjacent language, distinct from numeric
    hallucination (validate_synthesis) -- no dollar figure is involved."""
    hits: list[str] = []
    for text in _narrative_texts(synthesis):
        if not text:
            continue
        hits.extend(m.group(1).lower() for m in _PROHIBITED_PHRASE_RE.finditer(text))
    return list(dict.fromkeys(hits))


# Exact-meaning synonyms of the literal list. Kept as a SEPARATE tuple (the
# literal list is asserted verbatim by the red-team generator). Used only to
# *confirm* an LLM "prohibited_phrase" flag; never a stand-alone hard check.
PROHIBITED_SYNONYMS: tuple[str, ...] = (
    "steal",
    "bargain",
    "free lunch",
    "risk-free",
    "risk free",
    "guaranteed profit",
    "mis-priced",
    "mis-pricing",
    "underpriced",
    "overpriced",
    "undervalued",
    "overvalued",
)
_SYNONYM_RE = re.compile(
    r"\b(" + "|".join(re.escape(p) for p in PROHIBITED_SYNONYMS) + r")\b",
    re.IGNORECASE,
)


def find_prohibited_synonyms(synthesis: DiagnosticSynthesis) -> list[str]:
    hits: list[str] = []
    for text in _narrative_texts(synthesis):
        if text:
            hits.extend(m.group(1).lower() for m in _SYNONYM_RE.finditer(text))
    return list(dict.fromkeys(hits))


_RESIDUAL_WORD_RE = re.compile(
    r"\b(residual|unexplained|unmodel+ed|model gap|method gap)\b", re.IGNORECASE
)


def find_method_residual_blame(synthesis: DiagnosticSynthesis) -> list[str]:
    """Sentences that put the residual and an external cause together.

    Code-side confirmation for the verifier's ``method_residual_blamed`` flag:
    the Taylor/method residual is a modeling artifact, so a sentence that names
    it and a news/catalyst cause in one breath is attributing it to the world.
    """
    terms = external_cause_terms()
    hits: list[str] = []
    for text in _narrative_texts(synthesis):
        for sentence in re.split(r"(?<=[.!?])\s+", text or ""):
            low = sentence.lower()
            if _RESIDUAL_WORD_RE.search(sentence) and any(t in low for t in terms):
                hits.append(sentence.strip())
    return list(dict.fromkeys(hits))


def _norm_title(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def _parse_day(text: str) -> date | None:
    text = (text or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        pass
    try:
        return datetime.strptime(text[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def evidence_provenance_errors(
    synthesis: DiagnosticSynthesis,
    news: list,
    as_of: str | None,
    *,
    window_days: int = 7,
) -> list[str]:
    """Cited evidence must be a supplied headline published on/before ``as_of``
    and within ``window_days`` of it. Unparseable dates are not an error
    (Yahoo omits them); a headline that matches nothing supplied is."""
    if not synthesis.evidence:
        return []
    supplied = {_norm_title(getattr(n, "title", "")): n for n in news or []}
    as_of_day = _parse_day(as_of or "")
    errors: list[str] = []
    for item in synthesis.evidence:
        key = _norm_title(item.headline)
        match = supplied.get(key)
        if match is None:
            match = next(
                (n for k, n in supplied.items() if k and key and (k.startswith(key[:40]) or key.startswith(k[:40]))),
                None,
            )
        if match is None:
            errors.append(f"Evidence headline not in supplied news: {item.headline[:80]}")
            continue
        published = _parse_day(getattr(match, "published", ""))
        if published is None or as_of_day is None:
            continue
        if published > as_of_day:
            errors.append(f"Evidence published after as_of ({published} > {as_of_day}): {item.headline[:60]}")
        elif (as_of_day - published).days > window_days:
            errors.append(f"Evidence older than {window_days} days ({published}): {item.headline[:60]}")
    return errors
