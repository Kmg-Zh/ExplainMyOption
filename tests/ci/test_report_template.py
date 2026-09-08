"""Report template: reconciliation, validation, portfolio roll-up."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


from bootstrap import install

install()

from explain_my_option.data.synthetic import list_fixtures, load_fixture
from ci.engine_config import engine_config_for_tests
from explain_my_option.pricing.facade import price_and_attribute
from explain_my_option.report.facts import PositionBundle, build_portfolio_facts, build_position_facts
from explain_my_option.report.schema import DiagnosticSynthesis, EvidenceItem
from explain_my_option.report.synthesis import fallback_synthesis
from explain_my_option.intel.types import SearchPlan
from explain_my_option.report.template import render_portfolio_report, render_position_report
from explain_my_option.report.validate import validate_synthesis

CFG = engine_config_for_tests()


def test_attribution_reconciles_with_gamma():
    for name in list_fixtures():
        snap, surf = load_fixture(name)
        result = price_and_attribute(snap, surf, config=CFG)
        pnl = result.pnl
        recon = pnl.delta_pnl + pnl.gamma_pnl + pnl.vega_pnl + pnl.theta_pnl + pnl.residual_pnl
        assert abs(recon - pnl.total_pnl) < 1e-8, name


def test_position_report_has_seven_sections():
    snap, surf = load_fixture("vol_crush")
    result = price_and_attribute(snap, surf, config=CFG)
    facts = build_position_facts(snap, result)
    syn = fallback_synthesis(facts, llm_unavailable=True)
    md = render_position_report(facts, syn)
    for heading in (
        "## 1. Headline",
        "## 2. Observation Lock",
        "## 3. Mark Reconciliation",
        "## 4. Quantitative PnL Attribution",
        "## 5. Residual Drill",
        "## 6. Root-Cause Market Intelligence",
        "## 7. Trading Desk Watchlist",
    ):
        assert heading in md, heading
    assert "Gamma PnL" in md


def test_section_six_skips_catalyst_search_when_plan_empty():
    snap, surf = load_fixture("vol_crush")
    result = price_and_attribute(snap, surf, config=CFG)
    facts = build_position_facts(snap, result)
    syn = fallback_synthesis(facts, llm_unavailable=True)
    plan = SearchPlan(queries=[], skip_reason="below_materiality")
    md = render_position_report(facts, syn, plan=plan)
    assert "_No catalyst search — move below materiality / observation lock._" in md


def test_validate_rejects_numeric_hallucination():
    bad = DiagnosticSynthesis(
        primary_driver="Vega",
        verdict="The option gained $2.45 on a 12% move.",
        confidence_level="high",
        confidence_rationale="Clean marks.",
        evidence=[],
        takeaways=[],
    )
    errors = validate_synthesis(bad)
    assert errors


def test_validate_accepts_clean_synthesis():
    good = DiagnosticSynthesis(
        primary_driver="Vega contraction",
        verdict="Volatility repricing dominated after the catalyst window.",
        confidence_level="medium",
        confidence_rationale="Prior IV mark is a proxy; news sparse.",
        evidence=[
            EvidenceItem(
                headline="Earnings preview",
                source="Reuters",
                relevance="Explains vol bid into the event.",
            )
        ],
        takeaways=["Hedge vega into the print."],
    )
    assert validate_synthesis(good) == []


def test_portfolio_report_multi_position():
    bundles: list[PositionBundle] = []
    syntheses: list[DiagnosticSynthesis] = []
    for name in ("vol_crush", "spot_gap"):
        snap, surf = load_fixture(name)
        pricing = price_and_attribute(snap, surf, config=CFG)
        bundles.append(PositionBundle(snapshot=snap, pricing=pricing))
        facts = build_position_facts(snap, pricing)
        syntheses.append(fallback_synthesis(facts, llm_unavailable=True))

    pf = build_portfolio_facts(bundles)
    assert pf.position_count == 2
    md = render_portfolio_report(bundles, syntheses)
    assert "# Portfolio Option Diagnostic Report" in md
    assert "## Portfolio Executive Summary" in md
    assert "### Position 1" in md
    assert "### Position 2" in md


if __name__ == "__main__":
    test_attribution_reconciles_with_gamma()
    test_position_report_has_seven_sections()
    test_section_six_skips_catalyst_search_when_plan_empty()
    test_validate_rejects_numeric_hallucination()
    test_validate_accepts_clean_synthesis()
    test_portfolio_report_multi_position()
    print("OK — report template checks passed")
