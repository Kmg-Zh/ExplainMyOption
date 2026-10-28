# Live book run — 2026-10-27

Run `2026-10-27-1793150106`. 6/8 legs completed, 2 failed. `legs_narrated=6` `legs_silent=0` `llm_calls=7`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-27` | **Positions**: 6 | **Tickers**: AAPL, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$262.0000`
* **Total Model PnL**: `-$216.1799`
* **Aggregate model vs mark gap**: `-$478.1799`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `-$233.1799` |
| 2 | `AAPL 350C 2026-11-20` | `-$122.5000` |
| 3 | `SPY 715P 2026-11-20` | `+$59.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$51.9392` |
| Gamma | `+$25.0147` |
| Vega | `-$179.3339` |
| Theta | `-$0.5089` |
| Residual | `-$9.4127` |

### Notable underlyings

* **AAPL**: `-$355.6799` aggregate option PnL
* **SPY**: `+$117.5000` aggregate option PnL
* **VZ**: `+$22.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-27` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$245.0000` (-854.2%)
* **Model ΔP**: `-$233.1799`
* **Primary drivers**: **Delta PnL** (73%) and **Vega PnL** (19%) and **Theta decay** (5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is dominated by the model’s delta exposure to the lower underlying, with gamma only cushioning the downside modestly. Vega is present in the Taylor bucket, but the run explicitly suppresses a vega narrative and the observation lock means the attribution should be kept at the coarser spot-driven level rather than over-interpreted. The remaining break is small in context and is consistent with higher-order truncation and quote noise rather than a separate catalyst. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by the observation lock, failed IV calibration checks, and the terminal unexplained break flagged by the code. The blotter still provides a clear dominant delta story with high attribution coverage, but there are no retrieved headlines to validate a Layer B mechanism, so the narrative should stay anchored to the model revaluation.

---

## 2. Observation Lock

* **As-of**: `2026-10-27` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 9.5%)
* **IV move**: +3.01 vol pts vs noise band ±4.30 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-26`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$245.0000`
* **Model ΔP (engine)**: `-$233.1799`
* **Model vs Mark gap**: `-$478.1799` (+205.1% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$237.5587`

