"""Repository layout: fixtures, eval suites and their (gitignored) output folders."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

TESTS_DIR = REPO_ROOT / "tests"
LIVE_BOOK_DIR = TESTS_DIR / "live_book"
HISTORICAL_DIR = TESTS_DIR / "historical"

# Synthetic market snapshots (the CLI's --fixture names live here).
FIXTURES_DIR = TESTS_DIR / "fixtures"
# Hand-tuned "case" fixtures (spot/IV chosen to force a residual regime):
# regression inputs for the attribution code, not evidence about real days.
STRESS_FIXTURES_DIR = FIXTURES_DIR / "stress"
# Real-chain slices written by scripts/fetch_chains.py.
HISTORICAL_FIXTURES_DIR = FIXTURES_DIR / "historical"
GOLDEN_DIR = FIXTURES_DIR / "golden"
HISTORICAL_SUMMARY_PATH = HISTORICAL_DIR / "historical_benchmark_summary.json"

LIVE_BOOK_OUTPUT_DIR = LIVE_BOOK_DIR / "output"
HISTORICAL_OUTPUT_DIR = HISTORICAL_DIR / "output"


def historical_case_dir(test_id: str) -> Path:
    """Local folder for one historical event case (gitignored)."""
    return HISTORICAL_OUTPUT_DIR / test_id


def historical_compare_dir(test_id: str) -> Path:
    """Governed-vs-baseline artifacts for one historical case."""
    return historical_case_dir(test_id) / "compare"


# Markdown files allowed at repo root (not diagnostic report dumps).
ROOT_MARKDOWN_ALLOWLIST = frozenset({"README.md", "AGENTS.md", "ACKNOWLEDGMENTS.md"})


class ReportPathError(ValueError):
    """Refuse to write a diagnostic report outside the agreed layout."""


def resolve_report_output_path(raw: str, *, cwd: Path | None = None) -> Path:
    """Resolve CLI ``--output`` and enforce OSS layout rules.

    Relative paths are resolved from ``cwd`` (default: process cwd).
    Diagnostic ``*.md`` files must not land in the repo root.
    """
    base = cwd or Path.cwd()
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (base / path).resolve()
    else:
        path = path.resolve()

    if path.suffix.lower() == ".md" and path.parent == REPO_ROOT:
        if path.name not in ROOT_MARKDOWN_ALLOWLIST:
            raise ReportPathError(
                f"Refusing to write report to repo root ({path.name}). "
                f"Use {LIVE_BOOK_OUTPUT_DIR.relative_to(REPO_ROOT)}/ or "
                f"{HISTORICAL_OUTPUT_DIR.relative_to(REPO_ROOT)}/<case>/ "
                f"(not the repo root)."
            )
    return path


def ensure_report_output_dir() -> Path:
    """Create gitignored eval output folders if missing."""
    LIVE_BOOK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    HISTORICAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return LIVE_BOOK_OUTPUT_DIR
