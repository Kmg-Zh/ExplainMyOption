"""The workflow as software, offline: the graph runs, guards its inputs, fans out a book, ships a CLI.

Governance outcomes of the same runs (verifier, invented figures, catalysts) are in
tests/agent/test_governed_runs.py.
"""

from __future__ import annotations

import json
import runpy
import shutil
import subprocess
import sys

import pytest
from support import (
    FAST,
    LEG,
    NeverPrice,
    ScriptedNarrator,
    ScriptedVerifier,
    frozen_intel,
    invoke_leg,
    no_llm_roles,
    roles,
    run_leg,
)

from explain_my_option import cli
from explain_my_option.data_loader import LoadedData
from explain_my_option.graph.deps import GraphDeps, OfficialFdmPnlSource
from explain_my_option.graph.topology import book_mermaid, leg_mermaid
from explain_my_option.paths import FIXTURES_DIR, LIVE_BOOK_DIR, REPO_ROOT
from explain_my_option.pipeline.book_schema import load_book_json
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.portfolio_graph import run_book_pipeline
from explain_my_option.pricing.types import MarketSnapshot


def test_a_fixture_leg_runs_end_to_end_offline():
    narrator, verifier = ScriptedNarrator(), ScriptedVerifier()
    out = run_leg(fixture="vol_crush", llm=roles(narrator, verifier))
    assert "## 7. Risk Watchlist" in out["report"]
    assert narrator.verdict in out["report"]
    # No headlines: the digester and critic make no call; narrator and verifier make one each.
    assert (narrator.calls, verifier.calls, out["llm_calls"]) == (1, 1, 2)
    assert {"fetch_market", "quant", "diagnostic_pass", "synthesize", "verify"} <= set(out["stage_timings"])


def test_a_mis_based_quote_aborts_before_pricing():
    """A pre-split strike against a post-split spot: the call mid sits far above spot."""
    snap = MarketSnapshot(
        ticker="GME", option_type="call", strike=340.0, expiry="2027-01-15", spot_now=25.0, spot_prev=25.0,
        iv_now=0.30, iv_prev=0.28, option_price_now=300.0, option_price_prev=295.0, time_to_expiry_years=0.5,
        mid=300.0, data_source="yfinance", as_of="2026-08-30",
    )

    class MisBased:
        def load(self, **_):
            return LoadedData(snapshot=snap)

    out = invoke_leg(LEG, market=MisBased(), pnl=NeverPrice(), llm=no_llm_roles())
    assert out["basis_mismatch_suspected"] and "blotter" not in out
    assert out["report"].startswith("## Basis Mismatch Suspected")


# --- Book, entry gate, CLI, topology -----------------------------------------------------------


def test_a_book_reports_every_leg_and_lists_the_failed_ones():
    book = load_book_json(FIXTURES_DIR / "books" / "demo_book.json")
    deps = GraphDeps(pnl=OfficialFdmPnlSource(config=FAST), intel=frozen_intel())
    out = run_book_pipeline(book, config=PipelineConfig(require_openai=False), deps=deps, roles=roles())
    assert {r["leg_id"]: r["ok"] for r in out["leg_results"]} == {"AAPL": True, "META": True, "FAIL": False}
    assert "### Position 2" in out["report"] and "## Failed legs" in out["report"]


def test_the_pipeline_refuses_to_start_without_an_api_key():
    book = load_book_json(FIXTURES_DIR / "books" / "demo_book.json")
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        run_book_pipeline(book, config=PipelineConfig(), roles=roles())


def test_no_llm_cli_renders_a_complete_report_without_a_key(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["explain-my-option", "--fixture", "vol_crush", "--no-llm"])
    cli.run_cli()
    report = capsys.readouterr().out
    assert "## 4. Quantitative PnL Attribution" in report and "No OPENAI_API_KEY" in report
    monkeypatch.setattr(sys, "argv", ["explain-my-option", "--book", "x.json", "--no-llm"])
    with pytest.raises(SystemExit):
        cli.run_cli()


def test_the_compiled_graph_matches_the_documented_workflow():
    leg = leg_mermaid(roles=roles())
    for node in ("fetch_market", "quant", "blotter", "diagnostic_pass", "plan_search", "search", "digest_news",
                 "challenge_catalyst", "synthesize", "reconcile_debate", "verify", "reflect_verifier",
                 "terminal_unexplained_break", "finalize_leg_report", "leg_failure_finalize"):
        assert node in leg
    book = book_mermaid(config=PipelineConfig(require_openai=False), roles=roles())
    assert all(node in book for node in ("require_openai", "leg_branch", "aggregate_book"))


@pytest.mark.parametrize("path", [REPO_ROOT / "docs" / "runlog" / "book.json", *sorted((LIVE_BOOK_DIR / "pinned_books").glob("*.json"))])
def test_pinned_books_name_explicit_unique_contracts(path):
    """The scheduled jobs read these; a re-pin must keep every leg explicit."""
    legs = json.loads(path.read_text())["legs"]
    ids = [leg.get("leg_id") or leg["ticker"] for leg in legs]
    assert len(ids) == len(set(ids))
    assert all(leg.get("strike") and leg.get("expiry") for leg in legs)


# --- Your own PnL system (docs/INTEGRATION.md) ----------------------------------------------

EXAMPLE = REPO_ROOT / "examples" / "bring_your_own_pnl.py"
# What docs/INTEGRATION.md says a desk with its own adapters may delete.
REFERENCE_ENGINE_FILES = (
    "pricing/analysis_api.py", "pricing/calibrate.py", "pricing/engines", "pricing/facade.py",
    "pricing/ql_engine.py", "pricing/registry.py", "pricing/risk.py", "pricing/second_order.py",
    "pricing/sequential_reval.py", "pricing/surface.py", "pricing/vol_models.py", "data_loader.py",
    "data/cache.py", "data/dividends.py", "data/historical_chain.py", "data/rates.py", "data/realized.py",
    "cli.py",
)


def test_the_example_runs_a_desk_pnl_source_end_to_end():
    report = runpy.run_path(str(EXAMPLE))["main"]()
    assert "Priced by desk_risk" in report
    assert "QuantLib" not in report and "FDM" not in report
    # The headline return is per option, not the 10 × 100 position PnL over one option's price.
    assert "`+$1,550.0000` (+36.7%)" in report
    assert "`taylor_second_order` — the PnL source has no revaluation hook" in report


def test_the_agent_runs_with_the_reference_engine_deleted(tmp_path):
    pkg = tmp_path / "explain_my_option"
    shutil.copytree(REPO_ROOT / "src" / "explain_my_option", pkg, ignore=shutil.ignore_patterns("__pycache__"))
    for rel in REFERENCE_ENGINE_FILES:
        path = pkg / rel
        shutil.rmtree(path) if path.is_dir() else path.unlink()
    script = f"""
import runpy, sys
for name in ("QuantLib", "yfinance", "pandas", "scipy", "numpy"):
    sys.modules[name] = None  # importing any of them now fails
sys.path.insert(0, {str(tmp_path)!r})
import explain_my_option
assert explain_my_option.__file__.startswith({str(tmp_path)!r}), explain_my_option.__file__
assert "## 7. Risk Watchlist" in runpy.run_path({str(EXAMPLE)!r})["main"]()
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
