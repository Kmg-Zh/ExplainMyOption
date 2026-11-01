"""Test-only helpers: ATM / ITM / OTM strike selection for portfolio e2e books."""

from __future__ import annotations

from typing import Literal

import pandas as pd

Moneyness = Literal["ATM", "ITM", "OTM"]


def target_spot_for_moneyness(
    spot: float,
    option_type: str,
    moneyness: Moneyness,
    *,
    distance_pct: float = 0.05,
) -> float:
    """Map moneyness label to a target underlying level for strike search."""
    if moneyness == "ATM":
        return float(spot)
    d = abs(float(distance_pct))
    right = option_type.lower()
    if right == "call":
        return float(spot) * (1.0 - d if moneyness == "ITM" else 1.0 + d)
    return float(spot) * (1.0 + d if moneyness == "ITM" else 1.0 - d)


def pick_strike(
    chain: pd.DataFrame,
    spot: float,
    option_type: str,
    moneyness: Moneyness = "ATM",
    *,
    distance_pct: float = 0.05,
) -> float:
    """Return the listed strike closest to the moneyness target."""
    if chain is None or chain.empty:
        raise ValueError("Empty option chain.")
    if "strike" not in chain.columns:
        raise ValueError("Chain missing strike column.")
    target = target_spot_for_moneyness(
        spot, option_type, moneyness, distance_pct=distance_pct
    )
    idx = (chain["strike"].astype(float) - target).abs().idxmin()
    return float(chain.loc[idx, "strike"])
