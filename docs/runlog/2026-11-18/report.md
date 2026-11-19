# Live book run — 2026-11-18

Run `2026-11-18-1795055026`. 8/8 legs diagnosed, 0 settled at expiry, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=11`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-18` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$381.5000`
* **Total Model PnL**: `+$263.8843`
* **Aggregate model vs mark gap**: `-$117.6157`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `JPM 340P 2026-12-18` | `+$355.0000` |
| 2 | `JPM 340C 2026-12-18` | `-$252.5000` |
| 3 | `SPY 715P 2026-11-20` | `+$112.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$150.2746` |
| Gamma | `+$50.9772` |
| Vega | `-$25.1470` |
| Theta | `+$87.0256` |
| Residual | `+$0.7539` |

### Notable underlyings

* **SPY**: `+$112.5000` aggregate option PnL
* **JPM**: `+$102.5000` aggregate option PnL
* **AAPL**: `+$44.8843` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-18` | **Status**: Verified by QuantLib (fdm_local_vol)

---

## 1. Headline

* **Mark MTM PnL**: `+$105.0000` (-0.5%)
* **Model ΔP**: `-$12.6157`
* **Primary drivers**: **Theta decay** (-46.7%) and **Delta PnL** (+40.3%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter’s modeled story is dominated by theta decay, with spot and vol contributing only minor offsets in the same engine revaluation. However, the attribution does not explain this move: the residual remains large, observation quality is weak, and the terminal break flag means the result needs human review rather than a clean one-factor read. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is limited by the low attribution coverage band, unreliable observation flag, and the terminal unexplained break. The gap is still unexplained after the diagnostic pass, and there are no relevant headlines or catalyst mechanisms to anchor a Layer B explanation.

---

## 2. Observation Lock

* **As-of**: `2026-11-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.3%)
* **IV move**: +1.05 vol pts vs noise band ±22.12 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$105.0000`
* **Model ΔP (engine)**: `-$12.6157`
* **Model vs Mark gap**: `-$117.6157` (+932.3% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$2.2221`

* **Method residual (ε_method)**: `-$10.3936` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$117.6157` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (82.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$49.1042` | +40.3% | Stock moved from $351.91 to $352.45 (+0.5400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1106` | +0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$5.4700` | +4.5% | IV moved +1.05 vol pts (67.46% → 68.51%) |
| **Theta decay (Δt · Theta)** | `-$56.9070` | -46.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$10.3936` | -8.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$12.6157** | **-10.3%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$10.3936` (82.4% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.1661` | other second-order: `+$0.0725`
* Combined: `-$0.0935` | Residual after: `-$10.3001`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$64.2388`
* **spot**: `+$51.6280`
* **vol**: `+$0.0000`
* **rate**: `+$0.0119`
* Step sum: `-$12.5989` | Model ΔP: `-$12.6157` | Audit residual: `-$0.0168`

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
* Watch whether a full-surface reprice or path-dependent effects materially change the attribution, since the residual is still large.
* Verify the marks and calibration status before relying on the model read, because the diagnostic pass did not fully explain the move.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$57.5000` (-11.0%)
* **Model ΔP**: `+$57.5000`
* **Primary drivers**: **Theta decay** (+133.4%) and **Delta PnL** (-54.7%) and **Vega PnL** (+29.7%).
* **Verdict**: The modeled move is dominated by time decay in the option’s value, with spot up only modestly and implied volatility lower on the day. Delta and gamma were secondary drags, while the residual is consistent with ordinary higher-order effects and full-engine path differences rather than a separate catalyst. There are no retrieved headlines or named microstructure signals, so the run is a clean factor story rather than a news-led reprice.
* **Confidence**: **Medium** — Confidence is moderate because attribution coverage is high and the dominant modeled factor is clear, but the residual is not trivial and the market move was small enough that higher-order effects can matter. The feed also has no relevant headlines, so there is no independent catalyst to corroborate or challenge the desk decomposition.

---

## 2. Observation Lock

* **As-of**: `2026-11-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.2%)
* **IV move**: -2.26 vol pts vs noise band ±0.76 pts (exceeds noise band)
* **Prior observation**: `2026-11-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$57.5000`
* **Model ΔP (engine)**: `+$57.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$61.7918`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$4.2918` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (7.5%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$31.4604` | -54.7% | Stock moved from $351.91 to $352.45 (+0.5400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.5440` | -0.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$17.0811` | +29.7% | IV moved -1.37 vol pts (32.80% → 31.42%) |
| **Theta decay (Δt · Theta)** | `+$76.7151` | +133.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$4.2918` | -7.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$57.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$4.2918` (7.5% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.2581`
* Combined: `-$0.2581` | Residual after: `-$4.0337`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$76.7922`
* **spot**: `-$32.8827`
* **vol**: `+$13.5873`
* **rate**: `-$0.0083`
* Step sum: `+$57.4885` | Model ΔP: `+$57.5000` | Audit residual: `+$0.0115`

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

* Verify whether the remaining gap is just truncation or a full-surface reprice effect in the FDM path.
* With no retrieved headlines, there is no borrow, squeeze, or IV-crush tape to monitor from the news side.

---

### Position 3 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$252.5000` (-42.4%)
* **Model ΔP**: `-$252.5000`
* **Primary drivers**: **Delta PnL** (-84.9%) and **Vega PnL** (-23.3%) and **Gamma PnL** (+10.3%).
* **Verdict**: The option loss was driven primarily by the underlying's move lower, which dominated the revaluation of this call. Gamma offset part of that move and the IV decline added a smaller headwind, while theta contributed the usual decay; the remaining gap is consistent with a low residual and second-order approximation limits rather than a separate catalyst. With no relevant headlines retrieved, there is no Layer B event story to add beyond the price and volatility move itself.
* **Confidence**: **Medium** — Confidence is medium because the attribution is dominated by the modeled delta move with a small residual and reliable observations, but there were no retrieved headlines to corroborate an external catalyst. The American versus European check shows negligible early-exercise effect, so there is no dividend or assignment angle to complicate the read.

---

## 2. Observation Lock

* **As-of**: `2026-11-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 13.1%)
* **IV move**: -1.12 vol pts vs noise band ±0.74 pts (exceeds noise band)
* **Prior observation**: `2026-11-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$252.5000`
* **Model ΔP (engine)**: `-$252.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$262.7248`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$10.2248` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$214.4003` | -84.9% | Stock moved from $329.96 to $324.11 (-5.8500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$26.1017` | +10.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$58.7362` | -23.3% | IV moved -1.62 vol pts (25.63% → 24.01%) |
| **Theta decay (Δt · Theta)** | `-$15.6899` | -6.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$10.2248` | +4.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$252.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$10.2248` (4.0% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$4.5750` | other second-order: `+$0.2428`
* Combined: `+$4.8178` | Residual after: `+$5.4070`

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

* Watch whether the next move is large enough to make the Taylor truncation less reliable; with a mostly delta-led day, a fresh full revaluation can still differ from the Greek split.
* No Layer B catalyst is available from the digest; keep an eye on any later headlines for borrow, squeeze, or implied-volatility context only if they actually appear.

---

### Position 4 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$355.0000` (+23.9%)
* **Model ΔP**: `+$355.0000`
* **Primary drivers**: **Delta PnL** (+106.7%) and **Vega PnL** (-13.7%) and **Gamma PnL** (+7.9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained first by delta exposure to the lower spot print, with gamma adding convexity in the same direction. Vega and theta were secondary offsets, while the small residual is consistent with ordinary truncation and quote noise rather than a separate event-driven gap. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is structurally clean and the dominant driver is clear, but observation reliability is limited and the surface note says local vol was deferred to mark calibration. The residual is low and there are no relevant headlines, so there is no supported Layer B catalyst to add.

---

## 2. Observation Lock

* **As-of**: `2026-11-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 9.8%)
* **IV move**: +1.01 vol pts vs noise band ±3.12 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$355.0000`
* **Model ΔP (engine)**: `+$355.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$345.1602`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$9.8398` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$378.6566` | +106.7% | Stock moved from $329.96 to $324.11 (-5.8500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$28.0523` | +7.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$48.7873` | -13.7% | IV moved -1.37 vol pts (24.01% → 22.64%) |
| **Theta decay (Δt · Theta)** | `-$12.7614` | -3.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$9.8398` | +2.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$355.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$9.8398` (2.8% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$4.9279` | other second-order: `+$0.2704`
* Combined: `+$5.1983` | Residual after: `+$4.6414`

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
* Watch whether the full revaluation versus Taylor view stays aligned if spot continues to move, since higher-order convexity can widen the gap when the underlying shifts further.
* Verify the time-value versus dividend setup if early exercise becomes more relevant, but the current premium is still modest.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$112.5000` (-43.7%)
* **Model ΔP**: `+$112.5000`
* **Primary drivers**: **Theta decay** (+94.1%) and **Vega PnL** (+54.2%) and **Delta PnL** (-40.8%).
* **Verdict**: The move is dominated by time decay in the model, with spot drift and the vol drop acting as secondary offsets rather than the main explanation. The residual is small enough to fit normal second-order and marking noise around the full revaluation, and there is no named catalyst or microstructure mechanism in the digest to add beyond the blotter factors.
* **Confidence**: **Medium** — Confidence is supported by high attribution coverage, a small residual band, reliable observation, and the engine’s clear dominant factor. Confidence is held to medium because the mark set is calibrated rather than fully clean, the spot move was modest, and no external headlines were retrieved to challenge or enrich the factor story.

---

## 2. Observation Lock

* **As-of**: `2026-11-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.8%)
* **IV move**: -3.16 vol pts vs noise band ±0.15 pts (exceeds noise band)
* **Prior observation**: `2026-11-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$112.5000`
* **Model ΔP (engine)**: `+$112.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$117.7070`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$5.2070` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$45.9145` | -40.8% | Stock moved from $732.44 to $730.20 (-2.2400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$3.2363` | -2.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$60.9875` | +54.2% | IV moved -3.23 vol pts (33.19% → 29.96%) |
| **Theta decay (Δt · Theta)** | `+$105.8702` | +94.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$5.2070` | -4.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$112.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$5.2070` (4.6% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$5.0023` | Volga PnL: `-$1.9546`
* Combined: `+$3.0476` | Residual after: `-$8.2546`

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

* Check whether the model remains stable if the full surface is repriced, since the short-dated setup can still be sensitive to truncation and quote noise.
* No relevant catalyst tags were retrieved, so there is no borrow, squeeze, or IV-crush watch item to layer onto this run.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (+48.9%) and **Theta decay** (-15.3%) and **Delta PnL** (-6.2%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by revaluation sensitivity to implied volatility, with spot and decay secondary in the Taylor view. However, the attribution does not explain this move cleanly: the terminal break flags a large unexplained gap, so the story needs human review rather than a single-factor explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation quality is weak, the residual is large, and the playbook explicitly says the attribution does not explain this move. The headline layer is empty, so there is no named catalyst to support a fuller Layer B explanation, and the gap remains unexplained.

---

## 2. Observation Lock

* **As-of**: `2026-11-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: +8.59 vol pts vs noise band ±1.72 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$1.7501`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.7501` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.3842` | -6.2% | Stock moved from $732.44 to $730.20 (-2.2400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0679` | +1.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$3.0064` | +48.9% | IV moved +8.21 vol pts (30.65% → 38.86%) |
| **Theta decay (Δt · Theta)** | `-$0.9400` | -15.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.7501` | -28.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **-0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.7501` (>1000% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.18).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (vanna, volga) — reference only, see Regime above
* Vanna PnL: `-$1.6544` | Volga PnL: `+$3.3668`
* Combined: `+$1.7124` | Residual after: `-$3.4625`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.9333`
* **spot**: `-$0.0285`
* **vol**: `+$0.9618`
* **rate**: `+$0.0000`
* Step sum: `+$0.0001` | Model ΔP: `-$0.0000` | Audit residual: `-$0.0001`

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
* Check whether a full-surface reprice or quote-quality issue is distorting the Taylor breakdown, since the residual is large and the pass is not fully explained.
* Verify whether the implied-vol move was stable in the source surface, because the move is being tagged to volatility revaluation but no catalyst evidence was retrieved.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$4.0000` (+3.3%)
* **Model ΔP**: `+$4.0000`
* **Primary drivers**: **Delta PnL** (+47.5%) and **Theta decay** (-29.9%) and **Vega PnL** (-13.5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is primarily a spot-driven revaluation of the call, with the model showing delta as the dominant Taylor contributor while gamma and theta partially offset the move. The residual is sizable relative to the modeled change, so the close-to-close decomposition should be read as a reference view rather than a complete explanation of the price path; with no relevant headlines and observation locked, there is no Layer B catalyst to add. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the dominant driver is clearly identified, but attribution coverage is low and the residual share is high. Observation reliability is false, there are no relevant headlines, and Vega narrative is suppressed, so the diagnostic should stay at the coarse model-reprice level.

---

## 2. Observation Lock

* **As-of**: `2026-11-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 18.6%)
* **IV move**: -4.49 vol pts vs noise band ±13.43 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$4.0000`
* **Model ΔP (engine)**: `+$4.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$1.6571`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$2.3429` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (58.6%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$14.5408` | +47.5% | Stock moved from $45.93 to $46.13 (+0.2000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.4187` | +1.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$4.1426` | -13.5% | IV moved -3.00 vol pts (38.24% → 35.24%) |
| **Theta decay (Δt · Theta)** | `-$9.1598` | -29.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$2.3429` | +7.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$4.0000** | **+13.1%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$2.3429` (58.6% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.2022` | other second-order: `+$0.0249`
* Combined: `+$0.2271` | Residual after: `+$2.1158`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$9.1646`
* **spot**: `+$15.8241`
* **vol**: `-$2.6590`
* **rate**: `+$0.0011`
* Step sum: `+$4.0016` | Model ΔP: `+$4.0000` | Audit residual: `-$0.0016`

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
* A large residual means higher-order terms, quote noise, or path effects may be distorting the Taylor split; verify against the full revaluation rather than over-reading the Greeks.
* With no relevant news or named microstructure token in the digest, do not force a catalyst story; this remains a model reprice diagnosis only.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Delta PnL** (+47.8%) and **Theta decay** (-36.7%) and **Vega PnL** (-9.3%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by delta from the higher underlying price, with gamma a smaller supportive contribution and theta offsetting part of the change. However, the attribution does not fully explain this move: the diagnostic pass leaves a terminal unexplained break, so this should be treated as a partial model read rather than a complete answer and needs human review. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation is unreliable, the residual is flagged as high, and the playbook explicitly says the attribution does not explain the move. There are no retrieved headlines or named catalyst mechanisms to support a Layer B explanation, and the remaining gap is unexplained rather than confirmed by a news event.

---

## 2. Observation Lock

* **As-of**: `2026-11-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: +0.00 vol pts vs noise band ±17.46 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0111`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0111` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.1324` | +47.8% | Stock moved from $1.05 to $1.08 (+0.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0061` | +2.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.0259` | -9.3% | IV moved -0.91 vol pts (225.17% → 224.27%) |
| **Theta decay (Δt · Theta)** | `-$0.1015` | -36.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0111` | -4.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **+0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0111` (>1000% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.0018`
* Combined: `-$0.0018` | Residual after: `-$0.0093`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.1015`
* **spot**: `+$0.1277`
* **vol**: `-$0.0262`
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
* Check whether the unexplained break is coming from Taylor truncation or a path-dependent revaluation effect rather than a clean one-factor move.
* Because no catalyst tape was retrieved, verify the quote quality and marks before assigning any external news-based explanation.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = -0.0911 | level_proxy(t) = 0.3451
* Δskew = -0.1176 | Δlevel = +0.0272
* Put 715 delta=-0.1668 | Call 795 delta=0.0017
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
