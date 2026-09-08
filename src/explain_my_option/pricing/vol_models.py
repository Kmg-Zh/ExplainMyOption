"""Heston calibration and pricing helpers (diagnostics only)."""

from __future__ import annotations

import math
from typing import Optional

from .surface import build_black_variance_surface
from .types import MarketSnapshot, SurfaceDiagnostics, VolSurfaceData


def _require_ql():
    try:
        import QuantLib as ql
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "QuantLib is required for pricing. Install with: pip install QuantLib"
        ) from exc
    return ql


def _parse_iso(d: str):
    ql = _require_ql()
    y, m, day = (int(x) for x in d.split("-"))
    return ql.Date(day, m, y)


def _eval_date(snapshot: MarketSnapshot, surface: VolSurfaceData):
    ql = _require_ql()
    raw = snapshot.as_of or surface.as_of
    return _parse_iso(raw) if isinstance(raw, str) else ql.Date.todaysDate()


def calibrate_heston(
    snapshot: MarketSnapshot,
    surface: VolSurfaceData,
) -> tuple[Optional[object], Optional[dict], Optional[float], list[str]]:
    """Calibrate a Heston model to the vol grid. Fail soft on thin/bad data.

    Returns ``(model, params_dict, rmse, limitations)``.
    """
    ql = _require_ql()
    limitations: list[str] = []
    vol_ts, surf_lim = build_black_variance_surface(surface)
    limitations.extend(surf_lim)
    if vol_ts is None:
        limitations.append("heston_calibration_failed")
        return None, None, None, limitations

    today = _eval_date(snapshot, surface)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    calendar = ql.NullCalendar()
    spot = float(snapshot.spot_now)
    r = float(snapshot.risk_free_rate)
    q = float(snapshot.dividend_yield)

    spot_h = ql.QuoteHandle(ql.SimpleQuote(spot))
    r_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, r, dc))
    q_ts = ql.YieldTermStructureHandle(ql.FlatForward(today, q, dc))

    helpers = []
    for exp_s, row in zip(surface.expiries, surface.matrix):
        exp = _parse_iso(exp_s)
        if exp <= today:
            continue
        period = ql.Period(exp - today, ql.Days)
        for strike, iv in zip(surface.strikes, row):
            try:
                sigma = float(iv)
            except (TypeError, ValueError):
                continue
            if not (sigma == sigma and sigma > 0):
                continue
            helper = ql.HestonModelHelper(
                period,
                calendar,
                spot,
                float(strike),
                ql.QuoteHandle(ql.SimpleQuote(sigma)),
                r_ts,
                q_ts,
                ql.BlackCalibrationHelper.PriceError,
            )
            helpers.append(helper)

    if len(helpers) < 5:
        limitations.append("heston_calibration_failed")
        limitations.append("surface_unavailable")
        return None, None, None, limitations

    # Seed from ATM-ish variance
    v0 = max(snapshot.iv_now, 0.05) ** 2
    process = ql.HestonProcess(r_ts, q_ts, spot_h, v0, 1.5, v0, 0.3, -0.5)
    model = ql.HestonModel(process)
    engine = ql.AnalyticHestonEngine(model)
    for h in helpers:
        h.setPricingEngine(engine)

    try:
        model.calibrate(
            helpers,
            ql.LevenbergMarquardt(),
            ql.EndCriteria(400, 40, 1.0e-8, 1.0e-8, 1.0e-8),
        )
    except Exception:
        limitations.append("heston_calibration_failed")
        return None, None, None, limitations

    params = model.params()
    # QuantLib HestonModel parameter order: kappa, theta, sigma, rho, v0
    params_dict = {
        "kappa": float(params[0]),
        "theta": float(params[1]),
        "sigma": float(params[2]),
        "rho": float(params[3]),
        "v0": float(params[4]),
    }
    sse = 0.0
    for h in helpers:
        err = h.calibrationError()
        sse += err * err
    rmse = math.sqrt(sse / len(helpers))
    return model, params_dict, float(rmse), limitations


