"""Benchmark narrative scoring (offline)."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


from bootstrap import install

install()

from historical.scoring import score_narrative_for_case, synthesis_narrative_text
from explain_my_option.report.schema import DiagnosticSynthesis, EvidenceItem
from historical.cases import load_cases


def test_evidence_headline_counts_for_keyword_groups():
    case = load_cases()[0]  # meta
    syn = DiagnosticSynthesis(
        primary_driver="Delta decline",
        verdict="Extreme spot move and higher-order convexity left a Taylor gap.",
        confidence_level="medium",
        confidence_rationale="Residual band is medium.",
        evidence=[
            EvidenceItem(
                headline="Meta options volume surged as implied volatility collapsed after earnings (IV crush)",
                source="Reuters",
                relevance="Supports vol-driven component alongside the spot shock.",
            )
        ],
        takeaways=["Re-price on the full surface after the jump."],
    )
    text = synthesis_narrative_text(syn)
    assert "iv crush" in text.lower()
    scores = score_narrative_for_case(syn, case, residual_pct=30.0)
    assert scores["keyword_groups_hit"] >= 1
    assert scores["keyword_groups_pass"]


def test_keyword_groups_allow_synonyms():
    case = next(c for c in load_cases() if c.test_id == "meta_earnings_gap_2022")
    syn = DiagnosticSynthesis(
        primary_driver="Gamma convexity",
        verdict="Taylor truncation on the extreme jump left unexplained residual.",
        confidence_level="medium",
        confidence_rationale="Medium residual with large spot move.",
        evidence=[],
        takeaways=[],
    )
    scores = score_narrative_for_case(syn, case, residual_pct=29.0)
    assert scores["keyword_groups_hit"] >= 1
    assert "higher-order convexity" in scores["post_hoc_keyword_groups"]
    assert "iv crush" in scores["as_of_keyword_groups"]


def test_vmw_hindsight_is_not_a_hard_pass_line():
    case = next(c for c in load_cases() if c.test_id == "vmw_htb_2008")
    syn = DiagnosticSynthesis(
        primary_driver="Delta decline",
        verdict="Spot sold off after weak guidance; residual is small.",
        confidence_level="medium",
        confidence_rationale="Earnings tape only.",
        evidence=[],
        takeaways=["Watch the next print."],
    )
    scores = score_narrative_for_case(syn, case, residual_pct=3.0)
    assert scores["keyword_groups_required"] == 0
    assert scores["keyword_groups_pass"]
    assert scores["action_themes_required"] == 0
    assert scores["action_themes_pass"]
    assert not scores["possible_parametric_leak"]
    assert "hard-to-borrow" in scores["hindsight_keyword_groups"]


def test_avellaneda_is_flagged_as_parametric_leak_not_required():
    case = next(c for c in load_cases() if c.test_id == "vmw_htb_2008")
    syn = DiagnosticSynthesis(
        primary_driver="Delta decline",
        verdict="Avellaneda hard-to-borrow conversion left about a gap after earnings.",
        confidence_level="low",
        confidence_rationale="Cites the later HTB paper.",
        evidence=[],
        takeaways=["Update borrow curve assumptions."],
    )
    scores = score_narrative_for_case(syn, case, residual_pct=3.0)
    assert scores["keyword_groups_pass"]
    assert scores["possible_parametric_leak"]
    assert "avellaneda" in [m.lower() for m in scores["leak_marker_hits"]]
    assert "hard-to-borrow" in scores["hindsight_groups_hit"]
    assert "parametric_leak_flag" in scores["failure_hints"]
    assert "info_gap_oracle_only" in scores["failure_hints"]


def test_structure_helps_when_governed_has_layer_b_baseline_misses():
    from historical.scoring import attribute_governed_vs_baseline

    case = next(c for c in load_cases() if c.test_id == "gme_squeeze_2021")
    governed = {
        "layer_a": {"pass": True, "configured": True},
        "layer_b": {"pass": True, "configured": True},
        "keyword_groups_pass": True,
    }
    baseline = {
        "layer_a": {"pass": True, "configured": True},
        "layer_b": {"pass": False, "configured": True},
        "keyword_groups_pass": False,
    }
    hint = attribute_governed_vs_baseline(governed, baseline, case)
    assert hint["primary"] == "structure_helps_layer_b"


def test_compare_scorecard_writes_even_when_narrative_scores_are_zero():
    from historical.compare import _empty_narrative_scores, _write_compare_scorecard
    import tempfile

    case = next(c for c in load_cases() if c.test_id == "gme_squeeze_2021")
    empty = _empty_narrative_scores(case, error="narrative_failed")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        _write_compare_scorecard(
            out,
            case=case,
            residual_ratio=0.3703,
            gov_scores=empty,
            base_scores=empty,
            hint={"primary": "both_miss_layer_b_try_prompt_and_structure"},
        )
        text = (out / "scorecard.md").read_text(encoding="utf-8")
    assert "Residual ratio (deterministic)" in text
    assert "0.3703" in text or "37.0%" in text
    assert "keyword groups" in text
    assert "soft and model-dependent" in text


if __name__ == "__main__":
    test_evidence_headline_counts_for_keyword_groups()
    test_keyword_groups_allow_synonyms()
    test_vmw_hindsight_is_not_a_hard_pass_line()
    test_avellaneda_is_flagged_as_parametric_leak_not_required()
    test_structure_helps_when_governed_has_layer_b_baseline_misses()
    test_compare_scorecard_writes_even_when_narrative_scores_are_zero()
    print("OK — benchmark scoring tests passed")
