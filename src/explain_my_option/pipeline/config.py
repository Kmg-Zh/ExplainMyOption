"""Runtime knobs for unified diagnostic loop/verifier behavior."""

from __future__ import annotations

import os
from dataclasses import dataclass, field


def _features_from_env() -> set[str]:
    raw = (
        os.getenv("EMO_PIPELINE_FEATURES")
        or os.getenv("EMO_SHOWCASE_FEATURES")
        or "a1,a2,a3"
    )
    return {x.strip().lower() for x in raw.split(",") if x.strip()}


@dataclass
class PipelineConfig:
    features: set[str] = field(default_factory=_features_from_env)
    diag_budget: int = 3
    diag_iterations: int = 2
    verify_budget: int = 1
    require_openai: bool = True

    @classmethod
    def from_env(cls) -> PipelineConfig:
        return cls(
            features=_features_from_env(),
            diag_budget=int(os.getenv("EMO_DIAG_BUDGET", "3")),
            diag_iterations=int(os.getenv("EMO_DIAG_ITERATIONS", "2")),
            verify_budget=int(os.getenv("EMO_VERIFY_BUDGET", "1")),
            require_openai=os.getenv(
                "EMO_PIPELINE_REQUIRE_KEY",
                os.getenv("EMO_SHOWCASE_REQUIRE_KEY", "1"),
            )
            != "0",
        )

    def enabled(self, feature: str) -> bool:
        return feature.lower() in self.features
