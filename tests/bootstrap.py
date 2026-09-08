"""Put repo root and ``tests/`` on ``sys.path`` for ``python tests/...`` invocations."""

from __future__ import annotations

import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
SRC_DIR = REPO_ROOT / "src"


def _is_repo_root(path: Path) -> bool:
    return (path / "src" / "explain_my_option").is_dir() and (path / "pyproject.toml").is_file()


def find_repo_root(start: Path | None = None) -> Path:
    """Walk up from ``start`` (default: cwd) to the package root.

    Notebooks and ``python tests/...`` scripts should call this instead of
    probing for the removed ``src/agent_graph.py`` path.
    """
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if _is_repo_root(candidate):
            return candidate
    via_file = Path(__file__).resolve().parent.parent
    if _is_repo_root(via_file):
        return via_file
    raise RuntimeError(
        "Cannot find the ExplainMyOption repo root. Open notebooks from the "
        "repo (or set the kernel cwd there). Expected src/explain_my_option/ "
        "and pyproject.toml."
    )


def install(start: Path | None = None) -> Path:
    root = find_repo_root(start)
    tests = root / "tests"
    src = root / "src"
    for path in (root, tests, src):
        s = str(path)
        if s not in sys.path:
            sys.path.insert(0, s)
    return root