def _sane_price(price: Optional[float], spot: float) -> Optional[float]:
    """Reject non-finite or absurd FD/Heston NPVs (fail soft)."""
    if price is None:
        return None
    if not (price == price) or price < 0:
        return None
    # Intrinsic upper bound with a generous vol buffer
    if price > max(spot * 2.0, 1.0):
        return None
    return price


def price_american_fd_surface(
    snapshot: MarketSnapshot,
    surface: VolSurfaceData,
) -> Optional[float]:
    """American FD price under BlackVarianceSurface (diagnostic only)."""
    ql = _require_ql()
    vol_ts, lim = build_black_variance_surface(surface)
    if vol_ts is None:
        return None
    today = _parse_iso(snapshot.as_of or surface.as_of)
    ql.Settings.instance().evaluationDate = today
    dc = ql.Actual365Fixed()
    spot_h = ql.QuoteHandle(ql.SimpleQuote(float(snapshot.spot_now)))
    r_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(today, float(snapshot.risk_free_rate), dc)
    )
    q_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(today, float(snapshot.dividend_yield), dc)
    )
    vol_h = ql.BlackVolTermStructureHandle(vol_ts)
    process = ql.BlackScholesMertonProcess(spot_h, q_ts, r_ts, vol_h)
    exp = _parse_iso(snapshot.expiry)
    opt = ql.Option.Call if snapshot.option_type == "call" else ql.Option.Put
    option = ql.VanillaOption(
        ql.PlainVanillaPayoff(opt, float(snapshot.strike)),
        ql.AmericanExercise(today, exp),
    )
    try:
        option.setPricingEngine(ql.FdBlackScholesVanillaEngine(process, 100, 100))
        return _sane_price(float(option.NPV()), float(snapshot.spot_now))
    except Exception:
        return None


def price_american_fd_heston(
    model,
    snapshot: MarketSnapshot,
) -> Optional[float]:
    """American FD price under Heston (diagnostic only)."""
    ql = _require_ql()
    if model is None:
        return None
    raw = snapshot.as_of
    today = _parse_iso(raw) if raw else ql.Date.todaysDate()
    ql.Settings.instance().evaluationDate = today
    exp = _parse_iso(snapshot.expiry)
    opt = ql.Option.Call if snapshot.option_type == "call" else ql.Option.Put
    option = ql.VanillaOption(
        ql.PlainVanillaPayoff(opt, float(snapshot.strike)),
        ql.AmericanExercise(today, exp),
    )
    try:
        option.setPricingEngine(ql.FdHestonVanillaEngine(model, 50, 100, 40))
        return _sane_price(float(option.NPV()), float(snapshot.spot_now))
    except Exception:
        return None


def run_surface_diagnostics(
    snapshot: MarketSnapshot,
    surface: VolSurfaceData,
) -> SurfaceDiagnostics:
    """Skew/term proxies + Heston calibrate + FD American prices; fail soft."""
    from .surface import descriptive_surface_stats

    base = descriptive_surface_stats(surface, snapshot.spot_now)
    limitations = list(base.limitations)

    model, params, rmse, hest_lim = calibrate_heston(snapshot, surface)
    for flag in hest_lim:
        if flag not in limitations:
            limitations.append(flag)

    am_surf = None
    am_hest = None
    if "surface_unavailable" not in limitations:
        am_surf = price_american_fd_surface(snapshot, surface)
        if am_surf is None and "surface_unavailable" not in limitations:
            limitations.append("american_fd_surface_failed")
    if model is not None:
        am_hest = price_american_fd_heston(model, snapshot)
        if am_hest is None:
            limitations.append("american_fd_heston_failed")

    return SurfaceDiagnostics(
        term_slope=base.term_slope,
        skew_proxy=base.skew_proxy,
        heston_params=params,
        heston_rmse=rmse,
        american_surface_price=am_surf,
        american_heston_price=am_hest,
        limitations=limitations,
    )
