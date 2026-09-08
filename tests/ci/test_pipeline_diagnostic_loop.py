"""A2 helper-policy tests."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import bootstrap

bootstrap.install()

from explain_my_option.pricing.types import Greeks, PnLAttribution, PricingDiagnostics, PricingResult
from explain_my_option.pipeline.diagnostic_loop import choose_a2_tool, compute_residual_pct, merge_iteration


def _pricing(total: float, residual: float) -> PricingResult:
    return PricingResult(
        greeks_prev=Greeks(price=4.0, delta=0.5, gamma=0.02, vega=0.1, theta=-0.04),
        greeks_now=Greeks(price=5.0, delta=0.52, gamma=0.02, vega=0.1, theta=-0.04),
        pnl=PnLAttribution(
            total_pnl=total,
            delta_pnl=0.5,
            gamma_pnl=0.1,
            vega_pnl=0.2,
            theta_pnl=-0.1,
            residual_pnl=residual,
            d_spot=1.0,
            d_vol=0.01,
        ),
        diagnostics=PricingDiagnostics(data_source="synthetic", exercise_style="american"),
    )


def test_compute_residual_pct():
    pct = compute_residual_pct(_pricing(total=1.0, residual=0.2))
    assert abs(pct - 20.0) < 1e-9
    assert compute_residual_pct(_pricing(total=0.0, residual=0.2)) == 0.0


def test_choose_a2_tool_policy_and_duplicates():
    assert choose_a2_tool(residual_pct=4.9, tools_run=[]) is None
    assert choose_a2_tool(residual_pct=10.0, tools_run=[]) == "taylor_second_order"
    assert choose_a2_tool(residual_pct=30.0, tools_run=[]) == "path_reprice"
    assert (
        choose_a2_tool(residual_pct=10.0, tools_run=["taylor_second_order"]) is None
    )
    assert choose_a2_tool(residual_pct=30.0, tools_run=["path_reprice"]) is None


def test_merge_iteration_updates_findings():
    out = merge_iteration(
        findings={},
        tool_name="taylor_second_order",
        payload={"combined_pnl": 0.1},
        residual_before=12.5,
        budget_remaining=1,
        iterations=1,
    )
    assert out["tools_run"] == ["taylor_second_order"]
    assert out["results"]["taylor_second_order"]["combined_pnl"] == 0.1
    assert out["diag_budget_remaining"] == 1
    assert out["diag_iterations"] == 1
    assert out["tool_calls_used"] == 1
    assert out["diag_tool_history"][0]["residual_pct"] == 12.5


if __name__ == "__main__":
    test_compute_residual_pct()
    test_choose_a2_tool_policy_and_duplicates()
    test_merge_iteration_updates_findings()
    print("OK — pipeline diagnostic-loop helper tests passed")
