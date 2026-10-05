"""Quant-path determinism (Task B3): the same fixture, run 3x, must produce
bit-identical blotter values.

No LLM involved here -- this is pricing + attribution + PositionFacts only.
Any variation across runs is a real bug (uninitialised RNG, dict ordering,
wall-clock leaking into a as-of-less snapshot's day-count), not something to
loosen a tolerance around.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from ci.engine_config import engine_config_for_tests
from explain_my_option.data.historical_chain import load_historical_case
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.pricing.facade import price_and_attribute
from explain_my_option.report.facts import build_position_facts

CFG = engine_config_for_tests()


def _run_once(source: str):
    if source in ("aapl_exdiv_2023_real", "gme_squeeze_2021_real", "quiet_aapl_2023-04-24"):
        snap = load_historical_case(source)
        surf = None
    else:
        snap, surf = load_fixture(source)
    pricing = price_and_attribute(snap, surface_data=surf, config=CFG)
    facts = build_position_facts(snap, pricing)
    return pricing.as_dict(), asdict(facts)


def _assert_bit_identical(source: str):
    runs = [_run_once(source) for _ in range(3)]
    pricing0, facts0 = runs[0]
    for pricing_i, facts_i in runs[1:]:
        assert pricing_i == pricing0, f"{source}: pricing.as_dict() differs across runs"
        assert facts_i == facts0, f"{source}: PositionFacts differs across runs"


def test_synthetic_fixture_is_bit_identical_across_three_runs():
    _assert_bit_identical("aapl_exdiv_2023")


def test_american_put_div_fixture_is_bit_identical_across_three_runs():
    _assert_bit_identical("american_put_div")


def test_real_historical_case_is_bit_identical_across_three_runs():
    _assert_bit_identical("aapl_exdiv_2023_real")


def test_real_squeeze_case_is_bit_identical_across_three_runs():
    _assert_bit_identical("gme_squeeze_2021_real")


if __name__ == "__main__":
    test_synthetic_fixture_is_bit_identical_across_three_runs()
    test_american_put_div_fixture_is_bit_identical_across_three_runs()
    test_real_historical_case_is_bit_identical_across_three_runs()
    test_real_squeeze_case_is_bit_identical_across_three_runs()
    print("OK — quant-path determinism tests passed")
