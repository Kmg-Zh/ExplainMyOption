# Live book run — 2026-11-09

Run `2026-11-09-1794276902`. 8/8 legs diagnosed, 0 settled at expiry, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=11`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-09` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$773.5000`
* **Total Model PnL**: `+$773.5000`
* **Aggregate model vs mark gap**: `+$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `+$665.0000` |
| 2 | `SPY 715P 2026-11-20` | `+$481.5000` |
| 3 | `JPM 340P 2026-12-18` | `-$442.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$807.6163` |
| Gamma | `-$67.5265` |
| Vega | `+$65.5959` |
| Theta | `+$34.5634` |
| Residual | `-$66.7491` |

### Notable underlyings

* **SPY**: `+$487.0000` aggregate option PnL
* **AAPL**: `+$425.0000` aggregate option PnL
* **JPM**: `-$150.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-09` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$665.0000` (+33.1%)
* **Model ΔP**: `+$665.0000`
* **Primary drivers**: **Delta PnL** (+100.5%) and **Theta decay** (-11.2%) and **Gamma PnL** (+6.6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is dominated by the stock’s upward spot move, with the option revalued primarily through Delta and supported secondarily by positive Gamma. Theta drag offset part of the gain, while the remaining gap is small and consistent with higher-order model effects rather than a separate catalyst. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by the observation lock and the lack of retrieved headlines, so there is no independent catalyst check. The attribution is still clear because the modeled revaluation is led by spot sensitivity, the residual is low, and the American premium is not material.

---

## 2. Observation Lock

* **As-of**: `2026-11-09` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.3%)
* **IV move**: +4.23 vol pts vs noise band ±5.72 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-06`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$665.0000`
* **Model ΔP (engine)**: `+$665.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$659.7707`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$5.2293` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$668.6230` | +100.5% | Stock moved from $342.37 to $350.69 (+8.3200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$43.6200` | +6.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$21.6996` | +3.3% | IV moved +1.17 vol pts (32.78% → 33.95%) |
| **Theta decay (Δt · Theta)** | `-$74.1719` | -11.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$5.2293` | +0.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$665.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$5.2293` (0.8% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$5.6049`
* Combined: `-$5.6049` | Residual after: `+$10.8342`

