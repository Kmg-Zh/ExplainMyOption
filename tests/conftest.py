"""Offline test setup: import this checkout's ``src`` and never see real credentials."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT / "tests", ROOT / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

# Blank rather than unset: python-dotenv (loaded by the CLI) never overrides an
# existing variable, so a developer's .env cannot leak a real key into a test.
_CREDENTIALS = (
    "OPENAI_API_KEY",
    "TAVILY_API_KEY",
    "EMO_SEC_USER_AGENT",
    "EMO_DIAGNOSE_SYSTEM_EXTRA",
    "EMO_DIAGNOSE_SYSTEM_EXTRA_FILE",
    "LANGSMITH_TRACING",
    "LANGCHAIN_TRACING_V2",
)


@pytest.fixture(autouse=True)
def offline(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in _CREDENTIALS:
        monkeypatch.setenv(name, "")
