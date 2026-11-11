# Live book run — 2026-11-10

Run `2026-11-10-1794363389`. 8/8 legs diagnosed, 0 settled at expiry, 0 failed. `legs_narrated=6` `legs_silent=2` `llm_calls=8`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-10` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$10.0000`
* **Total Model PnL**: `-$10.0000`
* **Aggregate model vs mark gap**: `-$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `-$200.0000` |
| 2 | `AAPL 350C 2026-11-20` | `+$147.5000` |
| 3 | `SPY 715P 2026-11-20` | `+$28.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$98.6155` |
| Gamma | `-$5.1092` |
| Vega | `+$94.0879` |
| Theta | `+$0.8930` |
| Residual | `-$1.2561` |

### Notable underlyings

* **AAPL**: `-$52.5000` aggregate option PnL
* **SPY**: `+$22.0000` aggregate option PnL
* **VZ**: `+$15.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-10` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$200.0000` (-7.5%)
* **Model ΔP**: `-$200.0000`
* **Primary drivers**: **Delta PnL** (-99.0%) and **Theta decay** (-9.3%) and **Vega PnL** (+7.9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position’s modeled change is led by directional exposure: the call moved mainly with the lower share price, with gamma only softening the move and theta adding carry drag. The residual is small, so the Taylor view is broadly consistent with the full revaluation. There is no separate headline catalyst to layer in, and the American premium is not material, so this reads as a carry-and-direction case rather than an early-exercise story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is capped by the observation lock and the absence of retrieved headlines, so there is no independent catalyst check. The residual is small and the dominant driver is clear, but the surface notes and reliability flags argue for a coarser attribution rather than a more granular narrative.

---

## 2. Observation Lock

* **As-of**: `2026-11-10` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.1%)
* **IV move**: +1.42 vol pts vs noise band ±5.75 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$200.0000`
* **Model ΔP (engine)**: `-$200.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$198.7418`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.2582` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$198.0206` | -99.0% | Stock moved from $350.69 to $348.51 (-2.1800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.8976` | +0.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$15.8917` | +7.9% | IV moved +1.59 vol pts (33.88% → 35.47%) |
| **Theta decay (Δt · Theta)** | `-$18.5104` | -9.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.2582` | -0.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$200.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.2582` (0.6% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$2.3650`
* Combined: `+$2.3650` | Residual after: `-$3.6233`

### Ex-div attribution overlay (official PnL stays the American FDM Taylor blotter)
* **Spot drop vs dividend** (per share): spot `-$2.1800` vs next cash dividend `+$0.2700` (gap `-$1.9100`)
* **American FDM vs European analytic (no cash div, cross-check, per option)**: `+$24.7250` vs `+$24.9375` (gap `-$0.2125`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored, per option): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs, per option): `-$0.2134`
* **Dividend coverage** (dividend / time value): `0.22` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$15.8917`
* **Residual (Taylor ε)**: `-$1.2582`
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
* Watch whether a fuller revaluation continues to differ from the Taylor breakdown if spot or implied volatility become more volatile than this run suggests.
* No early-exercise adjustment is indicated here; the dividend does not cover the remaining time value, so ex-div does not create a material exercise boundary issue.
* **Assignment watch**: ex-div `2026-11-12` — Dividend coverage 0.22 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-10` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$147.5000` (-23.0%)
* **Model ΔP**: `+$147.5000`
* **Primary drivers**: **Delta PnL** (+78.5%) and **Theta decay** (+20.2%) and **Vega PnL** (+6.2%).
* **Verdict**: The move is dominated by the option's delta exposure to the underlying decline, with theta adding supportive carry and gamma only a minor offset. The residual is small, so the Taylor breakdown is coherent and there is no need to invoke a separate catalyst story; the blotter also shows no relevant headlines or microstructure tags to support one.
* **Confidence**: **Medium** — Confidence is medium because the attribution is internally consistent and the residual is small, but the move is still a model revaluation based on prior-close Greeks rather than a live mark. The blotter provides no relevant headlines, and the diagnostic brief explicitly says no Layer B mechanism is required, so there is no external catalyst to validate beyond the modeled spot-driven move.

---

## 2. Observation Lock

* **As-of**: `2026-11-10` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.0%)
* **IV move**: -0.78 vol pts vs noise band ±0.33 pts (exceeds noise band)
* **Prior observation**: `2026-11-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$147.5000`
* **Model ΔP (engine)**: `+$147.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$148.3915`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.8915` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$115.8209` | +78.5% | Stock moved from $350.69 to $348.51 (-2.1800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$6.3145` | -4.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$9.1288` | +6.2% | IV moved -0.38 vol pts (24.60% → 24.22%) |
| **Theta decay (Δt · Theta)** | `+$29.7563` | +20.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.8915` | -0.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$147.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.8915` (0.6% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.1738`
* Combined: `+$0.1738` | Residual after: `-$1.0653`

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

