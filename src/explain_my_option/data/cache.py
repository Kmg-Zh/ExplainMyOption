"""Local SQLite cache of live chain snapshots (t-1 lookup). Gitignored path."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, fields
from datetime import date
from pathlib import Path
from typing import Optional

from ..pricing.types import (
    DiscreteDividend,
    MarketSnapshot,
    VolSurfaceData,
)

DEFAULT_CACHE = Path(".cache/explain-my-option/market.sqlite")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS snapshots (
    ticker TEXT NOT NULL,
    expiry TEXT NOT NULL,
    strike REAL NOT NULL,
    option_type TEXT NOT NULL,
    as_of TEXT NOT NULL,
    snapshot_json TEXT NOT NULL,
    surface_json TEXT,
    PRIMARY KEY (ticker, expiry, strike, option_type, as_of)
);
"""


def cache_path(root: Optional[Path] = None) -> Path:
    p = root or DEFAULT_CACHE
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _connect(path: Optional[Path] = None) -> sqlite3.Connection:
    conn = sqlite3.connect(cache_path(path))
    conn.execute(_SCHEMA)
    return conn


def _snapshot_to_dict(snap: MarketSnapshot) -> dict:
    d = asdict(snap)
    return d


def _snapshot_from_dict(d: dict) -> MarketSnapshot:
    divs = [
        DiscreteDividend(ex_date=x["ex_date"], amount=float(x["amount"]))
        for x in d.get("discrete_dividends") or []
    ]
    d = dict(d)
    d["discrete_dividends"] = divs
    known = {f.name for f in fields(MarketSnapshot)}
    filtered = {k: v for k, v in d.items() if k in known}
    return MarketSnapshot(**filtered)  # type: ignore[arg-type]


def _surface_from_dict(d: Optional[dict]) -> Optional[VolSurfaceData]:
    if not d:
        return None
    return VolSurfaceData(
        as_of=d["as_of"],
        expiries=list(d["expiries"]),
        strikes=[float(k) for k in d["strikes"]],
        matrix=[[float(v) for v in row] for row in d["matrix"]],
        data_source=d.get("data_source", "yfinance"),
    )


def upsert_snapshot(
    snap: MarketSnapshot,
    surface: Optional[VolSurfaceData],
    *,
    path: Optional[Path] = None,
) -> None:
    as_of = snap.as_of or date.today().isoformat()
    surf_json = json.dumps(asdict(surface)) if surface is not None else None
    with _connect(path) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO snapshots
            (ticker, expiry, strike, option_type, as_of, snapshot_json, surface_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                snap.ticker.upper(),
                snap.expiry,
                float(snap.strike),
                snap.option_type,
                as_of,
                json.dumps(_snapshot_to_dict(snap)),
                surf_json,
            ),
        )
        conn.commit()


def load_t1(
    ticker: str,
    expiry: str,
    strike: float,
    option_type: str,
    as_of: str,
    *,
    path: Optional[Path] = None,
) -> tuple[Optional[MarketSnapshot], Optional[VolSurfaceData]]:
    """Load the most recent cached row strictly before ``as_of`` for this contract."""
    with _connect(path) as conn:
        row = conn.execute(
            """
            SELECT snapshot_json, surface_json FROM snapshots
            WHERE ticker = ? AND expiry = ? AND option_type = ?
              AND as_of < ? AND ABS(strike - ?) < 1e-6
            ORDER BY as_of DESC
            LIMIT 1
            """,
            (ticker.upper(), expiry, option_type, as_of, float(strike)),
        ).fetchone()
    if not row:
        return None, None
    snap = _snapshot_from_dict(json.loads(row[0]))
    surf = _surface_from_dict(json.loads(row[1]) if row[1] else None)
    return snap, surf


def list_as_of_dates(*, path: Optional[Path] = None) -> list[str]:
    """Distinct ``as_of`` dates in the cache, ascending."""
    with _connect(path) as conn:
        rows = conn.execute(
            "SELECT DISTINCT as_of FROM snapshots ORDER BY as_of ASC"
        ).fetchall()
    return [r[0] for r in rows]


def count_snapshots(*, path: Optional[Path] = None) -> int:
    with _connect(path) as conn:
        row = conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()
    return int(row[0]) if row else 0


def list_snapshots_for_as_of(
    as_of: str,
    *,
    path: Optional[Path] = None,
) -> list[tuple[str, str, float, str]]:
    """Return ``(ticker, expiry, strike, option_type)`` rows for one day."""
    with _connect(path) as conn:
        rows = conn.execute(
            """
            SELECT ticker, expiry, strike, option_type FROM snapshots
            WHERE as_of = ?
            ORDER BY ticker, option_type, strike
            """,
            (as_of,),
        ).fetchall()
    return [(r[0], r[1], float(r[2]), r[3]) for r in rows]
