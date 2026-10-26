# Live book run — 2026-10-22

Run `2026-10-22-1792719310`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=12`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-22` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$233.5000`
* **Total Model PnL**: `-$233.5000`
* **Aggregate model vs mark gap**: `+$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `+$362.5000` |
| 2 | `AAPL 350C 2026-11-20` | `-$247.5000` |
| 3 | `SPY 795C 2026-11-20` | `-$163.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$213.0646` |
| Gamma | `+$45.0202` |
| Vega | `+$55.9837` |
| Theta | `-$59.7036` |
| Residual | `-$61.7357` |

### Notable underlyings

* **SPY**: `-$284.0000` aggregate option PnL
* **JPM**: `-$138.0000` aggregate option PnL
* **AAPL**: `+$115.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$362.5000` (+>1000%)
* **Model ΔP**: `+$362.5000`
* **Primary drivers**: **Delta PnL** (80%) and **Vega PnL** (12%).
* **Verdict**: The move is primarily explained by the stock's upward reprice, with delta contributing the dominant share of the modeled option change and gamma providing a smaller convexity lift. Vega also helped because implied volatility firmed, while theta was a drag; the remaining gap is small and consistent with normal second-order and model-structure effects. No relevant headlines were retrieved, so there is no separate catalyst layer to add beyond the modeled spot and volatility move.
* **Confidence**: **Medium** — The attribution is supported by high coverage and a low residual, but the move includes a non-trivial volatility component and the diagnostic notes show surface limitations, so the story is best kept at the model level rather than over-specific. There are no relevant headlines or catalyst mechanisms to validate an external event narrative, and the American-versus-European premium is not material.

---

## 2. Observation Lock

