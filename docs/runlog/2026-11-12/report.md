# Live book run — 2026-11-12

Run `2026-11-12-1794536104`. 8/8 legs diagnosed, 0 settled at expiry, 0 failed. `legs_narrated=6` `legs_silent=2` `llm_calls=7`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-12` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$15.0000`
* **Total Model PnL**: `+$15.0000`
* **Aggregate model vs mark gap**: `+$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `-$67.5000` |
| 2 | `AAPL 350C 2026-11-20` | `+$67.5000` |
| 3 | `JPM 340P 2026-12-18` | `+$62.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$51.1100` |
| Gamma | `-$0.4825` |
| Vega | `+$59.0385` |
| Theta | `+$3.9236` |
| Residual | `+$3.6304` |

### Notable underlyings

* **JPM**: `+$35.0000` aggregate option PnL
* **SPY**: `-$19.5000` aggregate option PnL
* **VZ**: `-$0.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$67.5000` (-2.2%)
* **Model ΔP**: `-$67.5000`
* **Primary drivers**: **Delta PnL** (-109.3%) and **Vega PnL** (+16.3%) and **Theta decay** (-9.5%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-11-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.0%)
* **IV move**: +4.79 vol pts vs noise band ±16.89 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-11`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$67.5000`
* **Model ΔP (engine)**: `-$67.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$69.1186`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.6186` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$73.7853` | -109.3% | Stock moved from $355.63 to $354.88 (-0.7500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0744` | +0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$11.0199` | +16.3% | IV moved +4.89 vol pts (27.35% → 32.24%) |
| **Theta decay (Δt · Theta)** | `-$6.4275` | -9.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.6186` | +2.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$67.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.6186` (2.4% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.00).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (vanna, volga) — reference only, see Regime above
* Vanna PnL: `+$1.6326` | Volga PnL: `+$4.5327`
* Combined: `+$6.1652` | Residual after: `-$4.5466`

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

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$67.5000` (-7.8%)
* **Model ΔP**: `+$67.5000`
* **Primary drivers**: **Delta PnL** (+76.3%) and **Theta decay** (+41.9%) and **Vega PnL** (-18.7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by the option’s sensitivity to the small down move in the underlying, with theta decay offsetting some of that effect and leaving a modest net gain in the model. Vega is present in the blotter but the diagnostic flags suppress a vega narrative here, so the clean Layer A read is a delta-led revaluation rather than a volatility story. There are no retrieved headlines or named microstructure mechanisms, so there is no separate Layer B catalyst to attach to the move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is high and the residual is low, but observation reliability is flagged false and there are no headlines to corroborate a catalyst. The early-exercise premium is negligible, so American-style exercise does not add a separate explanation.

---

## 2. Observation Lock

* **As-of**: `2026-11-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.7%)
* **IV move**: +0.70 vol pts vs noise band ±1.18 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-11`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$67.5000`
* **Model ΔP (engine)**: `+$67.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$66.3911`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.1089` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$51.5062` | +76.3% | Stock moved from $355.63 to $354.88 (-0.7500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.7772` | -1.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$12.6512` | -18.7% | IV moved +0.64 vol pts (22.97% → 23.60%) |
| **Theta decay (Δt · Theta)** | `+$28.3133` | +41.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.1089` | +1.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$67.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.1089` (1.6% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.3634`
* Combined: `-$0.3634` | Residual after: `+$1.4722`

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
* Model attribution is well behaved, but the small residual means higher-order terms and quote noise remain the only minor checks on the revaluation.
* No catalyst layer is available from the digest, so there is nothing to verify on IV crush, borrow, buy-in, liquidity, or conversion from headlines.

---

### Position 3 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$27.5000` (-2.2%)
* **Model ΔP**: `-$27.5000`
* **Primary drivers**: **Delta PnL** (-120.0%) and **Vega PnL** (+72.7%) and **Theta decay** (-52.7%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-11-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.9%)
* **IV move**: +0.51 vol pts vs noise band ±0.83 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-11`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$27.5000`
* **Model ΔP (engine)**: `-$27.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$27.2628`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.2371` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$32.9954` | -120.0% | Stock moved from $343.39 to $342.82 (-0.5700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.2503` | +0.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$19.9858` | +72.7% | IV moved +0.47 vol pts (23.16% → 23.63%) |
| **Theta decay (Δt · Theta)** | `-$14.5037` | -52.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.2371` | -0.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$27.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.2371` (0.9% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.0742`
* Combined: `+$0.0742` | Residual after: `-$0.3113`

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

### Position 4 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$62.5000` (+8.9%)
* **Model ΔP**: `+$62.5000`
* **Primary drivers**: **Vega PnL** (+80.2%) and **Delta PnL** (+37.9%) and **Theta decay** (-17.7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven primarily by the model’s revaluation to higher implied volatility, with spot contributing a smaller supportive gain and theta partly offsetting the move. The residual is minimal, so the Taylor decomposition is clean; however, the observation lock and suppressed Vega narrative mean the run should be read as a model repricing rather than a news-led catalyst story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is limited by the observation lock and the fact that no relevant headlines were retrieved, so there is no independent catalyst confirmation. The attribution itself is internally consistent, but the suppressed Vega narrative means the volatility move should be treated as a proxied market input rather than a fully sourced event explanation.

---

## 2. Observation Lock

* **As-of**: `2026-11-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 7.2%)
* **IV move**: +0.53 vol pts vs noise band ±0.65 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-11`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$62.5000`
* **Model ΔP (engine)**: `+$62.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$63.0113`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.5113` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$23.6979` | +37.9% | Stock moved from $343.39 to $342.82 (-0.5700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.2850` | +0.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$50.0991` | +80.2% | IV moved +1.18 vol pts (20.52% → 21.70%) |
| **Theta decay (Δt · Theta)** | `-$11.0707` | -17.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.5113` | -0.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$62.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.5113` (0.8% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.2915`
* Combined: `+$0.2915` | Residual after: `-$0.8028`

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
* Residual is low, so the first thing to verify is whether any later mark or full-surface reprice changes the balance between volatility and spot effects.
* With no retrieved catalyst tape, monitor for any subsequent implied-volatility or liquidity update that would validate the model repricing rather than a news-driven move.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$15.5000` (+31.3%)
* **Model ΔP**: `-$15.5000`
* **Primary drivers**: **Vega PnL** (-112.1%) and **Theta decay** (+84.5%) and **Delta PnL** (-75.2%).
* **Verdict**: The blotter’s dominant modeled driver is a revaluation from higher implied volatility, with spot also drifting lower and adding a smaller downside contribution. The residual is consistent with ordinary higher-order effects and model truncation around a short-dated option, rather than a separate catalyst. The headlines only supply background on implied volatility and IV crush; they do not show an issuer-specific event, but they do support describing the tape as an implied volatility move rather than a pure spot-only repricing.
* **Confidence**: **Medium** — The attribution coverage is high and the observation is reliable, but the residual is still material enough to keep the diagnosis at a coarser level. The headline set is generic volatility education rather than issuer-specific news, so it supports the mechanism language only in a background sense and does not establish a distinct event-driven cause.

---

## 2. Observation Lock

* **As-of**: `2026-11-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.1%)
* **IV move**: +1.62 vol pts vs noise band ±0.08 pts (exceeds noise band)
* **Prior observation**: `2026-11-11`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$15.5000`
* **Model ΔP (engine)**: `-$15.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$17.1414`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.6414` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (10.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$11.6611` | -75.2% | Stock moved from $759.81 to $757.12 (-2.6900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$1.2072` | -7.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$17.3721` | -112.1% | IV moved +1.58 vol pts (23.12% → 24.70%) |
| **Theta decay (Δt · Theta)** | `+$13.0991` | +84.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.6414` | +10.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$15.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.6414` (10.6% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$2.4513` | Volga PnL: `-$1.7092`
* Combined: `-$4.1605` | Residual after: `+$5.8018`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$13.0944`
* **spot**: `-$10.5501`
* **vol**: `-$18.0454`
* **rate**: `+$0.0115`
* Step sum: `-$15.4897` | Model ΔP: `-$15.5000` | Audit residual: `-$0.0103`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega / implied volatility move**._

_Intel note: All three items are general options/volatility education or market-structure discussion, with SPY mentioned only as an example in one headline. None is a corporate or issuer-specific event for SPY, so they are kept as background rather than relevant._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Implied Volatility and IV Crush Explained** _(Source: proptraderz.com)_
   Educational piece explaining implied volatility and IV crush; not a ticker-specific news event.
2. **help me understand implied volatility : r/options** _(Source: reddit.com)_
   Options forum discussion about implied volatility, with no SPY-specific issuer or corporate event.

_Peer / sector background (indirect context, not a required catalyst):_

3. **Do Long Options Pay in Negative Gamma? SPY, QQQ, IWM Backtest | FlashAlpha** _(Source: FlashAlpha)_
   Backtest discussing SPY alongside other broad ETFs; useful market context but not a company-specific event.

---

## 7. Risk Watchlist

* Model truncation and short-dated convexity can still leave a noticeable residual, so the Greek breakdown should be treated as a reference view rather than a perfect replay.
* Keep an eye on implied volatility and IV crush behavior in the tape, since the move is being driven more by volatility repricing than by spot alone.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$4.0000` (-61.5%)
* **Model ΔP**: `-$4.0000`
* **Primary drivers**: **Delta PnL** (-84.3%) and **Theta decay** (-61.5%) and **Gamma PnL** (+19.5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best explained by the option’s delta exposure to the modest spot decline, with theta decay adding a meaningful second drag to the model revaluation. Gamma partially cushioned the move and the small residual is consistent with higher-order effects around a short-dated American call, but there is no separate news catalyst to layer on top of the blotter story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by the observation lock and the fact that no headlines were retrieved, so there is no catalyst evidence to supplement the factor story. The residual is not trivial, but the blotter still shows a clean dominant delta explanation with theta as a secondary drag and no meaningful early-exercise premium.

---

## 2. Observation Lock

* **As-of**: `2026-11-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 40.0%)
* **IV move**: +0.29 vol pts vs noise band ±0.28 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-11`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$4.0000`
* **Model ΔP (engine)**: `-$4.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$4.4681`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.4681` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (11.7%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$3.3701` | -84.3% | Stock moved from $759.81 to $757.12 (-2.6900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.7804` | +19.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.5803` | +14.5% | IV moved +0.15 vol pts (12.59% → 12.74%) |
| **Theta decay (Δt · Theta)** | `-$2.4586` | -61.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.4681` | +11.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$4.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.4681` (11.7% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.3974` | other second-order: `+$0.0182`
* Combined: `-$0.3792` | Residual after: `+$0.8473`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$2.4543`
* **spot**: `-$1.7989`
* **vol**: `+$0.2551`
* **rate**: `+$0.0012`
* Step sum: `-$3.9970` | Model ΔP: `-$4.0000` | Audit residual: `-$0.0030`

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
* Watch whether a full-surface reprice or higher-order convexity would widen the residual on the next close-to-close run.
* With no retrieved headlines, there is no basis to add a borrow, squeeze, or IV-crush interpretation; keep the focus on the model’s delta and decay inputs.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$0.5000` (-0.3%)
* **Model ΔP**: `-$0.5000`
* **Primary drivers**: **Vega PnL** (+48.1%) and **Delta PnL** (-28.5%) and **Theta decay** (-21.0%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by a modeled volatility reprice: the option’s value was driven mainly by the higher implied-vol input, while the small spot slip and time decay were secondary offsets. Because the observation is locked and no relevant headlines were retrieved, there is no separate news catalyst to attach to the move; the residual mainly reflects model truncation and other higher-order effects rather than a named event. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is only medium because observation is unreliable, the attribution coverage is low, and the residual band is high. The desk also suppresses a Vega narrative from news, and no catalyst evidence was retrieved, so the explanation should stay at the modeled-factor level.

---

## 2. Observation Lock

* **As-of**: `2026-11-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 12.7%)
* **IV move**: +3.66 vol pts vs noise band ±5.65 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-11`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$0.5000`
* **Model ΔP (engine)**: `-$0.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$0.1729`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.3271` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (65.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$3.9937` | -28.5% | Stock moved from $46.60 to $46.55 (-0.0500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0180` | +0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$6.7464` | +48.1% | IV moved +3.30 vol pts (27.09% → 30.39%) |
| **Theta decay (Δt · Theta)** | `-$2.9436` | -21.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.3271` | -2.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.5000** | **-3.6%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.3271` (65.4% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.1140` | Volga PnL: `+$0.1937`
* Combined: `+$0.3078` | Residual after: `-$0.6349`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$2.9427`
* **spot**: `-$4.0434`
* **vol**: `+$6.4870`
* **rate**: `+$0.0076`
* Step sum: `-$0.4914` | Model ΔP: `-$0.5000` | Audit residual: `-$0.0086`

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
* Taylor decomposition can be distorted by truncation and higher-order terms when the residual band is high; treat the factor split as a reference view rather than a perfect audit.
* No named catalyst was retrieved, so verify the mark quality and the implied-vol input rather than forcing a news-based explanation.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-12` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (+43.5%) and **Delta PnL** (-35.1%) and **Gamma PnL** (+6.5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is dominated by the spot drop interacting with the option’s delta, with gamma partly offsetting the directional loss and theta a smaller drag. The large residual and wide vol reprice mean the Taylor view is only a rough attribution here; the full revaluation is not being replaced by a cleaner Greek story. With no retrieved headlines and observation marked unreliable, there is no supported external catalyst to add beyond the market move itself. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation reliability is false, attribution coverage is weak, the residual band is high, and the diagnostic tools show the Greek decomposition is only a reference view. Vega is flagged as the code driver, but the run also says to suppress Vega narrative and no relevant headlines were retrieved, so the story should stay coarse.

---

## 2. Observation Lock

* **As-of**: `2026-11-12` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: +43.75 vol pts vs noise band ±86.67 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-11`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000`
* **Explained ΔP (Taylor ex-residual)**: `+$0.1310`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.1310` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.5086` | -35.1% | Stock moved from $1.36 to $1.24 (-0.1250) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0939` | +6.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.6303` | +43.5% | IV moved +16.66 vol pts (167.92% → 184.58%) |
| **Theta decay (Δt · Theta)** | `-$0.0846` | -5.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.1310` | -9.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **-0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.1310` (>1000% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.2899` | Volga PnL: `+$0.1298`
* Combined: `-$0.1601` | Residual after: `+$0.0292`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.0846`
* **spot**: `-$0.3915`
* **vol**: `+$0.4761`
* **rate**: `+$0.0001`
* Step sum: `+$0.0001` | Model ΔP: `-$0.0000` | Audit residual: `-$0.0001`

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
* Treat the Greek split as approximate; higher-order effects and model/quote noise can materially distort the attribution in this setup.
* No named catalyst or microstructure mechanism was retrieved, so there is nothing to verify on IV crush, borrow, buy-in, or squeeze from the tape supplied here.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.1138 | level_proxy(t) = 0.1887
* Δskew = +0.0133 | Δlevel = +0.0096
* Put 715 delta=-0.0546 | Call 795 delta=0.0055
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
