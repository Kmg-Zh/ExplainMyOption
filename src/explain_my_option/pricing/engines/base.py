"""PricingEngine protocol — swap numerical methods without changing the facade."""

from __future__ import annotations

from typing import Protocol

from ..types import EngineId, Greeks, PricingSpec


class PricingEngine(Protocol):
    name: EngineId

    def price(self, spec: PricingSpec) -> tuple[Greeks, list[str]]:
        """Return Greeks and engine-local limitation flags."""
        ...
