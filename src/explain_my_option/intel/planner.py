"""Query planners: blotter cues → bounded SearchPlan. Default is deterministic (no LLM)."""

from __future__ import annotations

from typing import Protocol

from explain_my_option.pricing.types import MarketSnapshot, PricingResult

from .types import SearchPlan, SearchQuery

DEFAULT_MAX_QUERIES = 3
HEADLINE_LIMIT = 3
# Share of |factor| / sum(|factors|) that counts as "large".
_LARGE_SHARE = 0.35
# Move-magnitude cues (independent of Greek share — a Delta-led gap can still crush IV).
_SPOT_LARGE_PCT = 10.0
_VOL_LARGE_PTS = 8.0
_RESIDUAL_VS_MODEL = 0.15
# Per-option floors. Quiet theta / microstructure noise should not burn a news call.
MATERIAL_USD = 0.50
MATERIAL_PCT_MID = 0.05


class QueryPlanner(Protocol):
    """Swap for a small LLM planner later; keep the same SearchPlan cap."""

    def plan(
        self,
        snapshot: MarketSnapshot,
        pricing: PricingResult,
        *,
        observation_reliable: bool = True,
    ) -> SearchPlan: ...


def move_is_material(snapshot: MarketSnapshot, pricing: PricingResult) -> bool:
    """True when the 1-day move is large enough to justify a catalyst search."""
    pnl = pricing.pnl
    abs_model = abs(pnl.total_pnl)
    if abs_model >= MATERIAL_USD:
        return True
    if snapshot.option_price_now > 0 and snapshot.option_price_prev > 0:
        if abs(snapshot.option_price_now - snapshot.option_price_prev) >= MATERIAL_USD:
            return True
    mid = snapshot.mid
    if mid is None and snapshot.option_price_now > 0:
        mid = snapshot.option_price_now
    if mid is not None and abs(mid) > 1e-12 and abs_model / abs(mid) >= MATERIAL_PCT_MID:
        return True
    spot_prev = snapshot.spot_prev or 0.0
    spot_pct = abs(100.0 * pnl.d_spot / spot_prev) if abs(spot_prev) > 1e-12 else 0.0
    vol_pts = abs(pnl.d_vol) * 100.0
    return spot_pct >= _SPOT_LARGE_PCT or vol_pts >= _VOL_LARGE_PTS


