"""Benchmark compare helpers — desk packet unit test (offline-safe)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from historical.baseline_agent import format_desk_packet
from historical.pipeline_position import (
    PIPELINE_MULTIPLIER,
    apply_pipeline_position,
)
from explain_my_option.report.facts import build_position_facts
from historical.compare import run_comparison_case, summarize_rows
from historical.cases import frozen_news_for_case, load_cases
from explain_my_option.data.synthetic import load_fixture
from ci.engine_config import engine_config_for_tests
from explain_my_option.pricing.facade import price_and_attribute

CFG = engine_config_for_tests()


def test_desk_packet_includes_greeks_and_pnl():
    case = load_cases()[0]
    snap, surf = load_fixture(case.fixture)
    apply_pipeline_position(snap)
    pricing = price_and_attribute(snap, surf, None, config=CFG)
    news = frozen_news_for_case(case)
    packet = format_desk_packet(snap, pricing, news)
    assert "Delta:" in packet
    assert "Factor PnL" in packet
    assert "Full quant blotter" in packet
    assert case.ticker in packet
    assert "Desk color" not in packet
    assert case.input_text not in packet


def test_pipeline_position_matches_run_pipeline_defaults():
    case = load_cases()[0]
    snap, surf = load_fixture(case.fixture)
    raw_mult = snap.multiplier
    apply_pipeline_position(snap)
    assert snap.quantity == 1.0
    assert snap.multiplier == PIPELINE_MULTIPLIER
    pricing_aligned = price_and_attribute(snap, surf, None, config=CFG)
    facts_aligned = build_position_facts(snap, pricing_aligned)
    if raw_mult != PIPELINE_MULTIPLIER:
        snap_raw, _ = load_fixture(case.fixture)
        pricing_raw = price_and_attribute(snap_raw, surf, None, config=CFG)
        facts_raw = build_position_facts(snap_raw, pricing_raw)
        assert facts_aligned.model_pnl_usd != facts_raw.model_pnl_usd


def test_comparison_suite_live_smoke():
    """Opt-in live comparison. Set EMO_BENCHMARK_LIVE=1 and OPENAI_API_KEY."""
    if os.getenv("EMO_BENCHMARK_LIVE", "0") != "1":
        return
    case = load_cases()[0]
    row = run_comparison_case(case)
    assert row.governed_report_path
    assert row.baseline_report_path
    assert not row.baseline["used_fallback"]
    summary = summarize_rows([row])
    assert summary["case_count"] == 1


if __name__ == "__main__":
    test_desk_packet_includes_greeks_and_pnl()
    test_comparison_suite_live_smoke()
    print("OK — historical desk-packet checks passed")
