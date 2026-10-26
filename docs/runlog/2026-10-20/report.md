# Live book run — 2026-10-20

Run `2026-10-20-1792545306`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=11`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-20` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$251.0000`
* **Total Model PnL**: `+$282.9493`
* **Aggregate model vs mark gap**: `+$533.9493`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `JPM 350P 2026-10-23` | `+$466.4493` |
| 2 | `AAPL 325C 2026-11-20` | `-$225.0000` |
| 3 | `AAPL 350C 2026-11-20` | `+$170.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$435.9207` |
| Gamma | `+$90.6063` |
| Vega | `+$138.9942` |
| Theta | `-$223.9385` |
| Residual | `-$158.6334` |

### Notable underlyings

* **JPM**: `+$427.9493` aggregate option PnL
* **SPY**: `-$86.0000` aggregate option PnL
* **AAPL**: `-$55.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-20` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$225.0000` (-980.4%)
* **Model ΔP**: `-$225.0000`
* **Primary drivers**: **Vega PnL** (51%) and **Theta decay** (26%) and **Delta PnL** (16%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by a drop in implied volatility, with theta also contributing and delta a smaller offset from the mild spot drift. The residual is consistent with higher-order effects and model truncation around the full revaluation, so the Greek split should be read as a reference view rather than a complete explanation. There is no retrieved headline catalyst, so the tape reads as a model-driven repricing rather than a news-led event. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — The dominant driver is clear in the blotter, but observation is unreliable and the Vega narrative is explicitly suppressed by the diagnostics. There are no retrieved headlines, no named microstructure mechanisms, and the residual is only medium-sized, so the attribution should stay at a coarse level.

---

## 2. Observation Lock

* **As-of**: `2026-10-20` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.3%)
* **IV move**: +0.77 vol pts vs noise band ±2.19 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$225.0000`
* **Model ΔP (engine)**: `-$225.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$242.8302`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$17.8302` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (7.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$40.7546` | +18.1% | Stock moved from $343.46 to $342.94 (-0.5200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1473` | -0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$133.3994` | +59.3% | IV moved -4.22 vol pts (32.14% → 32.90%) |
| **Theta decay (Δt · Theta)** | `-$68.8234` | +30.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$17.8302` | -7.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$225.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$17.8302` (7.9% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0204`
* Combined: `+$0.0204` | Residual after: `-$2.2704`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.6978`
* **spot**: `-$0.4131`
* **vol**: `-$1.1392`
* **rate**: `-$0.0018`
* Step sum: `-$2.2519` | Model ΔP: `-$2.2500` | Audit residual: `+$0.0019`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$0.5200` vs next cash dividend `+$0.2700` (gap `-$0.2500`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$20.7000` vs `+$20.8460` (gap `-$0.1460`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1467`
* **Dividend coverage** (dividend / time value): `0.10` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$1.3340`
* **Residual (Taylor ε)**: `+$0.1783`
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
* Watch whether the full revaluation continues to diverge from the Taylor split, since higher-order effects can distort the modeled attribution when spot and vol both move.
* Verify whether implied volatility remains the main input behind the repricing, given the lack of headline support and the observed observation-quality limits.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.10 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-20` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$170.0000` (+>1000%)
* **Model ΔP**: `+$170.0000`
* **Primary drivers**: **Theta decay** (44%) and **Vega PnL** (41%) and **Delta PnL** (12%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by modeled time decay, with smaller contributions from the option’s exposure to the spot drift and the volatility move. The residual is limited, so the Taylor decomposition is broadly consistent with the model revaluation. There is no separate named news catalyst here, and the observation lock means the diagnostic should stay at the factor level rather than forcing a tape story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is internally consistent and the residual is low, but observation reliability is flagged false and the Vega narrative is suppressed, so confidence is limited to the modeled decomposition rather than a full market read. No relevant headlines were retrieved, and the catalyst brief was explicitly skipped under the observation lock.

---

## 2. Observation Lock

* **As-of**: `2026-10-20` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.2%)
* **IV move**: +0.01 vol pts vs noise band ±0.26 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$170.0000`
* **Model ΔP (engine)**: `+$170.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$174.8403`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$4.8403` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$22.4891` | +13.2% | Stock moved from $343.46 to $342.94 (-0.5200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.2059` | -0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$73.7109` | +43.4% | IV moved -1.74 vol pts (26.80% → 26.81%) |
| **Theta decay (Δt · Theta)** | `+$78.8463` | +46.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$4.8403` | -2.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$170.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$4.8403` (2.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0030`
* Combined: `+$0.0030` | Residual after: `-$1.7030`

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
* Higher-order truncation is mild here, but the full engine revaluation still matters more than the second-order approximation.
* With no retrieved catalyst and observation lock in place, verify the mark quality and surface inputs before leaning on any news-based explanation.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-10-20` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$38.5000` (->1000%)
* **Model ΔP**: `-$38.5000`
* **Primary drivers**: **Vega PnL** (31%) and **Delta PnL** (21%) and **Theta decay** (15%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by a revaluation of implied volatility, with spot weakness and time decay also weighing on the option while gamma partly offsets the move. Because the observation is not reliable and the residual is large, the Greek decomposition should be treated as a reference view rather than a complete explanation of the full reprice. There are no retrieved headlines or microstructure tokens to support a separate catalyst layer, so no additional news-based mechanism should be inferred. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The code identifies vega as the dominant modeled driver, but observation reliability is false and the residual is high, so the attribution is only moderately firm. The news layer is empty and the independent catalyst brief is skipped under an observation lock, which limits any catalyst-level certainty. The early-exercise premium is negligible, so American exercise features do not add an explanatory layer.

---

## 2. Observation Lock

* **As-of**: `2026-10-20` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 75.0%)
* **IV move**: +3.76 vol pts vs noise band ±1.65 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$38.5000`
* **Model ΔP (engine)**: `-$38.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$27.3310`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$65.8310` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (171.0%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$71.9665` | +186.9% | Stock moved from $339.72 to $333.53 (-6.1900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$45.3149` | -117.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$104.6501` | -271.8% | IV moved +10.64 vol pts (22.32% → 26.07%) |
| **Theta decay (Δt · Theta)** | `-$50.6675` | +131.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$65.8310` | +171.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$38.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$65.8310` (171.0% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.63).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (Layer 3) — reference only, see Regime above
* Vanna PnL: `-$0.6574` | other second-order: `+$0.2747`
* Combined: `-$0.3827` | Residual after: `-$0.0023`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.4200`
* **spot**: `-$0.0442`
* **vol**: `+$0.0791`
* **rate**: `-$0.0000`
* Step sum: `-$0.3851` | Model ΔP: `-$0.3850` | Audit residual: `+$0.0001`

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
* Monitor whether the full revaluation stays sensitive to higher-order convexity and truncation effects, since the residual is large relative to the modeled move.
* Verify the implied-volatility move against fresh market data, because the tape lacks retrieved headlines and the volatility reprice is the main modeled contributor.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-10-20` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$67.5000` (+>1000%)
* **Model ΔP**: `+$466.4493`
* **Primary drivers**: **Delta PnL** (45%) and **Vega PnL** (24%) and **Theta decay** (15%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best explained by the modeled delta response to a lower underlying price, with gamma and vega contributing around that core and theta partially offsetting it. The residual is sizable, so the Taylor view should be treated as an approximation rather than a full decomposition. Because observation is unreliable and the vega narrative is suppressed, there is no supported catalyst layer to attach beyond the model revaluation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because the observation is flagged unreliable, the residual share is elevated, and the standard path reprice leaves an unexplained break. The only supported story is the model’s own close-to-close revaluation; no relevant headlines were retrieved, so there is no independent catalyst evidence to strengthen or replace the factor attribution.

---

## 2. Observation Lock

* **As-of**: `2026-10-20` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 21.0%)
* **IV move**: +14.48 vol pts vs noise band ±24.32 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$67.5000`
* **Model ΔP (engine)**: `+$466.4493`
* **Model vs Mark gap**: `+$533.9493` (+114.5% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$579.7964`

* **Method residual (ε_method)**: `-$113.3471` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$533.9493` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (24.3%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$455.0042` | +97.5% | Stock moved from $339.72 to $333.53 (-6.1900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$41.0149` | +8.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$238.0657` | +51.0% | IV moved +14.48 vol pts (30.69% → 45.17%) |
| **Theta decay (Δt · Theta)** | `-$154.2884` | -33.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$113.3471` | -24.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$466.4493** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$113.3471` (24.3% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.3190`
* Combined: `-$0.3190` | Residual after: `+$4.9835`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$1.6499`
* **spot**: `+$5.6597`
* **vol**: `+$0.6549`
* **rate**: `+$0.0001`
* Step sum: `+$4.6649` | Model ΔP: `+$4.6645` | Audit residual: `-$0.0004`

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
* The attribution may still be distorted by Taylor truncation and the full path reprice, so treat the Greek breakdown as a reference rather than a complete explanation.
* Verify whether the apparent volatility move is real or a data artifact before drawing any inference about implied volatility, since the vega narrative is suppressed and the feed quality is weak.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-20` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$13.5000` (+559.0%)
* **Model ΔP**: `+$13.5000`
* **Primary drivers**: **Vega PnL** (45%) and **Theta decay** (29%) and **Delta PnL** (19%).
* **Verdict**: The blotter’s dominant modeled driver is vega, so the option’s revaluation is mainly explained by the change in implied volatility rather than the small spot move. The Taylor residual is sizable, which is consistent with higher-order effects and the limits of a short-horizon Greek expansion. Layer B is supported by the relevant earnings-style background headline: the tape is consistent with an implied volatility reset, i.e. IV crush, with the peer earnings context helping explain why option value could reprice sharply even without a large underlying move.
* **Confidence**: **Medium** — Confidence is medium because the engine tags the position with a vega-led attribution, but the residual is large enough that truncation and path effects matter. The retrieved headlines are peer-level rather than SPY-specific, so they support an implied volatility narrative only as auxiliary context, not as direct evidence of a SPY-specific catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-10-20` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.9%)
* **IV move**: +0.51 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-10-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$13.5000`
* **Model ΔP (engine)**: `+$13.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$3.6495`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$9.8505` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (73.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$36.0385` | +267.0% | Stock moved from $763.25 to $766.48 (+3.2300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$2.2753` | -16.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$84.1905` | -623.6% | IV moved +1.85 vol pts (19.76% → 20.26%) |
| **Theta decay (Δt · Theta)** | `+$54.0768` | +400.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$9.8505` | +73.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$13.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$9.8505` (73.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0126`
* Combined: `-$0.0126` | Residual after: `-$0.1224`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.5360`
* **spot**: `-$0.2905`
* **vol**: `+$0.6917`
* **rate**: `+$0.0005`
* Step sum: `-$0.1344` | Model ΔP: `-$0.1350` | Audit residual: `-$0.0006`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega / implied volatility move**._

_Intel note: The items are peer-level earnings context rather than SPY-specific news. They are kept as background because they may inform broad index sentiment, but they do not directly concern SPY or a control-structure event in the ETF._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **AMD Earnings IV Crush & Implied vs Actual Moves** _(Source: volradar.com)_
   AMD is a semiconductor peer; the headline discusses earnings-related implied/actual move dynamics for that issuer, which can serve as sector context for SPY.

_Peer / sector background (indirect context, not a required catalyst):_

2. **V Stock Before Earnings: Why Calls Lose on a ±4.0% Move** _(Source: earnings-watcher.com)_
   Visa is a large-cap index constituent; this is an earnings-focused note on a peer issuer that may be part of broader market/sector backdrop for SPY.

---

## 7. Risk Watchlist

* Watch whether the remaining residual is mostly higher-order convexity or path effects, since truncation can materially distort the Greek decomposition.
* Track whether the implied volatility reset persists, because IV crush is the named catalyst mechanism in the tape context and should remain part of the diagnosis.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-20` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$99.5000` (->1000%)
* **Model ΔP**: `-$99.5000`
* **Primary drivers**: **Vega PnL** (40%) and **Theta decay** (30%) and **Delta PnL** (27%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model revaluation is dominated by a decline in implied volatility, with the spot uptick providing a smaller offset and the second-order spot term remaining minor. The tape context is consistent with an IV crush regime, so the headline mechanism belongs in the diagnosis even though the kept headlines are broad peer/sector background rather than SPY-specific. Truncation only explains a small leftover; it does not displace the vol-led attribution. Caveats: Layer B omitted mechanisms present in headlines; residual truncation does not replace those catalysts. Gaps: Headline catalyst not used in narrative: earnings
* **Confidence**: **Medium** — Confidence is supported by reliable observations, high attribution coverage, and a low residual. The main limitation is that the available news is broad background rather than direct SPY-specific catalyst evidence, so the IV-crush link is contextual rather than issuer-specific.

---

## 2. Observation Lock

* **As-of**: `2026-10-20` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.1%)
* **IV move**: +0.28 vol pts vs noise band ±0.03 pts (exceeds noise band)
* **Prior observation**: `2026-10-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$99.5000`
* **Model ΔP (engine)**: `-$99.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$101.1143`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.6143` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$66.0381` | -66.4% | Stock moved from $763.25 to $766.48 (+3.2300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$4.3551` | -4.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$98.2165` | +98.7% | IV moved -1.44 vol pts (12.28% → 12.56%) |
| **Theta decay (Δt · Theta)** | `-$73.2911` | +73.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.6143` | -1.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$99.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.6143` (1.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0390`
* Combined: `-$0.0390` | Residual after: `-$0.9560`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: The headlines are unrelated issuer earnings-volatility items that can serve only as broad market/sector background for SPY. No SPY-specific or direct control-structure headline is present._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **AMD Earnings IV Crush & Implied vs Actual Moves** _(Source: volradar.com)_
   AMD is discussed in an earnings-volatility context, which is sector-level background rather than a SPY-specific headline.

_Peer / sector background (indirect context, not a required catalyst):_

2. **V Stock Before Earnings: Why Calls Lose on a ±4.0% Move** _(Source: earnings-watcher.com)_
   Visa is mentioned in a pre-earnings options-volatility discussion, which is only indirect background for SPY.

---

## 7. Risk Watchlist

* **Verifier reflect**: Layer B omitted mechanisms present in headlines; residual truncation does not replace those catalysts. Gaps: Headline catalyst not used in narrative: earnings
* Keep in mind that Taylor truncation can still leave a small mismatch when spot or vol shifts are not perfectly linearized; the full revaluation remains the clean reference.
* Watch whether implied volatility continues to compress or stabilize, since the kept headlines point to an IV crush regime as the relevant market context.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-20` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$4.0000` (-306.5%)
* **Model ΔP**: `-$4.0000`
* **Primary drivers**: **Vega PnL** (45%) and **Delta PnL** (37%) and **Theta decay** (11%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is primarily a model revaluation driven by the volatility input, with spot weakness and time decay offsetting part of the effect. Because the observation is unreliable and the Vega narrative is suppressed, this should be treated as a coarse attribution rather than a tightly sourced market story. There are no relevant headlines or microstructure tags to support a separate catalyst explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is only medium because the blotter flags unreliable observation, low attribution coverage, and a high residual share. The early-exercise premium is negligible, so American-style exercise is not a material explanation, and there is no retrieved catalyst evidence to anchor a more specific Layer B story.

---

## 2. Observation Lock

* **As-of**: `2026-10-20` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 8.7%)
* **IV move**: +0.61 vol pts vs noise band ±1.09 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$4.0000`
* **Model ΔP (engine)**: `-$4.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$0.1181`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$3.8819` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (97.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$30.8729` | +36.6% | Stock moved from $44.79 to $44.15 (-0.6400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$2.2546` | +2.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$37.9521` | +45.0% | IV moved +6.81 vol pts (28.98% → 29.59%) |
| **Theta decay (Δt · Theta)** | `-$9.4519` | +11.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$3.8819` | +4.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$4.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$3.8819` (97.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0034`
* Combined: `-$0.0034` | Residual after: `-$0.0366`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0976`
* **spot**: `-$0.2832`
* **vol**: `+$0.3408`
* **rate**: `-$0.0001`
* Step sum: `-$0.0401` | Model ΔP: `-$0.0400` | Audit residual: `+$0.0001`

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
* Residual size and surface diagnostics suggest higher-order convexity or pricing-path effects may be distorting the Greek decomposition.
* With no retrieved relevant headlines, avoid reading a squeeze, borrow, or IV-crush narrative into the move absent independent tape confirmation.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-20` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (50%) and **Theta decay** (40%) and **Delta PnL** (7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model move is dominated by the rise in implied volatility, with theta decay and a smaller spot-related drag offsetting part of that benefit. The residual is consistent with higher-order curvature and Taylor truncation around a small spot move in a short-dated American contract. No relevant headline catalyst was retrieved, so the run should be read as a model revaluation rather than a news-driven repricing. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is capped by unreliable observation and a low attribution coverage band, even though the code’s dominant driver is clear. The missing headline set means there is no independent catalyst confirmation, and the large residual leaves room for curvature and surface effects beyond the first-pass Greek split.

---

## 2. Observation Lock

* **As-of**: `2026-10-20` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 66.7%)
* **IV move**: +10.94 vol pts vs noise band ±8.12 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000`
* **Explained ΔP (Taylor ex-residual)**: `+$0.0280`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0280` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.0553` | +6.5% | Stock moved from $1.38 to $1.37 (-0.0100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0007` | +0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.4218` | +49.9% | IV moved +6.53 vol pts (126.56% → 137.50%) |
| **Theta decay (Δt · Theta)** | `-$0.3392` | +40.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0280` | +3.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0280` (>1000% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0002`
* Combined: `+$0.0002` | Residual after: `-$0.0002`

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
* Small spot changes can still leave the Taylor split sensitive to truncation and higher-order curvature in a short-dated option.
* With no relevant headlines retrieved, verify whether the move was primarily an implied-volatility reprice rather than a tape-specific catalyst.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0771 | level_proxy(t) = 0.1641
* Δskew = +0.0023 | Δlevel = +0.0039
* Put 715 delta=-0.1040 | Call 795 delta=0.1850
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
