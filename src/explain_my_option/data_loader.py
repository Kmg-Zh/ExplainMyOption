"""yfinance loaders: the market snapshot and vol surface (no news, no LLM), and
ticker headlines for the ``search`` node. Pricing never imports this module."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

import numpy as np
import pandas as pd
import yfinance as yf

from .data.cache import MIN_PLAUSIBLE_IV, load_t1, upsert_snapshot
from .data.dividends import normalize_dividend_yield, project_dividends
from .data.observation import DataBreakError, ObservationStatus, continuity_gate
from .data.rates import fetch_irx_rate
from .data.realized import hv20_from_closes, iv_prev_from_hv20
from .pricing.surface import parallel_shift_surface
from .intel.types import NewsItem
from .pricing.types import LoadedData, MarketSnapshot, VolSurfaceData
from .report.settlement import intrinsic


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
    if not np.isfinite(iv) or iv < MIN_PLAUSIBLE_IV:
        return None
    return iv


def _valid_closes(hist: pd.DataFrame) -> dict[date, float]:
    """Session date → close, for bars with a finite, positive close."""
    closes = pd.to_numeric(hist["Close"], errors="coerce")
    return {ts.date(): float(c) for ts, c in closes.items() if np.isfinite(c) and c > 0}


def _exchange_time(stamp, tz_name: Optional[str]) -> Optional[pd.Timestamp]:
    """A Yahoo timestamp (epoch seconds or Timestamp) in exchange-local time."""
    if stamp is None:
        return None
    try:
        ts = pd.Timestamp(stamp, unit="s") if isinstance(stamp, (int, float)) else pd.Timestamp(stamp)
        if pd.isna(ts):
            return None
        if ts.tzinfo is None:
            ts = ts.tz_localize("UTC")
        return ts.tz_convert(tz_name or "America/New_York")
    except Exception:
        return None


def _exchange_date(stamp, tz_name: Optional[str]) -> Optional[date]:
    """Exchange-local date of a Yahoo timestamp (epoch seconds or Timestamp)."""
    ts = _exchange_time(stamp, tz_name)
    return None if ts is None else ts.date()


def session_closed(hist: pd.DataFrame, session: date, metadata: Optional[dict] = None) -> bool:
    """True once ``session`` has a final price: its daily close, or Yahoo's
    regular-market price stamped at or after that session's regular close."""
    if session in _valid_closes(hist):
        return True
    md = metadata or {}
    tz = md.get("exchangeTimezoneName")
    stamped = _exchange_time(md.get("regularMarketTime"), tz)
    if stamped is None or stamped.date() != session:
        return False
    end = _exchange_time(((md.get("currentTradingPeriod") or {}).get("regular") or {}).get("end"), tz)
    if end is None or end.date() != session:
        end = pd.Timestamp(session).tz_localize(tz or "America/New_York") + pd.Timedelta(hours=16)
    return stamped >= end


def settlement_snapshot(
    hist: pd.DataFrame,
    metadata: Optional[dict],
    *,
    ticker: str,
    option_type: str,
    strike: Optional[float],
    expiry: str,
    session: date,
) -> MarketSnapshot:
    """A contract whose expiry is on or before ``session``: the expiry
    session's close and the last cached mark before it. No chain is read: by
    the evening of expiry Yahoo has already delisted the contract.
    """
    contract = f"{ticker.upper()} {option_type} {strike} {expiry}"
    if strike is None:
        raise ValueError(f"{contract} has expired; settling it needs its strike.")
    exp_d = date.fromisoformat(expiry)
    md = metadata or {}
    if exp_d == session:
        if not session_closed(hist, session, md):
            raise ValueError(
                f"{contract} expires today and settles at the {session} close; rerun after the close."
            )
        settle_d = session
        spot = session_close(
            hist,
            session,
            market_price=_finite_or_none(md.get("regularMarketPrice")),
            market_price_session=_exchange_date(md.get("regularMarketTime"), md.get("exchangeTimezoneName")),
        )
    else:
        closes = _valid_closes(hist)
        settle_d = max((d for d in closes if d <= exp_d), default=None)
        if settle_d is None:
            raise DataBreakError(
                "expiry session close", f"The source has no close on or before the {expiry} expiry of {contract}."
            )
        spot = closes[settle_d]

    cached, _ = load_t1(ticker.upper(), expiry, float(strike), option_type, settle_d.isoformat())
    mark_d = date.fromisoformat(cached.as_of) if cached is not None and cached.as_of else None
    spot_prev, prev_session = prior_close(hist, settle_d, prior_mark_date=mark_d)
    return MarketSnapshot(
        ticker=ticker.upper(),
        option_type=option_type,
        strike=float(strike),
        expiry=expiry,
        spot_now=spot,
        spot_prev=spot_prev,
        iv_now=float(cached.iv_now) if cached is not None else 0.0,
        iv_prev=float(cached.iv_now) if cached is not None else 0.0,
        option_price_now=intrinsic(option_type, float(strike), spot),
        option_price_prev=float(cached.option_price_now) if cached is not None else 0.0,
        time_to_expiry_years=0.0,
        risk_free_rate=float(cached.risk_free_rate) if cached is not None else 0.0,
        exercise_style="american",
        data_source="yfinance",
        as_of=settle_d.isoformat(),
        prev_as_of=prev_session.isoformat(),
        iv_prev_source="chain_t1" if cached is not None else "copied",
    )


def quote_session(hist: pd.DataFrame, metadata: Optional[dict] = None) -> date:
    """The trading session today's option quotes belong to.

    Yahoo stamps its latest regular-market price with that session's time;
    that date wins. Without it, the newest daily bar's date, even when the
    bar's close is still NaN: in the evening Yahoo lists the session's daily
    bar before it has a close.
    """
    md = metadata or {}
    stamped = _exchange_date(md.get("regularMarketTime"), md.get("exchangeTimezoneName"))
    if stamped is not None:
        return stamped
    return hist.index[-1].date()


