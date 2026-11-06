"""Expiry settlement: a leg's last day, accounted without a model.

A listed equity option still open at the close of its expiry session is worth
its intrinsic value at that close: OCC exercises it when it closes at least
$0.01 in the money, unless the holder instructs otherwise. The settlement
day's PnL therefore needs no pricer, vol or news, and it splits exactly:

    settlement − prior mark = [intrinsic(S_E) − intrinsic(S_prev)] − (prior mark − intrinsic(S_prev))

the spot move on intrinsic value, plus the time value the prior mark still
carried, released at expiry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional, Sequence

from ..pricing.types import MarketSnapshot
from .formatting import contract_id, money

AUTO_EXERCISE_THRESHOLD = 0.01
# A close this near the strike leaves exercise to the holder's late
# instruction, so the short side cannot be sure of assignment.
PIN_BAND = 0.005

Outcome = Literal["exercised", "assigned", "expired worthless"]


def is_settlement(snap: MarketSnapshot) -> bool:
    """True when the snapshot's session is on or after the contract's expiry."""
    return bool(snap.as_of) and snap.as_of >= snap.expiry


def intrinsic(option_type: str, strike: float, spot: float) -> float:
    if option_type == "call":
        return max(spot - strike, 0.0)
    return max(strike - spot, 0.0)


@dataclass(frozen=True)
class ExpirySettlement:
    """One leg settled at intrinsic value. Figures are per option unless named ``position_``."""

    contract: str
    option_type: str
    strike: float
    session: str
    spot: float
    value: float
    quantity: float
    multiplier: float
    prior_mark: Optional[float] = None
    prior_mark_session: Optional[str] = None
    spot_prev: Optional[float] = None

    @property
    def scale(self) -> float:
        return self.quantity * self.multiplier

    @property
    def outcome(self) -> Outcome:
        if self.value < AUTO_EXERCISE_THRESHOLD:
            return "expired worthless"
        return "assigned" if self.quantity < 0 else "exercised"

    @property
    def pin(self) -> bool:
        return abs(self.spot - self.strike) <= PIN_BAND * self.strike

    @property
    def has_prior_mark(self) -> bool:
        return self.prior_mark is not None and self.spot_prev is not None

    @property
    def intrinsic_change(self) -> float:
        return self.value - intrinsic(self.option_type, self.strike, self.spot_prev or 0.0)

    @property
    def time_value_released(self) -> float:
        return -((self.prior_mark or 0.0) - intrinsic(self.option_type, self.strike, self.spot_prev or 0.0))

    @property
    def pnl(self) -> Optional[float]:
        """Settlement value minus the prior mark; None without a prior mark."""
        return self.value - self.prior_mark if self.has_prior_mark else None

    @property
    def position_pnl(self) -> Optional[float]:
        return None if self.pnl is None else self.pnl * self.scale

    def delivery(self) -> str:
        if self.outcome == "expired worthless":
            return "Expires worthless: no exercise, no stock delivery."
        shares = abs(self.quantity) * self.multiplier
        buys = (self.option_type == "call") == (self.quantity >= 0)
        side = "buys" if buys else "sells"
        verb = "Exercised" if self.outcome == "exercised" else "Assigned"
        return (
            f"{verb}: the position {side} {shares:g} shares at {self.strike:g}. "
            "This report does not track the resulting stock position."
        )


def settle(snap: MarketSnapshot) -> ExpirySettlement:
    """Settle a snapshot whose ``as_of`` is its expiry session (``spot_now`` is that close).

    ``option_price_prev`` is the last mark before expiry; ``0.0`` means none.
    """
    has_prior = snap.option_price_prev > 0
    return ExpirySettlement(
        contract=contract_id(snap),
        option_type=snap.option_type,
        strike=float(snap.strike),
        session=str(snap.as_of),
        spot=float(snap.spot_now),
        value=intrinsic(snap.option_type, snap.strike, snap.spot_now),
        quantity=float(snap.quantity),
        multiplier=float(snap.multiplier),
        prior_mark=float(snap.option_price_prev) if has_prior else None,
        prior_mark_session=snap.prev_as_of if has_prior else None,
        spot_prev=float(snap.spot_prev) if has_prior else None,
    )


def render_settlement(s: ExpirySettlement, *, heading: str = "## Expiry Settlement") -> str:
    lines = [
        heading,
        "",
        f"`{s.contract}` expired at the {s.session} close (spot {s.spot:,.2f}) and settles at "
        f"intrinsic value, {s.value:,.4f} per option. No model, vol or news search is involved.",
        "",
    ]
    if s.has_prior_mark:
        lines.extend(
            [
                f"Prior mark: {s.prior_mark:,.4f} on {s.prior_mark_session} (spot {s.spot_prev:,.2f}).",
                "",
                "| Component | Per option | Position ($) |",
                "| :--- | ---: | ---: |",
                f"| Intrinsic change from spot | `{money(s.intrinsic_change)}` | `{money(s.intrinsic_change * s.scale)}` |",
                f"| Time value released | `{money(s.time_value_released)}` | `{money(s.time_value_released * s.scale)}` |",
                f"| **Settlement PnL** | `{money(s.pnl)}` | `{money(s.position_pnl)}` |",
                "",
            ]
        )
    else:
        lines.extend(["No prior mark is on record for this contract, so the settlement PnL is not computed.", ""])
    lines.append(f"* {s.delivery()}")
    if s.pin:
        lines.append(
            f"* Pin: the close is within {PIN_BAND:.1%} of the strike, so exercise turns on the holder's "
            "instruction and assignment on a short position is not certain."
        )
    return "\n".join(lines) + "\n"


def render_settlements(settlements: Sequence[ExpirySettlement]) -> str:
    """The book section for legs settled at expiry: a table, then each leg."""
    lines = [
        "## Settled at expiry",
        "",
        "| Contract | Outcome | Settlement | PnL ($) |",
        "| :--- | :--- | ---: | ---: |",
    ]
    for s in settlements:
        pnl = "n/a" if s.position_pnl is None else f"`{money(s.position_pnl)}`"
        lines.append(f"| `{s.contract}` | {s.outcome} | {s.value:,.4f} | {pnl} |")
    lines.append("")
    for s in settlements:
        lines.append(render_settlement(s, heading=f"### Settled — `{s.contract}`"))
    return "\n".join(lines).rstrip() + "\n"


def settlement_total(settlements: Sequence[ExpirySettlement]) -> float:
    return sum(s.position_pnl or 0.0 for s in settlements)
