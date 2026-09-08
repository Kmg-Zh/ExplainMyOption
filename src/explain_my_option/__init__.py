"""Explain My Option — diagnose why an equity option price moved."""

from __future__ import annotations

from .agent_graph import build_graph, run_pipeline
from .api import DiagnoseResult, ExplainMyOption
from .pipeline.config import PipelineConfig

__version__ = "0.1.0"

__all__ = [
    "DiagnoseResult",
    "ExplainMyOption",
    "PipelineConfig",
    "build_graph",
    "run_pipeline",
    "__version__",
]
