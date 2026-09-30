# Live book run — 2026-09-29

Run `2026-09-29-1790730904`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=10`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-09-29` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$246.0000`
* **Total Model PnL**: `-$246.0000`
* **Aggregate model vs mark gap**: `+$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `-$592.5000` |
| 2 | `AAPL 350C 2026-11-20` | `+$310.0000` |
| 3 | `JPM 350P 2026-10-23` | `+$167.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$212.7307` |
| Gamma | `+$79.2813` |
| Vega | `-$79.5978` |
| Theta | `-$41.1824` |
| Residual | `+$8.2297` |

### Notable underlyings

* **AAPL**: `-$282.5000` aggregate option PnL
* **JPM**: `+$107.5000` aggregate option PnL
* **VZ**: `-$55.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-09-29` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$592.5000` (-2654.0%)
* **Model ΔP**: `-$592.5000`
* **Primary drivers**: **Vega PnL** (63%) and **Delta PnL** (30%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model move is dominated by the option’s sensitivity to the lower implied volatility, while the smaller spot decline and theta decay played supporting roles. The residual is modest, so the Taylor breakdown is broadly consistent with the full revaluation; however, the observation lock means the quote quality should be treated cautiously and the Vega story should be kept at a coarse level. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — The code flags the vega component as the dominant modeled driver, but observation_reliable is false and suppress_vega_narrative is true, so the vol explanation should not be overstated. There are no relevant headlines to anchor a catalyst layer, and the residual is limited, which supports the model revaluation without requiring a separate event explanation.

---

## 2. Observation Lock

* **As-of**: `2026-09-29` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.7%)
* **IV move**: -0.45 vol pts vs noise band ±0.96 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-28`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$592.5000`
* **Model ΔP (engine)**: `-$592.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$621.3046`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$28.8046` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$199.5513` | +33.7% | Stock moved from $341.07 to $338.40 (-2.6700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$3.9037` | -0.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$414.2346` | +69.9% | IV moved -9.97 vol pts (29.67% → 29.22%) |
| **Theta decay (Δt · Theta)** | `-$11.4225` | +1.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$28.8046` | -4.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$592.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$28.8046` (4.9% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0310`
* Combined: `+$0.0310` | Residual after: `-$5.9560`

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
* Recheck the full-surface repricing against the prior close Greeks if the mark quality improves, since the move is mostly explained by the vol input change.
* No catalyst layer is available from the digest, so do not force a borrow, squeeze, or IV-crush narrative without fresh relevant headlines.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.09 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-09-29` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$310.0000` (+3573.5%)
* **Model ΔP**: `+$310.0000`
* **Primary drivers**: **Vega PnL** (59%) and **Delta PnL** (33%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by the model’s vol reprice: the option lost value as implied volatility eased alongside a softer underlying. Spot moved in a relatively modest way, so delta helped but did not set the tone; the move is mainly a volatility-led revaluation inside the FDM engine. The residual is small, consistent with normal second-order effects rather than a separate story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — The blotter’s driver is clear, but observation reliability is flagged as false and the Vega narrative is suppressed by the code, so the diagnosis should stay coarse. There are no relevant headlines or microstructure tags to add a Layer B mechanism, and the residual is low, which limits the need for a more elaborate explanation.

---

## 2. Observation Lock

* **As-of**: `2026-09-29` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.5%)
* **IV move**: +0.13 vol pts vs noise band ±0.26 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-28`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$310.0000`
* **Model ΔP (engine)**: `+$310.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$320.6137`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$10.6137` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$112.7768` | +36.4% | Stock moved from $341.07 to $338.40 (-2.6700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$4.7222` | -1.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$200.0950` | +64.5% | IV moved -3.93 vol pts (26.45% → 26.58%) |
| **Theta decay (Δt · Theta)** | `+$12.4641` | +4.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$10.6137` | -3.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$310.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$10.6137` (3.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0376`
* Combined: `+$0.0376` | Residual after: `-$3.1376`

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
* Reconcile the move with a full-surface repricing rather than a simple spot-only attribution, since the option behaved primarily through vol revaluation and second-order terms.
* No catalyst overlay is supported by the blotter, so avoid forcing an IV-crush, borrow, or squeeze explanation absent relevant headlines.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.05 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-09-29` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$60.0000` (-1454.5%)
* **Model ΔP**: `-$60.0000`
* **Primary drivers**: **Delta PnL** (47%) and **Vega PnL** (35%) and **Gamma PnL** (9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is explained first by the modeled delta exposure reacting to the downside spot move, with gamma partly offsetting and theta adding a smaller carry drag. The residual is meaningful relative to the model move, so the close-to-close revaluation should be read as a truncation-and-path-risk diagnosis rather than a pure one-greek story. There are no retrieved headlines or named microstructure tags, so no separate catalyst layer can be asserted from the tape. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is internally consistent with the blotter, but observation reliability is false and the residual band is high, which limits precision. Vega narrative is suppressed by the code, and there are no retrieved headlines or independent mechanisms to support a second-layer catalyst explanation.

---

## 2. Observation Lock

* **As-of**: `2026-09-29` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 15.6%)
* **IV move**: +0.09 vol pts vs noise band ±0.96 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-28`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$60.0000`
* **Model ΔP (engine)**: `-$60.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$31.3602`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$28.6398` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (47.7%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$227.0161` | +378.4% | Stock moved from $343.06 to $336.59 (-6.4700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$43.3944` | -72.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$167.1382` | -278.6% | IV moved +5.04 vol pts (26.96% → 27.05%) |
| **Theta decay (Δt · Theta)** | `-$14.8766` | +24.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$28.6398` | +47.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$60.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$28.6398` (47.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.1081`
* Combined: `-$0.1081` | Residual after: `-$0.4919`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1487`
* **spot**: `-$1.8250`
* **vol**: `+$1.3739`
* **rate**: `+$0.0005`
* Step sum: `-$0.5994` | Model ΔP: `-$0.6000` | Audit residual: `-$0.0006`

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
* Recheck the full revaluation path because the residual is large enough that higher-order convexity and path effects matter alongside the delta move.
* No named catalyst layer is available from the digest, so do not force an IV, borrow, or liquidity narrative without new evidence.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.43 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-09-29` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$167.5000` (+943.7%)
* **Model ΔP**: `+$167.5000`
* **Primary drivers**: **Delta PnL** (55%) and **Vega PnL** (34%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model move is led by downside spot action, which is the dominant Taylor factor and the main source of the revaluation. The smaller residual is consistent with higher-order convexity and truncation effects in a fast one-day move, while the observed IV slip and decay are secondary in the run. There is no named news catalyst in the digest, so the tape reads as a mechanically driven repricing rather than a headline event. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The blotter flags the dominant driver clearly, but observation is not reliable and the residual band is high, so the decomposition should be read as approximate. Vega narrative is suppressed and there are no retrieved headlines, which limits any catalyst-specific explanation beyond the model move. The American-versus-European premium exists, but it is not an early-exercise finding because dividend coverage does not support that interpretation.

---

## 2. Observation Lock

* **As-of**: `2026-09-29` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 8.0%)
* **IV move**: -0.12 vol pts vs noise band ±2.56 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-28`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$167.5000`
* **Model ΔP (engine)**: `+$167.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$139.5434`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$27.9566` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (16.7%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$369.6521` | +220.7% | Stock moved from $343.06 to $336.59 (-6.4700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$24.7090` | +14.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$229.8947` | -137.3% | IV moved -6.55 vol pts (31.86% → 31.74%) |
| **Theta decay (Δt · Theta)** | `-$24.9230` | -14.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$27.9566` | +16.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$167.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$27.9566` (16.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.1511`
* Combined: `+$0.1511` | Residual after: `+$1.5239`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2492`
* **spot**: `+$3.9631`
* **vol**: `-$2.0389`
* **rate**: `-$0.0010`
* Step sum: `+$1.6741` | Model ΔP: `+$1.6750` | Audit residual: `+$0.0009`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$6.4700` vs next cash dividend `+$1.5000` (gap `-$4.9700`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$19.4250` vs `+$18.5596` (gap `+$0.8654`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.1340` — material
* **Dividend PV effect** (European, same divs − no divs): `+$0.7309`
* **Dividend coverage** (dividend / time value): `0.25` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$2.2989`
* **Residual (Taylor ε)**: `+$0.2796`
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
* Reconcile the move with a full-surface repricing and allow for convexity / truncation effects rather than reading the Taylor split too literally.
* Watch the IV and decay components as background to the spot-led revaluation; no catalyst-specific mechanism is supported by the digest.
* Dividend carry remains inside the model, but the setup is not an early-exercise case.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.25 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-09-29` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$8.5000` (+195.2%)
* **Model ΔP**: `+$8.5000`
* **Primary drivers**: **Delta PnL** (44%) and **Vega PnL** (43%) and **Theta decay** (6%).
* **Verdict**: The run is explained primarily by the put’s delta exposure to the lower SPY print, with gamma and theta acting as secondary supports in the Taylor view. The residual is sizable relative to the model move, so the close-to-close decomposition should be treated as a reference and the full revaluation remains the cleaner read. No relevant headline catalyst was retrieved, so there is no Layer B event to overlay.
* **Confidence**: **Medium** — Observation quality is reliable and the engine output is calibrated, but attribution coverage is low and the residual is high, so the Taylor breakdown is only a partial explanation. There are no relevant headlines or microstructure tags to anchor a catalyst layer, and the critic did not require one.

---

## 2. Observation Lock

* **As-of**: `2026-09-29` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.5%)
* **IV move**: -0.27 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-09-28`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$8.5000`
* **Model ΔP (engine)**: `+$8.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$3.8135`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$4.6865` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (55.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$80.3545` | -945.3% | Stock moved from $771.35 to $765.61 (-5.7400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$6.2264` | -73.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$78.8517` | +927.7% | IV moved -1.21 vol pts (18.18% → 17.90%) |
| **Theta decay (Δt · Theta)** | `+$11.5426` | +135.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$4.6865` | +55.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$8.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$4.6865` (55.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0497`
* Combined: `-$0.0497` | Residual after: `-$0.0353`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1155`
* **spot**: `+$0.8574`
* **vol**: `-$0.8269`
* **rate**: `-$0.0012`
* Step sum: `-$0.0862` | Model ΔP: `-$0.0850` | Audit residual: `+$0.0012`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Reconcile the move with a full-surface reprice and delta rehedge rather than leaning on the second-order Taylor split.
* No catalyst layer is available from the digest, so do not force an IV, borrow, or squeeze explanation without new evidence.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-09-29` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$23.5000` (-443.8%)
* **Model ΔP**: `-$23.5000`
* **Primary drivers**: **Delta PnL** (46%) and **Vega PnL** (42%).
* **Verdict**: The run is dominated by the model’s delta exposure: the underlying moved lower, and that was the main source of the option’s decline. Gamma and vega partly offset the move, but the remaining gap is consistent with higher-order Taylor truncation rather than a separate news catalyst. With no relevant headlines retrieved, the tape is explained by the full revaluation and the option’s path dependence, not by a distinct event.
* **Confidence**: **Medium** — Confidence is moderate because the attribution coverage is low and the residual share is high, so second-order and higher-order effects matter alongside delta. Market observation is reliable, but there are no relevant headlines to anchor a Layer B catalyst, and the run does not support inventing one.

---

## 2. Observation Lock

* **As-of**: `2026-09-29` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.8%)
* **IV move**: +0.24 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-09-28`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$23.5000`
* **Model ΔP (engine)**: `-$23.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$9.6999`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$13.8001` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (58.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$157.4747` | +670.1% | Stock moved from $771.35 to $765.61 (-5.7400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$17.1278` | -72.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$142.4561` | -606.2% | IV moved +1.46 vol pts (13.37% → 13.61%) |
| **Theta decay (Δt · Theta)** | `-$11.8092` | +50.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$13.8001` | +58.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$23.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$13.8001` (58.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0726`
* Combined: `-$0.0726` | Residual after: `-$0.1624`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1180`
* **spot**: `-$1.3928`
* **vol**: `+$1.2761`
* **rate**: `+$0.0021`
* Step sum: `-$0.2326` | Model ΔP: `-$0.2350` | Audit residual: `-$0.0024`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Recheck the full-surface revaluation and delta hedge after the spot move, since the Taylor buckets leave a meaningful residual.
* No catalyst layer was available from the digest, so do not force an IV, borrow, or squeeze narrative here.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-09-29` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$55.5000` (-2198.0%)
* **Model ΔP**: `-$55.5000`
* **Primary drivers**: **Delta PnL** (52%) and **Vega PnL** (43%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained first by the modeled delta exposure as the stock softened, with a smaller assist from theta and a modest offset from gamma. The vol line also moved against the call, but the run explicitly suppresses a Vega narrative and the absence of reliable observations means there is no headline catalyst to layer on top of the revaluation. Early exercise remains economically relevant because the dividend does not fully cover the remaining time value, so the American structure matters in the valuation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is moderate because the attribution coverage is high and the residual is small, but observation reliability is false and the surface diagnostics show limitations. There are no retrieved headlines to support a separate catalyst story, and the run is intended to be read as a model revaluation rather than a market-news narrative.

---

## 2. Observation Lock

* **As-of**: `2026-09-29` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 45.7%)
* **IV move**: +3.81 vol pts vs noise band ±9.37 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-28`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$55.5000`
* **Model ΔP (engine)**: `-$55.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$55.4624`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0376` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.1%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$29.5877` | +53.3% | Stock moved from $47.08 to $46.68 (-0.4000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.9572` | -1.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$24.7718` | +44.6% | IV moved -4.62 vol pts (23.78% → 27.59%) |
| **Theta decay (Δt · Theta)** | `-$2.0601` | +3.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0376` | +0.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$55.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0376` (0.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0053`
* Combined: `-$0.0053` | Residual after: `-$0.5497`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$0.4000` vs next cash dividend `+$0.7080` (gap `+$0.3080`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$1.9700` vs `+$2.0851` (gap `-$0.1151`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0944` — material
* **Dividend PV effect** (European, same divs − no divs): `-$0.2095`
* **Dividend coverage** (dividend / time value): `2.44` — early exercise is economically relevant
* **Vol (Taylor Vega PnL)**: `-$0.2477`
* **Residual (Taylor ε)**: `-$0.0004`
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
* Recheck the option through a full-surface reprice and delta hedge around the spot move, with attention to second-order spot convexity even though the residual is small.
* Keep the American exercise boundary and dividend timing in view because early exercise is economically relevant here; no catalyst-based overlay is supported by the feed.
* **Assignment watch**: ex-div `2026-10-09` — Dividend coverage 2.44 (dividend $0.7080 vs time value $0.2900); ex-div is 10d out, expiry 52d out — early exercise is economically relevant.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-09-29` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$0.5000` (-1428.6%)
* **Model ΔP**: `-$0.5000`
* **Primary drivers**: **Delta PnL** (51%) and **Vega PnL** (33%) and **Gamma PnL** (6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is dominated by the modeled spot sensitivity: the call was pressured as the underlying moved lower, with convexity and decay partially offsetting that damage. The residual is large enough that the revaluation should be read as a path-and-surface move rather than a clean one-factor fit, but the headline story does not add an external catalyst because none was retrieved and the observation is not reliable. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation reliability is false, attribution coverage is low, and the residual band is high. Vega narrative is suppressed by the run settings, there are no relevant headlines to anchor a catalyst, and the surface diagnostics themselves carry limitations, so the diagnosis should stay at a coarse level.

---

## 2. Observation Lock

* **As-of**: `2026-09-29` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 66.7%)
* **IV move**: -5.47 vol pts vs noise band ±7.20 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-28`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$0.5000`
* **Model ΔP (engine)**: `-$0.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$0.3731`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.1269` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (25.4%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$1.1754` | +51.1% | Stock moved from $1.98 to $1.86 (-0.1200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1378` | +6.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.7623` | +33.1% | IV moved +4.73 vol pts (104.69% → 99.22%) |
| **Theta decay (Δt · Theta)** | `-$0.0978` | +4.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.1269` | +5.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.1269` (25.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0014`
* Combined: `-$0.0014` | Residual after: `-$0.0036`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0010`
* **spot**: `-$0.0102`
* **vol**: `+$0.0062`
* **rate**: `+$0.0000`
* Step sum: `-$0.0050` | Model ΔP: `-$0.0050` | Audit residual: `-$0.0000`

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
* Recheck the full-surface reprice and delta hedge explanation before treating the Taylor split as economically precise, since the residual is elevated and the mark quality is limited.
* No catalyst layer is available from the tape, so do not infer a borrow, squeeze, or implied-volatility story without new evidence.

---


## Skew proxy (Task C3.3, SPY risk reversal)

* skew_proxy(t) = +0.0429 | level_proxy(t) = 0.1576
* Δskew = -0.0052 | Δlevel = -0.0002
* Put 715 delta=-0.1471 | Call 795 delta=0.2447
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
