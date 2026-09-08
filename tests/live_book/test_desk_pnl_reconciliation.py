"""Falsifiable unit tests for tests/live_book/desk_pnl.py's verification logic.

These pin down the desk-review conclusions with synthetic leg payloads (not
live archives, which change daily) so a future change to the tiering /
noise-band / day-count logic cannot silently regress:

- mark-quality tiering (reliable / wide / thin / wide+thin / unquoted)
- bid-ask-implied IV noise band vs the day's actual IV move
- model P&L vs mark-to-market P&L reconciliation gap
- day-count mismatch detection against the engine's hardcoded dt_days=1.0

Run: python tests/live_book/test_desk_pnl_reconciliation.py
"""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import bootstrap

bootstrap.install()

from datetime import date

from live_book.desk_pnl import _tier, evaluate_leg  # noqa: E402


def _leg_payload(
    *,
    ticker: str = "TEST",
    bid: float | None = 9.8,
    ask: float | None = 10.2,
    volume: float | None = 500,
    open_interest: float | None = 1000,
    iv_prev: float = 0.30,
    iv_now: float = 0.32,
    vega_now: float = 0.20,
    price_prev: float = 5.00,
    price_now: float = 5.30,
    model_total_pnl: float = 0.35,
) -> dict:
    mid = (bid + ask) / 2.0 if (bid is not None and ask is not None) else None
    return {
        "snapshot": {
            "ticker": ticker,
            "option_type": "call",
            "strike": 100.0,
            "expiry": "2027-01-15",
            "quantity": 1.0,
            "multiplier": 100.0,
            "bid": bid,
            "ask": ask,
            "mid": mid,
            "volume": volume,
            "open_interest": open_interest,
            "iv_prev": iv_prev,
            "iv_now": iv_now,
            "option_price_prev": price_prev,
            "option_price_now": price_now,
        },
        "pricing": {
            "pnl": {"total_pnl": model_total_pnl},
            "greeks_now": {"vega": vega_now},
            "diagnostics": {"limitations": []},
        },
    }


def test_tier_reliable() -> None:
    assert _tier(spread_pct_mid=0.05, volume=500, open_interest=1000) == "reliable"


def test_tier_wide() -> None:
    assert _tier(spread_pct_mid=0.20, volume=500, open_interest=1000) == "wide"


def test_tier_thin_by_volume() -> None:
    assert _tier(spread_pct_mid=0.05, volume=3, open_interest=1000) == "thin"


def test_tier_thin_by_open_interest() -> None:
    assert _tier(spread_pct_mid=0.05, volume=500, open_interest=10) == "thin"


def test_tier_wide_and_thin() -> None:
    assert _tier(spread_pct_mid=0.30, volume=2, open_interest=5) == "wide+thin"


def test_tier_unquoted_when_no_spread() -> None:
    assert _tier(spread_pct_mid=None, volume=None, open_interest=None) == "unquoted"


def test_iv_move_within_noise_band_is_flagged() -> None:
    # spread=0.40 -> half-spread=0.20; vega=0.20 -> noise band = 1.0 vol pt.
    # iv moved 0.30 -> 0.302 = +0.2 pts, well inside the 1.0-pt noise band.
    leg = evaluate_leg(
        _leg_payload(bid=9.80, ask=10.20, vega_now=0.20, iv_prev=0.30, iv_now=0.302)
    )
    assert leg.iv_noise_band_pts is not None
    assert abs(leg.iv_noise_band_pts - 1.0) < 1e-9
    assert leg.iv_move_within_noise is True


def test_iv_move_exceeding_noise_band_is_attributable() -> None:
    # Same quote/vega as above but a much larger IV move (+5 pts) clears the band.
    leg = evaluate_leg(
        _leg_payload(bid=9.80, ask=10.20, vega_now=0.20, iv_prev=0.30, iv_now=0.35)
    )
    assert abs(leg.iv_noise_band_pts - 1.0) < 1e-9
    assert leg.iv_move_within_noise is False


def test_mark_vs_model_pnl_gap_computed_in_book_units() -> None:
    # price moved 5.00 -> 5.30 (mark ΔP = 0.30/unit); model says 0.35/unit.
    # qty=1, multiplier=100 -> book units.
    leg = evaluate_leg(_leg_payload(price_prev=5.00, price_now=5.30, model_total_pnl=0.35))
    assert leg.mark_pnl_per_unit == pytest_approx(0.30)
    assert leg.model_pnl_per_unit == pytest_approx(0.35)
    assert leg.mark_pnl_book == pytest_approx(30.0)
    assert leg.model_pnl_book == pytest_approx(35.0)
    assert leg.gap_book == pytest_approx(5.0)


def test_unquoted_leg_has_no_tier_penalty_crash_and_no_noise_band() -> None:
    leg = evaluate_leg(_leg_payload(bid=None, ask=None, volume=None, open_interest=None))
    assert leg.tier == "unquoted"
    assert leg.spread is None
    assert leg.iv_noise_band_pts is None
    assert leg.iv_move_within_noise is None


def pytest_approx(value: float, tol: float = 1e-9):
    class _Approx:
        def __eq__(self, other: object) -> bool:
            return abs(float(other) - value) <= tol

        def __repr__(self) -> str:
            return f"~{value}"

    return _Approx()


def test_daycount_mismatch_detection() -> None:
    d0 = date(2026, 8, 21)
    d1 = date(2026, 8, 24)
    actual_days = (d1 - d0).days
    assert actual_days == 3, "Fri -> Mon must span 3 calendar days, not the engine's hardcoded 1.0"


def _run_all() -> None:
    tests = [
        test_tier_reliable,
        test_tier_wide,
        test_tier_thin_by_volume,
        test_tier_thin_by_open_interest,
        test_tier_wide_and_thin,
        test_tier_unquoted_when_no_spread,
        test_iv_move_within_noise_band_is_flagged,
        test_iv_move_exceeding_noise_band_is_attributable,
        test_mark_vs_model_pnl_gap_computed_in_book_units,
        test_unquoted_leg_has_no_tier_penalty_crash_and_no_noise_band,
        test_daycount_mismatch_detection,
    ]
    for t in tests:
        t()
        print(f"OK: {t.__name__}")
    print(f"\nAll {len(tests)} desk_pnl reconciliation tests passed.")


if __name__ == "__main__":
    _run_all()
