"""The workflow as software, offline: the graph runs, guards its inputs, fans out a book, ships a CLI.

Governance outcomes of the same runs (verifier, invented figures, catalysts) are in
tests/agent/test_governed_runs.py.
"""

from __future__ import annotations

import dataclasses
import json
import runpy
import shutil
import subprocess
import sys
from datetime import date

import pytest
from live_book.roll import RollInputs, is_standard_monthly, pick_expiry, pick_strike, successor, third_friday
from support import (
    FAST,
    LEG,
    NeverPrice,
    ScriptedNarrator,
    ScriptedVerifier,
    aapl_nov20_call,
    frozen_intel,
    invoke_leg,
    jpm_oct23_straddle,
    no_llm_roles,
    roles,
    run_leg,
)

from explain_my_option import cli
from explain_my_option.agent_graph import run_pipeline
from explain_my_option.data_loader import LoadedData
from explain_my_option.graph.deps import GraphDeps, OfficialFdmPnlSource
from explain_my_option.graph.topology import book_mermaid, leg_mermaid
from explain_my_option.paths import FIXTURES_DIR, LIVE_BOOK_DIR, REPO_ROOT
from explain_my_option.pipeline.book_schema import BookLegSpec, load_book_json
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


@pytest.mark.parametrize(
    "strike, pnl, failing",
    [
        (325.0, NeverPrice(), "T-1 mark >= no-arbitrage lower bound"),  # stops before pricing
        (350.0, None, "T calibrated IV ~= quote-source IV"),  # stops after calibration, before the blotter
    ],
)
def test_marks_paired_with_a_stale_spot_end_in_a_data_break(strike, pnl, failing):
    """The 2026-11-04 AAPL vertical: no blotter, no narrative, no LLM call."""
    snap = aapl_nov20_call(strike, stale_spot=True)

    class StaleSpot:
        def load(self, **_):
            return LoadedData(snapshot=snap)

    leg = BookLegSpec(leg_id="aapl", ticker="AAPL", option_type="call", strike=strike, expiry="2026-11-20")
    out = invoke_leg(leg, market=StaleSpot(), pnl=pnl, llm=no_llm_roles())
    assert out["data_break"] and "blotter" not in out and not out.get("llm_calls")
    assert out["report"].startswith("## Data Break") and f"Data break: {failing} failed" in out["report"]


# --- Expiry and roll ---------------------------------------------------------------------------


class _Expired:
    def __init__(self, snap: MarketSnapshot):
        self.snap = snap

    def load(self, **_):
        return LoadedData(snapshot=self.snap)


def test_an_expired_leg_settles_without_pricing_search_or_an_llm_call():
    """The JPM 350P from 10-23 on: a RuntimeError every day, instead of a settlement."""
    deps = GraphDeps(market=_Expired(jpm_oct23_straddle("put")), pnl=NeverPrice(), intel=frozen_intel())
    out = run_pipeline("JPM", "put", 350.0, "2026-10-23", multiplier=100.0, deps=deps,
                       config=PipelineConfig(require_openai=False), roles=no_llm_roles())
    settlement = out["settlement"]
    assert settlement.outcome == "exercised" and settlement.position_pnl == pytest.approx(432.0)
    assert out["report"].startswith("## Expiry Settlement") and not out["llm_calls"]
    assert "pricing" not in out and "Exercised: the position sells 100 shares at 350" in out["report"]


