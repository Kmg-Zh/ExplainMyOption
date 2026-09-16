"""Basis-consistency invariants: Task A3.5/A3.6, the silent-failure catcher.

Splits and ticker renames fail *silently* -- a mis-based price is still a
plausible-looking number. These checks run on the raw chain before pricing
and abort with a named invariant on a hit; they never apply a correction
factor.

Note on the spec's own illustrative number: a strike chain scaled by
exactly 4x against an unscaled spot, with a realistic ATM-centered spread,
lands right at (not past) the stated bounds -- ``median(strike)/spot`` is
exactly 4.0 (inside ``[0.2, 5.0]``) and ~71% of strikes still satisfy
``|ln(K/F)| <= 1.5`` (above the 60% floor). Verified numerically before
writing this test. The mismatch used below is scaled 8x (two stacked 4-for-1
splits is a real occurrence), which is unambiguously outside both bounds,
to test the mechanism rather than an edge case that the stated thresholds
themselves do not actually catch.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from explain_my_option.data.observation import check_basis_consistency
from explain_my_option.graph.deps import GraphDeps
from explain_my_option.pipeline.book_schema import BookLegSpec
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.leg_graph import build_leg_diagnosis_subgraph
from explain_my_option.data_loader import LoadedData
from explain_my_option.pricing.types import MarketSnapshot


def test_call_mid_above_spot_bound_trips():
    result = check_basis_consistency(
        spot=100.0, rate=0.04, time_to_expiry_years=0.5,
        call_mid=105.0, call_strike=90.0,
    )
    assert result.basis_mismatch_suspected
    assert result.failing_invariant == "call_mid <= spot * 1.01"


def test_put_mid_above_strike_pv_bound_trips():
    result = check_basis_consistency(
        spot=100.0, rate=0.04, time_to_expiry_years=0.5,
        put_mid=100.0, put_strike=90.0,
    )
    assert result.basis_mismatch_suspected
    assert result.failing_invariant == "put_mid <= strike * exp(-r*T) * 1.01"


def test_well_formed_single_contract_passes():
    result = check_basis_consistency(
        spot=100.0, rate=0.04, time_to_expiry_years=0.5,
        call_mid=8.0, call_strike=95.0,
    )
    assert result.ok


def test_4x_mis_based_chain_sits_inside_the_stated_bounds():
    """Documents the boundary case explained in the module docstring."""
    spot = 25.0
    mis_strikes = [k * 4 for k in (17.5, 20, 22.5, 25, 27.5, 30, 32.5)]
    result = check_basis_consistency(
        spot=spot, rate=0.0, time_to_expiry_years=0.5,
        carried_strikes=mis_strikes, forward=spot,
    )
    assert result.ok  # median(strike)/spot == 4.0, inside [0.2, 5.0]


def test_split_basis_mismatched_chain_trips_basis_mismatch_suspected():
    """A3.6: a synthetic chain scaled against an unscaled spot trips the guard."""
    spot = 25.0
    mis_strikes = [k * 8 for k in (17.5, 20, 22.5, 25, 27.5, 30, 32.5)]
    result = check_basis_consistency(
        spot=spot, rate=0.0, time_to_expiry_years=0.5,
        carried_strikes=mis_strikes, forward=spot,
    )
    assert result.basis_mismatch_suspected
    assert result.failing_invariant in (
        "|ln(K / F)| <= 1.5 for at least 60% of carried strikes",
        "0.2 <= median(strike) / spot <= 5.0",
    )


@dataclass
class _MisBasedSingleContractLoader:
    def load(self, *, ticker, option_type, strike, expiry):
        # A mis-based call: the source still carries a pre-split strike of
        # 340 against an already-split spot of 25 -- call_mid ends up far
        # above spot, a plausible-looking number for the *old* basis but
        # not this one.
        snap = MarketSnapshot(
            ticker=ticker, option_type="call", strike=340.0, expiry="2027-01-15",
            spot_now=25.0, spot_prev=25.0, iv_now=0.30, iv_prev=0.28,
            option_price_now=300.0, option_price_prev=295.0,
            time_to_expiry_years=0.5, data_source="yfinance", as_of="2026-08-30",
            mid=300.0,
        )
        return LoadedData(snapshot=snap, surface=None, surface_prev=None)


@dataclass
class _FailIfCalledPnl:
    def attribute(self, snapshot, surface_data=None, surface_prev=None):
        raise AssertionError("pricing must not run past a basis-mismatch abort")


def test_basis_mismatch_produces_no_blotter():
    deps = GraphDeps(market=_MisBasedSingleContractLoader(), pnl=_FailIfCalledPnl())
    app = build_leg_diagnosis_subgraph(
        config=PipelineConfig(features={"a1", "a2", "a3"}, verify_budget=0),
        deps=deps,
    )
    out = app.invoke(
        {"leg": BookLegSpec(leg_id="demo", fixture=None, ticker="GME", strike=340.0)}
    )
    assert out.get("basis_mismatch_suspected") is True
    assert out.get("leg_ok") is False
    assert "blotter" not in out
    assert "Basis Mismatch Suspected" in out["report"]


if __name__ == "__main__":
    test_call_mid_above_spot_bound_trips()
    test_put_mid_above_strike_pv_bound_trips()
    test_well_formed_single_contract_passes()
    test_4x_mis_based_chain_sits_inside_the_stated_bounds()
    test_split_basis_mismatched_chain_trips_basis_mismatch_suspected()
    test_basis_mismatch_produces_no_blotter()
    print("OK — basis guard tests passed")
