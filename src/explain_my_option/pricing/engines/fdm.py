"""American finite-difference engine (official PnL path)."""

from __future__ import annotations

from datetime import date
from typing import Optional, Sequence

from ..config import EngineConfig
from ..ql_engine import (
    _day_count,
    _dividend_schedule,
    _parse_iso,
    _payoff,
    _require_ql,
    _to_ql_date,
    set_evaluation_date,
)
from ..surface import build_black_variance_surface
from ..types import (
    DiscreteDividend,
    EngineId,
    Greeks,
    PricingSpec,
    VolSurfaceData,
)

_VEGA_BUMP = 1.0e-4


def ql_version_string() -> Optional[str]:
    try:
        ql = _require_ql()
        return str(getattr(ql, "__version__", None) or "")
    except Exception:
        return None


def probe_local_vol(
    vol_ts,
    r_ts,
    q_ts,
    spot: float,
    eval_date: date | str,
    expiry: str,
) -> bool:
    """Return True iff Dupire local vol is positive at ATM-neighborhood probes.

    Sparse implied-vol grids can make the Dupire denominator negative and
    trip a QuantLib C++ assert. Probe in Python first.
    """
    ql = _require_ql()
    try:
        spot_h = ql.QuoteHandle(ql.SimpleQuote(float(spot)))
        vol_h = ql.BlackVolTermStructureHandle(vol_ts)
        local = ql.LocalVolSurface(vol_h, r_ts, q_ts, spot_h)
        eval_d = _to_ql_date(eval_date)
        exp = _parse_iso(expiry)
        dc = _day_count()
        t_mid = max(dc.yearFraction(eval_d, exp) * 0.5, 1.0 / 365.0)
        t_near = max(dc.yearFraction(eval_d, exp) * 0.25, 1.0 / 365.0)
        times = (t_near, t_mid)
        moneyness = (0.90, 0.95, 1.00, 1.05, 1.10)
        for t in times:
            for m in moneyness:
                lv = float(local.localVol(float(t), float(spot) * m, True))
                if not (lv == lv) or lv <= 0.0:
                    return False
        return True
    except Exception:
        return False


def _greeks_from_fd(option, theta_fallback: float = 0.0) -> tuple[float, float, float, float]:
    price = float(option.NPV())
    try:
        delta = float(option.delta())
    except Exception:
        delta = 0.0
    try:
        gamma = float(option.gamma())
    except Exception:
        gamma = 0.0
    try:
        theta_day = float(option.theta()) / 365.0
    except Exception:
        theta_day = theta_fallback
    return price, delta, gamma, theta_day


def _make_option(ql, spec: PricingSpec, eval_d, exp):
    payoff = _payoff(spec.option_type, spec.strike)
    if spec.exercise_style == "european":
        exercise = ql.EuropeanExercise(exp)
    else:
        exercise = ql.AmericanExercise(eval_d, exp)
    return ql.VanillaOption(payoff, exercise)


def _attach_engine(
    ql,
    option,
    process,
    cfg: EngineConfig,
    local_vol: bool,
    overwrite: float,
    dividends=None,
):
    kwargs = dict(
        tGrid=int(cfg.t_grid),
        xGrid=int(cfg.x_grid),
        dampingSteps=int(cfg.damping_steps),
    )
    used_divs = False
    try:
        if dividends is not None:
            engine = ql.FdBlackScholesVanillaEngine(
                process,
                dividends,
                int(cfg.t_grid),
                int(cfg.x_grid),
                int(cfg.damping_steps),
                ql.FdmSchemeDesc.Douglas(),
                bool(local_vol),
                float(overwrite),
            )
            used_divs = True
        else:
            engine = ql.FdBlackScholesVanillaEngine(
                process,
                localVol=bool(local_vol),
                illegalLocalVolOverwrite=float(overwrite),
                **kwargs,
            )
    except TypeError:
        engine = ql.FdBlackScholesVanillaEngine(process, cfg.t_grid, cfg.x_grid)
        used_divs = False
    option.setPricingEngine(engine)
    npv = float(option.NPV())
    if not (npv == npv) or npv < 0:
        raise RuntimeError("FdBlackScholesVanillaEngine returned invalid NPV")
    return option, used_divs


