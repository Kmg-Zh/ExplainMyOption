"""Load synthetic MarketSnapshot + VolSurfaceData fixtures (no network)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from explain_my_option.paths import FIXTURES_DIR as _FIXTURES_DIR
from explain_my_option.pricing.types import (
    DiscreteDividend,
    MarketSnapshot,
    VolSurfaceData,
)

# Snapshot keys that must be present in every market fixture JSON.
# Market assumptions (rates, yields, vol sources) are never invented here.
_REQUIRED_SNAPSHOT_KEYS = (
    "ticker",
    "option_type",
    "strike",
    "expiry",
    "spot_now",
    "spot_prev",
    "iv_now",
    "iv_prev",
    "time_to_expiry_years",
    "risk_free_rate",
    "dividend_yield",
    "exercise_style",
    "iv_prev_source",
)


def fixtures_dir() -> Path:
    return _FIXTURES_DIR


def _require_keys(d: dict[str, Any], keys: tuple[str, ...], *, context: str) -> None:
    missing = [k for k in keys if k not in d]
    if missing:
        raise ValueError(f"{context}: missing required keys {missing}")


def _snapshot_from_dict(d: dict[str, Any], *, context: str = "snapshot") -> MarketSnapshot:
    _require_keys(d, _REQUIRED_SNAPSHOT_KEYS, context=context)
    divs = [
        DiscreteDividend(ex_date=x["ex_date"], amount=float(x["amount"]))
        for x in d.get("discrete_dividends", [])
    ]
    return MarketSnapshot(
        ticker=d["ticker"],
        option_type=d["option_type"],
        strike=float(d["strike"]),
        expiry=d["expiry"],
        spot_now=float(d["spot_now"]),
        spot_prev=float(d["spot_prev"]),
        iv_now=float(d["iv_now"]),
        iv_prev=float(d["iv_prev"]),
        option_price_now=float(d.get("option_price_now", 0.0)),
        option_price_prev=float(d.get("option_price_prev", 0.0)),
        time_to_expiry_years=float(d["time_to_expiry_years"]),
        risk_free_rate=float(d["risk_free_rate"]),
        dividend_yield=float(d["dividend_yield"]),
        discrete_dividends=divs,
        exercise_style=d["exercise_style"],
        data_source="synthetic",
        as_of=d.get("as_of"),
        prev_as_of=d.get("prev_as_of"),
        risk_free_rate_prev=d.get("risk_free_rate_prev"),
        iv_prev_source=d["iv_prev_source"],
        hv20_now=d.get("hv20_now"),
        hv20_prev=d.get("hv20_prev"),
        bid=d.get("bid"),
        ask=d.get("ask"),
        mid=d.get("mid"),
        volume=d.get("volume"),
        open_interest=d.get("open_interest"),
        risk_free_rate_source=d.get("risk_free_rate_source", "fixture"),
        quantity=float(d.get("quantity", 1.0)),
        multiplier=float(d.get("multiplier", 1.0)),
    )


def _surface_from_dict(d: Optional[dict]) -> Optional[VolSurfaceData]:
    if d is None:
        return None
    return VolSurfaceData(
        as_of=d["as_of"],
        expiries=list(d["expiries"]),
        strikes=[float(k) for k in d["strikes"]],
        matrix=[[float(v) for v in row] for row in d["matrix"]],
        data_source="synthetic",
    )


def load_fixture(
    name: str,
    *,
    fixtures_root: Optional[Path] = None,
) -> tuple[MarketSnapshot, Optional[VolSurfaceData]]:
    """Load ``{name}.json`` → ``(MarketSnapshot, VolSurfaceData | None)``."""
    root = fixtures_root or _FIXTURES_DIR
    path = root / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Synthetic fixture not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "snapshot" not in payload:
        raise ValueError(f"{path.name}: expected object with 'snapshot' key")
    snap = _snapshot_from_dict(payload["snapshot"], context=path.name)
    surface = _surface_from_dict(payload.get("surface"))
    return snap, surface


def list_fixtures(*, fixtures_root: Optional[Path] = None) -> list[str]:
    """Return market snapshot fixture stems (excludes manifests like historical_test_cases)."""
    root = fixtures_root or _FIXTURES_DIR
    if not root.exists():
        return []
    names: list[str] = []
    for path in sorted(root.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and "snapshot" in payload:
            names.append(path.stem)
    return names
