"""Live-data hazards that broke the 9pm unattended runs.

Every 21:00 launchd run since 2026-09-16 failed on every leg with QuantLib's
"negative or null underlying given": Yahoo's history can end in a row whose
Close is NaN, and the loader took iloc[-1] blindly. A separate hazard rode
along: impliedVolatility=1e-05 is Yahoo's stale-quote sentinel, and a
pre-market run had cached it as the next day's t-1.
"""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

import numpy as np
import pandas as pd

from explain_my_option.data.cache import MIN_PLAUSIBLE_IV, load_t1, upsert_snapshot
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.data_loader import _clean_iv, latest_two_closes


def test_trailing_nan_close_is_dropped_not_used_as_spot():
    hist = pd.DataFrame({"Close": [330.0, 331.5, 336.13, np.nan]})
    assert latest_two_closes(hist) == (336.13, 331.5)


def test_interior_and_nonpositive_closes_are_skipped():
    hist = pd.DataFrame({"Close": [100.0, np.nan, 0.0, -1.0, 102.0, 103.0]})
    assert latest_two_closes(hist) == (103.0, 102.0)


def test_fewer_than_two_valid_closes_raises_the_real_cause():
    hist = pd.DataFrame({"Close": [np.nan, 336.13, np.nan]})
    try:
        latest_two_closes(hist)
    except RuntimeError as exc:
        assert "fewer than 2 valid daily closes" in str(exc)
    else:
        raise AssertionError("expected RuntimeError")


def test_sentinel_iv_is_not_a_reading():
    assert _clean_iv(1e-05) is None
    assert _clean_iv(0.0) is None
    assert _clean_iv(float("nan")) is None
    assert _clean_iv(MIN_PLAUSIBLE_IV) == MIN_PLAUSIBLE_IV
    assert _clean_iv(0.30) == 0.30


def test_sentinel_iv_snapshot_is_not_cached_and_good_t1_wins():
    snap, surf = load_fixture("flat_only")
    with TemporaryDirectory() as td:
        db = Path(td) / "market.sqlite"
        snap.as_of = "2026-09-16"
        assert upsert_snapshot(snap, surf, path=db) is True
        snap.as_of = "2026-09-17"
        snap.iv_now = 1e-05
        assert upsert_snapshot(snap, surf, path=db) is False
        loaded, _ = load_t1(
            snap.ticker, snap.expiry, snap.strike, snap.option_type, "2026-09-18", path=db
        )
        assert loaded is not None and loaded.as_of == "2026-09-16"


def test_sentinel_row_already_in_cache_is_skipped_on_read():
    """The row a pre-fix run already wrote must not be served as t-1."""
    import sqlite3, json
    from dataclasses import asdict

    snap, surf = load_fixture("flat_only")
    with TemporaryDirectory() as td:
        db = Path(td) / "market.sqlite"
        snap.as_of = "2026-09-16"
        upsert_snapshot(snap, surf, path=db)
        bad = asdict(snap)
        bad["as_of"], bad["iv_now"] = "2026-09-17", 1e-05
        with sqlite3.connect(db) as conn:
            conn.execute(
                "INSERT INTO snapshots VALUES (?,?,?,?,?,?,NULL)",
                (snap.ticker.upper(), snap.expiry, float(snap.strike),
                 snap.option_type, "2026-09-17", json.dumps(bad)),
            )
        loaded, _ = load_t1(
            snap.ticker, snap.expiry, snap.strike, snap.option_type, "2026-09-18", path=db
        )
        assert loaded is not None and loaded.as_of == "2026-09-16"


if __name__ == "__main__":
    test_trailing_nan_close_is_dropped_not_used_as_spot()
    test_interior_and_nonpositive_closes_are_skipped()
    test_fewer_than_two_valid_closes_raises_the_real_cause()
    test_sentinel_iv_is_not_a_reading()
    test_sentinel_iv_snapshot_is_not_cached_and_good_t1_wins()
    test_sentinel_row_already_in_cache_is_skipped_on_read()
    print("OK — data robustness (NaN close / sentinel IV) tests passed")
