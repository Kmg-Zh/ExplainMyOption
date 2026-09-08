"""Data-agnostic QuantLib pricing facade.

Consumes plain dataclasses only — never imports yfinance or fixture I/O.
"""

from .analysis_api import compare_to_official
from .config import EngineConfig, MertonParams
from .facade import price_and_attribute
from .types import (
    CrossCheckResult,
    Greeks,
    MarketSnapshot,
    PnLAttribution,
    PricingDiagnostics,
    PricingResult,
    SurfaceDiagnostics,
    VolSurfaceData,
)

__all__ = [
    "CrossCheckResult",
    "EngineConfig",
    "Greeks",
    "MarketSnapshot",
    "MertonParams",
    "PnLAttribution",
    "PricingDiagnostics",
    "PricingResult",
    "SurfaceDiagnostics",
    "VolSurfaceData",
    "compare_to_official",
    "price_and_attribute",
]
