"""An LLM's hard FAIL counts only when code can reproduce it.

The verifier LLM checks the narrator's story, but its hard FAIL ends a leg only
if code finds the same violation. Two runs on the same position:

1. The verifier fails a clean narrative for an invented number that is not
   there. Code finds none, so the leg ships as PARTIAL with the verifier's note.
2. The narrator blames the model residual on earnings and the verifier fails
   it. Code confirms the violation, so the leg stops with a terminal break and
   goes to a person.

Offline, no key:

    python examples/governance/03_verifier_needs_code_proof.py

Pinned by tests/agent/test_governed_runs.py::test_an_unconfirmed_llm_failure_is_downgraded_to_partial
and ::test_a_confirmed_hard_failure_escalates_to_a_terminal_break.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from explain_my_option import ExplainMyOption, PipelineConfig  # noqa: E402
from explain_my_option.testing import ScriptedNarrator, ScriptedVerifier, scripted_roles  # noqa: E402

RUNS = (
    ("A false alarm", ScriptedNarrator(), ScriptedVerifier("FAIL", ("numeric_hallucination",))),
    (
        "A real violation",
        ScriptedNarrator(verdict="The residual is explained by the earnings announcement."),
        ScriptedVerifier("FAIL", ("method_residual_blamed",)),
    ),
)


def show(label: str, text: str) -> None:
    print(f"    {label + ':':<22}{text}")


def main() -> list[dict]:
    outcomes = []
    for title, narrator, verifier in RUNS:
        agent = ExplainMyOption(config=PipelineConfig(require_openai=False), roles=scripted_roles(narrator, verifier))
        result = agent.diagnose_fixture("vol_crush")
        findings = result.state["diagnostic_findings"]
        final = findings["verifier_audit"]["trace"][-1]
        terminal = bool(findings.get("terminal_unexplained_break"))
        shipped = "terminal break, for human review" if terminal else f"{final['verdict']}, with the verifier's caveat"
        verifier_line = next(line for line in result.report.splitlines() if line.startswith("* **Verifier**"))

        print(title)
        show("The narrator wrote", narrator.verdict)
        show("The verifier said", f"{verifier.verdict} {list(verifier.flags)}")
        show("After the code check", f"{final['verdict']} {final['policy_flags']}")
        show("Shipped as", shipped)
        show("Report", verifier_line.removeprefix("* "))
        print()
        outcomes.append({"code_verdict": final["verdict"], "code_flags": final["policy_flags"], "terminal": terminal})
    return outcomes


if __name__ == "__main__":
    main()
