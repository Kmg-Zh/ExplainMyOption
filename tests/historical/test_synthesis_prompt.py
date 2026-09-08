"""Governed synthesis human prompt includes full desk blotter."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


from bootstrap import install

install()

from explain_my_option.data.synthetic import load_fixture
from explain_my_option.graph.prompts import STRUCTURED_DIAGNOSE_SYSTEM_PROMPT
from explain_my_option.report.facts import build_position_facts
from explain_my_option.pipeline.digest import empty_digest
from explain_my_option.report.synthesis import _human_prompt
from ci.engine_config import engine_config_for_tests
from explain_my_option.pricing.facade import price_and_attribute
from historical.cases import frozen_news_for_case, load_cases

CFG = engine_config_for_tests()


def test_human_prompt_includes_desk_blotter():
    case = load_cases()[0]
    snap, surf = load_fixture(case.fixture)
    pricing = price_and_attribute(snap, surf, None, config=CFG)
    news = frozen_news_for_case(case)
    facts = build_position_facts(snap, pricing, news_count=len(news))
    human = _human_prompt(snap, pricing, facts, news, None, {})
    assert "## Desk blotter (read-only)" in human
    assert "Full quant blotter (engine output)" in human
    assert "Factor PnL (Greek-based Taylor" in human
    assert news[0].title in human
    assert "Layer B — intel digest" in human
    assert "iv crush" in human.lower()


def test_system_prompt_is_two_layer_not_mutex():
    text = STRUCTURED_DIAGNOSE_SYSTEM_PROMPT.lower()
    assert "layer a" in text
    assert "layer b" in text
    assert "not mutually exclusive" in text or "additive" in text
    assert "QuantLib American" in STRUCTURED_DIAGNOSE_SYSTEM_PROMPT
    assert "residual" in text
    assert "Taylor" in STRUCTURED_DIAGNOSE_SYSTEM_PROMPT
    assert "hv20" not in text


def test_human_prompt_infers_gme_borrow_and_vow_squeeze_from_tape():
    by_id = {c.test_id: c for c in load_cases()}
    empty = {
        "intel_digest": empty_digest(reason="digester role not configured").model_dump(),
        "observation_reliable": True,
    }
    for test_id, required in (
        ("gme_squeeze_2021", ("squeeze", "borrow")),
        ("vow_float_squeeze_2008", ("float", "squeeze")),
    ):
        case = by_id[test_id]
        snap, surf = load_fixture(case.fixture)
        pricing = price_and_attribute(snap, surf, None, config=CFG)
        news = frozen_news_for_case(case)
        facts = build_position_facts(snap, pricing, news_count=len(news))
        human = _human_prompt(snap, pricing, facts, news, None, empty)
        blob = human.lower()
        for token in required:
            assert token in blob, (test_id, token, human)


if __name__ == "__main__":
    test_human_prompt_includes_desk_blotter()
    test_system_prompt_is_two_layer_not_mutex()
    test_human_prompt_infers_gme_borrow_and_vow_squeeze_from_tape()
    print("OK — synthesis prompt checks passed")