* **Method residual (ε_method)**: `+$4.3788` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$478.1799` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$301.8843` | +129.5% | Stock moved from $347.73 to $343.91 (-3.8200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$6.6189` | -2.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$78.8422` | -33.8% | IV moved +3.01 vol pts (34.90% → 37.91%) |
| **Theta decay (Δt · Theta)** | `-$21.1356` | +9.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$4.3788` | -1.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$233.1799** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$4.3788` (1.9% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0880`
* Combined: `+$0.0880` | Residual after: `-$2.4198`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2113`
* **spot**: `-$2.9643`
* **vol**: `+$0.8440`
* **rate**: `+$0.0023`
* Step sum: `-$2.3293` | Model ΔP: `-$2.3318` | Audit residual: `-$0.0025`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$3.8200` vs next cash dividend `+$0.2700` (gap `-$3.5500`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$24.9675` vs `+$25.1104` (gap `-$0.1428`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1437`
* **Dividend coverage** (dividend / time value): `0.04` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.7884`
* **Residual (Taylor ε)**: `+$0.0438`
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
* Watch whether the unexplained remainder persists after a fresh full revaluation, since truncation and quote noise can distort the Taylor split when spot moves.
* Verify the next tape for any liquidity or surface-quality issues, but do not infer a squeeze, borrow, or IV-crush story from this run because no relevant headline mechanism was supplied.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-27` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$122.5000` (->1000%)
* **Model ΔP**: `-$122.5000`
* **Primary drivers**: **Vega PnL** (58%) and **Delta PnL** (33%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The desk revaluation is primarily driven by the change in implied volatility, with the spot decline and second-order spot effects acting as secondary offsets. Because the observation is locked and the support tools were not reliable, the correct read is the model’s full reprice rather than a finer causal claim from the headline tape. There is no named catalyst in the blotter, so the move is explained at the factor level without adding an external event story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — The code points to vega as the dominant modeled driver, but observation reliability is false and the Vega narrative is explicitly suppressed, so the attribution should stay coarse. The residual is only moderate, and the headline set is empty, which prevents a stronger catalyst-based diagnosis.

---

## 2. Observation Lock

* **As-of**: `2026-10-27` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.8%)
* **IV move**: +0.10 vol pts vs noise band ±0.36 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-26`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$122.5000`
* **Model ΔP (engine)**: `-$122.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$137.1246`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$14.6246` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (11.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$184.1634` | -150.3% | Stock moved from $347.73 to $343.91 (-3.8200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$13.9020` | +11.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$326.0082` | +266.1% | IV moved +8.99 vol pts (28.89% → 28.99%) |
| **Theta decay (Δt · Theta)** | `+$18.6223` | -15.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$14.6246` | -11.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$122.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$14.6246` (11.9% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0140`
* Combined: `-$0.0140` | Residual after: `+$1.2390`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1862`
* **spot**: `-$1.6937`
* **vol**: `+$3.1051`
* **rate**: `+$0.0014`
* Step sum: `+$1.2266` | Model ΔP: `+$1.2250` | Audit residual: `-$0.0016`

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
* Check whether the full-surface repricing and Taylor truncation are distorting the factor split, especially given the moderate residual and the larger spot move.
* Watch for any later-confirmed implied-vol move or quote-quality issue before treating the vega attribution as economically clean.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-27` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$59.0000` (+>1000%)
* **Model ΔP**: `+$59.0000`
* **Primary drivers**: **Delta PnL** (64%) and **Theta decay** (16%) and **Vega PnL** (13%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven primarily by the spot move, with the short put benefiting from the underlying rally as the dominant modeled factor. The Greek decomposition also shows offsetting theta and smaller gamma and vega effects, while the unexplained remainder is minimal and consistent with normal Taylor truncation noise. No named catalyst or microstructure mechanism is available in the blotter, so this is a clean factor-led revaluation rather than a headline-driven gap. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the observation is not fully reliable and there are no relevant headlines to validate a separate catalyst story. The residual is low, but the short-dated option and the suppression of the Vega narrative mean the safest read is the coded delta-led move only.

---

## 2. Observation Lock

* **As-of**: `2026-10-27` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.1%)
* **IV move**: -0.02 vol pts vs noise band ±0.03 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-26`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$59.0000`
* **Model ΔP (engine)**: `+$59.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$58.5638`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.4362` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$63.0866` | +106.9% | Stock moved from $759.97 to $765.37 (+5.4000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$6.9812` | -11.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$12.9169` | -21.9% | IV moved +0.33 vol pts (21.83% → 21.81%) |
| **Theta decay (Δt · Theta)** | `+$15.3753` | +26.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.4362` | +0.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$59.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.4362` (0.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0165`
* Combined: `-$0.0165` | Residual after: `-$0.5735`

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
* Watch whether a larger spot continuation would make higher-order convexity more important than the current Taylor view.
* With no retrieved headlines, do not infer a squeeze, borrow, or implied-vol story; keep the focus on the revaluation mechanics already in the blotter.

---

### Position 4 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-27` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$58.5000` (+>1000%)
* **Model ΔP**: `+$58.5000`
* **Primary drivers**: **Delta PnL** (69%) and **Theta decay** (12%) and **Gamma PnL** (11%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained first by directional exposure: the position benefited from the underlying’s rise, with gamma adding a secondary convexity boost. Offsetting that, theta decay and a small implied-volatility dip reduced the mark, leaving a modest residual consistent with higher-order effects and Taylor truncation rather than a separate catalyst. No relevant headlines were retrieved, so there is no Layer B event story to add beyond the model revaluation. Caveats: Layer A is supported: the dominant driver is delta, matching the code-supplied primary driver and the described spot move Gaps: No headline evidence is available, so Layer B cannot be independently verified from retrieved news. The narrative’s statement that no relevant headlines were retrieved is consistent with the evidence set, but it cannot be corroborated further.
* **Confidence**: **Medium** — The attribution is supported by a clean, marked feed and a high coverage band, but the residual is not negligible and the move includes both convexity and carry effects. There are no retrieved headlines and the catalyst brief was skipped, so the diagnosis stays at the model-driven level rather than a news-led explanation.

---

## 2. Observation Lock

* **As-of**: `2026-10-27` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.9%)
* **IV move**: +0.12 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-10-26`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$58.5000`
* **Model ΔP (engine)**: `+$58.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$61.4742`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$2.9742` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (5.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$66.9734` | +114.5% | Stock moved from $759.97 to $765.37 (+5.4000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$10.7194` | +18.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$4.1283` | -7.1% | IV moved -0.10 vol pts (12.85% → 12.97%) |
| **Theta decay (Δt · Theta)** | `-$12.0904` | -20.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$2.9742` | -5.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$58.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$2.9742` (5.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0099`
* Combined: `-$0.0099` | Residual after: `+$0.5949`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1208`
* **spot**: `+$0.7543`
* **vol**: `-$0.0487`
* **rate**: `+$0.0012`
* Step sum: `+$0.5860` | Model ΔP: `+$0.5850` | Audit residual: `-$0.0010`

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

* **Verifier reflect**: Layer A is supported: the dominant driver is delta, matching the code-supplied primary driver and the described spot move Gaps: No headline evidence is available, so Layer B cannot be independently verified from retrieved news. The narrativ
* Higher-order convexity and Taylor truncation can still affect the residual even when delta is dominant; verify the full revaluation remains consistent with the close-to-close move.
* No Layer B catalyst was identified, so there is no borrow, squeeze, or IV-crush tape to monitor from the headline set.

---

### Position 5 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-27` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$22.0000` (+>1000%)
* **Model ΔP**: `+$22.0000`
* **Primary drivers**: **Vega PnL** (41%) and **Delta PnL** (31%) and **Gamma PnL** (14%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter’s modeled driver is Vega: the option revalued higher as implied volatility moved, even though the spot drop and theta decay worked against it. Because observation is unreliable and the Vega narrative is suppressed, treat this as a full revaluation outcome rather than a finely decomposed economics story; the large residual and failed surface diagnostics suggest higher-order model effects and path dependence are doing meaningful work. There are no retrieved headlines or approved microstructure tags, so there is no supported catalyst layer beyond the volatility revaluation itself. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is only medium because the observation flag is off, the residual share is large, and the surface diagnostics failed, which limits how far the Taylor decomposition can be trusted. The news layer is empty, and the brief explicitly blocks inventing a squeeze, borrow, or IV-crush catalyst from outside evidence.

---

## 2. Observation Lock

* **As-of**: `2026-10-27` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 12.8%)
* **IV move**: -0.49 vol pts vs noise band ±1.15 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-26`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$22.0000`
* **Model ΔP (engine)**: `+$22.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$47.8745`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$25.8745` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (117.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$64.2231` | -291.9% | Stock moved from $44.66 to $43.10 (-1.5600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$28.5589` | +129.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$84.7376` | +385.2% | IV moved +18.71 vol pts (27.10% → 26.61%) |
| **Theta decay (Δt · Theta)** | `-$1.1989` | -5.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$25.8745` | -117.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$22.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$25.8745` (117.6% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.44).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (Layer 3) — reference only, see Regime above
* other second-order: `-$0.0330`
* Combined: `-$0.0330` | Residual after: `+$0.2530`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0120`
* **spot**: `-$0.3853`
* **vol**: `+$0.6173`
* **rate**: `+$0.0001`
* Step sum: `+$0.2202` | Model ΔP: `+$0.2200` | Audit residual: `-$0.0002`

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
* Treat the Taylor split as reference only; the large residual and surface failure mean higher-order effects and full revaluation matter here.
* With no retrieved headlines or microstructure tags, do not infer a borrow, squeeze, or other catalyst from the tape alone.

---

### Position 6 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-27` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Vega PnL** (50%) and **Theta decay** (29%) and **Delta PnL** (20%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is best described by time decay as the dominant Taylor component, with the option’s small spot response and convexity effects secondary in the revaluation. Because observation quality is locked down and the Vega narrative is suppressed by the code, the headline read should stay at the model layer: this is a low-confidence attribution where the residual is large relative to the unchanged model price, so higher-order truncation and mark noise are the most plausible explanation for the gap. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because the run flags observation unreliability, a high residual band, and a terminal unexplained break, while no relevant headlines were retrieved. The code also suppresses a Vega narrative, so the attribution should stay coarse and avoid over-reading the factor mix.

---

## 2. Observation Lock

* **As-of**: `2026-10-27` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 66.7%)
* **IV move**: -3.12 vol pts vs noise band ±8.65 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-26`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0036`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0036` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.0553` | +19.7% | Stock moved from $1.38 to $1.37 (-0.0100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0007` | +0.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.1398` | +49.7% | IV moved +2.38 vol pts (150.00% → 146.88%) |
| **Theta decay (Δt · Theta)** | `-$0.0816` | +29.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0036` | +1.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0036` (>1000% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0000`
* Combined: `-$0.0000` | Residual after: `+$0.0000`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0008`
* **spot**: `-$0.0005`
* **vol**: `+$0.0013`
* **rate**: `+$0.0000`
* Step sum: `+$0.0000` | Model ΔP: `+$0.0000` | Audit residual: `-$0.0000`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Watch whether the full revaluation continues to diverge from the Greek decomposition, since truncation and quote quality can dominate when the run is this noisy.
* Verify the mark and surface inputs rather than forcing a news-based explanation; no relevant catalyst set was identified in the digest.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0883 | level_proxy(t) = 0.1739
* Δskew = -0.0014 | Δlevel = +0.0005
* Put 715 delta=-0.0923 | Call 795 delta=0.1606
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **jpm_straddle_call** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-10-30, 2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
- **jpm_straddle_put** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-10-30, 2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