* **As-of**: `2026-10-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.3%)
* **IV move**: +2.19 vol pts vs noise band ±1.65 pts (exceeds noise band)
* **Prior observation**: `2026-10-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$362.5000`
* **Model ΔP (engine)**: `+$362.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$366.8174`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$4.3173` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$325.2872` | +89.7% | Stock moved from $343.99 to $348.22 (+4.2300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$9.2542` | +2.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$49.9465` | +13.8% | IV moved +1.66 vol pts (32.93% → 35.12%) |
| **Theta decay (Δt · Theta)** | `-$17.6706` | -4.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$4.3173` | -1.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$362.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$4.3173` (1.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0352`
* Combined: `-$0.0352` | Residual after: `+$3.6602`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$4.2300` vs next cash dividend `+$0.2700` (gap `+$4.5000`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$27.5500` vs `+$27.6923` (gap `-$0.1423`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1433`
* **Dividend coverage** (dividend / time value): `0.06` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.4995`
* **Residual (Taylor ε)**: `-$0.0432`
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

* Monitor whether the full-surface reprice or higher-order convexity would materially alter the attribution if spot continues to move.
* Watch implied volatility and the mark quality, since the quoted vol rise contributed alongside the spot move.
* Dividend timing does not currently point to a meaningful early-exercise boundary effect.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.06 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$247.5000` (->1000%)
* **Model ΔP**: `-$247.5000`
* **Primary drivers**: **Delta PnL** (65%) and **Vega PnL** (24%) and **Theta decay** (6%).
* **Verdict**: The position was driven mainly by the spot rally, with the Taylor decomposition showing delta as the dominant modeled factor and only secondary contributions from gamma and implied volatility. The residual is negligible, so the full revaluation is well explained by the engine rather than by a large unmodeled gap. On the American side, early exercise is not a factor here; the dividend does not cover the remaining time value, so this is a carry and theta case rather than an exercise premium story.
* **Confidence**: **Medium** — Confidence is supported by a high attribution-coverage run, reliable observations, and a very small method residual. The main limitation is that there were no retrieved headlines, so there is no Layer B catalyst to tie to the tape, and the market move should be treated as a modeled spot-led reprice rather than a news-specific event.

---

## 2. Observation Lock

* **As-of**: `2026-10-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.4%)
* **IV move**: +2.03 vol pts vs noise band ±0.45 pts (exceeds noise band)
* **Prior observation**: `2026-10-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$247.5000`
* **Model ΔP (engine)**: `-$247.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$247.5871`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0872` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$184.2696` | +74.5% | Stock moved from $343.99 to $348.22 (+4.2300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$13.7976` | +5.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$67.9790` | +27.5% | IV moved +1.75 vol pts (27.06% → 29.09%) |
| **Theta decay (Δt · Theta)** | `+$18.4590` | -7.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0872` | -0.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$247.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0872` (0.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0182`
* Combined: `+$0.0182` | Residual after: `+$2.4568`

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

* Watch whether any future move is large enough to make higher-order convexity or full-surface revaluation materially different from the Taylor view.
* Verify that the dividend/exercise setup stays non-binding; with no material early-exercise premium, the American feature should remain a secondary consideration.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-10-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$0.5000` (->1000%)
* **Model ΔP**: `-$0.5000`
* **Primary drivers**: **Vega PnL** (35%) and **Theta decay** (17%) and **Delta PnL** (11%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The desk run is dominated by the unexplained residual in the Taylor decomposition, so the modeled move is best read as a full revaluation gap rather than a clean single-Greek story. The large gap is consistent with higher-order convexity and truncation effects in a very short-dated American call, where the linear and second-order buckets do not fully capture the engine move. There are no relevant headlines in the blotter, so there is no catalyst layer to add beyond the model mechanics. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is limited by the low attribution coverage, the high residual band, and the observation lock on the catalyst side. The spot move is small, the vol move is moderate, and the run reports no relevant headlines, so the decomposition should be treated as a model-price diagnostic rather than a market-news explanation.

---

## 2. Observation Lock

* **As-of**: `2026-10-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 100.0%)
* **IV move**: +7.81 vol pts vs noise band ±2.06 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$0.5000`
* **Model ΔP (engine)**: `-$0.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$4.5752`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$5.0752` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$1.5569` | +10.7% | Stock moved from $335.19 to $336.54 (+1.3500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.4340` | +3.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$5.0279` | +34.6% | IV moved +6.72 vol pts (26.17% → 33.99%) |
| **Theta decay (Δt · Theta)** | `-$2.4436` | +16.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$5.0752` | +34.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$5.0752` (>1000% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.28).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (Layer 3) — reference only, see Regime above
* Vanna PnL: `+$0.0418` | Volga PnL: `+$0.0362`
* Combined: `+$0.0780` | Residual after: `-$0.0830`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0243`
* **spot**: `+$0.0015`
* **vol**: `+$0.0178`
* **rate**: `-$0.0000`
* Step sum: `-$0.0050` | Model ΔP: `-$0.0050` | Audit residual: `+$0.0000`

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
* Treat the Greek decomposition as a reference view only; the residual is large enough that higher-order effects or engine path dependence may be distorting the attribution.
* No catalyst tags were available, so there is no borrow, squeeze, or IV-crush mechanism to verify from headlines in this run.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-10-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$137.5000` (-888.5%)
* **Model ΔP**: `-$137.5000`
* **Primary drivers**: **Delta PnL** (42%) and **Vega PnL** (25%) and **Theta decay** (18%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by delta: the put lost value as the underlying edged higher, with theta also working against the position. The residual is sizable relative to the model move, so the clean Greek split should be treated as a reference view rather than a complete explanation; higher-order effects and pricing noise likely matter here. There are no retrieved headlines or named microstructure tags, and the observation lock plus suppressed Vega narrative mean no catalyst-specific overlay should be added beyond the model story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation reliability is false, attribution coverage is low, the residual share is high, and the move was accompanied by a large implied-vol change while Vega narration is suppressed. The news set is empty, so there is no independent catalyst evidence to sharpen the Layer B story.

---

## 2. Observation Lock

* **As-of**: `2026-10-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 18.4%)
* **IV move**: -3.44 vol pts vs noise band ±36.68 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$137.5000`
* **Model ΔP (engine)**: `-$137.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$98.1803`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$39.3197` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (28.6%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$118.9804` | +86.5% | Stock moved from $335.19 to $336.54 (+1.3500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.5075` | -1.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$71.1331` | -51.7% | IV moved +14.46 vol pts (66.19% → 62.74%) |
| **Theta decay (Δt · Theta)** | `-$51.8406` | +37.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$39.3197` | +28.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$137.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$39.3197` (28.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.1547`
* Combined: `+$0.1547` | Residual after: `-$1.5297`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.5169`
* **spot**: `-$1.2770`
* **vol**: `+$0.4191`
* **rate**: `+$0.0003`
* Step sum: `-$1.3745` | Model ΔP: `-$1.3750` | Audit residual: `-$0.0005`

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
* Watch whether the residual remains large on a full reprice path, since truncation and surface effects can distort the Greek split when spot and volatility both move.
* Verify future marks for quote quality and surface consistency before leaning on any implied-vol read, because the current feed does not support a stronger catalyst narrative.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$120.5000` (->1000%)
* **Model ΔP**: `-$120.5000`
* **Primary drivers**: **Delta PnL** (54%) and **Vega PnL** (23%) and **Gamma PnL** (10%).
* **Verdict**: The model move was led by the put’s negative delta responding to the lower spot print, with gamma and vega adding smaller supportive effects and theta partially offsetting the move. The residual is modest relative to the modeled change, so the revaluation is well explained by the spot move and normal higher-order approximation error rather than a separate event-driven gap. No relevant headlines were retrieved, so there is no auxiliary catalyst layer to add beyond the blotter.
* **Confidence**: **Medium** — The attribution is supported by the official Taylor breakdown and the diagnostic tools, with high coverage and only a medium residual band. Confidence is limited by the absence of headlines and the fact that the run uses a flat-vol engine with a short-dated American option, so some model gap can remain from path and boundary effects.

---

## 2. Observation Lock

* **As-of**: `2026-10-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.6%)
* **IV move**: +0.94 vol pts vs noise band ±0.06 pts (exceeds noise band)
* **Prior observation**: `2026-10-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$120.5000`
* **Model ΔP (engine)**: `-$120.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$113.5996`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$6.9004` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (5.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$77.9102` | +64.7% | Stock moved from $773.09 to $763.96 (-9.1300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$14.0438` | +11.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$33.1192` | +27.5% | IV moved +0.96 vol pts (20.50% → 21.45%) |
| **Theta decay (Δt · Theta)** | `+$11.4736` | -9.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$6.9004` | +5.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$120.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$6.9004` (5.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0947`
* Combined: `+$0.0947` | Residual after: `+$1.1103`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1146`
* **spot**: `+$0.9013`
* **vol**: `+$0.4173`
* **rate**: `+$0.0030`
* Step sum: `+$1.2072` | Model ΔP: `+$1.2050` | Audit residual: `-$0.0022`

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

* Higher-order convexity and Taylor truncation can still leave a small gap when spot moves through a short-dated American put.
* No relevant headline set was available, so there is no separate catalyst layer to verify from the news tape.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$163.5000` (->1000%)
* **Model ΔP**: `-$163.5000`
* **Primary drivers**: **Delta PnL** (69%) and **Gamma PnL** (15%) and **Vega PnL** (9%).
* **Verdict**: The move is primarily explained by the direction of the underlying, with the call losing value as spot fell. Gamma and vega partially offset that move, while theta added a smaller drag; the remaining residual is consistent with normal second-order truncation rather than a separate story. There are no relevant headlines or microstructure tags to add a Layer B catalyst, and the American feature does not change the narrative because early exercise is not material here.
* **Confidence**: **Medium** — Confidence is medium because the attribution is clean on the dominant Greek and the observation quality is reliable, but the residual is not zero and the option is short-dated enough for curvature effects to matter. The news layer is empty, so there is no external catalyst to validate or refine the tape story.

---

## 2. Observation Lock

* **As-of**: `2026-10-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.4%)
* **IV move**: +0.32 vol pts vs noise band ±0.05 pts (exceeds noise band)
* **Prior observation**: `2026-10-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$163.5000`
* **Model ΔP (engine)**: `-$163.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$156.0326`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$7.4674` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$216.5838` | +132.5% | Stock moved from $773.09 to $763.96 (-9.1300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$47.8768` | -29.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$28.0190` | -17.1% | IV moved +0.41 vol pts (12.80% → 13.12%) |
| **Theta decay (Δt · Theta)** | `-$15.3446` | +9.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$7.4674` | +4.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$163.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$7.4674` (4.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0519`
* Combined: `-$0.0519` | Residual after: `-$1.5831`

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

* Monitor whether a fuller surface revaluation or higher-order convexity would explain the residual better than the Taylor approximation.
* Check for any later news or market microstructure change, but there is currently no relevant borrow, squeeze, or implied-volatility catalyst to layer onto the move.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$76.0000` (+>1000%)
* **Model ΔP**: `+$76.0000`
* **Primary drivers**: **Delta PnL** (72%) and **Gamma PnL** (17%) and **Vega PnL** (7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained first by delta exposure to the stronger underlying price, with gamma adding a smaller convexity lift and theta a modest drag. The remaining gap is small and consistent with second-order Taylor truncation rather than a separate event-driven catalyst. Observation quality is limited, so the run should be read as a model revaluation rather than a tightly sourced tape story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is moderate because the dominant driver is clearly identified by the blotter, but observation reliability is flagged false and no relevant headlines were retrieved. The residual is low, the attribution coverage is high, and the early-exercise premium is negligible, so there is little evidence of a competing mechanism or material American-style boundary effect.

---

## 2. Observation Lock

* **As-of**: `2026-10-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.6%)
* **IV move**: +0.44 vol pts vs noise band ±0.89 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$76.0000`
* **Model ΔP (engine)**: `+$76.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$75.3251`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.6749` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$58.2025` | +76.6% | Stock moved from $43.56 to $45.20 (+1.6400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$13.7797` | +18.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$5.5097` | +7.2% | IV moved +1.19 vol pts (29.88% → 30.32%) |
| **Theta decay (Δt · Theta)** | `-$2.1669` | -2.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.6749` | +0.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$76.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.6749` (0.9% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0095`
* Combined: `+$0.0095` | Residual after: `+$0.7505`

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
* Check whether higher-order convexity or a full-surface reprice would materially change the decomposition if the spot move is treated as more than a linear shift.
* Keep an eye on quote quality and mark stability since the observation lock leaves little external catalyst evidence to validate the revaluation.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-22` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$2.5000` (->1000%)
* **Model ΔP**: `-$2.5000`
* **Primary drivers**: **Vega PnL** (69%) and **Delta PnL** (10%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The dominant modeled driver is vega, with the option repriced lower as implied volatility fell while the spot move was comparatively small. Delta and theta also contributed on the downside, while gamma was minor and the residual is consistent with higher-order effects and the engine’s American boundary / truncation noise rather than a separate catalyst. The early-exercise premium is negligible, so the American feature is not part of the explanation for the move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The feed is observation-locked with no retrieved headlines, so Layer B cannot be independently challenged. Confidence is limited by the large residual band, the small spot move relative to the vol move, and the surface diagnostics showing a failed American FD surface under the current setup.

---

## 2. Observation Lock

* **As-of**: `2026-10-22` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 100.0%)
* **IV move**: -23.44 vol pts vs noise band ±13.88 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$2.5000`
* **Model ΔP (engine)**: `-$2.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$3.0822`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.5822` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (23.3%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.3672` | +10.0% | Stock moved from $1.41 to $1.38 (-0.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0094` | +0.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$2.5543` | +69.3% | IV moved -22.40 vol pts (173.44% → 150.00%) |
| **Theta decay (Δt · Theta)** | `-$0.1701` | +4.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.5822` | +15.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$2.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.5822` (23.3% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0050`
* Combined: `+$0.0050` | Residual after: `-$0.0300`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0017`
* **spot**: `-$0.0035`
* **vol**: `-$0.0198`
* **rate**: `-$0.0000`
* Step sum: `-$0.0250` | Model ΔP: `-$0.0250` | Audit residual: `+$0.0000`

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
* Modeled attribution should still be checked against full-surface repricing and truncation effects, since the residual is material relative to the model move.
* No borrow, squeeze, or IV-crush mechanism is supported by the digest or headline set, so there is no separate catalyst to verify from the tape.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0833 | level_proxy(t) = 0.1728
* Δskew = +0.0062 | Δlevel = +0.0063
* Put 715 delta=-0.1271 | Call 795 delta=0.1488
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
