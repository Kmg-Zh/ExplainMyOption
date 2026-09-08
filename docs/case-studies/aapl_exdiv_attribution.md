# Case study: AAPL ex-div attribution (FO overlay, not an edge)

**Contract:** `AAPL 170C 2023-11-17` (American call)  
**As-of:** 2023-11-09 (day before ex-div 2023-11-10, $0.24 cash dividend)  
**Fixture:** `aapl_exdiv_2023`  
**Companion synthetic:** `deep_itm_exdiv` (deep ITM call, spot drop equals a $2 cash dividend)

This is an **attribution story** for a 1-day American option move around an ex-dividend window. It is **not** a claim that early exercise is mispriced, and not a trading alpha.

Official PnL stays **American FDM** Taylor. LSM / Heston stay diagnostic-only.

---

## What the overlay splits

When `flag_ex_div_window` is true, the residual drill adds a four-way FO overlay (code, not LLM):

| Piece | What it is | AAPL 2023-11-09 | Synthetic deep ITM |
|-------|------------|----------------:|-------------------:|
| (a) Spot drop vs dividend | ΔS versus next cash dividend | −$0.30 vs $0.24 (gap −$0.06) | −$2.00 vs $2.00 (gap $0) |
| (b) American vs European | FDM American price minus European analytic **without** cash divs | $12.12 vs $12.30 (gap −$0.18) | $28.01 vs $28.14 (gap −$0.13) |
| (c) Vol | Taylor Vega PnL | −$0.28 (IV 28% → 18%) | $0 (IV unchanged) |
| (d) Residual | Taylor ε (official FDM ΔP minus Δ+Γ+V+Θ) | +$0.19 (~42% of \|model ΔP\|) | ~$0 |

Shipped `early_exercise_premium` is `max(0, American flat FDM − European analytic with no cash dividend)`. On these fixtures that floor is **$0** — American FDM *with* the cash dividend can print *below* a no-div European. The overlay still shows the signed AM−EU gap. `american_commentary` mentions early exercise **only** when that floored premium is material (≥ $0.01).

---

## What Taylor misses

Greek-based (Taylor) attribution uses T−1 FDM Greeks × observed ΔS, Δσ, Δt. It does **not**:

- Isolate the cash-dividend jump from an ordinary spot move (a).
- Isolate American continuation vs a European (no-div) comparison (b).
- Capture higher-order / boundary effects when IV also collapses (AAPL residual ~42%).

On the synthetic, ΔS ≈ −dividend and vol is unchanged: Delta PnL ≈ model ΔP and residual is ~0. That is the control — Taylor can look clean when the only move is a dividend-sized spot drop.

On AAPL, IV crush is a first-class Taylor slice (Vega). The leftover residual is the honest unexplained bucket: short-dated ITM boundary, discrete dividend vs no-div European comparison, and truncation. It is **not** a signal to trade the call.

---

## What the diagnostic tool does

AAPL residual is above the 20% severity band, so `path_reprice` takes the deep slot and `american_dividend_exercise_check` is **skipped with an explicit reason** (`path_reprice outranks ex-div window`). The overlay still attaches so the four-way split is visible.

On `deep_itm_exdiv` residual is tiny, so `american_dividend_exercise_check` **runs**. European analytic and American FDM prices still differ; that difference is diagnostic, not an edge.

---

## Language to avoid

Do not write that the desk “should have exercised,” that American FDM is cheap vs European, or that residual is alpha. The product explains a 1-day move. It does not predict the next print.

VW squeeze walkthrough: [vow_float_squeeze_2008.md](vow_float_squeeze_2008.md).