def test_a_book_lists_settled_legs_apart_from_the_diagnosed_ones():
    book = load_book_json(FIXTURES_DIR / "books" / "demo_book.json")
    expired = BookLegSpec(leg_id="jpm_call", ticker="JPM", option_type="call", strike=350.0, expiry="2026-10-23", multiplier=100.0)
    book = dataclasses.replace(book, legs=(*book.legs[:2], expired))
    deps = GraphDeps(market=_Expired(jpm_oct23_straddle("call")), pnl=OfficialFdmPnlSource(config=FAST), intel=frozen_intel())
    out = run_book_pipeline(book, config=PipelineConfig(require_openai=False), deps=deps, roles=roles())
    results = {r["leg_id"]: r for r in out["leg_results"]}
    assert all(r["ok"] for r in results.values()) and results["jpm_call"]["bundle"] is None
    assert results["jpm_call"]["settlement"].outcome == "expired worthless"
    report = out["report"]
    assert "* **Settled at expiry**: `-$2.0000` across 1 leg(s), not in the totals above" in report
    assert "### Position 2" in report and "### Position 3" not in report
    assert "| `JPM 350C 2026-10-23` | expired worthless | 0.0000 | `-$2.0000` |" in report


LISTED_NOV05 = ("2026-11-06", "2026-11-13", "2026-11-20", "2026-11-27", "2026-12-04", "2026-12-11",
                "2026-12-18", "2027-01-15", "2027-03-19")  # JPM's list on 2026-11-05


def test_the_roll_takes_the_first_monthly_expiry_at_least_35_days_out():
    assert pick_expiry(LISTED_NOV05, date(2026, 11, 5)) == "2026-12-18"  # 43 days; weeklies skipped
    assert pick_expiry(LISTED_NOV05, date(2026, 11, 20)) == "2027-01-15"  # 12-18 is only 28 days out
    assert third_friday(2027, 3) == date(2027, 3, 19)
    # A holiday-shortened week lists the Thursday instead of the third Friday.
    assert is_standard_monthly(date(2027, 3, 18), {date(2027, 3, 18)})
    assert not is_standard_monthly(date(2027, 3, 18), {date(2027, 3, 18), date(2027, 3, 19)})


def test_a_rolled_leg_keeps_its_target_strike_to_spot():
    rows = {row["leg_id"]: row for row in json.loads((REPO_ROOT / "docs" / "runlog" / "book.json").read_text())["legs"]}
    inputs = RollInputs(session=date(2026, 11, 5), spot=337.34, expiries=LISTED_NOV05,
                        quoted_strikes={"2026-12-18": (325.0, 330.0, 335.0, 340.0, 345.0)})
    for leg_id in ("jpm_straddle_call", "jpm_straddle_put"):
        row = rows[leg_id]
        new = successor(row, inputs)
        # 1.0031 × 337.34 = 338.39: both straddle legs land on the same strike.
        assert (new["strike"], new["expiry"], new["picked_session"]) == (340.0, "2026-12-18", "2026-11-05")
        assert {k: new[k] for k in ("leg_id", "option_type", "quantity", "target_strike_to_spot")} == {
            k: row[k] for k in ("leg_id", "option_type", "quantity", "target_strike_to_spot")
        }
    assert pick_strike((335.0, 340.0), 337.5) == 335.0  # a tie goes to the lower strike
    with pytest.raises(ValueError, match="two-sided quote"):
        pick_strike((), 337.5)


def test_every_run_log_leg_carries_its_roll_target():
    for leg in json.loads((REPO_ROOT / "docs" / "runlog" / "book.json").read_text())["legs"]:
        assert leg["target_strike_to_spot"] > 0 and leg["spot_at_pick"] > 0
        date.fromisoformat(leg["picked_session"])


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
    for node in ("fetch_market", "settle_expiry", "quant", "blotter", "diagnostic_pass", "plan_search", "search", "digest_news",
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
import explain_my_option.testing  # the scripted roles need no engine either
from explain_my_option.graph.playbook import DEFAULT_PLAYBOOK, check_playbook, select_records
check_playbook(DEFAULT_PLAYBOOK)  # nor do the playbook's checks and selection
assert select_records({{"terminal_unexplained_break": True}}, DEFAULT_PLAYBOOK)
assert "## 7. Risk Watchlist" in runpy.run_path({str(EXAMPLE)!r})["main"]()
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
