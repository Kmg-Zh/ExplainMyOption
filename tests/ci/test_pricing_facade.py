"""Synthetic-first verification of the FDM pricing facade (no network)."""

from __future__ import annotations

from pathlib import Path
import sys

_TESTS_DIR = Path(__file__).resolve().parents[1]
if str(_TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(_TESTS_DIR))


import math

from bootstrap import install

install()

from explain_my_option.paths import GOLDEN_DIR

from explain_my_option.data.synthetic import list_fixtures, load_fixture
from explain_my_option.pricing.analysis_api import compare_to_official
from ci.engine_config import engine_config_for_tests
from explain_my_option.pricing.facade import price_and_attribute
from explain_my_option.pricing.ql_engine import price_european_flat
from explain_my_option.report_generator import build_quant_section, scale_pnl

CFG = engine_config_for_tests()


def _reconciles(pnl, tol: float = 1e-9) -> bool:
    recon = (
        pnl.delta_pnl
        + pnl.gamma_pnl
        + pnl.vega_pnl
        + pnl.theta_pnl
        + pnl.residual_pnl
    )
    return abs(recon - pnl.total_pnl) < tol


def test_all_fixtures_reconcile():
    names = list_fixtures()
    assert names, "expected synthetic fixtures under tests/ci/fixtures/"
    for name in names:
        snap, surf = load_fixture(name)
        result = price_and_attribute(snap, surf, config=CFG)
        assert _reconciles(result.pnl), f"{name}: PnL does not reconcile"
        assert result.diagnostics.data_source == "synthetic"
        assert result.diagnostics.engine in ("fdm_local_vol", "fdm_flat")


def test_calibration_ok_heston_converges():
    snap, surf = load_fixture("calibration_ok")
    result = price_and_attribute(snap, surf, config=CFG)
    assert result.surface_diagnostics is not None
    sd = result.surface_diagnostics
    assert sd.heston_params is not None, "Heston should calibrate on known-good fixture"
    assert sd.heston_rmse is not None and sd.heston_rmse < 0.05
    assert "heston_calibration_failed" not in sd.limitations
    assert "surface_unavailable" not in sd.limitations
    assert result.greeks_now.price > 0


def test_thin_surface_fails_soft():
    snap, surf = load_fixture("thin_surface")
    result = price_and_attribute(snap, surf, config=CFG)
    assert result.surface_diagnostics is not None
    lim = result.surface_diagnostics.limitations
    assert "surface_unavailable" in lim or "heston_calibration_failed" in lim
    assert result.diagnostics.engine == "fdm_flat"
    assert result.diagnostics.local_vol_used is False
    assert "local_vol_failed" in result.diagnostics.limitations
    assert _reconciles(result.pnl)


def test_flat_only_no_surface_block():
    snap, surf = load_fixture("flat_only")
    assert surf is None
    result = price_and_attribute(snap, surf, config=CFG)
    assert result.surface_diagnostics is None
    assert result.diagnostics.engine == "fdm_flat"
    assert result.diagnostics.local_vol_used is False
    assert "local_vol_failed" not in result.diagnostics.limitations
    assert _reconciles(result.pnl)


def test_european_fdm_matches_analytic():
    snap, _ = load_fixture("flat_only")
    snap.exercise_style = "european"
    result = price_and_attribute(snap, None, config=CFG)
    eu = price_european_flat(
        spot=snap.spot_now,
        strike=snap.strike,
        rate=snap.risk_free_rate,
        dividend_yield=snap.dividend_yield,
        vol=snap.iv_now,
        expiry=snap.expiry,
        eval_date=snap.as_of or "2026-08-14",
        option_type=snap.option_type,  # type: ignore[arg-type]
    )
    assert abs(result.greeks_now.price - eu.price) / max(eu.price, 1e-8) < 0.03


def test_american_put_div_ee_premium():
    snap, surf = load_fixture("american_put_div")
    result = price_and_attribute(snap, surf, config=CFG)
    assert result.diagnostics.engine == "fdm_flat"
    assert _reconciles(result.pnl)
    assert "discrete_dividends_ignored" not in result.diagnostics.limitations
    assert result.greeks_now.price > 0


def test_compare_to_official_records_engine():
    snap, surf = load_fixture("flat_only")
    cc = compare_to_official(snap, surf, config=CFG)
    assert cc.engine_used_for_official == "fdm_flat"
    assert cc.official_price > 0
    assert cc.lsm_bs is not None
    rel = abs(cc.lsm_bs - cc.official_price) / max(cc.official_price, 1e-8)
    assert rel < 0.35