* Watch for any further spot gap or full-surface repricing, since the Greek decomposition is a first-order view and higher-order effects can grow if the underlying moves again.
* No Layer B catalyst was identified in the feed; keep an eye on any new company-specific headlines or market structure changes that could alter the attribution on the next run.
* **Assignment watch**: ex-div `2026-11-12` — Dividend coverage 0.05 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-10` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$17.5000` (+1.4%)
* **Model ΔP**: `+$17.5000`
* **Primary drivers**: **Vega PnL** (+190.5%) and **Theta decay** (-84.9%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-11-10` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 8.4%)
* **IV move**: +1.15 vol pts vs noise band ±1.21 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$17.5000`
* **Model ΔP (engine)**: `+$17.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$17.9245`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.4245` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.5556` | -3.2% | Stock moved from $342.08 to $342.07 (-0.0100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0001` | +0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$33.3403` | +190.5% | IV moved +0.76 vol pts (24.38% → 25.14%) |
| **Theta decay (Δt · Theta)** | `-$14.8603` | -84.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.4245` | -2.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$17.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.4245` (2.4% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.0051`
* Combined: `+$0.0051` | Residual after: `-$0.4296`

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
**Analysis Date**: `2026-11-10` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$12.5000` (-1.5%)
* **Model ΔP**: `-$12.5000`
* **Primary drivers**: **Theta decay** (-94.7%) and **Vega PnL** (-9.0%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-11-10` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 10.7%)
* **IV move**: -0.51 vol pts vs noise band ±1.04 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$12.5000`
* **Model ΔP (engine)**: `-$12.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$12.5148`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0148` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.4410` | +3.5% | Stock moved from $342.08 to $342.07 (-0.0100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0001` | +0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$1.1221` | -9.0% | IV moved -0.03 vol pts (22.33% → 22.30%) |
| **Theta decay (Δt · Theta)** | `-$11.8338` | -94.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0148` | +0.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$12.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0148` (0.1% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.0000`
* Combined: `-$0.0000` | Residual after: `+$0.0149`

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

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-10` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$28.0000` (-18.9%)
* **Model ΔP**: `+$28.0000`
* **Primary drivers**: **Vega PnL** (+117.8%) and **Delta PnL** (-98.3%) and **Theta decay** (+84.8%).
* **Verdict**: The position’s modeled gain was led by implied volatility moving lower, with spot and higher-order effects acting as smaller offsets against the short put exposure. The residual is small enough to sit comfortably inside normal Taylor truncation for a one-day revaluation. The relevant background tape supports an IV crush context, but there is no SPY-specific catalyst or control-structure event here, so the move is best read as a surface repricing rather than a news shock.
* **Confidence**: **Medium** — Confidence is medium because the attribution is internally consistent and observation quality is reliable, but the headline set is mostly generic background and not a direct SPY catalyst. The residual is low, yet the run still depends on a one-day Taylor view with some truncation and the market-feed limitations noted in the blotter.

---

## 2. Observation Lock

* **As-of**: `2026-11-10` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.5%)
* **IV move**: -1.42 vol pts vs noise band ±0.07 pts (exceeds noise band)
* **Prior observation**: `2026-11-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$28.0000`
* **Model ΔP (engine)**: `+$28.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$27.0825`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.9175` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.3%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$27.5150` | -98.3% | Stock moved from $752.69 to $749.92 (-2.7700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$2.1567` | -7.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$32.9974` | +117.8% | IV moved -1.45 vol pts (23.80% → 22.36%) |
| **Theta decay (Δt · Theta)** | `+$23.7569` | +84.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.9175` | +3.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$28.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.9175` (3.3% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$3.3975` | Volga PnL: `-$1.6267`
* Combined: `+$1.7708` | Residual after: `-$0.8533`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: Only one item is a SPY-related market-structure overview, and it is background rather than a direct issuer or control-structure story. The other headlines are generic implied-volatility education or discussion and were discarded._
_Intel triage discarded 2 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **Today's SPY, QQQ & VIX Gamma, Dealer Positioning & Regime | FlashAlpha** _(Source: FlashAlpha)_
   Market-structure overview mentioning SPY alongside QQQ and VIX gamma/dealer positioning.

---

## 7. Risk Watchlist

* Check whether the modeled reprice remains stable under a full-surface refresh versus the one-day Taylor view, since truncation can still shift the attribution at the margin.
* Watch for continued implied volatility compression and any broad market-structure readthrough that would reinforce the IV crush backdrop without requiring a stock-specific catalyst.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-10` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$6.0000` (-52.2%)
* **Model ΔP**: `-$6.0000`
* **Primary drivers**: **Delta PnL** (-78.4%) and **Theta decay** (-57.0%) and **Gamma PnL** (+14.2%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained primarily by spot drifting lower, which reduced the call’s value and dominated the day’s model revaluation. Theta also weighed on the position, while gamma and a small vol uptick softened part of the decline and left a modest method residual. There is no named catalyst in the digest, so the tape reads as a clean factor-driven repricing rather than a news-led move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is only medium because observation quality is flagged unreliable and the residual is not trivial relative to the model move. The attribution still aligns with the dominant Greek profile, and the available diagnostics do not support a separate catalyst narrative.

---

## 2. Observation Lock

* **As-of**: `2026-11-10` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 18.2%)
* **IV move**: +0.17 vol pts vs noise band ±0.16 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$6.0000`
* **Model ΔP (engine)**: `-$6.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$6.5992`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.5992` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (10.0%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$4.7044` | -78.4% | Stock moved from $752.69 to $749.92 (-2.7700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.8520` | +14.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.6734` | +11.2% | IV moved +0.12 vol pts (14.52% → 14.64%) |
| **Theta decay (Δt · Theta)** | `-$3.4202` | -57.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.5992` | +10.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$6.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.5992` (10.0% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.3111` | other second-order: `+$0.0133`
* Combined: `-$0.2978` | Residual after: `+$0.8970`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$3.4078`
* **spot**: `-$2.9393`
* **vol**: `+$0.3628`
* **rate**: `+$0.0148`
* Step sum: `-$5.9695` | Model ΔP: `-$6.0000` | Audit residual: `-$0.0305`

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
* Higher-order convexity and Taylor truncation can still distort the reference decomposition when spot moves through a thin option value zone.
* No catalyst tape was retrieved, so verify the price action against the next clean mark set before assigning any news-based explanation.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-10` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$15.5000` (+10.0%)
* **Model ΔP**: `+$15.5000`
* **Primary drivers**: **Delta PnL** (+109.3%) and **Theta decay** (-24.7%) and **Vega PnL** (+12.4%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The option’s move is primarily explained by the underlying’s higher close, with the Taylor decomposition showing delta as the main modeled contributor and gamma adding a smaller convexity boost. Theta offset some of that gain, while the residual was negligible, so the revaluation is well explained by the price move rather than by a missing model term. There are no relevant headlines or microstructure tags, so Layer B is empty and no separate catalyst story is supported. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution coverage is high and the residual is low, which makes the model story clean. Confidence is kept at medium because observation quality is flagged as unreliable and the desk notes suppress a Vega narrative, so the diagnosis should stay coarse and tied to the revaluation rather than any finer catalyst inference.

---

## 2. Observation Lock

* **As-of**: `2026-11-10` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 9.4%)
* **IV move**: +0.05 vol pts vs noise band ±3.11 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$15.5000`
* **Model ΔP (engine)**: `+$15.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$15.4997`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0003` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$16.9466` | +109.3% | Stock moved from $46.06 to $46.31 (+0.2500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.4678` | +3.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$1.9187` | +12.4% | IV moved +0.67 vol pts (30.14% → 30.81%) |
| **Theta decay (Δt · Theta)** | `-$3.8335` | -24.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0003` | +0.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$15.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0003` (0.0% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.0758`
* Combined: `-$0.0758` | Residual after: `+$0.0761`

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
* Monitor whether the move remains dominated by spot revaluation versus any later truncation or full-surface reprice as expiry approaches.
* No catalyst layer is available here; with no relevant headlines or microstructure tags, avoid inferring borrow, squeeze, or implied-volatility effects.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-10` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Vega PnL** (+44.9%) and **Delta PnL** (-36.6%) and **Theta decay** (-5.8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by a volatility revaluation, with spot weakness and second-order effects offsetting part of the repricing. However, the attribution does not fully explain the move and needs human review: the residual is still material, so this is a terminal-break case rather than a clean single-factor story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is limited because observation quality is weak, the residual remains large, and the surface diagnostics include a failed American surface check. The driver label follows the desk blotter, but the move is not fully explained by the Taylor buckets, so the gap remains unresolved.

---

## 2. Observation Lock

* **As-of**: `2026-11-10` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 120.0%)
* **IV move**: +17.19 vol pts vs noise band ±22.64 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-09`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.2138`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.2138` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$1.0284` | -36.6% | Stock moved from $1.50 to $1.37 (-0.1300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1444` | +5.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$1.2598` | +44.9% | IV moved +17.43 vol pts (175.87% → 193.30%) |
| **Theta decay (Δt · Theta)** | `-$0.1621` | -5.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.2138` | -7.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **+0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.2138` (>1000% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.3830` | Volga PnL: `+$0.1748`
* Combined: `-$0.2082` | Residual after: `-$0.0056`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.1620`
* **spot**: `-$0.8444`
* **vol**: `+$1.0065`
* **rate**: `+$0.0007`
* Step sum: `+$0.0008` | Model ΔP: `+$0.0000` | Audit residual: `-$0.0008`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%
* **Playbook records** (selected by code for the narrator): `terminal-break` (`terminal_unexplained_break`)

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Watch whether a full-surface reprice or truncation effects are distorting the modeled attribution.
* Verify the market marks and surface calibration before treating the volatility-led revaluation as complete.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0715 | level_proxy(t) = 0.1857
* Δskew = -0.0159 | Δlevel = -0.0063
* Put 715 delta=-0.0919 | Call 795 delta=0.0091
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
