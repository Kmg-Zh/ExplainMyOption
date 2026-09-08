"""Loose headline pre-filter before LLM relevance digestion."""

from __future__ import annotations

import re

_DROP_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\boptions?\s+strategy\b", re.IGNORECASE),
    re.compile(r"\bhow to position\b", re.IGNORECASE),
    re.compile(r"\bmoomoo\s+community\b", re.IGNORECASE),
)


def coarse_keep(title: str) -> bool:
    """Cheap prefilter: drop empty and obvious promo spam only."""
    text = (title or "").strip()
    if not text:
        return False
    for pat in _DROP_PATTERNS:
        if pat.search(text):
            return False
    return True
