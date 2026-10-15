"""Offline building blocks for the tests: scripted LLM roles, frozen markets and news."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from explain_my_option.data.historical_chain import load_historical_case
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.data_loader import LoadedData, NewsItem
from explain_my_option.graph.deps import GraphDeps, OfficialFdmPnlSource
from explain_my_option.intel.sources import IntelRegistry, StubIntelSource
from explain_my_option.pipeline.book_schema import BookLegSpec
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.leg_graph import build_leg_diagnosis_subgraph
from explain_my_option.pipeline.llm_roles import LlmRoleRegistry
from explain_my_option.pricing.config import EngineConfig
from explain_my_option.report.schema import DiagnosticSynthesis

FAST = EngineConfig.fast()

QUIET_DAYS = ("quiet_aapl_2023-04-24", "quiet_spy_2023-03-06", "quiet_spy_2023-04-24")


@dataclass
class ScriptedNarrator:
    verdict: str = "Vega led the move while the spot move partly offset it."
    takeaways: tuple[str, ...] = ("Watch implied volatility around the next scheduled event.",)
    calls: int = 0

    def structured_invoke(self, *, system: str, human: str, schema):
        self.calls += 1
        return schema(
            primary_driver="Vega / implied volatility",
            verdict=self.verdict,
            confidence_level="medium",
            confidence_rationale="Scripted narrator.",
            takeaways=list(self.takeaways),
        )


@dataclass
class ScriptedVerifier:
    verdict: str = "PASS"
    flags: tuple[str, ...] = ()
    calls: int = 0

    def structured_invoke(self, *, system: str, human: str, schema):
        self.calls += 1
        return schema(verdict=self.verdict, policy_flags=list(self.flags), rationale="Scripted verifier.")


@dataclass
class ScriptedRole:
    """Returns one fixed payload for any schema (digester or catalyst critic)."""

    payload: dict[str, Any]
    seen: list[str] = field(default_factory=list)

    def structured_invoke(self, *, system: str, human: str, schema):
        self.seen.append(human)
        return schema.model_validate(self.payload)


class NoLlm:
    """A role whose use fails the test: the pipeline must not reach an LLM."""

    def structured_invoke(self, *, system: str, human: str, schema):
        raise AssertionError(f"unexpected LLM call ({schema.__name__})")


def no_llm_roles() -> LlmRoleRegistry:
    return LlmRoleRegistry(narrator=NoLlm(), verifier=NoLlm(), challenger=NoLlm(), digester=NoLlm())


def roles(narrator=None, verifier=None, *, digester=None, challenger=None) -> LlmRoleRegistry:
    return LlmRoleRegistry(
        narrator=narrator or ScriptedNarrator(),
        verifier=verifier or ScriptedVerifier(),
        digester=digester,
        challenger=challenger,
    )


class _FrozenNews:
    def __init__(self, source_id: str, news: list[NewsItem]) -> None:
        self.source_id = source_id
        self._news = news

    def search(self, query, *, ticker: str) -> list[NewsItem]:
        return list(self._news)


def frozen_intel(news: list[NewsItem] | tuple = ()) -> IntelRegistry:
    """Yahoo returns ``news``; Tavily and SEC return nothing. No network."""
    return IntelRegistry(
        {
            "yfinance_news": _FrozenNews("yfinance_news", list(news)),
            "tavily": StubIntelSource("tavily"),
            "sec_8k": StubIntelSource("sec_8k"),
        }
    )


@dataclass
class CaseLoader:
    """MarketLoader for a committed real-chain slice."""

    name: str

    def load(self, *, ticker, option_type, strike, expiry) -> LoadedData:
        return LoadedData(snapshot=load_historical_case(self.name))


def invoke_leg(leg: BookLegSpec, *, market=None, pnl=None, news=(), llm: LlmRoleRegistry | None = None, verify: bool = True) -> dict:
    """Run one leg through the real subgraph with offline ports."""
    deps = GraphDeps(market=market, pnl=pnl or OfficialFdmPnlSource(config=FAST), intel=frozen_intel(news))
    app = build_leg_diagnosis_subgraph(config=PipelineConfig(verify=verify), deps=deps, roles=llm or roles())
    return app.invoke({"leg": leg, "ticker": leg.ticker, "strike": leg.strike, "expiry": leg.expiry})


def run_leg(*, fixture: str | None = None, case: str | None = None, news=(), llm: LlmRoleRegistry | None = None, verify: bool = True) -> dict:
    """Run a committed synthetic fixture or real-chain case as one leg."""
    market = None
    if case is not None:
        snap, market = load_historical_case(case), CaseLoader(case)
    else:
        snap, _ = load_fixture(fixture)
    # The leg spec overrides the snapshot's contract fields, so copy them over.
    leg = BookLegSpec(
        leg_id=case or fixture,
        fixture=fixture,
        ticker=snap.ticker,
        option_type=snap.option_type,
        strike=snap.strike,
        expiry=snap.expiry,
        quantity=snap.quantity,
        multiplier=snap.multiplier,
    )
    return invoke_leg(leg, market=market, news=news, llm=llm, verify=verify)


def synthesis(**overrides) -> DiagnosticSynthesis:
    base = dict(
        primary_driver="Delta / spot move",
        verdict="The spot move dominated the session.",
        confidence_level="medium",
        confidence_rationale="Clean attribution.",
        takeaways=["Watch the ex-dividend boundary."],
    )
    return DiagnosticSynthesis(**{**base, **overrides})
