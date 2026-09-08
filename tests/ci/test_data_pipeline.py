"""Market-data helpers: HV20 proxy and SQLite t-1 cache (no network)."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

from bootstrap import install

install()

from explain_my_option.data.cache import load_t1, upsert_snapshot
from explain_my_option.data.dividends import normalize_dividend_yield
from explain_my_option.data.realized import hv20_from_closes, iv_prev_from_hv20
from explain_my_option.data.synthetic import load_fixture
from explain_my_option.pricing.surface import parallel_shift_surface


def test_hv20_from_canned_returns():
    rng = np.random.default_rng(0)
    # Geometric random walk with a vol step-up in the last window.
    n = 40
    rets = np.concatenate(
        [rng.normal(0, 0.01, 20), rng.normal(0, 0.03, 19)]
    )
    closes = 100.0 * np.exp(np.cumsum(np.concatenate([[0.0], rets])))
    hv_now, hv_prev = hv20_from_closes(closes)
    assert hv_now is not None and hv_prev is not None
    assert hv_now > hv_prev
    iv_prev, d_proxy = iv_prev_from_hv20(0.25, hv_now, hv_prev)
    assert iv_prev > 0
    assert abs(d_proxy - (hv_now - hv_prev)) < 1e-12


def test_sqlite_round_trip(tmp_path=None):
    if tmp_path is None:
        with TemporaryDirectory() as td:
            _sqlite_round_trip(Path(td) / "market.sqlite")
        return
    _sqlite_round_trip(Path(tmp_path) / "market.sqlite")


def _sqlite_round_trip(db: Path) -> None:
    snap, surf = load_fixture("flat_only")
    snap.as_of = "2026-08-14"
    upsert_snapshot(snap, surf, path=db)
    loaded, _loaded_surf = load_t1(
        snap.ticker,
        snap.expiry,
        snap.strike,
        snap.option_type,
        "2026-08-15",
        path=db,
    )
    assert loaded is not None
    assert loaded.iv_now == snap.iv_now
    assert loaded.ticker == snap.ticker
    missing, _ = load_t1(
        snap.ticker,
        snap.expiry,
        snap.strike,
        snap.option_type,
        "2026-08-14",
        path=db,
    )
    assert missing is None


def test_normalize_dividend_yield_yahoo_percent_as_fraction():
    # Live smoke 2026-08-18: Yahoo returned 0.35 / 0.76 for AAPL / MSFT.
    q, rescaled = normalize_dividend_yield(0.35)
    assert rescaled and abs(q - 0.0035) < 1e-12
    q, rescaled = normalize_dividend_yield(0.76)
    assert rescaled and abs(q - 0.0076) < 1e-12
    q, rescaled = normalize_dividend_yield(0.0101)
    assert not rescaled and abs(q - 0.0101) < 1e-12
    q, rescaled = normalize_dividend_yield(0.0)
    assert not rescaled and q == 0.0
    q, rescaled = normalize_dividend_yield(4.5)
    assert rescaled and abs(q - 0.045) < 1e-12
    q, _ = normalize_dividend_yield(-1.0)
    assert q == 0.0


def test_parallel_shift_surface_floors():
    _, surf = load_fixture("calibration_ok")
    assert surf is not None
    shifted = parallel_shift_surface(surf, -0.50)
    for row in shifted.matrix:
        assert all(v >= 1e-4 for v in row)


if __name__ == "__main__":
    test_hv20_from_canned_returns()
    test_sqlite_round_trip()
    test_normalize_dividend_yield_yahoo_percent_as_fraction()
    test_parallel_shift_surface_floors()
    print("OK — data pipeline checks passed")
