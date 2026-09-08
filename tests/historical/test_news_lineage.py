"""Historical cases must not feed future news or the answer key to the agent."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from historical.cases import (
    comparison_news_for_case,
    frozen_news_for_case,
    ground_truth_news_for_case,
    load_cases,
    news_lineage_errors,
    split_keyword_groups_by_lineage,
)


def test_as_of_news_has_no_lookahead():
    errors = news_lineage_errors()
    assert not errors, "\n".join(errors)


def test_eval_dimensions_exist():
    for case in load_cases():
        assert case.eval_dimensions.get("layer_a"), f"{case.test_id}: missing layer_a"
        assert case.eval_dimensions.get("layer_b"), f"{case.test_id}: missing layer_b"
        assert case.ground_truth, f"{case.test_id}: empty ground_truth"
        assert any(row.get("excerpt") for row in case.ground_truth), (
            f"{case.test_id}: ground_truth needs at least one excerpt"
        )


def test_comparison_news_matches_as_of_and_excludes_answer_key():
    for case in load_cases():
        frozen = frozen_news_for_case(case)
        comparison = comparison_news_for_case(case)
        assert [item.title for item in comparison] == [item.title for item in frozen]
        blob = " ".join(
            f"{item.publisher} {item.title}" for item in comparison
        ).lower()
        assert "desk color" not in blob
        assert case.input_text.strip().lower() not in blob
        gt_titles = {item.title for item in ground_truth_news_for_case(case)}
        as_of_titles = {item.title for item in frozen}
        assert gt_titles.isdisjoint(as_of_titles)


def test_post_hoc_groups_are_not_all_spoiled_by_as_of_tape():
    """At least the microstructure cases hide some rubric tokens from as-of news."""
    gme = next(c for c in load_cases() if c.test_id == "gme_squeeze_2021")
    vmw = next(c for c in load_cases() if c.test_id == "vmw_htb_2008")
    _as_of_gme, post_gme = split_keyword_groups_by_lineage(gme)
    _as_of_vmw, post_vmw = split_keyword_groups_by_lineage(vmw)
    assert post_gme, "GME borrow/buy-in should stay out of as-of tape even if squeeze is visible"
    assert post_vmw, "VMW HTB/conversion should be post-hoc, not same-day tape"
    assert "hard-to-borrow" in [g[0] for g in vmw.hindsight_keyword_groups()]
    assert not vmw.required_keyword_groups()


if __name__ == "__main__":
    test_as_of_news_has_no_lookahead()
    test_eval_dimensions_exist()
    test_comparison_news_matches_as_of_and_excludes_answer_key()
    test_post_hoc_groups_are_not_all_spoiled_by_as_of_tape()
    print("OK — historical news lineage checks passed")
