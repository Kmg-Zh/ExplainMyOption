"""Public pricing entrypoint: American FDM PnL + optional surface diagnostics."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Optional

from .calibrate import implied_vol_flat
from .config import EngineConfig
from .engines.fdm import FdmFlatEngine, probe_local_vol, ql_version_string
from .ql_engine import price_european_flat
from .registry import get_engine, resolve_official_engine
from .risk import attribute_pnl
from .surface import build_black_variance_surface
from .types import (
    EngineId,
    MarketSnapshot,
    PricingDiagnostics,
    PricingResult,
    PricingSpec,
    SurfaceDiagnostics,
    VolSurfaceData,
)
from .vol_models import run_surface_diagnostics


def _as_of_date(snapshot: MarketSnapshot) -> date:
    if snapshot.as_of:
        return datetime.strptime(snapshot.as_of, "%Y-%m-%d").date()
    return date.today()


def _calendar_days_elapsed(snapshot: MarketSnapshot) -> float:
    """Calendar days between T-1 and T from snapshot metadata."""
    as_of = _as_of_date(snapshot)
    if snapshot.prev_as_of:
        prev = datetime.strptime(snapshot.prev_as_of, "%Y-%m-%d").date()
    else:
        prev = as_of - timedelta(days=1)
    days = (as_of - prev).days
    return float(max(days, 1))


def _prev_eval_date(as_of: date, snapshot: MarketSnapshot) -> date:
    if snapshot.prev_as_of:
        return datetime.strptime(snapshot.prev_as_of, "%Y-%m-%d").date()
    return as_of - timedelta(days=1)


def _spec(
    snapshot: MarketSnapshot,
    *,
    spot: float,
    vol: float,
    eval_date: date,
    surface: Optional[VolSurfaceData],
) -> PricingSpec:
    return PricingSpec(
        spot=spot,
        strike=snapshot.strike,
        rate=snapshot.risk_free_rate,
        dividend_yield=snapshot.dividend_yield,
        vol=vol,
        expiry=snapshot.expiry,
        eval_date=eval_date,
        option_type=snapshot.option_type,  # type: ignore[arg-type]
        exercise_style=snapshot.exercise_style,
        discrete_dividends=snapshot.discrete_dividends,
        surface=surface,
    )


def _surface_dupire_ok(
    snapshot: MarketSnapshot,
    surface: Optional[VolSurfaceData],
    eval_date: date,
    spot: float,
) -> bool:
    if surface is None:
        return False
    vol_ts, lim = build_black_variance_surface(surface, eval_date=eval_date)
    if vol_ts is None or "surface_unavailable" in lim:
        return False
    from .ql_engine import _day_count, _require_ql, _to_ql_date, set_evaluation_date

    ql = _require_ql()
    set_evaluation_date(eval_date)
    eval_d = _to_ql_date(eval_date)
    dc = _day_count()
    r_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(eval_d, float(snapshot.risk_free_rate), dc)
    )
    q_ts = ql.YieldTermStructureHandle(
        ql.FlatForward(eval_d, float(snapshot.dividend_yield), dc)
    )
    return probe_local_vol(
        vol_ts, r_ts, q_ts, spot, eval_date, snapshot.expiry
    )


def _try_mark_calibration(
    snapshot: MarketSnapshot,
    as_of: date,
    prev_date: date,
    cfg: EngineConfig,
) -> tuple[Optional[float], Optional[float], list[str]]:
    """Invert flat FDM vols to market mids at T and T-1.

    Returns ``(iv_now, iv_prev, limitations)``. Both vols are set only when
    both marks calibrate; otherwise both are None and callers keep vendor IV.
    """
    limitations: list[str] = []
    mark_now = float(snapshot.option_price_now)
    mark_prev = float(snapshot.option_price_prev)
    if mark_now <= 0.0 or mark_prev <= 0.0:
        # Synthetic fixtures leave marks at 0 — silent skip, not a limitation.
        return None, None, limitations

    spec_now = _spec(
        snapshot,
        spot=snapshot.spot_now,
        vol=snapshot.iv_now,
        eval_date=as_of,
        surface=None,
    )
    spec_prev = _spec(
        snapshot,
        spot=snapshot.spot_prev,
        vol=snapshot.iv_prev,
        eval_date=prev_date,
        surface=None,
    )
    iv_now, lim_now = implied_vol_flat(
        spec_now, mark_now, config=cfg, guess=snapshot.iv_now
    )
    iv_prev, lim_prev = implied_vol_flat(
        spec_prev, mark_prev, config=cfg, guess=snapshot.iv_prev
    )
    limitations.extend(lim_now)
    limitations.extend(x for x in lim_prev if x not in limitations)

    if iv_now is None or iv_prev is None:
        if "iv_calibration_failed_solver" not in limitations and (
            iv_now is None or iv_prev is None
        ):
            limitations.append("iv_calibration_failed")
        return None, None, limitations
    return iv_now, iv_prev, limitations


def price_and_attribute(
    snapshot: MarketSnapshot,
    surface_data: Optional[VolSurfaceData] = None,
    surface_prev: Optional[VolSurfaceData] = None,
    *,
    config: Optional[EngineConfig] = None,
) -> PricingResult:
    """Price T-1 and T under official FDM, attribute PnL.

    When both ``option_price_now`` and ``option_price_prev`` are positive market
    marks, invert flat vols so official NPV matches those marks (desk-style
    single-contract recalibration). Local vol then stays diagnostic-only for
    that run. When marks are missing (typical synthetic fixtures), keep the
    prior path: local vol when Dupire-safe, else flat vendor IV.

    ``surface_prev`` is yesterday's grid (cached chain or HV-shifted copy of
    today's surface). Heston remains diagnostic-only.
    """
    cfg = config or EngineConfig.from_env()
    as_of = _as_of_date(snapshot)
    prev_date = _prev_eval_date(as_of, snapshot)
    limitations: list[str] = []
    mark_calibrated = False

    iv_cal_now, iv_cal_prev, cal_lim = _try_mark_calibration(
        snapshot, as_of, prev_date, cfg
    )
    limitations.extend(cal_lim)

    if iv_cal_now is not None and iv_cal_prev is not None:
        # Mark-calibrated official path: flat FDM at inverted vols.
        mark_calibrated = True
        limitations.append("mark_calibrated")
        if surface_data is not None:
            # Surface / local-vol still run as diagnostics below; do not use
            # them for official NPV (would break mark alignment).
            limitations.append("local_vol_deferred_to_mark_calibration")
        official: EngineId = "fdm_flat"
        iv_now = float(iv_cal_now)
        iv_prev = float(iv_cal_prev)
        engine_t = get_engine("fdm_flat", cfg)
        engine_t1 = get_engine("fdm_flat", cfg)
        spec_now = _spec(
            snapshot,
            spot=snapshot.spot_now,
            vol=iv_now,
            eval_date=as_of,
            surface=None,
        )
        spec_prev = _spec(
            snapshot,
            spot=snapshot.spot_prev,
            vol=iv_prev,
            eval_date=prev_date,
            surface=None,
        )
        greeks_now, lim_now = engine_t.price(spec_now)
        greeks_prev, lim_prev = engine_t1.price(spec_prev)
        limitations.extend(x for x in lim_now if x not in limitations)
        limitations.extend(x for x in lim_prev if x not in limitations)
    else:
        # Vendor-IV path (fixtures / calibration failure).
        t_ok = _surface_dupire_ok(snapshot, surface_data, as_of, snapshot.spot_now)
        t1_surface = surface_prev
        t1_ok = _surface_dupire_ok(
            snapshot, t1_surface, prev_date, snapshot.spot_prev
        )
        if surface_data is not None and t_ok and not t1_ok:
            limitations.append("local_vol_t1_shifted_failed")

        official = resolve_official_engine(
            surface=surface_data, local_vol_ok=t_ok, config=cfg
        )
        if surface_data is not None and not t_ok and official != "crr":
            if official == "fdm_local_vol":
                official = "fdm_flat"
            limitations.append("local_vol_failed")

        iv_now = float(snapshot.iv_now)
        iv_prev = float(snapshot.iv_prev)
        engine_t = get_engine(official, cfg)
        spec_now = _spec(
            snapshot,
            spot=snapshot.spot_now,
            vol=iv_now,
            eval_date=as_of,
            surface=surface_data if official == "fdm_local_vol" else None,
        )
        greeks_now, lim_now = engine_t.price(spec_now)
        limitations.extend(lim_now)
        if official == "fdm_local_vol" and "local_vol_failed" in lim_now:
            official = "fdm_flat"
            engine_t = get_engine("fdm_flat", cfg)
            spec_now = _spec(
                snapshot,
                spot=snapshot.spot_now,
                vol=iv_now,
                eval_date=as_of,
                surface=None,
            )
            greeks_now, lim_retry = engine_t.price(spec_now)
            limitations.extend(x for x in lim_retry if x not in limitations)

        engine_t1_id: EngineId = official
        spec_prev_surface = t1_surface if official == "fdm_local_vol" else None
        if official == "fdm_local_vol" and not t1_ok:
            engine_t1_id = "fdm_flat"
            spec_prev_surface = None
        engine_t1 = get_engine(engine_t1_id, cfg)
        spec_prev = _spec(
            snapshot,
            spot=snapshot.spot_prev,
            vol=iv_prev,
            eval_date=prev_date,
            surface=spec_prev_surface,
        )
        greeks_prev, lim_prev = engine_t1.price(spec_prev)
        limitations.extend(x for x in lim_prev if x not in limitations)

    pnl = attribute_pnl(
        greeks_prev=greeks_prev,
        price_prev=greeks_prev.price,
        price_now=greeks_now.price,
        d_spot=snapshot.spot_now - snapshot.spot_prev,
        d_vol=iv_now - iv_prev,
        dt_days=_calendar_days_elapsed(snapshot),
    )

    am_price = eu_price = ee_prem = None
    try:
        eu_g = price_european_flat(
            spot=snapshot.spot_now,
            strike=snapshot.strike,
            rate=snapshot.risk_free_rate,
            dividend_yield=snapshot.dividend_yield,
            vol=iv_now,
            expiry=snapshot.expiry,
            eval_date=as_of,
            option_type=snapshot.option_type,  # type: ignore[arg-type]
            discrete_dividends=(),
        )
        eu_price = eu_g.price
        if snapshot.exercise_style == "american":
            am_price = greeks_now.price
            if official == "fdm_flat":
                am_flat = greeks_now.price
            else:
                g_flat, _ = FdmFlatEngine(cfg).price(
                    _spec(
                        snapshot,
                        spot=snapshot.spot_now,
                        vol=iv_now,
                        eval_date=as_of,
                        surface=None,
                    )
                )
                am_flat = g_flat.price
            ee_prem = max(0.0, am_flat - eu_price)
        else:
            am_price = eu_price
            ee_prem = 0.0
    except Exception:
        limitations.append("early_exercise_premium_unavailable")
        am_price = greeks_now.price

    diagnostics = PricingDiagnostics(
        data_source=snapshot.data_source,
        exercise_style=snapshot.exercise_style,
        engine=official,
        ql_version=ql_version_string(),
        iv_prev_source=snapshot.iv_prev_source,
        local_vol_used=official == "fdm_local_vol",
        mark_calibrated=mark_calibrated,
        effective_iv_now=float(iv_now),
        effective_iv_prev=float(iv_prev),
        european_price=eu_price,
        american_price=am_price,
        early_exercise_premium=ee_prem,
        limitations=list(dict.fromkeys(limitations)),
    )

    surface_diag: Optional[SurfaceDiagnostics] = None
    if surface_data is not None:
        try:
            surface_diag = run_surface_diagnostics(snapshot, surface_data)
        except Exception:
            surface_diag = SurfaceDiagnostics(
                limitations=["surface_unavailable", "heston_calibration_failed"]
            )

    return PricingResult(
        greeks_prev=greeks_prev,
        greeks_now=greeks_now,
        pnl=pnl,
        diagnostics=diagnostics,
        surface_diagnostics=surface_diag,
    )
