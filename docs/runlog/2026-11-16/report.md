# Live book run — 2026-11-16

Run `2026-11-16-1794881704`. 7/8 legs diagnosed, 0 settled at expiry, 1 failed. `legs_narrated=7` `legs_silent=0` `llm_calls=10`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-16` | **Positions**: 7 | **Tickers**: AAPL, JPM, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$183.0000`
* **Total Model PnL**: `-$179.7185`
* **Aggregate model vs mark gap**: `+$3.2815`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `JPM 340C 2026-12-18` | `-$367.5000` |
| 2 | `JPM 340P 2026-12-18` | `+$357.5000` |
| 3 | `AAPL 325C 2026-11-20` | `-$354.2185` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$357.9901` |
| Gamma | `+$48.2373` |
| Vega | `+$137.2924` |
| Theta | `-$27.6064` |
| Residual | `+$20.3482` |

### Notable underlyings

* **AAPL**: `-$94.2185` aggregate option PnL
* **SPY**: `-$72.0000` aggregate option PnL
* **JPM**: `-$10.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-16` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$357.5000` (-10.9%)
* **Model ΔP**: `-$354.2185`
* **Primary drivers**: **Delta PnL** (-90.6%) and **Theta decay** (-23.7%) and **Vega PnL** (+23.6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model move is dominated by the downside spot move in the underlying, with gamma only lightly offsetting that effect. Because the observation is not reliable and the Vega narrative is explicitly suppressed, the vol jump is treated as a secondary market condition rather than the main explanatory thread for this run. There are no retrieved headlines or named microstructure mechanisms, so the residual is best read as model-path noise and higher-order effects around the revaluation, not as a separate catalyst story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is supported by the desk’s dominant factor label and the close alignment of the factor buckets with the full model revaluation. Confidence is capped by the noted surface and calibration limitations, the medium residual band, and the fact that observation reliability is false, so the run should be interpreted as a coarse model explanation rather than a precise market narrative.

---

## 2. Observation Lock

* **As-of**: `2026-11-16` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.9%)
* **IV move**: +11.33 vol pts vs noise band ±13.72 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$357.5000`
* **Model ΔP (engine)**: `-$354.2185`
* **Model vs Mark gap**: `+$3.2815` (-0.9% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$317.4982`

