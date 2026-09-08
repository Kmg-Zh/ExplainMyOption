"""Injectable ports for the product graph — swap market, PnL, planner, intel."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Protocol

from explain_my_option.data.synthetic import load_fixture
from explain_my_option.data_loader import LoadedData, load_market_data
from explain_my_option.graph.prompts import extra_from_env
from explain_my_option.intel.planner import QueryPlanner, default_planner
from explain_my_option.intel.sources import IntelRegistry, StubIntelSource, default_registry
from explain_my_option.pricing import price_and_attribute
from explain_my_option.pricing.config import EngineConfig
from explain_my_option.pricing.types import MarketSnapshot, PricingResult, VolSurfaceData


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
    """Official 1-day PnL. Default wraps ``price_and_attribute`` (FDM)."""

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
        return load_market_data(
            ticker=ticker,
            option_type=option_type,
            strike=strike,
            expiry=expiry,
        )


class FixtureMarketLoader:
    """Synthetic snapshot from ``tests/ci/fixtures/{name}.json``. No network."""

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
    """Official American FDM PnL. Pass ``config`` in tests via ``tests.shared.engine_config``."""

    config: Optional[EngineConfig] = None

    def attribute(
        self,
        snapshot: MarketSnapshot,
        surface_data: Optional[VolSurfaceData] = None,
        surface_prev: Optional[VolSurfaceData] = None,
    ) -> PricingResult:
        return price_and_attribute(
            snapshot=snapshot,
            surface_data=surface_data,
            surface_prev=surface_prev,
            config=self.config,
        )


@dataclass
class GraphDeps:
    """Defaults are live yfinance + official FDM + cue planner + yahoo/Tavily/8-K registry."""

    market: MarketLoader = field(default_factory=YFinanceMarketLoader)
    pnl: PnlSource = field(default_factory=OfficialFdmPnlSource)
    planner: QueryPlanner = field(default_factory=default_planner)
    intel: IntelRegistry = field(default_factory=default_registry)
    # None → STRUCTURED_DIAGNOSE_SYSTEM_PROMPT in src/graph/prompts.py. Extra is author-local eval only.
    diagnose_system_prompt: Optional[str] = None
    diagnose_system_extra: str = ""


def default_deps() -> GraphDeps:
    return GraphDeps(diagnose_system_extra=extra_from_env())
