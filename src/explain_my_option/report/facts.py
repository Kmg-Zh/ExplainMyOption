"""Deterministic report facts — sole source of numeric truth for the template."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from ..data_loader import NewsItem
from ..intel.types import SearchPlan
from ..pricing.types import MarketSnapshot, PnLAttribution, PricingResult
from ..report_generator import contract_id, scale_pnl
from .reconciliation import ReconciliationFacts, build_reconciliation_facts

DriverKey = Literal["delta", "gamma", "vega", "theta", "residual"]
ConfidenceLevel = Literal["high", "medium", "low"]


@dataclass
class AttributionRow:
    key: DriverKey
    label: str
    usd: float
    pct_of_total: float
    driver_note: str


@dataclass
class AmericanFacts:
    exercise_style: str
    american_price: float | None
    european_price: float | None
    early_exercise_premium: float | None
    dividend_pv_effect: float | None
    ee_premium_anomaly: bool
    intrinsic: float
    time_value: float
    spot_now: float
    strike: float
    next_ex_div: str | None
    next_div_amount: float | None
    early_exercise_assessment: str


@dataclass
class PositionFacts:
    """All numbers for one option position — consumed by the Markdown template."""

    contract_label: str
    ticker: str
    option_type: str
    strike: float
    expiry: str
    eval_date: str
    data_source: str
    engine: str
    iv_prev_source: str
    quantity: float
    multiplier: float

    spot_prev: float
    spot_now: float
    d_spot: float
    spot_pct: float
    iv_prev: float
    iv_now: float
    d_vol_pts: float
    price_prev: float
    price_now: float
    total_pnl: float
    pnl_pct: float
    headline_pnl_usd: float
    headline_is_mtm: bool
    model_pnl_usd: float
    mark_pnl_usd: float | None

    greeks_delta: float
    greeks_gamma: float
    greeks_vega: float
    greeks_theta: float

    attribution: list[AttributionRow]
    primary_driver: DriverKey
    primary_driver_label: str
    primary_driver_pct: float
    explained_pct: float
    residual_pct: float
    confidence: ConfidenceLevel
    confidence_reasons: list[str]

    american: AmericanFacts
    reconciliation: ReconciliationFacts | None
    limitations: list[str]
    surface_notes: list[str]
    pct_uses_abs_share: bool
    prev_as_of_note: str | None = None


@dataclass
class PortfolioFacts:
    """Roll-up when multiple positions are diagnosed together."""

    eval_date: str
    position_count: int
    total_pnl: float
    total_mark_pnl: float | None
    total_model_pnl: float
    aggregate_mark_gap: float | None
    tickers: list[str]
    top_by_abs_pnl: list[tuple[str, float]]
    top_by_ticker: list[tuple[str, float]]
    aggregate_attribution: dict[DriverKey, float]


@dataclass
class PositionBundle:
    """One position's inputs for report assembly."""

    snapshot: MarketSnapshot
    pricing: PricingResult
    news: list[NewsItem] = field(default_factory=list)
    plan: SearchPlan | None = None


def _pct(part: float, whole: float) -> float:
    if abs(whole) < 1e-12:
        return 0.0
    return 100.0 * part / whole


def _abs_share(part: float, parts: list[float]) -> float:
    denom = sum(abs(x) for x in parts)
    if denom < 1e-12:
        return 0.0
    return 100.0 * abs(part) / denom


def _intrinsic(snap: MarketSnapshot) -> float:
    if snap.option_type.lower().startswith("c"):
        return max(snap.spot_now - snap.strike, 0.0)
    return max(snap.strike - snap.spot_now, 0.0)


def _spot_pct(d_spot: float, spot_prev: float) -> float:
    if abs(spot_prev) < 1e-12:
        return 0.0
    return 100.0 * d_spot / spot_prev


def _confidence(
    *,
    explained_pct: float,
    residual_pct: float,
    iv_prev_source: str,
    limitations: list[str],
    news_count: int,
    reconciliation: ReconciliationFacts | None = None,
) -> tuple[ConfidenceLevel, list[str]]:
    reasons: list[str] = []
    level: ConfidenceLevel = "high"

    if explained_pct < 85.0 or abs(residual_pct) > 15.0:
        level = "medium"
        reasons.append(
            f"Taylor attribution explains {explained_pct:.1f}% of total PnL; "
            f"residual is {abs(residual_pct):.1f}%."
        )
    if iv_prev_source == "hv20_proxy":
        if level == "high":
            level = "medium"
        reasons.append("Prior-day IV is an HV20 proxy, not a chain mark.")
    if iv_prev_source == "copied":
        level = "low"
        reasons.append("No t-1 IV mark — prior vol copied from today.")
    if limitations:
        if level == "high":
            level = "medium"
        reasons.append(f"Engine limitations: {', '.join(limitations)}.")
    if news_count == 0:
        if level == "high":
            level = "medium"
        reasons.append("No news hits to corroborate the narrative.")
    if reconciliation is not None:
        if reconciliation.iv_move_within_noise:
            if level == "high":
                level = "medium"
            reasons.append(
                "IV move sits inside the bid-ask noise band — Vega story not falsifiable from this quote."
            )
        if reconciliation.quote_tier != "reliable":
            if reconciliation.quote_tier in ("wide+thin", "unquoted"):
                level = "low"
            elif level == "high":
                level = "medium"
            reasons.append(f"Quote tier: {reconciliation.quote_tier}.")
        if reconciliation.deep_otm_itm:
            if level == "high":
                level = "medium"
            reasons.append("Deep OTM/ITM — Vega near zero; IV moves may be numerically unstable.")
    if not reasons:
        reasons.append(
            f"Taylor attribution explains {explained_pct:.1f}% of total PnL "
            f"(residual {abs(residual_pct):.1f}%)."
        )
    return level, reasons


