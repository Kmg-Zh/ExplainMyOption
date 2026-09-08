"""Industrial diagnostic report assembly."""

from .facts import PositionBundle, build_position_facts, build_portfolio_facts
from .schema import DiagnosticSynthesis
from .synthesis import fallback_synthesis, synthesize_diagnosis, synthesis_to_legacy_diagnosis
from .template import render_portfolio_report, render_position_report
from .validate import validate_synthesis

__all__ = [
    "DiagnosticSynthesis",
    "PositionBundle",
    "build_portfolio_facts",
    "build_position_facts",
    "fallback_synthesis",
    "render_portfolio_report",
    "render_position_report",
    "validate_synthesis",
    "synthesize_diagnosis",
    "synthesis_to_legacy_diagnosis",
]
