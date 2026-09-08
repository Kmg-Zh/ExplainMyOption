from pydantic import BaseModel, Field
from typing import Literal

VerifierVerdict = Literal["PASS", "PARTIAL", "FAIL"]


class DiagnosticVerifierResult(BaseModel):
    verdict: VerifierVerdict
    missing_evidence: list[str] = Field(default_factory=list)
    policy_flags: list[str] = Field(default_factory=list)
    rationale: str = ""
