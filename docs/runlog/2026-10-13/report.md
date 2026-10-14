# Live book run — 2026-10-13

Run `2026-10-13-1791940506`. 8/8 legs completed, 0 failed. `legs_narrated=7` `legs_silent=1` `llm_calls=9`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-13` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$159.5000`
* **Total Model PnL**: `-$136.1921`
* **Aggregate model vs mark gap**: `-$295.6921`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `JPM 350P 2026-10-23` | `-$95.6921` |
| 2 | `JPM 350C 2026-10-23` | `-$88.0000` |
| 3 | `VZ 45C 2026-11-20` | `+$24.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$46.7318` |
| Gamma | `+$5.0877` |
| Vega | `-$178.6605` |
| Theta | `-$49.7446` |
| Residual | `+$40.3936` |

### Notable underlyings

* **JPM**: `-$183.6921` aggregate option PnL
* **AAPL**: `+$37.5000` aggregate option PnL
* **VZ**: `+$24.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$20.0000` (+91.1%)
* **Model ΔP**: `+$20.0000`
* **Primary drivers**: **Delta PnL** (47%) and **Vega PnL** (45%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by spot-driven delta gains in the call, with gamma adding a smaller convexity boost while theta and the modest IV decline offset part of the move. The residual is sizable relative to the modeled change, so the close-to-close Taylor split should be treated as a reference view rather than a precise explanation; the full revaluation remains the headline result. There are no retrieved headlines or relevant microstructure tags, and the American-versus-European premium is not material, so there is no separate catalyst or early-exercise story to layer on top. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is limited by the low attribution coverage, the high residual band, and the observation-reliable flag being false. The coded dominant factor is clear, but the Taylor decomposition leaves a large unexplained remainder, and there are no headlines to validate an additional Layer B mechanism. The dividend does not cover remaining time value, so early exercise is not a finding.

---

## 2. Observation Lock

* **As-of**: `2026-10-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.7%)
* **IV move**: +0.09 vol pts vs noise band ±0.83 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$20.0000`
* **Model ΔP (engine)**: `+$20.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$1.9931`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$21.9931` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (110.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$284.2362` | +>1000% | Stock moved from $336.64 to $340.97 (+4.3300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$9.1853` | +45.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$275.3785` | ->1000% | IV moved -6.80 vol pts (29.52% → 29.60%) |
| **Theta decay (Δt · Theta)** | `-$20.0361` | -100.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$21.9931` | +110.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$20.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$21.9931` (110.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.1865`
* Combined: `+$0.1865` | Residual after: `+$0.0135`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2003`
* **spot**: `+$2.9377`
* **vol**: `-$2.5376`
* **rate**: `+$0.0017`
* Step sum: `+$0.2015` | Model ΔP: `+$0.2000` | Audit residual: `-$0.0015`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$4.3300` vs next cash dividend `+$0.2700` (gap `+$4.6000`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$22.1500` vs `+$22.2581` (gap `-$0.1081`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1089`
* **Dividend coverage** (dividend / time value): `0.04` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$2.7538`
* **Residual (Taylor ε)**: `+$0.2199`
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
* Treat the Taylor split as directional only, since truncation and path effects can distort the factor mix when the residual is large.
* No relevant headline mechanism was retrieved, so there is no borrow, squeeze, or IV-crush theme to monitor from the tape; continue to verify marks and surface quality.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$17.5000` (+228.8%)
* **Model ΔP**: `+$17.5000`
* **Primary drivers**: **Vega PnL** (46%) and **Delta PnL** (44%).
* **Verdict**: The modeled move is dominated by implied-volatility softening in the option’s revaluation, with spot strength and time decay acting as smaller offsets against the short call. The residual is meaningful relative to the explained move, so higher-order curvature and the model’s truncation are part of the tape, but there is no headline catalyst or microstructure tag to elevate beyond the blotter’s vega-led story.
* **Confidence**: **Medium** — Confidence is moderate because the driver is clearly identified by the quant engine, but attribution coverage is low and the residual share is elevated, which leaves room for higher-order effects and model simplification. There are no retrieved headlines or catalyst tags to support a separate Layer B explanation, and the market feed notes a deferred local-vol calibration on an American contract.

---

## 2. Observation Lock

* **As-of**: `2026-10-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.3%)
* **IV move**: -0.41 vol pts vs noise band ±0.29 pts (exceeds noise band)
* **Prior observation**: `2026-10-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$17.5000`
* **Model ΔP (engine)**: `+$17.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$11.5825`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$5.9175` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (33.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$160.4485` | -916.8% | Stock moved from $336.64 to $340.97 (+4.3300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$11.2255` | -64.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$166.5924` | +952.0% | IV moved -4.01 vol pts (26.13% → 25.71%) |
| **Theta decay (Δt · Theta)** | `+$16.6641` | +95.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$5.9175` | +33.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$17.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$5.9175` (33.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0759`
* Combined: `-$0.0759` | Residual after: `-$0.0991`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1666`
* **spot**: `+$1.7079`
* **vol**: `-$1.7164`
* **rate**: `+$0.0009`
* Step sum: `-$0.1741` | Model ΔP: `-$0.1750` | Audit residual: `-$0.0009`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Check whether the residual stays contained if the position is revalued on the full surface, since second-order curvature and truncation can matter here.
* Verify whether implied volatility continues to soften or stabilizes, because the current move is being driven primarily by vega rather than spot.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-10-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$88.0000` (->1000%)
* **Model ΔP**: `-$88.0000`
* **Primary drivers**: **Vega PnL** (65%) and **Delta PnL** (13%) and **Theta decay** (12%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by a volatility repricing in the option, with spot contributing only a smaller offset and theta adding further decay. The run should be read as a full model revaluation rather than a pure Greek story, because the residual is still meaningful and the path reprice diagnostics point to higher-order effects around the move. There are no relevant headlines or microstructure tags to add a separate catalyst layer, and the observation lock prevents forcing a news explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — The attribution is internally consistent and the confidence hint is medium, but the observation is not reliable and the suppression flag limits how far the Vega narrative should be pushed. The residual is elevated enough to suggest truncation or surface effects, so the Greek decomposition is only a reference view rather than a perfect explanation.

---

## 2. Observation Lock

* **As-of**: `2026-10-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 84.2%)
* **IV move**: -1.17 vol pts vs noise band ±2.42 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$88.0000`
* **Model ΔP (engine)**: `-$88.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$102.6064`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$14.6064` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (16.6%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$21.9844` | -25.0% | Stock moved from $332.99 to $334.30 (+1.3100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.2978` | -1.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$106.6872` | +121.2% | IV moved -7.36 vol pts (28.08% → 26.91%) |
| **Theta decay (Δt · Theta)** | `-$19.2013` | +21.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$14.6064` | -16.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$88.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$14.6064` (16.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0549`
* Combined: `+$0.0549` | Residual after: `-$0.9349`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1920`
* **spot**: `+$0.2169`
* **vol**: `-$0.9049`
* **rate**: `+$0.0001`
* Step sum: `-$0.8799` | Model ΔP: `-$0.8800` | Audit residual: `-$0.0001`

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
* Check whether the full revaluation remains stable if the surface and path assumptions are refreshed, since truncation and higher-order terms can distort the Greek split.
* With no relevant headline or microstructure tag, keep watching for any confirmed volatility repricing in the tape rather than assuming a news catalyst.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-10-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$200.0000` (-518.1%)
* **Model ΔP**: `-$95.6921`
* **Primary drivers**: **Delta PnL** (67%) and **Vega PnL** (19%) and **Theta decay** (12%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven mainly by the stock’s upward move, which hurts a put with negative delta and dominates the modeled revaluation. Theta also worked against the position, while gamma only slightly offset the move and the residual stayed small, so the Taylor view is broadly consistent with the model repricing. There is no headline catalyst to layer in, and the observation lock plus suppressed Vega narrative means the run should be read as a spot-led model move rather than a news-driven vol story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is limited by the observation lock, the failed surface and IV calibration flags, and the fact that the diagnostic tools show the Greek breakdown only as a reference while the full model revaluation remains the authoritative figure. The residual is small, but the engine also reports an unexplained break that belongs on the watchlist, and there are no retrieved headlines to independently challenge or confirm a catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-10-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 18.3%)
* **IV move**: +2.09 vol pts vs noise band ±10.78 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$200.0000`
* **Model ΔP (engine)**: `-$95.6921`
* **Model vs Mark gap**: `-$295.6921` (+309.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$94.5625`

* **Method residual (ε_method)**: `-$1.1295` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$295.6921` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.2%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$107.9048` | +112.8% | Stock moved from $332.99 to $334.30 (+1.3100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.3096` | -1.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$31.1317` | -32.5% | IV moved +2.09 vol pts (29.99% → 32.08%) |
| **Theta decay (Δt · Theta)** | `-$19.0991` | +20.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.1295` | +1.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$95.6921** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.1295` (1.2% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0329`
* Combined: `+$0.0329` | Residual after: `-$0.9898`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1910`
* **spot**: `-$1.0818`
* **vol**: `+$0.3159`
* **rate**: `-$0.0004`
* Step sum: `-$0.9574` | Model ΔP: `-$0.9569` | Audit residual: `+$0.0004`

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
* Watch whether higher-order convexity or full-surface revaluation continues to matter if the spot move broadens beyond the current regime.
* Verify the unexplained break and the surface calibration limitations before leaning on the reference Greek decomposition.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$5.5000` (+265.1%)
* **Model ΔP**: `+$5.5000`
* **Primary drivers**: **Theta decay** (68%) and **Delta PnL** (28%).
* **Verdict**: The position’s modeled one-day move is dominated by theta, with the small spot slip and minor vol uptick only partially offsetting that carry effect. The residual is low, so the Taylor view is broadly consistent with the full revaluation and there is no separate catalyst story to add from the tape. The American premium is small, so early exercise is present only as a minor model feature rather than a material driver.
* **Confidence**: **Medium** — Confidence is moderate because the data quality is good and the residual is low, but the tape lacks headlines and the move is mostly a model carry effect rather than a catalyst-driven repricing. The American-vs-European gap is small, so early exercise does not materially complicate the attribution.

---

## 2. Observation Lock

* **As-of**: `2026-10-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.0%)
* **IV move**: +0.11 vol pts vs noise band ±0.03 pts (exceeds noise band)
* **Prior observation**: `2026-10-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$5.5000`
* **Model ΔP (engine)**: `+$5.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$5.3788`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.1212` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$4.0248` | -73.2% | Stock moved from $778.57 to $778.10 (-0.4700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.0337` | -0.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.2983` | -5.4% | IV moved +0.01 vol pts (19.59% → 19.70%) |
| **Theta decay (Δt · Theta)** | `+$9.7356` | +177.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.1212` | +2.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$5.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.1212` (2.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0000`
* Combined: `+$0.0000` | Residual after: `-$0.0550`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Watch whether a larger spot move or a fuller surface reprice would disturb the theta-led attribution on the next run.
* Verify whether upcoming dividends remain too small to make early exercise economics meaningfully different from plain time decay.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$20.0000` (-318.0%)
* **Model ΔP**: `-$20.0000`
* **Primary drivers**: **Theta decay** (37%) and **Delta PnL** (36%) and **Vega PnL** (26%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-10-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.7%)
* **IV move**: -0.02 vol pts vs noise band ±0.02 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$20.0000`
* **Model ΔP (engine)**: `-$20.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$19.8807`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.1193` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$15.4572` | +77.3% | Stock moved from $778.57 to $778.10 (-0.4700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1343` | -0.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$11.3484` | -56.7% | IV moved +0.12 vol pts (12.72% → 12.70%) |
| **Theta decay (Δt · Theta)** | `-$15.9062` | +79.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.1193` | +0.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$20.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.1193` (0.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0004`
* Combined: `-$0.0004` | Residual after: `-$0.1996`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Observation unreliable — event linkage suppressed; reconcile marks before catalyst stories._


---

## 7. Risk Watchlist

* No action needed; move is within theta/carry tolerance.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$24.5000` (+>1000%)
* **Model ΔP**: `+$24.5000`
* **Primary drivers**: **Delta PnL** (69%) and **Vega PnL** (14%) and **Gamma PnL** (11%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best explained by the option’s positive delta responding to a higher underlying, with gamma providing a secondary boost as the spot move extended through the day. The residual is small, so the Taylor decomposition is broadly consistent with the model reprice rather than pointing to a separate catalyst. No headline-based mechanism is available here, and the observation lock means Layer B should stay at the model-attribution level rather than inventing a news explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by the observation lock and the lack of retrieved headlines, so there is no independent catalyst check. The residual is low and the dominant driver is clear in the blotter, but surface diagnostics were limited and the Vega narrative is suppressed by the data-quality flags.

---

## 2. Observation Lock

* **As-of**: `2026-10-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 7.7%)
* **IV move**: -0.10 vol pts vs noise band ±0.71 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$24.5000`
* **Model ΔP (engine)**: `+$24.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$25.4610`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.9610` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$28.6672` | +117.0% | Stock moved from $41.65 to $42.78 (+1.1300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$4.3948` | +17.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$5.7631` | -23.5% | IV moved -1.33 vol pts (27.78% → 27.69%) |
| **Theta decay (Δt · Theta)** | `-$1.8379` | -7.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.9610` | -3.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$24.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.9610` (3.9% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0125`
* Combined: `-$0.0125` | Residual after: `+$0.2575`

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
* Watch for Taylor truncation if spot continues to move sharply, since the option is sensitive to higher-order convexity as well as delta.
* Verify whether any later tape or quote-quality issue emerges, because the current run does not support a separate news or IV story.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-13` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (47%) and **Delta PnL** (38%) and **Theta decay** (8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is dominated by the vega line, with the spot decline and theta decay acting as smaller offsets and gamma providing only a limited cushion. Because the observation is unreliable and the Vega narrative is explicitly suppressed, the safest read is a full model revaluation driven mainly by the higher implied volatility print rather than a news-linked catalyst. The remaining gap is consistent with higher-order truncation and quote or surface noise, not a separate event-driven explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is only medium because the observation is unreliable, the attribution coverage is low, and the residual band is high. There are no headlines to anchor a catalyst, the critic did not require Layer B mechanisms, and the engine flags a terminal unexplained break, so the run should be treated as a model-based diagnostic rather than a clean tape story.

---

## 2. Observation Lock

* **As-of**: `2026-10-13` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 66.7%)
* **IV move**: +6.25 vol pts vs noise band ±6.65 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-12`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0348`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0348` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.3206` | +38.2% | Stock moved from $1.68 to $1.62 (-0.0600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0250` | +3.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.3942` | +47.0% | IV moved +5.04 vol pts (112.50% → 118.75%) |
| **Theta decay (Δt · Theta)** | `-$0.0638` | +7.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0348` | +4.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0348` (>1000% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0004`
* Combined: `-$0.0004` | Residual after: `+$0.0004`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0006`
* **spot**: `-$0.0029`
* **vol**: `+$0.0035`
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
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Check whether the full revaluation remains stable under the same engine and surface assumptions, since truncation and quote noise can distort the Greek split.
* Verify whether the implied volatility change persists in subsequent marks, but do not force a catalyst narrative without supporting headlines or microstructure evidence.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0700 | level_proxy(t) = 0.1620
* Δskew = +0.0013 | Δlevel = +0.0005
* Put 715 delta=-0.0847 | Call 795 delta=0.3219
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
