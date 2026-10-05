# Live book run — 2026-09-24

Run `2026-09-24-1790298905`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=10`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-09-24` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$28.5000`
* **Total Model PnL**: `-$28.5000`
* **Aggregate model vs mark gap**: `+$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 350C 2026-11-20` | `+$55.0000` |
| 2 | `AAPL 325C 2026-11-20` | `-$47.5000` |
| 3 | `VZ 45C 2026-11-20` | `+$39.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$260.6344` |
| Gamma | `+$19.1675` |
| Vega | `+$237.8860` |
| Theta | `-$34.9333` |
| Residual | `+$10.0143` |

### Notable underlyings

* **SPY**: `-$49.0000` aggregate option PnL
* **VZ**: `+$39.0000` aggregate option PnL
* **JPM**: `-$25.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-09-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$47.5000` (-218.9%)
* **Model ΔP**: `-$47.5000`
* **Primary drivers**: **Delta PnL** (53%) and **Vega PnL** (41%).
* **Verdict**: The modeled move was dominated by the stock’s softer close, with the option’s directional exposure doing most of the work. Vega helped offset part of that move because implied volatility eased in the run, while gamma was a small cushion and theta was a modest drag. The remaining gap sits in the model’s residual, which is consistent with higher-order effects and revaluation noise rather than a separate catalyst.
* **Confidence**: **Medium** — The blotter gives a clear dominant modeled factor and the observation is reliable, but the residual band is high and the spot move is only small, so truncation and path effects limit precision. There are no retrieved headlines or named microstructure mechanisms, and the independent catalyst brief was skipped, so Layer B does not add a specific event story.

---

## 2. Observation Lock

* **As-of**: `2026-09-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.6%)
* **IV move**: -0.64 vol pts vs noise band ±0.37 pts (exceeds noise band)
* **Prior observation**: `2026-09-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$47.5000`
* **Model ΔP (engine)**: `-$47.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$55.0312`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$7.5312` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (15.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$199.4992` | +420.0% | Stock moved from $339.75 to $337.02 (-2.7300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$4.1366` | -8.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$151.3576` | -318.6% | IV moved +3.38 vol pts (30.07% → 29.43%) |
| **Theta decay (Δt · Theta)** | `-$11.0262` | +23.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$7.5312` | -15.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$47.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$7.5312` (15.9% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0570`
* Combined: `+$0.0570` | Residual after: `-$0.5320`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1101`
* **spot**: `-$1.9548`
* **vol**: `+$1.5913`
* **rate**: `+$0.0130`
* Step sum: `-$0.4606` | Model ΔP: `-$0.4750` | Audit residual: `-$0.0144`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Reconcile the move with a fresh full-surface reprice and check whether the delta hedge needs updating after the softer spot close and the moderate volatility shift.
* No named catalyst tape is available here; keep the focus on the directional move, with the residual treated as model revaluation noise rather than event-driven flow.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-09-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$55.0000` (+614.5%)
* **Model ΔP**: `+$55.0000`
* **Primary drivers**: **Delta PnL** (57%) and **Vega PnL** (34%) and **Theta decay** (6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven primarily by the move in the underlying, with the short call benefitting from the favorable spot shift while the other Greek effects offset part of the move. The Greek decomposition is the right framing here because the residual is small and the diagnostic flags do not support a larger overlay story; with no relevant headlines and no usable catalyst digest, the run is explained by the modeled spot move rather than a news event. American early exercise is not a factor in this case, so the pricing change is a carry-and-reprice story rather than an exercise-boundary story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is moderate because the attribution is clean, but observation reliability is weak and the screen did not return usable catalyst headlines. The residual is small and the dominant driver is clearly identified by the blotter, while the Vega narrative is suppressed and the search plan notes no catalyst search under the observation lock.

---

## 2. Observation Lock

* **As-of**: `2026-09-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.6%)
* **IV move**: -0.03 vol pts vs noise band ±0.29 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$55.0000`
* **Model ΔP (engine)**: `+$55.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$52.9303`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$2.0697` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$113.3446` | +206.1% | Stock moved from $339.75 to $337.02 (-2.7300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$4.6344` | -8.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$67.8318` | -123.3% | IV moved +1.28 vol pts (26.90% → 26.86%) |
| **Theta decay (Δt · Theta)** | `+$12.0520` | +21.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$2.0697` | +3.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$55.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$2.0697` (3.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0108`
* Combined: `-$0.0108` | Residual after: `-$0.5392`

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
* Reconcile the move with the prior-close Greeks and keep the focus on spot-driven revaluation rather than higher-order effects.
* No catalyst overlay is supported by the digest, so do not force an IV or microstructure explanation from unavailable headlines.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-09-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$22.5000` (-432.7%)
* **Model ΔP**: `-$22.5000`
* **Primary drivers**: **Delta PnL** (45%) and **Vega PnL** (41%) and **Theta decay** (8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position’s modeled move was driven first by the lower underlying price, with gamma partially offsetting and theta adding carry drag in the Taylor view. The residual is meaningful, so the full revaluation should be treated as the headline explanation rather than over-reading any single Greek; with observation locked and no retrieved headlines, there is no supported catalyst layer to add. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The dominant driver is clear in the blotter, but the residual is sizable and the observation is not reliable, so the Greek breakdown is only a medium-confidence reference. Vega narrative is suppressed by the code, and there are no relevant headlines or microstructure tokens to support a separate catalyst explanation.

---

## 2. Observation Lock

* **As-of**: `2026-09-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 27.1%)
* **IV move**: -0.96 vol pts vs noise band ±1.99 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$22.5000`
* **Model ΔP (engine)**: `-$22.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$18.4568`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$4.0432` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (18.0%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$85.3174` | +379.2% | Stock moved from $340.00 to $337.53 (-2.4700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$4.8420` | -21.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$77.9145` | -346.3% | IV moved +2.18 vol pts (27.78% → 26.83%) |
| **Theta decay (Δt · Theta)** | `-$15.8959` | +70.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$4.0432` | +18.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$22.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$4.0432` (18.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0208`
* Combined: `-$0.0208` | Residual after: `-$0.2042`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1588`
* **spot**: `-$0.7952`
* **vol**: `+$0.7295`
* **rate**: `+$0.0032`
* Step sum: `-$0.2214` | Model ΔP: `-$0.2250` | Audit residual: `-$0.0036`

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
* Reconcile the move with a full-surface reprice and spot re-hedge rather than relying on the first-order delta bucket alone; the residual suggests higher-order effects matter.
* No supported catalyst layer is available from the feed, so do not infer borrow, squeeze, or IV-crush mechanics from peer tape or memory.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.30 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-09-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$2.5000` (-14.1%)
* **Model ΔP**: `-$2.5000`
* **Primary drivers**: **Vega PnL** (46%) and **Delta PnL** (45%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is dominated by the volatility repricing in the desk blotter, with spot only a secondary contributor and theta a smaller drag. Because the observation is not reliable and Vega narration is suppressed, this should be read as a model revaluation led by the IV reset rather than a higher-conviction tape read. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is capped by the observation lock, the high residual band, and the fact that the model uses a prior-close IV source rather than a fresh, fully trusted mark. There are no named headlines or independent catalyst mechanisms to anchor a stronger Layer B explanation, and the American-versus-European gap is present but not the main driver.

---

## 2. Observation Lock

* **As-of**: `2026-09-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 8.8%)
* **IV move**: +1.93 vol pts vs noise band ±2.35 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$2.5000`
* **Model ΔP (engine)**: `-$2.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$15.7853`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$13.2853` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (531.4%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$155.2592` | +44.6% | Stock moved from $340.00 to $337.53 (-2.4700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$4.0950` | +1.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$158.8797` | +45.7% | IV moved -4.34 vol pts (28.72% → 30.66%) |
| **Theta decay (Δt · Theta)** | `-$16.2597` | +4.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$13.2853` | +3.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$2.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$13.2853` (531.4% of |model|)

### Second-order Taylor (Layer 3)
* Vanna PnL: `+$0.0517` | other second-order: `+$0.0192`
* Combined: `+$0.0709` | Residual after: `-$0.0959`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1628`
* **spot**: `+$1.6016`
* **vol**: `-$1.4638`
* **rate**: `-$0.0058`
* Step sum: `-$0.0309` | Model ΔP: `-$0.0250` | Audit residual: `+$0.0059`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$2.4700` vs next cash dividend `+$1.5000` (gap `-$0.9700`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$17.6750` vs `+$16.8228` (gap `+$0.8522`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.1740` — material
* **Dividend PV effect** (European, same divs − no divs): `+$0.6778`
* **Dividend coverage** (dividend / time value): `0.29` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$1.5888`
* **Residual (Taylor ε)**: `+$0.1329`
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

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Review the full surface reprice rather than relying on the first-order Taylor split, since the residual is large relative to the modeled change.
* Treat the move as an implied volatility repricing case in the model; there is no supported borrow, squeeze, or IV-crush catalyst from the digest to add beyond the blotter overlay.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.29 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-09-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$22.0000` (-498.3%)
* **Model ΔP**: `-$22.0000`
* **Primary drivers**: **Delta PnL** (54%) and **Vega PnL** (32%) and **Theta decay** (8%).
* **Verdict**: The position was driven mainly by the adverse spot move against a short put, with gamma and theta only partly offsetting that directional impact. The run’s residual is consistent with higher-order convexity and revaluation effects around the option’s American pricing boundary, but there is no headline catalyst to layer on top of the factor story.
* **Confidence**: **Medium** — The blotter provides a clean engine-based decomposition with reliable marks and a clear dominant Taylor driver, but the residual share is still meaningful and the spot move is not large, so some path and truncation effects remain in view. No relevant headlines were retrieved, so there is no auxiliary catalyst evidence to reinforce or challenge the factor read.

---

## 2. Observation Lock

* **As-of**: `2026-09-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.6%)
* **IV move**: +0.33 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-09-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$22.0000`
* **Model ΔP (engine)**: `-$22.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$25.4384`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$3.4384` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (15.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$76.8056` | +349.1% | Stock moved from $773.38 to $767.81 (-5.5700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$5.6244` | +25.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$46.2662` | -210.3% | IV moved -0.68 vol pts (17.92% → 18.25%) |
| **Theta decay (Δt · Theta)** | `+$10.7254` | -48.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$3.4384` | -15.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$22.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$3.4384` (15.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0341`
* Combined: `-$0.0341` | Residual after: `+$0.2541`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1074`
* **spot**: `+$0.8176`
* **vol**: `-$0.4898`
* **rate**: `-$0.0068`
* Step sum: `+$0.2135` | Model ΔP: `+$0.2200` | Audit residual: `+$0.0065`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Reconcile the move with a full reprice and delta hedging first, since the directional spot shock is the dominant modeled driver and the Taylor residual is not negligible.
* No catalyst-based overlay is supported here; keep the focus on price action and the model’s American revaluation rather than inventing a news explanation.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-09-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$27.0000` (-419.6%)
* **Model ΔP**: `-$27.0000`
* **Primary drivers**: **Delta PnL** (47%) and **Vega PnL** (42%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The revaluation is dominated by the lower underlying, which hurt this call through the modeled delta channel. Gamma partly cushioned the move, while theta and the small residual reflect second-order effects and path dependence around the repriced surface. With no retrieved headlines and the observation lock in place, there is no supported catalyst layer beyond the spot-driven move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The blotter clearly identifies delta as the dominant modeled factor, but the attribution coverage is limited and the residual share is elevated, so the Greek split is only a reference view. News support is absent, and the observation is flagged unreliable, which limits how specific the diagnosis can be.

---

## 2. Observation Lock

* **As-of**: `2026-09-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.1%)
* **IV move**: +0.03 vol pts vs noise band ±0.03 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$27.0000`
* **Model ΔP (engine)**: `-$27.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$14.6686`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$12.3314` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (45.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$171.1365` | +633.8% | Stock moved from $773.38 to $767.81 (-5.5700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$16.2816` | -60.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$152.2705` | -564.0% | IV moved +1.41 vol pts (13.38% → 13.41%) |
| **Theta decay (Δt · Theta)** | `-$12.0842` | +44.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$12.3314` | +45.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$27.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$12.3314` (45.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0595`
* Combined: `-$0.0595` | Residual after: `-$0.2105`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1205`
* **spot**: `-$1.5364`
* **vol**: `+$1.3888`
* **rate**: `+$0.0128`
* Step sum: `-$0.2553` | Model ΔP: `-$0.2700` | Audit residual: `-$0.0147`

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
* Monitor the full-surface reprice and delta re-hedge because the move was primarily driven by spot.
* No catalyst overlay is supported by the digest; do not infer squeeze, borrow stress, or IV-crush from peer tape or memory.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-09-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$39.0000` (+1455.2%)
* **Model ΔP**: `+$39.0000`
* **Primary drivers**: **Vega PnL** (85%) and **Delta PnL** (10%) and **Theta decay** (5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move was driven primarily by a lower implied volatility input, with the option repricing higher as the surface reset after the spot uptick. Delta helped on the underlying drift and theta was a drag, but the vega term clearly dominated the one-day revaluation; the tiny residual suggests the Taylor view was clean. There are no relevant headlines, so the tape is explained by the model inputs rather than a news catalyst. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is moderate because observation quality is limited and there were no retrieved headlines to cross-check a catalyst. The model attribution is still strong: the vega bucket dominates, the residual is small, and the diagnostic tools support the revaluation story.

---

## 2. Observation Lock

* **As-of**: `2026-09-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 11.7%)
* **IV move**: -3.12 vol pts vs noise band ±2.61 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$39.0000`
* **Model ΔP (engine)**: `+$39.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$38.9708`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0292` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.1%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$4.3379` | +11.1% | Stock moved from $46.45 to $46.52 (+0.0700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0201` | +0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$36.9483` | +94.7% | IV moved +5.41 vol pts (28.76% → 25.64%) |
| **Theta decay (Δt · Theta)** | `-$2.3355` | -6.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0292` | +0.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$39.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0292` (0.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0034`
* Combined: `+$0.0034` | Residual after: `+$0.3866`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$0.0700` vs next cash dividend `+$0.7080` (gap `+$0.7780`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$3.0700` vs `+$3.2031` (gap `-$0.1331`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0187` — material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1519`
* **Dividend coverage** (dividend / time value): `0.46` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.3695`
* **Residual (Taylor ε)**: `+$0.0003`
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
* Reconcile the position with a full-surface reprice and verify the implied-vol reset is captured cleanly in the mark.
* For the American feature, treat this as a carry and dividend-boundary case rather than an early-exercise event; the dividend does not cover the remaining time value.
* **Assignment watch**: ex-div `2026-10-09` — Dividend coverage 0.46 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-09-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$1.0000` (-2222.2%)
* **Model ΔP**: `-$1.0000`
* **Primary drivers**: **Delta PnL** (70%) and **Vega PnL** (14%) and **Theta decay** (9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is primarily explained by the option’s directional sensitivity to the lower underlying price, with gamma partly cushioning the downside and theta adding a smaller decay effect. Vega is present in the decomposition, but the data quality flags and suppression note mean the run should be treated as a model revaluation rather than a firm implied-vol story; there are no headlines to supply a separate catalyst layer. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The blotter gives a clear dominant Taylor driver and the residual is small, but observation reliability is flagged false and the headline set is empty. Vega narrative is also explicitly suppressed, so confidence is limited to the model-based factor story.

---

## 2. Observation Lock

* **As-of**: `2026-09-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 28.6%)
* **IV move**: +0.00 vol pts vs noise band ±2.93 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$1.0000`
* **Model ΔP (engine)**: `-$1.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$1.0351`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0351` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.5%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.8175` | +69.7% | Stock moved from $2.11 to $2.04 (-0.0700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0511` | +4.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.1596` | +13.6% | IV moved -0.79 vol pts (96.88% → 96.88%) |
| **Theta decay (Δt · Theta)** | `-$0.1092` | +9.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0351` | +3.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$1.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0351` (3.5% of |model|)

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

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Monitor whether the move is mostly spot-led or whether a fresh full-surface reprice changes the mix versus the previous close.
* No headline-based catalyst layer is available here; do not force an IV or microstructure explanation without new evidence.

---


## Skew proxy (Task C3.3, SPY risk reversal)

* skew_proxy(t) = +0.0484 | level_proxy(t) = 0.1583
* Δskew = +0.0030 | Δlevel = +0.0018
* Put 715 delta=-0.1496 | Call 795 delta=0.2756
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
