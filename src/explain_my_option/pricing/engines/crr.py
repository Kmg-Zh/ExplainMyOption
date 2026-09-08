"""CRR binomial engine — retained, config-selectable."""

from __future__ import annotations

from typing import Optional

from ..config import EngineConfig
from ..ql_engine import price_american_crr, price_european_flat
from ..types import EngineId, Greeks, PricingSpec


class CrrEngine:
    name: EngineId = "crr"

    def __init__(self, config: Optional[EngineConfig] = None) -> None:
        self.config = config or EngineConfig.from_env()

    def price(self, spec: PricingSpec) -> tuple[Greeks, list[str]]:
        kwargs = dict(
            spot=spec.spot,
            strike=spec.strike,
            rate=spec.rate,
            dividend_yield=spec.dividend_yield,
            vol=spec.vol,
            expiry=spec.expiry,
            eval_date=spec.eval_date,
            option_type=spec.option_type,
            discrete_dividends=spec.discrete_dividends,
        )
        if spec.exercise_style == "european":
            return price_european_flat(**kwargs), []
        return price_american_crr(**kwargs, steps=self.config.crr_steps), []
