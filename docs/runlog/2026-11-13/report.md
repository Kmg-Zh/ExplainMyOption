# Live book run — 2026-11-13

Run `2026-11-13-1794622505`. 7/8 legs diagnosed, 0 settled at expiry, 1 failed. `legs_narrated=7` `legs_silent=0` `llm_calls=8`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-13` | **Positions**: 7 | **Tickers**: AAPL, JPM, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$64.5000`
* **Total Model PnL**: `+$11.4958`
* **Aggregate model vs mark gap**: `-$53.0042`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `JPM 340C 2026-12-18` | `+$147.5000` |
| 2 | `JPM 340P 2026-12-18` | `-$120.0000` |
| 3 | `AAPL 350C 2026-11-20` | `-$62.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$49.7248` |
| Gamma | `+$15.3618` |
| Vega | `+$18.1780` |
| Theta | `-$9.7696` |
| Residual | `-$61.9992` |

### Notable underlyings

* **JPM**: `+$27.5000` aggregate option PnL
* **VZ**: `-$15.5000` aggregate option PnL
* **AAPL**: `-$0.5042` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-13` | **Status**: Verified by QuantLib (fdm_local_vol)

---

## 1. Headline

* **Mark MTM PnL**: `+$115.0000` (+2.0%)
* **Model ΔP**: `+$61.9958`
* **Primary drivers**: **Delta PnL** (+203.9%) and **Theta decay** (-43.6%) and **Vega PnL** (+40.4%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The Taylor view is led by delta, with the spot uptick and positive gamma and vega offsetting theta drag in the modeled move. That said, the attribution does not explain this move: the residual is large, observation quality is weak, and the run needs human review rather than a single-factor story. No named catalyst was retrieved, and there is no supported borrow, squeeze, or IV-crush mechanism to add on top of the blotter. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is limited by the terminal unexplained break, unreliable observation flags, and the high residual relative to the modeled change. The Greek mix identifies the dominant modeled factor, but the gap remains unexplained and the playbook explicitly requires escalation to human review.

---

## 2. Observation Lock

* **As-of**: `2026-11-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.4%)
* **IV move**: +2.93 vol pts vs noise band ±15.85 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$115.0000`
* **Model ΔP (engine)**: `+$61.9958`
* **Model vs Mark gap**: `-$53.0042` (-85.5% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$125.0995`

