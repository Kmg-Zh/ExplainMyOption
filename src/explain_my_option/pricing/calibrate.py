"""Mark-to-model flat IV inversion (product artifact).

Desk practice: before explaining 1-day PnL, recalibrate so the official
engine's NPV matches the observed market mark. We do the single-contract
analogue — solve flat vol σ such that FDM(S, K, σ, …) = market mid —
rather than a full no-arbitrage surface rebuild (out of MVP scope).

Synthetic fixtures often leave ``option_price_*`` at 0; callers should skip
inversion when the target mark is missing or non-positive.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Optional

from scipy.optimize import brentq

from .config import EngineConfig
from .engines.fdm import price_fdm_no_vega
from .types import PricingSpec

_VOL_LO = 1.0e-4
_VOL_HI = 5.0
_PRICE_TOL = 1.0e-4  # absolute $ match after solve
_MAX_BRACKET_EXPAND = 6


def _intrinsic(spec: PricingSpec) -> float:
    if spec.option_type == "call":
        return max(float(spec.spot) - float(spec.strike), 0.0)
    return max(float(spec.strike) - float(spec.spot), 0.0)


def implied_vol_flat(
    spec: PricingSpec,
    target_price: float,
    *,
    config: Optional[EngineConfig] = None,
    guess: Optional[float] = None,
) -> tuple[Optional[float], list[str]]:
    """Solve flat FDM vol so NPV ≈ ``target_price``.

    Returns ``(vol, limitations)``. ``vol`` is None when the mark cannot be
    matched (below intrinsic, no bracket, or solver failure).
    """
    limitations: list[str] = []
    cfg = config or EngineConfig.from_env()
    target = float(target_price)
    if not (target == target) or target <= 0.0:
        return None, limitations

    floor = _intrinsic(spec)
    if target < floor - 1.0e-8:
        limitations.append("iv_calibration_failed_below_intrinsic")
        return None, limitations

    def npv(vol: float) -> float:
        trial = replace(spec, vol=float(vol), surface=None)
        price, _ = price_fdm_no_vega(trial, local_vol=False, config=cfg)
        return float(price) - target

    lo, hi = _VOL_LO, _VOL_HI
    seed = float(guess) if guess is not None and guess > 0 else float(spec.vol or 0.25)
    seed = min(max(seed, lo * 10), hi / 2)

    # Expand bracket around the seed until the objective changes sign.
    f_lo, f_hi = npv(lo), npv(hi)
    if f_lo * f_hi > 0:
        # Try a tighter window around the seed first, then widen.
        span = max(abs(seed) * 0.5, 0.05)
        for _ in range(_MAX_BRACKET_EXPAND):
            lo_try = max(_VOL_LO, seed - span)
            hi_try = min(_VOL_HI, seed + span)
            f_lo, f_hi = npv(lo_try), npv(hi_try)
            if f_lo * f_hi <= 0:
                lo, hi = lo_try, hi_try
                break
            span *= 2.0
        else:
            # Last resort: full domain already evaluated above.
            limitations.append("iv_calibration_failed_no_bracket")
            return None, limitations

    try:
        vol = float(
            brentq(npv, lo, hi, xtol=1.0e-8, rtol=1.0e-8, maxiter=80)
        )
    except Exception:
        limitations.append("iv_calibration_failed_solver")
        return None, limitations

    # Verify absolute price match under the solved vol.
    check = replace(spec, vol=vol, surface=None)
    priced, lim_p = price_fdm_no_vega(check, local_vol=False, config=cfg)
    limitations.extend(x for x in lim_p if x not in limitations)
    if abs(float(priced) - target) > _PRICE_TOL:
        limitations.append("iv_calibration_failed_tol")
        return None, limitations
    return vol, limitations
