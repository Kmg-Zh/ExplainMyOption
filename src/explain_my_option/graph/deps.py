"""Injectable ports for the product graph: swap market, PnL, planner and intel.

The defaults (yfinance market data, the QuantLib reference engine) are imported
only when used, so a desk that passes its own loader and PnL source never needs
them. See docs/INTEGRATION.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Protocol

from ..intel.planner import QueryPlanner, default_planner
from ..intel.sources import IntelRegistry, StubIntelSource, default_registry
from ..pricing.config import EngineConfig
from ..pricing.types import (
    LoadedData,
    MarketSnapshot,
    PricingResult,
    SecondOrderTaylorResult,
    SequentialRevalResult,
    VolSurfaceData,
)
from .playbook import DEFAULT_PLAYBOOK, PlaybookRecord, check_playbook
from .prompts import QUANTLIB_METHODOLOGY, extra_from_env


class MarketLoader(Protocol):
    def load(
        self,
        *,
        ticker: str,
        option_type: str,
        strike: Optional[float],
        expiry: Optional[str],
    ) -> LoadedData: ...


class PnlSource(Protocol):
    """The desk's 1-day PnL attribution for one position.

    Optional extras, used when present:
      ``methodology``: one paragraph, shown to the narrator, on how the PnL was computed.
      ``second_order(snapshot, pricing)``: vanna and volga terms (``SecondOrderTaylorResult``).
      ``path_reprice(snapshot, pricing, surface)``: full revaluation along t → S → σ → r
      (``SequentialRevalResult``).
    Without the last two, the diagnostic pass skips those audits and says so.
    """

    def attribute(
        self,
        snapshot: MarketSnapshot,
        surface_data: Optional[VolSurfaceData] = None,
        surface_prev: Optional[VolSurfaceData] = None,
    ) -> PricingResult: ...


class YFinanceMarketLoader:
    def load(
        self,
        *,
        ticker: str,
        option_type: str,
        strike: Optional[float],
        expiry: Optional[str],
    ) -> LoadedData:
        from ..data_loader import load_market_data

        return load_market_data(ticker=ticker, option_type=option_type, strike=strike, expiry=expiry)


class FixtureMarketLoader:
    """Synthetic snapshot from a committed fixture. No network."""

    def __init__(self, name: str) -> None:
        self.name = name

    def load(
        self,
        *,
        ticker: str,
        option_type: str,
        strike: Optional[float],
        expiry: Optional[str],
    ) -> LoadedData:
        from ..data.synthetic import load_fixture

        snap, surf = load_fixture(self.name)
        snap.ticker = ticker
        snap.option_type = option_type
        if strike is not None:
            snap.strike = float(strike)
        if expiry is not None:
            snap.expiry = expiry
        return LoadedData(snapshot=snap, surface=surf, surface_prev=None)


def fixture_deps(name: str) -> GraphDeps:
    """Offline product path: synthetic market, frozen (empty) news."""
    return GraphDeps(
        market=FixtureMarketLoader(name),
        intel=IntelRegistry(
            {
                "yfinance_news": StubIntelSource("yfinance_news"),
                "tavily": StubIntelSource("tavily"),
                "sec_8k": StubIntelSource("sec_8k"),
            }
        ),
    )


@dataclass
class OfficialFdmPnlSource:
    """The reference engine: QuantLib American FDM. ``config`` overrides grid sizes."""

    config: Optional[EngineConfig] = None
    methodology: str = QUANTLIB_METHODOLOGY

    def attribute(
        self,
        snapshot: MarketSnapshot,
        surface_data: Optional[VolSurfaceData] = None,
        surface_prev: Optional[VolSurfaceData] = None,
    ) -> PricingResult:
        from ..pricing.facade import price_and_attribute

        return price_and_attribute(
            snapshot=snapshot,
            surface_data=surface_data,
            surface_prev=surface_prev,
            config=self.config,
        )

    def second_order(self, snapshot: MarketSnapshot, pricing: PricingResult) -> SecondOrderTaylorResult:
        from ..pricing.analysis_api import taylor_second_order

        return taylor_second_order(snapshot, pricing, config=self.config)

    def path_reprice(
        self, snapshot: MarketSnapshot, pricing: PricingResult, surface: Optional[VolSurfaceData] = None
    ) -> SequentialRevalResult:
        from ..pricing.analysis_api import path_reprice

        return path_reprice(snapshot, pricing, config=self.config, surface=surface)


@dataclass
class GraphDeps:
    """Defaults are live yfinance + official FDM + cue planner + yahoo/Tavily/8-K registry."""

    market: MarketLoader = field(default_factory=YFinanceMarketLoader)
    pnl: PnlSource = field(default_factory=OfficialFdmPnlSource)
    planner: QueryPlanner = field(default_factory=default_planner)
    intel: IntelRegistry = field(default_factory=default_registry)
    # None means STRUCTURED_DIAGNOSE_SYSTEM_PROMPT. The extra is an optional
    # author-local addendum for evals.
    diagnose_system_prompt: Optional[str] = None
    diagnose_system_extra: str = ""
    # Narrator guidance for special cases, selected by code from the diagnostic
    # findings. A desk may append its own records; see graph/playbook.py.
    playbook: tuple[PlaybookRecord, ...] = DEFAULT_PLAYBOOK

    def __post_init__(self) -> None:
        self.playbook = tuple(self.playbook)
        check_playbook(self.playbook)


def default_deps() -> GraphDeps:
    return GraphDeps(diagnose_system_extra=extra_from_env())
