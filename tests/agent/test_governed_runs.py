"""Governance end to end: full legs through the compiled graph with scripted LLM roles.

Each test checks what reaches the report when an LLM role misbehaves or the
evidence is weak: the verifier's outcomes, invented figures, required catalysts,
and data gaps that must not be told as market stories.
"""

from __future__ import annotations

import pytest
from support import (
    LEG,
    NeverPrice,
    NoLlm,
    ScriptedNarrator,
    ScriptedRole,
    ScriptedVerifier,
    invoke_leg,
    no_llm_roles,
    roles,
    run_leg,
)

from explain_my_option.data.observation import ObservationStatus, continuity_gate
from explain_my_option.data_loader import NewsItem


def test_a_missing_observation_is_a_coverage_gap_not_an_unexplained_break():
    class MissingDay:
        def load(self, **_):
            continuity_gate(
                contract="TEST 100C",
                status_t1=ObservationStatus.OK,
                status_t=ObservationStatus.DAY_MISSING,
                date_t1="2026-08-28",
                date_t="2026-08-31",
            )

    out = invoke_leg(LEG, market=MissingDay(), pnl=NeverPrice(), llm=no_llm_roles())
    assert out["terminal_no_comparable_observation"]
    assert out["report"].startswith("## No Comparable Observation")
    assert "DAY_MISSING on 2026-08-31" in out["report"] and "not an unexplained market move" in out["report"]
    assert not (out.get("diagnostic_findings") or {}).get("terminal_unexplained_break")


# --- Verifier routing ----------------------------------------------------------------------


def _verified(narrator=None, verifier=None) -> dict:
    out = run_leg(fixture="vol_crush", llm=roles(narrator, verifier))
    return {"out": out, "findings": out["diagnostic_findings"], "verdict": out["diagnostic_synthesis"]["verdict"]}


def test_a_passing_narrative_ships_unchanged():
    run = _verified()
    assert run["verdict"] == ScriptedNarrator().verdict and "verifier_status" not in run["findings"]


def test_a_partial_verdict_ships_with_the_verifier_caveat():
    run = _verified(verifier=ScriptedVerifier("PARTIAL", ("thin_evidence",)))
    assert run["verdict"].startswith("Reflect (PARTIAL):") and run["findings"]["verifier_status"] == "PARTIAL"
    assert "**Verifier**: PARTIAL" in run["out"]["report"]


@pytest.mark.parametrize(
    "narrator, verifier, flag",
    [
        (ScriptedNarrator(verdict="The selloff makes the option look cheap here."), NoLlm(), "prohibited_phrase"),
        (ScriptedNarrator(verdict="The residual is explained by the earnings announcement."), ScriptedVerifier("FAIL", ("method_residual_blamed",)), "method_residual_blamed"),
    ],
    ids=["caught by code before the verifier", "llm flag confirmed by code"],
)
def test_a_confirmed_hard_failure_escalates_to_a_terminal_break(narrator, verifier, flag):
    run = _verified(narrator, verifier)
    findings = run["findings"]
    assert findings["terminal_unexplained_break"] and findings["terminal_cause"] == "verifier_hard_fail"
    assert findings["terminal_verifier_flags"] == [flag]
    assert run["verdict"].startswith(f"Verifier FAIL — terminal break escalation ({flag}).")
    assert len(findings["verifier_audit"]["trace"]) == 1
    assert "the verifier's hard failure was confirmed by code" in run["out"]["report"]
    assert "diagnostic budget exhausted" not in run["out"]["report"]


def test_an_unconfirmed_llm_failure_is_downgraded_to_partial():
    run = _verified(verifier=ScriptedVerifier("FAIL", ("numeric_hallucination",)))
    assert not run["findings"].get("terminal_unexplained_break")
    assert run["findings"]["verifier_status"] == "PARTIAL"
    assert run["findings"]["verifier_audit"]["trace"][0]["llm_verdict"] == "FAIL"


def test_an_invented_dollar_figure_never_reaches_the_report():
    """The narrator's figure is caught at synthesis and replaced by the rule-based summary."""
    run = _verified(narrator=ScriptedNarrator(verdict="The desk gained $2.50 on the contract today."))
    assert "$2.50" not in run["out"]["report"]
    assert run["out"]["diagnostic_synthesis"]["confidence_rationale"].startswith("LLM synthesis failed")


# --- Headlines through the digest, critic and reconcile steps ---------------------------------

SQUEEZE = NewsItem(title="Short squeeze grips the stock as borrow costs spike", publisher="Wire", published="2026-08-14")


def test_a_required_catalyst_from_the_critic_reaches_the_narrative():
    digester = ScriptedRole({"relevant": [{"title": SQUEEZE.title, "mechanisms": ["squeeze", "borrow"], "one_line_fact": "Squeeze and borrow stress."}]})
    critic = ScriptedRole({"layer_b_required": True, "mechanisms": ["squeeze", "borrow"], "rationale": "Headline names a squeeze."})
    out = run_leg(fixture="vol_crush", news=[SQUEEZE], llm=roles(digester=digester, challenger=critic))
    verdict = out["diagnostic_synthesis"]["verdict"]
    assert "Independent critic: evidence is consistent with squeeze" in verdict
    assert out["llm_calls"] == 4  # digester, critic, narrator, verifier
    assert SQUEEZE.title in out["report"]


DIVIDEND = NewsItem(title="Stock trades ex-dividend tomorrow with a $0.24 quarterly dividend", publisher="Wire", published="2026-08-14")


def test_a_headline_figure_the_digester_quotes_is_not_an_invented_number():
    """Digest facts become evidence after the narrator's check, so code applies the same rule there."""
    fact = "Trades ex-dividend tomorrow for a $0.24 dividend."
    digester = ScriptedRole({"relevant": [{"title": DIVIDEND.title, "mechanisms": [], "one_line_fact": fact}]})
    out = run_leg(fixture="vol_crush", news=[DIVIDEND], llm=roles(digester=digester))
    evidence = out["diagnostic_synthesis"]["evidence"]
    assert [e["headline"] for e in evidence] == [DIVIDEND.title]  # the headline keeps its figure
    assert fact not in evidence[0]["relevance"]
    assert out["diagnostic_findings"].get("verifier_status") != "FAIL"


def test_an_unreliable_quote_skips_search_and_strips_invented_evidence():
    narrator = ScriptedRole(
        {
            "primary_driver": "Vega / implied volatility",
            "verdict": "Vega led the move.",
            "confidence_level": "medium",
            "confidence_rationale": "Scripted.",
            "evidence": [{"headline": "A headline nobody supplied", "source": "x", "relevance": "Supports the story."}],
        }
    )
    out = run_leg(case="gme_squeeze_2021_real", news=[SQUEEZE], llm=roles(narrator, digester=NoLlm(), challenger=NoLlm()))
    assert out["diagnostic_findings"]["observation_reliable"] is False
    assert out["search_plan"].skip_reason == "observation_lock" and not out["news"]
    assert out["diagnostic_synthesis"]["evidence"] == []
