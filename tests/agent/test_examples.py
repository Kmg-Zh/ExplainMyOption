"""The governance examples run offline and show what they say they show (examples/governance/)."""

from __future__ import annotations

import runpy

import pytest

from explain_my_option.paths import REPO_ROOT

EXAMPLES = REPO_ROOT / "examples" / "governance"


@pytest.fixture
def run_example(capsys):
    def run(name: str):
        result = runpy.run_path(str(EXAMPLES / name))["main"]()
        assert capsys.readouterr().out  # every example prints its walk-through
        return result

    return run


def test_an_invented_figure_is_rejected_and_never_reaches_the_report(run_example):
    out = run_example("01_invented_number.py")
    assert out["reasons"] and not out["claim_in_report"]
    assert out["rationale"].startswith("LLM synthesis failed")


def test_an_injected_headline_stays_data_and_its_claim_is_rejected(run_example):
    out = run_example("02_injected_headline.py")
    assert out["block"].count("</untrusted_source>") == 1 and "&lt;/untrusted_source&gt;" in out["block"]
    assert out["reasons"] and not out["claim_in_verdict"]


def test_only_a_code_confirmed_verifier_fail_stops_the_leg(run_example):
    false_alarm, real = run_example("03_verifier_needs_code_proof.py")
    assert (false_alarm["code_verdict"], false_alarm["code_flags"], false_alarm["terminal"]) == ("PARTIAL", ["unconfirmed_hard_flag"], False)
    assert (real["code_verdict"], real["code_flags"], real["terminal"]) == ("FAIL", ["method_residual_blamed"], True)


def test_a_quiet_day_makes_no_llm_call_and_no_search(run_example):
    out = run_example("04_quiet_day.py")
    assert (out["llm_calls"], out["searched"], out["all_tools_free"], out["no_escalation"]) == (0, False, True, True)
    assert out["material_llm_calls"] == 2


def test_a_data_gap_stops_before_pricing_and_any_llm(run_example):
    out = run_example("05_data_gap.py")
    assert out["coverage_gap"] and (out["pricing_calls"], out["llm_calls"]) == (0, 0)
    assert "not an unexplained market move" in out["report"]


def test_every_example_has_a_test_here():
    tested = {"01_invented_number.py", "02_injected_headline.py", "03_verifier_needs_code_proof.py", "04_quiet_day.py", "05_data_gap.py"}
    assert {p.name for p in EXAMPLES.glob("*.py")} == tested
