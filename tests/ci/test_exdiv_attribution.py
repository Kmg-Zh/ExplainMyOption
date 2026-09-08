"""Ex-div FO attribution overlay — American FDM vs European, not a trading edge."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

import bootstrap

bootstrap.install()

from explain_my_option.data.synthetic import load_fixture
from explain_my_option.graph.diagnostic_controller import run_diagnostic_pass
from explain_my_option.graph.diagnostic_tools import american_dividend_exercise_check
from explain_my_option.pricing.ql_engine import price_european_flat
from explain_my_option.report.facts import build_position_facts
from explain_my_option.report.schema import DiagnosticSynthesis
from explain_my_option.report.synthesis import apply_american_commentary_policy
from explain_my_option.report.template import render_position_report
from ci.engine_config import engine_config_for_tests
from explain_my_option.pricing.facade import price_and_attribute

CFG = engine_config_for_tests()


def _price(name: str):
    snap, surf = load_fixture(name)
    pricing = price_and_attribute(snap, surf, None, config=CFG)
    return snap, surf, pricing


def test_european_and_american_differ_near_large_div():
    snap, _, pricing = _price("deep_itm_exdiv")
    am_now = pricing.greeks_now.price
    eu = price_european_flat(
        spot=snap.spot_now,
        strike=snap.strike,
        rate=snap.risk_free_rate,
        dividend_yield=snap.dividend_yield,
        vol=snap.iv_now,
        expiry=snap.expiry,
        eval_date=snap.as_of,
        option_type=snap.option_type,  # type: ignore[arg-type]
        discrete_dividends=(),
    )
    assert abs(am_now - eu.price) > 0.01, (am_now, eu.price)
    ee = pricing.diagnostics.early_exercise_premium
    assert ee is not None
    # Floored at 0 when American FDM with cash divs prints below no-div European.


def test_exdiv_overlay_and_tool_reason_on_aapl_and_synthetic():
    for name in ("aapl_exdiv_2023", "deep_itm_exdiv"):
        snap, surf, pricing = _price(name)
        preview = american_dividend_exercise_check(snap, pricing)
        assert preview["flag_ex_div_window"] is True
        findings = run_diagnostic_pass(snap, pricing, surf, config=CFG)
        split = findings.ex_div_attribution
        assert split is not None
        assert split["flag_ex_div_window"] is True
        assert "spot_drop" in split
        assert "dividend_amount" in split
        assert "ee_premium_now" in split
        assert "vega_pnl" in split
        assert "residual_pnl" in split
        ran = "american_dividend_exercise_check" in findings.tools_run
        skipped = [
            s for s in findings.skipped_tools if s.name == "american_dividend_exercise_check"
        ]
        assert ran or skipped, findings.as_dict()
        if skipped:
            assert skipped[0].reason

        facts = build_position_facts(snap, pricing)
        syn = DiagnosticSynthesis(
            primary_driver="Delta / spot move",
            verdict="Ex-div window; Taylor residual remains after the spot drop.",
            confidence_level="medium",
            confidence_rationale="American overlay is code-derived.",
            evidence=[],
            takeaways=["Watch assignment near the ex-div window."],
            american_commentary="Early exercise looks likely.",
        )
        syn = apply_american_commentary_policy(syn, facts)
        if split["ee_premium_material"]:
            assert syn.american_commentary
            assert "early-exercise" in syn.american_commentary.lower() or "early exercise" in syn.american_commentary.lower()
        else:
            assert "early exercise" not in syn.american_commentary.lower()
        report = render_position_report(
            facts, syn, diagnostic_findings=findings.as_dict()
        )
        assert "Ex-div attribution overlay" in report
        assert "official PnL stays American FDM" in report


def test_american_commentary_blank_when_premium_not_material():
    from explain_my_option.pricing.types import (
        Greeks,
        MarketSnapshot,
        PnLAttribution,
        PricingDiagnostics,
        PricingResult,
    )

    snap = MarketSnapshot(
        ticker="SYN",
        option_type="call",
        strike=100.0,
        expiry="2027-01-15",
        spot_now=100.0,
        spot_prev=100.0,
        iv_now=0.20,
        iv_prev=0.20,
        option_price_now=5.0,
        option_price_prev=5.0,
        time_to_expiry_years=0.5,
        data_source="synthetic",
        as_of="2026-08-30",
    )
    pricing = PricingResult(
        greeks_prev=Greeks(price=5.0, delta=0.5, gamma=0.02, vega=0.1, theta=-0.04),
        greeks_now=Greeks(price=5.0, delta=0.5, gamma=0.02, vega=0.1, theta=-0.04),
        pnl=PnLAttribution(
            total_pnl=0.0,
            delta_pnl=0.0,
            gamma_pnl=0.0,
            vega_pnl=0.0,
            theta_pnl=0.0,
            residual_pnl=0.0,
            d_spot=0.0,
            d_vol=0.0,
        ),
        diagnostics=PricingDiagnostics(
            data_source="synthetic",
            exercise_style="american",
            early_exercise_premium=0.0,
        ),
    )
    facts = build_position_facts(snap, pricing)
    syn = DiagnosticSynthesis(
        primary_driver="Vega / implied volatility",
        verdict="Vol repricing dominated.",
        confidence_level="medium",
        confidence_rationale="IV moved.",
        evidence=[],
        takeaways=["Monitor crush."],
        american_commentary="Early exercise risk into the print.",
    )
    out = apply_american_commentary_policy(syn, facts)
    assert out.american_commentary == ""


if __name__ == "__main__":
    test_european_and_american_differ_near_large_div()
    test_exdiv_overlay_and_tool_reason_on_aapl_and_synthetic()
    test_american_commentary_blank_when_premium_not_material()
    print("OK — ex-div attribution tests passed")