* **Method residual (ε_method)**: `-$63.1038` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$53.0042` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (101.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$126.4376` | +203.9% | Stock moved from $354.88 to $356.27 (+1.3900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.6513` | +1.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$25.0659` | +40.4% | IV moved +2.93 vol pts (45.97% → 48.90%) |
| **Theta decay (Δt · Theta)** | `-$27.0553` | -43.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$63.1038` | -101.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$61.9958** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$63.1038` (101.8% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$1.7474` | Volga PnL: `+$1.3582`
* Combined: `-$0.3892` | Residual after: `-$62.7146`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$71.1200`
* **spot**: `+$133.1132`
* **vol**: `+$0.0000`
* **rate**: `-$0.0357`
* Step sum: `+$61.9574` | Model ΔP: `+$61.9958` | Audit residual: `+$0.0383`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%
* **Playbook records** (selected by code for the narrator): `terminal-break` (`terminal_unexplained_break`)

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* The modeled result is still sensitive to truncation and path effects around the close-to-close reprice, so the residual should be treated as unresolved rather than absorbed into the Greek mix.
* Watch for any later evidence of quote quality issues or a full-surface reprice that could clarify the unexplained gap; no supported catalyst mechanism was available in the digest.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$62.5000` (+7.9%)
* **Model ΔP**: `-$62.5000`
* **Primary drivers**: **Delta PnL** (-148.8%) and **Theta decay** (+50.1%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained primarily by the contract’s directional exposure to the underlying, with a smaller offset from time decay and only minor higher-order effects around the Taylor fit. The run’s residual is small, so the model revaluation is largely accounted for by the quoted factor decomposition. There is no headline-backed catalyst layer here, and the observation lock means the tape should be treated as a clean factor-driven reprice rather than a news-driven event. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the dominant driver is clear in the blotter, but observation reliability is flagged as false and the market-feed diagnostics note a clean news absence rather than a corroborating catalyst. The residual is small, so truncation is not the main issue, but the lack of relevant headlines limits any Layer B confirmation.

---

## 2. Observation Lock

* **As-of**: `2026-11-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.7%)
* **IV move**: -0.11 vol pts vs noise band ±1.21 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$62.5000`
* **Model ΔP (engine)**: `-$62.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$60.6722`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.8278` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$93.0121` | -148.8% | Stock moved from $354.88 to $356.27 (+1.3900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$2.8235` | -4.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$3.8759` | +6.2% | IV moved -0.20 vol pts (23.61% → 23.40%) |
| **Theta decay (Δt · Theta)** | `+$31.2875` | +50.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.8278` | -2.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$62.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.8278` (2.9% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.1832`
* Combined: `-$0.1832` | Residual after: `-$1.6446`

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
* Model attribution could still be nudged by small second-order effects or quote noise, but the decomposition already captures most of the move.
* No catalyst layer is supported here; do not infer a squeeze, borrow, or implied-volatility event from this tape.

---

### Position 3 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$147.5000` (+12.3%)
* **Model ΔP**: `+$147.5000`
* **Primary drivers**: **Delta PnL** (+130.1%) and **Vega PnL** (-27.0%) and **Theta decay** (-10.2%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best explained by the stock’s upward drift being carried through the option’s delta exposure, with gamma adding a smaller convexity boost. The model’s reprice is broadly consistent with that path, while the lower implied volatility worked against the call and theta also detracted. There is no separate news catalyst to layer in, and the observation lock means the run should be read as a factor attribution rather than a headline-driven event story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the dominant driver is clear and the residual is small, but observation reliability is flagged false and the market feed is limited. The Greek decomposition is still the right reference view, yet the setup does not support a more granular catalyst diagnosis.

---

## 2. Observation Lock

* **As-of**: `2026-11-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 15.3%)
* **IV move**: +0.82 vol pts vs noise band ±2.53 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$147.5000`
* **Model ΔP (engine)**: `+$147.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$145.8851`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.6149` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.1%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$191.8839` | +130.1% | Stock moved from $342.82 to $346.19 (+3.3700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$8.7477` | +5.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$39.7599` | -27.0% | IV moved -0.94 vol pts (23.63% → 22.69%) |
| **Theta decay (Δt · Theta)** | `-$14.9866` | -10.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.6149` | +1.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$147.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.6149` (1.1% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.7223`
* Combined: `+$0.7223` | Residual after: `+$0.8926`

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
* Watch whether a fuller surface reprice would change the balance between delta and convexity in the attribution.
* With no retrieved headlines and no named microstructure mechanism, do not force a borrow, squeeze, or implied-vol story into the tape.

---

### Position 4 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$120.0000` (-15.7%)
* **Model ΔP**: `-$120.0000`
* **Primary drivers**: **Delta PnL** (-120.2%) and **Vega PnL** (+23.0%) and **Theta decay** (-10.0%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained primarily by the put’s negative delta responding to a higher underlying spot, with gamma and vega partially offsetting that pressure and theta adding a smaller decay drag. The revaluation is internally consistent with the model, and the small residual leaves no need to force a separate catalyst story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is dominated by the model’s own delta bucket and the residual is low, but observation quality is not fully reliable and the first-pass market feed is limited. With no relevant headlines and the catalyst challenge skipped under observation lock, confidence rests on the engine decomposition rather than on an external news bridge.

---

## 2. Observation Lock

* **As-of**: `2026-11-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 17.9%)
* **IV move**: +1.48 vol pts vs noise band ±1.42 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$120.0000`
* **Model ΔP (engine)**: `-$120.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$119.0242`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.9758` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.8%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$144.2398` | -120.2% | Stock moved from $342.82 to $346.19 (+3.3700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$9.6229` | +8.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$27.5567` | +23.0% | IV moved +0.65 vol pts (21.70% → 22.35%) |
| **Theta decay (Δt · Theta)** | `-$11.9640` | -10.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.9758` | -0.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$120.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.9758` (0.8% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.6859`
* Combined: `-$0.6859` | Residual after: `-$0.2898`

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
* Higher-order convexity can still matter when spot gaps widen, so verify whether the full revaluation stays close to the Taylor view if moves become larger.
* No relevant catalyst tokens were retrieved, so do not infer a borrow, squeeze, or implied-volatility narrative without new tape evidence.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$1.0000` (-1.5%)
* **Model ΔP**: `+$1.0000`
* **Primary drivers**: **Theta decay** (+43.4%) and **Delta PnL** (-36.5%) and **Vega PnL** (-8.7%).
* **Verdict**: The run is dominated by time decay: the option’s modeled value was lifted mainly by passage of time, with spot slipping modestly and vol edging higher enough to partially offset that carry. The remaining gap is best read as model residual from higher-order effects and truncation, not as a separate catalyst, because there are no relevant headlines or microstructure tags to attach a news explanation to.
* **Confidence**: **Medium** — The dominant modeled factor is clear and the observation is reliable, but the attribution coverage is low and the residual band is high, so the Taylor view is only a reference rather than a complete explanation. There are no retrieved headlines or required Layer B mechanisms, and the early-exercise premium is negligible, which keeps the diagnosis focused on the model’s theta-led repricing.

---

## 2. Observation Lock

* **As-of**: `2026-11-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.1%)
* **IV move**: +0.29 vol pts vs noise band ±0.08 pts (exceeds noise band)
* **Prior observation**: `2026-11-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$1.0000`
* **Model ΔP (engine)**: `+$1.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$2.2057`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$3.2057` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (320.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$15.0241` | -36.5% | Stock moved from $757.12 to $754.37 (-2.7500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$1.5122` | -3.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$3.5702` | -8.7% | IV moved +0.29 vol pts (24.70% → 24.99%) |
| **Theta decay (Δt · Theta)** | `+$17.9007` | +43.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$3.2057` | +7.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$1.0000** | **+2.4%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$3.2057` (320.6% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.4865` | Volga PnL: `-$0.0523`
* Combined: `-$0.5388` | Residual after: `+$3.7445`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$17.8893`
* **spot**: `-$13.5105`
* **vol**: `-$3.3793`
* **rate**: `-$0.0048`
* Step sum: `+$0.9947` | Model ΔP: `+$1.0000` | Audit residual: `+$0.0053`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Check whether higher-order truncation or the full revaluation path still accounts for the residual gap versus the Taylor buckets.
* No catalyst layer was available here, so there is no headline-based borrow, squeeze, or IV-crush check to carry forward.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$1.0000` (-40.0%)
* **Model ΔP**: `-$1.0000`
* **Primary drivers**: **Vega PnL** (+33.5%) and **Delta PnL** (-27.2%) and **Theta decay** (-21.5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position’s modeled move was driven primarily by a reprice from higher implied volatility, with spot and time decay secondary and partially offset by convexity. Because the observation is unreliable and the residual is sizable, the full revaluation is the better headline than a pure Greeks story; the tape supports a model repricing rather than a clean single-factor move. There are no relevant headlines or named catalyst mechanisms to layer on top, so this remains a model-driven attribution. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The engine points to vega as the dominant modeled driver, but observation quality is flagged as unreliable and the residual is large, so the attribution should be treated as approximate. No relevant headlines were retrieved, and the catalyst critic was suppressed, so there is no independent news confirmation to strengthen a Layer B explanation.

---

## 2. Observation Lock

* **As-of**: `2026-11-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 66.7%)
* **IV move**: +1.17 vol pts vs noise band ±0.46 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$1.0000`
* **Model ΔP (engine)**: `-$1.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$0.4296`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.5704` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (57.0%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$1.5161` | -27.2% | Stock moved from $757.12 to $754.37 (-2.7500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.4175` | +7.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$1.8652` | +33.5% | IV moved +1.05 vol pts (12.74% → 13.80%) |
| **Theta decay (Δt · Theta)** | `-$1.1962` | -21.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.5704` | -10.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$1.0000** | **-18.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.5704` (57.0% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$1.9394` | Volga PnL: `+$0.5602`
* Combined: `-$1.3792` | Residual after: `+$0.8088`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$1.1942`
* **spot**: `-$0.6576`
* **vol**: `+$0.8515`
* **rate**: `-$0.0003`
* Step sum: `-$1.0005` | Model ΔP: `-$1.0000` | Audit residual: `+$0.0005`

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
* Monitor whether the residual remains elevated on a full-surface reprice or other path-dependent check, since truncation and quote noise can distort the Greek split.
* With no relevant catalyst digest available, verify whether the implied-vol move persists in subsequent marks before leaning on a volatility-only explanation.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$15.5000` (-8.6%)
* **Model ΔP**: `-$15.5000`
* **Primary drivers**: **Delta PnL** (-95.5%) and **Theta decay** (-24.2%) and **Vega PnL** (+20.3%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven primarily by the underlying slipping lower, which reduced the call’s intrinsic value and dominated the revaluation. Theta and a small residual also weighed on the option, while the volatility uptick partially offset the move but did not change the net direction. No named catalyst was retrieved, and the observation lock means the run should be read as a model revaluation rather than a news-led explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is clear from the blotter because the dominant modeled factor is the spot move and the residual is small. Confidence is still only medium because observation reliability is false, the vega narrative is suppressed, and no headlines were retrieved to independently challenge or confirm a catalyst story.

---

## 2. Observation Lock

* **As-of**: `2026-11-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 23.0%)
* **IV move**: +5.18 vol pts vs noise band ±9.44 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$15.5000`
* **Model ΔP (engine)**: `-$15.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$15.1579`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.3421` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.2%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$14.8046` | -95.5% | Stock moved from $46.55 to $46.36 (-0.1900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.2581` | +1.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$3.1443` | +20.3% | IV moved +1.54 vol pts (30.39% → 31.94%) |
| **Theta decay (Δt · Theta)** | `-$3.7557` | -24.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.3421` | -2.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$15.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.3421` (2.2% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.1749` | other second-order: `+$0.0314`
* Combined: `+$0.2063` | Residual after: `-$0.5484`

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
* Watch for Taylor truncation if spot moves become larger, since that can distort the reference decomposition relative to the full revaluation.
* No named catalyst was available; keep an eye on whether future tape or filing headlines add a borrow, squeeze, or implied volatility narrative, but do not infer one from this run.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.1050 | level_proxy(t) = 0.1961
* Δskew = -0.0088 | Δlevel = +0.0073
* Put 715 delta=-0.0567 | Call 795 delta=0.0034
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **plug_deep_otm** (PLUG): RuntimeError: Data break: T calibrated IV ~= quote-source IV failed. PLUG 4C 2026-12-18 mark 0.0300 on 2026-11-13 at spot 1.11 calibrates to 247.18% vol; the quote source reads 187.50% (+59.68 vol pts). A mark and a spot taken at different times produce this gap. No correction applied; nothing was narrated. This is a data problem, not an unexplained market move.
