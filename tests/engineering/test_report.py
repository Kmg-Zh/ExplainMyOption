"""Report facts and Markdown: attribution shares, residual drill, reconciliation, goldens."""

from __future__ import annotations

import dataclasses
import os
import re

import pytest
from support import FAST, jpm_oct23_straddle

from explain_my_option.data.historical_chain import load_historical_case
from explain_my_option.data.synthetic import list_fixtures, load_fixture
from explain_my_option.graph.deps import OfficialFdmPnlSource
from explain_my_option.graph.diagnostic_controller import run_diagnostic_pass
from explain_my_option.intel.types import SearchPlan
from explain_my_option.paths import GOLDEN_DIR
from explain_my_option.pricing import price_and_attribute
from explain_my_option.pricing.types import Greeks, MarketSnapshot, PnLAttribution, PricingDiagnostics, PricingResult
from explain_my_option.report import PositionBundle, render_portfolio_report, render_position_report
from explain_my_option.report.blotter import build_quant_section
from explain_my_option.report.facts import build_portfolio_facts, build_position_facts
from explain_my_option.report.formatting import money, pct
from explain_my_option.report.reconciliation import build_reconciliation_facts, marks_reliable, quote_tier
from explain_my_option.report.settlement import render_settlement, render_settlements, settle
from explain_my_option.report.synthesis import fallback_synthesis


def _priced(name: str):
    if name.endswith("_real") or name.startswith("quiet_"):
        snap, surf = load_historical_case(name), None
    else:
        snap, surf = load_fixture(name)
    return snap, surf, price_and_attribute(snap, surf, config=FAST)


def _report(name: str, *, findings: dict | None = None, plan: SearchPlan | None = None, **snap_overrides) -> str:
    snap, surf, pricing = _priced(name)
    snap = dataclasses.replace(snap, **snap_overrides)
    facts = build_position_facts(snap, pricing)
    return render_position_report(facts, fallback_synthesis(facts, llm_unavailable=True), plan=plan, diagnostic_findings=findings)


def _table_share(report: str, label: str) -> str:
    row = next(line for line in report.splitlines() if line.startswith(f"| **{label}"))
    return row.split("|")[3].strip().strip("*")


ALL_CASES = [*list_fixtures(), "gme_squeeze_2021_real", "aapl_exdiv_2023_real", "quiet_aapl_2023-04-24"]


# --- Attribution shares ----------------------------------------------------------------


@pytest.mark.parametrize("name", ALL_CASES)
def test_every_share_carries_the_sign_of_its_dollar_amount(name):
    snap, _, pricing = _priced(name)
    facts = build_position_facts(snap, pricing)
    for row in facts.attribution:
        if abs(row.usd) > 1e-12:
            assert (row.share_pct > 0) == (row.usd > 0), (row.key, row.usd, row.share_pct)
    gross = sum(abs(r.usd) for r in facts.attribution)
    expected_total = 100.0 * facts.model_pnl_usd / (gross if facts.shares_of_gross else abs(facts.model_pnl_usd))
    assert facts.total_share_pct == pytest.approx(expected_total)


def test_a_real_loss_is_a_share_of_the_total_not_near_zero():
    """vol_crush loses $1.47 (-35% of the option): shares are of |ΔP|, signed."""
    report = _report("vol_crush")
    assert "near zero" not in report and "largely offset" not in report
    assert _table_share(report, "Vega PnL") == "-118.7%"
    assert _table_share(report, "Delta PnL") == "+18.1%"
    assert _table_share(report, "Total Model PnL") == "-100.0%"


def test_offsetting_components_switch_to_shares_of_gross_movement():
    """GME 2021-01-25: a -$3.35 delta loss against a +$5.69 vega gain nets to +$1.60."""
    report = _report("gme_squeeze_2021_real")
    assert "the components largely offset" in report
    assert _table_share(report, "Delta PnL") == "-31.1%"
    assert _table_share(report, "Vega PnL") == "+52.9%"
    assert _table_share(report, "Total Model PnL") == "+14.9%"


