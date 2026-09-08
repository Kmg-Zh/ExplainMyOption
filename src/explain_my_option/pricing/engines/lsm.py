"""Longstaff–Schwartz Monte Carlo: BS (QuantLib) and Merton (numpy paths)."""

from __future__ import annotations

from typing import Optional

import numpy as np

from ..config import EngineConfig, MertonParams, default_merton_params
from ..ql_engine import (
    _day_count,
    _parse_iso,
    _payoff,
    _require_ql,
    _to_ql_date,
    build_bsm_process,
    set_evaluation_date,
)
from ..types import Greeks, PricingSpec


def _year_frac(eval_date, expiry: str) -> float:
    ql = _require_ql()
    eval_d = _to_ql_date(eval_date)
    exp = _parse_iso(expiry)
    return max(_day_count().yearFraction(eval_d, exp), 1.0 / 365.0)


def price_lsm_bs(
    spec: PricingSpec,
    *,
    config: Optional[EngineConfig] = None,
) -> tuple[Greeks, list[str]]:
    ql = _require_ql()
    cfg = config or EngineConfig.from_env()
    process, _, *_ = build_bsm_process(
        spec.spot,
        spec.rate,
        spec.dividend_yield,
        spec.vol,
        spec.eval_date,
        spec.discrete_dividends,
    )
    eval_d = _to_ql_date(spec.eval_date)
    exp = _parse_iso(spec.expiry)
    set_evaluation_date(spec.eval_date)
    if spec.exercise_style == "european":
        option = ql.VanillaOption(_payoff(spec.option_type, spec.strike), ql.EuropeanExercise(exp))
        option.setPricingEngine(
            ql.MCEuropeanEngine(
                process,
                "pseudorandom",
                timeSteps=cfg.lsm_steps,
                requiredSamples=cfg.lsm_paths,
                seed=int(cfg.lsm_seed) if cfg.lsm_seed else 42,
            )
        )
    else:
        option = ql.VanillaOption(
            _payoff(spec.option_type, spec.strike),
            ql.AmericanExercise(eval_d, exp),
        )
        option.setPricingEngine(
            ql.MCAmericanEngine(
                process,
                "pseudorandom",
                timeSteps=cfg.lsm_steps,
                requiredSamples=cfg.lsm_paths,
                seed=int(cfg.lsm_seed) if cfg.lsm_seed else 42,
            )
        )
    price = float(option.NPV())
    return Greeks(price=price, delta=0.0, gamma=0.0, vega=0.0, theta=0.0), []


def _laguerre_basis(x: np.ndarray, order: int) -> np.ndarray:
    """Weighted Laguerre polynomials on scaled spot (Longstaff–Schwartz 2001)."""
    x = np.asarray(x, dtype=float)
    cols = [np.exp(-x / 2.0)]
    if order >= 1:
        cols.append(np.exp(-x / 2.0) * (1.0 - x))
    if order >= 2:
        cols.append(np.exp(-x / 2.0) * (1.0 - 2.0 * x + 0.5 * x * x))
    for k in range(3, order + 1):
        cols.append(x**k)
    return np.column_stack(cols)


def simulate_merton_paths(
    spot: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    time_years: float,
    params: MertonParams,
    n_steps: int,
    n_paths: int,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(int(seed))
    dt = time_years / max(n_steps, 1)
    k = float(np.exp(params.jump_mean + 0.5 * params.jump_vol**2) - 1.0)
    drift = (rate - dividend_yield - params.jump_intensity * k - 0.5 * vol**2) * dt
    vol_step = vol * np.sqrt(dt)
    paths = np.empty((n_paths, n_steps + 1), dtype=float)
    paths[:, 0] = spot
    log_s = np.full(n_paths, np.log(spot), dtype=float)
    lam_dt = params.jump_intensity * dt
    for t in range(n_steps):
        z = rng.standard_normal(n_paths)
        n_j = rng.poisson(lam_dt, n_paths)
        jump = np.zeros(n_paths, dtype=float)
        jumped = n_j > 0
        if np.any(jumped):
            # Sum of n_j independent N(μ, δ²) log-jumps per path.
            idx = np.where(jumped)[0]
            for i in idx:
                nj = int(n_j[i])
                jump[i] = rng.normal(params.jump_mean, params.jump_vol, size=nj).sum()
        log_s = log_s + drift + vol_step * z + jump
        paths[:, t + 1] = np.exp(log_s)
    return paths


def lsm_price_from_paths(
    paths: np.ndarray,
    strike: float,
    rate: float,
    time_years: float,
    option_type: str,
    poly_order: int = 2,
    european: bool = False,
) -> float:
    n_paths, n_times = paths.shape
    n_steps = n_times - 1
    dt = time_years / max(n_steps, 1)
    df = float(np.exp(-rate * dt))
    if option_type == "put":
        payoff = np.maximum(strike - paths, 0.0)
    else:
        payoff = np.maximum(paths - strike, 0.0)
    cash = payoff[:, -1].copy()
    if european:
        return float(np.mean(cash) * np.exp(-rate * time_years))
    s0 = float(paths[0, 0])
    for t in range(n_steps - 1, 0, -1):
        intrinsic = payoff[:, t]
        itm = intrinsic > 1e-12
        cash *= df
        if int(itm.sum()) < poly_order + 3:
            continue
        x = paths[itm, t] / s0
        y = cash[itm]
        a = _laguerre_basis(x, poly_order)
        try:
            coeff, *_ = np.linalg.lstsq(a, y, rcond=None)
        except np.linalg.LinAlgError:
            continue
        continuation = a @ coeff
        exercise = intrinsic[itm] > continuation
        take = np.where(itm)[0][exercise]
        cash[take] = intrinsic[take]
    cash *= df
    euro_style = float(np.mean(cash))
    return float(max(euro_style, float(np.mean(payoff[:, 0]))))


def price_lsm_merton(
    spec: PricingSpec,
    *,
    params: Optional[MertonParams] = None,
    config: Optional[EngineConfig] = None,
    european: bool = False,
) -> tuple[Greeks, list[str]]:
    cfg = config or EngineConfig.from_env()
    p = params or default_merton_params()
    t = _year_frac(spec.eval_date, spec.expiry)
    seed = cfg.lsm_seed if cfg.lsm_seed else 42
    paths = simulate_merton_paths(
        spec.spot,
        spec.rate,
        spec.dividend_yield,
        spec.vol,
        t,
        p,
        cfg.lsm_steps,
        cfg.lsm_paths,
        seed,
    )
    price = lsm_price_from_paths(
        paths,
        spec.strike,
        spec.rate,
        t,
        spec.option_type,
        poly_order=cfg.lsm_poly_order,
        european=european or spec.exercise_style == "european",
    )
    return Greeks(price=price, delta=0.0, gamma=0.0, vega=0.0, theta=0.0), []
