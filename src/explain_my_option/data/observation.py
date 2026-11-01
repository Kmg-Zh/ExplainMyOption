"""Input guards that run before pricing.

1. Continuity: a one-day attribution needs the same contract observed on both
   T-1 and T. A missing day or contract is a data coverage gap, never an
   unexplained market move.
2. Basis consistency: splits and ticker renames fail silently, because a
   mis-based price still looks plausible. No-arbitrage sanity bounds on the
   raw quotes catch them before the engine sees them.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional, Sequence


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
