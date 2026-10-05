"""Showcase verifier gate unit tests."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import bootstrap

bootstrap.install()

from dataclasses import dataclass

from explain_my_option.pricing.types import Greeks, MarketSnapshot, PnLAttribution, PricingDiagnostics, PricingResult
from explain_my_option.report.facts import build_position_facts
from explain_my_option.report.schema import DiagnosticSynthesis, EvidenceItem
from explain_my_option.pipeline.verifier import (
    apply_verifier_reflection,
    deterministic_precheck,
    is_hard_verifier_fail,
    verify_synthesis,
    violation_sentence,
)
from explain_my_option.pipeline.verifier_schema import DiagnosticVerifierResult


@dataclass
class _MockRole:
    response: object

    def structured_invoke(self, *, system, human, schema):
        return self.response


def _sample_facts():
    snap = MarketSnapshot(
        ticker="AAPL",
        option_type="call",
        strike=100.0,
        expiry="2027-01-15",
        spot_now=105.0,
        spot_prev=100.0,
        iv_now=0.30,
        iv_prev=0.28,
        option_price_now=5.0,
        option_price_prev=4.0,
        time_to_expiry_years=0.5,
        data_source="synthetic",
        as_of="2026-08-30",
    )
    pricing = PricingResult(
        greeks_prev=Greeks(price=4.0, delta=0.5, gamma=0.02, vega=0.1, theta=-0.04),
        greeks_now=Greeks(price=5.0, delta=0.52, gamma=0.02, vega=0.1, theta=-0.04),
        pnl=PnLAttribution(
            total_pnl=1.0,
            delta_pnl=0.8,
            gamma_pnl=0.05,
            vega_pnl=0.1,
            theta_pnl=-0.01,
            residual_pnl=0.06,
            d_spot=5.0,
            d_vol=0.02,
        ),
        diagnostics=PricingDiagnostics(data_source="synthetic", exercise_style="american"),
    )
    return build_position_facts(snap, pricing)


def test_deterministic_precheck_fails_numeric_hallucination():
    syn = DiagnosticSynthesis(
        primary_driver="Vega",
        verdict="Gained $2.00 on the move.",
        confidence_level="high",
        confidence_rationale="Test",
        evidence=[],
        takeaways=[],
    )
    pre = deterministic_precheck(
        syn, _sample_facts(), suppress_vega=False, observation_reliable=True
    )
    assert pre is not None and pre.verdict == "FAIL"


def test_deterministic_precheck_partial_when_observation_unreliable():
    syn = DiagnosticSynthesis(
        primary_driver="Delta rally",
        verdict="Spot move dominated.",
        confidence_level="high",
        confidence_rationale="Test",
        evidence=[],
        takeaways=[],
    )
    pre = deterministic_precheck(
        syn, _sample_facts(), suppress_vega=False, observation_reliable=False
    )
    assert pre is not None and pre.verdict == "PARTIAL"


def test_deterministic_precheck_unreliable_with_evidence_is_partial():
    syn = DiagnosticSynthesis(
        primary_driver="Delta rally",
        verdict="Spot move dominated.",
        confidence_level="high",
        confidence_rationale="Test",
        evidence=[EvidenceItem(headline="headline", source="src", relevance="context")],
        takeaways=[],
    )
    pre = deterministic_precheck(
        syn, _sample_facts(), suppress_vega=False, observation_reliable=False
    )
    assert pre is not None and pre.verdict == "PARTIAL"
    assert "observation_soft_lock" in pre.policy_flags


def test_is_hard_verifier_fail_only_on_policy_flags():
    soft = DiagnosticVerifierResult(verdict="FAIL", policy_flags=[], rationale="thin")
    hard = DiagnosticVerifierResult(
        verdict="FAIL", policy_flags=["numeric_hallucination"], rationale="bad"
    )
    assert not is_hard_verifier_fail(soft)
    assert is_hard_verifier_fail(hard)


def test_deterministic_precheck_fails_prohibited_trade_advice_phrase():
    """A9.4: opportunity/mispricing/arbitrage/etc. are hard FAILs regardless
    of context -- the borrow field (A9.3) makes these newly likely."""
    syn = DiagnosticSynthesis(
        primary_driver="Vega",
        verdict="The elevated borrow looks like an arbitrage opportunity for the desk.",
        confidence_level="high",
        confidence_rationale="Test",
        evidence=[],
        takeaways=[],
    )
    pre = deterministic_precheck(
        syn, _sample_facts(), suppress_vega=False, observation_reliable=True
    )
    assert pre is not None and pre.verdict == "FAIL"
    assert "prohibited_phrase" in pre.policy_flags


def test_deterministic_precheck_fails_should_have_language():
    syn = DiagnosticSynthesis(
        primary_driver="Delta",
        verdict="The desk should have exercised the deep ITM call before the drop.",
        confidence_level="medium",
        confidence_rationale="Test",
        evidence=[],
        takeaways=[],
    )
    pre = deterministic_precheck(
        syn, _sample_facts(), suppress_vega=False, observation_reliable=True
    )
    assert pre is not None and pre.verdict == "FAIL"
    assert "prohibited_phrase" in pre.policy_flags


def test_deterministic_precheck_fails_catalyst_on_no_escalation():
    """A7.5: any catalyst/event language on a no_escalation run is FAIL."""
    syn = DiagnosticSynthesis(
        primary_driver="Theta / carry",
        verdict="Nothing to explain, though a short squeeze kept things contained.",
        confidence_level="high",
        confidence_rationale="quiet day",
        evidence=[],
        takeaways=[],
    )
    pre = deterministic_precheck(
        syn,
        _sample_facts(),
        suppress_vega=False,
        observation_reliable=True,
        no_escalation=True,
    )
    assert pre is not None and pre.verdict == "FAIL"
    assert "quiet_day_confabulation" in pre.policy_flags


def test_deterministic_precheck_fails_evidence_on_no_escalation():
    syn = DiagnosticSynthesis(
        primary_driver="Theta / carry",
        verdict="Nothing to explain. The move is accounted for by carry and a small spot move.",
        confidence_level="high",
        confidence_rationale="quiet day",
        evidence=[EvidenceItem(headline="Some headline", source="wire", relevance="context")],
        takeaways=[],
    )
    pre = deterministic_precheck(
        syn,
        _sample_facts(),
        suppress_vega=False,
        observation_reliable=True,
        no_escalation=True,
    )
    assert pre is not None and pre.verdict == "FAIL"
    assert "quiet_day_confabulation" in pre.policy_flags


def test_deterministic_precheck_passes_clean_no_escalation_synthesis():
    from explain_my_option.pipeline.leg_graph import NO_ESCALATION_TEXT

    syn = DiagnosticSynthesis(
        primary_driver="Theta / carry",
        verdict=NO_ESCALATION_TEXT,
        confidence_level="high",
        confidence_rationale=(
            "Escalation metric is at or below the quiet-day threshold; see the "
            "Mark Reconciliation section for the exact figures."
        ),
        evidence=[],
        takeaways=["No action needed; move is within theta/carry tolerance."],
    )
    pre = deterministic_precheck(
        syn,
        _sample_facts(),
        suppress_vega=False,
        observation_reliable=True,
        no_escalation=True,
    )
    assert pre is None  # falls through to the LLM verifier -- nothing hard-coded to object to


def test_is_hard_verifier_fail_on_method_residual_blamed():
    """A6.4/A6.5: a synthesis blaming news for the method residual is rejected."""
    hard = DiagnosticVerifierResult(
        verdict="FAIL",
        policy_flags=["method_residual_blamed"],
        rationale="verdict attributes the arithmetic residual to an earnings headline",
    )
    assert is_hard_verifier_fail(hard)


def test_apply_verifier_reflection_prefixes_verdict():
    syn = DiagnosticSynthesis(
        primary_driver="Delta",
        verdict="Spot move dominated.",
        confidence_level="high",
        confidence_rationale="Test",
        evidence=[],
        takeaways=[],
    )
    verdict = DiagnosticVerifierResult(
        verdict="PARTIAL",
        missing_evidence=["quote noise"],
        policy_flags=["observation_soft_lock"],
        rationale="Direction OK; quotes weak.",
    )
    out = apply_verifier_reflection(syn, verdict, observation_reliable=False)
    assert out.verdict.startswith("Reflect (PARTIAL):")
    assert out.confidence_level == "medium"
    assert out.takeaways[0].startswith("**Verifier reflect**")


def test_verifier_pass_from_mock_role():
    from explain_my_option.pipeline.verifier_schema import DiagnosticVerifierResult

    syn = DiagnosticSynthesis(
        primary_driver="Delta rally",
        verdict="Spot move dominated.",
        confidence_level="high",
        confidence_rationale="Clean.",
        evidence=[],
        takeaways=["Watch the ex-dividend boundary."],
    )
    role = _MockRole(
        DiagnosticVerifierResult(verdict="PASS", missing_evidence=[], policy_flags=[], rationale="ok")
    )
    result = verify_synthesis(
        syn,
        _sample_facts(),
        role=role,
        suppress_vega=False,
        observation_reliable=True,
        news_titles=[],
    )
    assert result.verdict == "PASS"


def test_hedge_directive_is_partial_not_hard_fail():
    """Hedge/sizing directives are soft (PARTIAL, flag hedge_advice); only the
    literal prohibited list is a hard FAIL."""
    for text in (
        "Continue standard hedging.",
        "Consider hedging vega before the print.",
        "Rebalance delta hedges tomorrow.",
        "Take profits into strength.",
    ):
        syn = DiagnosticSynthesis(
            primary_driver="Delta rally",
            verdict="Spot move dominated.",
            confidence_level="high",
            confidence_rationale="Clean.",
            evidence=[],
            takeaways=[text],
        )
        result = deterministic_precheck(
            syn, _sample_facts(), suppress_vega=False, observation_reliable=True
        )
        assert result is not None and result.verdict == "PARTIAL", text
        assert result.policy_flags == ["hedge_advice"], text
        assert not is_hard_verifier_fail(result)


def test_neutral_monitoring_language_is_not_hedge_advice():
    syn = DiagnosticSynthesis(
        primary_driver="Delta rally",
        verdict="Spot move dominated.",
        confidence_level="high",
        confidence_rationale="Clean.",
        evidence=[],
        takeaways=["Monitor the position; watch for further moves."],
    )
    assert (
        deterministic_precheck(
            syn, _sample_facts(), suppress_vega=False, observation_reliable=True
        )
        is None
    )


def _clean_synthesis(**kw):
    base = dict(
        primary_driver="Delta rally",
        verdict="Spot move dominated.",
        confidence_level="high",
        confidence_rationale="Clean.",
        evidence=[],
        takeaways=["Watch the ex-dividend boundary."],
    )
    base.update(kw)
    return DiagnosticSynthesis(**base)


def _fail_role(flags, rationale="The narrative is mostly right. It violates policy."):
    return _MockRole(
        DiagnosticVerifierResult(
            verdict="FAIL", missing_evidence=[], policy_flags=list(flags), rationale=rationale
        )
    )


def _verify(syn, role, **kw):
    return verify_synthesis(
        syn,
        _sample_facts(),
        role=role,
        suppress_vega=False,
        observation_reliable=True,
        news_titles=[],
        **kw,
    )


def test_unconfirmed_hard_flags_downgrade_to_partial():
    for flag in (
        "numeric_hallucination",
        "prohibited_phrase",
        "quiet_day_confabulation",
        "method_residual_blamed",
    ):
        out = _verify(_clean_synthesis(), _fail_role([flag]))
        assert out.verdict == "PARTIAL", flag
        assert "unconfirmed_hard_flag" in out.policy_flags
        assert out.llm_verdict == "FAIL" and out.llm_policy_flags == [flag]
        assert not is_hard_verifier_fail(out)


def test_method_residual_blame_needs_external_cause_in_same_sentence():
    # Model/math vocabulary is not blame -> downgraded.
    syn = _clean_synthesis(verdict="The residual reflects convexity and path effects.")
    assert _verify(syn, _fail_role(["method_residual_blamed"])).verdict == "PARTIAL"
    # Residual tied to an outside cause -> stays a hard FAIL.
    syn = _clean_synthesis(verdict="The residual is explained by the earnings headline.")
    out = _verify(syn, _fail_role(["method_residual_blamed"]))
    assert out.verdict == "FAIL" and is_hard_verifier_fail(out)


def test_prohibited_phrase_confirmed_by_literal_or_synonym():
    syn = _clean_synthesis(verdict="This looks like a bargain.")
    assert _verify(syn, _fail_role(["prohibited_phrase"])).verdict == "FAIL"


def test_quiet_day_flag_requires_no_escalation():
    syn = _clean_synthesis(verdict="Earnings drove the move.")
    assert _verify(syn, _fail_role(["quiet_day_confabulation"])).verdict == "PARTIAL"


def test_violation_sentence_picks_the_violation_not_the_concession():
    out = DiagnosticVerifierResult(
        verdict="FAIL",
        policy_flags=["method_residual_blamed"],
        rationale="The narrative correctly names Delta. It blames the residual on earnings.",
    )
    assert violation_sentence(out) == "It blames the residual on earnings."
    bare = DiagnosticVerifierResult(
        verdict="FAIL", policy_flags=["numeric_hallucination"], rationale="Looks fine overall."
    )
    assert "number" in violation_sentence(bare).lower()


def test_evidence_provenance_flags_future_stale_and_unsupplied():
    from explain_my_option.data_loader import NewsItem
    from explain_my_option.report.validate import evidence_provenance_errors

    syn = _clean_synthesis(
        evidence=[EvidenceItem(headline="Acme beats estimates", source="X", relevance="r")]
    )
    ok = [NewsItem(title="Acme beats estimates", published="2026-10-01")]
    assert evidence_provenance_errors(syn, ok, "2026-10-02") == []
    future = [NewsItem(title="Acme beats estimates", published="2026-10-05")]
    assert "after as_of" in evidence_provenance_errors(syn, future, "2026-10-02")[0]
    stale = [NewsItem(title="Acme beats estimates", published="2026-09-01")]
    assert "older than" in evidence_provenance_errors(syn, stale, "2026-10-02")[0]
    assert "not in supplied" in evidence_provenance_errors(syn, [], "2026-10-02")[0]
    undated = [NewsItem(title="Acme beats estimates")]
    assert evidence_provenance_errors(syn, undated, "2026-10-02") == []
    pre = deterministic_precheck(
        syn, _sample_facts(), suppress_vega=False, observation_reliable=True,
        news=future, as_of="2026-10-02",
    )
    assert pre is not None and pre.policy_flags == ["evidence_provenance"]


def test_deterministic_precheck_partial_when_headline_catalyst_omitted():
    syn = DiagnosticSynthesis(
        primary_driver="Delta-driven gap",
        verdict="Spot move dominated via higher-order convexity.",
        confidence_level="medium",
        confidence_rationale="Truncation after an extreme gap.",
        evidence=[],
        takeaways=["Re-price on the full surface."],
    )
    titles = [
        "Meta options volume surged as implied volatility collapsed after earnings (IV crush)"
    ]
    pre = deterministic_precheck(
        syn,
        _sample_facts(),
        suppress_vega=False,
        observation_reliable=True,
        news_titles=titles,
    )
    assert pre is not None and pre.verdict == "PARTIAL"
    assert "missing_catalyst_layer" in pre.policy_flags


def test_deterministic_precheck_passes_when_catalyst_named():
    syn = DiagnosticSynthesis(
        primary_driver="Delta-driven gap with IV crush overlay",
        verdict="Spot gap led the move; implied volatility crush was a second overlay.",
        confidence_level="medium",
        confidence_rationale="Earnings and IV crush in the tape.",
        evidence=[],
        takeaways=["Watch post-earnings IV crush, not only a full-surface reprice."],
    )
    titles = [
        "Meta options volume surged as implied volatility collapsed after earnings (IV crush)"
    ]
    pre = deterministic_precheck(
        syn,
        _sample_facts(),
        suppress_vega=False,
        observation_reliable=True,
        news_titles=titles,
    )
    assert pre is None


if __name__ == "__main__":
    test_deterministic_precheck_fails_numeric_hallucination()
    test_deterministic_precheck_partial_when_observation_unreliable()
    test_deterministic_precheck_unreliable_with_evidence_is_partial()
    test_is_hard_verifier_fail_only_on_policy_flags()
    test_is_hard_verifier_fail_on_method_residual_blamed()
    test_deterministic_precheck_fails_prohibited_trade_advice_phrase()
    test_deterministic_precheck_fails_should_have_language()
    test_deterministic_precheck_fails_catalyst_on_no_escalation()
    test_deterministic_precheck_fails_evidence_on_no_escalation()
    test_deterministic_precheck_passes_clean_no_escalation_synthesis()
    test_apply_verifier_reflection_prefixes_verdict()
    test_verifier_pass_from_mock_role()
    test_deterministic_precheck_partial_when_headline_catalyst_omitted()
    test_deterministic_precheck_passes_when_catalyst_named()
    print("OK — pipeline verifier tests passed")
