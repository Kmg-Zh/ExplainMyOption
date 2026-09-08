"""Intel registry + Tavily / SEC 8-K ports (no network)."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

import os

from bootstrap import install

install()

from explain_my_option.intel.sec_edgar import SecEdgar8KSource, reset_ticker_cache
from explain_my_option.intel.sources import IntelRegistry, TavilyNewsSource
from explain_my_option.intel.types import SearchPlan, SearchQuery


def test_intel_skips_unregistered_source():
    registry = IntelRegistry(sources={})
    plan = SearchPlan(queries=[SearchQuery(q="AAPL", source_id="yfinance_news")])
    hits, skipped, failed = registry.execute(plan, ticker="AAPL")
    assert hits == []
    assert skipped == ["yfinance_news"]
    assert failed == []


class _BoomNews:
    source_id = "yfinance_news"

    def search(self, query, *, ticker: str):
        raise RuntimeError("yahoo down")


def test_intel_source_exception_fail_soft():
    registry = IntelRegistry(sources={"yfinance_news": _BoomNews()})
    plan = SearchPlan(queries=[SearchQuery(q="AAPL", source_id="yfinance_news")])
    hits, skipped, failed = registry.execute(plan, ticker="AAPL")
    assert hits == []
    assert skipped == []
    assert failed == ["yfinance_news"]


class _FakeTavily:
    def search(self, **kwargs):
        assert kwargs["query"] == "AAPL implied volatility earnings"
        assert kwargs["topic"] == "news"
        return {
            "results": [
                {
                    "title": "AAPL IV into earnings",
                    "url": "https://example.com/iv",
                    "source": "Reuters",
                    "published_date": "2026-08-18",
                }
            ]
        }


def test_tavily_skips_when_key_missing():
    old = os.environ.pop("TAVILY_API_KEY", None)
    try:
        registry = IntelRegistry(sources={"tavily": TavilyNewsSource(api_key="")})
        plan = SearchPlan(
            queries=[SearchQuery(q="AAPL IV", source_id="tavily", cue="vega")]
        )
        hits, skipped, failed = registry.execute(plan, ticker="AAPL")
    finally:
        if old is not None:
            os.environ["TAVILY_API_KEY"] = old
    assert hits == []
    assert skipped == ["tavily"]
    assert failed == []
    notes = " ".join(plan.model_copy(update={"skipped_sources": skipped}).honesty_notes())
    assert "not configured" in notes


def _fake_sec_fetch(url: str, headers: dict[str, str]):
    assert headers.get("User-Agent")
    if "company_tickers.json" in url:
        return {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}}
    if "submissions" in url:
        return {
            "filings": {
                "recent": {
                    "form": ["10-Q", "8-K", "8-K/A"],
                    "filingDate": ["2026-08-01", "2026-08-15", "2026-08-10"],
                    "accessionNumber": [
                        "0000320193-26-000001",
                        "0000320193-26-000050",
                        "0000320193-26-000040",
                    ],
                    "primaryDocDescription": [
                        "Quarterly report",
                        "Results of operations",
                        "Amended current report",
                    ],
                    "primaryDocument": [
                        "aapl-20260801.htm",
                        "aapl-20260815.htm",
                        "aapl-20260810.htm",
                    ],
                }
            }
        }
    raise AssertionError(f"unexpected url {url}")


def test_sec_8k_skips_without_user_agent():
    old = os.environ.pop("EMO_SEC_USER_AGENT", None)
    reset_ticker_cache()
    try:
        registry = IntelRegistry(sources={"sec_8k": SecEdgar8KSource(user_agent="")})
        plan = SearchPlan(
            queries=[SearchQuery(q="AAPL 8-K", source_id="sec_8k", cue="residual")]
        )
        hits, skipped, failed = registry.execute(plan, ticker="AAPL")
    finally:
        reset_ticker_cache()
        if old is not None:
            os.environ["EMO_SEC_USER_AGENT"] = old
    assert hits == []
    assert skipped == ["sec_8k"]
    assert failed == []


def test_sec_8k_uses_injected_fetch():
    reset_ticker_cache()
    src = SecEdgar8KSource(
        user_agent="ExplainMyOption test@example.com",
        fetch_json=_fake_sec_fetch,
    )
    registry = IntelRegistry(sources={"sec_8k": src})
    plan = SearchPlan(
        queries=[
            SearchQuery(q="AAPL 8-K", source_id="sec_8k", cue="residual", limit=2)
        ]
    )
    hits, skipped, failed = registry.execute(plan, ticker="AAPL")
    reset_ticker_cache()
    assert skipped == []
    assert failed == []
    assert len(hits) == 2
    assert hits[0].publisher == "SEC EDGAR"
    assert hits[0].title == "Results of operations"
    assert "sec.gov/Archives/edgar/data" in hits[0].link
    notes = " ".join(plan.honesty_notes())
    assert "SEC EDGAR" in notes
    assert "not wired" not in notes


def test_tavily_uses_injected_client():
    src = TavilyNewsSource(api_key="tvly-test-not-real", client=_FakeTavily())
    registry = IntelRegistry(sources={"tavily": src})
    plan = SearchPlan(
        queries=[
            SearchQuery(
                q="AAPL implied volatility earnings",
                source_id="tavily",
                cue="vega",
            )
        ]
    )
    hits, skipped, failed = registry.execute(plan, ticker="AAPL")
    assert skipped == []
    assert failed == []
    assert hits[0].title == "AAPL IV into earnings"
    assert hits[0].link.endswith("/iv")


if __name__ == "__main__":
    test_intel_skips_unregistered_source()
    test_intel_source_exception_fail_soft()
    test_tavily_skips_when_key_missing()
    test_tavily_uses_injected_client()
    test_sec_8k_skips_without_user_agent()
    test_sec_8k_uses_injected_fetch()
    print("OK — intel checks passed")
