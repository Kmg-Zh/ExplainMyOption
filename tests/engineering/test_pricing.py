"""Pricing engine: arbitrage and numerical invariants, the official PnL path, analysis tools.

Base contract unless stated: S=100, K=100, r=4%, q=0, sigma=25%, T=0.5y.
Every check goes through the shipped engine (``price_fdm`` / ``price_and_attribute``),
never raw QuantLib, so it validates what the product actually runs.
"""

from __future__ import annotations

import dataclasses
import math
from datetime import date, timedelta

import pytest
from scipy.stats import norm
from support import FAST

from explain_my_option.data.historical_chain import load_historical_case
from explain_my_option.data.synthetic import list_fixtures, load_fixture
from explain_my_option.pricing import price_and_attribute
from explain_my_option.pricing.analysis_api import calibrate_merton, compare_to_official, path_reprice, taylor_second_order
from explain_my_option.pricing.config import EngineConfig, default_merton_params
from explain_my_option.pricing.engines.fdm import price_fdm
from explain_my_option.pricing.engines.lsm import price_lsm_merton
from explain_my_option.pricing.engines.merton import price_merton_european
from explain_my_option.pricing.ql_engine import price_european_flat, year_fraction
from explain_my_option.pricing.types import DiscreteDividend, MarketSnapshot, PricingSpec

S0, K0, R0, VOL0, T0 = 100.0, 100.0, 0.04, 0.25, 0.5
EVAL = "2025-01-02"


def _expiry(years: float) -> str:
    return (date.fromisoformat(EVAL) + timedelta(days=round(years * 365))).isoformat()


def _spec(*, strike=K0, T=T0, option_type="call", style="american", divs=(), rate=R0, spot=S0, vol=VOL0, eval_date=EVAL):
    return PricingSpec(
        spot=spot,
        strike=strike,
        rate=rate,
        dividend_yield=0.0,
        vol=vol,
        expiry=_expiry(T),
        eval_date=eval_date,
        option_type=option_type,
        exercise_style=style,
        discrete_dividends=list(divs),
    )


def _fdm(spec: PricingSpec, config: EngineConfig = FAST) -> float:
    return price_fdm(spec, local_vol=False, config=config)[0].price


def _snapshot(*, strike=K0, option_type="call", divs=(), rate=R0) -> MarketSnapshot:
    return MarketSnapshot(
        ticker="SYN",
        option_type=option_type,
        strike=strike,
        expiry=_expiry(T0),
        spot_now=S0,
        spot_prev=S0,
        iv_now=VOL0,
        iv_prev=VOL0,
        option_price_now=0.0,
        option_price_prev=0.0,
        time_to_expiry_years=T0,
        risk_free_rate=rate,
        discrete_dividends=list(divs),
        data_source="synthetic",
        as_of=EVAL,
    )


# --- Arbitrage and numerical invariants -------------------------------------------------


def test_put_call_parity_with_discrete_dividends():
    """European C - P = (S - PV(D)) - K e^{-rT}, with zero, one and two cash dividends."""

    def pv(divs):
        return sum(d.amount * math.exp(-R0 * (date.fromisoformat(d.ex_date) - date.fromisoformat(EVAL)).days / 365) for d in divs)

    call = price_european_flat(spot=S0, strike=K0, rate=R0, dividend_yield=0.0, vol=VOL0, expiry=_expiry(T0), eval_date=EVAL)
    put = price_european_flat(
        spot=S0, strike=K0, rate=R0, dividend_yield=0.0, vol=VOL0, expiry=_expiry(T0), eval_date=EVAL, option_type="put"
    )
    assert abs((call.price - put.price) - (S0 - K0 * math.exp(-R0 * T0))) < 1e-4 * S0

    for divs in (
        [DiscreteDividend(_expiry(0.05), 0.24)],
        [DiscreteDividend(_expiry(0.1), 0.30), DiscreteDividend(_expiry(0.3), 0.30)],
    ):
        c = _fdm(_spec(style="european", divs=divs))
        p = _fdm(_spec(option_type="put", style="european", divs=divs))
        assert abs((c - p) - ((S0 - pv(divs)) - K0 * math.exp(-R0 * T0))) < 1e-3 * S0


