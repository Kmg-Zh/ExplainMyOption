"""In-repo 1-day PnL attribution (flat-vol Greeks)."""

from __future__ import annotations

from .types import Greeks, PnLAttribution


def attribute_pnl(
    greeks_prev: Greeks,
    price_prev: float,
    price_now: float,
    d_spot: float,
    d_vol: float,
    dt_days: float = 1.0,
) -> PnLAttribution:
    """Attribute a 1-day option price change to Delta, Vega and Theta.

    Uses yesterday's Greeks as the sensitivities:
        dP ~= Delta * dS + Vega * (dVol / 0.01) + Theta * dt

    Args:
        greeks_prev: Greeks at the previous day's market state.
        price_prev: Model option price yesterday.
        price_now: Model option price today.
        d_spot: S_now - S_prev.
        d_vol: IV change as a decimal (0.02 = +2 vol points).
        dt_days: Elapsed calendar days (default 1).
    """
    total_pnl = price_now - price_prev
    delta_pnl = greeks_prev.delta * d_spot
    gamma_pnl = 0.5 * greeks_prev.gamma * d_spot * d_spot
    vega_pnl = greeks_prev.vega * (d_vol / 0.01)
    theta_pnl = greeks_prev.theta * dt_days
    residual_pnl = total_pnl - (delta_pnl + gamma_pnl + vega_pnl + theta_pnl)

    return PnLAttribution(
        total_pnl=float(total_pnl),
        delta_pnl=float(delta_pnl),
        gamma_pnl=float(gamma_pnl),
        vega_pnl=float(vega_pnl),
        theta_pnl=float(theta_pnl),
        residual_pnl=float(residual_pnl),
        d_spot=float(d_spot),
        d_vol=float(d_vol),
    )
