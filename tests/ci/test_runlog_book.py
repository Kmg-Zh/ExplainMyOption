"""Task C3.1: the 30-day live-book run log's book definition. Offline,
structural checks only -- no network, no pricing. scripts/daily_run.py
(not in run-tests.sh, needs OPENAI_API_KEY + live network -- same
convention as historical/run.py) is what actually prices these legs.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from live_book.portfolio_book import load_pinned_book

BOOK_PATH = _TESTS_DIR.parent / "docs" / "runlog" / "book.json"


def test_book_has_eight_legs_with_unique_ids():
    baseline, legs = load_pinned_book(BOOK_PATH)
    assert len(legs) == 8
    ids = [leg.leg_id for leg in legs]
    assert all(ids), "every leg needs a leg_id (scripts/daily_run.py keys metrics by it)"
    assert len(set(ids)) == len(ids), "leg_id must be unique"
    datetime.strptime(baseline, "%Y-%m-%d")


def test_every_leg_is_at_least_35_dte_at_baseline():
    """C3.1: no rolls needed inside a 30-day window."""
    baseline, legs = load_pinned_book(BOOK_PATH)
    base_d = datetime.strptime(baseline, "%Y-%m-%d").date()
    for leg in legs:
        exp_d = date.fromisoformat(leg.expiry)
        dte = (exp_d - base_d).days
        assert dte >= 35, f"{leg.leg_id}: {dte} DTE at baseline, need >=35"


def test_book_covers_the_required_structures():
    """C3.1's table: vertical spread, straddle, risk reversal, ITM div
    payer, deep-OTM thin name -- checked by leg_id naming, not by strike
    math (the strikes themselves are real, live-discovered contracts)."""
    _, legs = load_pinned_book(BOOK_PATH)
    ids = {leg.leg_id for leg in legs}
    for expected in (
        "aapl_vertical_long", "aapl_vertical_short",
        "jpm_straddle_call", "jpm_straddle_put",
        "spy_reversal_put", "spy_reversal_call",
        "vz_div_call", "plug_deep_otm",
    ):
        assert expected in ids, f"missing leg_id {expected!r}"


def test_vertical_spread_legs_offset_and_share_expiry():
    _, legs = load_pinned_book(BOOK_PATH)
    by_id = {leg.leg_id: leg for leg in legs}
    long_leg = by_id["aapl_vertical_long"]
    short_leg = by_id["aapl_vertical_short"]
    assert long_leg.expiry == short_leg.expiry
    assert long_leg.strike != short_leg.strike
    assert long_leg.quantity > 0 and short_leg.quantity < 0


def test_straddle_legs_share_strike_and_expiry():
    _, legs = load_pinned_book(BOOK_PATH)
    by_id = {leg.leg_id: leg for leg in legs}
    call_leg = by_id["jpm_straddle_call"]
    put_leg = by_id["jpm_straddle_put"]
    assert call_leg.strike == put_leg.strike
    assert call_leg.expiry == put_leg.expiry
    assert call_leg.option_type == "call" and put_leg.option_type == "put"


if __name__ == "__main__":
    test_book_has_eight_legs_with_unique_ids()
    test_every_leg_is_at_least_35_dte_at_baseline()
    test_book_covers_the_required_structures()
    test_vertical_spread_legs_offset_and_share_expiry()
    test_straddle_legs_share_strike_and_expiry()
    print("OK — runlog book structural tests passed")
