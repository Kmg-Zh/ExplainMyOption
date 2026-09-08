"""Coarse promo filter + LLM digest that *labels* headlines (not a ticker gate)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..data_loader import NewsItem
from ..intel.relevance import coarse_keep
from ..report.catalysts import (
    CATALYST_TAGS,
    MICROSTRUCTURE_TAGS,
    normalize_catalyst_tags,
    tags_from_headlines,
    with_inferred_microstructure,
)
from .llm_roles import LlmRole


class DigestRelevantItem(BaseModel):
    title: str
    publisher: str = ""
    mechanisms: list[str] = Field(default_factory=list, max_length=6)
    one_line_fact: str = ""


class DigestDiscardedItem(BaseModel):
    title: str
    reason: str = ""


class IntelDigest(BaseModel):
    relevant: list[DigestRelevantItem] = Field(default_factory=list, max_length=5)
    background: list[DigestRelevantItem] = Field(default_factory=list, max_length=5)
    discarded: list[DigestDiscardedItem] = Field(default_factory=list, max_length=10)
    mechanisms: list[str] = Field(default_factory=list, max_length=8)
    brief: str = ""
    reason: str = ""


INTEL_DIGEST_SYSTEM_PROMPT = """You are a desk intel triage analyst for options PnL explain.
Quant / Layer A is already computed upstream. Your output is IntelDigest JSON only.
You label headlines as background for that PnL story — you do not decide the PnL.

Task:
1) Classify each headline as relevant, background, or discarded for the target ticker.
2) Extract mechanisms from relevant headlines only, using this allow-list exactly:
   iv crush, borrow, squeeze, float, buy-in, earnings, ex-dividend, conversion.
3) Write a factual brief (1-2 sentences) describing what you labeled. Do not claim
   the tape is empty when headlines remain.

Classification:
- relevant: the target name (ticker, company name, common abbreviation, listing
  variant) OR a related issuer / control-structure story (acquisition, stake,
  domination, squeeze that names the target).
- background: peer, competitor, or sector tape that can indirectly affect the
  name. Keep these. Do not treat them as proof the residual *is* that peer event.
  Do not attach mechanism tags to background items.
- discarded: leftover promo or clearly unrelated noise only.

Rules:
- Infer the company from the ticker yourself. Do not require the ticker string
  to appear in the title.
