"""Graph compile + fixture invoke (no network)."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import os

from bootstrap import install

install()

from explain_my_option.agent_graph import build_graph, run_pipeline

from explain_my_option.data_loader import NewsItem
from explain_my_option.graph.deps import FixtureMarketLoader, GraphDeps, OfficialFdmPnlSource, fixture_deps
from explain_my_option.graph.prompts import (
    DEFAULT_DIAGNOSE_SYSTEM_PROMPT,
    STRUCTURED_DIAGNOSE_SYSTEM_PROMPT,
    compose_diagnose_system_prompt,
    extra_from_env,
)
from explain_my_option.intel.planner import CueQueryPlanner
from explain_my_option.intel.sources import IntelRegistry, StubIntelSource
from explain_my_option.intel.types import SearchQuery
from ci.engine_config import engine_config_for_tests
from explain_my_option.pipeline.config import PipelineConfig
from explain_my_option.pipeline.llm_roles import LlmRoleRegistry
from explain_my_option.pipeline.verifier_schema import DiagnosticVerifierResult

CFG = engine_config_for_tests()


class RecordingNewsSource:
    source_id = "yfinance_news"

    def __init__(self) -> None:
        self.seen: list[str] = []

    def search(self, query: SearchQuery, *, ticker: str) -> list[NewsItem]:
        self.seen.append(query.q)
        return [NewsItem(title=f"{ticker} headline ({query.cue})", publisher="test")]


class _MockNarrator:
    def structured_invoke(self, *, system, human, schema):
        return schema(
            primary_driver="Delta / spot move",
            verdict="Spot move dominated the session.",
            confidence_level="medium",
            confidence_rationale="Mock narrator for offline tests.",
            evidence=[],
            takeaways=["Monitor residuals and verify marks."],
            american_commentary="",
        )


class _MockVerifier:
    def __init__(
        self,
        verdicts: list[str] | None = None,
        policy_flags: list[list[str]] | None = None,
    ):
        self.verdicts = verdicts or ["PASS"]
        self.policy_flags = policy_flags or []
        self.idx = 0

    def structured_invoke(self, *, system, human, schema):
        verdict = self.verdicts[min(self.idx, len(self.verdicts) - 1)]
        flags: list[str] = []
        if self.policy_flags:
            flags = self.policy_flags[min(self.idx, len(self.policy_flags) - 1)]
        self.idx += 1
        return DiagnosticVerifierResult(
            verdict=verdict,
            missing_evidence=[],
            policy_flags=flags,
            rationale="mock verifier",
        )


def test_public_diagnose_prompt_has_no_proxy_lecture():
    text = STRUCTURED_DIAGNOSE_SYSTEM_PROMPT.lower()
    assert "hv20" not in text
    assert "proxy" not in text
    assert DEFAULT_DIAGNOSE_SYSTEM_PROMPT == STRUCTURED_DIAGNOSE_SYSTEM_PROMPT


def test_compose_appends_eval_extra():
    out = compose_diagnose_system_prompt(
        extra="If IV prev source is hv20_proxy, do not narrate a vol crush."
    )
    assert out.startswith(STRUCTURED_DIAGNOSE_SYSTEM_PROMPT)
    assert "hv20_proxy" in out


def test_extra_from_env_file():
    from tempfile import TemporaryDirectory

    old_file = os.environ.pop("EMO_DIAGNOSE_SYSTEM_EXTRA_FILE", None)
    old_inline = os.environ.pop("EMO_DIAGNOSE_SYSTEM_EXTRA", None)
    try:
        with TemporaryDirectory() as td:
            path = Path(td) / "eval.md"
            path.write_text("Do not force-fit news to proxy Vega.\n", encoding="utf-8")
            os.environ["EMO_DIAGNOSE_SYSTEM_EXTRA_FILE"] = str(path)
            assert "force-fit" in extra_from_env()
    finally:
        if old_file is not None:
            os.environ["EMO_DIAGNOSE_SYSTEM_EXTRA_FILE"] = old_file
        else:
            os.environ.pop("EMO_DIAGNOSE_SYSTEM_EXTRA_FILE", None)
        if old_inline is not None:
            os.environ["EMO_DIAGNOSE_SYSTEM_EXTRA"] = old_inline
        else:
            os.environ.pop("EMO_DIAGNOSE_SYSTEM_EXTRA", None)


def test_graph_compiles():
    app = build_graph()
    names = set(app.get_graph().nodes.keys())
    for node in ("require_openai", "leg_branch", "aggregate_book"):
        assert node in names, f"missing node {node}"
    xray_names = set(app.get_graph(xray=True).nodes.keys())
    assert any("diagnostic_pass" in x for x in xray_names)
    assert any("residual_gate" in x for x in xray_names)
    assert any("digest_news" in x for x in xray_names)
    assert any("challenge_catalyst" in x for x in xray_names)
    assert any("reconcile_debate" in x for x in xray_names)
    assert any("verify" in x for x in xray_names)


def test_pipeline_mermaid_lists_nodes():
    from explain_my_option.graph.topology import book_mermaid, leg_mermaid, pipeline_mermaid

    md = pipeline_mermaid(xray=True)
    for node in ("require_openai", "leg_branch", "diagnostic_pass", "residual_gate", "digest_news", "challenge_catalyst", "reconcile_debate", "verify"):
        assert node in md, f"missing node {node} in pipeline Mermaid"
    assert "-->" in md

    leg_md = leg_mermaid(xray=True)
    assert "react_tool_exec" in leg_md
    assert "digest_news" in leg_md
    assert "challenge_catalyst" in leg_md
    assert "reconcile_debate" in leg_md
    assert "revise_synthesis" in leg_md

    book_md = book_mermaid()
    assert "aggregate_book" in book_md


def test_pipeline_requires_openai_key_by_default():
    old_key = os.environ.pop("OPENAI_API_KEY", None)
    try:
        ok = False
        try:
            run_pipeline(ticker="AAPL", option_type="call")
        except RuntimeError as exc:
            ok = "OPENAI_API_KEY" in str(exc)
        assert ok, "run_pipeline should require OPENAI_API_KEY by default"
    finally:
        if old_key is not None:
            os.environ["OPENAI_API_KEY"] = old_key


def test_pipeline_fixture_no_network_with_mock_roles():
    old_key = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-test-not-real"
    recorder = RecordingNewsSource()
    deps = GraphDeps(
        market=FixtureMarketLoader("flat_only"),
        pnl=OfficialFdmPnlSource(config=CFG),
        planner=CueQueryPlanner(),
        intel=IntelRegistry(
            {
                "yfinance_news": recorder,
                "tavily": StubIntelSource("tavily"),
                "sec_8k": StubIntelSource("sec_8k"),
            }
        ),
    )
    roles = LlmRoleRegistry(narrator=_MockNarrator(), verifier=_MockVerifier(["PASS"]))
    cfg = PipelineConfig(
        features={"a1", "a2", "a3"},
        diag_budget=3,
        diag_iterations=2,
        verify_budget=1,
        require_openai=True,
    )
    try:
        result = run_pipeline(
            ticker="AAPL",
            option_type="call",
            deps=deps,
            roles=roles,
            config=cfg,
        )
    finally:
        if old_key is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = old_key

    assert result["snapshot"].ticker == "AAPL"
    assert result["pricing"].diagnostics.data_source == "synthetic"
    assert "diagnostic_findings" in result
    assert isinstance(result["diagnostic_findings"].get("tools_run"), list)
    assert "1-day factor PnL" in result["blotter"]
    assert result["search_plan"].queries
    assert recorder.seen, "search node should execute the plan"
    assert result["news"] and "headline" in result["news"][0].title
    assert "1-day factor PnL" in result["blotter"]
    assert "## 4. Quantitative PnL Attribution" in result["report"]
    assert "query string is not applied" in result["report"]


def test_a3_fail_exhausted_sets_terminal_break():
    old_key = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-test-not-real"
    roles = LlmRoleRegistry(
        narrator=_MockNarrator(),
        verifier=_MockVerifier(
            ["FAIL"],
            policy_flags=[["numeric_hallucination"]],
        ),
    )
    cfg = PipelineConfig(
        features={"a1", "a2", "a3"},
        diag_budget=3,
        diag_iterations=2,
        verify_budget=1,
        require_openai=True,
    )
    try:
        result = run_pipeline(
            ticker="SYN",
            option_type="call",
            deps=fixture_deps("vol_crush"),
            roles=roles,
            config=cfg,
        )
    finally:
        if old_key is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = old_key
    assert result["diagnostic_findings"].get("terminal_unexplained_break") is True


def test_fixture_deps_freezes_news():
    old_key = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "sk-test-not-real"
    roles = LlmRoleRegistry(narrator=_MockNarrator(), verifier=_MockVerifier(["PASS"]))
    cfg = PipelineConfig(
        features={"a1", "a2", "a3"},
        diag_budget=3,
        diag_iterations=2,
        verify_budget=1,
        require_openai=True,
    )
    try:
        result = run_pipeline(
            ticker="SYN",
            option_type="call",
            deps=fixture_deps("vol_crush"),
            roles=roles,
            config=cfg,
        )
    finally:
        if old_key is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = old_key
    assert result["pricing"].diagnostics.data_source == "synthetic"
    assert result["news"] == []
    assert "No corroborating headlines" in result["report"] or "Root-Cause Market Intelligence" in result["report"]


if __name__ == "__main__":
    test_public_diagnose_prompt_has_no_proxy_lecture()
    test_compose_appends_eval_extra()
    test_extra_from_env_file()
    test_graph_compiles()
    test_pipeline_mermaid_lists_nodes()
    test_pipeline_requires_openai_key_by_default()
    test_pipeline_fixture_no_network_with_mock_roles()
    test_a3_fail_exhausted_sets_terminal_break()
    test_fixture_deps_freezes_news()
    print("OK — agent graph checks passed")
