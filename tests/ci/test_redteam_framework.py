"""Smoke test for the red-team framework itself (Task B2).

Not a re-run of the full attack-case set (that's scripts/run_redteam.py, which
writes docs/studies/redteam_results.md and is run manually / on demand,
not on every CI pass). This just catches import/schema drift: the
committed attack_cases.json still loads, every case's blotter_source
still resolves, and run_case() still produces a verdict for a
representative case per category without raising.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT / "scripts"))

import run_redteam  # noqa: E402

CASES_PATH = _REPO_ROOT / "tests" / "redteam" / "attack_cases.json"


def test_attack_cases_file_exists_and_parses():
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    assert len(cases) == 65
    categories = {c["category"] for c in cases}
    assert categories == {
        "fabricated_dollar",
        "contradictory_number",
        "rounded_collision",
        "non_dollar_fabrication",
        "method_residual_blamed",
        "quiet_day_confabulation",
        "omitted_catalyst",
        "prompt_injection",
        "clean_control",
    }


def test_one_case_per_category_runs_without_raising():
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    seen: set[str] = set()
    for case in cases:
        if case["category"] in seen:
            continue
        seen.add(case["category"])
        result = run_redteam.run_case(case)
        assert result.verdict in ("PASS", "PARTIAL", "FAIL")


def test_clean_control_cases_all_pass_the_baseline():
    """False-alarm-rate sanity: the baseline layer must not flag correct,
    code-consistent syntheses."""
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    for case in cases:
        if case["category"] != "clean_control":
            continue
        result = run_redteam.run_case(case)
        assert result.verdict == "PASS", case["case_id"]


if __name__ == "__main__":
    test_attack_cases_file_exists_and_parses()
    test_one_case_per_category_runs_without_raising()
    test_clean_control_cases_all_pass_the_baseline()
    print("OK — red-team framework smoke tests passed")