def test_headline_drivers_quote_the_table_shares():
    headline = next(line for line in _report("gme_squeeze_2021_real").splitlines() if "Primary drivers" in line)
    assert "**Vega PnL** (+52.9%)" in headline and "**Delta PnL** (-31.1%)" in headline


def test_percentages_over_a_near_zero_denominator_are_clamped():
    assert pct(6_582_029_380.9) == "+>1000%"
    assert pct(-2500.0) == "->1000%"
    assert pct(12.34, signed=False) == "12.3%"


@pytest.mark.parametrize("name", ["gme_squeeze_2021_real", "vol_crush"])
def test_the_iv_move_is_quoted_in_the_vols_the_engine_priced(name):
    """With marks, the engine prices at mark-calibrated vols; the report quotes those."""
    snap, _, pricing = _priced(name)
    facts = build_position_facts(snap, pricing)
    assert facts.iv_now - facts.iv_prev == pytest.approx(pricing.pnl.d_vol)
    vega_note = next(r.driver_note for r in facts.attribution if r.key == "vega")
    assert f"({facts.iv_prev * 100:.2f}% → {facts.iv_now * 100:.2f}%)" in vega_note


# --- Residual drill --------------------------------------------------------------------


def test_residual_drill_is_position_scaled_and_residual_after_nets_second_order():
    """Tool payloads are per option; the drill prints them at position size, and
    'Residual after' is the Taylor residual left once vanna and volga are added."""
    snap, surf, pricing = _priced("vol_crush")
    snap = dataclasses.replace(snap, quantity=2.0, multiplier=100.0)
    findings = run_diagnostic_pass(snap, pricing, surf, pnl=OfficialFdmPnlSource(config=FAST)).as_dict()
    facts = build_position_facts(snap, pricing)
    report = render_position_report(facts, fallback_synthesis(facts, llm_unavailable=True), diagnostic_findings=findings)

    combined = 200.0 * findings["results"]["taylor_second_order"]["combined_pnl"]
    residual = facts.attribution[-1].usd
    assert residual == pytest.approx(200.0 * pricing.pnl.residual_pnl)
    line = next(line for line in report.splitlines() if line.startswith("* Combined:"))
    assert line == f"* Combined: `{money(combined)}` | Residual after: `{money(residual - combined)}`"


# --- Sections and reconciliation ---------------------------------------------------------


def test_position_report_has_the_seven_sections():
    report = _report("vol_crush", plan=SearchPlan(skip_reason="below_materiality"))
    for heading in (
        "## 1. Headline",
        "## 2. Observation Lock",
        "## 3. Mark Reconciliation",
        "## 4. Quantitative PnL Attribution",
        "## 5. Residual Drill",
        "## 6. Root-Cause Market Intelligence",
        "## 7. Risk Watchlist",
    ):
        assert heading in report
    assert "_No catalyst search — move below materiality / observation lock._" in report


def _quoted_position(*, bid=9.8, ask=10.2, volume=500, open_interest=1000, iv_now=0.32, vega_now=0.20):
    snap = MarketSnapshot(
        ticker="TEST", option_type="call", strike=100.0, expiry="2027-01-15", spot_now=101.0, spot_prev=100.0,
        iv_now=iv_now, iv_prev=0.30, option_price_now=5.30, option_price_prev=5.00, time_to_expiry_years=0.5,
        bid=bid, ask=ask, mid=None if bid is None else (bid + ask) / 2, volume=volume, open_interest=open_interest,
        multiplier=100.0, data_source="yfinance", as_of="2026-08-30",
    )
    greeks = Greeks(price=5.0, delta=0.5, gamma=0.02, vega=vega_now, theta=-0.04)
    pricing = PricingResult(
        greeks_prev=greeks,
        greeks_now=dataclasses.replace(greeks, price=5.35),
        pnl=PnLAttribution(total_pnl=0.35, delta_pnl=0.5, gamma_pnl=0.01, vega_pnl=-0.1, theta_pnl=-0.04, residual_pnl=-0.02, d_spot=1.0, d_vol=iv_now - 0.30),
        diagnostics=PricingDiagnostics(data_source="yfinance", exercise_style="american"),
    )
    return snap, pricing


