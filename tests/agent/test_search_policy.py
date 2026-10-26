"""Search policy: the agent searches only material, reliably observed moves, with a bounded plan.

A quiet move or an unreliable observation gets no search at all; a material one gets
one base query plus cue queries chosen from the blotter, never more than the cap.
"""

from __future__ import annotations

import pytest

from explain_my_option.intel.planner import CueQueryPlanner
from explain_my_option.pricing.types import Greeks, MarketSnapshot, PnLAttribution, PricingDiagnostics, PricingResult


def _priced(*, delta=1.0, gamma=0.0, vega=0.1, theta=0.1, residual=0.1, d_spot=1.0, d_vol=0.0, prices=(5.0, 4.5)):
    snap = MarketSnapshot(
        ticker="AAPL", option_type="call", strike=100.0, expiry="2026-12-18", spot_now=100.0 + d_spot, spot_prev=100.0,
        iv_now=0.30, iv_prev=0.30, option_price_now=prices[0], option_price_prev=prices[1], time_to_expiry_years=0.25,
        data_source="synthetic",
    )
    greeks = Greeks(price=4.5, delta=0.5, gamma=0.02, vega=0.1, theta=-0.04)
    pnl = PnLAttribution(
        total_pnl=delta + gamma + vega + theta + residual, delta_pnl=delta, gamma_pnl=gamma, vega_pnl=vega,
        theta_pnl=theta, residual_pnl=residual, d_spot=d_spot, d_vol=d_vol,
    )
    return snap, PricingResult(greeks, greeks, pnl, PricingDiagnostics(data_source="synthetic", exercise_style="american"))


def _cues(**kwargs) -> list[str]:
    return [q.cue for q in CueQueryPlanner().plan(*_priced(**kwargs)).queries]


def test_planner_searches_only_material_reliable_moves():
    plan = CueQueryPlanner().plan(*_priced())
    assert [(q.source_id, q.cue) for q in plan.queries] == [("yfinance_news", "material")]
    quiet = CueQueryPlanner().plan(*_priced(delta=0.05, vega=0.02, theta=0.04, residual=0.01, prices=(4.52, 4.50)))
    assert quiet.queries == [] and quiet.skip_reason == "below_materiality"
    locked = CueQueryPlanner().plan(*_priced(delta=2.0), observation_reliable=False)
    assert locked.queries == [] and locked.skip_reason == "observation_lock"


@pytest.mark.parametrize(
    "factors, cue",
    [
        ({"vega": 2.0, "delta": 0.1}, "vega"),
        ({"delta": 5.0, "d_vol": -0.20}, "vega"),  # a large IV move even when vega is not the biggest share
        ({"residual": 2.0, "delta": 0.1}, "residual"),  # 8-K
        ({"delta": 5.0, "residual": 2.0, "d_spot": -30.0}, "microstructure"),
    ],
)
def test_planner_adds_bounded_cue_queries(factors, cue):
    cues = _cues(**factors)
    assert cues[0] == "material" and cue in cues and len(cues) <= 3


def test_planner_respects_the_query_cap():
    plan = CueQueryPlanner(max_queries=1).plan(*_priced(delta=0.1, vega=2.0, residual=2.0))
    assert [q.cue for q in plan.queries] == ["material"]