def _mask_optimizer_lines(text: str) -> str:
    """Heston calibration is a numerical optimizer: its output varies at ~1e-3
    across BLAS/platform builds, so pin the line's presence, not its digits."""
    import re

    return "\n".join(
        re.sub(r"-?\d+\.\d+(e-?\d+)?", "<num>", ln) if ln.startswith("- Heston") else ln
        for ln in text.splitlines()
    )


def test_golden_quant_reports():
    golden_dir = GOLDEN_DIR
    golden_dir.mkdir(exist_ok=True)
    from explain_my_option.pricing.demo_report import render_fixture

    for name in ("vol_crush", "spot_gap"):
        text = render_fixture(name, config=CFG)
        path = golden_dir / f"{name}.md"
        if not path.exists():
            path.write_text(text)
        expected = path.read_text()
        assert _mask_optimizer_lines(expected) == _mask_optimizer_lines(text), f"golden drift in {name}; regenerate tests/ci/golden/{name}.md"


def test_blotter_scales_quantity_not_engine():
    snap, surf = load_fixture("vol_crush")
    result = price_and_attribute(snap, surf, config=CFG)
    per_option = result.pnl.total_pnl
    one = build_quant_section(snap, result)
    assert "| Quantity | 1 |" in one
    snap.quantity = 2.0
    two = build_quant_section(snap, result)
    scaled = scale_pnl(result.pnl, 2.0)
    assert result.pnl.total_pnl == per_option
    assert "| Quantity | 2 |" in two
    assert two != one
    assert f"{abs(scaled.total_pnl):,.4f}" in two
    assert abs(scaled.total_pnl - 2.0 * per_option) < 1e-12


def test_mark_calibration_aligns_model_to_mid():
    """Live-style marks: invert flat IV so model P&L equals mark P&L.

    Product path (src/pricing/calibrate.py). Synthetic fixtures leave marks at
    0 and skip this; this test injects marks so the calibration branch runs.
    """
    from dataclasses import replace

    snap, surf = load_fixture("flat_only")
    # First pass under vendor IV → known model prices at those vols.
    baseline = price_and_attribute(snap, surf, config=CFG)
    mark_now = baseline.greeks_now.price
    mark_prev = baseline.greeks_prev.price
    assert mark_now > 0 and mark_prev > 0

    # Poison vendor IVs; keep the same market marks. Calibration must recover.
    poisoned = replace(
        snap,
        iv_now=max(snap.iv_now * 1.35, snap.iv_now + 0.08),
        iv_prev=max(snap.iv_prev * 0.70, 0.05),
        option_price_now=mark_now,
        option_price_prev=mark_prev,
        data_source="yfinance",  # mark path is for live-style snapshots
    )
    result = price_and_attribute(poisoned, None, config=CFG)
    assert result.diagnostics.mark_calibrated is True
    assert "mark_calibrated" in result.diagnostics.limitations
    assert abs(result.greeks_now.price - mark_now) < 1e-3
    assert abs(result.greeks_prev.price - mark_prev) < 1e-3
    mark_pnl = mark_now - mark_prev
    assert abs(result.pnl.total_pnl - mark_pnl) < 1e-3
    assert _reconciles(result.pnl)


def test_fixtures_without_marks_skip_calibration():
    snap, surf = load_fixture("vol_crush")
    assert snap.option_price_now == 0.0
    result = price_and_attribute(snap, surf, config=CFG)
    assert result.diagnostics.mark_calibrated is False
    assert "mark_calibrated" not in result.diagnostics.limitations
    assert "iv_calibration_skipped_no_mark" not in result.diagnostics.limitations
    assert _reconciles(result.pnl)


if __name__ == "__main__":
    test_all_fixtures_reconcile()
    test_calibration_ok_heston_converges()
    test_thin_surface_fails_soft()
    test_flat_only_no_surface_block()
    test_european_fdm_matches_analytic()
    test_american_put_div_ee_premium()
    test_compare_to_official_records_engine()
    test_golden_quant_reports()
    test_blotter_scales_quantity_not_engine()
    test_mark_calibration_aligns_model_to_mid()
    test_fixtures_without_marks_skip_calibration()
    print("OK — synthetic facade checks passed")
