"""Playbook records: fixed narrator guidance that code selects for a special case.

A record is text for the narrator only. These tests pin who selects it (code,
from a diagnostic finding), what it may say (no figures, no trade or hedge
wording, no engine names, nothing a historical eval rewards) and what it must
not change (the search plan and the tools). Whether the narrator follows a
record is measured by an eval, not here.
"""

from __future__ import annotations

import pytest
from support import ScriptedNarrator, roles, run_leg

from historical.cases import frozen_news_for_case, ground_truth_news_for_case, load_cases
from explain_my_option.graph.deps import GraphDeps
from explain_my_option.graph.playbook import (
    DEFAULT_PLAYBOOK,
    TERMINAL_BREAK,
    PlaybookRecord,
    check_playbook,
    playbook_prompt_lines,
    select_records,
)

CASES = {case.test_id: case for case in load_cases()}


def _vw(playbook=DEFAULT_PLAYBOOK) -> tuple[dict, ScriptedNarrator]:
    """The VW 2008 stress fixture: a diagnostic-pass terminal break."""
    case, narrator = CASES["vow_float_squeeze_2008"], ScriptedNarrator()
    out = run_leg(fixture=case.fixture, news=frozen_news_for_case(case), llm=roles(narrator), playbook=playbook)
    return out, narrator


# --- Selection --------------------------------------------------------------------------------


def test_code_selects_a_record_when_its_finding_is_true():
    assert select_records({"terminal_unexplained_break": True}, DEFAULT_PLAYBOOK) == [TERMINAL_BREAK]
    assert select_records({"terminal_unexplained_break": False}, DEFAULT_PLAYBOOK) == []
    assert select_records({}, DEFAULT_PLAYBOOK) == []


def test_a_terminal_break_gives_the_narrator_the_record_and_the_report_lists_it():
    out, narrator = _vw()
    assert out["diagnostic_findings"]["terminal_unexplained_break"]
    assert TERMINAL_BREAK.guidance in narrator.seen[0]
    assert out["diagnostic_findings"]["playbook_records"] == [{"id": "terminal-break", "when": "terminal_unexplained_break"}]
    assert "**Playbook records** (selected by code for the narrator): `terminal-break` (`terminal_unexplained_break`)" in out["report"]


def test_a_leg_without_the_finding_gets_no_record():
    narrator = ScriptedNarrator()
    out = run_leg(fixture="vol_crush", llm=roles(narrator))
    assert "### Playbook" not in narrator.seen[0]
    assert "playbook_records" not in out["diagnostic_findings"]
    assert "Playbook records" not in out["report"]


def test_a_record_changes_the_narrator_prompt_and_nothing_else():
    """Same leg with the playbook on and off: the search plan, the tools and the
    news are identical, and the prompts differ by the record's lines only."""
    on, narrator_on = _vw()
    off, narrator_off = _vw(playbook=())
    assert on["search_plan"].model_dump() == off["search_plan"].model_dump()
    for key in ("tools_run", "skipped_tools", "tool_calls_used"):
        assert on["diagnostic_findings"][key] == off["diagnostic_findings"][key]
    assert [n.title for n in on["news"]] == [n.title for n in off["news"]]
    record_lines = "\n" + "\n".join(playbook_prompt_lines([TERMINAL_BREAK]))
    assert narrator_on.seen[0].replace(record_lines, "") == narrator_off.seen[0]


# --- What a record may say ---------------------------------------------------------------------


def test_the_bundled_records_pass_the_record_rules():
    check_playbook(DEFAULT_PLAYBOOK)


def test_no_bundled_record_says_what_a_historical_eval_rewards():
    """A record that named a squeeze or a borrow would pass a case's rubric for
    the narrator, and one that named the event would leak hindsight."""
    for record in DEFAULT_PLAYBOOK:
        text = f"{record.title} {record.guidance}".lower()
        for case in CASES.values():
            terms = [
                *(term for group in case.expected_keyword_groups for term in group),
                *case.expected_root_cause_keywords,
                *case.expected_action_themes,
                *case.hindsight_leak_markers,
            ]
            hits = [term for term in terms if term.lower() in text]
            assert not hits, f"{record.record_id} uses {case.test_id} rubric terms: {hits}"
            for item in ground_truth_news_for_case(case):
                assert item.title.lower() not in text


def _desk_record(**overrides) -> PlaybookRecord:
    base = dict(
        record_id="quote-noise",
        when="suppress_vega_narrative",
        title="The vol move sits inside the quote noise",
        guidance="Say the implied vol change cannot be told apart from bid-ask noise.",
    )
    return PlaybookRecord(**{**base, **overrides})


def test_a_desk_can_add_its_own_record():
    deps = GraphDeps(playbook=(*DEFAULT_PLAYBOOK, _desk_record()))
    assert [r.record_id for r in select_records({"suppress_vega_narrative": True}, deps.playbook)] == ["quote-noise"]


@pytest.mark.parametrize(
    ("overrides", "error"),
    [
        ({"guidance": "Flag any residual above 15 points."}, "digits"),
        ({"guidance": "Say the option now looks cheap."}, "trade or hedge wording: cheap"),
        ({"guidance": "Tell the desk to consider re-hedging the position."}, "trade or hedge wording"),
        ({"guidance": "Note that QuantLib does not model this."}, "names a pricing engine: quantlib"),
        ({"when": "residual_pct"}, "`when` must be one of"),
        ({"record_id": "terminal-break"}, "duplicate record_id"),
    ],
)
def test_a_desk_record_that_breaks_a_rule_is_refused(overrides, error):
    with pytest.raises(ValueError, match=error):
        GraphDeps(playbook=(*DEFAULT_PLAYBOOK, _desk_record(**overrides)))
