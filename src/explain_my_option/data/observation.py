"""Observation preconditions and basis-consistency guards (Task A3).

Two independent problems, both about trusting the *inputs* before pricing:

1. A one-day attribution needs the *same contract* observed on both t-1 and
   t. When a source can't supply that -- a whole day missing, or just this
   contract missing on an otherwise-fine day -- that is a data coverage gap,
   not an unexplained market move, and must never be reported as one.
2. Splits and ticker renames fail *silently*: a mis-based price is still a
   plausible-looking number. A handful of no-arbitrage-adjacent sanity
   checks on the raw quotes catches this before it reaches the engine.

Both are source-agnostic. Today only the live/fixture single-contract path
exercises a subset of these (see ``leg_graph.fetch_market_node``); the full
per-date chain-level checks (strike-window diagnostics, labelled
substitution, the two multi-strike basis invariants) are built and tested
here so Task A4's historical-chain adapter has them ready to call.
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
    """A3.1: classify one date's observability for one contract.

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
    """A3.2: continuity gate failure. Never conflate with an unexplained break.

    One says the market did something the model did not capture; this says
    no comparison was possible at all. Carries both per-date statuses so
    the caller can route to a distinct terminal state.
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
    """A3.2: raise ``NoComparableObservationError`` unless both dates are OK."""
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
    """A3.5: the silent-failure catcher, run before pricing.

    A single-contract caller (today's live/fixture path) can only ever
    supply ``call_mid``/``put_mid`` + the matching strike; the two
    multi-strike checks need a full chain (``carried_strikes`` + a
    ``forward``), which only Task A4's historical adapter has. Whichever
    inputs are missing, that check is skipped -- never guessed. On a hit,
    never apply a correction factor: report the failing invariant and stop.
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


@dataclass
class StrikeWindowDiagnostics:
    """A3.3: per (symbol, date) strike-window coverage.

    Coverage narrows as the move widens, so deep-OTM contracts are
    systematically absent on the most extreme days -- that bias must be
    named in any case study built on a source exercising this.
    """

    strikes_available: tuple[float, ...]
    expiries_available: tuple[str, ...]
    spot: float

    @property
    def strike_min(self) -> Optional[float]:
        return min(self.strikes_available) if self.strikes_available else None

    @property
    def strike_max(self) -> Optional[float]:
        return max(self.strikes_available) if self.strikes_available else None


def compute_strike_overlap(
    t1: StrikeWindowDiagnostics, t: StrikeWindowDiagnostics, *, target_strike: float
) -> tuple[Optional[tuple[float, float]], bool]:
    """``(strike_overlap, overlap_contains_target)`` across the two dates."""
    if t1.strike_min is None or t.strike_min is None:
        return None, False
    lo = max(t1.strike_min, t.strike_min)
    hi = min(t1.strike_max, t.strike_max)  # type: ignore[arg-type]
    if lo > hi:
        return None, False
    return (lo, hi), (lo <= target_strike <= hi)


@dataclass
class SubstitutionResult:
    target_strike: float
    used_strike: float
    substitution_reason: str

    @property
    def substituted(self) -> bool:
        return self.used_strike != self.target_strike


def select_substitute_strike(
    *,
    target_strike: float,
    target_expiry: str,
    available: Mapping[str, Sequence[float]],
    overlap: tuple[float, float],
) -> Optional[SubstitutionResult]:
    """A3.4: labelled substitution. Never silent, never across expiries.

    ``available`` maps expiry -> strikes that are OK on *both* dates for
    that expiry only. Picks the nearest such strike to the target inside
    the overlap window, on the target's own expiry only.
    """
    strikes = available.get(target_expiry, ())
    lo, hi = overlap
    candidates = [k for k in strikes if lo <= k <= hi]
    if not candidates:
        return None
    if target_strike in candidates:
        return SubstitutionResult(target_strike, target_strike, "exact strike available")
    nearest = min(candidates, key=lambda k: abs(k - target_strike))
    return SubstitutionResult(
        target_strike=target_strike,
        used_strike=nearest,
        substitution_reason=(
            f"target strike {target_strike} not OK on both dates; substituted "
            f"nearest in-overlap strike {nearest} on the same expiry"
        ),
    )