- If uncertain, keep (prefer background over discard).
- Do not include PnL attribution, option-pricing numbers, or trading advice.
- Mechanisms must only use the allow-list labels exactly, and only on relevant."""


def empty_digest(*, reason: str = "") -> IntelDigest:
    return IntelDigest(
        relevant=[],
        background=[],
        discarded=[],
        mechanisms=[],
        brief="",
        reason=reason,
    )


def coarse_kept_news(news: list[NewsItem]) -> list[NewsItem]:
    """Headlines that survive the promo/empty coarse filter."""
    return [hit for hit in news if coarse_keep(hit.title)]


def _coarse_partition(news: list[NewsItem]) -> tuple[list[NewsItem], list[DigestDiscardedItem]]:
    kept: list[NewsItem] = []
    dropped: list[DigestDiscardedItem] = []
    for hit in news:
        if coarse_keep(hit.title):
            kept.append(hit)
            continue
        dropped.append(
            DigestDiscardedItem(
                title=hit.title,
                reason="coarse filter: empty/promotional headline",
            )
        )
    return kept, dropped


def _title_key(title: str) -> str:
    return (title or "").strip().lower()


def _item_from_source(
    source: NewsItem,
    row: DigestRelevantItem,
    *,
    keep_mechanisms: bool,
) -> DigestRelevantItem:
    return DigestRelevantItem(
        title=source.title,
        publisher=source.publisher or row.publisher,
        mechanisms=normalize_catalyst_tags(row.mechanisms) if keep_mechanisms else [],
        one_line_fact=(row.one_line_fact or "").strip(),
    )


def _default_brief(*, relevant: list[DigestRelevantItem], background: list[DigestRelevantItem]) -> str:
    if relevant:
        return "Relevant headlines were retained as Layer B background."
    if background:
        return "Peer or sector headlines retained as indirect background."
    return "Headlines were labeled; none were tagged as ticker-relevant catalysts."


def _post_process_digest(
    *,
    digest: IntelDigest,
    coarse_kept: list[NewsItem],
    coarse_dropped: list[DigestDiscardedItem],
) -> IntelDigest:
    by_title: dict[str, NewsItem] = {
        _title_key(item.title): item for item in coarse_kept if item.title
    }
    seen: set[str] = set()

    relevant: list[DigestRelevantItem] = []
    for row in digest.relevant:
        key = _title_key(row.title)
        if not key or key not in by_title or key in seen:
            continue
        relevant.append(_item_from_source(by_title[key], row, keep_mechanisms=True))
        seen.add(key)

    background: list[DigestRelevantItem] = []
    for row in digest.background:
        key = _title_key(row.title)
        if not key or key not in by_title or key in seen:
            continue
        background.append(_item_from_source(by_title[key], row, keep_mechanisms=False))
        seen.add(key)

    discarded = list(coarse_dropped)
    for row in digest.discarded:
        key = _title_key(row.title)
        if not key or key in seen:
            continue
        if any(_title_key(d.title) == key for d in discarded):
            continue
        title = by_title[key].title if key in by_title else row.title
        discarded.append(
            DigestDiscardedItem(
                title=title,
                reason=(row.reason or "unrelated noise").strip(),
            )
        )
        seen.add(key)

    # Unclassified kept titles stay visible as background (keep-if-uncertain).
    for item in coarse_kept:
        key = _title_key(item.title)
        if not key or key in seen:
            continue
        background.append(
            DigestRelevantItem(
                title=item.title,
                publisher=item.publisher,
                mechanisms=[],
                one_line_fact="",
            )
        )
        seen.add(key)

    # Digest miss: promote microstructure named in the visible tape so a squeeze
    # / float headline is not treated as invention. Do not promote generic
    # earnings / ex-div from unclassified peer mixes.
    if not relevant:
        still_background: list[DigestRelevantItem] = []
        for item in background:
            scanned = [
                tag
                for tag in tags_from_headlines([item.title])
                if tag in MICROSTRUCTURE_TAGS
            ]
            if scanned:
                relevant.append(
                    item.model_copy(update={"mechanisms": scanned})
                )
            else:
                still_background.append(item)
        background = still_background

    mechanisms = with_inferred_microstructure(
        [m for item in relevant for m in item.mechanisms]
    )
    brief = (digest.brief or "").strip() or _default_brief(relevant=relevant, background=background)
    return IntelDigest(
        relevant=relevant[:5],
        background=background[:5],
        discarded=discarded[:10],
        mechanisms=mechanisms,
        brief=brief,
        reason=digest.reason,
    )


def run_intel_digest(
    *,
    role: LlmRole | None,
    ticker: str,
    news: list[NewsItem],
) -> IntelDigest:
    if not news:
        return empty_digest(reason="no headlines retrieved")
    kept, coarse_dropped = _coarse_partition(news)
    if not kept:
        return empty_digest(reason="coarse filter removed all headlines").model_copy(
            update={"discarded": coarse_dropped[:10]}
        )
    if role is None:
        return _post_process_digest(
            digest=empty_digest(reason="digester role not configured"),
            coarse_kept=kept,
            coarse_dropped=coarse_dropped,
        )
    lines = [
        "Return IntelDigest JSON only.",
        f"Target ticker: {ticker.upper()}",
        "Match company names, common abbreviations, listing variants, and related issuers yourself.",
        f"Allowed mechanisms (relevant headlines only): {', '.join(CATALYST_TAGS)}",
        "Headlines:",
    ]
    for idx, hit in enumerate(kept[:8], 1):
        pub = hit.publisher or "?"
        lines.append(f"{idx}. {hit.title} ({pub})")
    human = "\n".join(lines)
    try:
        raw = role.structured_invoke(
            system=INTEL_DIGEST_SYSTEM_PROMPT,
            human=human,
            schema=IntelDigest,
        )
        digest = raw if isinstance(raw, IntelDigest) else IntelDigest.model_validate(raw)
        return _post_process_digest(
            digest=digest,
            coarse_kept=kept,
            coarse_dropped=coarse_dropped,
        )
    except Exception:
        # Fail soft: keep coarse titles visible; microstructure promotion may
        # still label squeeze/float named in the tape (not peer earnings).
        return _post_process_digest(
            digest=empty_digest(reason="digest invoke failed"),
            coarse_kept=kept,
            coarse_dropped=coarse_dropped,
        )