@pytest.mark.parametrize("moneyness", [0.8, 1.0, 1.2])
@pytest.mark.parametrize("T", [0.08, 0.5, 2.0])
def test_american_call_without_dividends_equals_european(moneyness, T):
    """Early exercise of a call on a non-dividend asset is never optimal (Merton)."""
    am = _fdm(_spec(strike=S0 * moneyness, T=T))
    eu = _fdm(_spec(strike=S0 * moneyness, T=T, style="european"))
    assert abs(am - eu) / max(eu, 1e-8) < 1e-3


def test_early_exercise_premium_is_non_negative_and_reported_against_same_dividends():
    """American minus European with the same dividend schedule is >= 0, and the
    shipped diagnostic is exactly that difference (signed, never floored)."""
    div = [DiscreteDividend(_expiry(0.1), 2.0)]
    cases = {
        "put": _snapshot(option_type="put"),
        "put_with_div": _snapshot(option_type="put", divs=div),
        "itm_call_with_div": _snapshot(strike=90.0, divs=div),
        "otm_call_with_div": _snapshot(strike=120.0, divs=div),
        "aapl_exdiv_2023": load_fixture("aapl_exdiv_2023")[0],
        "deep_itm_exdiv": load_fixture("deep_itm_exdiv")[0],
    }
    for name, snap in cases.items():
        spec = PricingSpec(
            spot=snap.spot_now,
            strike=snap.strike,
            rate=snap.risk_free_rate,
            dividend_yield=snap.dividend_yield,
            vol=snap.iv_now,
            expiry=snap.expiry,
            eval_date=snap.as_of,
            option_type=snap.option_type,
            discrete_dividends=list(snap.discrete_dividends),
        )
        premium = _fdm(spec) - _fdm(dataclasses.replace(spec, exercise_style="european"))
        assert premium >= -1e-6 * snap.spot_now, name
        shipped = price_and_attribute(snap, None, config=FAST).diagnostics.early_exercise_premium
        assert shipped is not None and abs(shipped - premium) < 1e-6, name

    assert abs(_fdm(_spec(option_type="put", rate=0.0)) - _fdm(_spec(option_type="put", rate=0.0, style="european"))) < 1e-2 * S0
    deep_put = _spec(strike=150.0, option_type="put", rate=0.10)
    assert _fdm(deep_put) - _fdm(dataclasses.replace(deep_put, exercise_style="european")) > 1.0


def test_fdm_converges_as_the_grid_is_refined():
    """Successive differences shrink, the finest step is under 1e-3·S, and the
    observed order of convergence lies in [0.8, 2.5]."""
    prices = [_fdm(_spec(option_type="put"), EngineConfig(t_grid=n, x_grid=n)) for n in (100, 200, 400, 800)]
    d1, d2, d3 = (abs(b - a) for a, b in zip(prices, prices[1:]))
    assert d3 < d2 < d1
    assert d3 < 1e-3 * S0
    assert 0.8 <= math.log2(d2 / d3) <= 2.5


def _bs_greeks(option_type: str, T: float) -> dict[str, float]:
    d1 = (math.log(S0 / K0) + (R0 + 0.5 * VOL0**2) * T) / (VOL0 * math.sqrt(T))
    d2 = d1 - VOL0 * math.sqrt(T)
    call = option_type == "call"
    theta = -S0 * norm.pdf(d1) * VOL0 / (2 * math.sqrt(T)) + (
        -R0 * K0 * math.exp(-R0 * T) * norm.cdf(d2) if call else R0 * K0 * math.exp(-R0 * T) * norm.cdf(-d2)
    )
    return {
        "delta": norm.cdf(d1) if call else norm.cdf(d1) - 1.0,
        "gamma": norm.pdf(d1) / (S0 * VOL0 * math.sqrt(T)),
        "vega": S0 * norm.pdf(d1) * math.sqrt(T) * 0.01,  # per vol point
        "theta": theta / 365.0,  # per calendar day
    }


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_bumped_greeks_match_black_scholes_in_the_european_limit(option_type):
    """Delta and vega within 1e-3 relative error; gamma and theta within 1e-2.
    Vega is per vol point and theta per calendar day, as the blotter prints them."""
    cfg = EngineConfig(t_grid=400, x_grid=400)
    expiry = _expiry(T0)
    T = year_fraction(EVAL, expiry)

    def price(spot=S0, vol=VOL0, eval_date=EVAL) -> float:
        spec = PricingSpec(
            spot=spot, strike=K0, rate=R0, dividend_yield=0.0, vol=vol, expiry=expiry, eval_date=eval_date,
            option_type=option_type, exercise_style="european",
        )
        return _fdm(spec, cfg)

    h_s, h_v = 0.01 * S0, 0.0025
    base = price()
    up, dn = price(spot=S0 + h_s), price(spot=S0 - h_s)
    next_day = (date.fromisoformat(EVAL) + timedelta(days=1)).isoformat()
    fd = {
        "delta": (up - dn) / (2 * h_s),
        "gamma": (up - 2 * base + dn) / h_s**2,
        "vega": (price(vol=VOL0 + h_v) - price(vol=VOL0 - h_v)) / (2 * h_v) * 0.01,
        "theta": price(eval_date=next_day) - base,
    }
    bs = _bs_greeks(option_type, T)
    for greek, tol in (("delta", 1e-3), ("vega", 1e-3), ("gamma", 1e-2), ("theta", 1e-2)):
        assert abs(fd[greek] - bs[greek]) / abs(bs[greek]) < tol, greek


