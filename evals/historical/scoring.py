"""Narrative scoring for historical cases (test-only).

Pass/fail uses desk-inferable keyword/action bars. Layer A / Layer B dimensions
and ``failure_hints`` help attribute misses to prompt vs structure vs info gap.
Hindsight / leak markers are coverage only — never product input.
"""

from __future__ import annotations

from typing import Any

from explain_my_option.report.schema import DiagnosticSynthesis

from historical.cases import (
    PARAMETRIC_KNOWLEDGE_CAVEAT,
    BenchmarkCase,
    leak_marker_hits,
    score_group_lists,
    score_theme_list,
    split_keyword_groups_by_lineage,
)


def synthesis_narrative_text(synthesis: DiagnosticSynthesis) -> str:
    """Text used for keyword groups — includes quoted headlines (validate-safe)."""
    return " ".join(
        [
            synthesis.primary_driver,
            synthesis.verdict,
            synthesis.confidence_rationale,
            synthesis.american_commentary,
            " ".join(synthesis.takeaways),
            " ".join(e.headline for e in synthesis.evidence),
            " ".join(e.source for e in synthesis.evidence),
            " ".join(e.relevance for e in synthesis.evidence),
        ]
    )


def _required_bar(hit: int, available: int, configured_min: int) -> tuple[int, bool]:
    if available <= 0:
        return 0, True
    required = min(configured_min, available)
    return required, hit >= required


def _score_dimension(text: str, dim: dict[str, Any] | None) -> dict[str, Any]:
    if not dim:
        return {
            "configured": False,
            "hit": 0,
            "required": 0,
            "pass": True,
            "matched_tokens": [],
        }
    tokens = [str(t) for t in dim.get("tokens") or []]
    min_hits = int(dim.get("min_hits", 1))
    text_l = text.lower()
    matched = [tok for tok in tokens if tok.lower() in text_l]
    required = min(min_hits, len(tokens)) if tokens else 0
    return {
        "configured": True,
        "label": str(dim.get("label") or ""),
        "hit": len(matched),
        "required": required,
        "pass": len(matched) >= required if required else True,
        "matched_tokens": matched,
    }


def failure_hints_for_scores(scores: dict[str, Any], case: BenchmarkCase) -> list[str]:
    """Single-path hints: where to look next (prompt vs info gap vs leak)."""
    hints: list[str] = []
    if case.tier == "C" and not case.required_keyword_groups():
        hints.append("info_gap_oracle_only")
    layer_a = scores.get("layer_a") or {}
    layer_b = scores.get("layer_b") or {}
    if layer_a.get("configured") and not layer_a.get("pass"):
        hints.append("prompt_layer_a")
    if layer_b.get("configured") and not layer_b.get("pass"):
        hints.append("prompt_or_structure_layer_b")
    if not scores.get("keyword_groups_pass"):
        hints.append("desk_keyword_bar_miss")
    if not scores.get("action_themes_pass"):
        hints.append("desk_action_bar_miss")
    if scores.get("residual_ack_required") and not scores.get("residual_ack_pass"):
        hints.append("prompt_residual_ack")
    if scores.get("possible_parametric_leak"):
        hints.append("parametric_leak_flag")
    if not hints:
        hints.append("ok")
    return hints


