# Live book run — 2026-10-14

Run `2026-10-14-1792026903`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=12`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-14` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$532.5000`
* **Total Model PnL**: `-$633.4358`
* **Aggregate model vs mark gap**: `-$100.9358`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `JPM 350P 2026-10-23` | `-$418.4358` |
| 2 | `SPY 795C 2026-11-20` | `-$264.5000` |
| 3 | `AAPL 325C 2026-11-20` | `+$170.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$541.3247` |
| Gamma | `+$54.8909` |
| Vega | `-$97.6417` |
| Theta | `-$38.9888` |
| Residual | `-$10.3715` |

### Notable underlyings

* **JPM**: `-$401.9358` aggregate option PnL
* **SPY**: `-$348.5000` aggregate option PnL
* **AAPL**: `+$82.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-14` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$170.0000` (+767.5%)
* **Model ΔP**: `+$170.0000`
* **Primary drivers**: **Delta PnL** (61%) and **Vega PnL** (29%) and **Theta decay** (7%).
* **Verdict**: The move is primarily explained by the stock’s rise, with the option’s positive directional exposure doing most of the work in the model revaluation. Vega also contributed meaningfully because implied volatility lifted over the day, while theta was a drag; the small residual is consistent with normal truncation rather than a separate story. There are no relevant headlines or named microstructure catalysts in the digest, so the attribution stays with the modeled spot and volatility inputs.
* **Confidence**: **Medium** — Confidence is medium because the blotter is reliable and the attribution coverage is high, but the run also shows a modest residual and the surface diagnostics note limitations. There are no retrieved headlines to support an auxiliary catalyst layer, so the explanation rests on the quant engine’s factor decomposition rather than external confirmation.

---

## 2. Observation Lock