@pytest.mark.parametrize(
    "strike, spot, T, vol, expected",
    [(45.0, 40.0, 0.0833, 0.20, 5.000), (35.0, 40.0, 0.5833, 0.20, 0.433), (35.0, 40.0, 0.3333, 0.20, 0.201), (35.0, 40.0, 0.0833, 0.20, 0.006)],
)
def test_american_put_matches_published_reference_values(strike, spot, T, vol, expected):
    """Ju (1999) short-dated American puts, r=4.88%, as reproduced in QuantLib's
    own test suite (``americanoption.cpp``); absolute tolerance 5e-3."""
    spec = _spec(strike=strike, spot=spot, T=T, vol=vol, rate=0.0488, option_type="put")
    assert abs(_fdm(spec, EngineConfig(t_grid=400, x_grid=400)) - expected) < 5e-3


@pytest.mark.parametrize("name", list_fixtures())
def test_taylor_decomposition_reconstructs_the_model_move(name):
    """delta + gamma + vega + theta + residual == ΔP_model exactly, for every fixture."""
    snap, surf = load_fixture(name)
    pnl = price_and_attribute(snap, surf, config=FAST).pnl
    parts = pnl.delta_pnl + pnl.gamma_pnl + pnl.vega_pnl + pnl.theta_pnl + pnl.residual_pnl
    assert abs(parts - pnl.total_pnl) < 1e-9


def test_unit_conventions():
    """Vol is a decimal, vega is per vol point, theta per calendar day (negative for a long vanilla)."""
    snap, _ = load_fixture("aapl_exdiv_2023")
    assert (snap.iv_prev, snap.iv_now) == (0.28, 0.18)
    greeks = price_fdm(_spec(style="european"), local_vol=False, config=FAST)[0]
    assert greeks.vega > 0 and greeks.theta < 0


# --- Official PnL path -----------------------------------------------------------------


def test_engine_selection_follows_the_surface():
    flat_snap, flat_surf = load_fixture("flat_only")
    flat = price_and_attribute(flat_snap, flat_surf, config=FAST)
    assert flat_surf is None and flat.surface_diagnostics is None
    assert flat.diagnostics.engine == "fdm_flat" and "local_vol_failed" not in flat.diagnostics.limitations

    thin = price_and_attribute(*load_fixture("thin_surface"), config=FAST)
    assert thin.diagnostics.engine == "fdm_flat" and "local_vol_failed" in thin.diagnostics.limitations
    assert {"surface_unavailable", "heston_calibration_failed"} & set(thin.surface_diagnostics.limitations)

    good = price_and_attribute(*load_fixture("calibration_ok"), config=FAST)
    assert good.surface_diagnostics.heston_rmse is not None and good.surface_diagnostics.heston_rmse < 0.05


