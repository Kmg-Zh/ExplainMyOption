# Live book run — 2026-11-25

Run `2026-11-25-1795660218`. 8/8 legs diagnosed, 0 settled at expiry, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=13`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-25` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$179.5000`
* **Total Model PnL**: `-$179.5000`
* **Aggregate model vs mark gap**: `-$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 360C 2027-01-15` | `-$307.5000` |
| 2 | `AAPL 335C 2027-01-15` | `+$195.0000` |
| 3 | `SPY 655P 2027-01-15` | `-$88.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$251.0008` |
| Gamma | `-$24.0105` |
| Vega | `+$58.5733` |
| Theta | `-$11.2135` |
| Residual | `+$48.1515` |

### Notable underlyings

* **AAPL**: `-$112.5000` aggregate option PnL
* **SPY**: `-$82.0000` aggregate option PnL
* **VZ**: `+$60.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 335C 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 335C 2027-01-15`  
**Analysis Date**: `2026-11-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$195.0000` (+7.2%)
* **Model ΔP**: `+$195.0000`
* **Primary drivers**: **Delta PnL** (+57.2%) and **Vega PnL** (+50.4%) and **Theta decay** (-7.2%).
* **Verdict**: The move is primarily explained by the option’s positive delta against a modest rise in the underlying, with a smaller supporting contribution from higher implied volatility. The residual is negligible, so the close-to-close revaluation is well captured by the model rather than by a large truncation or mark-gap effect. The headline set does not supply an Apple-specific catalyst, so the tape reads as a clean factor move rather than a news-led reprice.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is strong and the residual is low, but the news digest does not identify a relevant issuer-specific catalyst. The run also notes a surface diagnostic limitation, so the Greek view should be treated as a model-based explanation of the revaluation rather than a deeper event-driven inference.

---

## 2. Observation Lock

* **As-of**: `2026-11-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 6.4%)
* **IV move**: +2.47 vol pts vs noise band ±2.14 pts (exceeds noise band)
* **Prior observation**: `2026-11-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$195.0000`
* **Model ΔP (engine)**: `+$195.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$196.7893`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.7893` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$111.4549` | +57.2% | Stock moved from $354.07 to $355.58 (+1.5100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.0097` | +0.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$98.2980` | +50.4% | IV moved +2.26 vol pts (27.48% → 29.74%) |
| **Theta decay (Δt · Theta)** | `-$13.9733` | -7.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.7893` | -0.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$195.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.7893` (0.9% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.7546`
* Combined: `-$0.7546` | Residual after: `-$1.0347`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Intel note: The headline set is mostly broad market or unrelated coverage and does not include an Apple-specific issuer, control-structure, or options-mechanism story. No relevant AAPL-linked items were identified._
_Intel triage discarded 3 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. [As Anthropic shares tank, investors scramble to hedge. It could be very expensive - CNBC](https://www.cnbc.com/2026/11/20/as-anthropic-shares-tank-investors-scramble-to-hedge-it-could-be-very-expensive.html)
2. [This VIX Signal Is Bullish For The S&P 500. - Investor's Business Daily](https://www.investors.com/news/sp-500-nasdaq-dow-jones-vix-ai-trade-stock-market/)
3. [20 Best Undervalued Stocks Now To Buy For December 2026 - Forbes](https://www.forbes.com/sites/investor-hub/article/best-undervalued-stocks-december-2026/)

---

## 7. Risk Watchlist

* Higher-order convexity is not a major distortion here, but the model can still drift if the spot path or surface inputs become less stable.
* No Apple-specific catalyst was identified in the headline set; verify that the move remains a factor-driven revaluation rather than a late issuer-level headline or quote update.

---

### Position 2 — `AAPL 360C 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 360C 2027-01-15`  
**Analysis Date**: `2026-11-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$307.5000` (+35.5%)
* **Model ΔP**: `-$307.5000`
* **Primary drivers**: **Delta PnL** (-85.8%) and **Vega PnL** (-14.1%) and **Gamma PnL** (-8.5%).
* **Verdict**: The model move is dominated by delta from the higher stock price, with gamma adding a smaller convexity drag and theta partly offsetting the loss on the short call. Vega also contributed modestly as implied volatility rose, but the position’s day was mainly a spot-driven revaluation rather than a volatility story. The residual is negligible, so the Taylor view is a close read of the engine repricing.
* **Confidence**: **Medium** — Confidence is supported by high attribution coverage, a low residual, reliable observation, and a completed reconciliation. Confidence is held to medium because there are no named headlines, the move is modest, and the blotter explicitly limits the story to the model revaluation without an external catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-11-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.5%)
* **IV move**: +1.06 vol pts vs noise band ±0.61 pts (exceeds noise band)
* **Prior observation**: `2026-11-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$307.5000`
* **Model ΔP (engine)**: `-$307.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$307.9544`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.4544` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$263.9626` | -85.8% | Stock moved from $349.08 to $355.58 (+6.5000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$26.2266` | -8.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$43.4926` | -14.1% | IV moved +0.84 vol pts (23.48% → 24.32%) |
| **Theta decay (Δt · Theta)** | `+$25.7274` | +8.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.4544` | +0.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$307.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.4544` (0.1% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$2.1580`
* Combined: `-$2.1580` | Residual after: `+$2.6124`

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

* Watch whether the next repricing is still dominated by spot and second-order convexity rather than truncation or a broader full-surface reprice.
* Given the lack of named catalysts, do not force a borrow, squeeze, or IV-crush narrative; the tape here is a clean delta-led model move.

---

### Position 3 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$4.0000` (+3.8%)
* **Model ΔP**: `+$4.0000`
* **Primary drivers**: **Vega PnL** (+56.6%) and **Theta decay** (-26.5%) and **Delta PnL** (-14.9%).
* **Verdict**: The position was lifted primarily by the rise in implied volatility, which outweighed the small adverse effect from the slight spot drift and the usual time decay. The model also leaves a modest residual, which is consistent with second-order curvature and revaluation effects rather than a separate news catalyst. No relevant headlines were retrieved, so Layer B is limited to the market’s own vol repricing in the model.
* **Confidence**: **Medium** — The dominant driver is clearly identified by the blotter and the attribution coverage is high, but the residual is still material enough to leave some room for truncation and path effects. There are no named headlines or relevant microstructure tokens to anchor a separate catalyst story, so the diagnosis stays at the market-move level.

---

## 2. Observation Lock

* **As-of**: `2026-11-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 7.3%)
* **IV move**: +0.36 vol pts vs noise band ±0.25 pts (exceeds noise band)
* **Prior observation**: `2026-11-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$4.0000`
* **Model ΔP (engine)**: `+$4.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$4.5427`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.5427` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (13.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$4.3710` | -14.9% | Stock moved from $317.10 to $316.74 (-0.3600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0721` | +0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$16.6189` | +56.6% | IV moved +1.01 vol pts (22.30% → 23.31%) |
| **Theta decay (Δt · Theta)** | `-$7.7773` | -26.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.5427` | -1.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$4.0000** | **+13.6%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.5427` (13.6% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.3894` | Volga PnL: `+$0.4955`
* Combined: `+$0.1061` | Residual after: `-$0.6489`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$7.7796`
* **spot**: `-$4.1062`
* **vol**: `+$15.8848`
* **rate**: `-$0.0310`
* Step sum: `+$3.9680` | Model ΔP: `+$4.0000` | Audit residual: `+$0.0320`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Monitor whether the residual remains contained under a fuller reprice, since higher-order effects can matter when spot and vol both move.
* With no relevant headlines, treat the move as a pure implied volatility repricing inside the model rather than a catalyst-driven tape.

---

### Position 4 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$50.0000` (-2.1%)
* **Model ΔP**: `-$50.0000`
* **Primary drivers**: **Vega PnL** (-229.3%) and **Delta PnL** (+62.8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The option’s model move was led by a lower implied volatility reprice, with the stock’s small down move and theta decay acting as secondary drags in the reference decomposition. Because the observation is locked and the digest contains no relevant headlines, there is no named catalyst layer to add; the run is a model revaluation story rather than a news-led attribution. The large residual means higher-order convexity and model-path effects likely absorbed a meaningful part of the move around the FDM reprice. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is capped by the observation lock, the missing headline set, and the large residual share, so the Greek split should be treated as a reference view rather than a fully clean causal explanation. The engine also flags the condition that the Vega narrative is suppressed, which limits how strongly the implied-vol move can be asserted as an economic fact from the tape alone.

---

## 2. Observation Lock

* **As-of**: `2026-11-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 10.9%)
* **IV move**: -2.84 vol pts vs noise band ±24.01 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$50.0000`
* **Model ΔP (engine)**: `-$50.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$90.2581`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$40.2581` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (80.5%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$31.4172` | +62.8% | Stock moved from $317.10 to $316.74 (-0.3600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0763` | +0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$114.6437` | -229.3% | IV moved -6.85 vol pts (23.54% → 16.69%) |
| **Theta decay (Δt · Theta)** | `-$7.1079` | -14.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$40.2581` | +80.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$50.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$40.2581` (80.5% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$2.3096` | Volga PnL: `+$17.7002`
* Combined: `+$20.0098` | Residual after: `+$20.2483`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$7.0981`
* **spot**: `+$31.6926`
* **vol**: `-$74.5134`
* **rate**: `+$0.0690`
* Step sum: `-$49.8499` | Model ΔP: `-$50.0000` | Audit residual: `-$0.1501`

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
* Residual size is large enough that Taylor truncation and path-dependent repricing can materially distort the Greek bucket split.
* Monitor whether the observed implied-vol move persists in the full surface and whether any future tape adds a borrow, squeeze, buy-in, or earnings-linked catalyst.

---

### Position 5 — `SPY 655P 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 655P 2027-01-15`  
**Analysis Date**: `2026-11-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$88.0000` (+11.8%)
* **Model ΔP**: `-$88.0000`
* **Primary drivers**: **Vega PnL** (-77.3%) and **Delta PnL** (-40.9%) and **Theta decay** (+20.1%).
* **Verdict**: The move is dominated by the option’s sensitivity to the higher implied-volatility print, with spot lower and gamma comparatively minor in the one-day revaluation. The residual is small, so the Taylor breakdown is consistent with the model repricing cleanly rather than pointing to a separate gap. The broad-market VIX commentary in the kept headlines is background only and does not add a separate catalyst mechanism for this SPY contract.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is high, observation quality is reliable, and the residual is low. The main limitation is that the headlines are broad market context rather than a direct SPY-specific catalyst, so Layer B stays auxiliary and does not materially sharpen the story.

---

## 2. Observation Lock

* **As-of**: `2026-11-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.3%)
* **IV move**: +1.01 vol pts vs noise band ±0.08 pts (exceeds noise band)
* **Prior observation**: `2026-11-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$88.0000`
* **Model ΔP (engine)**: `-$88.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$87.0809`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.9191` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$35.9560` | -40.9% | Stock moved from $718.78 to $716.70 (-2.0800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.7228` | -0.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$68.0599` | -77.3% | IV moved +0.98 vol pts (28.44% → 29.42%) |
| **Theta decay (Δt · Theta)** | `+$17.6579` | +20.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.9191` | -1.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$88.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.9191` (1.0% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$1.5566` | Volga PnL: `-$0.9693`
* Combined: `-$2.5259` | Residual after: `+$1.6067`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction / implied volatility move**._

_Intel note: Two headlines are background for SPY because they discuss broad equity-market and volatility conditions. One headline about Anthropic is unrelated to the ETF and was discarded._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **Goldman watching for 3 conditions that could support a stock correction bottom - Seeking Alpha** _(Source: Seeking Alpha)_
   Market commentary on conditions that could help a correction bottom in equities, relevant as broad SPY context.
2. **This VIX Signal Is Bullish For The S&P 500. - Investor's Business Daily** _(Source: Investor's Business Daily)_
   Discusses a VIX-based signal for the S&P 500, which can affect broad index sentiment and volatility for SPY.

---

## 7. Risk Watchlist

* Watch whether the next reprice stays well explained by the model or whether a larger residual emerges from higher-order convexity and surface effects.
* Monitor the broad volatility backdrop and implied volatility behavior, since that is the main mechanism behind the contract’s one-day repricing.
* **Assignment watch**: ex-div `2026-12-17` — Dividend coverage 0.23 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 6 — `SPY 725C 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 725C 2027-01-15`  
**Analysis Date**: `2026-11-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$6.0000` (+0.3%)
* **Model ΔP**: `+$6.0000`
* **Primary drivers**: **Vega PnL** (+50.5%) and **Delta PnL** (-38.8%) and **Theta decay** (-9.4%).
* **Verdict**: The option move was dominated by a revaluation of implied volatility, with spot down modestly and delta and theta offsetting part of the gain. The residual is small relative to the modeled move, so the run is mostly a clean Vega-led repricing rather than a path or boundary anomaly. No relevant headlines were retrieved, and the catalyst layer is intentionally empty here, so there is no separate news mechanism to add.
* **Confidence**: **Medium** — The attribution is supported by the engine output and the observation is reliable, but the residual band is high and the surface diagnostics are only a reference because local vol was deferred. With no retrieved headlines and no required Layer B mechanism, confidence stays medium rather than high.

---

## 2. Observation Lock

* **As-of**: `2026-11-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.8%)
* **IV move**: +1.20 vol pts vs noise band ±0.08 pts (exceeds noise band)
* **Prior observation**: `2026-11-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$6.0000`
* **Model ΔP (engine)**: `+$6.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$7.6834`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.6834` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (28.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$101.1836` | -38.8% | Stock moved from $718.78 to $716.70 (-2.0800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.6113` | +0.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$131.6912` | +50.5% | IV moved +1.22 vol pts (19.76% → 20.98%) |
| **Theta decay (Δt · Theta)** | `-$24.4355` | -9.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.6834` | -0.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$6.0000** | **+2.3%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.6834` (28.1% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.2101` | other second-order: `+$0.0091`
* Combined: `-$0.2010` | Residual after: `-$1.4824`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$24.4505`
* **spot**: `-$99.3608`
* **vol**: `+$129.7805`
* **rate**: `-$0.5797`
* Step sum: `+$5.3895` | Model ΔP: `+$6.0000` | Audit residual: `+$0.6105`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Higher-order convexity and Taylor truncation can still affect the residual, even though it is small in this run.
* No relevant catalyst or borrow/IV-crush tape was retrieved; keep watching for any later surface move or quote-quality shift that would change the Vega read.
* **Assignment watch**: ex-div `2026-12-17` — Dividend coverage 0.10 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 7 — `VZ 42C 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 42C 2027-01-15`  
**Analysis Date**: `2026-11-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$60.0000` (+10.8%)
* **Model ΔP**: `+$60.0000`
* **Primary drivers**: **Vega PnL** (+63.2%) and **Delta PnL** (+18.3%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is primarily explained by the option’s sensitivity to a sharp rise in implied volatility, with a smaller supporting contribution from the modest uptick in the underlying and a minor theta drag. The remaining gap is consistent with higher-order effects and revaluation path dependence rather than a separate headline catalyst, since no relevant news was retrieved and the observation lock limits tape-based confirmation. This is an American contract, but the dividend does not appear to create a material early-exercise story here. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is moderate because the dominant factor and vol move are clear, but observation is unreliable, the residual band is high, and there were no retrieved headlines to validate a catalyst layer. The engine notes also point to surface limitations, so some of the unexplained move may reflect higher-order revaluation effects rather than a clean single-Greek story.

---

## 2. Observation Lock

* **As-of**: `2026-11-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 24.4%)
* **IV move**: +18.70 vol pts vs noise band ±16.93 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$60.0000`
* **Model ΔP (engine)**: `+$60.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$47.7007`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$12.2993` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (20.5%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$10.9523` | +18.3% | Stock moved from $47.16 to $47.28 (+0.1200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0265` | +0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$37.8967` | +63.2% | IV moved +13.90 vol pts (25.87% → 39.77%) |
| **Theta decay (Δt · Theta)** | `-$1.1746` | -2.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$12.2993` | +20.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$60.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$12.2993` (20.5% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.9770` | Volga PnL: `+$9.8821`
* Combined: `+$8.9052` | Residual after: `+$3.3941`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$1.1759`
* **spot**: `+$11.0031`
* **vol**: `+$50.1648`
* **rate**: `-$0.0511`
* Step sum: `+$59.9410` | Model ΔP: `+$60.0000` | Audit residual: `+$0.0590`

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
* Watch whether the residual stays elevated, since higher-order convexity and full-surface revaluation can matter when spot and implied volatility both reprice together.
* No named catalyst or microstructure mechanism was retrieved, so there is no basis here to add an IV crush, borrow, or squeeze narrative.
* The contract should remain a carry/theta case rather than an early-exercise case unless the dividend or ex-div setup changes materially.
* **Assignment watch**: ex-div `2027-01-07` — Dividend coverage 0.81 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$1.0000` (+100.0%)
* **Model ΔP**: `+$1.0000`
* **Primary drivers**: **Delta PnL** (+64.8%) and **Vega PnL** (+26.5%) and **Gamma PnL** (+14.3%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is primarily explained by the stock rally feeding through the option's delta, with gamma adding some convexity as the underlying lifted. Vega also contributed because implied volatility rose, but the run is still anchored in the spot move rather than a tape event. The residual is modest and consistent with higher-order effects and path reprice noise, while the named headlines only provide background context for a stock-specific turnaround narrative. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is limited because observation is not reliable, the IV narrative is suppressed by the data tags, and the feed flags a medium residual with large spot and volatility moves. The headlines name the issuer and a turnaround framing, but they do not supply an allow-listed mechanism, so they support context rather than a precise catalyst diagnosis.

---

## 2. Observation Lock

* **As-of**: `2026-11-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: +65.62 vol pts vs noise band ±79.43 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$1.0000`
* **Model ΔP (engine)**: `+$1.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.9258`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0742` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (7.4%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.6482` | +64.8% | Stock moved from $0.93 to $1.07 (+0.1400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1431` | +14.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.2647` | +26.5% | IV moved +11.45 vol pts (278.51% → 289.96%) |
| **Theta decay (Δt · Theta)** | `-$0.1303` | -13.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0742` | +7.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$1.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0742` (7.4% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.1008` | Volga PnL: `+$0.0188`
* Combined: `+$0.1196` | Residual after: `-$0.0454`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.1302`
* **spot**: `+$0.7246`
* **vol**: `+$0.4056`
* **rate**: `-$0.0000`
* Step sum: `+$1.0000` | Model ΔP: `+$1.0000` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Observation lock on the option tape: headlines below are context for the **spot move** only, not for the IV change or the residual._

_Intel note: Both headlines are directly about Plug Power (PLUG) and frame the name around a price move and turnaround narrative. No allow-listed mechanism is explicitly stated in either headline._

_Observation lock: searched only for the catalyst of the spot move; option-tape cues (IV, residual, 8-K) stay off._
_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Plug Power (PLUG) Stock Is Up 12.2% Today Without Company News** _(Source: Yahoo Finance)_
   The headline is about Plug Power and notes a same-day move without citing any new company-specific announcement.
2. **PLUG Stock: Can Falling Cash Burn and New Deals Fuel a Turnaround?** _(Source: MarketBeat)_
   The headline discusses Plug Power’s operating outlook, focusing on cash burn and new deals as part of a turnaround narrative.

---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Higher-order convexity and path effects can still distort the reference Greek split when the underlying move is large, so the residual should be treated as a modeling artifact rather than a separate story.
* Watch whether the issuer-specific turnaround narrative persists in the tape, but do not force a borrow, squeeze, or IV-crush interpretation because no qualifying headline mechanism is present.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0699 | level_proxy(t) = 0.2546
* Δskew = -0.0019 | Δlevel = +0.0110
* Put 655 delta=-0.1853 | Call 725 delta=0.4733
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
