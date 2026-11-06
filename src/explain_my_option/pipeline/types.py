"""Shared pipeline typed states/results."""

from __future__ import annotations

from typing import Any, TypedDict

from ..report import PositionBundle
from ..report.settlement import ExpirySettlement


class LegResult(TypedDict, total=False):
    leg_id: str
    ok: bool
    error: str | None
    # A diagnosed leg has a bundle; a leg settled at expiry has a settlement instead.
    bundle: PositionBundle | None
    settlement: ExpirySettlement | None
    synthesis: dict[str, Any] | None
    diagnostic_findings: dict[str, Any]
    report: str
    blotter: str
    diagnosis: str
    stage_timings: dict[str, float]
    llm_calls: int | None
    no_escalation: bool
    terminal_no_comparable_observation: bool