def test_mark_calibration_aligns_model_to_market_mid():
    """With marks on both dates, flat vols are inverted so model ΔP equals mark ΔP."""
    snap, surf = load_fixture("flat_only")
    baseline = price_and_attribute(snap, surf, config=FAST)
    mark_now, mark_prev = baseline.greeks_now.price, baseline.greeks_prev.price
    poisoned = dataclasses.replace(
        snap,
        iv_now=snap.iv_now + 0.10,
        iv_prev=max(snap.iv_prev * 0.7, 0.05),
        option_price_now=mark_now,
        option_price_prev=mark_prev,
        data_source="yfinance",
    )
    result = price_and_attribute(poisoned, None, config=FAST)
    assert result.diagnostics.mark_calibrated
    assert abs(result.pnl.total_pnl - (mark_now - mark_prev)) < 1e-3

    unmarked = price_and_attribute(*load_fixture("vol_crush"), config=FAST)
    assert not unmarked.diagnostics.mark_calibrated


def test_european_fdm_matches_the_analytic_price():
    snap, _ = load_fixture("flat_only")
    snap.exercise_style = "european"
    fdm = price_and_attribute(snap, None, config=FAST).greeks_now.price
    eu = price_european_flat(
        spot=snap.spot_now, strike=snap.strike, rate=snap.risk_free_rate, dividend_yield=snap.dividend_yield,
        vol=snap.iv_now, expiry=snap.expiry, eval_date=snap.as_of, option_type=snap.option_type,
    )
    assert abs(fdm - eu.price) / eu.price < 0.03


def test_day_count_uses_the_prior_observation_date():
    """Theta covers the calendar days between observations (3 over a weekend)."""
    snap = dataclasses.replace(_snapshot(), as_of="2025-01-06", prev_as_of="2025-01-03")
    result = price_and_attribute(snap, None, config=FAST)
    one_day = price_and_attribute(dataclasses.replace(snap, prev_as_of="2025-01-05"), None, config=FAST)
    assert result.pnl.theta_pnl == pytest.approx(3 * result.greeks_prev.theta, rel=1e-9)
    assert one_day.pnl.theta_pnl == pytest.approx(one_day.greeks_prev.theta, rel=1e-9)


@pytest.mark.parametrize("source", ["aapl_exdiv_2023", "american_put_div", "aapl_exdiv_2023_real", "gme_squeeze_2021_real"])
def test_pricing_is_deterministic(source):
    def run():
        if source.endswith("_real"):
            snap, surf = load_historical_case(source), None
        else:
            snap, surf = load_fixture(source)
        return price_and_attribute(snap, surf, config=FAST).as_dict()

    assert run() == run()


# --- Analysis tools (diagnostics only, never the official PnL) ---------------------------


def test_sequential_revaluation_telescopes_to_the_model_move():
    snap, surf = load_fixture("spot_gap")
    pricing = price_and_attribute(snap, surf, config=FAST)
    result = path_reprice(snap, pricing, config=FAST, surface=surf)
    assert [s.factor for s in result.steps][:3] == ["time", "spot", "vol"]
    assert abs(result.step_sum - pricing.pnl.total_pnl) < 0.05


def test_second_order_residual_after_is_the_taylor_residual_less_vanna_and_volga():
    snap, surf = load_fixture("vol_crush")
    pricing = price_and_attribute(snap, surf, config=FAST)
    second = taylor_second_order(snap, pricing, config=FAST)
    assert second.combined_pnl == pytest.approx(second.vanna_pnl + second.volga_pnl)
    assert second.residual_after == pytest.approx(pricing.pnl.residual_pnl - second.combined_pnl)


def test_cross_checks_against_lsm_and_merton():
    snap, surf = load_fixture("flat_only")
    cross = compare_to_official(snap, surf, config=FAST)
    assert cross.engine_used_for_official == "fdm_flat"
    assert abs(cross.lsm_bs - cross.official_price) / cross.official_price < 0.35

    snap.exercise_style = "european"
    spec = snap.spec(spot=snap.spot_now, vol=snap.iv_now, eval_date=snap.as_of_date())
    params = default_merton_params()
    analytic = price_merton_european(spec, params=params)[0].price
    lsm = price_lsm_merton(spec, params=params, config=FAST, european=True)[0].price
    assert analytic > 0 and abs(lsm - analytic) / analytic < 0.25

    params, limitations = calibrate_merton(snap, None)
    assert "merton_params_defaulted" in limitations and params == default_merton_params()
