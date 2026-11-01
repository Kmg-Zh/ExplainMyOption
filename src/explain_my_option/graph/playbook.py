"""Playbook records: fixed narrator guidance for special cases, selected by code.

A record is selected when a diagnostic finding it names is true, and its text
goes into the narrator's prompt for that leg. It never changes the search plan,
the tools or the routing. The text is held to the narrator's own rules (no
figures, no trade or hedge wording) and names no pricing engine, since a desk
may bring its own. Bundled records also name no event: a historical eval must
not be passable by copying a record (``tests/agent/test_playbook.py``).

A desk adds its own records through ``GraphDeps(playbook=(*DEFAULT_PLAYBOOK, ...))``;
``check_playbook`` runs when the deps are built.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from typing import Iterable, Sequence

_ENGINE_NAME_RE = re.compile(
    r"\b(quantlib|fdm|finite[- ]difference|dupire|local[- ]vol\w*|heston|lsm|merton|black[- ]scholes)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class PlaybookRecord:
    """``when`` names a boolean diagnostic finding; the record applies when it is true."""

    record_id: str
    when: str
    title: str
    guidance: str


TERMINAL_BREAK = PlaybookRecord(
    record_id="terminal-break",
    when="terminal_unexplained_break",
    title="The attribution does not explain this move",
    guidance=(
        "The diagnostic pass used its budget and a large part of this move is still unexplained. "
        "The verdict must say so plainly: the attribution does not explain this move, and the story "
        "needs human review. Keep the Layer A sentence, but do not present a Greek or a headline as "
        "the full explanation. Name any headline mechanisms the code lists as context the "
        "attribution has not confirmed, not as the cause. confidence_rationale must say the gap is "
        "unexplained."
    ),
)

DEFAULT_PLAYBOOK: tuple[PlaybookRecord, ...] = (TERMINAL_BREAK,)


def finding_triggers() -> frozenset[str]:
    """The diagnostic findings a record may name: the boolean ones."""
    from .diagnostic_controller import DiagnosticFindings

    return frozenset(f.name for f in fields(DiagnosticFindings) if f.type == "bool")


def record_errors(record: PlaybookRecord) -> list[str]:
    from ..report.validate import advice_wording_hits

    errors: list[str] = []
    if not record.record_id.strip():
        errors.append("record_id is empty")
    if record.when not in finding_triggers():
        errors.append(f"`when` must be one of {sorted(finding_triggers())}, not {record.when!r}")
    text = f"{record.title}\n{record.guidance}"
    if not record.guidance.strip():
        errors.append("guidance is empty")
    if re.search(r"\d", text):
        errors.append("text must not contain digits (figures or dates)")
    advice = advice_wording_hits(text)
    if advice:
        errors.append(f"trade or hedge wording: {', '.join(advice)}")
    engines = sorted({m.group(1).lower() for m in _ENGINE_NAME_RE.finditer(text)})
    if engines:
        errors.append(f"names a pricing engine: {', '.join(engines)}")
    return errors


def check_playbook(records: Iterable[PlaybookRecord]) -> None:
    """Raise ValueError naming every record that breaks the rules above."""
    records = tuple(records)
    problems = [f"{r.record_id or '?'}: {e}" for r in records for e in record_errors(r)]
    ids = [r.record_id for r in records]
    problems += [f"{i}: duplicate record_id" for i in sorted({i for i in ids if ids.count(i) > 1})]
    if problems:
        raise ValueError("invalid playbook record(s): " + "; ".join(problems))


def select_records(findings: dict | None, playbook: Sequence[PlaybookRecord]) -> list[PlaybookRecord]:
    findings = findings or {}
    return [record for record in playbook if findings.get(record.when) is True]


def playbook_prompt_lines(records: Sequence[PlaybookRecord]) -> list[str]:
    if not records:
        return []
    lines = ["", "### Playbook (selected by code for this case; follow each record)"]
    lines.extend(f"- **{r.title}** (`{r.record_id}`): {r.guidance}" for r in records)
    return lines
