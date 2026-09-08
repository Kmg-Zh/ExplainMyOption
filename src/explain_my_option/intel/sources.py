"""Intel sources: execute a SearchQuery. Register new backends without touching nodes."""

from __future__ import annotations

import os
from typing import Any, Optional, Protocol

from explain_my_option.data_loader import NewsItem, fetch_news

from .types import IntelSourceId, IntelUnconfigured, SearchPlan, SearchQuery
from .sec_edgar import SecEdgar8KSource


class IntelSource(Protocol):
    """One news / filings backend. ``source_id`` must match SearchQuery.source_id."""

    source_id: IntelSourceId

    def search(self, query: SearchQuery, *, ticker: str) -> list[NewsItem]: ...


class YFinanceNewsSource:
    """Yahoo ``Ticker.news`` titles. Query text is ignored."""

    source_id: IntelSourceId = "yfinance_news"

    def search(self, query: SearchQuery, *, ticker: str) -> list[NewsItem]:
        return fetch_news(ticker, limit=query.limit)


class TavilyNewsSource:
    """Tavily Search ``topic=news``. Uses ``query.q``. No key → ``IntelUnconfigured``."""

    source_id: IntelSourceId = "tavily"

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        client: Any = None,
    ) -> None:
        self._api_key = api_key
        self._client = client

    def _key(self) -> str:
        if self._api_key is not None:
            return self._api_key.strip()
        return (os.getenv("TAVILY_API_KEY") or "").strip()

    def search(self, query: SearchQuery, *, ticker: str) -> list[NewsItem]:
        del ticker  # query.q already includes the ticker from the planner
        key = self._key()
        if not key:
            raise IntelUnconfigured("tavily")
        client = self._client
        if client is None:
            from tavily import TavilyClient

            client = TavilyClient(api_key=key)
        resp = client.search(
            query=query.q,
            max_results=query.limit,
            topic="news",
            time_range="week",
        )
        raw = resp.get("results") if isinstance(resp, dict) else None
        items: list[NewsItem] = []
        for row in raw or []:
            if not isinstance(row, dict):
                continue
            title = (row.get("title") or "").strip()
            if not title:
                continue
            items.append(
                NewsItem(
                    title=title,
                    publisher=str(row.get("source") or ""),
                    link=str(row.get("url") or ""),
                    published=str(row.get("published_date") or ""),
                )
            )
        return items


class StubIntelSource:
    """Placeholder (8-K). Returns nothing until wired."""

    def __init__(self, source_id: IntelSourceId) -> None:
        self.source_id = source_id

    def search(self, query: SearchQuery, *, ticker: str) -> list[NewsItem]:
        return []


class IntelRegistry:
    """Dispatch SearchPlan queries by ``source_id``. Unknown / unconfigured ids are skipped."""

    def __init__(self, sources: dict[str, IntelSource] | None = None) -> None:
        self._sources: dict[str, IntelSource] = dict(
            default_sources() if sources is None else sources
        )

    def register(self, source: IntelSource) -> None:
        self._sources[source.source_id] = source

    def execute(self, plan: SearchPlan, *, ticker: str) -> tuple[list[NewsItem], list[str], list[str]]:
        hits: list[NewsItem] = []
        skipped: list[str] = []
        failed: list[str] = []
        seen_titles: set[str] = set()
        for query in plan.queries[: plan.max_queries]:
            src = self._sources.get(query.source_id)
            if src is None:
                skipped.append(query.source_id)
                continue
            try:
                batch = src.search(query, ticker=ticker)
            except IntelUnconfigured:
                skipped.append(query.source_id)
                continue
            except Exception:
                failed.append(query.source_id)
                continue
            for item in batch:
                key = item.title.strip().lower()
                if not key or key in seen_titles:
                    continue
                seen_titles.add(key)
                hits.append(item)
        return hits, skipped, failed


def default_sources() -> dict[str, IntelSource]:
    return {
        "yfinance_news": YFinanceNewsSource(),
        "tavily": TavilyNewsSource(),
        "sec_8k": SecEdgar8KSource(),
    }


def default_registry() -> IntelRegistry:
    return IntelRegistry()