* **As-of**: `2026-10-14` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 7.1%)
* **IV move**: +3.22 vol pts vs noise band ±2.45 pts (exceeds noise band)
* **Prior observation**: `2026-10-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$170.0000`
* **Model ΔP (engine)**: `+$170.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$171.9629`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.9629` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$125.4411` | +73.8% | Stock moved from $341.27 to $342.96 (+1.6900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.5697` | +0.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$60.0906` | +35.3% | IV moved +1.69 vol pts (29.60% → 32.82%) |
| **Theta decay (Δt · Theta)** | `-$15.1386` | -8.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.9629` | -1.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$170.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.9629` (1.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0114`
* Combined: `-$0.0114` | Residual after: `+$1.7114`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$1.6900` vs next cash dividend `+$0.2700` (gap `+$1.9600`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$23.8500` vs `+$23.9624` (gap `-$0.1124`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1133`
* **Dividend coverage** (dividend / time value): `0.05` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.6009`
* **Residual (Taylor ε)**: `-$0.0196`
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

* Watch whether the spot move remains the main source of day-to-day revaluation; a larger gap between the Taylor buckets and full reprice would point to higher-order convexity.
* Keep an eye on implied volatility and the mark quality, since the run uses a prior-chain IV source and the surface diagnostics indicate limitations in the calibration path.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.05 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-14` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$87.5000` (->1000%)
* **Model ΔP**: `-$87.5000`
* **Primary drivers**: **Delta PnL** (58%) and **Vega PnL** (27%) and **Theta decay** (13%).
* **Verdict**: The position’s move was driven mainly by the stock uptick against a short call, with gamma and theta secondary and only a modest vol contribution. The residual is negligible, so the Taylor decomposition is a clean read of the model revaluation rather than a truncation-driven exception. On the American side, early exercise is not a meaningful factor here; the dividend does not cover the remaining time value.
* **Confidence**: **Medium** — Confidence is medium because the attribution is internally consistent and the residual is small, but the feed contains no relevant headlines and the model notes local vol was deferred to mark calibration. The quote quality is reliable and the observation is reliable, yet the absence of a named catalyst limits Layer B support.

---

## 2. Observation Lock

* **As-of**: `2026-10-14` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.6%)
* **IV move**: +0.84 vol pts vs noise band ±0.35 pts (exceeds noise band)
* **Prior observation**: `2026-10-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$87.5000`
* **Model ΔP (engine)**: `-$87.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$87.7004`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.2004` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$68.6275` | +78.4% | Stock moved from $341.27 to $342.96 (+1.6900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$2.0642` | +2.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$32.2530` | +36.9% | IV moved +0.76 vol pts (25.71% → 26.56%) |
| **Theta decay (Δt · Theta)** | `+$15.2444` | -17.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.2004` | -0.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$87.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.2004` (0.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0049`
* Combined: `+$0.0049` | Residual after: `+$0.8701`

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

* Monitor whether further spot movement continues to dominate the revaluation, since the short call is still primarily delta-sensitive.
* Keep an eye on any implied-vol change or surface re-marking, but do not overread this run as an early-exercise case given the dividend coverage test.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-10-14` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$16.5000` (+>1000%)
* **Model ΔP**: `+$16.5000`
* **Primary drivers**: **Delta PnL** (49%) and **Vega PnL** (15%) and **Theta decay** (15%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position’s change was driven primarily by the favorable spot move in the underlying, with gamma adding convexity support while theta and vega offset part of the gain. The residual is sizable enough to indicate higher-order effects and Taylor truncation are contributing to the gap between the linear Greek view and the full revaluation, but there is no headline catalyst layer to add here. Early exercise is not a factor in this run because the American and European values are effectively aligned at the current marks. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The data quality flags keep confidence below high: observation reliability is off and the residual share is material, so the Greek split should be treated as a reference view rather than a complete explanation. The dominant driver is still clear from the blotter, and there are no relevant news hits or independent mechanisms to override it.

---

## 2. Observation Lock

* **As-of**: `2026-10-14` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 34.0%)
* **IV move**: -2.54 vol pts vs noise band ±1.16 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$16.5000`
* **Model ΔP (engine)**: `+$16.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$22.7792`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$6.2792` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (38.1%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$35.8590` | +217.3% | Stock moved from $331.43 to $335.28 (+3.8500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$9.2617` | +56.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$11.3353` | -68.7% | IV moved -1.24 vol pts (26.91% → 24.37%) |
| **Theta decay (Δt · Theta)** | `-$11.0063` | -66.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$6.2792` | -38.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$16.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$6.2792` (38.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0391`
* Combined: `-$0.0391` | Residual after: `+$0.2041`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1100`
* **spot**: `+$0.4135`
* **vol**: `-$0.1385`
* **rate**: `+$0.0003`
* Step sum: `+$0.1652` | Model ΔP: `+$0.1650` | Audit residual: `-$0.0002`

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
* Watch whether higher-order convexity and Taylor truncation continue to matter if spot keeps moving away from the previous close.
* Verify the next full revaluation against the same surface input path if the residual remains elevated; there is no separate borrow, squeeze, or IV-crush layer to monitor from the available tape.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-10-14` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$317.5000` (->1000%)
* **Model ΔP**: `-$418.4358`
* **Primary drivers**: **Delta PnL** (74%) and **Vega PnL** (18%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by delta: the put lost value as JPM traded higher, with gamma, theta, and the lower implied volatility acting as secondary drags rather than the main story. The residual is small enough to be consistent with ordinary Taylor truncation and pricing noise, while the run’s own diagnostics also flag that the observation is not fully reliable and should be treated as a model revaluation rather than a clean market-microstructure read. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the dominant modeled factor is clear, but the feed is flagged as not fully reliable and the engine limitations indicate failed IV calibration and local-vol handling. There are no retrieved headlines or relevant mechanism tags, so there is no catalyst layer to strengthen or overturn the blotter story; the unexplained break therefore stays as a watch item.

---

## 2. Observation Lock

* **As-of**: `2026-10-14` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 8.6%)
* **IV move**: -5.86 vol pts vs noise band ±5.25 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$317.5000`
* **Model ΔP (engine)**: `-$418.4358`
* **Model vs Mark gap**: `-$100.9358` (+24.1% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$410.8637`

* **Method residual (ε_method)**: `-$7.5721` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$100.9358` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.8%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$323.9350` | +77.4% | Stock moved from $331.43 to $335.28 (+3.8500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$10.4156` | -2.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$77.4640` | +18.5% | IV moved -5.86 vol pts (32.08% → 26.22%) |
| **Theta decay (Δt · Theta)** | `-$19.8802` | +4.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$7.5721` | +1.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$418.4358** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$7.5721` (1.8% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.1012`
* Combined: `-$0.1012` | Residual after: `-$4.0832`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1989`
* **spot**: `-$3.1805`
* **vol**: `-$0.8051`
* **rate**: `-$0.0014`
* Step sum: `-$4.1860` | Model ΔP: `-$4.1844` | Audit residual: `+$0.0016`

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
* Watch whether a fuller reprice versus the same engine changes the residual, since the current decomposition sits in a regime where truncation and calibration limits can matter.
* Monitor the next dividend and time-value relationship for any change in American exercise relevance; the current early-exercise premium is negligible relative to the option’s remaining time value.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-14` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$84.0000` (->1000%)
* **Model ΔP**: `-$84.0000`
* **Primary drivers**: **Delta PnL** (69%) and **Gamma PnL** (10%) and **Vega PnL** (10%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven primarily by the downside spot move, with the put gaining as the underlying sold off and the Taylor decomposition assigning the clear share of the move to delta. Gamma and vega were secondary contributors, while theta partially offset the move; the remaining gap is small and consistent with normal truncation and pricing noise. No relevant headline catalyst was retrieved, so the tape is explained by the model revaluation rather than an event-driven news shock. Caveats: This is a no-headline / no-relevant-news run, so the synthesis must stay within the model explanation only Gaps: LLM raised hard flag(s) ['quiet_day_confabulation'] that code could not confirm; downgraded to PARTIAL
* **Confidence**: **Medium** — The attribution coverage is high, the residual is low, and observation quality is reliable, which supports the modeled delta-led explanation. Confidence is capped at medium because the feed has no retrieved headlines and the run relies on the official engine view rather than an independently confirmed market catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-10-14` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.4%)
* **IV move**: +0.26 vol pts vs noise band ±0.04 pts (exceeds noise band)
* **Prior observation**: `2026-10-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$84.0000`
* **Model ΔP (engine)**: `-$84.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$83.1296`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.8704` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$71.2671` | +84.8% | Stock moved from $778.01 to $769.60 (-8.4100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$10.8494` | +12.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$10.7903` | +12.8% | IV moved +0.28 vol pts (19.70% → 19.96%) |
| **Theta decay (Δt · Theta)** | `+$9.7772` | -11.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.8704` | +1.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$84.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.8704` (1.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0236`
* Combined: `+$0.0236` | Residual after: `+$0.8164`

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

* **Verifier reflect**: This is a no-headline / no-relevant-news run, so the synthesis must stay within the model explanation only Gaps: LLM raised hard flag(s) ['quiet_day_confabulation'] that code could not confirm; downgraded to PARTIAL
* Watch whether future moves stay within the second-order Taylor envelope or start to show larger truncation from a sharper spot swing.
* With no relevant headline set, do not infer a borrow, squeeze, or IV-crush story from the tape alone.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-14` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$264.5000` (->1000%)
* **Model ΔP**: `-$264.5000`
* **Primary drivers**: **Delta PnL** (75%) and **Gamma PnL** (12%) and **Vega PnL** (7%).
* **Verdict**: The move is dominated by the downside spot move, with the call’s positive delta driving the revaluation lower. Gamma partially offset the loss through convexity, while vega and theta were smaller secondary drags. There are no relevant headlines in the blotter, so the run is explained by the modeled spot and volatility inputs rather than a separate catalyst.
* **Confidence**: **Medium** — Confidence is supported by high attribution coverage and a low residual band, but the session still has a small method residual and the market feed notes a deferred local-vol calibration limitation. With no retrieved headlines and no named microstructure tags, there is no Layer B catalyst to add.

---

## 2. Observation Lock

* **As-of**: `2026-10-14` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.5%)
* **IV move**: -0.44 vol pts vs noise band ±0.03 pts (exceeds noise band)
* **Prior observation**: `2026-10-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$264.5000`
* **Model ΔP (engine)**: `-$264.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$270.7638`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$6.2638` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$270.3732` | +102.2% | Stock moved from $778.01 to $769.60 (-8.4100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$42.6597` | -16.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$26.9565` | +10.2% | IV moved -0.30 vol pts (12.70% → 12.26%) |
| **Theta decay (Δt · Theta)** | `-$16.0939` | +6.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$6.2638` | -2.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$264.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$6.2638` (2.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0250`
* Combined: `+$0.0250` | Residual after: `-$2.6700`

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

* Watch whether a larger spot gap or a faster surface repricing would make the Taylor approximation less representative than the full revaluation.
* No headline-based catalyst was retrieved, so there is no borrow, squeeze, or IV-crush context to verify.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-14` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$34.5000` (+>1000%)
* **Model ΔP**: `+$34.5000`
* **Primary drivers**: **Delta PnL** (84%) and **Gamma PnL** (10%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was primarily driven by the underlying’s rise, with gamma a secondary support and theta a small offset. The model residual is negligible, so the Taylor decomposition is clean and the full revaluation is well explained by the spot move rather than any separate catalyst. Observation is locked and no relevant headlines were retrieved, so there is no basis for a borrow, squeeze, or implied-volatility narrative here. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is high and the residual is low, but observation reliability is flagged false and the news layer is empty. The option is American, yet the early-exercise premium is negligible, so there is no meaningful exercise boundary effect to elevate.

---

## 2. Observation Lock

* **As-of**: `2026-10-14` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 14.3%)
* **IV move**: +0.90 vol pts vs noise band ±1.62 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$34.5000`
* **Model ΔP (engine)**: `+$34.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$34.5377`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0377` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$32.1714` | +93.3% | Stock moved from $43.53 to $44.42 (+0.8900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$3.8131` | +11.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.3793` | +1.1% | IV moved +0.07 vol pts (27.69% → 28.59%) |
| **Theta decay (Δt · Theta)** | `-$1.8261` | -5.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0377` | -0.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$34.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0377` (0.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0003`
* Combined: `+$0.0003` | Residual after: `+$0.3447`

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
* Watch whether the next reprice stays dominated by spot; with the current decomposition, truncation or full-surface revaluation would be the main source of drift from the Taylor view.
* No headline-backed borrow, squeeze, or IV-crush mechanism is present; keep that layer empty unless new relevant tape appears.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-14` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (45%) and **Delta PnL** (38%) and **Gamma PnL** (5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position’s modeled move is led by the IV increase, with spot weakness and second-order curvature offsetting part of the option’s sensitivity. Because the observation is unreliable and the residual is large, the attribution should be read as a revaluation story rather than a clean tape-to-PnL map; the American vs European check shows no meaningful early-exercise effect. No relevant headlines were retrieved, so there is no supported Layer B catalyst to add beyond the volatility and spot move already inside the model. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is capped by unreliable observation, low attribution coverage, and a large unexplained remainder. The factor ranking is still clear from the blotter, but there is no headline support or named catalyst to strengthen the narrative, and the early-exercise premium is negligible.

---

## 2. Observation Lock

* **As-of**: `2026-10-14` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 66.7%)
* **IV move**: +9.37 vol pts vs noise band ±7.38 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.1134`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.1134` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.5934` | +38.4% | Stock moved from $1.56 to $1.45 (-0.1100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0846` | +5.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.6875` | +44.5% | IV moved +9.46 vol pts (118.75% → 128.13%) |
| **Theta decay (Δt · Theta)** | `-$0.0652` | +4.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.1134` | +7.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.1134` (>1000% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0012`
* Combined: `-$0.0012` | Residual after: `+$0.0012`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0007`
* **spot**: `-$0.0050`
* **vol**: `+$0.0056`
* **rate**: `+$0.0000`
* Step sum: `+$0.0000` | Model ΔP: `-$0.0000` | Audit residual: `-$0.0000`

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
* Watch whether the full-surface reprice and Taylor truncation continue to leave a sizable unexplained remainder versus the model.
* Monitor implied volatility and borrow-related tape only if future headlines or quote changes introduce a supported Layer B mechanism; none is evidenced in this run.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0770 | level_proxy(t) = 0.1611
* Δskew = +0.0070 | Δlevel = -0.0009
* Put 715 delta=-0.1141 | Call 795 delta=0.2172
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
