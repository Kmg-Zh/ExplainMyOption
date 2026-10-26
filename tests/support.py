"""Offline building blocks for the tests: frozen markets, one-leg runners, synthesis stubs.

The scripted LLM roles live in ``explain_my_option.testing`` and are re-exported here.
"""

from __future__ import annotations

from dataclasses import dataclass

from explain_my_option.data.historical_chain import load_historical_case
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.data_loader import LoadedData
from explain_my_option.graph.deps import GraphDeps, OfficialFdmPnlSource
from explain_my_option.pipeline.book_schema import BookLegSpec
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.leg_graph import build_leg_diagnosis_subgraph
from explain_my_option.pipeline.llm_roles import LlmRoleRegistry
from explain_my_option.pricing.config import EngineConfig
from explain_my_option.report.schema import DiagnosticSynthesis

# The scripted LLM roles ship with the package; the tests use them under these names.
from explain_my_option.testing import (  # noqa: F401
    NoLlm,
    ScriptedNarrator,
    ScriptedRole,
    ScriptedVerifier,
    frozen_intel,
    no_llm_roles,
)
from explain_my_option.testing import scripted_roles as roles  # noqa: F401

FAST = EngineConfig.fast()

QUIET_DAYS = ("quiet_aapl_2023-04-24", "quiet_spy_2023-03-06", "quiet_spy_2023-04-24")

LEG = BookLegSpec(leg_id="t", ticker="TEST", strike=100.0, expiry="2026-12-18")


class NeverPrice:
    """A PnL source whose use fails the test: the leg must stop before pricing."""

    def attribute(self, snapshot, surface_data=None, surface_prev=None):
        raise AssertionError("the leg must stop before pricing")


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
