"""Independent verifier gate for diagnostic synthesis."""

from __future__ import annotations

import re

from ..data_loader import UNTRUSTED_SOURCE_INSTRUCTION, format_untrusted_source
from ..report.catalysts import external_cause_terms, missing_catalyst_tags, tags_from_headlines
from ..report.facts import PositionFacts
from ..report.schema import DiagnosticSynthesis
from ..report.validate import (
    evidence_provenance_errors,
    find_bare_figures,
    find_hedge_directives,
    find_method_residual_blame,
    find_prohibited_phrases,
    find_prohibited_synonyms,
    validate_synthesis,
)
from .llm_roles import LlmRole
from .verifier_schema import DiagnosticVerifierResult, GuardedVerifierResult

VERIFIER_SYSTEM_PROMPT = """You are an independent diagnostic verifier for an options PnL explain report.
Judge whether the synthesis candidate is supported by quant facts and evidence metadata.

The narrator must cover TWO layers when evidence exists:
- Layer A: dominant Taylor driver from the code (modeled factor only).
- Layer B: named catalysts in the supplied headlines (IV crush, borrow, squeeze, float,
  buy-in, earnings, ex-div, conversion). Residual truncation is additive — it does not
  replace Layer B. An independent catalyst critic may have required Layer B mechanisms;
  omitting those is PARTIAL, not FAIL.

Two residuals (Task A6.4): the method residual is the part of the model's own price change not
captured by the chosen Greek decomposition -- arithmetic, not news. Only the model residual --
the gap between the market's price change and the model's -- may be discussed in terms of
events. A synthesis that attributes the method residual to any external cause (a headline, an
event, "the market reacted to...") is a hard FAIL, flagged "method_residual_blamed" --
regardless of whether the cited catalyst is otherwise real and well-evidenced.

NOT a violation of this rule: describing the method residual with model/math vocabulary --
"higher-order effects", "convexity", "path effects", "full reprice", "Taylor truncation",
"quote noise", "mark noise", "model gap", or similar. That vocabulary describes how the model's
own decomposition falls short of the model's own price, which is exactly what the method
residual is -- it is the correct, expected way to talk about it, not a violation. Only flag
method_residual_blamed when the residual is tied to something happening outside the model: a
headline, a news event, an earnings print, "the market reacted to...", a named catalyst. If the
cited cause is the model's own arithmetic, curvature, or numerical behavior, that is not
method_residual_blamed no matter how the sentence is phrased.

Quiet days (Task A7.5), the symmetric rule: on a run whose terminal state is no_escalation
("nothing to explain" -- carry and a small spot move only, no search was performed), a
synthesis that names a catalyst, an event, or any external cause is a hard FAIL, flagged
"quiet_day_confabulation". There is no news evidence on a no_escalation run by construction, so
any such claim is fabricated by definition, not merely unsupported.

Trade-advice language (Task A9.4): the implied-borrow field (A9.3) makes "opportunity",
"mispricing" and "arbitrage" newly tempting -- an elevated/extreme q_implied is a cost now
inside the model, not a tradeable edge. Any of these words, or "free money", "riskless",
"cheap", "rich", "should have" (as in "should have exercised"), anywhere in narrative fields is
a hard FAIL, flagged "prohibited_phrase" -- this product explains a price move, it never
advises a trade, regardless of how well-evidenced the rest of the synthesis is.

Flag "prohibited_phrase" ONLY when one of those exact listed words/phrases (or an unambiguous
synonym carrying the identical meaning, e.g. "steal" for "cheap") is literally present in a
narrative field -- the same narrow rule the code's own deterministic check enforces
(report/validate.py's find_prohibited_phrases). Hedge, rebalance, sizing or
profit-taking directives ("continue standard hedging", "rebalance delta hedges", "take
profits") are also out of scope for this product, but they are NOT this flag: report them as
PARTIAL (code also checks them), never a hard FAIL. Neutral monitoring language ("monitor the
position", "watch for further moves", "review before the next print") is fine. If you cannot point to the specific listed word (or its
exact synonym) actually present in the text, it is not a "prohibited_phrase" violation --
regardless of how "advisory" the tone feels. If a borderline case still concerns you, use
PARTIAL, never a hard FAIL on resemblance alone.

Verdict policy:
- PASS: Layer A matches the dominant driver, Layer B is covered when headlines name a
  mechanism, and observation locks are respected.
- PARTIAL (preferred over FAIL when unsure): evidence is thin, quote quality is weak, IV sits
  inside the noise band, OR headlines name a catalyst that verdict/takeaways omit.
  Use PARTIAL instead of FAIL for "cannot prove" and "missing catalyst layer" situations.
- FAIL (hard violations only): numeric hallucination in narrative fields, the method residual
  attributed to an external cause (flag "method_residual_blamed"), a catalyst claim on a
  no_escalation run (flag "quiet_day_confabulation"), or trade-advice language anywhere
  (flag "prohibited_phrase").

Do not invent numbers or prices.

""" + UNTRUSTED_SOURCE_INSTRUCTION

