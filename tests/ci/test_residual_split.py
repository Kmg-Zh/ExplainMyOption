"""Two residuals and the escalation basis switch: Task A6.

ε_method (arithmetic, never news) vs ε_model (the only residual a catalyst
may explain), and which one drives escalation this run.
"""

from __future__ import annotations

from dataclasses import replace
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
from explain_my_option.report.reconciliation import build_reconciliation_facts, marks_reliable


def test_marks_reliable_labels():
    assert marks_reliable("tight")
    assert marks_reliable("normal")
    assert marks_reliable("reliable")  # this module's own live-path label
    assert not marks_reliable("wide")
    assert not marks_reliable("rejected")
    assert not marks_reliable(None)


def test_escalation_basis_is_model_with_reliable_marks_both_dates():
    """A6.5: with reliable marks on both dates the basis is 'model'."""
    snap = load_historical_case("aapl_exdiv_2023_real")
    assert snap.quote_tier_now in ("tight", "normal")
    assert snap.quote_tier_prev in ("tight", "normal")
    pricing = price_and_attribute(snap, config=engine_config_for_tests())
    rec = build_reconciliation_facts(snap, pricing)
    assert rec.marks_reliable_now and rec.marks_reliable_prev
    assert rec.escalation_basis == "model"
    assert rec.residual_model_usd is not None


def test_escalation_basis_falls_back_to_method_with_a_wide_tier():
    """A6.5: with a wide tier on either date it is 'method'."""
    snap = replace(load_historical_case("aapl_exdiv_2023_real"), quote_tier_prev="wide")
    pricing = price_and_attribute(snap, config=engine_config_for_tests())
    rec = build_reconciliation_facts(snap, pricing)
    assert not rec.marks_reliable_prev
    assert rec.escalation_basis == "method"
    assert rec.escalation_metric_pct == 100.0 * abs(rec.residual_method_usd) / abs(
        rec.model_pnl_usd
    )


def test_escalation_basis_is_method_on_the_live_fixture_path():
    """The live/fixture path never verifies t-1 marks, so it can never
    reach escalation_basis="model" -- conservative by construction, not a
    special case."""
    snap, surf = load_fixture("vol_crush")
    assert snap.quote_tier_prev is None
    pricing = price_and_attribute(snap, surface_data=surf, config=engine_config_for_tests())
    rec = build_reconciliation_facts(snap, pricing)
    assert not rec.marks_reliable_prev
    assert rec.escalation_basis == "method"


def test_residual_method_equals_pnl_residual_pnl():
    """A6.1: residual_method is pnl.residual_pnl (position-scaled, like the
    blotter's other dollar figures), unchanged in substance under a new name."""
    snap, surf = load_fixture("vol_crush")
    pricing = price_and_attribute(snap, surface_data=surf, config=engine_config_for_tests())
    rec = build_reconciliation_facts(snap, pricing)
    assert rec.residual_method_usd == pricing.pnl.residual_pnl * snap.position_scale()


if __name__ == "__main__":
    test_marks_reliable_labels()
    test_escalation_basis_is_model_with_reliable_marks_both_dates()
    test_escalation_basis_falls_back_to_method_with_a_wide_tier()
    test_escalation_basis_is_method_on_the_live_fixture_path()
    test_residual_method_equals_pnl_residual_pnl()
    print("OK — residual split / escalation basis tests passed")
