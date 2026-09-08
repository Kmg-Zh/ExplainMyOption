"""Independent verifier gate for diagnostic synthesis."""

from __future__ import annotations

from ..report.catalysts import missing_catalyst_tags, tags_from_headlines
from ..report.facts import PositionFacts
from ..report.schema import DiagnosticSynthesis
from ..report.validate import validate_synthesis
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

Verdict policy:
- PASS: Layer A matches the dominant driver, Layer B is covered when headlines name a
  mechanism, and observation locks are respected.
- PARTIAL (preferred over FAIL when unsure): evidence is thin, quote quality is weak, IV sits
  inside the noise band, OR headlines name a catalyst that verdict/takeaways omit.
  Use PARTIAL instead of FAIL for "cannot prove" and "missing catalyst layer" situations.
- FAIL (hard violations only): numeric hallucination in narrative fields.

Do not invent numbers or prices."""

HARD_FAIL_POLICY_FLAGS = frozenset({"numeric_hallucination"})


def deterministic_precheck(
    synthesis: DiagnosticSynthesis,
    facts: PositionFacts,
    *,
    suppress_vega: bool,
    observation_reliable: bool,
    news_titles: list[str] | None = None,
) -> DiagnosticVerifierResult | None:
    errors = validate_synthesis(synthesis)
    if errors:
        return DiagnosticVerifierResult(
            verdict="FAIL",
            missing_evidence=errors,
            policy_flags=["numeric_hallucination"],
            rationale="validate_synthesis failed",
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
            rationale=(
                "Direction may be OK, but quote quality limits falsifiability; "
                "treat factor attribution as indicative."
            ),
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
            rationale=(
                "Layer B omitted mechanisms present in headlines; residual truncation "
                "does not replace those catalysts."
            ),
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
) -> DiagnosticVerifierResult:
    pre = deterministic_precheck(
        synthesis,
        facts,
        suppress_vega=suppress_vega,
        observation_reliable=observation_reliable,
        news_titles=news_titles,
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
