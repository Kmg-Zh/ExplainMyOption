"""The narrator never prints a figure: every number in the report comes from the engine.

The narrator is scripted to claim a dollar gain. Code checks every reply before
it is used; this one carries a figure, so the report ships the rule-based
summary instead, and the invented "$2.50" never reaches it. Offline, no key:

    python examples/governance/01_invented_number.py

Pinned by tests/agent/test_governed_runs.py::test_an_invented_dollar_figure_never_reaches_the_report.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from explain_my_option import ExplainMyOption, PipelineConfig  # noqa: E402
from explain_my_option.report import validate_synthesis  # noqa: E402
from explain_my_option.report.schema import DiagnosticSynthesis  # noqa: E402
from explain_my_option.testing import ScriptedNarrator, scripted_roles  # noqa: E402

CLAIM = "The desk gained $2.50 on the contract today."


def show(label: str, text: str) -> None:
    print(f"{label + ':':<24}{text}")


def main() -> dict:
    agent = ExplainMyOption(
        config=PipelineConfig(require_openai=False),
        roles=scripted_roles(ScriptedNarrator(verdict=CLAIM)),
    )
    result = agent.diagnose_fixture("vol_crush")
    synthesis = result.state["diagnostic_synthesis"]

    # The check the synthesize step runs on every narrator reply.
    reply = ScriptedNarrator(verdict=CLAIM).structured_invoke(system="", human="", schema=DiagnosticSynthesis)
    reasons = validate_synthesis(reply)

    show("The narrator wrote", CLAIM)
    show("Code check", " ".join(reasons))
    show("Report verdict", synthesis["verdict"])
    show("Confidence note", synthesis["confidence_rationale"])
    show('"$2.50" in the report', "yes" if "$2.50" in result.report else "no")
    return {"reasons": reasons, "claim_in_report": "$2.50" in result.report, "rationale": synthesis["confidence_rationale"]}


if __name__ == "__main__":
    main()
