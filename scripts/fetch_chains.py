#!/usr/bin/env python3
"""Fetch the two verified real historical cases (Task A4.5) and commit slices.

Queries DoltHub + yfinance live (the DoltHub API is slow -- expect a couple
of minutes per case) and writes the resulting ``MarketSnapshot`` as a small
JSON slice under ``tests/ci/fixtures/historical/``. Not bulk data: one
snapshot per case, not the raw day chains.

Usage::

    python scripts/fetch_chains.py                 # both verified cases
    python scripts/fetch_chains.py gme_squeeze_2021_real
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "src"))
sys.path.insert(0, str(_REPO_ROOT / "tests"))

from bootstrap import install  # noqa: E402

install()

from explain_my_option.data.historical_chain import HistoricalChainMarketLoader  # noqa: E402

OUT_DIR = _REPO_ROOT / "tests" / "ci" / "fixtures" / "historical"

# A4.5: the only two confirmed convertible cases -- do not add others here
# without independently re-verifying convertibility per docs/dev/DATA_SOURCES.md.
CASES = {
    "gme_squeeze_2021_real": dict(
        ticker="GME",
        option_type="put",
        strike=55.0,
        expiry="2021-02-19",
        as_of="2021-01-25",
        prev_as_of="2021-01-22",
    ),
    "aapl_exdiv_2023_real": dict(
        ticker="AAPL",
        option_type="call",
        strike=180.0,
        expiry="2023-11-24",
        as_of="2023-11-09",
        prev_as_of="2023-11-08",
    ),
}


def fetch_one(name: str) -> None:
    params = CASES[name]
    loader = HistoricalChainMarketLoader(
        as_of=params["as_of"], prev_as_of=params["prev_as_of"]
    )
    print(f"Fetching {name} ({params['ticker']} {params['expiry']} "
          f"{params['strike']}{params['option_type'][0].upper()})...")
    data = loader.load(
        ticker=params["ticker"],
        option_type=params["option_type"],
        strike=params["strike"],
        expiry=params["expiry"],
    )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"{name}.json"
    payload = {"snapshot": asdict(data.snapshot)}
    out_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"  wrote {out_path.relative_to(_REPO_ROOT)}")
    print(f"  spot_now={data.snapshot.spot_now} spot_prev={data.snapshot.spot_prev}")
    print(f"  iv_now={data.snapshot.iv_now:.4f} iv_prev={data.snapshot.iv_prev:.4f}")
    print(f"  q_implied={data.snapshot.dividend_yield:.4f}")


def main(argv: list[str]) -> int:
    names = argv or list(CASES.keys())
    unknown = [n for n in names if n not in CASES]
    if unknown:
        print(f"Unknown case(s): {unknown}. Known: {list(CASES.keys())}", file=sys.stderr)
        return 1
    for name in names:
        fetch_one(name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
