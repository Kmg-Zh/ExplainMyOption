"""Graph ports (swap market / PnL / intel without rewriting nodes)."""

from .deps import (
    FixtureMarketLoader,
    GraphDeps,
    MarketLoader,
    OfficialFdmPnlSource,
    PnlSource,
    YFinanceMarketLoader,
    default_deps,
    fixture_deps,
)
from .prompts import (
    DEFAULT_DIAGNOSE_SYSTEM_PROMPT,
    STRUCTURED_DIAGNOSE_SYSTEM_PROMPT,
    compose_diagnose_system_prompt,
    extra_from_env,
)
from .topology import book_mermaid, leg_mermaid, pipeline_mermaid

__all__ = [
    "DEFAULT_DIAGNOSE_SYSTEM_PROMPT",
    "STRUCTURED_DIAGNOSE_SYSTEM_PROMPT",
    "FixtureMarketLoader",
    "GraphDeps",
    "MarketLoader",
    "OfficialFdmPnlSource",
    "PnlSource",
    "YFinanceMarketLoader",
    "book_mermaid",
    "compose_diagnose_system_prompt",
    "default_deps",
    "extra_from_env",
    "fixture_deps",
    "leg_mermaid",
    "pipeline_mermaid",
]
