"""Shared graph state types to avoid cross-module import cycles."""

from __future__ import annotations

from typing import Optional, TypedDict

from ..data_loader import MarketSnapshot, NewsItem
from ..intel.types import SearchPlan
from ..pricing.types import PricingResult, VolSurfaceData


class OptionState(TypedDict, total=False):
    """Single-leg compatibility view used by app.py and tests."""

    ticker: str
    option_type: str
    strike: Optional[float]
    expiry: Optional[str]
    quantity: float
    multiplier: float

    snapshot: MarketSnapshot
    surface: Optional[VolSurfaceData]
    surface_prev: Optional[VolSurfaceData]
    pricing: PricingResult
    blotter: str
    diagnostic_findings: dict
    search_plan: SearchPlan
    news: list[NewsItem]
    intel_digest: dict
    diagnosis: str
    diagnostic_synthesis: dict
    catalyst_challenge: dict
    report: str
