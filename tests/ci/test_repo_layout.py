"""Repo layout guardrails — paths, gitignore conventions, no root report clutter."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


from bootstrap import find_repo_root, install

install()

from explain_my_option.data.synthetic import fixtures_dir, list_fixtures
from ci.fixture_schema import validate_all_fixtures
from explain_my_option.paths import (
    CI_DIR,
    FIXTURES_DIR,
    GOLDEN_DIR,
    HISTORICAL_DIR,
    HISTORICAL_OUTPUT_DIR,
    HISTORICAL_SUMMARY_PATH,
    LIVE_BOOK_DIR,
    LIVE_BOOK_OUTPUT_DIR,
    REPO_ROOT,
    ROOT_MARKDOWN_ALLOWLIST,
    ensure_report_output_dir,
    resolve_report_output_path,
)
from explain_my_option.paths import ReportPathError


def test_paths_match_repo_layout():
    assert REPO_ROOT.is_dir()
    assert (REPO_ROOT / "src" / "explain_my_option").is_dir()
    assert (REPO_ROOT / "app.py").is_file()
    assert (REPO_ROOT / "notebooks" / "getting_started.ipynb").is_file()
    assert (REPO_ROOT / "notebooks" / "langgraph_architecture.ipynb").is_file()
    assert CI_DIR == REPO_ROOT / "tests" / "ci"
    assert FIXTURES_DIR == CI_DIR / "fixtures"
    assert GOLDEN_DIR == CI_DIR / "golden"
    assert LIVE_BOOK_DIR == REPO_ROOT / "tests" / "live_book"
    assert HISTORICAL_DIR == REPO_ROOT / "tests" / "historical"
    assert LIVE_BOOK_OUTPUT_DIR == LIVE_BOOK_DIR / "output"
    assert HISTORICAL_OUTPUT_DIR == HISTORICAL_DIR / "output"
    assert HISTORICAL_SUMMARY_PATH == HISTORICAL_DIR / "historical_benchmark_summary.json"
    assert fixtures_dir() == FIXTURES_DIR
    assert find_repo_root() == REPO_ROOT
    assert find_repo_root(REPO_ROOT / "notebooks") == REPO_ROOT


def test_visitor_notebooks_exist():
    nb = REPO_ROOT / "notebooks"
    for name in (
        "getting_started.ipynb",
        "langgraph_architecture.ipynb",
    ):
        assert (nb / name).is_file(), name


def test_eval_runners_stay_out_of_product_src():
    """The three suites stay under tests/, not shipped product code."""
    assert (CI_DIR / "test_pricing_facade.py").is_file()
    assert (LIVE_BOOK_DIR / "portfolio_e2e.py").is_file()
    assert (HISTORICAL_DIR / "run.py").is_file()
    assert not (REPO_ROOT / "src" / "experiments").exists()
    assert not (REPO_ROOT / "src" / "live_book").exists()
    assert not (REPO_ROOT / "src" / "ci").exists()
    assert not (REPO_ROOT / "src" / "data" / "strikes.py").exists()
    for retired in (
        "experiments",
        "historical_benchmark",
        "benchmark_compare",
        "fixtures",
        "golden",
        "shared",
    ):
        assert not (REPO_ROOT / "tests" / retired).exists(), retired


def test_fixtures_dir_has_json():
    names = list_fixtures()
    assert names, "expected JSON under tests/ci/fixtures/"
    for name in names:
        assert (FIXTURES_DIR / f"{name}.json").is_file(), name


def test_fixture_schema_contract():
    errors = validate_all_fixtures()
    assert not errors, "fixture contract violations:\n" + "\n".join(errors)


def test_golden_dir_has_committed_baselines():
    assert GOLDEN_DIR.is_dir()
    assert any(GOLDEN_DIR.glob("*.md")), "tests/ci/golden/ should contain *.md baselines"


def test_report_output_dir_ready():
    out = ensure_report_output_dir()
    assert LIVE_BOOK_OUTPUT_DIR.is_dir()
    assert HISTORICAL_OUTPUT_DIR.is_dir()
    assert out == LIVE_BOOK_OUTPUT_DIR


def test_reject_report_in_repo_root():
    try:
        resolve_report_output_path("report_vol_crush.md", cwd=REPO_ROOT)
        raise AssertionError("expected ReportPathError")
    except ReportPathError:
        pass


def test_allow_report_under_tests_output():
    path = resolve_report_output_path(
        "tests/live_book/output/example.md", cwd=REPO_ROOT
    )
    assert LIVE_BOOK_OUTPUT_DIR.resolve() in path.parents or path.parent == LIVE_BOOK_OUTPUT_DIR.resolve()


def test_allow_historical_case_report():
    path = resolve_report_output_path(
        "tests/historical/output/vow_float_squeeze_2008/report.md",
        cwd=REPO_ROOT,
    )
    assert HISTORICAL_OUTPUT_DIR.resolve() in path.parents


def test_docs_samples_are_committed_product_reports():
    samples = REPO_ROOT / "docs" / "samples"
    expected = {
        "live.md": ("# Option Price Movement Diagnostic Report", "## 1. Headline"),
        "historical.md": ("# Option Price Movement Diagnostic Report", "META"),
        "unexplained_break.md": ("terminal unexplained break", "Terminal break"),
    }
    for name, needles in expected.items():
        path = samples / name
        assert path.is_file(), name
        text = path.read_text(encoding="utf-8")
        assert "## 4. Quantitative PnL Attribution" in text, name
        assert "## 5. Residual Drill" in text, name
        for needle in needles:
            assert needle in text, f"{name} missing {needle!r}"


def test_no_stray_report_markdown_in_repo_root():
    for path in REPO_ROOT.glob("*.md"):
        assert path.name in ROOT_MARKDOWN_ALLOWLIST, (
            f"unexpected Markdown at repo root: {path.name} "
            f"(move to a suite output folder or tests/ci/golden/)"
        )


if __name__ == "__main__":
    test_paths_match_repo_layout()
    test_visitor_notebooks_exist()
    test_eval_runners_stay_out_of_product_src()
    test_fixtures_dir_has_json()
    test_fixture_schema_contract()
    test_golden_dir_has_committed_baselines()
    test_report_output_dir_ready()
    test_reject_report_in_repo_root()
    test_allow_report_under_tests_output()
    test_allow_historical_case_report()
    test_docs_samples_are_committed_product_reports()
    test_no_stray_report_markdown_in_repo_root()
    print("OK — repo layout checks passed")
