"""Historical-chain adapter: Task A4.2 (quote hygiene) and A4.0 (source client).

Offline / synthetic only -- no network. The live-network path (A4.1's
``HistoricalChainMarketLoader.load()`` against real DoltHub/yfinance data)
is exercised separately by the two verified real cases (A4.5), which are
not part of the offline CI suite for the same reason nothing else in this
repo makes a live network call in CI.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from explain_my_option.data.historical_chain import quote_hygiene

AS_OF = date(2026, 1, 15)
FAR_EXPIRY = "2026-07-15"  # ~181 days out, just past the max_dte=180 default


def _row(**kwargs):
    base = {
        "date": "2026-01-15",
        "act_symbol": "TEST",
        "expiration": "2026-06-15",  # ~151 days -> inside [7, 180]
        "strike": 100.0,
        "call_put": "Call",
        "bid": 4.9,
        "ask": 5.1,
        "vol": 0.30,
    }
    base.update(kwargs)
    return base


def test_well_formed_quote_is_kept_and_tiered_tight():
    result = quote_hygiene([_row(bid=4.95, ask=5.05)], as_of=AS_OF)
    assert len(result.kept) == 1
    assert result.kept[0]["quote_tier"] == "tight"
    assert not result.rejected


def test_zero_bid_is_rejected():
    result = quote_hygiene([_row(bid=0.0, ask=1.0)], as_of=AS_OF)
    assert not result.kept
    assert result.rejected[0][1] == "bid<=0"


def test_crossed_quote_is_rejected():
    result = quote_hygiene([_row(bid=5.0, ask=5.0)], as_of=AS_OF)
    assert not result.kept
    assert result.rejected[0][1] == "ask<=bid"


def test_sub_nickel_mid_is_rejected():
    result = quote_hygiene([_row(bid=0.01, ask=0.03)], as_of=AS_OF)
    assert not result.kept
    assert result.rejected[0][1] == "mid<0.05"


def test_wide_relative_spread_is_rejected():
    # mid = 5.5, spread = 3.0 -> rel_spread = 0.545 > 0.25
    result = quote_hygiene([_row(bid=4.0, ask=7.0)], as_of=AS_OF)
    assert not result.kept
    assert result.rejected[0][1] == "relative_spread>0.25"


def test_quote_tier_bands():
    tight = quote_hygiene([_row(bid=4.99, ask=5.01)], as_of=AS_OF).kept[0]  # rel ~0.4%
    normal = quote_hygiene([_row(bid=4.8, ask=5.2)], as_of=AS_OF).kept[0]  # rel = 8%
    wide = quote_hygiene([_row(bid=4.5, ask=5.5)], as_of=AS_OF).kept[0]  # rel = 20%
    assert tight["quote_tier"] == "tight"
    assert normal["quote_tier"] == "normal"
    assert wide["quote_tier"] == "wide"


def test_dte_outside_window_is_rejected():
    too_soon = quote_hygiene(
        [_row(expiration="2026-01-18")], as_of=AS_OF  # 3 DTE < 7
    )
    assert not too_soon.kept
    assert "DTE" in too_soon.rejected[0][1]

    too_far = quote_hygiene(
        [_row(expiration="2026-08-15")], as_of=AS_OF  # ~212 DTE > 180
    )
    assert not too_far.kept
    assert "DTE" in too_far.rejected[0][1]


def test_volume_open_interest_check_marked_not_applicable():
    result = quote_hygiene([_row()], as_of=AS_OF)
    assert result.volume_oi_check_applicable is False


if __name__ == "__main__":
    test_well_formed_quote_is_kept_and_tiered_tight()
    test_zero_bid_is_rejected()
    test_crossed_quote_is_rejected()
    test_sub_nickel_mid_is_rejected()
    test_wide_relative_spread_is_rejected()
    test_quote_tier_bands()
    test_dte_outside_window_is_rejected()
    test_volume_open_interest_check_marked_not_applicable()
    print("OK — historical chain (quote hygiene) tests passed")
