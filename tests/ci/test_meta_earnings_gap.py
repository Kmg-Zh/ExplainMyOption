"""META 2022-02 earnings gap — extreme ΔS + synthetic IV crush (offline).

Spot closes are historical (320.19 → 237.76). IV is synthetic (no free chain).
News is frozen stub hits (stand-in for live intel), same as_of as the snapshot.
"""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import os

from bootstrap import install

install()

from explain_my_option.agent_graph import run_pipeline
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.data_loader import NewsItem
from explain_my_option.graph.deps import FixtureMarketLoader, GraphDeps, OfficialFdmPnlSource
from explain_my_option.intel.planner import CueQueryPlanner
from explain_my_option.intel.sources import IntelRegistry, StubIntelSource
from explain_my_option.intel.types import SearchQuery
from explain_my_option.pricing import price_and_attribute
from ci.engine_config import engine_config_for_tests
from explain_my_option.report.facts import build_position_facts
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.llm_roles import LlmRoleRegistry
from explain_my_option.pipeline.verifier_schema import DiagnosticVerifierResult

CFG = engine_config_for_tests()
FIXTURE = "meta_earnings_gap"

# Frozen intel — same as_of story as the snapshot (not live Yahoo).
_META_NEWS: list[NewsItem] = [
    NewsItem(
        title=(
            "Meta Q4: EPS miss and Q1 revenue guide well below estimates; "
            "Apple privacy changes cited as ~$10B revenue headwind"
        ),
        publisher="CNBC",
        link="https://www.cnbc.com/2022/02/03/facebook-shares-plummet-22percent-after-reporting-weak-guidance.html",
        published="2022-02-03",
    ),
    NewsItem(
        title=(
            "Facebook DAU / user-growth slowdown collapses Meta growth narrative "
            "after earnings"
        ),
        publisher="AP",
        link="https://apnews.com/article/technology-business-media-social-media-facebook-cf74be789988e7e48f3e2fcdf80ddfa8",
        published="2022-02-03",
    ),
    NewsItem(
        title=(
            "Meta stock plunges ~26% in one day; ~$230B+ market-cap wipe "
            "(record single-day loss)"
        ),
        publisher="WSJ",
        link="https://www.wsj.com/articles/facebook-owner-metas-stock-price-plunges-premarket-jolting-tech-investors-11643887542",
        published="2022-02-03",
    ),
    NewsItem(
        title=(
            "Options volume surges; pre-earnings expected move only ~4.8% "
            "vs actual ~26% (far beyond straddle)"
        ),
        publisher="Reuters/ORATS",
        link="https://whbl.com/2022/02/03/meta-slide-drives-insane-options-volume-as-some-bet-on-bounce/",
        published="2022-02-03",
    ),
    NewsItem(
        title=(
            "JPMorgan downgrades Meta overweight to neutral; price target cut "
            "after weak guide"
        ),
        publisher="CNBC",
        link="https://www.cnbc.com/2022/02/03/facebook-shares-plummet-22percent-after-reporting-weak-guidance.html",
        published="2022-02-03",
    ),
]


class FixedNewsSource:
    """Return the same frozen headlines for every planned query."""

    source_id = "yfinance_news"

    def search(self, query: SearchQuery, *, ticker: str) -> list[NewsItem]:
        del query, ticker
        return list(_META_NEWS)


class _MockNarrator:
    def structured_invoke(self, *, system, human, schema):
        return schema(
            primary_driver="Delta / spot move",
            verdict="Earnings gap drove the move.",
            confidence_level="medium",
            confidence_rationale="Mock narrator for offline test.",
            evidence=[],
            takeaways=["Recheck residual and quote quality."],
            american_commentary="",
        )


class _MockVerifier:
    def structured_invoke(self, *, system, human, schema):
        return DiagnosticVerifierResult(
            verdict="PASS",
            missing_evidence=[],
            policy_flags=[],
            rationale="mock verifier",
        )


def _meta_deps() -> GraphDeps:
    return GraphDeps(
        market=FixtureMarketLoader(FIXTURE),
        pnl=OfficialFdmPnlSource(config=CFG),
        planner=CueQueryPlanner(),
        intel=IntelRegistry(
            {
                "yfinance_news": FixedNewsSource(),
                "tavily": StubIntelSource("tavily"),
                "sec_8k": StubIntelSource("sec_8k"),
            }
        ),
    )


def test_spot_move_matches_historical_closes():
    snap, _ = load_fixture(FIXTURE)
    assert snap.spot_prev == 320.19
    assert snap.spot_now == 237.76
    pct = snap.spot_now / snap.spot_prev - 1.0
    # 237.76 / 320.19 − 1 ≈ −25.7% (press often rounded to “~26%”).
    assert -0.27 < pct < -0.25


def test_taylor_residual_share_is_elevated():
    """Extreme gap → second-order Taylor leaves a large unexplained residual."""
    snap, surf = load_fixture(FIXTURE)
    pricing = price_and_attribute(snap, surf, None, config=CFG)
    pnl = pricing.pnl
    total = pnl.total_pnl
    assert abs(total) > 1.0
    share = abs(pnl.residual_pnl) / abs(total)
    assert share >= 0.20, f"expected residual share ≥20%, got {share:.1%}"
    facts = build_position_facts(snap, pricing)
    assert facts.residual_pct >= 15.0


def test_pipeline_frozen_news_and_elevated_residual():
    old_key = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-test-not-real"
    roles = LlmRoleRegistry(narrator=_MockNarrator(), verifier=_MockVerifier())
    cfg = PipelineConfig(
        features={"a1", "a2", "a3"},
        diag_budget=3,
        diag_iterations=2,
        verify_budget=1,
        require_openai=True,
    )
    try:
        result = run_pipeline(
            ticker="META",
            option_type="call",
            strike=320.0,
            expiry="2022-03-18",
            deps=_meta_deps(),
            roles=roles,
            config=cfg,
        )
    finally:
        if old_key is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = old_key

    assert result["snapshot"].as_of == "2022-02-03"
    assert result["snapshot"].spot_prev == 320.19
    assert result["snapshot"].spot_now == 237.76

    # Default CueQueryPlanner uses L1 factor shares; |delta| dwarfs residual/vega
    # here, so only the material ticker-headline query is required.
    cues = {q.cue for q in result["search_plan"].queries}
    assert "material" in cues
    assert result["search_plan"].skip_reason == ""

    titles = " ".join(n.title for n in result["news"])
    assert "EPS miss" in titles or "revenue guide" in titles
    assert "26%" in titles or "market-cap" in titles
    assert "4.8%" in titles

    facts = build_position_facts(result["snapshot"], result["pricing"])
    assert facts.residual_pct >= 15.0

    assert "1-day factor PnL" in result["blotter"]
    assert "Residual" in result["report"]
    assert "verdict" in result["diagnostic_synthesis"]


if __name__ == "__main__":
    test_spot_move_matches_historical_closes()
    test_taylor_residual_share_is_elevated()
    test_pipeline_frozen_news_and_elevated_residual()
    print("ok")
