"""Mixed portfolio: offline CI book + helpers for the live multi-day e2e experiment.

Test-only. Product code stays in ``src/``. Live end-to-end::

    python tests/live_book/portfolio_e2e.py --live
    ./scripts/run-portfolio-e2e.sh
"""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


from bootstrap import install

install()

from live_book.portfolio_book import (
    DEFAULT_PINNED_BOOK,
    OFFLINE_AS_OF,
    OFFLINE_LEGS,
    load_pinned_book,
)
from live_book.portfolio_e2e import (
    build_offline_bundles,
    run_offline_portfolio_e2e,
)
from live_book.strikes import pick_strike, target_spot_for_moneyness
from explain_my_option.data.synthetic import load_fixture
from ci.engine_config import engine_config_for_tests
from explain_my_option.pricing.facade import price_and_attribute
from explain_my_option.report.facts import build_portfolio_facts
from explain_my_option.report.template import render_portfolio_report

CFG = engine_config_for_tests()


def test_strike_moneyness_targets():
    assert target_spot_for_moneyness(100.0, "call", "ATM") == 100.0
    assert target_spot_for_moneyness(100.0, "call", "ITM", distance_pct=0.05) == 95.0
    assert target_spot_for_moneyness(100.0, "call", "OTM", distance_pct=0.05) == 105.0
    assert target_spot_for_moneyness(100.0, "put", "ITM", distance_pct=0.05) == 105.0
    assert target_spot_for_moneyness(100.0, "put", "OTM", distance_pct=0.05) == 95.0


def test_pick_strike_from_grid():
    import pandas as pd

    chain = pd.DataFrame({"strike": [90.0, 95.0, 100.0, 105.0, 110.0]})
    assert pick_strike(chain, 100.0, "call", "ATM") == 100.0
    assert pick_strike(chain, 100.0, "call", "ITM", distance_pct=0.05) == 95.0
    assert pick_strike(chain, 100.0, "put", "OTM", distance_pct=0.05) == 95.0


def test_portfolio_legs_reconcile():
    for leg in OFFLINE_LEGS:
        snap, surf = load_fixture(leg.fixture)
        snap.ticker = leg.ticker
        for key, val in leg.overrides.items():
            setattr(snap, key, val)
        result = price_and_attribute(snap, surf, config=CFG)
        pnl = result.pnl
        recon = (
            pnl.delta_pnl
            + pnl.gamma_pnl
            + pnl.vega_pnl
            + pnl.theta_pnl
            + pnl.residual_pnl
        )
        assert abs(recon - pnl.total_pnl) < 1e-8, leg.ticker


def test_portfolio_same_as_of_and_diversity():
    bundles, _ = build_offline_bundles(config=CFG)
    as_ofs = {b.snapshot.as_of for b in bundles}
    assert as_ofs == {OFFLINE_AS_OF}

    styles = {b.snapshot.exercise_style for b in bundles}
    assert "american" in styles and "european" in styles

    tickers = [b.snapshot.ticker for b in bundles]
    assert len(tickers) == len(set(tickers)), "each leg uses a distinct ticker"

    pf = build_portfolio_facts(bundles)
    assert pf.position_count == len(OFFLINE_LEGS)
    assert pf.eval_date == OFFLINE_AS_OF
    assert len(pf.tickers) == len(OFFLINE_LEGS)


def test_portfolio_dividend_legs_show_early_exercise_signal():
    bundles, _ = build_offline_bundles(config=CFG)
    by_ticker = {b.snapshot.ticker: b for b in bundles}
    for ticker in ("XOM", "KO", "JPM"):
        prem = by_ticker[ticker].pricing.diagnostics.early_exercise_premium
        assert prem is not None and prem >= 0.0, ticker


def test_portfolio_report_structure():
    bundles, syntheses = build_offline_bundles(config=CFG)
    md = render_portfolio_report(bundles, syntheses)
    assert "# Portfolio Option Diagnostic Report" in md
    assert "## Portfolio Executive Summary" in md
    assert "### Aggregate factor attribution" in md
    assert f"**Analysis Date**: `{OFFLINE_AS_OF}`" in md
    for i in range(1, len(OFFLINE_LEGS) + 1):
        assert f"### Position {i}" in md
    assert "AAPL" in md and "GOOGL" in md and "KO" in md


def test_pinned_book_has_ten_fixed_contracts():
    baseline, legs = load_pinned_book()
    assert baseline == "2026-09-01"
    assert DEFAULT_PINNED_BOOK.is_file()
    assert len(legs) == 10
    tickers = [leg.ticker for leg in legs]
    assert len(tickers) == len(set(tickers))
    # Same product identity fields tomorrow must keep.
    for leg in legs:
        assert leg.strike > 0
        assert leg.expiry
        assert leg.option_type in ("call", "put")
        assert leg.exercise_style in ("american", "european")
    # Spot-check contracts from the 2026-09-01 live pin.
    by_ticker = {leg.ticker: leg for leg in legs}
    assert by_ticker["AAPL"].strike == 300.0
    assert by_ticker["AAPL"].expiry == "2026-09-02"
    assert by_ticker["META"].quantity == 2.0 and by_ticker["META"].multiplier == 100.0
    assert by_ticker["GOOGL"].exercise_style == "european"
    assert by_ticker["SPY"].expiry == "2026-09-02"
    assert by_ticker["XOM"].expiry == "2026-09-04"


def test_offline_e2e_archives_run():
    run_dir = run_offline_portfolio_e2e(through_graph=False)
    assert (run_dir / "manifest.json").is_file()
    assert (run_dir / "portfolio_report.md").is_file()
    assert (run_dir / "legs").is_dir()
    leg_files = list((run_dir / "legs").glob("*.json"))
    assert len(leg_files) == len(OFFLINE_LEGS)
    assert "live_book" in run_dir.parts
    assert run_dir.name == "offline"


if __name__ == "__main__":
    test_strike_moneyness_targets()
    test_pick_strike_from_grid()
    test_portfolio_legs_reconcile()
    test_portfolio_same_as_of_and_diversity()
    test_portfolio_dividend_legs_show_early_exercise_signal()
    test_portfolio_report_structure()
    test_pinned_book_has_ten_fixed_contracts()
    test_offline_e2e_archives_run()
    pf = build_portfolio_facts(build_offline_bundles(config=CFG)[0])
    print(f"OK — {pf.position_count} legs, total PnL {pf.total_pnl:+.4f}")