def price_fdm(
    spec: PricingSpec,
    *,
    local_vol: bool,
    config: Optional[EngineConfig] = None,
) -> tuple[Greeks, list[str]]:
    """Price with FdBlackScholesVanillaEngine. ``local_vol`` requires a surface."""
    ql = _require_ql()
    cfg = config or EngineConfig.from_env()
    limitations: list[str] = []
    eval_d = _to_ql_date(spec.eval_date)
    set_evaluation_date(spec.eval_date)
    exp = _parse_iso(spec.expiry)
    if exp <= eval_d:
        raise ValueError("expiry must be after evaluation date.")
    if spec.spot <= 0 or spec.strike <= 0 or spec.vol <= 0:
        raise ValueError("spot, strike, and vol must be positive.")

    dc = _day_count()
    calendar = ql.NullCalendar()
    spot_h = ql.QuoteHandle(ql.SimpleQuote(float(spec.spot)))
    r_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(eval_d, float(spec.rate), dc)
    )
    div_sched = _dividend_schedule(spec.discrete_dividends, eval_d)
    q_used = 0.0 if div_sched is not None else float(spec.dividend_yield)
    q_ts = ql.YieldTermStructureHandle(ql.FlatForward(eval_d, q_used, dc))

    use_local = False
    vol_ts = None
    if local_vol and spec.surface is not None:
        vol_ts, surf_lim = build_black_variance_surface(
            spec.surface, eval_date=spec.eval_date
        )
        limitations.extend(surf_lim)
        if vol_ts is not None and probe_local_vol(
            vol_ts, r_ts, q_ts, spec.spot, spec.eval_date, spec.expiry
        ):
            use_local = True
        else:
            limitations.append("local_vol_failed")
            vol_ts = None

    if vol_ts is None:
        vol_ts = ql.BlackConstantVol(eval_d, calendar, float(spec.vol), dc)
        use_local = False

    vol_h = ql.BlackVolTermStructureHandle(vol_ts)
    process = ql.BlackScholesMertonProcess(spot_h, q_ts, r_ts, vol_h)
    option = _make_option(ql, spec, eval_d, exp)
    try:
        option, used_divs = _attach_engine(
            ql, option, process, cfg, use_local, spec.vol, dividends=div_sched
        )
        if div_sched is not None and not used_divs:
            limitations.append("discrete_dividends_ignored")
    except Exception:
        if div_sched is not None:
            limitations.append("discrete_dividends_ignored")
            q_ts = ql.YieldTermStructureHandle(
                ql.FlatForward(eval_d, float(spec.dividend_yield), dc)
            )
            process = ql.BlackScholesMertonProcess(spot_h, q_ts, r_ts, vol_h)
            option = _make_option(ql, spec, eval_d, exp)
            option, _ = _attach_engine(
                ql, option, process, cfg, use_local, spec.vol, dividends=None
            )
        else:
            raise

    price, delta, gamma, theta_day = _greeks_from_fd(option)
    vega = _vega_bump(spec, local_vol=use_local, config=cfg)
    return (
        Greeks(price=price, delta=delta, gamma=gamma, vega=vega, theta=theta_day),
        limitations,
    )


def _vega_bump(
    spec: PricingSpec,
    *,
    local_vol: bool,
    config: EngineConfig,
) -> float:
    """Per-vol-point vega via parallel implied-vol bump."""
    h = _VEGA_BUMP
    up = _shift_spec(spec, h)
    down = _shift_spec(spec, -h)
    try:
        g_up, _ = price_fdm_no_vega(up, local_vol=local_vol, config=config)
        g_dn, _ = price_fdm_no_vega(down, local_vol=local_vol, config=config)
    except Exception:
        return 0.0
    d_vol = (spec.vol + h) - max(spec.vol - h, 1e-6)
    if d_vol <= 0:
        return 0.0
    return ((g_up - g_dn) / d_vol) * 0.01


def price_fdm_no_vega(
    spec: PricingSpec,
    *,
    local_vol: bool,
    config: EngineConfig,
) -> tuple[float, list[str]]:
    """NPV only — used by the vega bump to avoid recursion."""
    # Reuse price_fdm but would recurse on vega. Inline a slim NPV path.
    greeks, lim = _price_fdm_core(spec, local_vol=local_vol, config=config)
    return greeks.price, lim


