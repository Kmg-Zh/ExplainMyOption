"""Validate market fixture JSON contracts (test-only)."""

from __future__ import annotations

import json
from pathlib import Path

from explain_my_option.data.synthetic import _REQUIRED_SNAPSHOT_KEYS
from explain_my_option.paths import FIXTURES_DIR


def validate_fixture_file(path: Path) -> list[str]:
    """Return list of validation errors (empty if OK)."""
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.name}: invalid JSON ({exc})"]
    if not isinstance(payload, dict):
        return [f"{path.name}: root must be an object"]
    if "snapshot" not in payload:
        return []  # manifest or non-market file
    snap = payload["snapshot"]
    if not isinstance(snap, dict):
        return [f"{path.name}: snapshot must be an object"]
    missing = [k for k in _REQUIRED_SNAPSHOT_KEYS if k not in snap]
    if missing:
        errors.append(f"{path.name}: snapshot missing {missing}")
    return errors


def validate_all_fixtures(*, fixtures_root: Path | None = None) -> list[str]:
    root = fixtures_root or FIXTURES_DIR
    all_errors: list[str] = []
    for path in sorted(root.glob("*.json")):
        all_errors.extend(validate_fixture_file(path))
    return all_errors
