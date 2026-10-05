from pydantic import BaseModel, Field
from typing import Literal

VerifierVerdict = Literal["PASS", "PARTIAL", "FAIL"]


class DiagnosticVerifierResult(BaseModel):
    """What the verifier LLM is asked to return (the structured-output schema)."""

    verdict: VerifierVerdict
    missing_evidence: list[str] = Field(default_factory=list)
    policy_flags: list[str] = Field(default_factory=list)
    rationale: str = ""


class GuardedVerifierResult(DiagnosticVerifierResult):
    """LLM verdict after the code-confirmation guard (never shown to the LLM).

    The two extra fields are written by code: when the LLM raised a hard FAIL
    that code could not confirm, the verdict is downgraded to PARTIAL and the
    LLM's original verdict/flags are kept here for the audit trail."""

    llm_verdict: VerifierVerdict | None = None
    llm_policy_flags: list[str] = Field(default_factory=list)