def test_mark_reconciliation_is_in_book_units():
    snap, pricing = _quoted_position()
    rec = build_reconciliation_facts(snap, pricing)
    assert rec.mark_pnl_usd == pytest.approx(30.0)  # (5.30 - 5.00) × 100
    assert rec.model_pnl_usd == pytest.approx(35.0)
    assert rec.model_vs_mark_gap_usd == pytest.approx(5.0)
    assert rec.residual_method_usd == pytest.approx(-2.0)  # pnl residual × 100, never news
    assert rec.residual_model_usd == pytest.approx(-5.0)  # market minus model
    report = render_position_report(build_position_facts(snap, pricing), fallback_synthesis(build_position_facts(snap, pricing)))
    assert "Model vs Mark gap" in report and "Quote tier" in report


@pytest.mark.parametrize(
    "spread_pct, volume, oi, tier",
    [(0.05, 500, 1000, "reliable"), (0.20, 500, 1000, "wide"), (0.05, 3, 1000, "thin"), (0.05, 500, 10, "thin"), (0.30, 2, 5, "wide+thin"), (None, None, None, "unquoted")],
)
def test_quote_tiers(spread_pct, volume, oi, tier):
    assert quote_tier(spread_pct, volume, oi) == tier


def test_iv_moves_inside_the_bid_ask_noise_band_are_not_attributable():
    """Noise band = half-spread / vega: 0.20 / 0.20 = 1 vol point."""
    inside = build_reconciliation_facts(*_quoted_position(iv_now=0.302))
    outside = build_reconciliation_facts(*_quoted_position(iv_now=0.35))
    assert inside.iv_noise_band_pts == pytest.approx(1.0) and inside.iv_move_within_noise is True
    assert outside.iv_move_within_noise is False and outside.observation_reliable
    unquoted = build_reconciliation_facts(*_quoted_position(bid=None, ask=None))
    assert unquoted.quote_tier == "unquoted" and unquoted.iv_noise_band_pts is None


def test_escalation_basis_is_the_model_residual_only_with_reliable_marks_on_both_dates():
    assert [marks_reliable(t) for t in ("tight", "normal", "reliable", "wide", None)] == [True, True, True, False, False]
    snap, _, pricing = _priced("aapl_exdiv_2023_real")
    assert build_reconciliation_facts(snap, pricing).escalation_basis == "model"
    wide = build_reconciliation_facts(dataclasses.replace(snap, quote_tier_prev="wide"), pricing)
    assert wide.escalation_basis == "method"
    assert wide.escalation_metric_pct == pytest.approx(100.0 * abs(wide.residual_method_usd) / abs(wide.model_pnl_usd))
    live = build_reconciliation_facts(*_quoted_position())
    assert live.escalation_basis == "method"  # the live path never verifies T-1 marks


def test_portfolio_report_rolls_up_the_legs():
    bundles, syntheses = [], []
    for name in ("vol_crush", "spot_gap"):
        snap, surf, pricing = _priced(name)
        bundles.append(PositionBundle(snapshot=snap, pricing=pricing))
        syntheses.append(fallback_synthesis(build_position_facts(snap, pricing)))
    pf = build_portfolio_facts(bundles)
    assert pf.position_count == 2
    assert pf.total_model_pnl == pytest.approx(sum(b.pricing.pnl.total_pnl for b in bundles))
    report = render_portfolio_report(bundles, syntheses)
    assert "## Portfolio Executive Summary" in report and "### Position 2" in report


# --- Expiry settlement -------------------------------------------------------------------


