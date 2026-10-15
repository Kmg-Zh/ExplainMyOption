"""Historical events: each case pins the desk lesson it exists to teach.

Real chains (DoltHub quotes on both days): the GME squeeze (2021-01-25), the AAPL
ex-dividend day (2023-11-09) and three quiet days in 2023. Stress fixtures use
hand-chosen spot and IV to force a residual regime; they test the attribution
code, not claims about the day. Agent-visible headlines are the case's frozen
as-of tape, never anything published later.
"""

from __future__ import annotations

import pytest
from support import FAST, QUIET_DAYS, ScriptedNarrator, no_llm_roles, roles, run_leg

from historical.cases import (
    comparison_news_for_case,
    frozen_news_for_case,
    ground_truth_news_for_case,
    load_cases,
    news_lineage_errors,
)
from historical.scoring import score_narrative_for_case
from explain_my_option.data.historical_chain import load_historical_case
from explain_my_option.data.observation import check_basis_consistency
from explain_my_option.pipeline.leg_graph import NO_ESCALATION_TEXT
from explain_my_option.pricing import price_and_attribute
from explain_my_option.report.facts import build_position_facts
from explain_my_option.report.reconciliation import build_reconciliation_facts
from explain_my_option.report.schema import DiagnosticSynthesis

CASES = {case.test_id: case for case in load_cases()}


def _stress(test_id: str, narrator=None) -> dict:
    """Run a benchmark case's stress fixture with its own frozen as-of headlines."""
    case = CASES[test_id]
    return run_leg(fixture=case.fixture, news=frozen_news_for_case(case), llm=roles(narrator))


def _real(name: str):
    snap = load_historical_case(name)
    pricing = price_and_attribute(snap, config=FAST)
    return snap, pricing


def _basis_ok(snap) -> bool:
    is_call = snap.option_type == "call"
    return check_basis_consistency(
        spot=snap.spot_now,
        rate=snap.risk_free_rate,
        time_to_expiry_years=snap.time_to_expiry_years,
        call_mid=snap.mid if is_call else None,
        call_strike=snap.strike if is_call else None,
        put_mid=None if is_call else snap.mid,
        put_strike=None if is_call else snap.strike,
    ).ok


# --- Real chains ---------------------------------------------------------------------------


def test_gme_2021_real_chain_is_a_squeeze_with_extreme_implied_borrow():
    snap, pricing = _real("gme_squeeze_2021_real")
    assert snap.data_source == "historical" and _basis_ok(snap)
    assert snap.iv_prev > 2.0 and snap.iv_now > 2.0  # squeeze-level vol on both days
    assert snap.dividend_yield > 0.20  # implied borrow, put-call parity: regime "extreme"
    rec = build_reconciliation_facts(snap, pricing)
    assert rec.mark_calibrated and abs(rec.model_vs_mark_gap_usd) < 1e-2


def test_aapl_2023_real_ex_div_is_a_carry_case_not_an_early_exercise_case():
    snap, pricing = _real("aapl_exdiv_2023_real")
    assert [(d.ex_date, d.amount) for d in snap.discrete_dividends] == [("2023-11-10", 0.24)]
    american = build_position_facts(snap, pricing).american
    assert american.ee_relevant is False and american.dividend_coverage < 1.0
    assert "carry/theta case" in american.early_exercise_assessment
    assert build_reconciliation_facts(snap, pricing).escalation_basis == "model"  # reliable marks both days
    assert run_leg(case="aapl_exdiv_2023_real", llm=no_llm_roles())["no_escalation"]


@pytest.mark.parametrize("name", QUIET_DAYS)
def test_quiet_days_have_nothing_to_explain(name):
    """No LLM call, no search, no costly tool, no catalyst story, never a terminal break."""
    out = run_leg(case=name, llm=no_llm_roles())
    findings = out["diagnostic_findings"]
    assert out["no_escalation"] and out["diagnostic_synthesis"]["verdict"] == NO_ESCALATION_TEXT
    assert out["diagnostic_synthesis"]["evidence"] == [] and not out.get("news")
    assert all(cost == "free" for cost in findings["tool_costs"].values())
    assert not findings["terminal_unexplained_break"]
    snap, pricing = _real(name)
    assert build_reconciliation_facts(snap, pricing).escalation_metric_pct <= 10.0


