"""Public facade for Explain My Option."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from .agent_graph import run_pipeline
from .data.synthetic import load_fixture
from .graph.deps import FixtureMarketLoader, GraphDeps, fixture_deps
from .pipeline.book_schema import BookSpec, load_book_json
from .pipeline.config import PipelineConfig
from .pipeline.llm_roles import LlmRoleRegistry
from .pipeline.portfolio_graph import run_book_pipeline


@dataclass(frozen=True)
class DiagnoseResult:
    """Outcome of a single diagnose run."""

    report: str
    blotter: str
    state: dict[str, Any]

    @property
    def report_markdown(self) -> str:
        return self.report


class ExplainMyOption:
    """Stable entrypoint for leg/book/fixture diagnosis."""

    def __init__(
        self,
        *,
        config: PipelineConfig | None = None,
        deps: GraphDeps | None = None,
        roles: LlmRoleRegistry | None = None,
    ) -> None:
        self.config = config or PipelineConfig.from_env()
        self.deps = deps
        self.roles = roles

    def diagnose_leg(
        self,
        ticker: str,
        *,
        option_type: str = "call",
        strike: Optional[float] = None,
        expiry: Optional[str] = None,
        quantity: float = 1.0,
        multiplier: float = 1.0,
    ) -> DiagnoseResult:
        state = run_pipeline(
            ticker,
            option_type=option_type,
            strike=strike,
            expiry=expiry,
            quantity=quantity,
            multiplier=multiplier,
            deps=self.deps,
            config=self.config,
            roles=self.roles,
        )
        return DiagnoseResult(
            report=str(state.get("report", "")),
            blotter=str(state.get("blotter", "")),
            state=dict(state),
        )

    def diagnose_book(self, book: BookSpec | str | Path) -> dict[str, Any]:
        if not isinstance(book, BookSpec):
            book = load_book_json(book)
        return dict(
            run_book_pipeline(
                book,
                config=self.config,
                deps=self.deps,
                roles=self.roles,
            )
        )

    def diagnose_fixture(self, name: str) -> DiagnoseResult:
        snap, _ = load_fixture(name)
        deps = self.deps or fixture_deps(name)
        if self.deps is not None:
            deps = GraphDeps(
                market=FixtureMarketLoader(name),
                pnl=self.deps.pnl,
                planner=self.deps.planner,
                intel=self.deps.intel,
                diagnose_system_prompt=self.deps.diagnose_system_prompt,
                diagnose_system_extra=self.deps.diagnose_system_extra,
            )
        state = run_pipeline(
            snap.ticker,
            option_type=snap.option_type,
            strike=snap.strike,
            expiry=snap.expiry,
            quantity=snap.quantity,
            multiplier=snap.multiplier,
            deps=deps,
            config=self.config,
            roles=self.roles,
        )
        return DiagnoseResult(
            report=str(state.get("report", "")),
            blotter=str(state.get("blotter", "")),
            state=dict(state),
        )