def _american_facts(snap: MarketSnapshot, pricing: PricingResult) -> AmericanFacts:
    diag = pricing.diagnostics
    american = diag.american_price if diag.american_price is not None else pricing.greeks_now.price
    intrinsic = _intrinsic(snap)
    time_value = max(american - intrinsic, 0.0)

    next_ex: str | None = None
    next_amt: float | None = None
    if snap.discrete_dividends:
        future = sorted(snap.discrete_dividends, key=lambda d: d.ex_date)
        if future:
            next_ex = future[0].ex_date
            next_amt = future[0].amount

    if diag.ee_premium_anomaly:
        ee_assessment = (
            "Early-exercise premium printed negative — a numerical "
            "anomaly (engine/grid inconsistency), not a genuine exercise "
            "signal; see docs/dev/WORK_ORDER_REPORT.md."
        )
    elif diag.early_exercise_premium is not None and diag.early_exercise_premium < 0.01:
        ee_assessment = (
            "Early-exercise premium vs European is negligible — "
            "immediate exercise is sub-optimal at current marks."
        )
    elif time_value > 0 and next_amt is not None and time_value > next_amt * 1.5:
        ee_assessment = (
            f"Time value (${time_value:.4f}) exceeds the next cash dividend "
            f"(${next_amt:.4f}) — early-exercise risk is low near term."
        )
    elif intrinsic > 0 and time_value < (next_amt or 0.0):
        ee_assessment = (
            "ITM with time value below the next dividend — monitor early-exercise boundary."
        )
    else:
        ee_assessment = (
            "Compare time value vs upcoming dividends and carry when assessing early exercise."
        )

    return AmericanFacts(
        exercise_style=diag.exercise_style,
        american_price=diag.american_price,
        european_price=diag.european_price,
        early_exercise_premium=diag.early_exercise_premium,
        dividend_pv_effect=diag.dividend_pv_effect,
        ee_premium_anomaly=diag.ee_premium_anomaly,
        intrinsic=intrinsic,
        time_value=time_value,
        spot_now=snap.spot_now,
        strike=snap.strike,
        next_ex_div=next_ex,
        next_div_amount=next_amt,
        early_exercise_assessment=ee_assessment,
    )


