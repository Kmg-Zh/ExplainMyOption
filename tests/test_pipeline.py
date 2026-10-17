"""The LangGraph workflow end to end, offline: scripted LLM roles, frozen market and news."""

from __future__ import annotations

import json
import runpy
import shutil
import subprocess
import sys

import pytest
from support import (
    FAST,
    NoLlm,
    ScriptedNarrator,
    ScriptedRole,
    ScriptedVerifier,
    frozen_intel,
    invoke_leg,
    no_llm_roles,
    roles,
    run_leg,
)

from explain_my_option import cli
from explain_my_option.data.observation import ObservationStatus, continuity_gate
from explain_my_option.data_loader import LoadedData, NewsItem
from explain_my_option.graph.deps import GraphDeps, OfficialFdmPnlSource
from explain_my_option.graph.topology import book_mermaid, leg_mermaid
from explain_my_option.paths import FIXTURES_DIR, LIVE_BOOK_DIR, REPO_ROOT
from explain_my_option.pipeline.book_schema import BookLegSpec, load_book_json
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.portfolio_graph import run_book_pipeline
from explain_my_option.pricing.types import MarketSnapshot


LEG = BookLegSpec(leg_id="t", ticker="TEST", strike=100.0, expiry="2026-12-18")


class _NeverPrice:
    def attribute(self, snapshot, surface_data=None, surface_prev=None):
        raise AssertionError("the leg must stop before pricing")


def test_a_fixture_leg_runs_end_to_end_offline():
    narrator, verifier = ScriptedNarrator(), ScriptedVerifier()
    out = run_leg(fixture="vol_crush", llm=roles(narrator, verifier))
    assert "## 7. Risk Watchlist" in out["report"]
    assert narrator.verdict in out["report"]
    # No headlines: the digester and critic make no call; narrator and verifier make one each.
    assert (narrator.calls, verifier.calls, out["llm_calls"]) == (1, 1, 2)
    assert {"fetch_market", "quant", "diagnostic_pass", "synthesize", "verify"} <= set(out["stage_timings"])


def test_a_missing_observation_is_a_coverage_gap_not_an_unexplained_break():
    class MissingDay:
        def load(self, **_):
            continuity_gate(
                contract="TEST 100C",
                status_t1=ObservationStatus.OK,
                status_t=ObservationStatus.DAY_MISSING,
                date_t1="2026-08-28",
                date_t="2026-08-31",
            )

    out = invoke_leg(LEG, market=MissingDay(), pnl=_NeverPrice(), llm=no_llm_roles())
    assert out["terminal_no_comparable_observation"]
    assert out["report"].startswith("## No Comparable Observation")
    assert "DAY_MISSING on 2026-08-31" in out["report"] and "not an unexplained market move" in out["report"]
    assert not (out.get("diagnostic_findings") or {}).get("terminal_unexplained_break")


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

    out = invoke_leg(LEG, market=MisBased(), pnl=_NeverPrice(), llm=no_llm_roles())
    assert out["basis_mismatch_suspected"] and "blotter" not in out
    assert out["report"].startswith("## Basis Mismatch Suspected")


# --- Verifier routing ----------------------------------------------------------------------


def _verified(narrator=None, verifier=None) -> dict:
    out = run_leg(fixture="vol_crush", llm=roles(narrator, verifier))
    return {"out": out, "findings": out["diagnostic_findings"], "verdict": out["diagnostic_synthesis"]["verdict"]}


def test_a_passing_narrative_ships_unchanged():
    run = _verified()
    assert run["verdict"] == ScriptedNarrator().verdict and "verifier_status" not in run["findings"]


def test_a_partial_verdict_ships_with_the_verifier_caveat():
    run = _verified(verifier=ScriptedVerifier("PARTIAL", ("thin_evidence",)))
    assert run["verdict"].startswith("Reflect (PARTIAL):") and run["findings"]["verifier_status"] == "PARTIAL"
    assert "**Verifier**: PARTIAL" in run["out"]["report"]


