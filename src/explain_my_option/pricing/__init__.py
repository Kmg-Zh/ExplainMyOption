"""Reference pricing engine (QuantLib) and the plain dataclasses the agent consumes.

``types`` has no vendor imports and is the agent's input contract; the engine
entry points load lazily, so importing the types never pulls in QuantLib.
"""

from importlib import import_module

from .config import EngineConfig, MertonParams
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

_ENGINE_ENTRY_POINTS = {"price_and_attribute": ".facade", "compare_to_official": ".analysis_api"}


def __getattr__(name: str):
    if name in _ENGINE_ENTRY_POINTS:
        return getattr(import_module(_ENGINE_ENTRY_POINTS[name], __name__), name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


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
