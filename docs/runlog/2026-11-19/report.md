# Live book run — 2026-11-19

Run `2026-11-19-1795141603`. 7/8 legs diagnosed, 0 settled at expiry, 1 failed. `legs_narrated=7` `legs_silent=0` `llm_calls=9`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-19` | **Positions**: 7 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$19.5000`
* **Total Model PnL**: `+$19.5000`
* **Aggregate model vs mark gap**: `+$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `-$332.5000` |
| 2 | `AAPL 350C 2026-11-20` | `+$250.0000` |
| 3 | `JPM 340P 2026-12-18` | `+$250.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$51.2462` |
| Gamma | `+$5.6118` |
| Vega | `-$51.6655` |
| Theta | `+$27.8716` |
| Residual | `-$13.5640` |

### Notable underlyings

* **JPM**: `+$144.5000` aggregate option PnL
* **AAPL**: `-$82.5000` aggregate option PnL
* **VZ**: `-$42.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-19` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$332.5000` (-11.9%)
* **Model ΔP**: `-$332.5000`
* **Primary drivers**: **Delta PnL** (-93.0%) and **Vega PnL** (+12.0%) and **Theta decay** (-9.9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained first by a spot drop in a deep-in-the-money call, so the dominant modeled driver is delta. The residual is meaningful, but with no retrieved headlines and observation marked unreliable, it should be treated as model truncation and path effects around the full revaluation rather than a separate catalyst story. The large implied-vol move is part of the reprice, but the run suppresses a Vega narrative here, so it should not be elevated as the explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is only medium because observation quality is flagged as unreliable, the residual is material, and the model notes local-vol calibration limits. The data support a clear delta-led revaluation, but the feed does not support a stronger event-based explanation, and no relevant headline mechanism is available to anchor Layer B.

---

## 2. Observation Lock

* **As-of**: `2026-11-19` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.7%)
* **IV move**: +15.38 vol pts vs noise band ±33.31 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$332.5000`
* **Model ΔP (engine)**: `-$332.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$299.1486`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$33.3514` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (10.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$309.1724` | -93.0% | Stock moved from $352.45 to $349.21 (-3.2400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$2.9280` | +0.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$40.0352` | +12.0% | IV moved +15.96 vol pts (66.05% → 82.01%) |
| **Theta decay (Δt · Theta)** | `-$32.9393` | -9.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$33.3514` | -10.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$332.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$33.3514` (10.0% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$11.4338` | Volga PnL: `+$13.2038`
* Combined: `+$24.6376` | Residual after: `-$57.9890`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$32.7970`
* **spot**: `-$319.7908`
* **vol**: `+$20.0895`
* **rate**: `+$0.0017`
* Step sum: `-$332.4966` | Model ΔP: `-$332.5000` | Audit residual: `-$0.0034`

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
* Model attribution can still be distorted by truncation and full-surface reprice effects when spot and vol both move together.
* Do not infer an IV-crush or borrow story here; the diagnostic feed provides no relevant headline mechanism to support one.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-19` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$250.0000` (-53.5%)
* **Model ΔP**: `+$250.0000`
* **Primary drivers**: **Delta PnL** (+81.1%) and **Theta decay** (+36.6%) and **Vega PnL** (-13.0%).
* **Verdict**: The run is driven first by the position’s positive delta exposure as spot moved lower into expiry, with gamma and vega both working against part of that move and theta providing offsetting carry. The residual is modest and fits a short-dated American option where higher-order effects and path dependence can leave a small gap between the Taylor view and the full revaluation. No named catalyst is available in the digest, so this is a model-driven price move rather than a news-led one.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is strong and the dominant driver is clear, but the position is near expiry and the residual is not trivial. The feed has no relevant headlines, so there is no external catalyst to anchor the gap story beyond the model dynamics.

---

## 2. Observation Lock

* **As-of**: `2026-11-19` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.2%)
* **IV move**: +2.78 vol pts vs noise band ±0.48 pts (exceeds noise band)
* **Prior observation**: `2026-11-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$250.0000`
* **Model ΔP (engine)**: `+$250.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$237.4975`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$12.5025` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (5.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$202.7403` | +81.1% | Stock moved from $352.45 to $349.21 (-3.2400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$24.2632` | -9.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$32.4916` | -13.0% | IV moved +3.29 vol pts (31.42% → 34.71%) |
| **Theta decay (Δt · Theta)** | `+$91.5119` | +36.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$12.5025` | +5.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$250.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$12.5025` (5.0% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$5.3447` | other second-order: `-$0.1451`
* Combined: `-$5.4898` | Residual after: `+$17.9923`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$91.6689`
* **spot**: `+$182.1331`
* **vol**: `-$23.8035`
* **rate**: `-$0.0009`
* Step sum: `+$249.9976` | Model ΔP: `+$250.0000` | Audit residual: `+$0.0024`

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

* Short-dated options can still show small model-vs-Taylor gaps from truncation and path dependence even when the dominant driver is clear.
* With no relevant headlines retrieved, verify whether the move was purely a spot-and-vol revaluation rather than a catalyst-driven repricing.

---

### Position 3 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-19` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$105.5000` (-30.8%)
* **Model ΔP**: `-$105.5000`
* **Primary drivers**: **Delta PnL** (-96.6%) and **Theta decay** (-11.9%) and **Gamma PnL** (+10.5%).
* **Verdict**: The move is explained primarily by the stock’s decline, which pushed the call lower and dominated the one-day revaluation. Gamma and theta partly offset that move, while the small implied-vol change and the negligible early-exercise premium kept the story centered on directional exposure rather than exercise or surface effects. No relevant headlines were retrieved, so there is no separate catalyst layer to add beyond the modeled spot-driven reprice.
* **Confidence**: **Medium** — The attribution is clean and the coverage is strong, but the residual is not zero and the run notes a deferred local-vol calibration, so the result should be read as a model revaluation rather than a fully tradeable mark explanation. With no retrieved headlines and no named microstructure mechanism, there is no additional catalyst evidence to strengthen or challenge the spot-led diagnosis.

---

## 2. Observation Lock

* **As-of**: `2026-11-19` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.4%)
* **IV move**: -0.76 vol pts vs noise band ±0.16 pts (exceeds noise band)
* **Prior observation**: `2026-11-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$105.5000`
* **Model ΔP (engine)**: `-$105.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$107.4268`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.9268` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$101.9543` | -96.6% | Stock moved from $324.11 to $320.22 (-3.8900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$11.0343` | +10.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$3.9020` | -3.7% | IV moved -0.13 vol pts (24.02% → 23.89%) |
| **Theta decay (Δt · Theta)** | `-$12.6048` | -11.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.9268` | +1.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$105.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.9268` (1.8% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.4076`
* Combined: `+$0.4076` | Residual after: `+$1.5192`

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

* Check whether higher-order convexity or surface recalibration would widen the residual if the spot move becomes larger than the current band.
* With no relevant headlines or named tape mechanism, keep watching for any later information on implied volatility or liquidity rather than assuming a separate catalyst is present.

---

### Position 4 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-19` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$250.0000` (+13.6%)
* **Model ΔP**: `+$250.0000`
* **Primary drivers**: **Delta PnL** (+117.9%) and **Vega PnL** (-24.7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven primarily by the downside move in the underlying, which helped the put gain value through its negative delta. Gamma added a small convexity lift, while the residual is consistent with higher-order Taylor effects and the American model path, not a separate news catalyst. There are no relevant headlines in the digest, so Layer B remains empty and no borrow, squeeze, or IV-crush explanation is supported. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The factor decomposition is clear and the dominant modeled driver is well identified, but observation reliability is flagged as weak and the residual is not negligible. Vega is suppressed by the diagnostics, and there are no relevant headlines to anchor a separate catalyst story.

---

## 2. Observation Lock

* **As-of**: `2026-11-19` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 6.2%)
* **IV move**: -2.61 vol pts vs noise band ±3.08 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$250.0000`
* **Model ΔP (engine)**: `+$250.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$234.8891`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$15.1109` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (6.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$294.6881` | +117.9% | Stock moved from $324.11 to $320.22 (-3.8900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$11.6771` | +4.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$61.7010` | -24.7% | IV moved -2.14 vol pts (22.62% → 20.48%) |
| **Theta decay (Δt · Theta)** | `-$9.7750` | -3.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$15.1109` | +6.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$250.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$15.1109` (6.0% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$7.3555` | other second-order: `+$1.3614`
* Combined: `+$8.7169` | Residual after: `+$6.3940`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$9.7742`
* **spot**: `+$307.6462`
* **vol**: `-$47.8748`
* **rate**: `-$0.0278`
* Step sum: `+$249.9695` | Model ΔP: `+$250.0000` | Audit residual: `+$0.0305`

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
* Watch whether the gap between the reference decomposition and the full revaluation stays contained, since truncation and model-path effects can still distort the attribution.
* No headline-based catalyst is supported here; with no relevant news, avoid layering in borrow, squeeze, or implied-vol narratives that are not in the blotter.

---

### Position 5 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-19` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Vega PnL** (+37.7%) and **Gamma PnL** (+12.3%) and **Delta PnL** (-11.2%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled attribution points to vega as the dominant factor, with spot and theta secondary and gamma partly offsetting the move. But the attribution does not explain this move: the residual is large, the observation is not reliable, and the case needs human review rather than a single-factor story. There are no retrieved headlines, so there is no confirmed catalyst layer to anchor the unexplained gap. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because the diagnostic gap is large, the residual is material, and the observation is flagged as not reliable. The vol move was extreme and the model’s factor stack does not fully reconcile the full revaluation, so the run explains only part of the price change and the remainder is still unexplained.

---

## 2. Observation Lock

* **As-of**: `2026-11-19` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: +23.44 vol pts vs noise band ±2.87 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$7.3045`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$7.3045` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$2.3878` | -11.2% | Stock moved from $730.20 to $715.87 (-14.3300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$2.6233` | +12.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$8.0734` | +37.7% | IV moved +27.81 vol pts (38.86% → 66.67%) |
| **Theta decay (Δt · Theta)** | `-$1.0044` | -4.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$7.3045` | -34.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **+0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$7.3045` (>1000% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 1.10).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (vanna, volga) — reference only, see Regime above
* Vanna PnL: `-$28.4078` | Volga PnL: `+$25.8855`
* Combined: `-$2.5222` | Residual after: `-$4.7823`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.9949`
* **spot**: `-$0.0050`
* **vol**: `+$1.0000`
* **rate**: `+$0.0000`
* Step sum: `+$0.0000` | Model ΔP: `+$0.0000` | Audit residual: `-$0.0000`

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
* Check whether the unexplained break persists under a full-surface reprice and quote-quality review; truncation and surface limitations can distort the modeled attribution.
* No headline mechanism was retrieved, so there is no confirmed catalyst layer to validate; keep an eye on whether an IV move or liquidity issue appears in a later tape review.

---

### Position 6 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-19` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$42.5000` (-34.4%)
* **Model ΔP**: `-$42.5000`
* **Primary drivers**: **Delta PnL** (-76.4%) and **Theta decay** (-17.0%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven primarily by the lower underlying price, which pushed the call lower and dominated the day’s revaluation. Theta decay added to the move, while the small residual is consistent with second-order effects from the option’s short-dated profile rather than a separate news catalyst. No relevant headlines were retrieved, so Layer B is not used to explain the move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is clear on the blotter, but observation reliability is false and the residual is not trivial for such a short-dated option. Vega narration is additionally suppressed by the desk flags, so the diagnosis stays at the coarse revaluation level rather than over-claiming a market catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-11-19` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 19.8%)
* **IV move**: -2.54 vol pts vs noise band ±13.23 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$42.5000`
* **Model ΔP (engine)**: `-$42.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$40.0833`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$2.4167` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (5.7%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$32.4494` | -76.4% | Stock moved from $46.13 to $45.74 (-0.3900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.5956` | +3.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$2.0174` | -4.7% | IV moved -2.36 vol pts (35.23% → 32.88%) |
| **Theta decay (Δt · Theta)** | `-$7.2121` | -17.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$2.4167` | -5.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$42.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$2.4167` (5.7% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.4401` | other second-order: `+$0.0315`
* Combined: `-$0.4086` | Residual after: `-$2.0081`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$7.2056`
* **spot**: `-$33.8254`
* **vol**: `-$1.4689`
* **rate**: `+$0.0002`
* Step sum: `-$42.4997` | Model ΔP: `-$42.5000` | Audit residual: `-$0.0003`

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
* Monitor whether the remaining move is still dominated by full revaluation effects, since short-dated options can show truncation and path sensitivity beyond the Taylor breakdown.
* No relevant news, borrow, or IV-crush tape was provided; do not force a catalyst story without an actual headline set.

---

### Position 7 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-19` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (+47.7%) and **Delta PnL** (-30.8%) and **Theta decay** (-14.8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter points to Vega as the dominant modeled driver, but the attribution does not explain this move and the run should be treated as a terminal break needing human review. Spot was small while implied volatility moved sharply, so the revaluation is consistent with a volatility-led repricing; however, the diagnostic budget leaves a large part of the move unexplained rather than fully reconciled. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Low** — Confidence is low because observation quality is weak, headline support is absent, and the run is flagged as a terminal unexplained break. The residual is large relative to the explained move, the surface diagnostics are strained, and the attribution should be treated as incomplete rather than economically closed.

---

## 2. Observation Lock

* **As-of**: `2026-11-19` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: +12.50 vol pts vs noise band ±18.35 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0316`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0316` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.2183` | -30.8% | Stock moved from $1.08 to $1.03 (-0.0500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0167` | +2.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.3380` | +47.7% | IV moved +11.80 vol pts (224.27% → 236.07%) |
| **Theta decay (Δt · Theta)** | `-$0.1047` | -14.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0316` | -4.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **-0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0316` (>1000% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.0425` | Volga PnL: `+$0.0303`
* Combined: `-$0.0123` | Residual after: `-$0.0193`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.1047`
* **spot**: `-$0.1849`
* **vol**: `+$0.2896`
* **rate**: `+$0.0000`
* Step sum: `+$0.0000` | Model ΔP: `-$0.0000` | Audit residual: `-$0.0000`

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
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Layer A remains fragile: the Greek decomposition is only a reference view here, and the unexplained break means the model revaluation should be reviewed for surface, calibration, or path-reprice issues.
* Layer B is empty: no relevant headlines or named microstructure mechanisms were retrieved, so do not infer IV crush, borrow stress, or squeeze from background tape.

---


## Errors

- **spy_reversal_put** (SPY): RuntimeError: Failed to perform, curl: (28) Operation timed out after 1004592 milliseconds with 0 bytes received. See https://curl.se/libcurl/c/libcurl-errors.html first for more details.
