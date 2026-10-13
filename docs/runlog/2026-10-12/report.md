# Live book run — 2026-10-12

Run `2026-10-12-1791854108`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=11`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-12` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$120.5000`
* **Total Model PnL**: `-$120.5000`
* **Aggregate model vs mark gap**: `-$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `+$262.5000` |
| 2 | `JPM 350P 2026-10-23` | `-$192.5000` |
| 3 | `AAPL 350C 2026-11-20` | `-$125.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$63.4520` |
| Gamma | `+$5.9917` |
| Vega | `-$76.6433` |
| Theta | `-$119.3076` |
| Residual | `+$6.0072` |

### Notable underlyings

* **JPM**: `-$217.0000` aggregate option PnL
* **AAPL**: `+$137.5000` aggregate option PnL
* **SPY**: `-$53.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$262.5000` (+>1000%)
* **Model ΔP**: `+$262.5000`
* **Primary drivers**: **Delta PnL** (83%) and **Theta decay** (13%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained primarily by the underlying rally feeding through the option’s positive directional exposure, with gamma adding a small convexity tail. Theta decay offset part of that gain, while the residual stays small enough to read as normal model noise rather than a separate story. There is no supported Layer B catalyst here: the run has no retrieved headlines, and the observation lock means we should not invent a squeeze, borrow, or implied-volatility narrative. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by the unreliable observation flag and the absence of headlines, but the attribution is still clear because the dominant modeled factor is explicit and the residual is low. The ex-div and American-vs-European checks do not indicate a material early-exercise effect, so the carry explanation remains secondary.

---

## 2. Observation Lock

* **As-of**: `2026-10-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.6%)
* **IV move**: +0.69 vol pts vs noise band ±1.10 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$262.5000`
* **Model ΔP (engine)**: `+$262.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$261.1307`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.3693` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.5%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$296.4824` | +112.9% | Stock moved from $336.64 to $340.97 (+4.3300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$11.0624` | +4.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.9353` | -0.4% | IV moved -0.02 vol pts (28.83% → 29.52%) |
| **Theta decay (Δt · Theta)** | `-$45.4788` | -17.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.3693` | +0.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$262.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.3693` (0.5% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0005`
* Combined: `+$0.0005` | Residual after: `+$2.6245`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$4.3300` vs next cash dividend `+$0.2700` (gap `+$4.6000`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$21.9500` vs `+$22.0567` (gap `-$0.1067`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1074`
* **Dividend coverage** (dividend / time value): `0.05` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$0.0094`
* **Residual (Taylor ε)**: `+$0.0137`
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
* Watch whether a larger spot gap or a full-surface reprice would change the convexity balance more than the current Taylor view suggests.
* Verify any future tape for borrow stress, squeeze conditions, or implied volatility shifts before adding a Layer B explanation.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.05 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$125.0000` (->1000%)
* **Model ΔP**: `-$125.0000`
* **Primary drivers**: **Delta PnL** (71%) and **Theta decay** (19%) and **Gamma PnL** (6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven mainly by the underlying rally against a short call, with second-order curvature and time decay contributing smaller offsets. The residual is small, so the Taylor view is broadly consistent with the full revaluation; with no retrieved headlines and observation locked, there is no separate catalyst layer to add. The American setup is a carry and theta case rather than an early-exercise case. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The driver split is internally coherent and the residual is low, but observation reliability is not strong and the feed notes a mark-calibrated limitation. Vega narrative is suppressed by the code, and there are no usable headlines, so the diagnosis stays at the coarse factor level rather than reaching for a finer event story.

---

## 2. Observation Lock

* **As-of**: `2026-10-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.9%)
* **IV move**: +0.25 vol pts vs noise band ±0.35 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$125.0000`
* **Model ΔP (engine)**: `-$125.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$128.1542`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$3.1542` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.5%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$152.7738` | +122.2% | Stock moved from $336.64 to $340.97 (+4.3300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$12.3878` | +9.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$4.2077` | +3.4% | IV moved +0.10 vol pts (25.87% → 26.13%) |
| **Theta decay (Δt · Theta)** | `+$41.2151` | -33.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$3.1542` | -2.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$125.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$3.1542` (2.5% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0024`
* Combined: `+$0.0024` | Residual after: `+$1.2476`

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
* Watch whether a fuller reprice or higher-order convexity would meaningfully change the attribution if the spot move extends.
* Keep the dividend and remaining time value in view, but the current setup does not point to early exercise as the key issue.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-10-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$24.5000` (->1000%)
* **Model ΔP**: `-$24.5000`
* **Primary drivers**: **Theta decay** (59%) and **Delta PnL** (28%) and **Vega PnL** (7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best explained by time decay in the model: the option lost value even though spot edged higher and implied volatility also firmed slightly. The remaining gap is consistent with higher-order truncation noise and path effects around a short-dated American contract, but there is no separate news catalyst in the digest to assign as the cause. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The factor decomposition points cleanly to theta as the dominant modeled driver, and the market-move bands are small. Confidence is capped by the medium residual share, observation not being reliable, and the absence of retrieved headlines, so the run should be read as a model revaluation rather than a catalyst-led move.

---

## 2. Observation Lock

* **As-of**: `2026-10-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 13.8%)
* **IV move**: +0.13 vol pts vs noise band ±0.67 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$24.5000`
* **Model ΔP (engine)**: `-$24.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$19.6573`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$4.8427` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (19.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$23.8751` | -97.4% | Stock moved from $332.99 to $334.30 (+1.3100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.2959` | -5.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$5.7842` | -23.6% | IV moved +0.34 vol pts (27.94% → 28.08%) |
| **Theta decay (Δt · Theta)** | `-$50.6125` | +206.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$4.8427` | +19.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$24.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$4.8427` (19.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0040`
* Combined: `+$0.0040` | Residual after: `-$0.2490`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.5058`
* **spot**: `+$0.2109`
* **vol**: `+$0.0498`
* **rate**: `-$0.0001`
* Step sum: `-$0.2452` | Model ΔP: `-$0.2450` | Audit residual: `+$0.0002`

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
* Watch whether the full reprice remains close to the Taylor view as expiry approaches, since short-dated options can be distorted by truncation and boundary effects.
* No headline-based mechanism was available in the digest, so there is nothing to validate for borrow, squeeze, or IV-crush behavior.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-10-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$192.5000` (->1000%)
* **Model ΔP**: `-$192.5000`
* **Primary drivers**: **Delta PnL** (52%) and **Vega PnL** (24%) and **Theta decay** (19%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best explained by the put’s negative delta against the higher underlying, with smaller contributions from theta decay and a modest vol reprice. The residual is low, so the Taylor view is broadly consistent with the model revaluation and there is no separate catalyst story to layer in from the tape. Because observation quality is flagged as weak and Vega narrative is suppressed, the vol line should be treated as a modeling component rather than a headline-driven explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is coherent and the residual is small, but the feed is marked unreliable and there were no headlines to confirm a separate event-driven mechanism. The American premium is present but small, so early exercise is not the main explanation.

---

## 2. Observation Lock

* **As-of**: `2026-10-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 15.0%)
* **IV move**: -1.73 vol pts vs noise band ±10.63 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$192.5000`
* **Model ΔP (engine)**: `-$192.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$199.5436`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$7.0436` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.7%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$109.3906` | +56.8% | Stock moved from $332.99 to $334.30 (+1.3100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.3253` | -0.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$51.1700` | +26.6% | IV moved -3.18 vol pts (31.73% → 29.99%) |
| **Theta decay (Δt · Theta)** | `-$40.3083` | +20.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$7.0436` | -3.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$192.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$7.0436` (3.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0105`
* Combined: `-$0.0105` | Residual after: `-$1.9145`

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
* Check whether the spot move or a full-surface reprice explains any remaining gap in the model decomposition, especially given the weak observation flag.
* Monitor the implied volatility input and the quoted surface for consistency, but do not infer a separate catalyst from the available tape.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$10.5000` (+481.7%)
* **Model ΔP**: `+$10.5000`
* **Primary drivers**: **Theta decay** (59%) and **Vega PnL** (30%) and **Delta PnL** (9%).
* **Verdict**: The modeled one-day move was dominated by time decay, with delta and vega acting as secondary offsets rather than the main explanation. The residual is modest enough to leave the theta-led attribution intact, and the spot and implied-vol moves were both small, so there is no separate catalyst story to layer on top of the blotter.
* **Confidence**: **Medium** — The attribution is internally consistent and observation quality is reliable, but the residual is not negligible and the market feed is limited to the contract-level marks with no relevant headlines. That keeps the diagnosis at medium confidence rather than high, and there is no Layer B mechanism to validate or reject.

---

## 2. Observation Lock

* **As-of**: `2026-10-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.5%)
* **IV move**: +0.36 vol pts vs noise band ±0.01 pts (exceeds noise band)
* **Prior observation**: `2026-10-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$10.5000`
* **Model ΔP (engine)**: `+$10.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$9.3811`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.1189` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (10.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$4.1420` | -39.4% | Stock moved from $778.57 to $778.10 (-0.4700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.0339` | -0.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$14.4768` | -137.9% | IV moved +0.34 vol pts (19.24% → 19.59%) |
| **Theta decay (Δt · Theta)** | `+$28.0338` | +267.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.1189` | +10.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$10.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.1189` (10.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0039`
* Combined: `+$0.0039` | Residual after: `-$0.1089`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2783`
* **spot**: `+$0.0385`
* **vol**: `+$0.1349`
* **rate**: `+$0.0005`
* Step sum: `-$0.1045` | Model ΔP: `-$0.1050` | Audit residual: `-$0.0005`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Theta decay**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* Check whether Taylor truncation or full-surface repricing would meaningfully alter the residual before treating the theta bucket as fully explanatory.
* Monitor the time-value-versus-dividend balance around American exercise, since the early-exercise premium is present but small and the dividend does not dominate remaining time value.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$64.0000` (-923.5%)
* **Model ΔP**: `-$64.0000`
* **Primary drivers**: **Theta decay** (74%) and **Delta PnL** (25%).
* **Verdict**: The position’s one-day change is dominated by time decay, with spot and implied volatility both essentially flat and the Taylor residual staying small. The move is therefore best read as a carry-driven revaluation of the option rather than a catalyst-led repricing. The American-versus-European check shows no material early-exercise effect, so the dividend/exercise boundary is not part of the explanation.
* **Confidence**: **Medium** — The attribution is supported by high coverage, a low residual band, and reliable observations. Confidence is tempered only by the lack of news catalysts and the fact that the run is a model revaluation rather than a tradeable mark-to-market explanation.

---

## 2. Observation Lock

* **As-of**: `2026-10-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.3%)
* **IV move**: -0.07 vol pts vs noise band ±0.01 pts (exceeds noise band)
* **Prior observation**: `2026-10-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$64.0000`
* **Model ΔP (engine)**: `-$64.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$64.1182`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.1182` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$15.9778` | +25.0% | Stock moved from $778.57 to $778.10 (-0.4700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1292` | -0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.7461` | +1.2% | IV moved -0.01 vol pts (12.79% → 12.72%) |
| **Theta decay (Δt · Theta)** | `-$47.5235` | +74.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.1182` | -0.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$64.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.1182` (0.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0000`
* Combined: `+$0.0000` | Residual after: `-$0.6400`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Theta decay**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* Watch whether the next revaluation remains dominated by decay or whether a larger spot move causes higher-order truncation to matter.
* Verify that the absence of material early-exercise premium persists; there is no meaningful dividend or exercise boundary distortion in the current marks.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$13.5000` (+>1000%)
* **Model ΔP**: `+$13.5000`
* **Primary drivers**: **Delta PnL** (55%) and **Vega PnL** (22%) and **Gamma PnL** (10%).
* **Verdict**: The position’s move was dominated by a favorable spot rally that lifted call value, with gamma adding some convexity support while theta and lower implied volatility worked against the move. The remaining gap is consistent with higher-order model effects and revaluation noise rather than a separate catalyst, and the run does not support a distinct news-based explanation because no relevant headlines were retrieved.
* **Confidence**: **Medium** — The driver call is well supported by the blotter and the attribution coverage is high, but the residual is still meaningful enough to leave some method-level noise and higher-order effects in play. Confidence is held at medium because there are no relevant headlines to cross-check a catalyst and the market feed notes a calibrated mark with local volatility deferred.

---

## 2. Observation Lock

* **As-of**: `2026-10-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 14.9%)
* **IV move**: -1.81 vol pts vs noise band ±1.05 pts (exceeds noise band)
* **Prior observation**: `2026-10-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$13.5000`
* **Model ΔP (engine)**: `+$13.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$15.6028`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$2.1028` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (15.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$25.8451` | +191.4% | Stock moved from $41.65 to $42.78 (+1.1300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$4.5702` | +33.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$10.4495` | -77.4% | IV moved -2.45 vol pts (29.59% → 27.78%) |
| **Theta decay (Δt · Theta)** | `-$4.3631` | -32.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$2.1028` | -15.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$13.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$2.1028` (15.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0200`
* Combined: `-$0.0200` | Residual after: `+$0.1550`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0439`
* **spot**: `+$0.2977`
* **vol**: `-$0.1187`
* **rate**: `-$0.0001`
* Step sum: `+$0.1349` | Model ΔP: `+$0.1350` | Audit residual: `+$0.0001`

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

* Monitor whether a fuller reprice or higher-order convexity effects would materially change the modeled split between spot and residual.
* No catalyst layer was provided here, so there is no borrow, squeeze, or IV-crush signal to verify from headlines.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$1.0000` (->1000%)
* **Model ΔP**: `-$1.0000`
* **Primary drivers**: **Delta PnL** (34%) and **Vega PnL** (33%) and **Theta decay** (20%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is primarily explained by the lower spot price moving the call further out of the money, with gamma partly offsetting and theta adding additional decay. Vega also declines with the implied-vol move, but that narrative is de-emphasized because the observation is unreliable and the desk explicitly suppresses a Vega story here; the remaining gap is consistent with higher-order truncation and path effects in the model reprice. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The factor split is clear and the dominant modeled driver is stable, but observation reliability is flagged false and the residual remains material enough to warrant caution. There are no headlines to anchor an external catalyst, so Layer B stays empty and the explanation should stay at the model-reprice level.

---

## 2. Observation Lock

* **As-of**: `2026-10-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 66.7%)
* **IV move**: -6.25 vol pts vs noise band ±6.60 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$1.0000`
* **Model ΔP (engine)**: `-$1.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$1.1485`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.1485` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (14.8%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.4665` | +34.4% | Stock moved from $1.68 to $1.62 (-0.0600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0304` | +2.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.4421` | +32.6% | IV moved -4.13 vol pts (118.75% → 112.50%) |
| **Theta decay (Δt · Theta)** | `-$0.2703` | +19.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.1485` | +10.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$1.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.1485` (14.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0008`
* Combined: `+$0.0008` | Residual after: `-$0.0108`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0027`
* **spot**: `-$0.0040`
* **vol**: `-$0.0033`
* **rate**: `-$0.0000`
* Step sum: `-$0.0100` | Model ΔP: `-$0.0100` | Audit residual: `+$0.0000`

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
* Watch whether the spot move keeps dominating the model reprice, since truncation and other higher-order effects can still distort a first-pass Taylor view.
* Verify quote quality and the surface fit before leaning on the volatility line, because the feed is incomplete and the Vega narrative is suppressed.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0688 | level_proxy(t) = 0.1616
* Δskew = +0.0043 | Δlevel = +0.0014
* Put 715 delta=-0.0860 | Call 795 delta=0.3256
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
