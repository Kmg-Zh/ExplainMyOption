# PnL units (source of truth = `src/pricing/risk.py`)

## Takeaway

IV is stored as a **decimal** (0.25 = 25%). Vega is **per 1 vol point (0.01)**. Vega PnL is `vega * (d_vol / 0.01)`. Gamma PnL is `0.5 * gamma * d_spot²` (named row in the diagnostic report). Attribution uses **official FDM** Greeks (local vol or flat). Heston does not rewrite PnL. Live `d_vol` may come from an HV20 proxy.

## Details

From `price_and_attribute` / `attribute_pnl`:

```text
vega  = parallel implied-vol bump, scaled × 0.01     # $ per 1 vol point
d_vol = iv_now - iv_prev                             # decimal, e.g. 0.02 = +2 vol points
vega_pnl = vega * (d_vol / 0.01)

theta  = annual_theta / 365                          # $ per calendar day
theta_pnl = theta * dt_days

gamma_pnl = 0.5 * gamma * d_spot * d_spot

residual = total_pnl - (delta_pnl + gamma_pnl + vega_pnl + theta_pnl)
```

**When** the diagnostic report template is used, Gamma is shown as its own row; residual captures American EE, skew, and Taylor truncation — **not** the model-vs-mark gap (separate reconciliation section).

**Diagnose cue (not a router):** a large `|residual|` is a signal for the LLM to discuss unmodeled effects (American EE, dividends, HV20-as-IV). Do not branch the graph on residual (no EDGAR diamond).

**Methods:** shipped blotter is Greek-based (Taylor). Sequential full revaluation uses **t → S → σ → r** (`path_reprice` on the diagnostic pass). Do not call these Predict/Explain in product copy — [pnl-attribution-methods.md](pnl-attribution-methods.md).

## Mark reconciliation & IV noise band

When bid/ask quotes exist:

```text
iv_noise_band_pts = (½ · spread) / vega     # vega in $ per 1 vol point (0.01)
```

If `|Δσ_pts| ≤ iv_noise_band_pts`, IV moved inside the **noise band** — Vega narrative is not falsifiable from that quote. Implementation: `src/report/reconciliation.py`.

## Near-zero total PnL display

When `|total_pnl| < $5` (position-scaled), attribution **% shares** use sum of |components| instead of `% of total`.

Signs: call delta ∈ [0, 1], put delta ∈ [-1, 0]; long-vanilla vega ≥ 0.

## Display scale (position blotter)

`price_and_attribute` always attributes **1 option**. The product report (`src/report_generator.py`) is a **single-position blotter**: contract identity, quantity, market move, Greeks, factor PnL.

```text
display_pnl = engine_pnl * quantity * multiplier
```

Defaults are `quantity=1`, `multiplier=1` (per option). Set `multiplier=100` for a US listed lot. `--book` fans out per leg and rolls up; it is not cross-gamma.

**When** live marks (`option_price_now` / `option_price_prev`) are both positive, `price_and_attribute` inverts flat FDM vols so official NPV matches those marks (`diagnostics.mark_calibrated`). Then `total_pnl` equals mark-to-market ΔP (within solver tolerance). Local vol is deferred to surface diagnostics on that path. Synthetic fixtures with zero marks keep the vendor-IV / local-vol path unchanged.

## Not this repo (unless asked)

- Smile-based *rewrite* of the identity — local vol may *price* the two dates, but the factor split still uses this formula.

## Source

- `src/pricing/risk.py`, `src/pricing/facade.py`, `src/pricing/engines/fdm.py` (Aug 2026)
- Skill `pnl-attribution` · rule `quant-engine.mdc`