HARD_FAIL_POLICY_FLAGS = frozenset(
    {
        "numeric_hallucination",
        "method_residual_blamed",
        "quiet_day_confabulation",
        "prohibited_phrase",
    }
)


def _quiet_day_catalyst_tags(synthesis: DiagnosticSynthesis) -> list[str]:
    """A7.5: catalyst/event language in a synthesis, reusing the same
    headline-mechanism vocabulary the narrator/verifier already use for
    news -- applied here to the synthesis's own text instead."""
    narrative = [synthesis.verdict, synthesis.confidence_rationale, *synthesis.takeaways]
    return tags_from_headlines(narrative)


def _quiet_day_rationale() -> str:
    return (
        "There is no news evidence on a no_escalation run by construction; "
        "any catalyst claim is fabricated."
    )


def _observation_lock_rationale() -> str:
    return (
        "Direction may be OK, but quote quality limits falsifiability; "
        "treat factor attribution as indicative."
    )


def _missing_catalyst_rationale() -> str:
    return (
        "Layer B omitted mechanisms present in headlines; residual truncation "
        "does not replace those catalysts."
    )


def _prohibited_phrase_rationale() -> str:
    return (
        "Trade-advice-adjacent language (arbitrage/mispricing/opportunity/riskless/"
        "cheap/rich/'should have') is out of scope regardless of context -- this "
        "product explains a price move, it does not advise a trade."
    )


def _evidence_provenance_rationale() -> str:
    return (
        "Cited evidence is not a supplied headline published on or before as_of "
        "within the look-back window."
    )


def _hedge_advice_rationale() -> str:
    return (
        "Hedge, rebalance or profit-taking directive in the narrative -- this "
        "product explains a price move and gives no hedge or sizing advice."
    )


# A9.1: the fixed set of rationale strings deterministic_precheck can return
# -- code-authored sentences, never the LLM's own prose. Lets a caller with
# only the returned DiagnosticVerifierResult (not a bool from this module)
# tell a deterministic precheck apart from an actual LLM verdict, e.g. to
# count llm_calls accurately without changing verify_synthesis's return
# type for its two call sites.
DETERMINISTIC_PRECHECK_RATIONALES = frozenset(
    {
        "validate_synthesis failed",
        _prohibited_phrase_rationale(),
        _hedge_advice_rationale(),
        _evidence_provenance_rationale(),
        _quiet_day_rationale(),
        "Vega story not falsifiable from quote",
        _observation_lock_rationale(),
        _missing_catalyst_rationale(),
    }
)


def deterministic_precheck(
    synthesis: DiagnosticSynthesis,
    facts: PositionFacts,
    *,
    suppress_vega: bool,
    observation_reliable: bool,
    news_titles: list[str] | None = None,
    no_escalation: bool = False,
    news: list | None = None,
    as_of: str | None = None,
) -> DiagnosticVerifierResult | None:
    errors = validate_synthesis(synthesis)
    if errors:
        return DiagnosticVerifierResult(
            verdict="FAIL",
            missing_evidence=errors,
            policy_flags=["numeric_hallucination"],
            rationale="validate_synthesis failed",
        )
    phrases = find_prohibited_phrases(synthesis)
    if phrases:
        return DiagnosticVerifierResult(
            verdict="FAIL",
            missing_evidence=[f"Prohibited trade-advice phrase: {p}" for p in phrases],
            policy_flags=["prohibited_phrase"],
            rationale=_prohibited_phrase_rationale(),
        )
    if no_escalation:
        tags = _quiet_day_catalyst_tags(synthesis)
        if tags or synthesis.evidence:
            return DiagnosticVerifierResult(
                verdict="FAIL",
                missing_evidence=[
                    f"Catalyst claim on a no_escalation run: {tags or 'evidence cited'}"
                ],
                policy_flags=["quiet_day_confabulation"],
                rationale=_quiet_day_rationale(),
            )
    if news is not None:
        provenance = evidence_provenance_errors(synthesis, news, as_of)
        if provenance:
            return DiagnosticVerifierResult(
                verdict="PARTIAL",
                missing_evidence=provenance,
                policy_flags=["evidence_provenance"],
                rationale=_evidence_provenance_rationale(),
            )
    directives = find_hedge_directives(synthesis)
    if directives:
        return DiagnosticVerifierResult(
            verdict="PARTIAL",
            missing_evidence=[f"Hedge/sizing directive in narrative: {d}" for d in directives],
            policy_flags=["hedge_advice"],
            rationale=_hedge_advice_rationale(),
        )
    driver_lower = synthesis.primary_driver.lower()
    if suppress_vega and "vega" in driver_lower:
        return DiagnosticVerifierResult(
            verdict="PARTIAL",
            missing_evidence=["Vega narrative suppressed by quote noise band"],
            policy_flags=["suppress_vega_narrative"],
            rationale="Vega story not falsifiable from quote",
        )
    if not observation_reliable:
        return DiagnosticVerifierResult(
            verdict="PARTIAL",
            missing_evidence=["Observation lock — quote tier or IV noise band"],
            policy_flags=["observation_soft_lock"],
            rationale=_observation_lock_rationale(),
        )

    titles = list(news_titles or [])
    narrative = " ".join(
        [
            synthesis.primary_driver,
            synthesis.verdict,
            synthesis.confidence_rationale,
            " ".join(synthesis.takeaways or []),
        ]
    )
    missing = missing_catalyst_tags(narrative, titles)
    if suppress_vega:
        missing = [tag for tag in missing if tag != "iv crush"]
    if missing:
        return DiagnosticVerifierResult(
            verdict="PARTIAL",
            missing_evidence=[f"Headline catalyst not used in narrative: {tag}" for tag in missing],
            policy_flags=["missing_catalyst_layer"],
            rationale=_missing_catalyst_rationale(),
        )
    return None


