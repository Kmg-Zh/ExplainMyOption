# Live book run — 2026-09-23

Run `2026-09-23-1790212502`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=10`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-09-23` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$328.0000`
* **Total Model PnL**: `-$458.5546`
* **Aggregate model vs mark gap**: `-$130.5546`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `-$240.0000` |
| 2 | `SPY 795C 2026-11-20` | `-$221.5000` |
| 3 | `JPM 350P 2026-10-23` | `+$132.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$213.0620` |
| Gamma | `+$320.8442` |
| Vega | `-$493.3749` |
| Theta | `-$45.4472` |
| Residual | `-$27.5147` |

### Notable underlyings

* **SPY**: `-$301.5000` aggregate option PnL
* **AAPL**: `-$110.0000` aggregate option PnL
* **VZ**: `-$106.0546` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-09-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$240.0000` (-995.9%)
* **Model ΔP**: `-$240.0000`
* **Primary drivers**: **Vega PnL** (79%) and **Delta PnL** (14%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven by a modeled revaluation on the option surface, with the IV decline doing the heavy lifting in the Taylor view. Spot drift was small enough that delta was secondary, and the remaining gap is consistent with higher-order curvature and model truncation rather than a separate narrative catalyst. Because observation quality was weak and Vega narrative is suppressed, this should be read as a model-based repricing rather than a news-led move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — The official attribution points clearly to the modeled vol move, but observation reliability is false and the diagnostic guidance explicitly suppresses a Vega narrative. The residual is only medium, and there are no retrieved headlines or named microstructure mechanisms to anchor a stronger catalyst story.

---

## 2. Observation Lock

* **As-of**: `2026-09-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 7.8%)
* **IV move**: -0.07 vol pts vs noise band ±1.90 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$240.0000`
* **Model ΔP (engine)**: `-$240.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$252.6942`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$12.6942` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (5.3%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$52.7150` | -22.0% | Stock moved from $338.98 to $339.75 (+0.7700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.2759` | -0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$291.8382` | +121.6% | IV moved -6.03 vol pts (30.14% → 30.07%) |
| **Theta decay (Δt · Theta)** | `-$13.8469` | +5.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$12.6942` | -5.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$240.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$12.6942` (5.3% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0645`
* Combined: `+$0.0645` | Residual after: `-$2.4645`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1384`
* **spot**: `+$0.5304`
* **vol**: `-$2.7926`
* **rate**: `+$0.0083`
* Step sum: `-$2.3923` | Model ΔP: `-$2.4000` | Audit residual: `-$0.0077`

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
* Check the full-surface reprice and path-based explanation against the quoted vol move, since the Taylor view is only approximate here.
* No catalyst-specific action is supported from the tape because no relevant headlines or microstructure tags were retrieved.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-09-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$130.0000` (+1268.3%)
* **Model ΔP**: `+$130.0000`
* **Primary drivers**: **Vega PnL** (76%) and **Delta PnL** (16%) and **Theta decay** (7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model revaluation is dominated by the implied-volatility move, with smaller help from time decay and a modest offset from spot drift; the Taylor residual is negligible, so the move is largely explained by the engine inputs. Layer B is effectively absent here: there are no retrieved headlines, no named microstructure tokens, and the observation lock suppresses a stronger catalyst read, so this should be treated as a clean factor-driven repricing rather than a news-led event. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — The attribution is internally consistent and the residual is low, but observation quality is not reliable and the feed explicitly suppresses a stronger Vega narrative. The headline set is empty, so there is no independent catalyst support to widen the story beyond the modeled IV move and carry.

---

## 2. Observation Lock

* **As-of**: `2026-09-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.4%)
* **IV move**: -0.08 vol pts vs noise band ±0.28 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$130.0000`
* **Model ΔP (engine)**: `+$130.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$130.7850`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.7850` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$32.4260` | -24.9% | Stock moved from $338.98 to $339.75 (+0.7700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.3274` | -0.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$150.2913` | +115.6% | IV moved -2.82 vol pts (26.98% → 26.90%) |
| **Theta decay (Δt · Theta)** | `+$13.2471` | +10.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.7850` | -0.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$130.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.7850` (0.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0034`
* Combined: `-$0.0034` | Residual after: `-$1.2966`

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
* Recheck the full-surface repricing and quote quality around the volatility move, since the engine attribution is mostly a Vega-led revaluation with a very small residual.
* No separate catalyst mechanism is evidenced in the blotter, so avoid forcing a news or borrow explanation without new inputs.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-09-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$72.5000` (-1223.6%)
* **Model ΔP**: `-$72.5000`
* **Primary drivers**: **Delta PnL** (46%) and **Vega PnL** (31%) and **Gamma PnL** (16%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by the underlying drop, with the option’s directional exposure doing the main work in the revaluation. Gamma and the vol move offset part of that, while the remaining gap is consistent with higher-order convexity and Taylor truncation rather than a separate catalyst. There is no named news backdrop in the run, and the observation lock means the tape should be treated as a model reprice story, not a headline-driven one. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The dominant Greek is clear, but the attribution coverage is limited and the residual is large relative to the modeled move. Vega narrative is suppressed by the code and no relevant headlines were retrieved, so the data support a coarse delta-led diagnosis rather than a finer catalyst explanation.

---

## 2. Observation Lock

* **As-of**: `2026-09-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 23.1%)
* **IV move**: +1.60 vol pts vs noise band ±1.68 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$72.5000`
* **Model ΔP (engine)**: `-$72.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$11.9209`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$84.4209` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (116.4%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$698.9885` | +964.1% | Stock moved from $352.04 to $340.00 (-12.0400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$248.4848` | -342.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$473.1774` | -652.7% | IV moved +12.01 vol pts (26.18% → 27.78%) |
| **Theta decay (Δt · Theta)** | `-$10.7527` | +14.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$84.4209` | +116.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$72.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$84.4209` (116.4% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.36).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (Layer 3) — reference only, see Regime above
* other second-order: `+$0.2528`
* Combined: `+$0.2528` | Residual after: `-$0.9778`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1075`
* **spot**: `-$4.5438`
* **vol**: `+$3.9273`
* **rate**: `+$0.0021`
* Step sum: `-$0.7219` | Model ΔP: `-$0.7250` | Audit residual: `-$0.0031`

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
* Reconcile the move with a full-surface reprice and delta hedge review, since the second-order Taylor view leaves a meaningful residual.
* No Layer B catalyst to action here; the run does not supply a borrow, squeeze, or IV-crush mechanism and the absence of headlines should be respected.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.29 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-09-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$132.5000` (+809.2%)
* **Model ΔP**: `+$132.5000`
* **Primary drivers**: **Delta PnL** (46%) and **Vega PnL** (42%) and **Gamma PnL** (6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model revaluation was driven primarily by the downside spot move in the underlying, with gamma reinforcing the move and theta a smaller offset. The vol input also moved, but that narrative is suppressed here because observation is unreliable and the run is explicitly locked to the quantified reprice rather than a catalyst story. The residual is sizable enough to point to higher-order convexity and truncation effects in the Taylor view, not a separate event-based explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is limited by the observation lock, low attribution coverage, and the large residual share relative to the modeled move. The dominant factor is still clear from the blotter, but the surface diagnostics and mark limitations mean the Greek decomposition should be treated as a reference view rather than a fully complete explanation.

---

## 2. Observation Lock

* **As-of**: `2026-09-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 10.2%)
* **IV move**: +0.40 vol pts vs noise band ±2.46 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$132.5000`
* **Model ΔP (engine)**: `+$132.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$89.9850`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$42.5150` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (32.1%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$556.5387` | +420.0% | Stock moved from $352.04 to $340.00 (-12.0400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$67.3263` | +50.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$507.6124` | -383.1% | IV moved -12.50 vol pts (28.33% → 28.72%) |
| **Theta decay (Δt · Theta)** | `-$26.2676` | -19.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$42.5150` | +32.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$132.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$42.5150` (32.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.1274`
* Combined: `-$0.1274` | Residual after: `+$1.4524`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2628`
* **spot**: `+$6.2661`
* **vol**: `-$4.6779`
* **rate**: `-$0.0034`
* Step sum: `+$1.3220` | Model ΔP: `+$1.3250` | Audit residual: `+$0.0030`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$12.0400` vs next cash dividend `+$1.5000` (gap `-$10.5400`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$17.7000` vs `+$16.9539` (gap `+$0.7461`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.1356` — material
* **Dividend PV effect** (European, same divs − no divs): `+$0.6100`
* **Dividend coverage** (dividend / time value): `0.19` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$5.0761`
* **Residual (Taylor ε)**: `+$0.4251`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Reconcile the move using the full revaluation path and not the first-order delta approximation alone; the residual suggests truncation and higher-order effects matter.
* No catalyst layer is available from the digest, so avoid forcing a borrow, squeeze, or IV-crush interpretation without relevant headlines.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.19 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-09-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$80.0000` (-2213.0%)
* **Model ΔP**: `-$80.0000`
* **Primary drivers**: **Vega PnL** (87%) and **Theta decay** (9%).
* **Verdict**: The blotter says the move was driven mainly by the options revaluation to a higher implied-volatility level, with spot essentially flat and delta/gamma contributing little. The residual is small, so the Taylor picture is internally consistent and the run is mostly a clean volatility-driven repricing rather than a spot-led move. Headline tape is only background here: it frames a broader index risk tone, but the digest found no direct SPY-specific catalyst to replace the modeled driver.
* **Confidence**: **Medium** — Observation quality is reliable, attribution coverage is high, and the residual band is low, which supports the factor read. Confidence stays medium because the headline set is broad market context rather than a direct SPY catalyst, so there is no strong Layer B confirmation beyond the tape tone.

---

## 2. Observation Lock

* **As-of**: `2026-09-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.7%)
* **IV move**: +0.19 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-09-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$80.0000`
* **Model ΔP (engine)**: `-$80.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$77.6302`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$2.3699` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$1.4823` | +1.9% | Stock moved from $773.50 to $773.38 (-0.1200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.0026` | +0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$85.3001` | +106.6% | IV moved +1.35 vol pts (17.73% → 17.92%) |
| **Theta decay (Δt · Theta)** | `+$9.1549` | -11.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$2.3699` | +3.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$80.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$2.3699` (3.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0438`
* Combined: `+$0.0438` | Residual after: `+$0.7562`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction / implied volatility move**._

_Intel note: The set is mostly broad S&P 500/index or peer-market commentary rather than direct SPY issuer news. I kept the index-level and market-tape items as background because they can frame SPY, but none of the headlines contains a direct relevant SPY catalyst._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **Netflix Is Down 42% in a Year and the Investor Who Exited in June Just Bought Back In** _(Source: 24/7 Wall St.)_
   Mentions NFLX as part of a market-moving stock-specific story, but it is not about SPY itself.
2. **Steve Weiss Dumped an Energy Stock That Tripled the S&P 500 Over a Decade** _(Source: 24/7 Wall St.)_
   Refers to the S&P 500 in a comparative investment piece, with no direct SPY-specific issuer event.
3. **S&P 500, Dow, Nasdaq Drop As Yields Spike Amid Calls For More Rate Hikes — AMZN, GOOGL, NFLX, SPCX, RKLB In Focus** _(Source: Stocktwits)_
   Broad market/sector tape on the S&P 500 and rates, which can affect SPY indirectly.
4. **S&P 500: Ready For A Melt Up (Technical Analysis) (SP500) - Seeking Alpha** _(Source: Seeking Alpha)_
   Index-level technical commentary on the S&P 500 rather than a specific SPY issuer catalyst.
5. **Micron Fell For 3 Months: Now One Wall Street Pro Says 110% Are About to Materialize - Yahoo Finance** _(Source: Yahoo Finance)_
   Single-name Micron coverage; at most a semiconductor peer signal for the broader tape.

---

## 7. Risk Watchlist

* Recheck the full surface reprice and vol mark path first, since the move was primarily a volatility revaluation with only minor spot impact.
* Use the broader rate/yield tape as context only; there is no direct SPY catalyst in the kept headlines, so no borrow, squeeze, or other microstructure mechanism should be inferred.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-09-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$221.5000` (-2560.7%)
* **Model ΔP**: `-$221.5000`
* **Primary drivers**: **Vega PnL** (90%) and **Theta decay** (6%).
* **Verdict**: The move was led by the model’s vega line: the option lost value as implied volatility eased, while spot barely changed and gamma impact was negligible. Theta was a smaller secondary drag, and the residual stayed modest, so the revaluation is mostly a clean volatility reset rather than a spot-led move. For SPY, the broader market-tape headlines about equities slipping alongside rising yields are consistent background for softer implied volatility, but they do not introduce a separate mechanism beyond the modeled vega move.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is high and the observation is reliable, but the move is still a one-day model revaluation with a small residual and no relevant named catalyst mechanism. The news set is broad market context rather than SPY-specific control-structure news, so it supports the tape but does not materially sharpen the causal story. The American-versus-European gap is negligible, so early exercise is not a factor.

---

## 2. Observation Lock

* **As-of**: `2026-09-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.5%)
* **IV move**: -0.43 vol pts vs noise band ±0.01 pts (exceeds noise band)
* **Prior observation**: `2026-09-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$221.5000`
* **Model ΔP (engine)**: `-$221.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$227.5589`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$6.0589` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$4.0635` | +1.8% | Stock moved from $773.50 to $773.38 (-0.1200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0067` | -0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$209.1404` | +94.4% | IV moved -1.84 vol pts (13.81% → 13.38%) |
| **Theta decay (Δt · Theta)** | `-$14.3617` | +6.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$6.0589` | -2.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$221.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$6.0589` (2.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0252`
* Combined: `+$0.0252` | Residual after: `-$2.2402`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: The items retained are broad S&P 500 / market-tape context for SPY rather than issuer-specific news. No relevant headlines contained one of the allowed mechanism triggers._
_Intel triage discarded 4 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **S&P 500, Dow, Nasdaq Drop As Yields Spike Amid Calls For More Rate Hikes — AMZN, GOOGL, NFLX, SPCX, RKLB In Focus** _(Source: Stocktwits)_
   Market-wide U.S. equity indices were lower as yields rose and rate-hike calls increased; this is broad tape context rather than SPY-specific issuer news.
2. **S&P 500: Ready For A Melt Up (Technical Analysis) (SP500) - Seeking Alpha** _(Source: Seeking Alpha)_
   A technical analysis piece discussing the S&P 500 index outlook, which is relevant as broad index context for SPY.

---

## 7. Risk Watchlist

* Reconcile the option through a full-surface reprice and treat spot as a minor contributor; the Greek breakdown is dominated by volatility sensitivity, not directional delta.
* Use the broad market-tape headlines as context for implied-volatility softening, but do not force a stock-specific catalyst or a microstructure story here.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-09-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$24.5000` (-2848.3%)
* **Model ΔP**: `-$106.0546`
* **Primary drivers**: **Delta PnL** (74%) and **Vega PnL** (19%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move was driven first by the underlying selloff, with the call’s positive delta doing most of the work in the model revaluation. A smaller implied-vol decline and modest residual drag added to the loss, but the tape does not support a separate catalyst story beyond the price move and surface repricing. Because observation quality was weak and the diagnostic tags suppress a Vega narrative, the safest read is a spot-led revaluation with some higher-order truncation left in the remainder. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation quality is flagged as unreliable, the model fit has limitations, and the run itself marks a terminal unexplained break for escalation. There are no retrieved headlines to anchor a Layer B catalyst, and the early-exercise premium is not the main issue here; the dominant explanation remains the modeled spot move. The residual is small relative to the model change, so truncation is secondary rather than the headline explanation.

---

## 2. Observation Lock

* **As-of**: `2026-09-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 19.4%)
* **IV move**: -3.37 vol pts vs noise band ±3.81 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$24.5000`
* **Model ΔP (engine)**: `-$106.0546`
* **Model vs Mark gap**: `-$130.5546` (+123.1% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$104.8112`

* **Method residual (ε_method)**: `-$1.2434` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$130.5546` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.2%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$85.6220` | +80.7% | Stock moved from $47.68 to $46.45 (-1.2300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$5.0762` | -4.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$21.7700` | +20.5% | IV moved -3.37 vol pts (32.13% → 28.76%) |
| **Theta decay (Δt · Theta)** | `-$2.4954` | +2.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.2434` | +1.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$106.0546** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.2434` (1.2% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0206`
* Combined: `-$0.0206` | Residual after: `-$1.0400`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0249`
* **spot**: `-$0.8039`
* **vol**: `-$0.2316`
* **rate**: `+$0.0008`
* Step sum: `-$1.0597` | Model ΔP: `-$1.0605` | Audit residual: `-$0.0008`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$1.2300` vs next cash dividend `+$0.7080` (gap `-$0.5220`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$2.6629` vs `+$2.7817` (gap `-$0.1188`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0307` — material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1496`
* **Dividend coverage** (dividend / time value): `0.58` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$0.2177`
* **Residual (Taylor ε)**: `-$0.0124`
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
* Reconcile the call’s exposure to the underlying move first; the Greek-based attribution is dominated by delta with only minor second-order remainder.
* No headline-supported catalyst is available here; keep the focus on model revaluation and note the unresolved break for follow-up rather than forcing an event narrative.
* **Assignment watch**: ex-div `2026-10-09` — Dividend coverage 0.58 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-09-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$1.0000` (-1818.2%)
* **Model ΔP**: `-$1.0000`
* **Primary drivers**: **Vega PnL** (73%) and **Delta PnL** (17%) and **Theta decay** (8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by a vega-driven repricing: the option was marked down as implied volatility eased while spot only moved modestly and delta/gamma were secondary. The Taylor residual is small, which is consistent with the move being captured mainly by the modeled volatility revaluation rather than by truncation or a boundary effect. Layer B is empty here, so there is no headline catalyst to add beyond the model story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is tempered by the observation lock and the note that the suppressed vega narrative should not be overstated from news, even though the market inputs clearly show a volatility-led move. Residuals are low and attribution coverage is high, but there are no retrieved headlines to anchor a catalyst story.

---

## 2. Observation Lock

* **As-of**: `2026-09-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 66.7%)
* **IV move**: +0.00 vol pts vs noise band ±7.46 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$1.0000`
* **Model ΔP (engine)**: `-$1.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$1.0363`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0363` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.6%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.2667` | +16.5% | Stock moved from $2.09 to $2.11 (+0.0200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0043` | +0.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$1.1825` | +73.2% | IV moved -5.38 vol pts (96.88% → 96.88%) |
| **Theta decay (Δt · Theta)** | `-$0.1249` | +7.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0363` | +2.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$1.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0363` (3.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0002`
* Combined: `+$0.0002` | Residual after: `-$0.0102`

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
* Reprice the position on the updated volatility level and confirm the vega mark against the chain-based prior close.
* No named catalyst is available from the digest; keep the diagnosis anchored to the implied-vol move and do not infer borrow or squeeze dynamics.

---


## Skew proxy (Task C3.3, SPY risk reversal)

* skew_proxy(t) = +0.0454 | level_proxy(t) = 0.1565
* Δskew = +0.0062 | Δlevel = -0.0012
* Put 715 delta=-0.1379 | Call 795 delta=0.3070
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
