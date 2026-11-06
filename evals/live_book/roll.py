"""The run log's roll rule (``docs/runlog/book.json``).

A leg is held to expiry. The run that settles it replaces it with the same
leg on a new contract, opened at that run's session close:

* expiry: the first standard monthly expiry (the third Friday, or the
  Thursday before it when that Friday is not listed) at least ``MIN_DTE``
  calendar days after the roll session;
* strike: among strikes with a two-sided quote, the one nearest
  ``target_strike_to_spot × spot``. The target is the strike / spot ratio
  the leg was first picked with and is carried unchanged through every roll,
  so a vertical, straddle or risk reversal keeps its shape.

No model or vendor IV is involved. The successor's snapshot is cached at the
roll session, so the next run compares against a real prior mark.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Iterable, Mapping

MIN_DTE = 35


def third_friday(year: int, month: int) -> date:
    first = date(year, month, 1)
    return first + timedelta(days=(4 - first.weekday()) % 7 + 14)


def is_standard_monthly(expiry: date, listed: set[date]) -> bool:
    friday = third_friday(expiry.year, expiry.month)
    return expiry == friday or (expiry == friday - timedelta(days=1) and friday not in listed)


def pick_expiry(listed: Iterable[str], roll_session: date, *, min_dte: int = MIN_DTE) -> str:
    dates = {date.fromisoformat(e) for e in listed}
    for d in sorted(dates):
        if (d - roll_session).days >= min_dte and is_standard_monthly(d, dates):
            return d.isoformat()
    raise ValueError(f"No standard monthly expiry at least {min_dte} days after {roll_session} is listed.")


def pick_strike(quoted_strikes: Iterable[float], target: float) -> float:
    """The quoted strike nearest ``target``; a tie goes to the lower strike."""
    strikes = sorted(set(float(k) for k in quoted_strikes))
    if not strikes:
        raise ValueError("No strike has a two-sided quote.")
    return min(strikes, key=lambda k: (abs(k - target), k))


@dataclass(frozen=True)
class RollInputs:
    """What the rule reads at the roll session: spot and the listed contracts."""

    session: date
    spot: float
    expiries: tuple[str, ...]
    quoted_strikes: Mapping[str, tuple[float, ...]]  # expiry -> strikes with bid > 0 and ask > 0


def contract_label(row: Mapping[str, Any]) -> str:
    right = "C" if row["option_type"] == "call" else "P"
    return f"{row['ticker']} {float(row['strike']):g}{right} {row['expiry']}"


def successor(row: Mapping[str, Any], inputs: RollInputs) -> dict[str, Any]:
    """The book row that replaces ``row``: same leg, new expiry and strike."""
    expiry = pick_expiry(inputs.expiries, inputs.session)
    ratio = float(row["target_strike_to_spot"])
    strike = pick_strike(inputs.quoted_strikes.get(expiry, ()), ratio * inputs.spot)
    new = dict(row)
    new.update(
        strike=strike,
        expiry=expiry,
        spot_at_pick=round(inputs.spot, 4),
        picked_session=inputs.session.isoformat(),
        notes=(
            f"Rolled from {contract_label(row)} at the {inputs.session} close by the roll rule "
            f"(target strike/spot {ratio:g}, spot {inputs.spot:,.2f})."
        ),
    )
    return new


def live_roll_inputs(ticker: str, option_type: str) -> RollInputs:
    """Read the roll session's spot and listed contracts from yfinance."""
    import yfinance as yf

    from explain_my_option.data_loader import _finite_or_none, _history_metadata, _exchange_date
    from explain_my_option.data_loader import quote_session, session_close

    tk = yf.Ticker(ticker)
    hist = tk.history(period="1mo", auto_adjust=False)
    md = _history_metadata(tk)
    session = quote_session(hist, md)
    spot = session_close(
        hist,
        session,
        market_price=_finite_or_none(md.get("regularMarketPrice")),
        market_price_session=_exchange_date(md.get("regularMarketTime"), md.get("exchangeTimezoneName")),
    )
    expiries = tuple(tk.options or ())
    expiry = pick_expiry(expiries, session)
    chain = tk.option_chain(expiry)
    table = chain.calls if option_type == "call" else chain.puts
    quoted = tuple(
        float(r.strike)
        for r in table.itertuples()
        if _finite_or_none(r.bid) and _finite_or_none(r.ask) and r.bid > 0 and r.ask > 0
    )
    return RollInputs(session=session, spot=spot, expiries=expiries, quoted_strikes={expiry: quoted})
