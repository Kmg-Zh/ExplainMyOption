"""Provider-neutral LLM roles for narrator / digest / challenger / verifier."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LlmRole(Protocol):
    def structured_invoke(
        self,
        *,
        system: str,
        human: str,
        schema: type[T],
    ) -> T: ...


@dataclass
class OpenAiRole:
    model: str
    temperature: float = 0.0
    timeout: float = 45.0
    # B3: fixed seed for the OpenAI API's own `seed` param (best-effort
    # determinism on the provider side -- OpenAI does not guarantee
    # bit-identical output even with temperature=0 and a fixed seed, only
    # that the same seed+params combination is more likely to reproduce).
    seed: int = 0

    def structured_invoke(
        self,
        *,
        system: str,
        human: str,
        schema: type[T],
    ) -> T:
        from langchain_core.messages import HumanMessage, SystemMessage
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            timeout=self.timeout,
            seed=self.seed,
        )
        structured = llm.with_structured_output(schema)
        result = structured.invoke(
            [SystemMessage(content=system), HumanMessage(content=human)]
        )
        if isinstance(result, schema):
            return result
        return schema.model_validate(result)

    def run_metadata(self) -> dict:
        return {
            "model": self.model,
            "temperature": self.temperature,
            "seed": self.seed,
        }


@dataclass
class LlmRoleRegistry:
    narrator: LlmRole
    verifier: LlmRole
    challenger: LlmRole | None = None
    digester: LlmRole | None = None


def default_openai_roles() -> LlmRoleRegistry:
    model = os.getenv("EMO_LLM_MODEL", "gpt-5.4-mini")
    verifier_model = os.getenv("EMO_VERIFIER_MODEL", model)
    digester_model = os.getenv("EMO_DIGEST_MODEL", model)
    return LlmRoleRegistry(
        narrator=OpenAiRole(model=model),
        verifier=OpenAiRole(model=verifier_model),
        challenger=OpenAiRole(model=os.getenv("EMO_CHALLENGER_MODEL", model)),
        digester=OpenAiRole(model=digester_model),
    )


def llm_run_metadata(registry: LlmRoleRegistry) -> dict:
    """B3: model string, temperature, and seed for every configured role, in
    one place, for the run manifest. Roles that are not ``OpenAiRole`` (mocks
    in offline/CI runs) are recorded by type name only, no fabricated params."""

    def _one(role) -> dict | None:
        if role is None:
            return None
        if isinstance(role, OpenAiRole):
            return role.run_metadata()
        return {"role_type": type(role).__name__}

    return {
        "narrator": _one(registry.narrator),
        "verifier": _one(registry.verifier),
        "challenger": _one(registry.challenger),
        "digester": _one(registry.digester),
    }


def require_openai_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "Showcase runs require OPENAI_API_KEY (set EMO_SHOWCASE_REQUIRE_KEY=0 to override)."
        )