### Ex-div attribution overlay (official PnL stays the American FDM Taylor blotter)
* **Spot drop vs dividend** (per share): spot `+$8.3200` vs next cash dividend `+$0.2700` (gap `+$8.5900`)
* **American FDM vs European analytic (no cash div, cross-check, per option)**: `+$26.7250` vs `+$26.9378` (gap `-$0.2128`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored, per option): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs, per option): `-$0.2138`
* **Dividend coverage** (dividend / time value): `0.26` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$21.6996`
* **Residual (Taylor ε)**: `+$5.2293`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Watch for Taylor truncation and quote noise if the spot move continues to widen the modeled gap from the full revaluation.
* No early-exercise issue is indicated here; the dividend does not cover the remaining time value, so this remains a carry and decay case rather than an assignment case.
* **Assignment watch**: ex-div `2026-11-12` — Dividend coverage 0.26 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-09` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$240.0000` (+60.0%)
* **Model ΔP**: `-$240.0000`
* **Primary drivers**: **Delta PnL** (-120.9%) and **Theta decay** (+31.0%) and **Gamma PnL** (-30.4%).
* **Verdict**: The move is dominated by the stock rally into a short call position, with second-order gamma effects and smaller offsetting theta and vega contributions shaping the full revaluation. The residual is small, so the Greek-based explanation is broadly consistent with the model price change. No relevant headlines were retrieved, so there is no separate catalyst layer to add beyond the spot-driven repricing.
* **Confidence**: **Medium** — Confidence is medium because observation quality is reliable and the attribution coverage is high, but the residual is not zero and the move sits in a short-dated American option where convexity and boundary effects can matter. The absence of relevant headlines means there is no external catalyst confirmation, and the analysis should stay at the modeled factor level.

---

## 2. Observation Lock

* **As-of**: `2026-11-09` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.7%)
* **IV move**: -1.40 vol pts vs noise band ±0.62 pts (exceeds noise band)
* **Prior observation**: `2026-11-06`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$240.0000`
* **Model ΔP (engine)**: `-$240.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$249.3068`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$9.3068` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$290.0768` | -120.9% | Stock moved from $342.37 to $350.69 (+8.3200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$72.9122` | -30.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$39.2247` | +16.3% | IV moved -1.58 vol pts (26.20% → 24.62%) |
| **Theta decay (Δt · Theta)** | `+$74.4574` | +31.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$9.3068` | +3.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$240.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$9.3068` (3.9% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$6.0552` | other second-order: `-$0.1877`
* Combined: `+$5.8675` | Residual after: `+$3.4394`

### Ex-div attribution overlay (official PnL stays the American FDM Taylor blotter)
* **Spot drop vs dividend** (per share): spot `+$8.3200` vs next cash dividend `+$0.2700` (gap `+$8.5900`)
* **American FDM vs European analytic (no cash div, cross-check, per option)**: `+$6.4000` vs `+$6.5246` (gap `-$0.1246`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored, per option): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs, per option): `-$0.1248`
* **Dividend coverage** (dividend / time value): `0.05` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$39.2247`
* **Residual (Taylor ε)**: `+$9.3068`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* Recheck whether a larger spot continuation or reversal would push the position further into higher-order convexity, where the Taylor approximation can widen.
* Because there are no relevant headlines or named microstructure tokens, do not infer a squeeze, borrow stress, or IV-crush narrative from this tape.
* **Assignment watch**: ex-div `2026-11-12` — Dividend coverage 0.05 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-09` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$292.5000` (+31.2%)
* **Model ΔP**: `+$292.5000`
* **Primary drivers**: **Delta PnL** (+117.2%) and **Vega PnL** (-15.5%) and **Theta decay** (-14.8%).
* **Verdict**: The revaluation was driven primarily by the underlying rally, with gamma adding support and the vol and theta buckets offsetting part of the gain. The residual is minimal, so the model story is clean; there is no separate news catalyst to layer on, and the early-exercise premium remains negligible at current marks.
* **Confidence**: **Medium** — The attribution is well covered and the observation is reliable, but the desk asked for a medium-confidence call and there are no headlines to cross-check a catalyst. The residual is small, so the main uncertainty is just normal Taylor approximation noise rather than a competing event story.

---

## 2. Observation Lock

* **As-of**: `2026-11-09` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.7%)
* **IV move**: -1.04 vol pts vs noise band ±0.79 pts (exceeds noise band)
* **Prior observation**: `2026-11-06`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$292.5000`
* **Model ΔP (engine)**: `+$292.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$293.6985`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.1985` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$342.9104` | +117.2% | Stock moved from $334.49 to $342.08 (+7.5900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$39.4313` | +13.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$45.3945` | -15.5% | IV moved -1.01 vol pts (25.45% → 24.44%) |
| **Theta decay (Δt · Theta)** | `-$43.2488` | -14.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.1985` | -0.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$292.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.1985` (0.4% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$1.5616`
* Combined: `-$1.5616` | Residual after: `+$0.3631`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* Watch whether the next move is still well described by the same factor mix or whether second-order effects start to matter more as spot shifts.
* No borrow, squeeze, or IV-crush readthrough is supported here; there are no relevant headlines to validate a separate catalyst story.

---

### Position 4 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-09` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$442.5000` (-34.0%)
* **Model ΔP**: `-$442.5000`
* **Primary drivers**: **Delta PnL** (-96.0%) and **Gamma PnL** (+10.0%) and **Theta decay** (-7.6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained first by the put’s negative delta reacting to the higher spot close, with gamma partially offsetting and theta plus a small residual adding to the repricing. Because observation is locked and no relevant headlines were retrieved, there is no separate catalyst layer to add; this is a clean factor-led revaluation rather than a news-driven gap. The American premium remains small, so early exercise is not a material part of the story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is internally consistent and the residual is low, but the observation flag is not reliable and the catalyst search was skipped under the lock, so the diagnosis should stay at the factor level. Vega narrative is also suppressed by the code, which further limits any broader event interpretation.

---

## 2. Observation Lock

* **As-of**: `2026-11-09` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 15.7%)
* **IV move**: -0.99 vol pts vs noise band ±1.53 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-06`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$442.5000`
* **Model ΔP (engine)**: `-$442.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$440.8609`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.6391` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.4%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$424.6987` | -96.0% | Stock moved from $334.49 to $342.08 (+7.5900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$44.4193` | +10.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$26.8247` | -6.1% | IV moved -0.60 vol pts (22.89% → 22.29%) |
| **Theta decay (Δt · Theta)** | `-$33.7567` | -7.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.6391` | -0.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$442.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.6391` (0.4% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$1.1843`
* Combined: `-$1.1843` | Residual after: `-$0.4548`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Check whether the full-surface reprice stays close to the current model move if spot continues to gap or if the residual widens.
* Monitor dividend and carry context for any future early-exercise assessment, but the current premium is not material enough to drive the result.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-09` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$481.5000` (-76.4%)
* **Model ΔP**: `+$481.5000`
* **Primary drivers**: **Delta PnL** (+98.5%) and **Gamma PnL** (-28.5%) and **Theta decay** (+26.5%).
* **Verdict**: The move is dominated by the option's negative delta responding to the underlying rally, with the short-put mark falling as spot pushed higher. The second-order Taylor buckets add context, but the headline story remains the spot-driven revaluation; the remaining gap is consistent with higher-order convexity and model truncation rather than a separate catalyst. No relevant headlines were retrieved, so there is no Layer B event to attach to this run.
* **Confidence**: **Medium** — Confidence is medium because the blotter is reliable and the dominant modeled driver is clear, but the residual is not negligible and the diagnostic is a reference-style Greek decomposition rather than a pure mark-only story. There are no retrieved headlines or named microstructure tags, so there is no external catalyst to confirm or challenge the factor view.

---

## 2. Observation Lock

* **As-of**: `2026-11-09` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.0%)
* **IV move**: -1.60 vol pts vs noise band ±0.07 pts (exceeds noise band)
* **Prior observation**: `2026-11-06`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$481.5000`
* **Model ΔP (engine)**: `+$481.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$548.0139`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$66.5139` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (13.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$474.1527` | +98.5% | Stock moved from $735.29 to $752.69 (+17.4000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$137.1471` | -28.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$83.2580` | +17.3% | IV moved -1.74 vol pts (25.54% → 23.80%) |
| **Theta decay (Δt · Theta)** | `+$127.7504` | +26.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$66.5139` | -13.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$481.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$66.5139` (13.8% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$23.9227` | other second-order: `-$0.9950`
* Combined: `-$24.9177` | Residual after: `-$41.5962`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$131.4528`
* **spot**: `+$308.2260`
* **vol**: `+$41.9982`
* **rate**: `+$0.0765`
* Step sum: `+$481.7534` | Model ΔP: `+$481.5000` | Audit residual: `-$0.2534`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* Monitor whether the full-surface reprice or higher-order convexity would shrink the residual versus the reference Greek decomposition.
* Keep in mind the American early-exercise premium is negligible here, so dividend or assignment effects are not a meaningful part of the diagnosis.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-09` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$5.5000` (+91.7%)
* **Model ΔP**: `+$5.5000`
* **Primary drivers**: **Gamma PnL** (+28.1%) and **Delta PnL** (+27.4%) and **Vega PnL** (-10.2%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is dominated by gamma, with spot rising enough to revalue the deep out-of-the-money call through convexity rather than simple directional exposure. The residual is large relative to the model move, which is consistent with higher-order truncation and path effects in the full revaluation; there is no headline-supported catalyst layer to add here. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by the large method residual, the observation lock, and the absence of relevant headlines. The attribution still cleanly points to gamma as the dominant modeled factor, but the gap versus the Taylor buckets means the revaluation should be read as a model diagnosis rather than a fully explained tape story.

---

## 2. Observation Lock

* **As-of**: `2026-11-09` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 8.7%)
* **IV move**: -1.88 vol pts vs noise band ±0.09 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-06`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$5.5000`
* **Model ΔP (engine)**: `+$5.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$17.6322`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$12.1322` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (220.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$13.7013` | +27.4% | Stock moved from $735.29 to $752.69 (+17.4000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$14.0618` | +28.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$5.0958` | -10.2% | IV moved -1.64 vol pts (16.16% → 14.52%) |
| **Theta decay (Δt · Theta)** | `-$5.0351` | -10.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$12.1322` | -24.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$5.5000** | **+11.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$12.1322` (220.6% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 1.03).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (vanna, volga) — reference only, see Regime above
* Vanna PnL: `-$15.1425` | Volga PnL: `+$1.6635`
* Combined: `-$13.4790` | Residual after: `+$1.3468`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$4.0708`
* **spot**: `+$20.9885`
* **vol**: `-$11.4234`
* **rate**: `+$0.0134`
* Step sum: `+$5.5077` | Model ΔP: `+$5.5000` | Audit residual: `-$0.0077`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Watch whether the full revaluation continues to diverge from the Taylor buckets as spot and expiry proximity change, since convexity and higher-order terms can remain material.
* No Layer B catalyst should be inferred from this run: there were no relevant headlines, so borrow, squeeze, or implied-vol narratives are not supported here.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-09` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$12.5000` (+8.7%)
* **Model ΔP**: `+$12.5000`
* **Primary drivers**: **Delta PnL** (+180.0%) and **Theta decay** (-86.8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The option was driven mainly by the underlying’s rise, with gamma providing a small convexity lift and theta decay offsetting part of the move. The residual is minor, so the model revaluation is well explained by the spot change rather than by a separate catalyst. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is internally consistent and the residual is small, but observation quality is flagged as unreliable and the run suppresses a Vega narrative. There are no relevant headlines or microstructure tags, so Layer B cannot add a catalyst explanation.

---

## 2. Observation Lock

* **As-of**: `2026-11-09` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 13.5%)
* **IV move**: +0.34 vol pts vs noise band ±3.67 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-06`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$12.5000`
* **Model ΔP (engine)**: `+$12.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$12.3478`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.1522` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$22.4962` | +180.0% | Stock moved from $45.69 to $46.06 (+0.3700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.9763` | +7.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.2756` | -2.2% | IV moved -0.08 vol pts (30.25% → 30.17%) |
| **Theta decay (Δt · Theta)** | `-$10.8491` | -86.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.1522` | +1.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$12.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.1522` (1.2% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.0091`
* Combined: `+$0.0091` | Residual after: `+$0.1431`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Check whether the full-surface reprice or boundary effects materially change the modeled spot-led attribution.
* Given the lack of relevant headlines, keep monitoring for any later liquidity or borrow developments before adding a tape-based explanation.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-09` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$1.0000` (-28.6%)
* **Model ΔP**: `-$1.0000`
* **Primary drivers**: **Vega PnL** (-99.6%) and **Theta decay** (-58.3%) and **Delta PnL** (+50.8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven primarily by the drop in implied volatility, with spot strength and second-order spot convexity only partially offsetting the move. The full revaluation is the most reliable read here because the observation lock and data-quality flags suppress a richer catalyst story, and the move should be treated as a model repricing rather than a news-led revaluation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is capped by the observation flag and the explicit instruction to suppress a Vega narrative, even though the quant engine still identifies Vega as the dominant modeled factor. The residual is small, the spot move is modest, and there are no retrieved headlines or named microstructure tokens to support a separate catalyst explanation.

---

## 2. Observation Lock

* **As-of**: `2026-11-09` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 120.0%)
* **IV move**: -10.94 vol pts vs noise band ±20.76 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-06`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$1.0000`
* **Model ΔP (engine)**: `-$1.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$1.0463`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0463` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.6%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.5081` | +50.8% | Stock moved from $1.45 to $1.50 (+0.0500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0241` | +2.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.9958` | -99.6% | IV moved -11.40 vol pts (187.28% → 175.88%) |
| **Theta decay (Δt · Theta)** | `-$0.5828` | -58.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0463` | +4.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$1.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0463` (4.6% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.1040` | Volga PnL: `+$0.0735`
* Combined: `-$0.0305` | Residual after: `+$0.0768`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Check whether the model-to-market gap stays small if the surface is rechecked with a fuller reprice, since the current attribution is a reference view under a flat-vol setup.
* With no retrieved headlines or named tape mechanism, avoid layering in squeeze, borrow, or IV-crush language unless fresh evidence appears.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0875 | level_proxy(t) = 0.1919
* Δskew = +0.0028 | Δlevel = -0.0174
* Put 715 delta=-0.0994 | Call 795 delta=0.0170
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
