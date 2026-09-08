"""Single-leg ``run_pipeline`` position scaling for fair benchmark parity.

Fixture JSON may carry ``multiplier=100`` for desk realism; the CLI book leg
defaults to ``quantity=1``, ``multiplier=1``. Baseline and governed paths must
share the same scale when comparing reports.
"""

from __future__ import annotations

from explain_my_option.pricing.types import MarketSnapshot

PIPELINE_QUANTITY = 1.0
PIPELINE_MULTIPLIER = 1.0


def apply_pipeline_position(snap: MarketSnapshot) -> MarketSnapshot:
    """Return the same snapshot with book-leg position fields applied."""
    snap.quantity = PIPELINE_QUANTITY
    snap.multiplier = PIPELINE_MULTIPLIER
    return snap


def pipeline_run_kwargs() -> dict[str, float]:
    return {
        "quantity": PIPELINE_QUANTITY,
        "multiplier": PIPELINE_MULTIPLIER,
    }