class CueQueryPlanner:
    """Rule planner: search only when the move is material and observation is reliable.

    Quiet / wide-quote days emit an empty plan (no Yahoo). Material + reliable days
    get ticker headlines plus vega / gap / microstructure / 8-K cues.

    Factor magnitudes include delta, gamma, vega, theta, and residual so the
    dominant share matches the Taylor attribution table.

    Cue mapping (still bounded by max_queries; not a graph branch):
    - Material + reliable → ticker headlines (Yahoo)
    - Vega dominant/large **or** |Δσ| large → earnings / IV Tavily query
    - Gamma dominant/large + spot move, or large |ΔS/S| (if microstructure not already queued)
      → gap / event Tavily query
    - Residual elevated vs |model ΔP| **and** large spot jump → microstructure
      (squeeze / borrow / float) Tavily query
    - Residual large + ex-dividend soon → dividend 8-K **and** generic 8-K
    - Residual large, no ex-div → generic 8-K
    """

    def __init__(
        self,
        *,
        max_queries: int = DEFAULT_MAX_QUERIES,
        large_share: float = _LARGE_SHARE,
    ) -> None:
        self.max_queries = max_queries
        self.large_share = large_share

    def plan(
        self,
        snapshot: MarketSnapshot,
        pricing: PricingResult,
        *,
        observation_reliable: bool = True,
    ) -> SearchPlan:
        from datetime import datetime

        if not observation_reliable:
            return SearchPlan(
                queries=[],
                max_queries=self.max_queries,
                skip_reason="observation_lock",
            )
        if not move_is_material(snapshot, pricing):
            return SearchPlan(
                queries=[],
                max_queries=self.max_queries,
                skip_reason="below_materiality",
            )

        ticker = snapshot.ticker
        pnl = pricing.pnl
        mag = {
            "delta": abs(pnl.delta_pnl),
            "gamma": abs(pnl.gamma_pnl),
            "vega": abs(pnl.vega_pnl),
            "theta": abs(pnl.theta_pnl),
            "residual": abs(pnl.residual_pnl),
        }
        total = sum(mag.values()) or 1e-12
        dominant = max(mag, key=mag.get)
        abs_model = abs(pnl.total_pnl) or 1e-12
        residual_vs_model = abs(pnl.residual_pnl) / abs_model
        spot_prev = snapshot.spot_prev or 0.0
        spot_pct = abs(100.0 * pnl.d_spot / spot_prev) if abs(spot_prev) > 1e-12 else 0.0
        vol_pts = abs(pnl.d_vol) * 100.0
        residual_large_share = mag["residual"] / total >= self.large_share
        residual_elevated = residual_large_share or residual_vs_model >= _RESIDUAL_VS_MODEL

        queries: list[SearchQuery] = [
            SearchQuery(
                q=ticker,
                source_id="yfinance_news",
                cue="material",
                limit=HEADLINE_LIMIT,
            )
        ]

        def _room() -> bool:
            return len(queries) < self.max_queries

        vega_cue = dominant == "vega" or mag["vega"] / total >= self.large_share or vol_pts >= _VOL_LARGE_PTS
        if _room() and vega_cue:
            queries.append(
                SearchQuery(
                    q=f"{ticker} implied volatility earnings event IV crush",
                    source_id="tavily",
                    cue="vega",
                    limit=HEADLINE_LIMIT,
                )
            )

        microstructure_cue = residual_elevated and spot_pct >= _SPOT_LARGE_PCT
        if _room() and microstructure_cue:
            queries.append(
                SearchQuery(
                    q=f"{ticker} short squeeze borrow float buy-in hard-to-borrow",
                    source_id="tavily",
                    cue="microstructure",
                    limit=HEADLINE_LIMIT,
                )
            )

        gamma_cue = (
            (dominant == "gamma" or mag["gamma"] / total >= self.large_share)
            and abs(pnl.d_spot) > 0.5
        ) or (spot_pct >= _SPOT_LARGE_PCT and not microstructure_cue)
        if _room() and gamma_cue:
            queries.append(
                SearchQuery(
                    q=f"{ticker} earnings gap news event",
                    source_id="tavily",
                    cue="gamma",
                    limit=HEADLINE_LIMIT,
                )
            )

        has_ex_div_soon = False
        if snapshot.discrete_dividends:
            try:
                as_of_date = datetime.fromisoformat(snapshot.as_of) if snapshot.as_of else datetime.now()
                for d in snapshot.discrete_dividends:
                    ex_dt = datetime.fromisoformat(d.ex_date)
                    days_to_ex = (ex_dt - as_of_date).days
                    if 0 <= days_to_ex <= 30:
                        has_ex_div_soon = True
                        break
            except (ValueError, AttributeError):
                pass

        if _room() and residual_large_share and has_ex_div_soon:
            queries.append(
                SearchQuery(
                    q=f"{ticker} 8-K dividend special",
                    source_id="sec_8k",
                    cue="residual_ex_div",
                    limit=HEADLINE_LIMIT,
                )
            )

        if _room() and residual_large_share:
            queries.append(
                SearchQuery(
                    q=f"{ticker} 8-K",
                    source_id="sec_8k",
                    cue="residual",
                    limit=HEADLINE_LIMIT,
                )
            )

        return SearchPlan(queries=queries[: self.max_queries], max_queries=self.max_queries)


def default_planner() -> QueryPlanner:
    return CueQueryPlanner()
