"""Input guards that run before pricing.

1. Continuity: a one-day attribution needs the same contract observed on both
   T-1 and T. A missing day or contract is a data coverage gap, never an
   unexplained market move.
2. Basis consistency: splits and ticker renames fail silently, because a
   mis-based price still looks plausible. No-arbitrage sanity bounds on the
   raw quotes catch them before the engine sees them.
3. Mark consistency: a mark and a spot taken at different times look like a
   real move, and mark calibration turns the gap into vega. No-arbitrage
   bounds on both marks run before pricing; a calibrated-vs-vendor IV
   cross-check runs right after it. A failure is a data break: nothing is
   narrated.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Mapping, Optional, Sequence

from ..pricing.types import MarketSnapshot, intrinsic_value

# Yahoo prints impliedVolatility=1e-05 (and similar) as a stale-quote sentinel,
# mostly outside market hours. No listed equity option trades at a 1% implied
# vol, so anything below this is "no usable IV", not a real reading -- at
# load time (data_loader._clean_iv), when reading a cached t-1 back
# (data.cache), and as the reference for the calibrated-IV check below.
MIN_PLAUSIBLE_IV = 0.01


class ObservationStatus(str, Enum):
    OK = "OK"
    DAY_MISSING = "DAY_MISSING"  # source has no rows for any symbol that date
    CONTRACT_MISSING = "CONTRACT_MISSING"  # day exists, but not this contract


def classify_observation_status(
    *, reference_row_counts: Mapping[str, int], contract_rows: int
) -> ObservationStatus:
    """Classify one date's observability for one contract.

    ``reference_row_counts`` is a basket of reference symbols (e.g. SPY,
    AAPL, plus the case symbol) mapped to the source's row count for that
    date. Zero rows across the whole basket means the source has no data
    for the date at all -- not just for this contract.
    """
    if sum(int(n) for n in reference_row_counts.values()) == 0:
        return ObservationStatus.DAY_MISSING
    if int(contract_rows) == 0:
        return ObservationStatus.CONTRACT_MISSING
    return ObservationStatus.OK


NO_COMPARABLE_OBSERVATION_TEMPLATE = (
    "No comparable observation. {contract} was {status_t1} on {date_t1} and "
    "{status_t} on {date_t}. A one-day attribution requires the same "
    "contract observed on both dates, so this run produces no attribution. "
    "This is a data coverage limitation, not an unexplained market move."
)


class NoComparableObservationError(Exception):
    """Continuity gate failure: no comparison was possible at all.

    Distinct from an unexplained break (the market did something the model
    did not capture). Carries both per-date statuses.
    """

    def __init__(
        self,
        *,
        contract: str,
        status_t1: ObservationStatus,
        status_t: ObservationStatus,
        date_t1: str,
        date_t: str,
    ) -> None:
        self.contract = contract
        self.status_t1 = status_t1
        self.status_t = status_t
        self.date_t1 = date_t1
        self.date_t = date_t
        super().__init__(self.report_text())

    def report_text(self) -> str:
        return NO_COMPARABLE_OBSERVATION_TEMPLATE.format(
            contract=self.contract,
            status_t1=self.status_t1.value,
            status_t=self.status_t.value,
            date_t1=self.date_t1,
            date_t=self.date_t,
        )


def continuity_gate(
    *,
    contract: str,
    status_t1: ObservationStatus,
    status_t: ObservationStatus,
    date_t1: str,
    date_t: str,
) -> None:
    """Raise ``NoComparableObservationError`` unless both dates are OK."""
    if status_t1 is ObservationStatus.OK and status_t is ObservationStatus.OK:
        return
    raise NoComparableObservationError(
        contract=contract,
        status_t1=status_t1,
        status_t=status_t,
        date_t1=date_t1,
        date_t=date_t,
    )


@dataclass
class BasisCheckResult:
    basis_mismatch_suspected: bool
    failing_invariant: Optional[str] = None
    detail: Optional[str] = None

    @property
    def ok(self) -> bool:
        return not self.basis_mismatch_suspected


def check_basis_consistency(
    *,
    spot: float,
    rate: float,
    time_to_expiry_years: float,
    call_mid: Optional[float] = None,
    call_strike: Optional[float] = None,
    put_mid: Optional[float] = None,
    put_strike: Optional[float] = None,
    carried_strikes: Sequence[float] = (),
    forward: Optional[float] = None,
) -> BasisCheckResult:
    """Catch a mis-based chain before pricing.

    Single-contract callers supply ``call_mid``/``put_mid`` with the matching
    strike; the two multi-strike checks need a full chain (``carried_strikes``
    and a ``forward``). A check whose inputs are missing is skipped, never
    guessed. On a hit, report the failing invariant; never apply a correction.
    """
    if call_mid is not None and call_strike is not None:
        limit = spot * 1.01
        if call_mid > limit:
            return BasisCheckResult(
                True,
                "call_mid <= spot * 1.01",
                f"call_mid={call_mid!r} > spot*1.01={limit!r} (spot={spot!r})",
            )

    if put_mid is not None and put_strike is not None:
        limit = put_strike * math.exp(-rate * time_to_expiry_years) * 1.01
        if put_mid > limit:
            return BasisCheckResult(
                True,
                "put_mid <= strike * exp(-r*T) * 1.01",
                f"put_mid={put_mid!r} > strike*exp(-r*T)*1.01={limit!r} "
                f"(strike={put_strike!r})",
            )

    strikes = [float(k) for k in carried_strikes if k and k > 0]

    if strikes and forward is not None and forward > 0:
        within = sum(1 for k in strikes if abs(math.log(k / forward)) <= 1.5)
        frac = within / len(strikes)
        if frac < 0.6:
            return BasisCheckResult(
                True,
                "|ln(K / F)| <= 1.5 for at least 60% of carried strikes",
                f"only {frac:.0%} of {len(strikes)} strikes satisfy the bound "
                f"(forward={forward!r})",
            )

    if strikes and spot > 0:
        strikes_sorted = sorted(strikes)
        mid_idx = len(strikes_sorted) // 2
        if len(strikes_sorted) % 2:
            median = strikes_sorted[mid_idx]
        else:
            median = 0.5 * (strikes_sorted[mid_idx - 1] + strikes_sorted[mid_idx])
        ratio = median / spot
        if not (0.2 <= ratio <= 5.0):
            return BasisCheckResult(
                True,
                "0.2 <= median(strike) / spot <= 5.0",
                f"median(strike)/spot={ratio!r} (median={median!r}, spot={spot!r})",
            )

    return BasisCheckResult(False)


class DataBreakError(Exception):
    """The inputs exist but do not belong together: a spot from another
    session, or a mark outside its no-arbitrage bounds or inconsistent with
    the quote source's own IV.

    Distinct from a coverage gap (nothing observed) and from an unexplained
    break (the market did something the model did not capture). Nothing is
    narrated and no correction is applied.
    """

    def __init__(self, check: str, detail: str) -> None:
        self.check = check
        self.detail = detail
        super().__init__(self.report_text())

    def report_text(self) -> str:
        return (
            f"Data break: {self.check} failed. {self.detail} No correction applied; "
            "nothing was narrated. This is a data problem, not an unexplained market move."
        )


@dataclass
class MarkCheckResult:
    failing_check: Optional[str] = None
    detail: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.failing_check is None

    def error(self) -> DataBreakError:
        return DataBreakError(self.failing_check or "mark check", self.detail or "")


# A mark may sit this far outside a no-arbitrage bound before it counts as a
# break: half today's quoted spread, 1% of the larger of mark and bound, or a
# cent, whichever is widest. Mids of deep ITM options print a few cents under
# intrinsic without anything being wrong.
MARK_BOUND_REL_TOL = 0.01
MARK_BOUND_ABS_TOL = 0.01

# Calibrated-vs-vendor IV cross-check. The quote source computes its IV with
# its own spot at quote time, so a mark paired with another session's spot
# calibrates to a vol far from the source's. Deep ITM marks carry almost no vol
# information (the source's IV there is noise), so the check needs time value
# of at least 30% of the mark. On the 2026-08..11 live cache this flags none of
# the 272 rows whose spot matched the session close, except one last-trade
# mark with no two-sided quote; it flags the stale-spot rows with a large move.
IV_CHECK_MIN_TIME_VALUE_SHARE = 0.30
IV_CHECK_ABS_PTS = 5.0
IV_CHECK_REL = 0.25


def _years(start: date, end: date) -> float:
    return max((end - start).days, 0) / 365.0


def _mark_bounds(snap: MarketSnapshot, spot: float, eval_date: date) -> tuple[float, float]:
    """(lower, upper) no-arbitrage bounds for one mark of this contract."""
    k = float(snap.strike)
    expiry = date.fromisoformat(snap.expiry)
    tau = _years(eval_date, expiry)
    r = float(snap.risk_free_rate)
    disc = math.exp(-r * tau)
    if snap.discrete_dividends:
        pv_div = sum(
            float(d.amount) * math.exp(-r * _years(eval_date, date.fromisoformat(d.ex_date)))
            for d in snap.discrete_dividends
            if eval_date < date.fromisoformat(d.ex_date) <= expiry
        )
        carried_spot = spot - pv_div
    else:
        carried_spot = spot * math.exp(-float(snap.dividend_yield) * tau)
    if str(snap.option_type).lower().startswith("c"):
        lower = max(carried_spot - k * disc, 0.0)
        upper = spot
    else:
        lower = max(k * disc - carried_spot, 0.0)
        upper = k if snap.exercise_style == "american" else k * disc
    if snap.exercise_style == "american":
        lower = max(lower, intrinsic_value(snap.option_type, spot, k))
    return lower, upper


def _contract_label(snap: MarketSnapshot) -> str:
    return f"{snap.ticker} {snap.strike:g}{str(snap.option_type)[:1].upper()} {snap.expiry}"


def _observed_marks(snap: MarketSnapshot):
    """(label, date, spot, mark) for each date that has an observed mark."""
    for label, eval_date, spot, mark in (
        ("T", snap.as_of_date(), snap.spot_now, snap.option_price_now),
        ("T-1", snap.prev_date(), snap.spot_prev, snap.option_price_prev),
    ):
        if mark is not None and mark > 0 and spot is not None and spot > 0:
            yield label, eval_date, float(spot), float(mark)


def check_mark_bounds(snap: MarketSnapshot) -> MarkCheckResult:
    """Both marks inside their no-arbitrage bounds at their own date's spot.

    Lower bound: intrinsic for an American, the discounted forward intrinsic
    for either style. Upper bound: spot for a call, strike for a put. A date
    without a mark (synthetic fixtures, a first live day) is skipped.
    """
    half_spread = 0.0
    if snap.bid is not None and snap.ask is not None and snap.ask >= snap.bid > 0:
        half_spread = 0.5 * (float(snap.ask) - float(snap.bid))
    for label, eval_date, spot, mark in _observed_marks(snap):
        lower, upper = _mark_bounds(snap, spot, eval_date)
        tol = max(half_spread, MARK_BOUND_REL_TOL * max(mark, lower), MARK_BOUND_ABS_TOL)
        if mark < lower - tol:
            return MarkCheckResult(
                f"{label} mark >= no-arbitrage lower bound",
                f"{_contract_label(snap)} mark {mark:.4f} on {eval_date} is below its lower "
                f"bound {lower:.4f} at spot {spot:.2f} (tolerance {tol:.4f}).",
            )
        if mark > upper + tol:
            return MarkCheckResult(
                f"{label} mark <= no-arbitrage upper bound",
                f"{_contract_label(snap)} mark {mark:.4f} on {eval_date} is above its upper "
                f"bound {upper:.4f} at spot {spot:.2f} (tolerance {tol:.4f}).",
            )
    return MarkCheckResult()


def check_calibrated_iv(
    snap: MarketSnapshot,
    *,
    iv_cal_now: Optional[float],
    iv_cal_prev: Optional[float],
) -> MarkCheckResult:
    """Mark-calibrated vols agree with the quote source's own IV readings.

    T-1 is checked only when its source IV is a real chain reading
    (``iv_prev_source == "chain_t1"``), never a proxy.
    """
    calibrated = {"T": iv_cal_now, "T-1": iv_cal_prev}
    source_iv = {"T": snap.iv_now, "T-1": snap.iv_prev if snap.iv_prev_source == "chain_t1" else None}
    for label, eval_date, spot, mark in _observed_marks(snap):
        cal, ref = calibrated[label], source_iv[label]
        if cal is None or ref is None or not (ref >= MIN_PLAUSIBLE_IV):
            continue
        time_value = mark - intrinsic_value(snap.option_type, spot, snap.strike)
        if time_value < IV_CHECK_MIN_TIME_VALUE_SHARE * mark:
            continue
        gap_pts = (float(cal) - float(ref)) * 100.0
        if abs(gap_pts) > IV_CHECK_ABS_PTS and abs(gap_pts) > IV_CHECK_REL * float(ref) * 100.0:
            return MarkCheckResult(
                f"{label} calibrated IV ~= quote-source IV",
                f"{_contract_label(snap)} mark {mark:.4f} on {eval_date} at spot {spot:.2f} "
                f"calibrates to {cal * 100:.2f}% vol; the quote source reads {ref * 100:.2f}% "
                f"({gap_pts:+.2f} vol pts). A mark and a spot taken at different times "
                "produce this gap.",
            )
    return MarkCheckResult()
