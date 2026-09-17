"""Fixed portfolio books for offline CI and live multi-day e2e (test-only)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from live_book.strikes import Moneyness

ExerciseStyle = Literal["american", "european"]

_LIVE_BOOK_DIR = Path(__file__).resolve().parent
DEFAULT_PINNED_BOOK = (
    _LIVE_BOOK_DIR / "pinned_books" / "book_2026-09-14.json"
)


@dataclass(frozen=True)
class OfflineLeg:
    """One synthetic leg: fixture base + display ticker + optional snapshot overrides."""

    ticker: str
    fixture: str
    moneyness: Moneyness
    overrides: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LiveLeg:
    """One live yfinance leg: moneyness target (discovery only; not for day-over-day)."""

    ticker: str
    option_type: Literal["call", "put"]
    moneyness: Moneyness
    exercise_style: ExerciseStyle = "american"
    quantity: float = 1.0
    multiplier: float = 1.0
    distance_pct: float = 0.05
    notes: str = ""


@dataclass(frozen=True)
class PinnedLeg:
    """Fixed listed contract for comparable multi-day live runs."""

    ticker: str
    option_type: Literal["call", "put"]
    strike: float
    expiry: str
    exercise_style: ExerciseStyle = "american"
    quantity: float = 1.0
    multiplier: float = 1.0
    moneyness_at_pin: str = ""
    notes: str = ""
    leg_id: str = ""


OFFLINE_AS_OF = "2026-08-14"

OFFLINE_LEGS: tuple[OfflineLeg, ...] = (
    OfflineLeg("AAPL", "spot_gap", "ITM"),
    OfflineLeg("MSFT", "put_skew", "OTM"),
    OfflineLeg("NVDA", "calibration_ok", "ATM"),
    OfflineLeg("GOOGL", "flat_only", "ATM", {"exercise_style": "european"}),
    OfflineLeg("XOM", "american_put_div", "ITM"),
    OfflineLeg("KO", "american_call_div", "ITM"),
    OfflineLeg("JPM", "american_put_div", "ITM"),
    OfflineLeg(
        "META", "vol_crush", "ATM", {"quantity": 2.0, "multiplier": 100.0}
    ),
    OfflineLeg("TSLA", "thin_surface", "ATM"),
    OfflineLeg("SPY", "put_skew", "OTM", {"exercise_style": "european"}),
)

# Discovery template only — prefer ``load_pinned_book`` for comparable live days.
LIVE_LEGS: tuple[LiveLeg, ...] = (
    LiveLeg("AAPL", "call", "ITM", notes="ITM equity call"),
    LiveLeg("MSFT", "put", "OTM", notes="OTM equity put"),
    LiveLeg("NVDA", "call", "ATM", notes="ATM growth name"),
    LiveLeg(
        "GOOGL",
        "call",
        "ATM",
        exercise_style="european",
        notes="European exercise override (engine path)",
    ),
    LiveLeg("XOM", "put", "ITM", notes="ITM put; dividend payer"),
    LiveLeg("KO", "call", "ITM", notes="ITM call; dividend / EE relevant"),
    LiveLeg("JPM", "put", "ITM", notes="ITM put; dividend payer"),
    LiveLeg(
        "META",
        "call",
        "ATM",
        quantity=2.0,
        multiplier=100.0,
        notes="Scaled lot for book PnL weight",
    ),
    LiveLeg("TSLA", "call", "ATM", notes="ATM; often thin / volatile surface"),
    LiveLeg(
        "SPY",
        "put",
        "OTM",
        exercise_style="european",
        notes="European put override on index ETF",
    ),
)


def load_pinned_book(
    path: Path | str | None = None,
) -> tuple[str, tuple[PinnedLeg, ...]]:
    """Load fixed contracts. Returns ``(baseline_as_of, legs)``."""
    book_path = Path(path) if path else DEFAULT_PINNED_BOOK
    payload = json.loads(book_path.read_text(encoding="utf-8"))
    baseline = str(payload["baseline_as_of"])
    legs = tuple(
        PinnedLeg(
            ticker=str(row["ticker"]).upper(),
            option_type=row["option_type"],
            strike=float(row["strike"]),
            expiry=str(row["expiry"]),
            exercise_style=row.get("exercise_style", "american"),
            quantity=float(row.get("quantity", 1.0)),
            multiplier=float(row.get("multiplier", 1.0)),
            moneyness_at_pin=str(row.get("moneyness_at_pin", "")),
            notes=str(row.get("notes", "")),
            leg_id=str(row.get("leg_id", "")),
        )
        for row in payload["legs"]
    )
    if not legs:
        raise ValueError(f"Pinned book has no legs: {book_path}")
    return baseline, legs
