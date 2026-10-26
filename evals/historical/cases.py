"""Shared historical anomaly benchmark cases (test-only).

Used by the historical eval runner, compare path, and prompt tests.

Lineage: agent-visible news is ``as_of_news`` only (``published <= case.date``).
Post-event papers, explainers, and the human ``input_text`` scenario note are
``ground_truth`` / eval rubric — never injected into the graph or baseline packet.

Pass/fail only uses causes a contemporaneous desk could reasonably infer from
the blotter plus as-of tape. Hindsight-only labels (later papers) are scored as
oracle coverage, not a hard bar. Live LLM weights may still contain those events;
that parametric leakage is flagged, not removed.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from explain_my_option.data_loader import NewsItem
from explain_my_option.paths import HISTORICAL_DIR, REPO_ROOT

_LOCAL_MEMO_DIR = REPO_ROOT / "private" / "eval" / "historical-memos"


def resolve_memo_path(case: "BenchmarkCase"):
    """Author-local desk memos; missing on a public clone is fine."""
    if not case.memo:
        return None
    name = Path(case.memo).name
    for path in (HISTORICAL_DIR / case.memo, _LOCAL_MEMO_DIR / name):
        if path.is_file():
            return path
    return None

CASE_PATH = HISTORICAL_DIR / "historical_test_cases.json"

PARAMETRIC_KNOWLEDGE_CAVEAT = (
    "Live LLMs are trained after these events. Stripping future news from the "
    "prompt does not remove that history from the weights. Hindsight hits "
    "(Avellaneda, SEC staff report, next-day recaps) may be parametric leakage; "
    "they are measured, not required to pass."
)


@dataclass(frozen=True)
class BenchmarkCase:
    test_id: str
    ticker: str
    date: str
    input_quant: dict[str, Any]
    input_text: str
    expected_root_cause_keywords: list[str]
    expected_action_items: list[str]
    tier: str = "B"
    tier_label: str = ""
    references: list[dict[str, str]] = field(default_factory=list)
    expected_keyword_groups: list[list[str]] = field(default_factory=list)
    min_keyword_groups_hit: int = 1
    expected_action_themes: list[str] = field(default_factory=list)
    min_action_themes_hit: int = 1
    as_of_news: list[dict[str, Any]] = field(default_factory=list)
    ground_truth: list[dict[str, Any]] = field(default_factory=list)
    hindsight_keyword_group_labels: list[str] = field(default_factory=list)
    hindsight_action_themes: list[str] = field(default_factory=list)
    hindsight_leak_markers: list[str] = field(default_factory=list)
    memo: str = ""
    eval_dimensions: dict[str, Any] = field(default_factory=dict)

    @property
    def fixture(self) -> str:
        return str(self.input_quant["fixture"])

    @property
    def min_residual_ratio(self) -> float:
        return float(self.input_quant.get("min_residual_ratio", 0.0))

    def as_of_date(self) -> date:
        return date.fromisoformat(self.date)

    def keyword_groups(self) -> list[list[str]]:
        if self.expected_keyword_groups:
            return list(self.expected_keyword_groups)
        return [[kw] for kw in self.expected_root_cause_keywords]

    def action_themes(self) -> list[str]:
        if self.expected_action_themes:
            return list(self.expected_action_themes)
        return list(self.expected_action_items)

    def _hindsight_label_set(self) -> set[str]:
        return {label.lower() for label in self.hindsight_keyword_group_labels}

    def required_keyword_groups(self) -> list[list[str]]:
        """Causes a desk could reasonably infer from as-of tape + blotter."""
        hidden = self._hindsight_label_set()
        return [group for group in self.keyword_groups() if group[0].lower() not in hidden]

    def hindsight_keyword_groups(self) -> list[list[str]]:
        """Oracle / later-paper causes. Measured, not required to pass."""
        hidden = self._hindsight_label_set()
        return [group for group in self.keyword_groups() if group[0].lower() in hidden]

    def required_action_themes(self) -> list[str]:
        hidden = {theme.lower() for theme in self.hindsight_action_themes}
        return [theme for theme in self.action_themes() if theme.lower() not in hidden]


def load_cases() -> list[BenchmarkCase]:
    rows = json.loads(CASE_PATH.read_text(encoding="utf-8"))
    return [
        BenchmarkCase(
            test_id=str(row["test_id"]),
            ticker=str(row["ticker"]),
            date=str(row["date"]),
            input_quant=dict(row["input_quant"]),
            input_text=str(row["input_text"]),
            expected_root_cause_keywords=list(row["expected_root_cause_keywords"]),
            expected_action_items=list(row["expected_action_items"]),
            tier=str(row.get("tier", "B")),
            tier_label=str(row.get("tier_label", "")),
            references=list(row.get("references", [])),
            expected_keyword_groups=[
                list(group) for group in row.get("expected_keyword_groups", [])
            ],
            min_keyword_groups_hit=int(row.get("min_keyword_groups_hit", 1)),
            expected_action_themes=list(row.get("expected_action_themes", [])),
            min_action_themes_hit=int(row.get("min_action_themes_hit", 1)),
            as_of_news=list(row.get("as_of_news", [])),
            ground_truth=list(row.get("ground_truth", [])),
            hindsight_keyword_group_labels=list(
                row.get("hindsight_keyword_group_labels", [])
            ),
            hindsight_action_themes=list(row.get("hindsight_action_themes", [])),
            hindsight_leak_markers=list(row.get("hindsight_leak_markers", [])),
            memo=str(row.get("memo") or ""),
            eval_dimensions=dict(row.get("eval_dimensions") or {}),
        )
        for row in rows
    ]


def _news_from_rows(rows: list[dict[str, Any]]) -> list[NewsItem]:
    return [
        NewsItem(
            title=str(row["title"]),
            publisher=str(row.get("publisher") or ""),
            link=str(row.get("link") or ""),
            published=str(row.get("published") or ""),
        )
        for row in rows
    ]


def frozen_news_for_case(case: BenchmarkCase) -> list[NewsItem]:
    """Contemporaneous headlines the agent may see (published <= as_of)."""
    return _news_from_rows(list(case.as_of_news))


def ground_truth_news_for_case(case: BenchmarkCase) -> list[NewsItem]:
    """Post-event sources for eval only — not graph input."""
    return _news_from_rows(list(case.ground_truth))


def comparison_news_for_case(case: BenchmarkCase) -> list[NewsItem]:
    """Same as frozen as-of news. Desk-color / answer-key injection is forbidden."""
    return frozen_news_for_case(case)


def _parse_published(value: str) -> date | None:
    text = (value or "").strip()
    if not text:
        return None
    return date.fromisoformat(text[:10])


def as_of_news_blob(case: BenchmarkCase) -> str:
    return " ".join(item.title for item in frozen_news_for_case(case))


def split_keyword_groups_by_lineage(case: BenchmarkCase) -> tuple[list[str], list[str]]:
    """Return (groups visible in as-of news, groups only in post-hoc rubric)."""
    blob = as_of_news_blob(case).lower()
    contemporaneous: list[str] = []
    post_hoc: list[str] = []
    for group in case.keyword_groups():
        label = group[0]
        if any(kw.lower() in blob for kw in group):
            contemporaneous.append(label)
        else:
            post_hoc.append(label)
    return contemporaneous, post_hoc


def news_lineage_errors(cases: list[BenchmarkCase] | None = None) -> list[str]:
    """Agent input must not include future or undated tape; GT must be strictly later."""
    errors: list[str] = []
    for case in cases or load_cases():
        as_of = case.as_of_date()
        if not case.as_of_news:
            errors.append(f"{case.test_id}: as_of_news is empty")
        for row in case.as_of_news:
            title = str(row.get("title") or "")[:80]
            published = _parse_published(str(row.get("published") or ""))
            if published is None:
                errors.append(f"{case.test_id}: as_of news missing published ({title})")
            elif published > as_of:
                errors.append(
                    f"{case.test_id}: as_of news published {published} > as_of {as_of} ({title})"
                )
        if not case.ground_truth:
            errors.append(f"{case.test_id}: ground_truth is empty")
        for row in case.ground_truth:
            title = str(row.get("title") or "")[:80]
            published = _parse_published(str(row.get("published") or ""))
            if published is None:
                errors.append(f"{case.test_id}: ground_truth missing published ({title})")
            elif published <= as_of:
                errors.append(
                    f"{case.test_id}: ground_truth published {published} <= as_of {as_of} ({title})"
                )
    return errors


def format_ground_truth_markdown(case: BenchmarkCase) -> str:
    """Human-readable eval key. Must not be passed into the agent."""
    lines = [
        f"# Ground truth (eval only) — {case.test_id}",
        "",
        f"as_of: `{case.date}`",
        "",
        "Agent-visible news is contemporaneous only. Sources below are **not** graph input.",
        "",
        "## Scenario note (eval, not agent input)",
        "",
        case.input_text.strip(),
        "",
        "## As-of news (agent input)",
        "",
    ]
    for item in frozen_news_for_case(case):
        lines.append(f"- {item.published} — **{item.publisher}**: {item.title}")
        if item.link:
            lines.append(f"  {item.link}")
    lines.extend(["", "## Post-event ground truth", ""])
    for row in case.ground_truth:
        note = str(row.get("note") or "").strip()
        excerpt = str(row.get("excerpt") or "").strip()
        lines.append(
            f"- {row.get('published')} — **{row.get('publisher')}**: {row.get('title')}"
        )
        if row.get("link"):
            lines.append(f"  {row['link']}")
        if note:
            lines.append(f"  _{note}_")
        if excerpt:
            lines.append(f"  > {excerpt}")
    contemporaneous, _post_hoc = split_keyword_groups_by_lineage(case)
    required = [group[0] for group in case.required_keyword_groups()]
    hindsight = [group[0] for group in case.hindsight_keyword_groups()]
    memo_path = resolve_memo_path(case)
    if memo_path is not None:
        try:
            rel = memo_path.relative_to(REPO_ROOT)
        except ValueError:
            rel = memo_path
        lines.extend(["", "## Desk memo", "", f"See `{rel.as_posix()}`", ""])
    dims = case.eval_dimensions or {}
    layer_a = dims.get("layer_a") or {}
    layer_b = dims.get("layer_b") or {}
    lines.extend(
        [
            "",
            "## Rubric",
            "",
            f"- Keyword groups in as-of tape: {', '.join(contemporaneous) or '(none)'}",
            f"- Desk-inferable bar (pass/fail): {', '.join(required) or '(none — no hard narrative bar)'}",
            f"- Hindsight / oracle only (not required): {', '.join(hindsight) or '(none)'}",
            f"- Min inferable groups hit: {case.min_keyword_groups_hit}",
            f"- Action themes (required): {', '.join(case.required_action_themes()) or '(none)'}",
            f"- Layer A tokens: {', '.join(layer_a.get('tokens') or []) or '(none)'}",
            f"- Layer B tokens: {', '.join(layer_b.get('tokens') or []) or '(none)'}",
            "",
            "## Parametric knowledge caveat",
            "",
            PARAMETRIC_KNOWLEDGE_CAVEAT,
            "",
        ]
    )
    return "\n".join(lines)


def score_keyword_groups(text: str, case: BenchmarkCase) -> tuple[int, list[str]]:
    """Hit count over the full catalog (inferable + hindsight)."""
    return score_group_lists(text, case.keyword_groups())


def score_group_lists(text: str, groups: list[list[str]]) -> tuple[int, list[str]]:
    """Return (groups_hit, missing_primary_labels)."""
    text_l = text.lower()
    hit = 0
    missing: list[str] = []
    for group in groups:
        if any(kw.lower() in text_l for kw in group):
            hit += 1
        else:
            missing.append(group[0])
    return hit, missing


def score_action_themes(text: str, case: BenchmarkCase) -> tuple[int, list[str]]:
    return score_theme_list(text, case.action_themes())


def score_theme_list(text: str, themes: list[str]) -> tuple[int, list[str]]:
    text_l = text.lower()
    hit = 0
    missing: list[str] = []
    for theme in themes:
        if theme.lower() in text_l:
            hit += 1
        else:
            missing.append(theme)
    return hit, missing


def leak_marker_hits(text: str, case: BenchmarkCase) -> list[str]:
    """Post-event-only tokens that are not in the as-of tape."""
    blob = text.lower()
    as_of = as_of_news_blob(case).lower()
    hits: list[str] = []
    for marker in case.hindsight_leak_markers:
        token = marker.lower()
        if token and token in blob and token not in as_of:
            hits.append(marker)
    return hits
