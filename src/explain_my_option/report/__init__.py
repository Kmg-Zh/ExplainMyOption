"""Diagnostic report assembly: facts, blotter, narrative synthesis, template."""

from .facts import PositionBundle, build_portfolio_facts, build_position_facts
from .schema import DiagnosticSynthesis
from .synthesis import fallback_synthesis, synthesize_diagnosis
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
    "synthesize_diagnosis",
    "validate_synthesis",
]
