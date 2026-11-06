"""Offline building blocks for the tests: frozen markets, one-leg runners, synthesis stubs.

The scripted LLM roles live in ``explain_my_option.testing`` and are re-exported here.
"""

from __future__ import annotations

from dataclasses import dataclass

from explain_my_option.data.historical_chain import load_historical_case
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.data_loader import LoadedData
from explain_my_option.graph.deps import GraphDeps, OfficialFdmPnlSource
from explain_my_option.graph.playbook import DEFAULT_PLAYBOOK
from explain_my_option.pipeline.book_schema import BookLegSpec
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.leg_graph import build_leg_diagnosis_subgraph
from explain_my_option.pipeline.llm_roles import LlmRoleRegistry
from explain_my_option.pricing.config import EngineConfig
from explain_my_option.pricing.types import DiscreteDividend, MarketSnapshot
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


def aapl_nov20_call(strike: float, *, stale_spot: bool) -> MarketSnapshot:
    """One leg of the 2026-11-04 live run's AAPL vertical, with its real quotes.

    At 21:15 ET Yahoo's 11-04 daily bar had no close yet, so that run paired the
    11-04 and 11-03 marks with the 11-03 and 11-02 closes (``stale_spot``). The
    session closes were 349.51 and 331.90.
    """
    quotes = {325.0: (25.35, 26.40, 0.3383, 11.95, 0.2953), 350.0: (6.75, 7.10, 0.2514, 1.50, 0.2489)}
    bid, ask, iv_now, mark_prev, iv_prev = quotes[strike]
    spot_now, spot_prev = (331.90, 338.32) if stale_spot else (349.51, 331.90)
    return MarketSnapshot(
        ticker="AAPL", option_type="call", strike=strike, expiry="2026-11-20",
        spot_now=spot_now, spot_prev=spot_prev, iv_now=iv_now, iv_prev=iv_prev,
        option_price_now=0.5 * (bid + ask), option_price_prev=mark_prev, time_to_expiry_years=16 / 365,
        risk_free_rate=0.04025, discrete_dividends=[DiscreteDividend(ex_date="2026-11-12", amount=0.27)],
        data_source="yfinance", as_of="2026-11-04", prev_as_of="2026-11-03", iv_prev_source="chain_t1",
        bid=bid, ask=ask, mid=0.5 * (bid + ask), volume=500.0, open_interest=10000.0,
    )


def jpm_oct23_straddle(option_type: str) -> MarketSnapshot:
    """One leg of the run log's JPM 350 straddle at its 2026-10-23 expiry.

    The prior marks are the real 10-22 cached mids (spot 336.54) and the
    expiry close was 331.58. The runs from 10-23 on failed on the delisted
    contract instead of settling it.
    """
    mark_prev, iv_prev = {"call": (0.02, 0.3399), "put": (14.10, 0.6274)}[option_type]
    return MarketSnapshot(
        ticker="JPM", option_type=option_type, strike=350.0, expiry="2026-10-23",
        spot_now=331.58, spot_prev=336.54, iv_now=iv_prev, iv_prev=iv_prev,
        option_price_now=max(350.0 - 331.58, 0.0) if option_type == "put" else 0.0, option_price_prev=mark_prev,
        time_to_expiry_years=0.0, risk_free_rate=0.04022, data_source="yfinance",
        as_of="2026-10-23", prev_as_of="2026-10-22", iv_prev_source="chain_t1", multiplier=100.0,
    )


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


def invoke_leg(leg: BookLegSpec, *, market=None, pnl=None, news=(), llm: LlmRoleRegistry | None = None, verify: bool = True, playbook=DEFAULT_PLAYBOOK) -> dict:
    """Run one leg through the real subgraph with offline ports."""
    deps = GraphDeps(market=market, pnl=pnl or OfficialFdmPnlSource(config=FAST), intel=frozen_intel(news), playbook=playbook)
    app = build_leg_diagnosis_subgraph(config=PipelineConfig(verify=verify), deps=deps, roles=llm or roles())
    return app.invoke({"leg": leg, "ticker": leg.ticker, "strike": leg.strike, "expiry": leg.expiry})


def run_leg(*, fixture: str | None = None, case: str | None = None, news=(), llm: LlmRoleRegistry | None = None, verify: bool = True, playbook=DEFAULT_PLAYBOOK) -> dict:
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
    return invoke_leg(leg, market=market, news=news, llm=llm, verify=verify, playbook=playbook)


def synthesis(**overrides) -> DiagnosticSynthesis:
    base = dict(
        primary_driver="Delta / spot move",
        verdict="The spot move dominated the session.",
        confidence_level="medium",
        confidence_rationale="Clean attribution.",
        takeaways=["Watch the ex-dividend boundary."],
    )
    return DiagnosticSynthesis(**{**base, **overrides})
