"""Independent verifier gate for diagnostic synthesis."""

from __future__ import annotations

from ..report.catalysts import missing_catalyst_tags, tags_from_headlines
from ..report.facts import PositionFacts
from ..report.schema import DiagnosticSynthesis
from ..report.validate import find_prohibited_phrases, validate_synthesis
from .llm_roles import LlmRole
from .verifier_schema import DiagnosticVerifierResult

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

Do not invent numbers or prices."""

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
        reflect_bits.append(rationale)
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
) -> DiagnosticVerifierResult:
    pre = deterministic_precheck(
        synthesis,
        facts,
        suppress_vega=suppress_vega,
        observation_reliable=observation_reliable,
        news_titles=news_titles,
        no_escalation=no_escalation,
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
        f"News titles: {news_titles[:3]}\n"
        f"Headline mechanisms present in titles: {tags_from_headlines(news_titles) or 'none'}\n"
        f"Independent critic Layer B required: {(catalyst_challenge or {}).get('layer_b_required')}\n"
        f"Independent critic mechanisms: {(catalyst_challenge or {}).get('mechanisms') or 'none'}\n"
    )
    return role.structured_invoke(
        system=VERIFIER_SYSTEM_PROMPT,
        human=human,
        schema=DiagnosticVerifierResult,
    )
