"""Scripted LLM roles: run the governed agent with no model and no key.

Each role answers ``structured_invoke`` with a fixed reply, so you can make an
LLM misbehave on purpose and check what code lets through to the report. The
repo's tests use them (``tests/agent/``), and so do the runnable examples in
``examples/governance/``. A desk wiring in its own PnL system can use them to
test its adapters before paying for a model.

Every role records the prompts it was sent in ``seen``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .intel.sources import IntelRegistry, StubIntelSource
from .intel.types import NewsItem
from .pipeline.llm_roles import LlmRoleRegistry


@dataclass
class ScriptedNarrator:
    """Returns ``verdict`` and ``takeaways`` as its synthesis, whatever it is asked."""

    verdict: str = "Vega led the move while the spot move partly offset it."
    takeaways: tuple[str, ...] = ("Watch implied volatility around the next scheduled event.",)
    calls: int = 0
    seen: list[str] = field(default_factory=list)

    def structured_invoke(self, *, system: str, human: str, schema):
        self.calls += 1
        self.seen.append(human)
        return schema(
            primary_driver="Vega / implied volatility",
            verdict=self.verdict,
            confidence_level="medium",
            confidence_rationale="Scripted narrator.",
            takeaways=list(self.takeaways),
        )


@dataclass
class ScriptedVerifier:
    """Returns ``verdict`` (PASS, PARTIAL or FAIL) with ``flags``, whatever the narrative says."""

    verdict: str = "PASS"
    flags: tuple[str, ...] = ()
    calls: int = 0
    seen: list[str] = field(default_factory=list)

    def structured_invoke(self, *, system: str, human: str, schema):
        self.calls += 1
        self.seen.append(human)
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
    """A role that raises if it is called: the run must not reach an LLM."""

    def structured_invoke(self, *, system: str, human: str, schema):
        raise AssertionError(f"unexpected LLM call ({schema.__name__})")


def no_llm_roles() -> LlmRoleRegistry:
    """All four roles raise if called."""
    return LlmRoleRegistry(narrator=NoLlm(), verifier=NoLlm(), challenger=NoLlm(), digester=NoLlm())


def scripted_roles(narrator=None, verifier=None, *, digester=None, challenger=None) -> LlmRoleRegistry:
    """A narrator and verifier that pass by default; no digester or critic unless given."""
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


def frozen_intel(news: Iterable[NewsItem] = ()) -> IntelRegistry:
    """Yahoo returns ``news``; Tavily and SEC return nothing. No network."""
    return IntelRegistry(
        {
            "yfinance_news": _FrozenNews("yfinance_news", list(news)),
            "tavily": StubIntelSource("tavily"),
            "sec_8k": StubIntelSource("sec_8k"),
        }
    )
