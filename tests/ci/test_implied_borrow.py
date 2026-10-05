"""Implied borrow rate: Task A4.3.

On a synthetic chain built from a known ``q``, ``imply_borrow_rate`` must
recover it within 1e-3; with fewer than 3 call/put pairs, the result must
fall back to the dividend yield and set ``borrow_unavailable``.
"""

from __future__ import annotations

import math
from datetime import date
from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))

from bootstrap import install

install()

from scipy.stats import norm

from explain_my_option.data.historical_chain import imply_borrow_rate

S = 100.0
R = 0.04
T = 0.5
Q_TRUE = 0.10
SIGMA = 0.30
EXPIRY = "2026-07-15"
AS_OF = date(2026, 1, 15)  # ~0.5y before EXPIRY


def _bs_price(K: float, *, call: bool) -> float:
    d1 = (math.log(S / K) + (R - Q_TRUE + 0.5 * SIGMA * SIGMA) * T) / (SIGMA * math.sqrt(T))
    d2 = d1 - SIGMA * math.sqrt(T)
    if call:
        return S * math.exp(-Q_TRUE * T) * norm.cdf(d1) - K * math.exp(-R * T) * norm.cdf(d2)
    return K * math.exp(-R * T) * norm.cdf(-d2) - S * math.exp(-Q_TRUE * T) * norm.cdf(-d1)


def _synthetic_rows(strikes: list[float]) -> list[dict]:
    rows: list[dict] = []
    for k in strikes:
        c = _bs_price(k, call=True)
        p = _bs_price(k, call=False)
        rows.append(
            {"expiration": EXPIRY, "strike": k, "call_put": "Call", "mid": c}
        )
        rows.append(
            {"expiration": EXPIRY, "strike": k, "call_put": "Put", "mid": p}
        )
    return rows


def test_imply_borrow_rate_recovers_known_q():
    rows = _synthetic_rows([80.0, 90.0, 100.0, 110.0, 120.0])
    result = imply_borrow_rate(rows, spot=S, rate=R, expiry=EXPIRY, as_of=AS_OF)
    assert not result.borrow_unavailable
    assert result.n_pairs_used == 5
    assert abs(result.q_implied - Q_TRUE) < 1e-3, result.q_implied
    assert result.borrow_regime == "elevated"  # 0.02 < 0.10 <= 0.20


def test_imply_borrow_rate_falls_back_below_three_pairs():
    rows = _synthetic_rows([95.0, 100.0])  # only 2 pairs
    result = imply_borrow_rate(
        rows, spot=S, rate=R, expiry=EXPIRY, as_of=AS_OF, fallback_dividend_yield=0.015
    )
    assert result.borrow_unavailable
    assert result.n_pairs_used == 2
    assert result.q_implied == 0.015
    assert result.borrow_regime == "normal"


def test_borrow_regime_bands():
    from explain_my_option.data.historical_chain import _borrow_regime

    assert _borrow_regime(0.005) == "normal"
    assert _borrow_regime(0.02) == "elevated"
    assert _borrow_regime(0.20) == "elevated"
    assert _borrow_regime(0.21) == "extreme"


def test_imply_borrow_rate_ignores_other_expiries():
    rows = _synthetic_rows([90.0, 100.0, 110.0])
    other_expiry_rows = []
    for r in rows:
        r2 = dict(r)
        r2["expiration"] = "2099-01-01"
        r2["mid"] = 999.0
        other_expiry_rows.append(r2)
    result = imply_borrow_rate(
        rows + other_expiry_rows, spot=S, rate=R, expiry=EXPIRY, as_of=AS_OF
    )
    assert result.n_pairs_used == 3


if __name__ == "__main__":
    test_imply_borrow_rate_recovers_known_q()
    test_imply_borrow_rate_falls_back_below_three_pairs()
    test_borrow_regime_bands()
    test_imply_borrow_rate_ignores_other_expiries()
    print("OK — implied borrow rate tests passed")