@pytest.mark.parametrize(
    "option_type, value, pnl, intrinsic_change, time_value",
    [("call", 0.0, -0.02, 0.0, -0.02), ("put", 18.42, 4.32, 4.96, -0.64)],
)
def test_settlement_is_intrinsic_at_the_close_and_splits_exactly(option_type, value, pnl, intrinsic_change, time_value):
    """JPM 350 straddle: 10-22 marks 0.02 / 14.10 at 336.54, expiry close 331.58."""
    s = settle(jpm_oct23_straddle(option_type))
    assert (s.value, s.pnl) == (pytest.approx(value), pytest.approx(pnl))
    assert (s.intrinsic_change, s.time_value_released) == (pytest.approx(intrinsic_change), pytest.approx(time_value))
    assert s.intrinsic_change + s.time_value_released == pytest.approx(s.pnl)
    assert s.position_pnl == pytest.approx(100 * pnl)
    report = render_settlement(s)
    assert f"| **Settlement PnL** | `{money(s.pnl)}` | `{money(s.position_pnl)}` |" in report


@pytest.mark.parametrize(
    "option_type, quantity, spot, outcome, delivery, pin",
    [
        ("put", 1.0, 331.58, "exercised", "sells 100 shares at 350", False),
        ("put", -1.0, 331.58, "assigned", "buys 100 shares at 350", False),
        ("call", -2.0, 351.0, "assigned", "sells 200 shares at 350", True),
        ("call", 1.0, 351.0, "exercised", "buys 100 shares at 350", True),
        ("call", 1.0, 349.995, "expired worthless", "no exercise, no stock delivery", True),
    ],
)
def test_settlement_names_exercise_assignment_and_pin(option_type, quantity, spot, outcome, delivery, pin):
    s = settle(dataclasses.replace(jpm_oct23_straddle(option_type), quantity=quantity, spot_now=spot))
    assert (s.outcome, s.pin) == (outcome, pin)
    assert delivery in s.delivery() and ("* Pin:" in render_settlement(s)) is pin


def test_settlement_without_a_prior_mark_reports_no_pnl():
    s = settle(dataclasses.replace(jpm_oct23_straddle("put"), option_price_prev=0.0))
    assert s.pnl is None and s.position_pnl is None
    assert "settlement PnL is not computed" in render_settlement(s)
    assert "| `JPM 350P 2026-10-23` | exercised | 18.4200 | n/a |" in render_settlements([s])


# --- Blotter goldens ---------------------------------------------------------------------

_GOLDEN_HEADER = "<!-- generated by tests/engineering/test_report.py (EMO_UPDATE_GOLDEN=1); do not edit -->\n\n"


def _mask_unstable_lines(text: str) -> str:
    """Pin these lines' presence, not their contents: Heston calibration is an optimizer
    whose digits vary across BLAS builds, and the QuantLib row tracks whichever release
    CI resolves under ``QuantLib>=1.43,<2`` (a release bump alone is not pricing drift)."""

    def mask(line: str) -> str:
        if line.startswith("- ") and "Heston" in line:
            return re.sub(r"-?\d+\.\d+(e-?\d+)?", "<num>", line)
        if line.startswith("| QuantLib |"):
            return "| QuantLib | <ver> |"
        return line

    return "\n".join(mask(line) for line in text.splitlines())


@pytest.mark.parametrize("name", sorted(p.stem for p in GOLDEN_DIR.glob("*.md")))
def test_blotter_matches_its_golden(name):
    snap, surf, pricing = _priced(name)
    text = _GOLDEN_HEADER + build_quant_section(snap, pricing) + "\n"
    path = GOLDEN_DIR / f"{name}.md"
    if os.getenv("EMO_UPDATE_GOLDEN") == "1":
        path.write_text(text)
    assert _mask_unstable_lines(path.read_text()) == _mask_unstable_lines(text)


def test_blotter_scales_quantity_not_engine_pnl():
    snap, _, pricing = _priced("vol_crush")
    per_option = pricing.pnl.total_pnl
    two = build_quant_section(dataclasses.replace(snap, quantity=2.0), pricing)
    assert "| Quantity | 2 |" in two and f"{abs(2 * per_option):,.4f}" in two
    assert pricing.pnl.total_pnl == per_option
