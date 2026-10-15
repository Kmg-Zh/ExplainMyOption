"""Runtime switches for the diagnosis pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class PipelineConfig:
    # Run the verifier role on the narrator's synthesis. Off only for evals
    # that score the raw narrator.
    verify: bool = True
    # Refuse to start without OPENAI_API_KEY (the product default).
    require_openai: bool = True

    @classmethod
    def from_env(cls) -> PipelineConfig:
        return cls(require_openai=os.getenv("EMO_PIPELINE_REQUIRE_KEY", "1") != "0")
