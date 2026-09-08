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
        )
        structured = llm.with_structured_output(schema)
        result = structured.invoke(
            [SystemMessage(content=system), HumanMessage(content=human)]
        )
        if isinstance(result, schema):
            return result
        return schema.model_validate(result)


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


def require_openai_key() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "Showcase runs require OPENAI_API_KEY (set EMO_SHOWCASE_REQUIRE_KEY=0 to override)."
        )
