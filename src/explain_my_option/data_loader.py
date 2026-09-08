"""Data loader: market snapshot / vol surface vs news search, via yfinance.

Market path (`load_market_data`) has no news and no LLM. News is `fetch_news`
for the graph's ``search`` node. Pricing stays decoupled from yfinance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

import numpy as np
import pandas as pd
import yfinance as yf

from .data.cache import load_t1, upsert_snapshot
from .data.dividends import normalize_dividend_yield, project_dividends
from .data.rates import DEFAULT_RATE, fetch_irx_rate
from .data.realized import hv20_from_closes, iv_prev_from_hv20
from .pricing.surface import parallel_shift_surface
from .pricing.types import MarketSnapshot, VolSurfaceData


@dataclass
class NewsItem:
    title: str
    publisher: str = ""
    link: str = ""
    published: str = ""


@dataclass
class LoadedData:
    snapshot: MarketSnapshot
    news: list[NewsItem] = field(default_factory=list)
    surface: Optional[VolSurfaceData] = None
    surface_prev: Optional[VolSurfaceData] = None


def _year_fraction(expiry: str, as_of: Optional[date] = None) -> float:
    as_of = as_of or date.today()
    exp = datetime.strptime(expiry, "%Y-%m-%d").date()
    days = max((exp - as_of).days, 1)
    return days / 365.0


def _pick_nearest_expiry(tk: yf.Ticker, min_days: int = 7) -> str:
    """Pick the nearest listed expiry that is at least ``min_days`` away."""
    expiries = tk.options
    if not expiries:
        raise ValueError("No option expiries available for this ticker.")
    today = date.today()
    for exp in expiries:
        d = (datetime.strptime(exp, "%Y-%m-%d").date() - today).days
        if d >= min_days:
            return exp
    return expiries[-1]


def _pick_atm_row(chain: pd.DataFrame, spot: float) -> pd.Series:
    """Return the option-chain row whose strike is closest to spot."""
    if chain.empty:
        raise ValueError("Empty option chain.")
    idx = (chain["strike"] - spot).abs().idxmin()
    return chain.loc[idx]


def fetch_news(ticker: str, limit: int = 3) -> list[NewsItem]:
    """Fetch up to ``limit`` recent news headlines for a ticker.

    Fail-soft: Yahoo ``Ticker.news`` often raises or returns odd shapes.
    """
    try:
        tk = yf.Ticker(ticker)
        raw = getattr(tk, "news", None) or []
    except Exception:
        return []
    items: list[NewsItem] = []
    if not isinstance(raw, list):
        return items
    for entry in raw[:limit]:
        if not isinstance(entry, dict):
            continue
        try:
            content = entry.get("content", entry)
            if not isinstance(content, dict):
                content = entry
            title = content.get("title") or entry.get("title") or ""
            if not title:
                continue
            provider = content.get("provider")
            publisher = (
                provider.get("displayName")
                if isinstance(provider, dict)
                else entry.get("publisher", "")
            ) or ""
            canon = content.get("canonicalUrl")
            link = (
                canon.get("url", "")
                if isinstance(canon, dict)
                else entry.get("link", "")
            ) or ""
            published = content.get("pubDate") or str(entry.get("providerPublishTime", ""))
            items.append(
                NewsItem(title=title, publisher=publisher, link=link, published=published)
            )
        except Exception:
            continue
    return items


def _clean_iv(raw) -> Optional[float]:
    try:
        iv = float(raw)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(iv) or iv <= 0:
        return None
    return iv


def fetch_vol_surface(
    ticker: str,
    option_type: str = "call",
    *,
    max_expiries: int = 4,
    min_days: int = 7,
    as_of: Optional[str] = None,
) -> Optional[VolSurfaceData]:
    """Build a live ``VolSurfaceData`` from today's yfinance option chain.

    yfinance exposes only the **current** chain (no historical surface).
    Returns ``None`` when the chain is too thin after filtering bad IVs.
    Fail-soft: never raises for empty/partial chains.
    """
    try:
        tk = yf.Ticker(ticker)
        expiries = list(tk.options or [])
    except Exception:
        return None
    if not expiries:
        return None

    today = date.today()
    as_of_s = as_of or today.isoformat()
    chosen: list[str] = []
    for exp in expiries:
        d = (datetime.strptime(exp, "%Y-%m-%d").date() - today).days
        if d >= min_days:
            chosen.append(exp)
        if len(chosen) >= max_expiries:
            break
    if len(chosen) < 2:
        return None

    # Collect per-expiry strike→IV maps, then align on a shared strike grid.
    per_expiry: list[dict[float, float]] = []
    all_strikes: set[float] = set()
    try:
        hist = tk.history(period="5d", auto_adjust=False)
        spot = float(hist["Close"].iloc[-1]) if not hist.empty else None
    except Exception:
        spot = None

    for exp in chosen:
        try:
            chain = tk.option_chain(exp)
            table = chain.calls if option_type == "call" else chain.puts
        except Exception:
            per_expiry.append({})
            continue
        iv_map: dict[float, float] = {}
        for _, row in table.iterrows():
            iv = _clean_iv(row.get("impliedVolatility"))
            if iv is None:
                continue
            k = float(row["strike"])
            iv_map[k] = iv
            all_strikes.add(k)
        per_expiry.append(iv_map)

    if not all_strikes:
        return None

    # Prefer strikes near spot when available; otherwise keep a dense mid band.
    strikes_sorted = sorted(all_strikes)
    if spot is not None and len(strikes_sorted) > 9:
        strikes_sorted = sorted(
            strikes_sorted, key=lambda k: abs(k - spot)
        )[:11]
        strikes_sorted = sorted(strikes_sorted)

    matrix: list[list[float]] = []
    valid_expiries: list[str] = []
    for exp, iv_map in zip(chosen, per_expiry):
        row = []
        for k in strikes_sorted:
            iv = iv_map.get(k)
            row.append(iv if iv is not None else float("nan"))
        # Require at least 3 finite IVs on the expiry
        if sum(1 for x in row if x == x) >= 3:
            matrix.append(row)
            valid_expiries.append(exp)

    if len(valid_expiries) < 2 or len(strikes_sorted) < 3:
        return None

    return VolSurfaceData(
        as_of=as_of_s,
        expiries=valid_expiries,
        strikes=strikes_sorted,
        matrix=matrix,
        data_source="yfinance",
    )


def load_market_data(
    ticker: str,
    option_type: str = "call",
    strike: Optional[float] = None,
    expiry: Optional[str] = None,
    risk_free_rate: Optional[float] = None,
    *,
    include_surface: bool = True,
) -> LoadedData:
    """Fetch snapshot + optional live vol surface. No news, no LLM.

    If ``strike``/``expiry`` are omitted, the nearest expiry and the
    at-the-money strike are chosen automatically.

    ``iv_prev`` resolution: SQLite t-1 chain, else HV20 proxy, else copy.
    """
    tk = yf.Ticker(ticker)
    as_of_d = date.today()
    as_of = as_of_d.isoformat()

    hist = tk.history(period="3mo", auto_adjust=False)
    if hist.empty or len(hist) < 2:
        raise ValueError(f"Not enough price history for {ticker!r}.")
    spot_now = float(hist["Close"].iloc[-1])
    spot_prev = float(hist["Close"].iloc[-2])

    expiry = expiry or _pick_nearest_expiry(tk)
    chain = tk.option_chain(expiry)
    table = chain.calls if option_type == "call" else chain.puts

    if strike is None:
        row = _pick_atm_row(table, spot_now)
        strike = float(row["strike"])
    else:
        row = table.loc[(table["strike"] - strike).abs().idxmin()]
        strike = float(row["strike"])

    iv_now = _clean_iv(row.get("impliedVolatility"))
    if iv_now is None:
        iv_now = 0.30

    bid = _finite_or_none(row.get("bid"))
    ask = _finite_or_none(row.get("ask"))
    last = _finite_or_none(row.get("lastPrice"))
    mid = None
    if bid is not None and ask is not None and bid > 0 and ask > 0:
        mid = 0.5 * (bid + ask)
    option_price_now = mid if mid is not None else (last if last is not None else 0.0)

    volume = _finite_or_none(row.get("volume"))
    open_interest = _finite_or_none(row.get("openInterest"))

    if risk_free_rate is None:
        risk_free_rate, rate_source = fetch_irx_rate(yf)
    else:
        rate_source = "default"

    q = 0.0
    info: dict = {}
    try:
        info = tk.info or {}
        dy = info.get("dividendYield")
        if dy is not None and np.isfinite(float(dy)) and float(dy) >= 0:
            q, _rescaled = normalize_dividend_yield(float(dy))
    except Exception:
        q = 0.0
        info = {}

    exp_d = datetime.strptime(expiry, "%Y-%m-%d").date()
    discrete, inferred = project_dividends(
        tk, as_of=as_of_d, expiry=exp_d, info=info
    )

    hv_now, hv_prev = hv20_from_closes(hist["Close"].to_numpy())
    iv_prev = iv_now
    iv_prev_source = "hv20_proxy"
    option_price_prev = option_price_now
    surface_prev = None
    prev_as_of: str | None = None
    rate_prev: float | None = None
    try:
        prev_as_of = hist.index[-2].date().isoformat()
    except Exception:
        prev_as_of = None

    cached_snap, cached_surf = load_t1(
        ticker.upper(), expiry, strike, option_type, as_of
    )
    if cached_snap is not None:
        iv_prev = float(cached_snap.iv_now)
        option_price_prev = float(cached_snap.option_price_now)
        iv_prev_source = "chain_t1"
        surface_prev = cached_surf
        if cached_snap.as_of:
            prev_as_of = cached_snap.as_of
        rate_prev = float(cached_snap.risk_free_rate)
    elif hv_now is not None and hv_prev is not None:
        iv_prev, _ = iv_prev_from_hv20(iv_now, hv_now, hv_prev)
        iv_prev_source = "hv20_proxy"
    else:
        iv_prev_source = "copied"

    snapshot = MarketSnapshot(
        ticker=ticker.upper(),
        option_type=option_type,
        strike=strike,
        expiry=expiry,
        spot_now=spot_now,
        spot_prev=spot_prev,
        iv_now=iv_now,
        iv_prev=iv_prev,
        option_price_now=option_price_now,
        option_price_prev=option_price_prev,
        time_to_expiry_years=_year_fraction(expiry),
        risk_free_rate=float(risk_free_rate),
        dividend_yield=q,
        discrete_dividends=discrete,
        exercise_style="american",
        data_source="yfinance",
        as_of=as_of,
        prev_as_of=prev_as_of,
        risk_free_rate_prev=rate_prev,
        iv_prev_source=iv_prev_source,  # type: ignore[arg-type]
        hv20_now=hv_now,
        hv20_prev=hv_prev,
        bid=bid,
        ask=ask,
        mid=mid,
        volume=volume,
        open_interest=open_interest,
        risk_free_rate_source=rate_source,  # type: ignore[arg-type]
    )

    surface = None
    if include_surface:
        try:
            surface = fetch_vol_surface(ticker, option_type=option_type, as_of=as_of)
        except Exception:
            surface = None

    if (
        surface_prev is None
        and surface is not None
        and iv_prev_source == "hv20_proxy"
        and iv_prev != iv_now
    ):
        surface_prev = parallel_shift_surface(
            surface, iv_prev - iv_now, as_of=as_of
        )

    try:
        upsert_snapshot(snapshot, surface)
    except Exception:
        pass

    return LoadedData(
        snapshot=snapshot, news=[], surface=surface, surface_prev=surface_prev
    )


def _finite_or_none(raw) -> Optional[float]:
    try:
        v = float(raw)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(v):
        return None
    return v


def load_option_data(
    ticker: str,
    option_type: str = "call",
    strike: Optional[float] = None,
    expiry: Optional[str] = None,
    risk_free_rate: Optional[float] = None,
    news_limit: int = 3,
    *,
    include_surface: bool = True,
) -> LoadedData:
    """Convenience: market snapshot + news. Graph nodes should call the split loaders."""
    data = load_market_data(
        ticker,
        option_type=option_type,
        strike=strike,
        expiry=expiry,
        risk_free_rate=risk_free_rate,
        include_surface=include_surface,
    )
    data.news = fetch_news(ticker, limit=news_limit)
    return data
