"""A quiet day costs nothing and says nothing.

SPY on 2023-03-06, from a real option chain: the option barely moved and carry
explains it. Every LLM role here raises if it is called, and the run still
finishes: code decides there is nothing to explain, so there is no search, no
costly tool and no LLM call, and the report carries a fixed sentence instead of
a story. For contrast, a material move (the synthetic vol_crush fixture) gets a
search plan and two LLM calls. Offline, no key:

    python examples/governance/04_quiet_day.py

Pinned by tests/agent/test_historical_cases.py::test_quiet_days_have_nothing_to_explain.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from explain_my_option import ExplainMyOption, PipelineConfig  # noqa: E402
from explain_my_option.data.historical_chain import load_historical_case  # noqa: E402
from explain_my_option.graph.deps import GraphDeps  # noqa: E402
from explain_my_option.pricing.types import LoadedData  # noqa: E402
from explain_my_option.testing import frozen_intel, no_llm_roles, scripted_roles  # noqa: E402

CASE = "quiet_spy_2023-03-06"


class RealChain:
    """Market loader for a committed real-chain slice (quotes on both days)."""

    def load(self, *, ticker, option_type, strike, expiry) -> LoadedData:
        return LoadedData(snapshot=load_historical_case(CASE))


def show(label: str, text) -> None:
    print(f"    {label + ':':<16}{text}")


def main() -> dict:
    snap = load_historical_case(CASE)
    quiet = ExplainMyOption(
        config=PipelineConfig(require_openai=False),
        deps=GraphDeps(market=RealChain(), intel=frozen_intel()),
        roles=no_llm_roles(),
    ).diagnose_leg(snap.ticker, option_type=snap.option_type, strike=snap.strike, expiry=snap.expiry)
    tools = quiet.state["diagnostic_findings"]["tool_costs"]

    print(f"{snap.ticker} {snap.strike:g} {snap.option_type}, {snap.as_of}: option {snap.option_price_prev:.2f} -> {snap.option_price_now:.2f}")
    show("LLM calls", quiet.state["llm_calls"] or 0)
    show("Search", "none" if quiet.state["search_plan"] is None else quiet.state["search_plan"].queries)
    show("Tools", ", ".join(f"{name} ({cost})" for name, cost in tools.items()))
    show("Verdict", quiet.state["diagnostic_synthesis"]["verdict"])

    material = ExplainMyOption(config=PipelineConfig(require_openai=False), roles=scripted_roles()).diagnose_fixture("vol_crush")
    print("\nFor contrast, vol_crush (the option loses about a third of its value):")
    show("LLM calls", material.state["llm_calls"])
    show("Search", ", ".join(q.cue for q in material.state["search_plan"].queries))
    return {
        "llm_calls": quiet.state["llm_calls"] or 0,
        "searched": quiet.state["search_plan"] is not None,
        "all_tools_free": all(cost == "free" for cost in tools.values()),
        "no_escalation": quiet.state["no_escalation"],
        "material_llm_calls": material.state["llm_calls"],
    }


if __name__ == "__main__":
    main()
