"""A data gap is not a market story.

The market loader reports that the contract had no quote on the second day. A
one-day attribution needs the same contract observed on both dates, so code
stops the leg before pricing and before any LLM role: the report names the
coverage gap and says it is not an unexplained market move. Every LLM role here
raises if called. Offline, no key:

    python examples/governance/05_data_gap.py

Pinned by tests/agent/test_governed_runs.py::test_a_missing_observation_is_a_coverage_gap_not_an_unexplained_break.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from explain_my_option import ExplainMyOption, PipelineConfig  # noqa: E402
from explain_my_option.data.observation import ObservationStatus, continuity_gate  # noqa: E402
from explain_my_option.graph.deps import GraphDeps  # noqa: E402
from explain_my_option.pipeline.book_schema import BookLegSpec, BookSpec  # noqa: E402
from explain_my_option.testing import frozen_intel, no_llm_roles  # noqa: E402


class MissingSecondDay:
    """Quoted on 2026-08-28, no data at all on 2026-08-31."""

    def load(self, *, ticker, option_type, strike, expiry):
        continuity_gate(
            contract=f"{ticker} {strike:g}{option_type[0].upper()} {expiry}",
            status_t1=ObservationStatus.OK,
            status_t=ObservationStatus.DAY_MISSING,
            date_t1="2026-08-28",
            date_t="2026-08-31",
        )


class CountingPnl:
    """A PnL source that counts how often it is asked to price."""

    calls = 0

    def attribute(self, snapshot, surface_data=None, surface_prev=None):
        self.calls += 1
        raise AssertionError("the leg should stop before pricing")


def show(label: str, text) -> None:
    print(f"{label + ':':<18}{text}")


def main() -> dict:
    pnl = CountingPnl()
    agent = ExplainMyOption(
        config=PipelineConfig(require_openai=False),
        deps=GraphDeps(market=MissingSecondDay(), pnl=pnl, intel=frozen_intel()),
        roles=no_llm_roles(),
    )
    leg = BookLegSpec(leg_id="AAPL", ticker="AAPL", strike=230.0, expiry="2026-12-18")
    result = agent.diagnose_book(BookSpec(version="1", as_of="", legs=(leg,)))["leg_results"][0]

    print(result["report"].strip())
    print()
    show("Steps that ran", " -> ".join(result["stage_timings"]))
    show("Pricing calls", pnl.calls)
    show("LLM calls", result["llm_calls"] or 0)
    return {
        "report": result["report"],
        "coverage_gap": result["terminal_no_comparable_observation"],
        "pricing_calls": pnl.calls,
        "llm_calls": result["llm_calls"] or 0,
    }


if __name__ == "__main__":
    main()
