"""Shared QuantLib helpers, analytic European, and CRR (env override).

Official 1-day PnL is American FDM in ``engines/fdm.py``, not this module.
"""

from __future__ import annotations

from datetime import date
from typing import Sequence

from .types import DiscreteDividend, Greeks, OptionType

_CRR_STEPS = 500
_VEGA_BUMP = 1.0e-4  # absolute vol bump for finite-difference vega


def _require_ql():
    try:
        import QuantLib as ql
    except ImportError as exc:  # pragma: no cover - install guard
        raise ImportError(
            "QuantLib is required for pricing. Install with: pip install QuantLib"
        ) from exc
    return ql


def _parse_iso(d: str):
    ql = _require_ql()
    y, m, day = (int(x) for x in d.split("-"))
    return ql.Date(day, m, y)


def _to_ql_date(d: date | str):
    ql = _require_ql()
    if isinstance(d, str):
        return _parse_iso(d)
    return ql.Date(d.day, d.month, d.year)


def set_evaluation_date(eval_date: date | str) -> None:
    """Set QuantLib's global evaluation date (must run before building curves)."""
    ql = _require_ql()
    ql.Settings.instance().evaluationDate = _to_ql_date(eval_date)


def _day_count():
    ql = _require_ql()
    return ql.Actual365Fixed()


def _payoff(option_type: OptionType, strike: float):
    ql = _require_ql()
    opt = ql.Option.Call if option_type == "call" else ql.Option.Put
    return ql.PlainVanillaPayoff(opt, float(strike))


def _dividend_schedule(
    discrete: Sequence[DiscreteDividend],
    eval_ql_date,
):
    ql = _require_ql()
    if not discrete:
        return None
    schedule = []
    for div in discrete:
        ex = _parse_iso(div.ex_date)
        if ex > eval_ql_date:
            schedule.append(ql.FixedDividend(float(div.amount), ex))
    if not schedule:
        return None
    return ql.DividendSchedule(schedule)


def build_bsm_process(
    spot: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    eval_date: date | str,
    discrete_dividends: Sequence[DiscreteDividend] = (),
):
    """Build a Black-Scholes-Merton process with flat curves."""
    ql = _require_ql()
    eval_d = _to_ql_date(eval_date)
    set_evaluation_date(eval_date)
    dc = _day_count()
    calendar = ql.NullCalendar()

    spot_h = ql.QuoteHandle(ql.SimpleQuote(float(spot)))
    r_ts = ql.YieldTermStructureHandle(ql.FlatForward(eval_d, float(rate), dc))
    q_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(eval_d, float(dividend_yield), dc)
    )
    vol_ts = ql.BlackVolTermStructureHandle(
        ql.BlackConstantVol(eval_d, calendar, float(vol), dc)
    )
    process = ql.BlackScholesMertonProcess(spot_h, q_ts, r_ts, vol_ts)
    div_sched = _dividend_schedule(discrete_dividends, eval_d)
    return process, div_sched, spot_h, r_ts, q_ts, vol_ts


def _greeks_from_european(option) -> Greeks:
    """AnalyticEuropeanEngine exposes analytic Greeks; scale to project units."""
    vega_per_point = float(option.vega()) * 0.01
    try:
        theta_day = float(option.thetaPerDay())
    except Exception:
        theta_day = float(option.theta()) / 365.0
    return Greeks(
        price=float(option.NPV()),
        delta=float(option.delta()),
        gamma=float(option.gamma()),
        vega=vega_per_point,
        theta=theta_day,
    )


def price_european_flat(
    spot: float,
    strike: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    expiry: str,
    eval_date: date | str,
    option_type: OptionType = "call",
    discrete_dividends: Sequence[DiscreteDividend] = (),
) -> Greeks:
    """European flat-vol price + Greeks via AnalyticEuropeanEngine."""
    ql = _require_ql()
    if spot <= 0 or strike <= 0 or vol <= 0:
        raise ValueError("spot, strike, and vol must be positive.")
    process, _divs, *_ = build_bsm_process(
        spot, rate, dividend_yield, vol, eval_date, discrete_dividends
    )
    exp = _parse_iso(expiry)
    eval_d = _to_ql_date(eval_date)
    if exp <= eval_d:
        raise ValueError("expiry must be after evaluation date.")
    option = ql.VanillaOption(_payoff(option_type, strike), ql.EuropeanExercise(exp))
    option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
    return _greeks_from_european(option)


def _american_vega_bump(
    spot: float,
    strike: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    expiry: str,
    eval_date: date | str,
    option_type: OptionType,
    discrete_dividends: Sequence[DiscreteDividend],
    steps: int,
) -> float:
    """Finite-difference vega per 1 vol point for CRR American (no analytic vega)."""
    ql = _require_ql()
    h = _VEGA_BUMP
    prices = []
    for bumped in (vol + h, max(vol - h, 1e-6)):
        process, _, *_ = build_bsm_process(
            spot, rate, dividend_yield, bumped, eval_date, discrete_dividends
        )
        eval_d = _to_ql_date(eval_date)
        exp = _parse_iso(expiry)
        option = ql.VanillaOption(
            _payoff(option_type, strike), ql.AmericanExercise(eval_d, exp)
        )
        option.setPricingEngine(ql.BinomialVanillaEngine(process, "crr", steps))
        prices.append(float(option.NPV()))
    d_price = prices[0] - prices[1]
    d_vol = (vol + h) - max(vol - h, 1e-6)
    return (d_price / d_vol) * 0.01


def price_american_crr(
    spot: float,
    strike: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    expiry: str,
    eval_date: date | str,
    option_type: OptionType = "call",
    discrete_dividends: Sequence[DiscreteDividend] = (),
    steps: int = _CRR_STEPS,
) -> Greeks:
    """American flat-vol price + Greeks via CRR binomial (vega by bump)."""
    ql = _require_ql()
    if spot <= 0 or strike <= 0 or vol <= 0:
        raise ValueError("spot, strike, and vol must be positive.")
    process, _, *_ = build_bsm_process(
        spot, rate, dividend_yield, vol, eval_date, discrete_dividends
    )
    eval_d = _to_ql_date(eval_date)
    exp = _parse_iso(expiry)
    if exp <= eval_d:
        raise ValueError("expiry must be after evaluation date.")
    option = ql.VanillaOption(
        _payoff(option_type, strike), ql.AmericanExercise(eval_d, exp)
    )
    option.setPricingEngine(ql.BinomialVanillaEngine(process, "crr", steps))
    price = float(option.NPV())
    delta = float(option.delta())
    gamma = float(option.gamma())
    try:
        theta_day = float(option.theta()) / 365.0
    except Exception:
        theta_day = 0.0
    vega = _american_vega_bump(
        spot,
        strike,
        rate,
        dividend_yield,
        vol,
        expiry,
        eval_date,
        option_type,
        discrete_dividends,
        steps,
    )
    return Greeks(
        price=price, delta=delta, gamma=gamma, vega=float(vega), theta=theta_day
    )