def build_position_facts(
    snap: MarketSnapshot,
    pricing: PricingResult,
    *,
    news_count: int = 0,
) -> PositionFacts:
    """Derive template numbers from the quant engine output."""
    scale = snap.position_scale()
    pnl = scale_pnl(pricing.pnl, scale)
    g = pricing.greeks_prev
    pos_g = pricing.greeks_prev  # per-option greeks for display rows

    price_prev = g.price
    price_now = pricing.greeks_now.price
    total = pnl.total_pnl
    explained = total - pnl.residual_pnl
    explained_pct = _pct(explained, total) if abs(total) > 1e-12 else 100.0
    residual_pct = _pct(pnl.residual_pnl, total)

    reconciliation: ReconciliationFacts | None = None
    if snap.option_price_now > 0 or (snap.bid is not None and snap.ask is not None):
        reconciliation = build_reconciliation_facts(snap, pricing)
    pct_uses_abs = (
        reconciliation.pct_uses_abs_share
        if reconciliation is not None
        else abs(total) < 1e-12 or abs(total) < 5.0
    )

    rows_spec: list[tuple[DriverKey, str, float, str]] = [
        (
            "delta",
            "Delta PnL (ΔS · Delta)",
            pnl.delta_pnl,
            f"Stock moved {_spot_note(pnl.d_spot, snap.spot_prev, snap.spot_now)}",
        ),
        (
            "gamma",
            "Gamma PnL (½(ΔS)² · Gamma)",
            pnl.gamma_pnl,
            "Convexity from the spot move",
        ),
        (
            "vega",
            "Vega PnL (Δσ · Vega)",
            pnl.vega_pnl,
            f"IV moved {pnl.d_vol * 100:+.2f} vol pts ({snap.iv_prev * 100:.2f}% → {snap.iv_now * 100:.2f}%)",
        ),
        (
            "theta",
            "Theta decay (Δt · Theta)",
            pnl.theta_pnl,
            "Calendar time decay (1 day)",
        ),
        (
            "residual",
            "Unexplained residual (ε)",
            pnl.residual_pnl,
            "American EE, skew curvature, dividend discreteness, model gap",
        ),
    ]
    usd_parts = [usd for _, _, usd, _ in rows_spec]
    attribution = [
        AttributionRow(
            key=key,
            label=label,
            usd=usd,
            pct_of_total=_abs_share(usd, usd_parts) if pct_uses_abs else _pct(usd, total),
            driver_note=note,
        )
        for key, label, usd, note in rows_spec
    ]

    primary = max(attribution, key=lambda r: abs(r.usd))
    diag = pricing.diagnostics
    iv_src = diag.iv_prev_source or snap.iv_prev_source
    lim = list(diag.limitations)
    surface_notes: list[str] = []
    sd = pricing.surface_diagnostics
    if sd is not None and sd.limitations:
        surface_notes.extend(sd.limitations)

    confidence, confidence_reasons = _confidence(
        explained_pct=explained_pct,
        residual_pct=residual_pct,
        iv_prev_source=iv_src,
        limitations=lim,
        news_count=news_count,
        reconciliation=reconciliation,
    )

    eval_date = snap.as_of or "—"
    model_pnl = total
    mark_pnl = reconciliation.mark_pnl_usd if reconciliation else None
    headline_is_mtm = mark_pnl is not None
    headline_pnl = mark_pnl if headline_is_mtm else model_pnl
    return PositionFacts(
        contract_label=contract_id(snap),
        ticker=snap.ticker,
        option_type=snap.option_type.upper(),
        strike=snap.strike,
        expiry=snap.expiry,
        eval_date=eval_date,
        data_source=diag.data_source,
        engine=diag.engine,
        iv_prev_source=iv_src,
        quantity=snap.quantity,
        multiplier=snap.multiplier,
        spot_prev=snap.spot_prev,
        spot_now=snap.spot_now,
        d_spot=pnl.d_spot,
        spot_pct=_spot_pct(pnl.d_spot, snap.spot_prev),
        iv_prev=snap.iv_prev,
        iv_now=snap.iv_now,
        d_vol_pts=pnl.d_vol * 100,
        price_prev=price_prev,
        price_now=price_now,
        total_pnl=total,
        pnl_pct=_pct(total, price_prev) if abs(price_prev) > 1e-12 else 0.0,
        headline_pnl_usd=headline_pnl,
        headline_is_mtm=headline_is_mtm,
        model_pnl_usd=model_pnl,
        mark_pnl_usd=mark_pnl,
        greeks_delta=g.delta,
        greeks_gamma=g.gamma,
        greeks_vega=g.vega,
        greeks_theta=g.theta,
        attribution=attribution,
        primary_driver=primary.key,
        primary_driver_label=primary.label.split(" ")[0],
        primary_driver_pct=abs(primary.pct_of_total),
        explained_pct=explained_pct,
        residual_pct=abs(residual_pct),
        confidence=confidence,
        confidence_reasons=confidence_reasons,
        american=_american_facts(snap, pricing),
        reconciliation=reconciliation,
        limitations=lim,
        surface_notes=surface_notes,
        pct_uses_abs_share=pct_uses_abs,
        prev_as_of_note=snap.prev_as_of,
    )


def _spot_note(d_spot: float, prev: float, now: float) -> str:
    return f"from ${prev:,.2f} to ${now:,.2f} ({d_spot:+.4f})"


def build_portfolio_facts(bundles: list[PositionBundle]) -> PortfolioFacts:
    """Aggregate PnL across positions for the portfolio header."""
    facts_list = [
        build_position_facts(b.snapshot, b.pricing, news_count=len(b.news))
        for b in bundles
    ]
    total = sum(f.total_pnl for f in facts_list)
    model_total = sum(f.model_pnl_usd for f in facts_list)
    mark_vals = [f.mark_pnl_usd for f in facts_list if f.mark_pnl_usd is not None]
    mark_total = sum(mark_vals) if mark_vals and len(mark_vals) == len(facts_list) else None
    agg_gap = (model_total - mark_total) if mark_total is not None else None
    by_label = [(f.contract_label, f.total_pnl) for f in facts_list]
    by_label.sort(key=lambda x: abs(x[1]), reverse=True)
    by_ticker: dict[str, float] = {}
    for f in facts_list:
        by_ticker[f.ticker] = by_ticker.get(f.ticker, 0.0) + f.total_pnl
    ticker_rows = sorted(by_ticker.items(), key=lambda x: abs(x[1]), reverse=True)

    agg: dict[DriverKey, float] = {
        "delta": 0.0,
        "gamma": 0.0,
        "vega": 0.0,
        "theta": 0.0,
        "residual": 0.0,
    }
    for f in facts_list:
        for row in f.attribution:
            agg[row.key] += row.usd

    eval_date = facts_list[0].eval_date if facts_list else "—"
    return PortfolioFacts(
        eval_date=eval_date,
        position_count=len(facts_list),
        total_pnl=total,
        total_mark_pnl=mark_total,
        total_model_pnl=model_total,
        aggregate_mark_gap=agg_gap,
        tickers=sorted({f.ticker for f in facts_list}),
        top_by_abs_pnl=by_label[:3],
        top_by_ticker=ticker_rows[:3],
        aggregate_attribution=agg,
    )
