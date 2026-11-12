# Live book run — 2026-11-11

Run `2026-11-11-1794450387`. 8/8 legs diagnosed, 0 settled at expiry, 0 failed. `legs_narrated=7` `legs_silent=1` `llm_calls=7`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-11` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$173.0000`
* **Total Model PnL**: `+$173.0000`
* **Aggregate model vs mark gap**: `-$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `+$630.0000` |
| 2 | `AAPL 350C 2026-11-20` | `-$367.5000` |
| 3 | `JPM 340P 2026-12-18` | `-$145.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$435.1992` |
| Gamma | `-$68.1006` |
| Vega | `-$203.5593` |
| Theta | `-$3.6118` |
| Residual | `+$13.0726` |

### Notable underlyings

* **AAPL**: `+$262.5000` aggregate option PnL
* **JPM**: `-$170.0000` aggregate option PnL
* **SPY**: `+$72.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-11` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$630.0000` (+25.5%)
* **Model ΔP**: `+$630.0000`
* **Primary drivers**: **Delta PnL** (+100.6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is dominated by the call’s strong directional exposure to the underlying rally, with smaller contributions from convexity, time decay, and the softening in implied volatility. The residual is modest and fits normal higher-order and marking noise in a one-day revaluation; there is no headline catalyst to add, and the observation lock means the tape should be treated as a model-driven repricing rather than a news-led gap. American early exercise is not the story here because the dividend does not clear the remaining time value. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the attribution is internally consistent and coverage is strong, but observation is flagged unreliable and there are no retrieved headlines to corroborate a separate catalyst. The residual is low, and the ex-div setting does not support a material early-exercise interpretation.

---

## 2. Observation Lock

* **As-of**: `2026-11-11` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.7%)
* **IV move**: -0.12 vol pts vs noise band ±8.41 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-10`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$630.0000`
* **Model ΔP (engine)**: `+$630.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$617.6312`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$12.3688` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$633.4695` | +100.6% | Stock moved from $348.51 to $355.63 (+7.1200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$23.3589` | +3.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$16.8793` | -2.7% | IV moved -1.55 vol pts (35.47% → 33.92%) |
| **Theta decay (Δt · Theta)** | `-$22.3179` | -3.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$12.3688` | +2.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$630.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$12.3688` (2.0% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$6.3164`
* Combined: `+$6.3164` | Residual after: `+$6.0524`

### Ex-div attribution overlay (official PnL stays the American FDM Taylor blotter)
* **Spot drop vs dividend** (per share): spot `+$7.1200` vs next cash dividend `+$0.2700` (gap `+$7.3900`)
* **American FDM vs European analytic (no cash div, cross-check, per option)**: `+$31.0250` vs `+$31.2563` (gap `-$0.2313`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored, per option): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs, per option): `-$0.2324`
* **Dividend coverage** (dividend / time value): `0.68` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$16.8793`
* **Residual (Taylor ε)**: `+$12.3688`
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
* Watch whether the full revaluation remains well explained by the spot move if the next mark quality changes, since truncation and quote noise can widen the residual.
* Keep monitoring ex-div and early-exercise conditions, but this run does not show a material American premium or a separate catalyst channel.
* **Assignment watch**: ex-div `2026-11-12` — Dividend coverage 0.68 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-11` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$367.5000` (+74.6%)
* **Model ΔP**: `-$367.5000`
* **Primary drivers**: **Delta PnL** (-90.9%) and **Gamma PnL** (-19.6%) and **Theta decay** (+8.2%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained mainly by the option’s directional exposure to the underlying rising above the prior close, with gamma amplifying the mark as the stock moved through the strike area. Vega and theta were secondary offsets in the model, and the remaining gap is small enough to sit within normal truncation noise for this run. There are no retrieved headlines or named microstructure tokens, so there is no supported Layer B catalyst to add beyond the modeled price move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is only medium because observation is unreliable and the surface diagnostics note a local-vol calibration limitation, so the run should be read as a model revaluation rather than a clean mark-to-market story. The residual is low, the driver is clear, and there is no headline evidence to support an auxiliary catalyst narrative.

---

## 2. Observation Lock

* **As-of**: `2026-11-11` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.7%)
* **IV move**: +0.27 vol pts vs noise band ±1.00 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-10`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$367.5000`
* **Model ΔP (engine)**: `-$367.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$366.2210`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.2790` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.3%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$334.0016` | -90.9% | Stock moved from $348.51 to $355.63 (+7.1200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$72.2045` | -19.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$9.6850` | +2.6% | IV moved -0.42 vol pts (24.22% → 23.80%) |
| **Theta decay (Δt · Theta)** | `+$30.3002` | +8.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.2790` | -0.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$367.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.2790` (0.3% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.0221`
* Combined: `-$0.0221` | Residual after: `-$1.2569`

### Ex-div attribution overlay (official PnL stays the American FDM Taylor blotter)
* **Spot drop vs dividend** (per share): spot `+$7.1200` vs next cash dividend `+$0.2700` (gap `+$7.3900`)
* **American FDM vs European analytic (no cash div, cross-check, per option)**: `+$8.6000` vs `+$8.7638` (gap `-$0.1638`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored, per option): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs, per option): `-$0.1641`
* **Dividend coverage** (dividend / time value): `0.09` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$9.6850`
* **Residual (Taylor ε)**: `-$1.2790`
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
* Second-order convexity can still matter if spot keeps moving through the strike, so verify whether the full revaluation remains consistent with the Taylor view.
* With no relevant headlines or microstructure tags, do not infer a borrow, squeeze, or IV-crush explanation from this tape.
* **Assignment watch**: ex-div `2026-11-12` — Dividend coverage 0.09 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-11` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$25.0000` (-2.0%)
* **Model ΔP**: `-$25.0000`
* **Primary drivers**: **Vega PnL** (-48.3%) and **Delta PnL** (+41.4%) and **Theta decay** (-8.7%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-11-11` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.3%)
* **IV move**: -2.38 vol pts vs noise band ±0.76 pts (exceeds noise band)
* **Prior observation**: `2026-11-10`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$25.0000`
* **Model ΔP (engine)**: `-$25.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$26.5846`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.5846` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (6.3%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$73.3830` | +41.4% | Stock moved from $342.07 to $343.39 (+1.3200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.2374` | +0.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$85.7239` | -48.3% | IV moved -1.97 vol pts (25.14% → 23.17%) |
| **Theta decay (Δt · Theta)** | `-$15.4811` | -8.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.5846` | +0.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$25.0000** | **-14.1%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.5846` (6.3% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.3827` | other second-order: `+$0.0222`
* Combined: `+$0.4049` | Residual after: `+$1.1797`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Theta / carry**._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* No action needed; move is within theta/carry tolerance.

---

### Position 4 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-11` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$145.0000` (-17.2%)
* **Model ΔP**: `-$145.0000`
* **Primary drivers**: **Vega PnL** (-53.6%) and **Delta PnL** (-40.2%) and **Theta decay** (-8.3%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The option’s move was driven first by the drop in implied volatility, with spot also drifting higher enough to add a smaller bearish contribution for the put. Theta was a secondary drag, while the residual is small enough to read as ordinary truncation and quote noise rather than a separate story. There are no relevant headlines in the digest, so Layer B is limited to the observed surface move and not a news catalyst. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is supported by the engine and the Taylor decomposition, but observation reliability is flagged low and the feed has no retrieved headlines. The residual is low, which helps, yet the lack of catalyst evidence means the explanation should stay at the factor level rather than a fuller event-based story.

---

## 2. Observation Lock

* **As-of**: `2026-11-11` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 15.7%)
* **IV move**: -1.48 vol pts vs noise band ±1.29 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-10`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$145.0000`
* **Model ΔP (engine)**: `-$145.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$146.5663`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.5663` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.1%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$58.3333` | -40.2% | Stock moved from $342.07 to $343.39 (+1.3200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.4098` | +1.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$77.6549` | -53.6% | IV moved -1.79 vol pts (22.30% → 20.52%) |
| **Theta decay (Δt · Theta)** | `-$11.9879` | -8.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.5663` | +1.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$145.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.5663` (1.1% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.5737`
* Combined: `+$0.5737` | Residual after: `+$0.9925`

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
* Check whether the move remains consistent after a fresh full-surface reprice, since the current decomposition is a reference view and the residual can shift with curvature.
* With no relevant headlines and no named microstructure tokens, avoid layering in a squeeze, borrow, or IV-crush explanation from outside the blotter.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-11` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$71.0000` (-58.9%)
* **Model ΔP**: `+$71.0000`
* **Primary drivers**: **Delta PnL** (+128.1%) and **Gamma PnL** (-41.0%) and **Theta decay** (+30.9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained first by the put’s short delta exposure to the underlying rally, with the second-order curvature and time decay offsetting part of that effect. The residual is small, so the model’s revaluation is largely accounted for without needing a separate tape catalyst. American early exercise is not a material feature here; the dividend does not cover the remaining time value, so exercise is sub-optimal at current marks. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the attribution is well covered by the model and the residual is low, but observation reliability is flagged false and there were no retrieved headlines to independently test the tape. The market move and vol move are both modest, so the diagnosis stays at the factor level supported by the blotter.

---

## 2. Observation Lock

* **As-of**: `2026-11-11` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.0%)
* **IV move**: +0.79 vol pts vs noise band ±0.05 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-10`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$71.0000`
* **Model ΔP (engine)**: `+$71.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$68.1664`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$2.8336` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$90.9191` | +128.1% | Stock moved from $749.92 to $759.81 (+9.8900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$29.1052` | -41.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$15.5777` | -21.9% | IV moved +0.76 vol pts (22.36% → 23.12%) |
| **Theta decay (Δt · Theta)** | `+$21.9301` | +30.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$2.8336` | +4.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$71.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$2.8336` (4.0% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$6.5498` | other second-order: `-$0.4610`
* Combined: `+$6.0888` | Residual after: `-$3.2552`

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
* Higher-order curvature can still distort the Taylor split, but the low residual suggests the close-to-close revaluation is already well captured.
* Keep an eye on any future dividend or exercise-boundary shift; the current American premium is negligible and not a live driver.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-11` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$1.0000` (+18.2%)
* **Model ΔP**: `+$1.0000`
* **Primary drivers**: **Delta PnL** (+29.8%) and **Gamma PnL** (+21.9%) and **Vega PnL** (-20.6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position’s modeled move was led by the spot rally in the underlying, with gamma helping the long call respond positively as the option stayed near the right side of the surface. That said, the full revaluation shows a meaningful gap versus the simple Greek bucket because the move was still small in headline terms but the option is very convex and close to the boundary where truncation and path effects can matter. There were no retrieved headlines or microstructure tags, so there is no supported Layer B catalyst to add beyond the reprice itself. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is strong, but observation is unreliable and the residual is large relative to the model move. The market-feed notes also limit the story to a model revaluation, with no named catalyst evidence to elevate beyond the blotter.

---

## 2. Observation Lock

* **As-of**: `2026-11-11` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 15.4%)
* **IV move**: -2.10 vol pts vs noise band ±0.13 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-10`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$1.0000`
* **Model ΔP (engine)**: `+$1.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$7.3537`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$6.3537` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (635.4%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$8.9881` | +29.8% | Stock moved from $749.92 to $759.81 (+9.8900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$6.5976` | +21.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$6.2185` | -20.6% | IV moved -2.04 vol pts (14.64% → 12.59%) |
| **Theta decay (Δt · Theta)** | `-$2.0135` | -6.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$6.3537` | -21.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$1.0000** | **+3.3%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$6.3537` (635.4% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.73).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (vanna, volga) — reference only, see Regime above
* Vanna PnL: `-$13.5810` | Volga PnL: `+$2.5890`
* Combined: `-$10.9920` | Residual after: `+$4.6383`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$2.0109`
* **spot**: `+$14.4679`
* **vol**: `-$11.4569`
* Step sum: `+$1.0000` | Model ΔP: `+$1.0000` | Audit residual: `+$0.0000`

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
* Watch whether the full revaluation stays sensitive to truncation and path dependence around this strike as spot and time decay evolve.
* With no retrieved headlines or microstructure tags, do not force an IV crush, borrow, or squeeze explanation from background tape.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-11` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$10.0000` (+5.8%)
* **Model ΔP**: `+$10.0000`
* **Primary drivers**: **Delta PnL** (+208.6%) and **Vega PnL** (-95.1%) and **Theta decay** (-38.7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The revaluation is primarily explained by the positive spot move acting through delta, with gamma adding a smaller convexity boost. The vega and theta lines offset part of that gain, while the remaining gap is consistent with higher-order model effects rather than a separate catalyst. There are no retrieved headlines, so the move should be read as a model reprice without a named news driver. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by the observation lock, lack of headlines, and the high residual band. The Taylor view is only a reference here, so the cleanest interpretation is the model’s own revaluation led by delta, with some truncation and path effects left over.

---

## 2. Observation Lock

* **As-of**: `2026-11-11` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 12.2%)
* **IV move**: -1.71 vol pts vs noise band ±5.37 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-10`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$10.0000`
* **Model ΔP (engine)**: `+$10.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$8.0767`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.9233` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (19.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$20.8553` | +208.6% | Stock moved from $46.31 to $46.60 (+0.2900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.6045` | +6.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$9.5088` | -95.1% | IV moved -3.69 vol pts (30.80% → 27.11%) |
| **Theta decay (Δt · Theta)** | `-$3.8744` | -38.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.9233` | +19.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$10.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.9233` (19.2% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.5987` | Volga PnL: `+$0.1461`
* Combined: `+$0.7449` | Residual after: `+$1.1784`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$3.8748`
* **spot**: `+$21.7521`
* **vol**: `-$7.8773`
* Step sum: `+$10.0000` | Model ΔP: `+$10.0000` | Audit residual: `+$0.0000`

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
* Higher-order convexity and Taylor truncation can still distort the reference decomposition when the spot path is choppy.
* With no relevant headlines retrieved, do not infer a borrow, squeeze, or IV-crush narrative from background tape.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-11` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$1.5000` (-60.0%)
* **Model ΔP**: `-$1.5000`
* **Primary drivers**: **Vega PnL** (-112.1%) and **Theta decay** (-11.2%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained first by the modeled volatility reprice: the option fell as implied volatility compressed, with spot only a minor contributor and theta a smaller drag. The remaining gap is consistent with higher-order effects and model truncation rather than a separate catalyst, and there is no headline evidence to add a news-driven layer. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Low** — Confidence is limited because the observation is flagged unreliable, the suppress-vega setting is active, and the residual is meaningful relative to the model move. The market feed also lacks headlines, so there is no independent catalyst confirmation; yesterday's implied volatility was taken from the prior chain mark, not a proxied or copied source.

---

## 2. Observation Lock

* **As-of**: `2026-11-11` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: -12.50 vol pts vs noise band ±39.65 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-10`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$1.5000`
* **Model ΔP (engine)**: `-$1.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$1.9286`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.4286` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (28.6%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.0809` | -5.4% | Stock moved from $1.37 to $1.36 (-0.0100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0009` | +0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$1.6813` | -112.1% | IV moved -25.38 vol pts (193.30% → 167.92%) |
| **Theta decay (Δt · Theta)** | `-$0.1674` | -11.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.4286` | +28.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$1.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.4286` (28.6% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.0403` | Volga PnL: `+$0.3120`
* Combined: `+$0.3524` | Residual after: `+$0.0763`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.1674`
* **spot**: `-$0.0760`
* **vol**: `-$1.2566`
* Step sum: `-$1.5000` | Model ΔP: `-$1.5000` | Audit residual: `+$0.0000`

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
* Watch whether the full revaluation or higher-order curvature continues to explain the residual as spot and volatility reset.
* No headline-based Layer B mechanism is available here; verify the volatility mark quality and quote consistency before leaning on the Vega attribution.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.1005 | level_proxy(t) = 0.1791
* Δskew = +0.0289 | Δlevel = -0.0065
* Put 715 delta=-0.0434 | Call 795 delta=0.0125
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