# --- Stress fixtures, with each case's frozen as-of headlines ---------------------------------


def test_meta_2022_earnings_gap_is_too_large_for_taylor():
    out = _stress("meta_earnings_gap_2022")
    snap, findings = out["snapshot"], out["diagnostic_findings"]
    assert (snap.spot_prev, snap.spot_now) == (320.19, 237.76)  # -26% overnight
    assert findings["taylor_regime"] == "INVALID"  # full revaluation is the headline
    assert build_position_facts(snap, out["pricing"]).residual_pct >= 15.0
    assert out["search_plan"].skip_reason == "" and "material" in {q.cue for q in out["search_plan"].queries}
    assert "implied volatility" in out["report"]  # the as-of IV-crush headline reaches the report


def test_aapl_ex_div_overlay_splits_dividend_and_early_exercise():
    out = _stress("aapl_exdiv_2023")
    split = out["diagnostic_findings"]["ex_div_attribution"]
    assert split["flag_ex_div_window"] and split["ee_premium_material"]
    assert split["dividend_amount"] > 0 and split["spot_drop"] < 0
    assert "Ex-div attribution overlay" in out["report"]
    assert "early-exercise" in out["diagnostic_synthesis"]["american_commentary"].lower()


def test_gme_squeeze_tape_mechanisms_must_appear_in_the_narrative():
    """The engine has no borrow factor: a squeeze headline is tape context the
    narrative must name, and code flags a narrative that leaves it out."""
    out = _stress("gme_squeeze_2021", narrator=ScriptedNarrator(verdict="Delta drove the loss."))
    assert {"squeeze", "borrow"} <= set(out["diagnostic_findings"]["intel_digest"]["mechanisms"])
    assert "missing_catalyst_layer" in out["verifier_trace"][-1]["policy_flags"]


def test_vw_2008_float_squeeze_escalates_instead_of_inventing_a_story():
    out = _stress("vow_float_squeeze_2008")
    findings = out["diagnostic_findings"]
    assert findings["taylor_regime"] == "INVALID" and findings["r_spot"] > 1.0
    assert findings["terminal_unexplained_break"]
    assert "Terminal break" in out["report"]


def test_vmw_2008_hard_to_borrow_leaves_a_small_residual_because_borrow_is_not_modelled():
    out = _stress("vmw_htb_2008")
    assert build_position_facts(out["snapshot"], out["pricing"]).residual_pct < 5.0
    assert not out["diagnostic_findings"]["terminal_unexplained_break"]


# --- Evaluation integrity ---------------------------------------------------------------------


def test_agent_visible_news_never_looks_ahead():
    """Headlines are published on or before as_of; the answer key stays hidden."""
    assert news_lineage_errors() == []
    for case in CASES.values():
        visible = comparison_news_for_case(case)
        assert [n.title for n in visible] == [n.title for n in frozen_news_for_case(case)]
        assert {n.title for n in ground_truth_news_for_case(case)}.isdisjoint(n.title for n in visible)
        assert case.input_text.strip().lower() not in " ".join(n.title for n in visible).lower()


def test_scoring_uses_the_contemporaneous_bar_and_flags_hindsight():
    """Later-paper vocabulary is not required, and naming it is flagged as parametric leakage."""
    case = CASES["vmw_htb_2008"]

    def score(verdict: str) -> dict:
        narrative = DiagnosticSynthesis(primary_driver="Delta decline", verdict=verdict, confidence_level="medium", confidence_rationale="Earnings tape only.")
        return score_narrative_for_case(narrative, case, residual_pct=3.0)

    plain = score("Spot sold off after weak guidance; the residual is small.")
    assert plain["keyword_groups_pass"] and plain["keyword_groups_required"] == 0 and not plain["possible_parametric_leak"]
    hindsight = score("Avellaneda hard-to-borrow conversion explains the gap after earnings.")
    assert hindsight["possible_parametric_leak"] and "parametric_leak_flag" in hindsight["failure_hints"]