@pytest.mark.parametrize(
    "narrator, verifier, flag",
    [
        (ScriptedNarrator(verdict="The selloff makes the option look cheap here."), NoLlm(), "prohibited_phrase"),
        (ScriptedNarrator(verdict="The residual is explained by the earnings announcement."), ScriptedVerifier("FAIL", ("method_residual_blamed",)), "method_residual_blamed"),
    ],
    ids=["caught by code before the verifier", "llm flag confirmed by code"],
)
def test_a_confirmed_hard_failure_escalates_to_a_terminal_break(narrator, verifier, flag):
    run = _verified(narrator, verifier)
    findings = run["findings"]
    assert findings["terminal_unexplained_break"] and findings["terminal_cause"] == "verifier_hard_fail"
    assert findings["terminal_verifier_flags"] == [flag]
    assert run["verdict"].startswith(f"Verifier FAIL — terminal break escalation ({flag}).")
    assert len(findings["verifier_audit"]["trace"]) == 1
    assert "the verifier's hard failure was confirmed by code" in run["out"]["report"]
    assert "diagnostic budget exhausted" not in run["out"]["report"]


def test_an_unconfirmed_llm_failure_is_downgraded_to_partial():
    run = _verified(verifier=ScriptedVerifier("FAIL", ("numeric_hallucination",)))
    assert not run["findings"].get("terminal_unexplained_break")
    assert run["findings"]["verifier_status"] == "PARTIAL"
    assert run["findings"]["verifier_audit"]["trace"][0]["llm_verdict"] == "FAIL"


def test_an_invented_dollar_figure_never_reaches_the_report():
    """The narrator's figure is caught at synthesis and replaced by the rule-based summary."""
    run = _verified(narrator=ScriptedNarrator(verdict="The desk gained $2.50 on the contract today."))
    assert "$2.50" not in run["out"]["report"]
    assert run["out"]["diagnostic_synthesis"]["confidence_rationale"].startswith("LLM synthesis failed")


# --- Headlines through the digest, critic and reconcile steps ---------------------------------

SQUEEZE = NewsItem(title="Short squeeze grips the stock as borrow costs spike", publisher="Wire", published="2026-08-14")


def test_a_required_catalyst_from_the_critic_reaches_the_narrative():
    digester = ScriptedRole({"relevant": [{"title": SQUEEZE.title, "mechanisms": ["squeeze", "borrow"], "one_line_fact": "Squeeze and borrow stress."}]})
    critic = ScriptedRole({"layer_b_required": True, "mechanisms": ["squeeze", "borrow"], "rationale": "Headline names a squeeze."})
    out = run_leg(fixture="vol_crush", news=[SQUEEZE], llm=roles(digester=digester, challenger=critic))
    verdict = out["diagnostic_synthesis"]["verdict"]
    assert "Independent critic: evidence is consistent with squeeze" in verdict
    assert out["llm_calls"] == 4  # digester, critic, narrator, verifier
    assert SQUEEZE.title in out["report"]


DIVIDEND = NewsItem(title="Stock trades ex-dividend tomorrow with a $0.24 quarterly dividend", publisher="Wire", published="2026-08-14")


def test_a_headline_figure_the_digester_quotes_is_not_an_invented_number():
    """Digest facts become evidence after the narrator's check, so code applies the same rule there."""
    fact = "Trades ex-dividend tomorrow for a $0.24 dividend."
    digester = ScriptedRole({"relevant": [{"title": DIVIDEND.title, "mechanisms": [], "one_line_fact": fact}]})
    out = run_leg(fixture="vol_crush", news=[DIVIDEND], llm=roles(digester=digester))
    evidence = out["diagnostic_synthesis"]["evidence"]
    assert [e["headline"] for e in evidence] == [DIVIDEND.title]  # the headline keeps its figure
    assert fact not in evidence[0]["relevance"]
    assert out["diagnostic_findings"].get("verifier_status") != "FAIL"


def test_an_unreliable_quote_skips_search_and_strips_invented_evidence():
    narrator = ScriptedRole(
        {
            "primary_driver": "Vega / implied volatility",
            "verdict": "Vega led the move.",
            "confidence_level": "medium",
            "confidence_rationale": "Scripted.",
            "evidence": [{"headline": "A headline nobody supplied", "source": "x", "relevance": "Supports the story."}],
        }
    )
    out = run_leg(case="gme_squeeze_2021_real", news=[SQUEEZE], llm=roles(narrator, digester=NoLlm(), challenger=NoLlm()))
    assert out["diagnostic_findings"]["observation_reliable"] is False
    assert out["search_plan"].skip_reason == "observation_lock" and not out["news"]
    assert out["diagnostic_synthesis"]["evidence"] == []


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
