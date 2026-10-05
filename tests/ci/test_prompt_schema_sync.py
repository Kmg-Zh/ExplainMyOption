"""Narrator prompt / blotter schema sync: Task A9.2.

The narrator prompt carries an explicit, generated (not hand-typed) list
of the blotter fields it may cite (graph.prompts.blotter_field_whitelist_section,
backed by report.facts.blotter_field_names). This checks both directions:
every field named in that generated section exists in the blotter
dataclasses, and every blotter field the verifier actually reads
(facts.<x> in pipeline/verifier.py) is named in the prompt.
"""

from __future__ import annotations

import re
from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from explain_my_option.graph.prompts import (
    STRUCTURED_DIAGNOSE_SYSTEM_PROMPT,
    blotter_field_whitelist_section,
    compose_diagnose_system_prompt,
)
from explain_my_option.report.facts import blotter_field_names

_VERIFIER_SRC = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "explain_my_option"
    / "pipeline"
    / "verifier.py"
).read_text(encoding="utf-8")

# facts.<name> -- PositionFacts attribute reads in the verifier's own code.
_FACTS_FIELD_RE = re.compile(r"\bfacts\.([a-zA-Z_][a-zA-Z0-9_]*)\b")


def test_whitelist_section_is_generated_not_stale():
    """Regenerating from the dataclasses right now must match what a fresh
    prompt composition embeds -- proves it's computed, not hand-typed."""
    fresh = blotter_field_whitelist_section()
    composed = compose_diagnose_system_prompt(extra=None)
    assert fresh in composed


def test_every_whitelisted_field_exists_in_the_blotter_dataclasses():
    schema_names = blotter_field_names()
    section = blotter_field_whitelist_section()
    cited = re.findall(r"`([a-zA-Z_][a-zA-Z0-9_]*)`", section)
    assert cited, "expected at least one backtick-quoted field name"
    for name in cited:
        assert name in schema_names, f"{name} is listed in the prompt but not in the blotter schema"


def test_every_verifier_checked_field_is_named_in_the_prompt():
    composed = compose_diagnose_system_prompt(extra=None)
    checked = sorted(set(_FACTS_FIELD_RE.findall(_VERIFIER_SRC)))
    assert checked, "expected the verifier source to reference at least one facts.<field>"
    schema_names = blotter_field_names()
    for name in checked:
        assert name in schema_names, f"verifier reads facts.{name}, not a real blotter field"
        assert f"`{name}`" in composed, f"verifier reads facts.{name}, but the prompt never names it"


def test_base_prompt_still_present_under_the_whitelist():
    composed = compose_diagnose_system_prompt(extra=None)
    assert composed.startswith(STRUCTURED_DIAGNOSE_SYSTEM_PROMPT.strip()[:200])


if __name__ == "__main__":
    test_whitelist_section_is_generated_not_stale()
    test_every_whitelisted_field_exists_in_the_blotter_dataclasses()
    test_every_verifier_checked_field_is_named_in_the_prompt()
    test_base_prompt_still_present_under_the_whitelist()
    print("OK — prompt/blotter schema sync tests passed")
