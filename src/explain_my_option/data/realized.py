"""20-day realized vol from close series (HV ≠ IV; used as a Δσ proxy)."""

from __future__ import annotations

from typing import Optional

import numpy as np


def hv20_from_closes(closes) -> tuple[Optional[float], Optional[float]]:
    """Return ``(HV20_t, HV20_{t-1})`` annualized from close-to-close log returns.

    Needs at least 22 closes (21 returns) so both windows exist.
    """
    arr = np.asarray(closes, dtype=float)
    arr = arr[np.isfinite(arr) & (arr > 0)]
    if arr.size < 22:
        return None, None
    rets = np.diff(np.log(arr))
    if rets.size < 21:
        return None, None
    hv_now = float(np.std(rets[-20:], ddof=1) * np.sqrt(252.0))
    hv_prev = float(np.std(rets[-21:-1], ddof=1) * np.sqrt(252.0))
    if not (hv_now == hv_now and hv_prev == hv_prev):
        return None, None
    return hv_now, hv_prev


def iv_prev_from_hv20(
    iv_now: float,
    hv_now: float,
    hv_prev: float,
    *,
    floor: float = 1.0e-4,
) -> tuple[float, float]:
    """σ_prev = σ_now − (HV20_t − HV20_{t-1}), floored."""
    d_proxy = float(hv_now) - float(hv_prev)
    iv_prev = max(float(iv_now) - d_proxy, floor)
    return iv_prev, d_proxy
