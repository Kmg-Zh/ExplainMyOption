"""Provider-neutral LLM roles: narrator, digester, catalyst critic, verifier."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

DEFAULT_LLM_MODEL = "gpt-5.4-mini"


class LlmUnavailable(RuntimeError):
    """The role has no credentials, so no call was attempted."""


class LlmRole(Protocol):
    def structured_invoke(self, *, system: str, human: str, schema: type[T]) -> T: ...


@dataclass
class OpenAiRole:
    model: str
    temperature: float = 0.0
    timeout: float = 45.0
    # Sent as OpenAI's ``seed``: best-effort determinism, not a guarantee.
    seed: int = 0
    # Token usage of the most recent call, for cost accounting.
    last_usage: dict | None = field(default=None, init=False, repr=False, compare=False)

    def structured_invoke(self, *, system: str, human: str, schema: type[T]) -> T:
        if not os.getenv("OPENAI_API_KEY"):
            raise LlmUnavailable("OPENAI_API_KEY is not set")
        from langchain_core.messages import HumanMessage, SystemMessage
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model=self.model, temperature=self.temperature, timeout=self.timeout, seed=self.seed)
        raw_result = llm.with_structured_output(schema, include_raw=True).invoke(
            [SystemMessage(content=system), HumanMessage(content=human)]
        )
        raw_msg = raw_result.get("raw")
        usage = getattr(raw_msg, "usage_metadata", None) if raw_msg is not None else None
        self.last_usage = dict(usage) if usage else None
        parsed = raw_result.get("parsed")
        if parsed is None:
            raise RuntimeError(f"{self.model}: structured parse failed: {raw_result.get('parsing_error')}")
        return parsed if isinstance(parsed, schema) else schema.model_validate(parsed)

    def run_metadata(self) -> dict:
        return {"model": self.model, "temperature": self.temperature, "seed": self.seed}


@dataclass
class LlmRoleRegistry:
    narrator: LlmRole
    verifier: LlmRole
    challenger: LlmRole | None = None
    digester: LlmRole | None = None


def default_openai_roles() -> LlmRoleRegistry:
    model = os.getenv("EMO_LLM_MODEL", DEFAULT_LLM_MODEL)
    return LlmRoleRegistry(
        narrator=OpenAiRole(model=model),
        verifier=OpenAiRole(model=os.getenv("EMO_VERIFIER_MODEL", model)),
        challenger=OpenAiRole(model=os.getenv("EMO_CHALLENGER_MODEL", model)),
        digester=OpenAiRole(model=os.getenv("EMO_DIGEST_MODEL", model)),
    )


def llm_run_metadata(registry: LlmRoleRegistry) -> dict:
    """Model, temperature and seed per role for a run manifest. Non-OpenAI
    roles (offline mocks) are recorded by type name only."""

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
