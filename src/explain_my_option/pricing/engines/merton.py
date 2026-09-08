"""European Merton (1976) jump-diffusion — analytic series / QuantLib."""

from __future__ import annotations

import math
from typing import Optional

from ..config import MertonParams, default_merton_params
from ..types import Greeks, PricingSpec


def merton_european_series(
    spot: float,
    strike: float,
    time_years: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    option_type: str,
    params: MertonParams,
    n_terms: int = 40,
) -> float:
    """Merton 1976 Poisson-weighted Black–Scholes mixture (European only)."""
    if time_years <= 0:
        if option_type == "put":
            return max(strike - spot, 0.0)
        return max(spot - strike, 0.0)
    k = math.exp(params.jump_mean + 0.5 * params.jump_vol**2) - 1.0
    lam = params.jump_intensity
    lam_p = lam * (1.0 + k)
    total = 0.0
    # Use scipy/analytic N(d1) via QuantLib BS for each term — but that needs dates.
    # Closed BS via math to stay date-free.
    from math import erf, log, sqrt

    def ncdf(x: float) -> float:
        return 0.5 * (1.0 + erf(x / sqrt(2.0)))

    def bs(r: float, sig: float) -> float:
        if sig <= 0 or time_years <= 0:
            fwd = spot * math.exp((r - dividend_yield) * time_years)
            disc = math.exp(-r * time_years)
            if option_type == "put":
                return disc * max(strike - fwd, 0.0)
            return disc * max(fwd - strike, 0.0)
        d1 = (
            log(spot / strike)
            + (r - dividend_yield + 0.5 * sig * sig) * time_years
        ) / (sig * sqrt(time_years))
        d2 = d1 - sig * sqrt(time_years)
        df_r = math.exp(-r * time_years)
        df_q = math.exp(-dividend_yield * time_years)
        call = spot * df_q * ncdf(d1) - strike * df_r * ncdf(d2)
        if option_type == "put":
            return call - spot * df_q + strike * df_r
        return call

    weight = math.exp(-lam_p * time_years)
    for n in range(n_terms):
        if n > 0:
            weight *= (lam_p * time_years) / n
        sig_n = math.sqrt(vol * vol + n * params.jump_vol**2 / time_years)
        r_n = rate - lam * k + (n * math.log(1.0 + k) / time_years if (1.0 + k) > 0 else 0.0)
        total += weight * bs(r_n, sig_n)
        if n > 8 and weight < 1e-14:
            break
    return float(total)


def price_merton_european(
    spec: PricingSpec,
    *,
    params: Optional[MertonParams] = None,
) -> tuple[Greeks, list[str]]:
    from ..ql_engine import _day_count, _parse_iso, _to_ql_date, set_evaluation_date

    p = params or default_merton_params()
    set_evaluation_date(spec.eval_date)
    t = max(_day_count().yearFraction(_to_ql_date(spec.eval_date), _parse_iso(spec.expiry)), 1.0 / 365.0)
    limitations: list[str] = []
    price = merton_european_series(
        spec.spot,
        spec.strike,
        t,
        spec.rate,
        spec.dividend_yield,
        spec.vol,
        spec.option_type,
        p,
    )
    # Delta via bump (analysis API does not need full Greeks).
    bump = max(spec.spot * 1e-4, 1e-4)
    up = merton_european_series(
        spec.spot + bump, spec.strike, t, spec.rate, spec.dividend_yield, spec.vol, spec.option_type, p
    )
    dn = merton_european_series(
        spec.spot - bump, spec.strike, t, spec.rate, spec.dividend_yield, spec.vol, spec.option_type, p
    )
    delta = (up - dn) / (2.0 * bump)
    return Greeks(price=price, delta=delta, gamma=0.0, vega=0.0, theta=0.0), limitations
