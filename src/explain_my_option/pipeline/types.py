"""Shared pipeline typed states/results."""

from __future__ import annotations

from typing import Any, TypedDict

from ..report import PositionBundle


class LegResult(TypedDict, total=False):
    leg_id: str
    ok: bool
    error: str | None
    bundle: PositionBundle | None
    synthesis: dict[str, Any] | None
    diagnostic_findings: dict[str, Any]
    report: str
    blotter: str
    diagnosis: str
