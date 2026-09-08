"""Ladder regression: Layers 3–4, diagnostic routing, as-of day-count."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import bootstrap

bootstrap.install()

from datetime import timedelta

from explain_my_option.data.synthetic import load_fixture
from explain_my_option.graph.diagnostic_controller import run_diagnostic_pass
from explain_my_option.pricing.analysis_api import path_reprice, taylor_second_order
from ci.engine_config import engine_config_for_tests
from explain_my_option.pricing.facade import _calendar_days_elapsed, price_and_attribute
from explain_my_option.pricing.types import MarketSnapshot
from explain_my_option.pricing.sequential_reval import sequential_full_revaluation

CFG = engine_config_for_tests()


def test_sequential_reval_telescopes_to_model_pnl():
    snap, surf = load_fixture("spot_gap")
    result = price_and_attribute(snap, surf, config=CFG)
    seq = sequential_full_revaluation(
        snap,
        model_total_pnl=result.pnl.total_pnl,
        config=CFG,
        iv_now=result.diagnostics.effective_iv_now,
        iv_prev=result.diagnostics.effective_iv_prev,
        engine_id=result.diagnostics.engine,
        surface=surf,
    )
    assert abs(seq.step_sum - seq.model_total_pnl) < 0.05, seq.as_dict()
    assert abs(seq.residual_vs_model) < 0.05


def test_taylor_second_order_returns_buckets():
    snap, surf = load_fixture("vol_crush")
    result = price_and_attribute(snap, surf, config=CFG)
    second = taylor_second_order(snap, result, config=CFG)
    assert hasattr(second, "vanna_pnl")
    assert hasattr(second, "volga_pnl")


def test_calendar_days_from_prev_as_of():
    snap = MarketSnapshot(
        ticker="T",
        option_type="call",
        strike=100.0,
        expiry="2027-01-15",
        spot_now=100.0,
        spot_prev=99.0,
        iv_now=0.3,
        iv_prev=0.3,
        option_price_now=0.0,
        option_price_prev=0.0,
        time_to_expiry_years=0.5,
        as_of="2026-08-17",
        prev_as_of="2026-08-14",
        data_source="synthetic",
    )
    assert _calendar_days_elapsed(snap) == 3.0


def test_diagnostic_pass_records_skipped_tools():
    snap, surf = load_fixture("spot_gap")
    result = price_and_attribute(snap, surf, config=CFG)
    findings = run_diagnostic_pass(snap, result, surf, config=CFG)
    assert findings.tool_calls_used <= 3
    d = findings.as_dict()
    assert "skipped_tools" in d


if __name__ == "__main__":
    test_sequential_reval_telescopes_to_model_pnl()
    test_taylor_second_order_returns_buckets()
    test_calendar_days_from_prev_as_of()
    test_diagnostic_pass_records_skipped_tools()
    print("OK — ladder regression tests passed")
