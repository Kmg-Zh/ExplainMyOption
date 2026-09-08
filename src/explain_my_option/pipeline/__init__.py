"""Compatibility namespace for unified book/leg graph components."""

from .config import PipelineConfig
from .runner import run_book_from_fixture_path

__all__ = ["PipelineConfig", "run_book_from_fixture_path"]
