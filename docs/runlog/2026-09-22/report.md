# Live book run — 2026-09-22

Run `2026-09-22-1790126106`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=11`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-09-22` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$67.0000`
* **Total Model PnL**: `+$153.4555`
* **Aggregate model vs mark gap**: `+$86.4555`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `JPM 350P 2026-10-23` | `+$702.5000` |
| 2 | `JPM 350C 2026-10-23` | `-$545.0000` |
| 3 | `SPY 795C 2026-11-20` | `-$39.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$563.4118` |
| Gamma | `+$24.8742` |
| Vega | `-$392.8032` |
| Theta | `-$44.4006` |
| Residual | `+$2.3733` |

### Notable underlyings

* **JPM**: `+$157.5000` aggregate option PnL
* **VZ**: `-$15.0445` aggregate option PnL
* **AAPL**: `+$10.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-09-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$15.0000` (+62.6%)
* **Model ΔP**: `+$15.0000`
* **Primary drivers**: **Delta PnL** (49%) and **Vega PnL** (44%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move was led by the stock’s upward spot shift, with gamma adding a smaller convexity tail. Vega and theta worked against the position, but the run is a model revaluation rather than a clean market-mark story, so the residual is best treated as truncation and quote noise around the full repricing. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The dominant factor is clear from the blotter, but observation reliability is weak and the attribution coverage is low. Vega narrative is suppressed, there are no retrieved headlines, and the residual is high enough that the Taylor view should be treated as reference-level rather than fully explanatory.

---

## 2. Observation Lock

* **As-of**: `2026-09-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.3%)
* **IV move**: -0.26 vol pts vs noise band ±0.83 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$15.0000`
* **Model ΔP (engine)**: `+$15.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$9.1160`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$5.8840` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (39.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$184.1100` | +1227.4% | Stock moved from $336.13 to $338.98 (+2.8500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$3.5462` | +23.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$163.1602` | -1087.7% | IV moved -3.22 vol pts (30.40% → 30.14%) |
| **Theta decay (Δt · Theta)** | `-$15.3800` | -102.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$5.8840` | +39.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$15.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$5.8840` (39.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0402`
* Combined: `+$0.0402` | Residual after: `+$0.1098`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1537`
* **spot**: `+$1.8774`
* **vol**: `-$1.5741`
* **rate**: `+$0.0077`
* Step sum: `+$0.1573` | Model ΔP: `+$0.1500` | Audit residual: `-$0.0073`

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
* Reconcile the move with a full-surface reprice and delta-aware hedging rather than relying on the linear bucket alone, since higher-order effects are material.
* No catalyst layer is available from the digest, so keep the focus on the modeled spot move and quote quality rather than adding an IV or microstructure story.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-09-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$5.0000` (-49.0%)
* **Model ΔP**: `-$5.0000`
* **Primary drivers**: **Delta PnL** (49%) and **Vega PnL** (42%) and **Theta decay** (6%).
* **Verdict**: The run is dominated by the modeled delta response to a modest rise in the underlying, with gamma a smaller second-order drag and theta partially offsetting the move. Vega helped cushion the option because implied volatility slipped, but the headline story remains the spot-driven revaluation in the flat FDM engine. The residual is small relative to the move and is consistent with normal truncation noise rather than a separate catalyst.
* **Confidence**: **Medium** — Confidence is medium because the attribution is internally coherent and observation quality is reliable, but the residual share is elevated and the spot and vol moves are both modest. There are no relevant headlines, no Layer B mechanism to anchor a catalyst story, and the American early-exercise premium is negligible, so the diagnosis should stay close to the blotter.

---

## 2. Observation Lock

* **As-of**: `2026-09-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.0%)
* **IV move**: -0.37 vol pts vs noise band ±0.19 pts (exceeds noise band)
* **Prior observation**: `2026-09-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$5.0000`
* **Model ΔP (engine)**: `-$5.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$6.7328`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.7328` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (34.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$114.3622` | +49.3% | Stock moved from $336.13 to $338.98 (+2.8500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$4.1367` | +1.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$98.1199` | +42.3% | IV moved -1.86 vol pts (27.34% → 26.98%) |
| **Theta decay (Δt · Theta)** | `+$13.6462` | +5.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.7328` | +0.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$5.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.7328` (34.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0206`
* Combined: `-$0.0206` | Residual after: `+$0.0706`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1364`
* **spot**: `+$1.1806`
* **vol**: `-$0.9944`
* **rate**: `+$0.0049`
* Step sum: `+$0.0547` | Model ΔP: `+$0.0500` | Audit residual: `-$0.0047`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Reconcile the position with the full model reprice rather than a single Greek slice, since second-order terms and theta are contributing around the main delta move.
* No catalyst overlay is supported by the digest, so avoid adding an IV-crush, borrow, squeeze, or early-exercise narrative not present in the blotter.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-09-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$545.0000` (-4791.2%)
* **Model ΔP**: `-$545.0000`
* **Primary drivers**: **Vega PnL** (81%) and **Delta PnL** (15%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move was dominated by a volatility revaluation: the option was marked lower as implied volatility fell, while the favorable spot uptick only partially offset that drag. With the observation flagged as unreliable and Vega narrative suppression in force, the cleanest reading is that the full revaluation was driven primarily by the vol move rather than by spot or carry. The residual is small relative to the model move, so higher-order truncation is not the main story here. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is medium because the quant engine clearly identifies Vega as the dominant modeled factor, but the observation is marked unreliable and the Vega narrative is suppressed due to data-quality constraints. There are no retrieved headlines to add a catalyst layer, and the available residual is low, so the diagnosis stays at the revaluation level rather than a more specific event claim.

---

## 2. Observation Lock

* **As-of**: `2026-09-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 11.0%)
* **IV move**: +0.38 vol pts vs noise band ±0.82 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$545.0000`
* **Model ΔP (engine)**: `-$545.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$559.7678`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$14.7678` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$121.2013` | -22.2% | Stock moved from $349.67 to $352.04 (+2.3700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$3.9101` | -0.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$664.3007` | +121.9% | IV moved -16.16 vol pts (25.81% → 26.18%) |
| **Theta decay (Δt · Theta)** | `-$20.5786` | +3.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$14.7678` | -2.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$545.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$14.7678` (2.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0204`
* Combined: `+$0.0204` | Residual after: `-$5.4704`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$2.3700` vs next cash dividend `+$1.5000` (gap `+$3.8700`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$5.9250` vs `+$6.3678` (gap `-$0.4428`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0901` — material
* **Dividend PV effect** (European, same divs − no divs): `-$0.5331`
* **Dividend coverage** (dividend / time value): `0.39` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$6.6430`
* **Residual (Taylor ε)**: `+$0.1477`
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

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Reprice the full surface and verify the vol mark path before leaning on delta-based intuition; the move is primarily a vol revaluation, not a spot-led shift.
* No named catalyst is available from the digest, so avoid adding a borrow, squeeze, or IV-crush explanation that is not supported by the blotter.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.39 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-09-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$702.5000` (+7513.4%)
* **Model ΔP**: `+$702.5000`
* **Primary drivers**: **Vega PnL** (85%) and **Delta PnL** (12%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The option’s move was dominated by the modeled volatility revaluation: the spot change was modest while the implied-vol shift was the clear driver in the Taylor view. Delta and theta were secondary drags, and the small residual is consistent with a clean fit rather than a missed event. With no retrieved headlines and observation reliability flagged low, there is no supported catalyst layer to add beyond the vol-driven repricing. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The driver is clear from the blotter, but observation reliability is not strong and there are no headlines to corroborate an external catalyst. The residual is small and the attribution coverage is high, which supports the modeled story, though the surface diagnostics note limitations.

---

## 2. Observation Lock

* **As-of**: `2026-09-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 8.2%)
* **IV move**: +2.54 vol pts vs noise band ±1.66 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$702.5000`
* **Model ΔP (engine)**: `+$702.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$712.5542`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$10.0542` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.4%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$119.5962` | -17.0% | Stock moved from $349.67 to $352.04 (+2.3700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$5.1015` | +0.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$839.4587` | +119.5% | IV moved +20.43 vol pts (25.79% → 28.33%) |
| **Theta decay (Δt · Theta)** | `-$12.4097` | -1.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$10.0542` | -1.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$702.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$10.0542` (1.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0179`
* Combined: `+$0.0179` | Residual after: `+$7.0071`

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
* Reconcile the move as a vol-led full-surface repricing rather than a spot-led move; keep the Taylor decomposition as a reference view only if you are validating the model path.
* No supported headline catalyst was retrieved, so avoid adding a borrow, squeeze, or earnings-style explanation without fresh tape evidence.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.09 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-09-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$38.0000` (+951.2%)
* **Model ΔP**: `+$38.0000`
* **Primary drivers**: **Delta PnL** (46%) and **Vega PnL** (37%) and **Gamma PnL** (8%).
* **Verdict**: The position’s one-day move is dominated by spot rising while the put’s negative delta worked in the short-book’s favor. Gamma and Vega ran against that move, and the remaining gap is consistent with higher-order truncation and path effects in the full revaluation. The only SPY-specific headline is a gamma and dealer-positioning note, which fits the tape as context but does not replace the modeled spot-driven explanation.
* **Confidence**: **Medium** — Confidence is moderate because the blotter’s attribution coverage is limited and the unexplained share is elevated, so the Taylor view is only a reference and higher-order effects likely matter. The feed is otherwise reliable, the dominant driver is explicit in the code, and the relevant headline supports a market-structure backdrop rather than a separate catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-09-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.8%)
* **IV move**: -0.45 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-09-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$38.0000`
* **Model ΔP (engine)**: `+$38.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$13.3891`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$24.6109` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (64.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$174.7020` | +459.7% | Stock moved from $761.69 to $773.50 (+11.8100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$31.8249` | -83.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$138.4146` | -364.2% | IV moved +1.94 vol pts (18.18% → 17.73%) |
| **Theta decay (Δt · Theta)** | `+$8.9266` | +23.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$24.6109` | +64.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$38.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$24.6109` (64.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.2068`
* Combined: `-$0.2068` | Residual after: `-$0.1732`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0894`
* **spot**: `-$1.4377`
* **vol**: `+$1.1464`
* **rate**: `-$0.0034`
* Step sum: `-$0.3840` | Model ΔP: `-$0.3800` | Audit residual: `+$0.0040`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Intel note: One headline directly references SPY and describes SPY-related gamma/dealer positioning. The remaining items are broad market or educational pieces that may provide context but do not specifically indicate a SPY event._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Today's SPY, QQQ & VIX Gamma, Dealer Positioning & Regime | FlashAlpha** _(Source: FlashAlpha)_
   This headline is directly about SPY and frames the market through SPY-related positioning and gamma context.

_Peer / sector background (indirect context, not a required catalyst):_

2. **The Market Is Near Another All-Time High and You’re 66 With Cash to Invest. Buying Now Feels Like the Top. These 3 ETFs Are How You Get In Anyway** _(Source: 24/7 Wall St.)_
   ETF market commentary that may provide broad context for SPY as a market proxy, but it does not specifically discuss SPY itself.
3. **Invest Like Buffett: Lessons From the Oracle of Omaha** _(Source: Zacks)_
   General investing commentary with no direct SPY-specific issuer or control-structure link.
4. **VGT Holders Bought ‘Tech’ and Own No Google, Meta, or Amazon: The Sector Rule That Decides What’s Inside** _(Source: 24/7 Wall St.)_
   Peer ETF/sector-structure discussion that could be tangentially relevant to broad market ETF flows, but it is not about SPY.
5. **Delta-Neutral Options Strategies for Earnings - SteadyOptions Trading Blog - SteadyOptions** _(Source: SteadyOptions)_
   General options education content that may be background for an options PnL story, but it is not SPY-specific.
6. **Learn Options Trading: A Path Built on Real Earnings Weeks** _(Source: Earnings-Watcher)_
   Broad options-learning content with no direct link to SPY.

---

## 7. Risk Watchlist

* Reconcile the position with a full-surface reprice and residual review, since the Taylor decomposition leaves a meaningful gap and the move is not well captured by first-order Greeks alone.
* Use the SPY gamma and dealer-positioning context as backdrop only; no separate squeeze, borrow, or IV-crush mechanism is supported by the relevant headline set.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-09-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$39.0000` (-431.4%)
* **Model ΔP**: `-$39.0000`
* **Primary drivers**: **Vega PnL** (46%) and **Delta PnL** (42%) and **Gamma PnL** (6%).
* **Verifier**: FAIL — hard policy violation; escalate before trading on story.
* **Verdict**: Verifier FAIL — terminal break escalation. The candidate attributes the large method residual to truncation and path effects and explicitly frames the move as a full-model reprice with no separate tape story
* **Confidence**: **Medium** — The engine flags the dominant modeled driver and the observation quality is reliable, but attribution coverage is low and the residual is large, so the Greek split is only a coarse explanation. With no retrieved headlines and no named microstructure mechanisms, there is no supported Layer B catalyst to add.

---

## 2. Observation Lock

* **As-of**: `2026-09-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.2%)
* **IV move**: -0.21 vol pts vs noise band ±0.01 pts (exceeds noise band)
* **Prior observation**: `2026-09-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$39.0000`
* **Model ΔP (engine)**: `-$39.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$3.3089`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$35.6911` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (91.5%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$347.7614` | -891.7% | Stock moved from $761.69 to $773.50 (+11.8100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$47.6941` | -122.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$382.5180` | +980.8% | IV moved -3.60 vol pts (14.02% → 13.81%) |
| **Theta decay (Δt · Theta)** | `-$16.2465` | +41.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$35.6911` | +91.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$39.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$35.6911` (91.5% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* Vanna PnL: `-$0.5940` | other second-order: `+$0.2056`
* Combined: `-$0.3884` | Residual after: `-$0.0016`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1623`
* **spot**: `+$3.9450`
* **vol**: `-$4.1740`
* **rate**: `+$0.0094`
* Step sum: `-$0.3819` | Model ΔP: `-$0.3900` | Audit residual: `-$0.0081`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* Verifier missing evidence: policy
* Use the full-surface reprice and second-order audit as the reference, since the residual is large and a first-order Greek read is incomplete.
* No separate catalyst mechanism is supported by the blotter, so keep the narrative at the model-revaluation level rather than forcing an event explanation.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-09-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$101.5000` (-388.4%)
* **Model ΔP**: `-$15.0445`
* **Primary drivers**: **Delta PnL** (60%) and **Vega PnL** (32%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by the option’s positive delta against the lower underlying price, with gamma only partially offsetting and theta adding a smaller drag. The model revaluation is therefore a spot-led move, while the remaining gap is consistent with higher-order truncation and mark noise rather than a separate news catalyst. Given the observation lock and absent headlines, there is no supported Layer B mechanism to add beyond the model story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is strong but the observation reliability is weak and the surface diagnostics show calibration limitations. The residual is not large enough to overturn the delta-led explanation, but the terminal unexplained break means the run should be treated as a model revaluation with some caution. No relevant headlines were retrieved, so there is no catalyst evidence to strengthen or challenge the blotter story.

---

## 2. Observation Lock

* **As-of**: `2026-09-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 58.7%)
* **IV move**: +2.69 vol pts vs noise band ±11.06 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$101.5000`
* **Model ΔP (engine)**: `-$15.0445`
* **Model vs Mark gap**: `+$86.4555` (-574.7% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$15.9596`

* **Method residual (ε_method)**: `+$0.9151` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$86.4555` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (6.1%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$30.4045` | +202.1% | Stock moved from $48.09 to $47.68 (-0.4100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.5839` | -3.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$16.1307` | -107.2% | IV moved +2.69 vol pts (29.44% → 32.13%) |
| **Theta decay (Δt · Theta)** | `-$2.2696` | +15.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.9151` | -6.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$15.0445** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.9151` (6.1% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0132`
* Combined: `+$0.0132` | Residual after: `-$0.1636`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0227`
* **spot**: `-$0.2985`
* **vol**: `+$0.1707`
* **rate**: `+$0.0008`
* Step sum: `-$0.1496` | Model ΔP: `-$0.1504` | Audit residual: `-$0.0008`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$0.4100` vs next cash dividend `+$0.7080` (gap `+$0.2980`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$3.7226` vs `+$3.8335` (gap `-$0.1110`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0500` — material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1611`
* **Dividend coverage** (dividend / time value): `0.68` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.1613`
* **Residual (Taylor ε)**: `+$0.0092`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%
  * `american_dividend_exercise_check` — path_reprice outranks ex-div window
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Treat the move as a spot-led revaluation and verify the hedge response against the delta exposure; the Taylor decomposition is still the right first lens despite the truncation residue.
* Because there is no validated catalyst tape, avoid forcing a vol or event narrative; keep focus on the model move and the noted surface limitations.
* **Assignment watch**: ex-div `2026-10-09` — Dividend coverage 0.68 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-09-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$2.0000` (+5714.3%)
* **Model ΔP**: `+$2.0000`
* **Primary drivers**: **Vega PnL** (86%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The option’s revaluation was driven primarily by the jump in implied volatility while spot was unchanged, so the move is best read as a volatility re-mark rather than a directional equity move. The remaining gap is consistent with higher-order convexity and Taylor truncation around the reprice, with no separate news catalyst available in the blotter. The American early-exercise layer is not a factor here because the dividend does not justify immediate exercise at current marks. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Low** — Confidence is limited because observation reliability is off, the Vega narrative is suppressed by the code, and there are no retrieved headlines to validate a catalyst layer. The residual is medium relative to the model move, but the input set does not support a more granular explanation than a volatility-led revaluation with truncation noise.

---

## 2. Observation Lock

* **As-of**: `2026-09-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 90.9%)
* **IV move**: +9.37 vol pts vs noise band ±11.38 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$2.0000`
* **Model ΔP (engine)**: `+$2.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$1.7919`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.2081` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (10.4%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.0000` | +0.0% | Stock moved from $2.09 to $2.09 (+0.0000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0000` | +0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$1.8810` | +86.4% | IV moved +10.57 vol pts (87.50% → 96.88%) |
| **Theta decay (Δt · Theta)** | `-$0.0891` | +4.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.2081` | +9.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$2.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.2081` (10.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0025`
* Combined: `+$0.0025` | Residual after: `+$0.0175`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0009`
* **spot**: `+$0.0000`
* **vol**: `+$0.0209`
* **rate**: `+$0.0000`
* Step sum: `+$0.0200` | Model ΔP: `+$0.0200` | Audit residual: `-$0.0000`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Use the full-surface model reprice as the reference for the volatility jump, since the Taylor decomposition leaves a meaningful residual.
* No Layer B catalyst is available from the digest, so do not infer borrow, squeeze, or IV-crush mechanics from background tape.

---


## Skew proxy (Task C3.3, SPY risk reversal)

* skew_proxy(t) = +0.0392 | level_proxy(t) = 0.1577
* Δskew = -0.0024 | Δlevel = -0.0033
* Put 715 delta=-0.1236 | Call 795 delta=0.3385
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
