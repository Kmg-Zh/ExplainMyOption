"""CLI smoke test for `python app.py --no-llm` (Task B4).

The quant path must run to a complete report with zero LLM calls and no
OPENAI_API_KEY -- this is how a reviewer without a key evaluates the repo.
Uses a fixture (no network) so this stays in the offline CI suite.
"""

from __future__ import annotations

import contextlib
import io
import os
import sys
from pathlib import Path

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

import app  # noqa: E402


def _run_cli(argv: list[str]) -> str:
    old_argv = sys.argv
    old_key = os.environ.pop("OPENAI_API_KEY", None)
    buf = io.StringIO()
    try:
        sys.argv = ["app.py", *argv]
        with contextlib.redirect_stdout(buf):
            app.run_cli()
    finally:
        sys.argv = old_argv
        if old_key is not None:
            os.environ["OPENAI_API_KEY"] = old_key
    return buf.getvalue()


def test_no_llm_flag_produces_a_complete_report_without_a_key():
    out = _run_cli(["--fixture", "vol_crush", "--no-llm"])
    assert "# Option Price Movement Diagnostic Report" in out
    assert "## 4. Quantitative PnL Attribution" in out
    assert "No OPENAI_API_KEY" in out  # fallback_synthesis's own rationale text


def test_no_llm_flag_rejects_book_mode():
    try:
        _run_cli(["--book", "whatever.json", "--no-llm"])
    except SystemExit:
        pass
    else:
        raise AssertionError("expected --book + --no-llm to be rejected via parser.error")


if __name__ == "__main__":
    test_no_llm_flag_produces_a_complete_report_without_a_key()
    test_no_llm_flag_rejects_book_mode()
    print("OK — --no-llm CLI smoke tests passed")