def session_close(
    hist: pd.DataFrame,
    session: date,
    *,
    market_price: Optional[float] = None,
    market_price_session: Optional[date] = None,
) -> float:
    """Spot for ``session``: its daily close, else Yahoo's regular-market
    price when that is stamped with the same session.

    Never the last *valid* close: while the session's bar has a NaN close,
    that is the previous session's, and it would pair today's option quotes
    with yesterday's spot move.
    """
    closes = _valid_closes(hist)
    if session in closes:
        return closes[session]
    if market_price_session == session and market_price is not None and np.isfinite(market_price) and market_price > 0:
        return float(market_price)
    last = max((d for d in closes if d < session), default=None)
    raise DataBreakError(
        "spot dated to the option quotes",
        f"The quotes are from the {session} session, but the source has no {session} close yet "
        f"and no regular-market price stamped {session}; the newest close is {last}. Pairing "
        "them would attribute the wrong day's spot move.",
    )


def prior_close(
    hist: pd.DataFrame,
    session: date,
    *,
    prior_mark_date: Optional[date] = None,
) -> tuple[float, date]:
    """(spot_prev, its session) for the prior mark.

    The close of the last session on or before ``prior_mark_date`` (a run
    on a weekend or holiday captured the previous session's quotes), else of
    the last session before ``session``.
    """
    closes = _valid_closes(hist)
    candidates = [d for d in closes if d < session and (prior_mark_date is None or d <= prior_mark_date)]
    if not candidates:
        anchor = prior_mark_date or session
        raise DataBreakError(
            "prior spot dated to the prior mark",
            f"The source has no close on or before {anchor} before the {session} session.",
        )
    prev = max(candidates)
    return closes[prev], prev


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

    hist = tk.history(period="3mo", auto_adjust=False)
    if hist.empty or len(hist) < 2:
        # The live loader never independently queries a historical chain for
        # t-1 (iv_prev/option_price_prev come from the SQLite cache or an
        # HV20 proxy, which always produce *some* value), so t-1 is OK by
        # construction of this path. Only t can be DAY_MISSING here.
        continuity_gate(
            contract=f"{ticker} {option_type}",
            status_t1=ObservationStatus.OK,
            status_t=ObservationStatus.DAY_MISSING,
            date_t1="t-1",
            date_t=date.today().isoformat(),
        )
    # as_of is the session the option quotes belong to, not the calendar day
    # of the run; both spots are dated to the marks they are paired with.
    metadata = _history_metadata(tk)
    as_of_d = quote_session(hist, metadata)
    if expiry and date.fromisoformat(expiry) <= as_of_d:
        return LoadedData(
            snapshot=settlement_snapshot(
                hist, metadata, ticker=ticker, option_type=option_type, strike=strike, expiry=expiry, session=as_of_d
            )
        )
    as_of = as_of_d.isoformat()
    spot_now = session_close(
        hist,
        as_of_d,
        market_price=_finite_or_none(metadata.get("regularMarketPrice")),
        market_price_session=_exchange_date(metadata.get("regularMarketTime"), metadata.get("exchangeTimezoneName")),
    )
    hist = hist[np.isfinite(pd.to_numeric(hist["Close"], errors="coerce"))]

    expiry = expiry or _pick_nearest_expiry(tk)
    chain = tk.option_chain(expiry)
    table = chain.calls if option_type == "call" else chain.puts

    if table.empty:
        continuity_gate(
            contract=f"{ticker} {option_type} {expiry}",
            status_t1=ObservationStatus.OK,
            status_t=ObservationStatus.CONTRACT_MISSING,
            date_t1="t-1",
            date_t=as_of,
        )

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
    # No prior mark until the t-1 cache supplies one: a copy of today's mark
    # would calibrate ΔP_model to zero and push the whole spot move into vega.
    option_price_prev = 0.0
    surface_prev = None
    rate_prev: float | None = None
    prior_mark_date: date | None = None

    cached_snap, cached_surf = load_t1(
        ticker.upper(), expiry, strike, option_type, as_of
    )
    if cached_snap is not None:
        iv_prev = float(cached_snap.iv_now)
        option_price_prev = float(cached_snap.option_price_now)
        iv_prev_source = "chain_t1"
        surface_prev = cached_surf
        if cached_snap.as_of:
            prior_mark_date = date.fromisoformat(cached_snap.as_of)
        rate_prev = float(cached_snap.risk_free_rate)
    elif hv_now is not None and hv_prev is not None:
        iv_prev, _ = iv_prev_from_hv20(iv_now, hv_now, hv_prev)
        iv_prev_source = "hv20_proxy"
    else:
        iv_prev_source = "copied"
    # A cached row's own spot_now may be stale (rows cached before the session
    # alignment above); never read it. Re-read the close of its session.
    spot_prev, prev_session = prior_close(hist, as_of_d, prior_mark_date=prior_mark_date)
    prev_as_of = prev_session.isoformat()

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
        time_to_expiry_years=_year_fraction(expiry, as_of_d),
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

    return LoadedData(snapshot=snapshot, surface=surface, surface_prev=surface_prev)


def _history_metadata(tk: yf.Ticker) -> dict:
    """Yahoo's chart metadata for the last ``history`` call; {} when absent."""
    try:
        return dict(tk.history_metadata or {})
    except Exception:
        return {}


def _finite_or_none(raw) -> Optional[float]:
    try:
        v = float(raw)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(v):
        return None
    return v
