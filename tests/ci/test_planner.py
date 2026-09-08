"""Query planner: materiality gate and blotter cues (no network)."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from explain_my_option.intel.planner import CueQueryPlanner
from explain_my_option.intel.types import SearchPlan
from explain_my_option.pricing.types import (
    Greeks,
    MarketSnapshot,
    PnLAttribution,
    PricingDiagnostics,
    PricingResult,
)


def _dummy_snap(ticker: str = "AAPL") -> MarketSnapshot:
    return MarketSnapshot(
        ticker=ticker,
        option_type="call",
        strike=100.0,
        expiry="2026-12-18",
        spot_now=100.0,
        spot_prev=99.0,
        iv_now=0.30,
        iv_prev=0.30,
        option_price_now=5.0,
        option_price_prev=4.5,
        time_to_expiry_years=0.25,
        data_source="synthetic",
    )


def _dummy_pricing(
    *,
    delta: float = 1.0,
    vega: float = 0.1,
    theta: float = 0.1,
    residual: float = 0.1,
) -> PricingResult:
    total = delta + vega + theta + residual
    return PricingResult(
        greeks_prev=Greeks(price=4.5, delta=0.5, gamma=0.02, vega=0.1, theta=-0.04),
        greeks_now=Greeks(price=5.0, delta=0.5, gamma=0.02, vega=0.1, theta=-0.04),
        pnl=PnLAttribution(
            total_pnl=total,
            delta_pnl=delta,
            gamma_pnl=0.0,
            vega_pnl=vega,
            theta_pnl=theta,
            residual_pnl=residual,
            d_spot=1.0,
            d_vol=0.0,
        ),
        diagnostics=PricingDiagnostics(
            data_source="synthetic",
            exercise_style="american",
        ),
    )


def _cues(plan: SearchPlan) -> set[str]:
    return {q.cue for q in plan.queries}


def test_planner_material_headlines():
    plan = CueQueryPlanner().plan(_dummy_snap(), _dummy_pricing())
    assert plan.queries[0].source_id == "yfinance_news"
    assert plan.queries[0].cue == "material"
    assert plan.skip_reason == ""
    assert "vega" not in _cues(plan)
    assert "residual" not in _cues(plan)


def test_planner_skips_immaterial_move():
    snap = _dummy_snap()
    snap.option_price_now = 4.52
    snap.option_price_prev = 4.50
    plan = CueQueryPlanner().plan(
        snap,
        _dummy_pricing(delta=0.05, vega=0.02, theta=0.04, residual=0.01),
    )
    assert plan.queries == []
    assert plan.skip_reason == "below_materiality"
    notes = " ".join(plan.honesty_notes())
    assert "No catalyst search" in notes


def test_planner_skips_when_observation_unreliable():
    plan = CueQueryPlanner().plan(
        _dummy_snap(),
        _dummy_pricing(delta=2.0, vega=0.1, theta=0.1, residual=0.1),
        observation_reliable=False,
    )
    assert plan.queries == []
    assert plan.skip_reason == "observation_lock"


def test_planner_vega_cue():
    plan = CueQueryPlanner().plan(
        _dummy_snap(),
        _dummy_pricing(delta=0.1, vega=2.0, theta=0.1, residual=0.1),
    )
    assert "vega" in _cues(plan)
    assert any(q.source_id == "tavily" for q in plan.queries)
    assert any("implied volatility" in q.q for q in plan.queries)
    assert not any(q.cue == "vega" and q.source_id == "yfinance_news" for q in plan.queries)


def test_planner_residual_cue_8k_source():
    plan = CueQueryPlanner().plan(
        _dummy_snap(),
        _dummy_pricing(delta=0.1, vega=0.1, theta=0.1, residual=2.0),
    )
    assert "residual" in _cues(plan)
    assert any(q.source_id == "sec_8k" for q in plan.queries)


def test_planner_respects_max_queries():
    plan = CueQueryPlanner(max_queries=1).plan(
        _dummy_snap(),
        _dummy_pricing(delta=0.1, vega=2.0, theta=0.1, residual=2.0),
    )
    assert len(plan.queries) == 1
    assert plan.queries[0].cue == "material"


def test_planner_vol_move_fires_vega_without_vega_share():
    pricing = _dummy_pricing(delta=5.0, vega=0.1, theta=0.1, residual=0.1)
    pricing.pnl.d_vol = -0.20
    plan = CueQueryPlanner().plan(_dummy_snap(), pricing)
    assert "vega" in _cues(plan)
    assert any("IV crush" in q.q or "implied volatility" in q.q for q in plan.queries)


def test_planner_extreme_spot_residual_fires_microstructure():
    snap = _dummy_snap()
    snap.spot_prev = 100.0
    snap.spot_now = 70.0
    pricing = _dummy_pricing(delta=5.0, vega=0.1, theta=0.1, residual=2.0)
    pricing.pnl.d_spot = -30.0
    plan = CueQueryPlanner().plan(snap, pricing)
    assert "microstructure" in _cues(plan)
    assert any(q.source_id == "tavily" and q.cue == "microstructure" for q in plan.queries)
    assert len(plan.queries) <= 3


def test_planner_includes_gamma_in_factor_magnitudes():
    snap = _dummy_snap()
    pricing = _dummy_pricing(delta=0.1, vega=0.1, theta=0.1, residual=0.1)
    pricing.pnl.gamma_pnl = 5.0
    plan = CueQueryPlanner().plan(snap, pricing)
    assert plan.queries[0].cue == "material"


if __name__ == "__main__":
    test_planner_material_headlines()
    test_planner_skips_immaterial_move()
    test_planner_skips_when_observation_unreliable()
    test_planner_vega_cue()
    test_planner_residual_cue_8k_source()
    test_planner_respects_max_queries()
    test_planner_vol_move_fires_vega_without_vega_share()
    test_planner_extreme_spot_residual_fires_microstructure()
    test_planner_includes_gamma_in_factor_magnitudes()
    print("OK — planner checks passed")