def attribute_governed_vs_baseline(
    governed: dict[str, Any],
    baseline: dict[str, Any],
    case: BenchmarkCase,
) -> dict[str, Any]:
    """Compare-path attribution: does the graph help where baseline fails?"""
    gov_a = bool((governed.get("layer_a") or {}).get("pass", True))
    base_a = bool((baseline.get("layer_a") or {}).get("pass", True))
    gov_b = bool((governed.get("layer_b") or {}).get("pass", True))
    base_b = bool((baseline.get("layer_b") or {}).get("pass", True))
    gov_kw = bool(governed.get("keyword_groups_pass"))
    base_kw = bool(baseline.get("keyword_groups_pass"))

    primary = "ok"
    if case.tier == "C" and not case.required_keyword_groups():
        primary = "info_gap_oracle_only"
    elif gov_b and not base_b:
        primary = "structure_helps_layer_b"
    elif (not gov_b) and (not base_b) and (governed.get("layer_b") or {}).get("configured"):
        primary = "both_miss_layer_b_try_prompt_and_structure"
    elif gov_a and not base_a:
        primary = "structure_helps_layer_a"
    elif (not gov_a) and (not base_a):
        primary = "both_miss_layer_a_try_prompt"
    elif gov_kw and not base_kw:
        primary = "structure_helps_keyword_bar"
    elif (not gov_kw) and (not base_kw):
        primary = "both_miss_desk_bar"
    elif gov_kw and base_kw:
        primary = "ok"

    return {
        "primary": primary,
        "governed_layer_a_pass": gov_a,
        "baseline_layer_a_pass": base_a,
        "governed_layer_b_pass": gov_b,
        "baseline_layer_b_pass": base_b,
        "governed_keyword_pass": gov_kw,
        "baseline_keyword_pass": base_kw,
        "memo": case.memo,
        "how_to_read": (
            "structure_helps_* → keep/inspect debate nodes; "
            "both_miss_* → prompt/catalyst first; "
            "info_gap_oracle_only → do not require later-paper HTB; "
            "ok → desk bar met on both or N/A."
        ),
    }


def score_narrative_for_case(
    synthesis: DiagnosticSynthesis,
    case: BenchmarkCase,
    *,
    residual_pct: float,
    residual_threshold: float = 15.0,
) -> dict[str, Any]:
    narrative_text = synthesis_narrative_text(synthesis)
    text_l = narrative_text.lower()
    required_groups = case.required_keyword_groups()
    hindsight_groups = case.hindsight_keyword_groups()
    groups_hit, groups_missing = score_group_lists(narrative_text, required_groups)
    _hindsight_hit, hindsight_missing = score_group_lists(
        narrative_text, hindsight_groups
    )
    required_themes = case.required_action_themes()
    themes_hit, themes_missing = score_theme_list(
        " ".join(synthesis.takeaways), required_themes
    )
    residual_terms = (
        "residual",
        "model gap",
        "unexplained",
        "truncation",
        "taylor truncation",
        "higher-order",
    )
    mentions_residual = any(t in text_l for t in residual_terms)
    groups_required, groups_pass = _required_bar(
        groups_hit, len(required_groups), case.min_keyword_groups_hit
    )
    themes_required, themes_pass = _required_bar(
        themes_hit, len(required_themes), case.min_action_themes_hit
    )
    as_of_groups, post_hoc_groups = split_keyword_groups_by_lineage(case)
    hindsight_labels = [group[0] for group in hindsight_groups]
    leak_hits = leak_marker_hits(narrative_text, case)
    dims = case.eval_dimensions or {}
    layer_a = _score_dimension(narrative_text, dims.get("layer_a"))
    layer_b = _score_dimension(narrative_text, dims.get("layer_b"))
    scores: dict[str, Any] = {
        "keyword_groups_hit": groups_hit,
        "keyword_groups_required": groups_required,
        "keyword_groups_pass": groups_pass,
        "missing_keyword_groups": groups_missing,
        "as_of_keyword_groups": as_of_groups,
        "post_hoc_keyword_groups": post_hoc_groups,
        "hindsight_keyword_groups": hindsight_labels,
        "hindsight_groups_hit": [
            label for label in hindsight_labels if label not in hindsight_missing
        ],
        "hindsight_groups_missed": hindsight_missing,
        "possible_parametric_leak": bool(leak_hits),
        "leak_marker_hits": leak_hits,
        "action_themes_hit": themes_hit,
        "action_themes_required": themes_required,
        "action_themes_pass": themes_pass,
        "missing_action_themes": themes_missing,
        "mentions_residual": mentions_residual,
        "residual_ack_required": residual_pct >= residual_threshold,
        "residual_ack_pass": (not (residual_pct >= residual_threshold))
        or mentions_residual,
        "layer_a": layer_a,
        "layer_b": layer_b,
        "memo": case.memo,
        "parametric_knowledge_caveat": PARAMETRIC_KNOWLEDGE_CAVEAT,
        # Legacy flat-keyword fields (deprecated; kept for notebook drift)
        "keyword_hits": groups_hit,
        "keyword_total": groups_required,
    }
    scores["failure_hints"] = failure_hints_for_scores(scores, case)
    return scores
