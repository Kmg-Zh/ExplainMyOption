"""Upsert today's live snapshot into the local SQLite cache.

    python -m src.data.cache_cli AAPL
    python -m src.data.cache_cli AAPL --type put --strike 180
"""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cache a live option snapshot")
    parser.add_argument("ticker")
    parser.add_argument("--type", dest="option_type", default="call", choices=["call", "put"])
    parser.add_argument("--strike", type=float, default=None)
    parser.add_argument("--expiry", default=None)
    args = parser.parse_args(argv)

    from explain_my_option.data.cache import upsert_snapshot
    from explain_my_option.data_loader import load_market_data

    data = load_market_data(
        args.ticker,
        option_type=args.option_type,
        strike=args.strike,
        expiry=args.expiry,
    )
    upsert_snapshot(data.snapshot, data.surface)
    print(
        f"cached {data.snapshot.ticker} {data.snapshot.strike:g} "
        f"{data.snapshot.option_type} exp {data.snapshot.expiry} "
        f"as_of={data.snapshot.as_of}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
