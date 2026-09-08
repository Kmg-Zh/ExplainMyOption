"""Schemas for targeted search (query plan + hits). Swap sources without changing the graph."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

# Allow-listed source ids. Register a new IntelSource to honor a new id.
IntelSourceId = Literal["yfinance_news", "tavily", "sec_8k"]
SearchCue = Literal[
    "material",
    "vega",
    "gamma",
    "residual",
    "residual_ex_div",
    "microstructure",
]
SearchSkipReason = Literal["", "below_materiality", "observation_lock"]


class IntelUnconfigured(Exception):
    """Registered source cannot run (missing API key, User-Agent, etc.)."""

    def __init__(self, source_id: str) -> None:
        self.source_id = source_id
        super().__init__(source_id)


class SearchQuery(BaseModel):
    """One bounded lookup. ``source_id`` selects the IntelSource implementation."""

    q: str
    source_id: IntelSourceId = "yfinance_news"
    cue: SearchCue = "material"
    limit: int = Field(default=3, ge=1, le=10)


class SearchPlan(BaseModel):
    """Bounded query list produced by ``plan_search``. Never unbounded crawl."""

    queries: list[SearchQuery] = Field(default_factory=list)
    max_queries: int = Field(default=3, ge=1, le=8)
    skipped_sources: list[str] = Field(default_factory=list)
    failed_sources: list[str] = Field(default_factory=list)
    skip_reason: SearchSkipReason = ""

    def honesty_notes(self) -> list[str]:
        """Captions for the report: what the plan asked vs what the backends can do."""
        notes: list[str] = []
        if self.skip_reason:
            notes.append(
                "No catalyst search — move below materiality / observation lock."
            )
            return notes
        if any(q.source_id == "yfinance_news" for q in self.queries):
            notes.append(
                "Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied."
            )
        if any(q.source_id == "sec_8k" for q in self.queries):
            notes.append(
                "SEC EDGAR lists recent Form 8-K filings (official API; set "
                "`EMO_SEC_USER_AGENT` locally — free, no API key)."
            )
        if self.failed_sources:
            notes.append(
                "News fetch failed and was skipped: "
                + ", ".join(dict.fromkeys(self.failed_sources))
                + "."
            )
        if self.skipped_sources:
            notes.append(
                "Skipped (unregistered or not configured): "
                + ", ".join(dict.fromkeys(self.skipped_sources))
                + "."
            )
        return notes