def is_hard_verifier_fail(verdict: DiagnosticVerifierResult) -> bool:
    """True only for policy violations that should escalate to terminal break."""
    flags = set(verdict.policy_flags or [])
    if flags & HARD_FAIL_POLICY_FLAGS:
        return True
    return False


def apply_verifier_reflection(
    synthesis: DiagnosticSynthesis,
    verdict: DiagnosticVerifierResult,
    *,
    observation_reliable: bool,
) -> DiagnosticSynthesis:
    """Merge verifier caveats into synthesis without terminal FAIL wording."""
    rationale = str(verdict.rationale or "").strip()
    missing = list(verdict.missing_evidence or [])
    reflect_bits: list[str] = []
    if not observation_reliable:
        reflect_bits.append(
            "Quote/IV observation lock limits how strongly we can attribute "
            "this move to a single Greek."
        )
    if rationale:
        first = rationale.split(". ")[0].strip()
        reflect_bits.append(first if len(first) <= 200 else first[:199].rstrip() + "…")
    if missing:
        reflect_bits.append(f"Gaps: {'; '.join(missing[:3])}")
    reflect_text = " ".join(reflect_bits) or (
        "Evidence thin — treat narrative as directional only."
    )

    original = synthesis.verdict.strip()
    lowered = original.lower()
    if lowered.startswith("reflect (partial):"):
        new_verdict = original
    else:
        new_verdict = f"Reflect (PARTIAL): {original} Caveats: {reflect_text}"

    confidence = synthesis.confidence_level
    if not observation_reliable:
        if confidence == "high":
            confidence = "medium"
        elif confidence == "medium":
            confidence = "low"

    takeaways = list(synthesis.takeaways)
    caveat = f"**Verifier reflect**: {reflect_text[:240]}"
    if not takeaways or takeaways[0] != caveat:
        takeaways.insert(0, caveat)

    return synthesis.model_copy(
        update={
            "verdict": new_verdict,
            "confidence_level": confidence,
            "takeaways": takeaways,
        }
    )


def _names_external_cause(synthesis: DiagnosticSynthesis) -> bool:
    text = " ".join(
        [synthesis.verdict, synthesis.confidence_rationale, *synthesis.takeaways]
    ).lower()
    return any(term in text for term in external_cause_terms())


def _confirmed_hard_flags(
    flags: set[str], synthesis: DiagnosticSynthesis, *, no_escalation: bool
) -> set[str]:
    """Hard flags that a deterministic code check can reproduce from the text."""
    confirmed: set[str] = set()
    if "numeric_hallucination" in flags and (
        validate_synthesis(synthesis) or find_bare_figures(synthesis)
    ):
        confirmed.add("numeric_hallucination")
    if "prohibited_phrase" in flags and (
        find_prohibited_phrases(synthesis) or find_prohibited_synonyms(synthesis)
    ):
        confirmed.add("prohibited_phrase")
    if (
        "quiet_day_confabulation" in flags
        and no_escalation
        and (
            _quiet_day_catalyst_tags(synthesis)
            or synthesis.evidence
            or _names_external_cause(synthesis)
        )
    ):
        confirmed.add("quiet_day_confabulation")
    if "method_residual_blamed" in flags and find_method_residual_blame(synthesis):
        confirmed.add("method_residual_blamed")
    return confirmed


