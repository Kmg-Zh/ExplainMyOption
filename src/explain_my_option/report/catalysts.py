"""Headline mechanism tags for Layer B (code scan — not LLM invention).

Used by the diagnose human prompt and the verifier precheck so dual-factor
days (gap + IV crush, squeeze/borrow) are not dropped when Delta dominates Taylor.
"""

from __future__ import annotations

from typing import Sequence

from ..data_loader import NewsItem

# (tag, tokens that mean the headline contains this mechanism,
#  tokens that mean the narrative already covered it)
_GROUPS: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = [
    (
        "iv crush",
        (
            "iv crush",
            "volatility crush",
            "vol crush",
            "implied volatility collapsed",
            "implied vol",
        ),
        (
            "iv crush",
            "volatility crush",
            "vol crush",
            "implied volatility",
            "iv normalization",
        ),
    ),
    (
        "borrow",
        ("borrow", "hard-to-borrow", "hard to borrow", "htb", "securities lending"),
        ("borrow", "hard-to-borrow", "hard to borrow", "htb"),
    ),
    (
        "squeeze",
        ("short squeeze", "short interest", "squeeze"),
        ("squeeze", "short interest"),
    ),
    (
        "float",
        ("free float", "cornered market", "corner"),
        ("free float", "float", "cornered", "corner"),
    ),
    (
        "buy-in",
        ("buy-in", "buy in", "recall"),
        ("buy-in", "buy in", "recall", "liquidity"),
    ),
    (
        "earnings",
        ("earnings", "guidance"),
        ("earnings", "guidance"),
    ),
    (
        "ex-dividend",
        ("ex-dividend", "ex-div", "dividend"),
        ("ex-div", "ex-dividend", "dividend", "early exercise", "assignment"),
    ),
    (
        "conversion",
        ("conversion", "put-call parity", "synthetic dividend"),
        ("conversion", "parity", "synthetic"),
    ),
]

CATALYST_TAGS: tuple[str, ...] = tuple(tag for tag, _h, _n in _GROUPS)

# Named in as-of tape even when digest.relevant is empty. Earnings / ex-div are
# too common in peer Yahoo mixes to promote from unclassified titles.
MICROSTRUCTURE_TAGS: frozenset[str] = frozenset(
    {"squeeze", "float", "borrow", "buy-in", "conversion", "iv crush"}
)


def _blob(parts: Sequence[str]) -> str:
    return " ".join(p for p in parts if p).lower()


def tags_from_headlines(titles: Sequence[str]) -> list[str]:
    """Stable tag list for mechanisms present in news titles."""
    text = _blob(list(titles))
    found: list[str] = []
    for tag, headline_tokens, _narrative in _GROUPS:
        if any(tok in text for tok in headline_tokens):
            found.append(tag)
    return found


def tags_from_news(news: Sequence[NewsItem]) -> list[str]:
    return tags_from_headlines([n.title for n in news])


def normalize_catalyst_tags(tags: Sequence[str]) -> list[str]:
    """Clamp arbitrary labels to the allow-list used by reports/verifier."""
    allowed = set(CATALYST_TAGS)
    out: list[str] = []
    seen: set[str] = set()
    for raw in tags:
        label = str(raw).strip().lower()
        if not label or label not in allowed or label in seen:
            continue
        out.append(label)
        seen.add(label)
    return out


def with_inferred_microstructure(tags: Sequence[str]) -> list[str]:
    """Desk-inferable overlays from as-of tape — no prices, no later-paper jargon.

    Short squeeze / maxed float → borrow stress (FDM does not model HTB).
    Collapsed free float / corner → squeeze (same unmodeled microstructure).
    """
    present = normalize_catalyst_tags(tags)
    extra: list[str] = []
    if "squeeze" in present and "borrow" not in present:
        extra.append("borrow")
    if "float" in present and "squeeze" not in present:
        extra.append("squeeze")
    return normalize_catalyst_tags([*present, *extra])


def missing_catalyst_tags(narrative: str, titles: Sequence[str]) -> list[str]:
    """Tags present in headlines but absent from synthesis prose."""
    present = tags_from_headlines(titles)
    if not present:
        return []
    body = narrative.lower()
    missing: list[str] = []
    lookup = {tag: narrative_tokens for tag, _h, narrative_tokens in _GROUPS}
    for tag in present:
        tokens = lookup[tag]
        if not any(tok in body for tok in tokens):
            missing.append(tag)
    return missing
