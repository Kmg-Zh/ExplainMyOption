"""Vol surface builder: VolSurfaceData → QuantLib BlackVarianceSurface."""

from __future__ import annotations

from datetime import date
from typing import Optional

from .types import SurfaceDiagnostics, VolSurfaceData


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


def _clean_grid(surface: VolSurfaceData) -> tuple[list, list[float], list[list[float]], list[str]]:
    """Drop non-finite / non-positive IVs; return QL dates, strikes, matrix, limitations."""
    limitations: list[str] = []
    if not surface.expiries or not surface.strikes:
        return [], [], [], ["surface_unavailable"]

    ql = _require_ql()
    n_e = len(surface.expiries)
    n_k = len(surface.strikes)
    raw = surface.matrix
    if len(raw) != n_e or any(len(row) != n_k for row in raw):
        return [], [], [], ["surface_unavailable"]

    # Keep strikes/expiries that have at least one valid quote; fill gaps
    # with nearest valid IV along the strike for that expiry when possible.
    cleaned: list[list[float]] = []
    valid_expiry_idx: list[int] = []
    for i, row in enumerate(raw):
        vals = []
        for j, v in enumerate(row):
            try:
                fv = float(v)
            except (TypeError, ValueError):
                fv = float("nan")
            if fv == fv and fv > 0:  # finite and positive
                vals.append(fv)
            else:
                vals.append(float("nan"))
        if sum(1 for x in vals if x == x) >= 2:
            # forward-fill then back-fill NaNs within the expiry row
            last = None
            for j, x in enumerate(vals):
                if x == x:
                    last = x
                elif last is not None:
                    vals[j] = last
            last = None
            for j in range(len(vals) - 1, -1, -1):
                if vals[j] == vals[j]:
                    last = vals[j]
                elif last is not None:
                    vals[j] = last
            if all(x == x and x > 0 for x in vals):
                cleaned.append(vals)
                valid_expiry_idx.append(i)

    if len(cleaned) < 2 or n_k < 2:
        limitations.append("surface_unavailable")
        return [], [], [], limitations

    dates = [_parse_iso(surface.expiries[i]) for i in valid_expiry_idx]
    strikes = [float(k) for k in surface.strikes]
    return dates, strikes, cleaned, limitations


def descriptive_surface_stats(
    surface: VolSurfaceData,
    spot: float,
) -> SurfaceDiagnostics:
    """Skew / term slope proxies from the IV grid (no QuantLib required)."""
    limitations: list[str] = []
    dates, strikes, matrix, lim = _clean_grid(surface)
    limitations.extend(lim)
    if not matrix:
        return SurfaceDiagnostics(limitations=limitations)

    # ATM strike index
    atm_j = min(range(len(strikes)), key=lambda j: abs(strikes[j] - spot))
    atm_term = [row[atm_j] for row in matrix]
    term_slope = None
    if len(atm_term) >= 2:
        term_slope = float(atm_term[-1] - atm_term[0])

    # Skew proxy on nearest expiry: IV(0.95K) - IV(1.05K) approx via strike list
    skew_proxy = None
    row0 = matrix[0]
    put_j = min(range(len(strikes)), key=lambda j: abs(strikes[j] - 0.95 * spot))
    call_j = min(range(len(strikes)), key=lambda j: abs(strikes[j] - 1.05 * spot))
    if put_j != call_j:
        skew_proxy = float(row0[put_j] - row0[call_j])

    return SurfaceDiagnostics(
        term_slope=term_slope,
        skew_proxy=skew_proxy,
        limitations=list(limitations),
    )


def build_black_variance_surface(
    surface: VolSurfaceData,
    eval_date: Optional[date | str] = None,
):
    """Build ``ql.BlackVarianceSurface`` or return ``(None, limitations)``."""
    ql = _require_ql()
    dates, strikes, matrix, limitations = _clean_grid(surface)
    if not matrix:
        return None, limitations

    as_of = eval_date or surface.as_of
    if isinstance(as_of, str):
        ref = _parse_iso(as_of)
    else:
        ref = ql.Date(as_of.day, as_of.month, as_of.year)
    ql.Settings.instance().evaluationDate = ref

    # QuantLib Matrix is (strikes × dates)
    n_k = len(strikes)
    n_d = len(dates)
    m = ql.Matrix(n_k, n_d)
    for j in range(n_d):
        for i in range(n_k):
            m[i][j] = matrix[j][i]

    vol_ts = ql.BlackVarianceSurface(
        ref,
        ql.NullCalendar(),
        dates,
        strikes,
        m,
        ql.Actual365Fixed(),
    )
    vol_ts.enableExtrapolation()
    return vol_ts, limitations


def parallel_shift_surface(
    surface: VolSurfaceData,
    d_vol: float,
    *,
    as_of: Optional[str] = None,
    floor: float = 1.0e-4,
) -> VolSurfaceData:
    """Return a copy of ``surface`` with every finite IV shifted by ``d_vol``.

    Used to synthesize a T-1 grid from today's chain when only an HV20 proxy
    for Δσ is available. Cells are floored so Dupire never sees non-positive IV.
    """
    matrix = []
    for row in surface.matrix:
        shifted = []
        for v in row:
            try:
                fv = float(v)
            except (TypeError, ValueError):
                shifted.append(float("nan"))
                continue
            if fv == fv and fv > 0:
                shifted.append(max(fv + d_vol, floor))
            else:
                shifted.append(fv)
        matrix.append(shifted)
    return VolSurfaceData(
        as_of=as_of or surface.as_of,
        expiries=list(surface.expiries),
        strikes=list(surface.strikes),
        matrix=matrix,
        data_source=surface.data_source,
    )
