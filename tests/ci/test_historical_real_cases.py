"""The two verified real historical cases: Task A4.5.

Offline -- reads the committed slices under tests/ci/fixtures/historical/
(written by ``scripts/fetch_chains.py`` against live DoltHub + yfinance)
rather than hitting the network in CI. Re-fetch with::

    python scripts/fetch_chains.py

Only these two cases are confirmed convertible to real chains; do not add
others here without independently re-verifying per docs/dev/DATA_SOURCES.md.
"""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from ci.engine_config import engine_config_for_tests
from explain_my_option.data.historical_chain import load_historical_case
from explain_my_option.data.observation import check_basis_consistency
from explain_my_option.pricing.facade import price_and_attribute
from explain_my_option.report.facts import build_position_facts
from explain_my_option.report.reconciliation import build_reconciliation_facts


def test_gme_squeeze_2021_real_is_a_real_squeeze():
    """A4.5: IV 276%->369%-ballpark, borrow_regime extreme, A3.5 passes."""
    snap = load_historical_case("gme_squeeze_2021_real")
    assert snap.data_source == "historical"
    assert snap.ticker == "GME"

    # A3.5 must pass before this case is trusted (GME predates the
    # 2022-07-22 4-for-1 split) -- it ran once already inside the adapter's
    # own fetch; re-run here against the frozen numbers so a future change
    # to check_basis_consistency's thresholds re-validates this case too.
    basis = check_basis_consistency(
        spot=snap.spot_now,
        rate=snap.risk_free_rate,
        time_to_expiry_years=snap.time_to_expiry_years,
        put_mid=snap.mid,
        put_strike=snap.strike,
    )
    assert basis.ok, (basis.failing_invariant, basis.detail)

    assert snap.iv_now > 2.0 and snap.iv_prev > 2.0  # squeeze-level IV, both dates
    assert snap.dividend_yield > 0.20  # borrow_regime = extreme (>20%)

    pricing = price_and_attribute(snap, config=engine_config_for_tests())
    reconciliation = build_reconciliation_facts(snap, pricing)
    # Both dates' IV were inverted to match the real mid exactly (A4.4), so
    # the mark-calibrated model price should reconcile to ~$0 gap.
    assert reconciliation.mark_calibrated
    assert reconciliation.model_vs_mark_gap_usd is not None
    assert abs(reconciliation.model_vs_mark_gap_usd) < 1e-2


def test_aapl_exdiv_2023_real_reports_ee_relevant_false():
    """A4.5: real dividend, real marks; ee_relevant is honestly False here."""
    snap = load_historical_case("aapl_exdiv_2023_real")
    assert snap.data_source == "historical"
    assert snap.ticker == "AAPL"
    assert len(snap.discrete_dividends) == 1
    assert snap.discrete_dividends[0].ex_date == "2023-11-10"
    assert abs(snap.discrete_dividends[0].amount - 0.24) < 1e-9

    basis = check_basis_consistency(
        spot=snap.spot_now,
        rate=snap.risk_free_rate,
        time_to_expiry_years=snap.time_to_expiry_years,
        call_mid=snap.mid,
        call_strike=snap.strike,
    )
    assert basis.ok, (basis.failing_invariant, basis.detail)

    pricing = price_and_attribute(snap, config=engine_config_for_tests())
    facts = build_position_facts(snap, pricing)
    am = facts.american

    # The spec's own prediction: AAPL's yield is low, so this is a
    # carry/theta case, not an early-exercise case -- and it must be
    # reported as such, not worked around.
    assert am.ee_relevant is False
    assert am.dividend_coverage is not None and am.dividend_coverage < 1.0
    assert "carry/theta case" in am.early_exercise_assessment


if __name__ == "__main__":
    test_gme_squeeze_2021_real_is_a_real_squeeze()
    test_aapl_exdiv_2023_real_reports_ee_relevant_false()
    print("OK — real historical case tests passed")
