"""SEC EDGAR 8-K filings via the official data.sec.gov API (free, no API key).

SEC requires a descriptive ``User-Agent`` on every request — set ``EMO_SEC_USER_AGENT``
locally (e.g. ``"ExplainMyOption you@example.com"``). See docs/references/sec-edgar.md.
"""

from __future__ import annotations

import json
import os
import re
from typing import Any, Callable, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from explain_my_option.data_loader import NewsItem

from .types import IntelUnconfigured, SearchQuery

_TICKER_MAP_URL = "https://www.sec.gov/files/company_tickers.json"
_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
_8K_FORMS = frozenset({"8-K", "8-K/A"})
_TICKER_MAP: dict[str, str] | None = None

FetchJson = Callable[[str, dict[str, str]], Any]


def _default_fetch_json(url: str, headers: dict[str, str]) -> Any:
    req = Request(url, headers=headers)
    with urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _normalize_ticker(ticker: str) -> str:
    sym = ticker.strip().upper()
    # Class shares like BRK.B → EDGAR tickers file uses BRK-B in some cases; try as-is first.
    return re.sub(r"\s+", "", sym)


def _ticker_to_cik(
    ticker: str,
    *,
    fetch_json: FetchJson,
    headers: dict[str, str],
) -> Optional[str]:
    global _TICKER_MAP
    sym = _normalize_ticker(ticker)
    if not sym:
        return None
    if _TICKER_MAP is None:
        raw = fetch_json(_TICKER_MAP_URL, headers)
        mapping: dict[str, str] = {}
        if isinstance(raw, dict):
            for row in raw.values():
                if not isinstance(row, dict):
                    continue
                t = str(row.get("ticker") or "").strip().upper()
                cik = row.get("cik_str")
                if t and cik is not None:
                    mapping[t] = str(int(cik)).zfill(10)
        _TICKER_MAP = mapping
    cik = _TICKER_MAP.get(sym)
    if cik is None and "." in sym:
        cik = _TICKER_MAP.get(sym.replace(".", "-"))
    return cik


def _filing_url(cik: str, accession: str, primary_doc: str) -> str:
    cik_path = str(int(cik))
    acc_path = accession.replace("-", "")
    return f"https://www.sec.gov/Archives/edgar/data/{cik_path}/{acc_path}/{primary_doc}"


def _index_url(cik: str, accession: str) -> str:
    cik_path = str(int(cik))
    acc_path = accession.replace("-", "")
    return f"https://www.sec.gov/Archives/edgar/data/{cik_path}/{acc_path}/"


def fetch_recent_8k(
    ticker: str,
    *,
    limit: int = 3,
    user_agent: str,
    fetch_json: FetchJson | None = None,
) -> list[NewsItem]:
    """Return recent Form 8-K / 8-K/A filings for ``ticker`` (newest first)."""
    ua = user_agent.strip()
    if not ua:
        return []
    loader = fetch_json or _default_fetch_json
    headers = {
        "User-Agent": ua,
        "Accept": "application/json",
    }
    cik = _ticker_to_cik(ticker, fetch_json=loader, headers=headers)
    if not cik:
        return []
    try:
        payload = loader(_SUBMISSIONS_URL.format(cik=cik), headers)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError):
        return []
    filings = payload.get("filings") if isinstance(payload, dict) else None
    recent = filings.get("recent") if isinstance(filings, dict) else None
    if not isinstance(recent, dict):
        return []
    forms = recent.get("form") or []
    dates = recent.get("filingDate") or []
    accessions = recent.get("accessionNumber") or []
    descriptions = recent.get("primaryDocDescription") or []
    primary_docs = recent.get("primaryDocument") or []
    n = min(len(forms), len(dates), len(accessions))
    items: list[NewsItem] = []
    for i in range(n):
        form = str(forms[i] or "").strip().upper()
        if form not in _8K_FORMS:
            continue
        acc = str(accessions[i] or "").strip()
        filed = str(dates[i] or "").strip()
        desc = ""
        if i < len(descriptions) and descriptions[i]:
            desc = str(descriptions[i]).strip()
        primary = ""
        if i < len(primary_docs) and primary_docs[i]:
            primary = str(primary_docs[i]).strip()
        title = desc or f"{_normalize_ticker(ticker)} {form} filed {filed}"
        link = _filing_url(cik, acc, primary) if primary else _index_url(cik, acc)
        items.append(
            NewsItem(
                title=title,
                publisher="SEC EDGAR",
                link=link,
                published=filed,
            )
        )
        if len(items) >= limit:
            break
    return items


class SecEdgar8KSource:
    """Recent Form 8-K filings from SEC EDGAR. Residual cue in ``CueQueryPlanner``."""

    source_id = "sec_8k"

    def __init__(
        self,
        *,
        user_agent: Optional[str] = None,
        fetch_json: FetchJson | None = None,
    ) -> None:
        self._user_agent = user_agent
        self._fetch_json = fetch_json

    def _ua(self) -> str:
        if self._user_agent is not None:
            return self._user_agent.strip()
        return (os.getenv("EMO_SEC_USER_AGENT") or "").strip()

    def search(self, query: SearchQuery, *, ticker: str) -> list[NewsItem]:
        ua = self._ua()
        if not ua:
            raise IntelUnconfigured("sec_8k")
        return fetch_recent_8k(
            ticker,
            limit=query.limit,
            user_agent=ua,
            fetch_json=self._fetch_json,
        )


def reset_ticker_cache() -> None:
    """Test helper — clear in-memory ticker→CIK map."""
    global _TICKER_MAP
    _TICKER_MAP = None
