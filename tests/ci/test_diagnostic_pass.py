"""Bounded diagnostic_pass controller and graph wiring."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import bootstrap

bootstrap.install()

from explain_my_option.graph.diagnostic_controller import MAX_DIAGNOSTIC_TOOL_CALLS, run_diagnostic_pass
from explain_my_option.pricing.types import (
    DiscreteDividend,
    Greeks,
    MarketSnapshot,
    PnLAttribution,
    PricingDiagnostics,
    PricingResult,
)


def _snap(**kw) -> MarketSnapshot:
    base = dict(
        ticker="TEST",
        option_type="call",
        strike=100.0,
        expiry="2027-01-15",
        spot_now=105.0,
        spot_prev=100.0,
        iv_now=0.32,
        iv_prev=0.30,
        option_price_now=5.30,
        option_price_prev=5.00,
        time_to_expiry_years=0.5,
        bid=9.80,
        ask=10.20,
        volume=500.0,
        open_interest=1000.0,
        quantity=1.0,
        multiplier=100.0,
        data_source="synthetic",
        as_of="2026-08-30",
    )
    base.update(kw)
    return MarketSnapshot(**base)


def _pricing(**kw) -> PricingResult:
    pnl_kw = kw.pop("pnl", {})
    residual = float(pnl_kw.get("residual_pnl", 0.05))
    total = float(pnl_kw.get("total_pnl", 0.35))
    return PricingResult(
        greeks_prev=Greeks(price=5.0, delta=0.5, gamma=0.02, vega=0.20, theta=-0.04),
        greeks_now=Greeks(price=5.35, delta=0.52, gamma=0.02, vega=0.20, theta=-0.04),
        pnl=PnLAttribution(
            total_pnl=total,
            delta_pnl=0.20,
            gamma_pnl=0.05,
            vega_pnl=0.04,
            theta_pnl=-0.01,
            residual_pnl=residual,
            d_spot=5.0,
            d_vol=0.02,
        ),
        diagnostics=PricingDiagnostics(
            data_source="synthetic",
            exercise_style="american",
            engine="fdm_flat",
            mark_calibrated=bool(kw.pop("mark_calibrated", False)),
        ),
    )


def test_diagnostic_pass_runs_mark_and_quote_tools():
    findings = run_diagnostic_pass(_snap(), _pricing())
    assert "reconcile_mark_vs_model" in findings.tools_run
    assert "quote_quality_and_noise_band" in findings.tools_run
    assert findings.tool_calls_used >= 2


def test_diagnostic_pass_suppresses_vega_inside_noise_band():
    findings = run_diagnostic_pass(
        _snap(iv_now=0.3002),
        _pricing(),
    )
    assert findings.suppress_vega_narrative is True


def test_diagnostic_pass_respects_max_budget():
    snap = _snap(
        discrete_dividends=[DiscreteDividend(ex_date="2026-09-05", amount=0.5)],
    )
    # large residual triggers compare_to_official; ex-div triggers american check
    findings = run_diagnostic_pass(
        snap,
        _pricing(pnl={"total_pnl": 1.0, "residual_pnl": 0.5}),
        surface=None,
    )
    assert findings.tool_calls_used <= MAX_DIAGNOSTIC_TOOL_CALLS


def test_graph_includes_diagnostic_pass_node():
    from explain_my_option.agent_graph import build_graph

    names = set(build_graph().get_graph(xray=True).nodes.keys())
    assert any("diagnostic_pass" in name for name in names)


if __name__ == "__main__":
    test_diagnostic_pass_runs_mark_and_quote_tools()
    test_diagnostic_pass_suppresses_vega_inside_noise_band()
    test_diagnostic_pass_respects_max_budget()
    test_graph_includes_diagnostic_pass_node()
    print("OK — diagnostic_pass tests passed")