* **Method residual (ε_method)**: `-$36.7203` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$3.2815` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (10.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$320.8712` | -90.6% | Stock moved from $356.27 to $352.78 (-3.4900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$3.7730` | +1.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$83.5439` | +23.6% | IV moved +11.33 vol pts (48.90% → 60.23%) |
| **Theta decay (Δt · Theta)** | `-$83.9439` | -23.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$36.7203` | -10.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$354.2185** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$36.7203` (10.4% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$15.2818` | Volga PnL: `+$18.0760`
* Combined: `+$33.3578` | Residual after: `-$70.0781`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$76.1334`
* **spot**: `-$334.3936`
* **vol**: `+$56.3159`
* **rate**: `+$0.0096`
* Step sum: `-$354.2015` | Model ΔP: `-$354.2185` | Audit residual: `-$0.0170`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Higher-order effects and model-path truncation can still distort the attribution when the spot and volatility moves are both active.
* No named catalyst, borrow, or squeeze mechanism was retrieved, so there is nothing to verify on the headline side for this run.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-16` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$260.0000` (-30.4%)
* **Model ΔP**: `+$260.0000`
* **Primary drivers**: **Delta PnL** (+96.8%) and **Vega PnL** (-39.0%) and **Theta decay** (+35.8%).
* **Verdict**: The run is dominated by the option’s positive delta exposure as the stock drifted lower, with gamma and theta partially offsetting the move and vega adding pressure as implied volatility rose. The residual is consistent with higher-order effects and the American FDM revaluation rather than any named catalyst.
* **Confidence**: **Medium** — The attribution is supported by the desk’s dominant factor label and a medium residual band, but the move includes a meaningful volatility change and a non-trivial unexplained remainder. No relevant headlines were retrieved, so there is no Layer B catalyst to anchor the gap story beyond the model revaluation.

---

## 2. Observation Lock

* **As-of**: `2026-11-16` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 10.1%)
* **IV move**: +6.60 vol pts vs noise band ±2.12 pts (exceeds noise band)
* **Prior observation**: `2026-11-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$260.0000`
* **Model ΔP (engine)**: `+$260.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$225.8351`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$34.1649` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (13.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$251.7292` | +96.8% | Stock moved from $356.27 to $352.78 (-3.4900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$17.7151` | -6.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$101.2926` | -39.0% | IV moved +6.11 vol pts (23.40% → 29.51%) |
| **Theta decay (Δt · Theta)** | `+$93.1135` | +35.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$34.1649` | +13.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$260.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$34.1649` (13.1% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$16.3049` | Volga PnL: `-$3.3661`
* Combined: `-$19.6710` | Residual after: `+$53.8359`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$98.2899`
* **spot**: `+$247.3658`
* **vol**: `-$85.6631`
* **rate**: `-$0.0069`
* Step sum: `+$259.9857` | Model ΔP: `+$260.0000` | Audit residual: `+$0.0143`

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

* Higher-order convexity and full-engine revaluation can still distort the Taylor breakdown when spot and implied volatility both move.
* No named catalyst was retrieved, so there is no separate borrow, squeeze, or IV-crush narrative to verify from headlines.

---

### Position 3 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-16` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$367.5000` (-27.4%)
* **Model ΔP**: `-$367.5000`
* **Primary drivers**: **Delta PnL** (-135.8%) and **Vega PnL** (+34.4%) and **Gamma PnL** (+13.5%).
* **Verdict**: The option loss was driven primarily by the underlying decline, with the modeled spot move overwhelming the other Taylor buckets. Gamma and vega cushioned part of that move, while theta added a smaller drag, leaving only a trivial method residual. No separate catalyst layer is available here, and the early-exercise premium is negligible, so this is a clean spot-led revaluation rather than an American exercise or dividend story.
* **Confidence**: **Medium** — The attribution is well-covered by the quant engine and the residual is very small, but the news layer is empty, so there is no external catalyst to corroborate beyond the market move itself. The exact mix is still a reference-style Greek decomposition, so the verdict stays at medium rather than high.

---

## 2. Observation Lock

* **As-of**: `2026-11-16` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.1%)
* **IV move**: +0.87 vol pts vs noise band ±0.50 pts (exceeds noise band)
* **Prior observation**: `2026-11-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$367.5000`
* **Model ΔP (engine)**: `-$367.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$366.1676`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.3324` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$498.9495` | -135.8% | Stock moved from $346.19 to $338.21 (-7.9800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$49.5142` | +13.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$126.4191` | +34.4% | IV moved +3.12 vol pts (22.68% → 25.80%) |
| **Theta decay (Δt · Theta)** | `-$43.1514` | -11.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.3324` | -0.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$367.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.3324` (0.4% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$9.2156` | other second-order: `+$0.4607`
* Combined: `+$9.6762` | Residual after: `-$11.0086`

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

* Watch for higher-order convexity if the spot gap widens further, since the current decomposition can understate truncation when moves get larger.
* Verify that the next mark remains consistent with a spot-led revaluation; there is no separate headline-based IV, borrow, or squeeze mechanism to carry this move.

---

### Position 4 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-16` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$357.5000` (+55.6%)
* **Model ΔP**: `+$357.5000`
* **Primary drivers**: **Delta PnL** (+83.5%) and **Gamma PnL** (+14.2%) and **Vega PnL** (+12.7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model move is dominated by the put’s negative delta responding to the lower spot print, with gamma adding convexity and theta offsetting part of the gain. The Greek decomposition is clean, and the tiny method residual indicates the revaluation is well explained by the blotter rather than by any separate event narrative. There are no relevant headlines, so there is no Layer B catalyst to add beyond the spot-led repricing. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is high and the residual is negligible, but observation quality is flagged as unreliable and Vega narration is suppressed, so the story should stay at the coarse spot-driven level. There are no retrieved headlines or microstructure tokens to support an auxiliary catalyst explanation.

---

## 2. Observation Lock

* **As-of**: `2026-11-16` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 10.0%)
* **IV move**: +0.82 vol pts vs noise band ±1.26 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$357.5000`
* **Model ΔP (engine)**: `+$357.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$357.4946`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0054` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$298.3557` | +83.5% | Stock moved from $346.19 to $338.21 (-7.9800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$50.6611` | +14.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$45.3366` | +12.7% | IV moved +1.12 vol pts (22.36% → 23.48%) |
| **Theta decay (Δt · Theta)** | `-$36.8586` | -10.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0054` | +0.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$357.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0054` (0.0% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$4.2559` | other second-order: `+$0.0839`
* Combined: `+$4.3398` | Residual after: `-$4.3344`

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
* Watch whether the next mark stays close to the model revaluation or whether truncation and surface effects begin to matter more as the option remains near the money.
* No headline-backed Layer B mechanism is available here; keep an eye only on future quote quality and any newly retrieved catalyst context.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-16` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$71.5000` (+111.7%)
* **Model ΔP**: `-$71.5000`
* **Primary drivers**: **Delta PnL** (-114.4%) and **Theta decay** (+83.0%) and **Gamma PnL** (-63.5%).
* **Verdict**: The move is dominated by spot moving lower, with the put benefiting primarily from the delta revaluation in the desk’s Taylor view. Gamma and implied volatility also added to the option’s sensitivity, while theta partially offset the move; the remaining gap is consistent with higher-order effects and truncation around a larger underlying move.
* **Confidence**: **Medium** — The blotter is calibrated and the observation is reliable, but the residual is still large relative to the modeled move, so the Taylor breakdown is only a reference view rather than a perfect explanation. No relevant headlines were retrieved, so there is no named catalyst layer to anchor beyond the market move and residual mechanics.

---

## 2. Observation Lock

* **As-of**: `2026-11-16` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.2%)
* **IV move**: +3.78 vol pts vs noise band ±0.10 pts (exceeds noise band)
* **Prior observation**: `2026-11-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$71.5000`
* **Model ΔP (engine)**: `-$71.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$112.4880`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$40.9880` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (57.3%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$81.8083` | -114.4% | Stock moved from $754.37 to $739.95 (-14.4200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$45.4235` | -63.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$44.5885` | -62.4% | IV moved +3.74 vol pts (24.99% → 28.73%) |
| **Theta decay (Δt · Theta)** | `+$59.3324` | +83.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$40.9880` | +57.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$71.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$40.9880` (57.3% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.56).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (vanna, volga) — reference only, see Regime above
* Vanna PnL: `-$33.2338` | Volga PnL: `-$8.2083`
* Combined: `-$41.4422` | Residual after: `+$82.4302`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$50.1984`
* **spot**: `-$68.5190`
* **vol**: `-$53.1798`
* **rate**: `+$0.0029`
* Step sum: `-$71.4976` | Model ΔP: `-$71.5000` | Audit residual: `-$0.0024`

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

* Higher-order convexity and Taylor truncation can still distort the reference attribution when the spot move is large relative to the option’s remaining life.
* With no retrieved catalyst headlines, focus on quote quality and the reprice path rather than layering in an unsupported event story.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-16` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$0.5000` (-33.3%)
* **Model ΔP**: `-$0.5000`
* **Primary drivers**: **Vega PnL** (+28.8%) and **Gamma PnL** (+20.5%) and **Delta PnL** (-13.6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The official Taylor breakdown leaves the residual as the dominant modeled driver, so the move is best read as a model revaluation gap rather than a clean single-Greek story. The large spot drop and sharp implied-vol jump provide the backdrop, but the residual is what most of the unexplained change sits in, with truncation and higher-order effects a plausible mechanism inside the model. There are no named headlines or microstructure tags to support a separate catalyst layer, so no external event should be layered onto the attribution. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation quality is weak, the attribution coverage is low, and the residual share is large relative to the full model move. The market feed is incomplete for catalyst confirmation, and there are no relevant headlines to tie the residual to a specific event. The diagnostics support a coarse explanation only.

---

## 2. Observation Lock

* **As-of**: `2026-11-16` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: +9.08 vol pts vs noise band ±1.07 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$0.5000`
* **Model ΔP (engine)**: `-$0.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$10.3629`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$10.8629` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$4.9364` | -13.6% | Stock moved from $754.37 to $739.95 (-14.4200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$7.4246` | +20.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$10.4141` | +28.8% | IV moved +9.67 vol pts (13.80% → 23.47%) |
| **Theta decay (Δt · Theta)** | `-$2.5394` | -7.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$10.8629` | -30.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.5000** | **-1.4%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$10.8629` (>1000% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 1.50).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (vanna, volga) — reference only, see Regime above
* Vanna PnL: `-$66.7743` | Volga PnL: `+$31.5493`
* Combined: `-$35.2249` | Residual after: `+$24.3620`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$1.4573`
* **spot**: `-$0.0425`
* **vol**: `+$0.9999`
* **rate**: `+$0.0000`
* Step sum: `-$0.4999` | Model ΔP: `-$0.5000` | Audit residual: `-$0.0001`

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
* Large residuals can reflect Taylor truncation, higher-order convexity, or path effects when spot and implied volatility move together; verify against the full reprice rather than the Greek sum alone.
* No named catalyst or microstructure tag is available here, so do not infer a squeeze, borrow stress, or IV-crush narrative from this tape.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-16` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$3.5000` (-2.1%)
* **Model ΔP**: `-$3.5000`
* **Primary drivers**: **Vega PnL** (+45.4%) and **Theta decay** (-35.3%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The desk run is dominated by the modeled volatility move, but the attribution is only a reference view because the observation is unreliable and the Vega narrative is suppressed by the run flags. The price change also carries a sizable unexplained remainder, so this is best read as a full model revaluation where higher-order effects and surface fit issues are doing meaningful work alongside the vega line. No external catalyst was retrieved, so there is no validated news-based Layer B mechanism to add. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — The code points to Vega as the dominant Taylor factor, but attribution coverage is low, the residual band is high, and observation reliability is false. The run also suppresses a Vega narrative and provides no relevant headlines, so the diagnosis must stay coarse and avoid a catalyst claim.

---

## 2. Observation Lock

* **As-of**: `2026-11-16` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 19.2%)
* **IV move**: +9.67 vol pts vs noise band ±10.31 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-13`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$3.5000`
* **Model ΔP (engine)**: `-$3.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$2.3944`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$5.8944` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (168.4%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$1.5095` | -3.9% | Stock moved from $46.36 to $46.34 (-0.0200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0031` | +0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$17.4598` | +45.4% | IV moved +8.67 vol pts (31.94% → 40.61%) |
| **Theta decay (Δt · Theta)** | `-$13.5589` | -35.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$5.8944` | -15.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$3.5000** | **-9.1%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$5.8944` (168.4% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.0807` | Volga PnL: `+$0.5755`
* Combined: `+$0.6562` | Residual after: `-$6.5507`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$14.1030`
* **spot**: `-$1.6307`
* **vol**: `+$12.2343`
* **rate**: `+$0.0009`
* Step sum: `-$3.4985` | Model ΔP: `-$3.5000` | Audit residual: `-$0.0015`

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
* Residuals can still distort the reference attribution because the move is being evaluated through a truncated Taylor lens with a large unexplained component.
* Watch for any later tape or chain update that clarifies whether the volatility move was a clean repricing or a noisy surface/mark effect.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0520 | level_proxy(t) = 0.2604
* Δskew = -0.0530 | Δlevel = +0.0643
* Put 715 delta=-0.1218 | Call 795 delta=0.0019
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **plug_deep_otm** (PLUG): RuntimeError: Data break: T-1 calibrated IV ~= quote-source IV failed. PLUG 4C 2026-12-18 mark 0.0300 on 2026-11-13 at spot 1.11 calibrates to 247.18% vol; the quote source reads 187.50% (+59.68 vol pts). A mark and a spot taken at different times produce this gap. No correction applied; nothing was narrated. This is a data problem, not an unexplained market move.
