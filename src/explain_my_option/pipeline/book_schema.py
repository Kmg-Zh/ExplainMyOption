"""JSON portfolio book schema for the book-level Send fan-out."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from explain_my_option.paths import FIXTURES_DIR

BOOKS_DIR = FIXTURES_DIR / "books"

ExerciseStyle = Literal["american", "european"]


@dataclass(frozen=True)
class BookLegSpec:
    leg_id: str
    ticker: str
    fixture: str | None = None
    option_type: Literal["call", "put"] = "call"
    strike: float | None = None
    expiry: str | None = None
    quantity: float = 1.0
    multiplier: float = 1.0
    exercise_style: ExerciseStyle = "american"
    overrides: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BookSpec:
    version: str
    as_of: str
    legs: tuple[BookLegSpec, ...]


def load_book_json(path: Path | str) -> BookSpec:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    legs = []
    for raw in payload.get("legs", []):
        legs.append(
            BookLegSpec(
                leg_id=str(raw.get("leg_id") or raw["ticker"]),
                fixture=(str(raw["fixture"]) if raw.get("fixture") else None),
                ticker=str(raw["ticker"]),
                option_type=raw.get("option_type", "call"),
                strike=raw.get("strike"),
                expiry=raw.get("expiry"),
                quantity=float(raw.get("quantity", 1.0)),
                multiplier=float(raw.get("multiplier", 1.0)),
                exercise_style=raw.get("exercise_style", "american"),
                overrides=dict(raw.get("overrides") or {}),
            )
        )
    return BookSpec(
        version=str(payload.get("version", "1")),
        as_of=str(payload.get("as_of", "")),
        legs=tuple(legs),
    )


def default_book_fixture_path() -> Path:
    return BOOKS_DIR / "demo_book.json"