def _confirm_hard_flags(
    result: GuardedVerifierResult,
    synthesis: DiagnosticSynthesis,
    *,
    no_escalation: bool,
) -> GuardedVerifierResult:
    """An LLM hard FAIL stays hard only if code can confirm the violation.

    escalate/abstain is decided by code, not by the model: a hard flag the code
    cannot reproduce downgrades FAIL to PARTIAL (flag ``unconfirmed_hard_flag``),
    keeping the LLM's verdict and flags in ``llm_verdict`` / ``llm_policy_flags``.
    """
    flags = set(result.policy_flags or [])
    hard = flags & HARD_FAIL_POLICY_FLAGS
    if result.verdict != "FAIL" or not hard:
        return result
    confirmed = _confirmed_hard_flags(hard, synthesis, no_escalation=no_escalation)
    if confirmed:
        kept = [f for f in result.policy_flags if f not in hard or f in confirmed]
        return result.model_copy(update={"policy_flags": kept})
    soft = [f for f in result.policy_flags if f not in hard]
    note = (
        "LLM raised hard flag(s) "
        f"{sorted(hard)} that code could not confirm; downgraded to PARTIAL"
    )
    return result.model_copy(
        update={
            "verdict": "PARTIAL",
            "policy_flags": [*soft, "unconfirmed_hard_flag"],
            "missing_evidence": [*result.missing_evidence, note],
            "llm_verdict": "FAIL",
            "llm_policy_flags": list(result.policy_flags),
        }
    )


_FLAG_DESCRIPTIONS = {
    "numeric_hallucination": "the narrative states a number the code did not produce",
    "method_residual_blamed": "the narrative blames the model residual on an outside cause",
    "quiet_day_confabulation": "the narrative names a catalyst on a day with nothing to explain",
    "prohibited_phrase": "the narrative uses prohibited trade-advice language",
}
_FLAG_KEYWORDS = {
    "numeric_hallucination": ("number", "figure", "dollar", "percent", "numeric"),
    "method_residual_blamed": ("residual", "method", "gap"),
    "quiet_day_confabulation": ("quiet", "catalyst", "fabricat", "no news"),
    "prohibited_phrase": ("phrase", "advice", "arbitrage", "mispric", "opportunity"),
}


def violation_sentence(result: DiagnosticVerifierResult) -> str:
    """The sentence of the verifier rationale that names the violation.

    Replaces "first sentence of the rationale", which was usually a concession
    ("The narrative is mostly right, but ...") and hid the actual reason.
    """
    flags = [f for f in (result.policy_flags or []) if f in _FLAG_DESCRIPTIONS]
    keywords = tuple(k for f in flags for k in _FLAG_KEYWORDS[f])
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", result.rationale or "") if s.strip()]
    for sentence in sentences:
        if keywords and any(k in sentence.lower() for k in keywords):
            return sentence if len(sentence) <= 240 else sentence[:239].rstrip() + "…"
    if flags:
        return "; ".join(_FLAG_DESCRIPTIONS[f] for f in flags).capitalize() + "."
    return sentences[0] if sentences else ""


def verify_synthesis(
    synthesis: DiagnosticSynthesis,
    facts: PositionFacts,
    *,
    role: LlmRole,
    suppress_vega: bool,
    observation_reliable: bool,
    news_titles: list[str],
    catalyst_challenge: dict | None = None,
    no_escalation: bool = False,
    news: list | None = None,
    as_of: str | None = None,
) -> DiagnosticVerifierResult:
    pre = deterministic_precheck(
        synthesis,
        facts,
        suppress_vega=suppress_vega,
        observation_reliable=observation_reliable,
        news_titles=news_titles,
        no_escalation=no_escalation,
        news=news,
        as_of=as_of,
    )
    if pre is not None:
        return pre

    human = (
        f"Dominant driver (code): {facts.primary_driver}\n"
        f"Observation reliable: {observation_reliable}\n"
        f"Suppress Vega: {suppress_vega}\n"
        f"Residual band: {facts.residual_pct:.1f}%\n"
        f"Candidate primary_driver: {synthesis.primary_driver}\n"
        f"Candidate verdict: {synthesis.verdict}\n"
        f"Candidate takeaways: {synthesis.takeaways}\n"
        f"Evidence count: {len(synthesis.evidence)}\n"
        "News titles: "
        + format_untrusted_source("; ".join(news_titles[:3]) or "none", idx=1, origin="news_titles")
        + "\n"
        f"Headline mechanisms present in titles: {tags_from_headlines(news_titles) or 'none'}\n"
        f"Independent critic Layer B required: {(catalyst_challenge or {}).get('layer_b_required')}\n"
        f"Independent critic mechanisms: {(catalyst_challenge or {}).get('mechanisms') or 'none'}\n"
    )
    raw = role.structured_invoke(
        system=VERIFIER_SYSTEM_PROMPT,
        human=human,
        schema=DiagnosticVerifierResult,
    )
    result = GuardedVerifierResult.model_validate(raw.model_dump())
    return _confirm_hard_flags(result, synthesis, no_escalation=no_escalation)