def _shift_spec(spec: PricingSpec, d_vol: float) -> PricingSpec:
    from ..surface import parallel_shift_surface

    vol = max(spec.vol + d_vol, 1e-6)
    surface = spec.surface
    if surface is not None:
        surface = parallel_shift_surface(surface, d_vol)
    return PricingSpec(
        spot=spec.spot,
        strike=spec.strike,
        rate=spec.rate,
        dividend_yield=spec.dividend_yield,
        vol=vol,
        expiry=spec.expiry,
        eval_date=spec.eval_date,
        option_type=spec.option_type,
        exercise_style=spec.exercise_style,
        discrete_dividends=spec.discrete_dividends,
        surface=surface,
    )


def _price_fdm_core(
    spec: PricingSpec,
    *,
    local_vol: bool,
    config: EngineConfig,
) -> tuple[Greeks, list[str]]:
    """Same as price_fdm but vega left at 0 (bump helper)."""
    ql = _require_ql()
    cfg = config
    limitations: list[str] = []
    eval_d = _to_ql_date(spec.eval_date)
    set_evaluation_date(spec.eval_date)
    exp = _parse_iso(spec.expiry)
    dc = _day_count()
    calendar = ql.NullCalendar()
    spot_h = ql.QuoteHandle(ql.SimpleQuote(float(spec.spot)))
    r_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(eval_d, float(spec.rate), dc)
    )
    div_sched = _dividend_schedule(spec.discrete_dividends, eval_d)
    q_used = 0.0 if div_sched is not None else float(spec.dividend_yield)
    q_ts = ql.YieldTermStructureHandle(ql.FlatForward(eval_d, q_used, dc))
    use_local = False
    vol_ts = None
    if local_vol and spec.surface is not None:
        vol_ts, _ = build_black_variance_surface(spec.surface, eval_date=spec.eval_date)
        if vol_ts is not None and probe_local_vol(
            vol_ts, r_ts, q_ts, spec.spot, spec.eval_date, spec.expiry
        ):
            use_local = True
        else:
            vol_ts = None
    if vol_ts is None:
        vol_ts = ql.BlackConstantVol(eval_d, calendar, float(spec.vol), dc)
        use_local = False
    process = ql.BlackScholesMertonProcess(
        spot_h, q_ts, r_ts, ql.BlackVolTermStructureHandle(vol_ts)
    )
    option = _make_option(ql, spec, eval_d, exp)
    try:
        option, _used = _attach_engine(
            ql, option, process, cfg, use_local, spec.vol, dividends=div_sched
        )
    except Exception:
        q_ts = ql.YieldTermStructureHandle(
            ql.FlatForward(eval_d, float(spec.dividend_yield), dc)
        )
        process = ql.BlackScholesMertonProcess(
            spot_h, q_ts, r_ts, ql.BlackVolTermStructureHandle(vol_ts)
        )
        option = _make_option(ql, spec, eval_d, exp)
        option, _ = _attach_engine(
            ql, option, process, cfg, use_local, spec.vol, dividends=None
        )
    price, delta, gamma, theta_day = _greeks_from_fd(option)
    return Greeks(price=price, delta=delta, gamma=gamma, vega=0.0, theta=theta_day), limitations


class FdmFlatEngine:
    name: EngineId = "fdm_flat"

    def __init__(self, config: Optional[EngineConfig] = None) -> None:
        self.config = config or EngineConfig.from_env()

    def price(self, spec: PricingSpec) -> tuple[Greeks, list[str]]:
        return price_fdm(spec, local_vol=False, config=self.config)


class FdmLocalVolEngine:
    name: EngineId = "fdm_local_vol"

    def __init__(self, config: Optional[EngineConfig] = None) -> None:
        self.config = config or EngineConfig.from_env()

    def price(self, spec: PricingSpec) -> tuple[Greeks, list[str]]:
        greeks, lim = price_fdm(spec, local_vol=True, config=self.config)
        if "local_vol_failed" in lim and spec.surface is not None:
            # Caller should treat this as a fallback to flat.
            pass
        return greeks, lim
