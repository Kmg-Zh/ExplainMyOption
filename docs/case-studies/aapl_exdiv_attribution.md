# Case study: AAPL ex-div attribution (FO overlay, not an edge)

**Contract:** `AAPL 170C 2023-11-17` (American call)  
**As-of:** 2023-11-09 (day before ex-div 2023-11-10, $0.24 cash dividend)  
**Fixture:** `aapl_exdiv_2023`  
**Companion synthetic:** `deep_itm_exdiv` (deep ITM call, spot drop equals a $2 cash dividend)

This is an **attribution story** for a 1-day American option move around an ex-dividend window. It is **not** a claim that early exercise is mispriced, and not a trading alpha.

Official PnL stays **American FDM** Taylor. LSM / Heston stay diagnostic-only.

---

## What the overlay splits

When `flag_ex_div_window` is true, the residual drill adds a five-way FO overlay (code, not LLM):

| Piece | What it is | AAPL 2023-11-09 | Synthetic deep ITM |
|-------|------------|----------------:|-------------------:|
| (a) Spot drop vs dividend | ΔS versus next cash dividend | −$0.30 vs $0.24 (gap −$0.06) | −$2.00 vs $2.00 (gap $0) |
| (b1) Early exercise | `P_am_div − P_eu_div` (signed, same FDM grid + dividend schedule both sides) | +$0.0607 | +$1.8656 |
| (b2) Dividend PV effect | `P_eu_div − P_eu_nodiv` (signed) | −$0.2389 | −$1.9997 |
| (b, legacy) American vs European analytic (no div) | Cross-check only, kept for continuity: FDM American minus European **analytic**, no cash divs | $12.12 vs $12.30 (gap −$0.18) | $28.01 vs $28.14 (gap −$0.13) |
| (c) Vol | Taylor Vega PnL | −$0.28 (IV 28% → 18%) | $0 (IV unchanged) |
| (d) Residual | Taylor ε (official FDM ΔP minus Δ+Γ+V+Θ) | +$0.19 (~42% of \|model ΔP\|) | ~$0 |

`early_exercise_premium` is `P_am_div − P_eu_div`: American and European priced on the same FDM grid with the same discrete dividend schedule. It is reported signed and is not floored. An earlier version of this repo compared the American price against a European with **no** dividends, which mixes the early exercise value with the dividend's present-value effect and produced a value that was floored to $0 on both fixtures. The two effects are now reported separately as `early_exercise_premium` and `dividend_pv_effect`.

On both fixtures the corrected `early_exercise_premium` is materially positive (+$0.06 on AAPL, +$1.87 on the deep-ITM synthetic) — not the $0.00 the earlier, floored definition reported on both. `american_commentary` mentions early exercise when that premium is material (≥ $0.01) **and** not flagged `ee_premium_anomaly` (a negative premium below −1e-6·S, which would indicate an engine/grid inconsistency rather than a real signal — not observed on either fixture here).

---

## What Taylor misses

Greek-based (Taylor) attribution uses T−1 FDM Greeks × observed ΔS, Δσ, Δt. It does **not**:

- Isolate the cash-dividend jump from an ordinary spot move (a).
- Isolate American continuation vs a European (no-div) comparison (b).
- Capture higher-order / boundary effects when IV also collapses (AAPL residual ~42%).

On the synthetic, ΔS ≈ −dividend and vol is unchanged: Delta PnL ≈ model ΔP and residual is ~0. That is the control — Taylor can look clean when the only move is a dividend-sized spot drop.

On AAPL, IV crush is a first-class Taylor slice (Vega). The leftover residual is the honest unexplained bucket: short-dated ITM boundary, discrete dividend vs no-div European comparison, and truncation. It is **not** a signal to trade the call.

---

## Where the residual went (Task A5)

AAPL's 28% → 18% IV move is a 10 vol point move — large enough that
`taylor_second_order` (Layer 3, vanna/volga via bump-and-revalue on the
official FDM engine) is not noise. Numbers below are from a live run of
`tests/ci/fixtures/aapl_exdiv_2023.json` through `run_diagnostic_pass`
(`python -c` snippet in the commit that added this section):

| Term | \$ | % of \|ΔP\| |
|---|---:|---:|
| Model ΔP | −0.4508 | 100.0% |
| Vega PnL (first-order) | −0.2813 | 62.4% |
| Residual, first-order only (`ε_method` before Layer 3) | +0.1883 | 41.8% |
| Vanna PnL | −0.0181 | 4.0% |
| Volga PnL | +0.1684 | 37.4% |
| Residual, after Layer 3 (`ε_method − second_order_explained`) | +0.0381 | 8.4% |

`residual_reduction_pct` = 79.8%: volga alone accounts for 37.4% of what
the first-order blotter reported as unexplained. The remaining ~8.4%
residual is short-dated ITM boundary behaviour, the discrete-dividend vs
no-div European comparison (b, legacy above), and FDM truncation — the
same honest bucket described in "What Taylor misses," just smaller now
that the vol convexity term has been named rather than lumped in.

**Regime (A5.3):** `r_vol = 0.599` (volga against a small first-order Vega
PnL) exceeds the 0.35 threshold, so `taylor_regime = INVALID` on this
fixture — the Taylor split above is a reference view, not the headline;
`path_reprice`'s full revaluation is. `path_reprice` already runs on this
fixture regardless (severity above the 10% band, "What the diagnostic
tool does" below), so the headline was already correct here by
coincidence of which tool the severity gate picks — the regime flag is
what makes that choice principled instead of incidental.

---

## What the diagnostic tool does

AAPL residual is above the 10% severity band, so `path_reprice` takes the deep slot and `american_dividend_exercise_check` is **skipped with an explicit reason** (`path_reprice outranks ex-div window`). `taylor_second_order` (Layer 3, above) also runs regardless — it is free (A5.1) and no longer competes for that slot. The overlay still attaches so the split is visible.

On `deep_itm_exdiv` residual is tiny, so `american_dividend_exercise_check` **runs**. European analytic and American FDM prices still differ; that difference is diagnostic, not an edge.

---

## Language to avoid

Do not write that the desk “should have exercised,” that American FDM is cheap vs European, or that residual is alpha. The product explains a 1-day move. It does not predict the next print.

VW squeeze walkthrough: [vow_float_squeeze_2008.md](vow_float_squeeze_2008.md).
