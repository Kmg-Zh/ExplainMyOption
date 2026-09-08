"""Report template renders mark reconciliation section."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import bootstrap

bootstrap.install()

from explain_my_option.pricing.types import Greeks, MarketSnapshot, PnLAttribution, PricingDiagnostics, PricingResult
from explain_my_option.report.facts import build_position_facts
from explain_my_option.report.schema import DiagnosticSynthesis
from explain_my_option.report.template import render_position_report


def _facts_with_quotes() -> tuple:
    snap = MarketSnapshot(
        ticker="AAPL",
        option_type="call",
        strike=150.0,
        expiry="2026-09-24",
        spot_now=147.0,
        spot_prev=145.0,
        iv_now=0.26,
        iv_prev=0.24,
        option_price_now=3.8,
        option_price_prev=2.5,
        time_to_expiry_years=0.2,
        bid=3.70,
        ask=3.90,
        volume=800,
        open_interest=5000,
        quantity=1,
        multiplier=100,
        data_source="synthetic",
        as_of="2026-08-30",
    )
    pricing = PricingResult(
        greeks_prev=Greeks(price=2.5, delta=0.65, gamma=0.008, vega=45.0, theta=-0.03),
        greeks_now=Greeks(price=3.8, delta=0.68, gamma=0.008, vega=45.0, theta=-0.03),
        pnl=PnLAttribution(
            total_pnl=1.30,
            delta_pnl=0.80,
            gamma_pnl=0.10,
            vega_pnl=0.35,
            theta_pnl=-0.03,
            residual_pnl=0.08,
            d_spot=2.0,
            d_vol=0.02,
        ),
        diagnostics=PricingDiagnostics(
            data_source="synthetic",
            exercise_style="american",
            engine="fdm_flat",
            mark_calibrated=True,
        ),
    )
    return snap, pricing


def test_report_shows_mark_reconciliation_section():
    snap, pricing = _facts_with_quotes()
    facts = build_position_facts(snap, pricing)
    synthesis = DiagnosticSynthesis(
        primary_driver="Vega",
        verdict="Test verdict.",
        confidence_level="high",
        confidence_rationale="Test.",
        evidence=[],
        takeaways=[],
        american_commentary="",
    )
    report = render_position_report(facts, synthesis)
    assert "## 3. Mark Reconciliation" in report
    assert "Model vs Mark gap" in report
    assert "Quote tier" in report or "Observation Lock" in report


if __name__ == "__main__":
    test_report_shows_mark_reconciliation_section()
    print("OK — report reconciliation tests passed")
