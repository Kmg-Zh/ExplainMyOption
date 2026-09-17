"""LLM-path determinism (Task B3). Requires OPENAI_API_KEY -- not part of
./scripts/run-tests.sh (same convention as tests/historical/run.py, see
tests/README.md), run manually:

    python tests/live_book/test_determinism_llm.py

temperature=0.0 and a fixed seed are pinned in one place
(pipeline.llm_roles.OpenAiRole, recorded on every run manifest via
llm_run_metadata()). OpenAI does not itself guarantee bit-identical output
even with temperature=0 and a fixed seed -- only that the same params make
identical output more likely -- so this checks the fields the product
actually depends on being stable, not raw text equality.

The v3.1 spec names `catalyst_name` and `figures[]` as the fields to check.
Neither exists as a schema field today (WORK_ORDER_REPORT.md FINDINGS
#14/#15: B1.2/B1.3 were satisfied by a stronger, differently-shaped
mechanism -- a hard ban on any LLM-authored number in prose, and
CATALYST_TAGS in place of a free-text catalyst_name). So this checks the
closest fields that actually exist: `verifier_verdict`
(DiagnosticVerifierResult.verdict), `confidence_level`, `primary_driver`,
and the `evidence[].headline` set (the closest analogue of catalyst
identification the schema has).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from dotenv import load_dotenv

load_dotenv()

from live_book.portfolio_book import OfflineLeg
from live_book.portfolio_e2e import PatchingMarketLoader
from explain_my_option.agent_graph import run_pipeline
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.graph.deps import FixtureMarketLoader, GraphDeps, OfficialFdmPnlSource
from explain_my_option.intel.sources import IntelRegistry, StubIntelSource
from explain_my_option.pipeline.llm_roles import default_openai_roles
from explain_my_option.report.schema import DiagnosticSynthesis
from ci.engine_config import engine_config_for_tests

_REQUIRES_KEY_MSG = (
    "SKIP tests/live_book/test_determinism_llm.py: OPENAI_API_KEY not set "
    "(this module needs a real model -- see tests/README.md)."
)


def _deps_for_leg(leg) -> GraphDeps:
    patches = dict(leg.overrides)
    patches.setdefault("ticker", leg.ticker)
    return GraphDeps(
        market=PatchingMarketLoader(FixtureMarketLoader(leg.fixture), {leg.ticker: patches}),
        pnl=OfficialFdmPnlSource(config=engine_config_for_tests()),
        intel=IntelRegistry(
            {
                "yfinance_news": StubIntelSource("yfinance_news"),
                "tavily": StubIntelSource("tavily"),
                "sec_8k": StubIntelSource("sec_8k"),
            }
        ),
    )


def _run_once(leg) -> DiagnosticSynthesis:
    snap0, _ = load_fixture(leg.fixture)
    deps = _deps_for_leg(leg)
    roles = default_openai_roles()
    state = run_pipeline(
        ticker=leg.ticker,
        option_type=snap0.option_type,
        strike=snap0.strike,
        expiry=snap0.expiry,
        quantity=float(leg.overrides.get("quantity", snap0.quantity)),
        multiplier=float(leg.overrides.get("multiplier", snap0.multiplier)),
        deps=deps,
        roles=roles,
    )
    syn_raw = state.get("diagnostic_synthesis")
    assert syn_raw, f"{leg.ticker}: no diagnostic_synthesis produced (LLM path did not run)"
    return DiagnosticSynthesis.model_validate(syn_raw)


def test_narrator_and_verifier_stable_across_three_runs():
    if not os.getenv("OPENAI_API_KEY"):
        print(_REQUIRES_KEY_MSG)
        return
    leg = OfflineLeg("AAPL", "aapl_exdiv_2023", "ITM")
    runs = [_run_once(leg) for _ in range(3)]
    first = runs[0]
    first_headlines = sorted(e.headline for e in first.evidence)
    for other in runs[1:]:
        assert other.confidence_level == first.confidence_level
        assert other.primary_driver == first.primary_driver
        assert sorted(e.headline for e in other.evidence) == first_headlines


if __name__ == "__main__":
    test_narrator_and_verifier_stable_across_three_runs()
    if os.getenv("OPENAI_API_KEY"):
        print("OK — LLM-path determinism test passed")
