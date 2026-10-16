# Live book run — 2026-10-15

Run `2026-10-15-1792113307`. 8/8 legs completed, 0 failed. `legs_narrated=5` `legs_silent=3` `llm_calls=6`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-15` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$3.0000`
* **Total Model PnL**: `-$3.0000`
* **Aggregate model vs mark gap**: `-$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `-$90.0000` |
| 2 | `AAPL 350C 2026-11-20` | `+$45.0000` |
| 3 | `SPY 715P 2026-11-20` | `+$44.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$21.8425` |
| Gamma | `+$1.4999` |
| Vega | `-$0.0394` |
| Theta | `-$25.4384` |
| Residual | `-$0.8645` |

### Notable underlyings

* **SPY**: `+$82.0000` aggregate option PnL
* **AAPL**: `-$45.0000` aggregate option PnL
* **JPM**: `-$44.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-15` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$90.0000` (-377.4%)
* **Model ΔP**: `-$90.0000`
* **Primary drivers**: **Delta PnL** (79%) and **Theta decay** (18%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-10-15` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.7%)
* **IV move**: -0.68 vol pts vs noise band ±1.88 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-14`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$90.0000`
* **Model ΔP (engine)**: `-$90.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$89.7997`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.2003` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$72.0900` | +80.1% | Stock moved from $342.96 to $342.00 (-0.9600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.4718` | -0.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$2.2165` | +2.5% | IV moved -0.06 vol pts (32.82% → 32.14%) |
| **Theta decay (Δt · Theta)** | `-$15.9650` | +17.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.2003` | +0.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$90.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.2003` (0.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0003`
* Combined: `-$0.0003` | Residual after: `-$0.8997`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$0.9600` vs next cash dividend `+$0.2700` (gap `-$0.6900`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$22.9500` vs `+$23.0639` (gap `-$0.1139`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1147`
* **Dividend coverage** (dividend / time value): `0.05` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$0.0222`
* **Residual (Taylor ε)**: `-$0.0020`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_Observation unreliable — event linkage suppressed; reconcile marks before catalyst stories._


---

## 7. Risk Watchlist

* No action needed; move is within theta/carry tolerance.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.05 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-15` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$45.0000` (+538.9%)
* **Model ΔP**: `+$45.0000`
* **Primary drivers**: **Delta PnL** (59%) and **Theta decay** (23%) and **Vega PnL** (17%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven primarily by the small downside move in the underlying, with gamma and theta acting as secondary offsets in the model. The vol uptick was modest and, with vega narrative suppressed and no relevant headlines, this looks like a straightforward revaluation dominated by spot rather than a separate catalyst. The American/European cross-check shows no material early-exercise effect, so the move is best read as a carry-and-spot story inside the FDM engine. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is internally coherent and the residual is small, but observation reliability is marked false and the market feed is incomplete enough to keep the diagnosis at medium confidence. There are no retrieved headlines or named microstructure mechanisms to support a separate Layer B explanation, and the early-exercise premium is negligible.

---

## 2. Observation Lock

* **As-of**: `2026-10-15` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.8%)
* **IV move**: +0.24 vol pts vs noise band ±0.36 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-14`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$45.0000`
* **Model ΔP (engine)**: `+$45.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$44.9036`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0964` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$41.4502` | +92.1% | Stock moved from $342.96 to $342.00 (-0.9600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.6603` | -1.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$12.1200` | -26.9% | IV moved +0.28 vol pts (26.56% → 26.80%) |
| **Theta decay (Δt · Theta)** | `+$16.2338` | +36.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0964` | +0.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$45.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0964` (0.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0007`
* Combined: `-$0.0007` | Residual after: `-$0.4493`

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
* Check whether the small residual remains contained if the same engine is rerun against a fuller mark set; higher-order truncation is not a major issue here, but quote quality still matters.
* Monitor the spot path and implied volatility input for any later re-mark, since the current move is mainly a delta-led revaluation with only modest vol influence.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-10-15` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$27.0000` (->1000%)
* **Model ΔP**: `-$27.0000`
* **Primary drivers**: **Vega PnL** (49%) and **Theta decay** (36%) and **Delta PnL** (8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven primarily by a revaluation lower in implied volatility, with theta decay as the other major modeled drag; the small spot uptick helped, but not enough to offset those effects. The residual is consistent with higher-order effects and path dependence around the full revaluation, while the early-exercise premium is negligible so American exercise does not change the diagnosis. No named catalyst was retrieved, and the observation lock means the tape should be treated as a model reprice rather than a news-led move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by incomplete market observation and the medium residual band, which leaves room for truncation and surface effects around the model reprice. The IV source comes from the prior chain, but the blotter still supports a clean Vega-led attribution and does not require a borrow, squeeze, or early-exercise explanation.

---

## 2. Observation Lock

* **As-of**: `2026-10-15` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 32.3%)
* **IV move**: -2.05 vol pts vs noise band ±0.89 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-14`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$27.0000`
* **Model ΔP (engine)**: `-$27.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$29.8074`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$2.8074` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (10.4%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$3.1019` | -11.5% | Stock moved from $335.28 to $335.53 (+0.2500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0527` | -0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$19.1186` | +70.8% | IV moved -1.77 vol pts (24.37% → 22.32%) |
| **Theta decay (Δt · Theta)** | `-$13.8434` | +51.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$2.8074` | -10.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$27.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$2.8074` (10.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0048`
* Combined: `+$0.0048` | Residual after: `-$0.2748`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1384`
* **spot**: `+$0.0279`
* **vol**: `-$0.1595`
* **rate**: `+$0.0000`
* Step sum: `-$0.2700` | Model ΔP: `-$0.2700` | Audit residual: `-$0.0000`

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
* Higher-order convexity and Taylor truncation can still distort the residual when the full engine reprice differs from the Greek bucket.
* Verify whether the implied volatility move is part of a broader surface reset rather than a single-point quote wobble.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-10-15` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$17.5000` (-115.5%)
* **Model ΔP**: `-$17.5000`
* **Primary drivers**: **Delta PnL** (46%) and **Vega PnL** (32%) and **Theta decay** (19%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-10-15` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 13.0%)
* **IV move**: +4.47 vol pts vs noise band ±10.53 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-14`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$17.5000`
* **Model ΔP (engine)**: `-$17.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$16.2501`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.2499` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (7.1%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$22.4844` | +128.5% | Stock moved from $335.28 to $335.53 (+0.2500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0521` | -0.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$15.7463` | -90.0% | IV moved +1.71 vol pts (26.22% → 30.69%) |
| **Theta decay (Δt · Theta)** | `-$9.5641` | +54.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.2499` | +7.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$17.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.2499` (7.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0119`
* Combined: `+$0.0119` | Residual after: `-$0.1869`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0956`
* **spot**: `-$0.2278`
* **vol**: `+$0.1484`
* **rate**: `-$0.0001`
* Step sum: `-$0.1751` | Model ΔP: `-$0.1750` | Audit residual: `+$0.0001`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
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
**Analysis Date**: `2026-10-15` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$44.5000` (+>1000%)
* **Model ΔP**: `+$44.5000`
* **Primary drivers**: **Delta PnL** (51%) and **Theta decay** (25%) and **Vega PnL** (19%).
* **Verdict**: The option’s one-day move was dominated by the modeled delta response to a small upward spot move, with theta decay and a smaller vega contribution also supporting the repricing. The residual is low, so the Taylor decomposition is broadly aligned with the full engine revaluation and does not require a separate catalyst story. Early-exercise effects are present but negligible, so the move reads as a routine American-option repricing rather than a dividend-driven boundary shift.
* **Confidence**: **Medium** — Confidence is medium because the dominant driver is clearly identified and the residual band is low, but the market move and IV change are both small and there are no relevant headlines to anchor an external catalyst. The feed is reliable and the IV source is the prior chain, so the vega line is usable, while the early-exercise premium is too small to be a meaningful explanation.

---

## 2. Observation Lock

* **As-of**: `2026-10-15` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.4%)
* **IV move**: -0.20 vol pts vs noise band ±0.01 pts (exceeds noise band)
* **Prior observation**: `2026-10-14`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$44.5000`
* **Model ΔP (engine)**: `+$44.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$45.9174`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.4174` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$24.9783` | +56.1% | Stock moved from $769.60 to $771.79 (+2.1900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.9247` | -2.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$9.5162` | +21.4% | IV moved -0.20 vol pts (19.96% → 19.76%) |
| **Theta decay (Δt · Theta)** | `+$12.3475` | +27.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.4174` | -3.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$44.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.4174` (3.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0053`
* Combined: `+$0.0053` | Residual after: `-$0.4503`

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

* Check for any Taylor truncation drift if spot or IV becomes more volatile, since the current fit is already close to the full revaluation.
* Verify upcoming dividend and carry conditions only if the price approaches the exercise boundary; the current early-exercise premium is not material.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-15` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$37.5000` (+>1000%)
* **Model ΔP**: `+$37.5000`
* **Primary drivers**: **Delta PnL** (74%) and **Theta decay** (20%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained first by spot drifting higher, which the blotter shows as the dominant modeled driver for this call. Gamma and theta helped shape the day-to-day revaluation, but they were secondary to the delta exposure; the remaining gap is small and consistent with higher-order model effects rather than a new event. With no relevant headlines retrieved and observation quality marked unreliable, there is no supported Layer B catalyst to add beyond the price-action explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is only medium because the data-quality flags say observation reliability is off and the surface calibration notes include a limitation, so the attribution should stay coarse. The residual is small, the dominant modeled driver is clear, and there are no retained news hits or catalyst mechanisms to challenge the blotter.

---

## 2. Observation Lock

* **As-of**: `2026-10-15` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.0%)
* **IV move**: +0.02 vol pts vs noise band ±0.03 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-14`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$37.5000`
* **Model ΔP (engine)**: `+$37.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$38.2823`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.7823` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$47.5646` | +126.8% | Stock moved from $769.60 to $771.79 (+2.1900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$2.4949` | +6.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.8190` | +2.2% | IV moved +0.01 vol pts (12.26% → 12.28%) |
| **Theta decay (Δt · Theta)** | `-$12.5961` | -33.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.7823` | -2.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$37.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.7823` (2.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0004`
* Combined: `+$0.0004` | Residual after: `+$0.3746`

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
* Higher-order convexity and Taylor truncation can still explain the small residual even when the delta story is dominant.
* No named catalyst or microstructure mechanism is available here; verify any later tape for fresh headlines only if they appear in the blotter.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-15` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$4.5000` (+357.1%)
* **Model ΔP**: `+$4.5000`
* **Primary drivers**: **Vega PnL** (71%) and **Theta decay** (19%) and **Delta PnL** (9%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-10-15` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.4%)
* **IV move**: +0.39 vol pts vs noise band ±0.64 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-14`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$4.5000`
* **Model ΔP (engine)**: `+$4.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$4.6042`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.1042` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.3%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.8968` | +8.6% | Stock moved from $44.42 to $44.40 (-0.0200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0020` | +0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$7.4835` | +71.5% | IV moved +1.34 vol pts (28.59% → 28.98%) |
| **Theta decay (Δt · Theta)** | `-$1.9845` | +19.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.1042` | +1.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$4.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.1042` (2.3% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0000`
* Combined: `-$0.0000` | Residual after: `+$0.0450`

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

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-15` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Delta PnL** (48%) and **Vega PnL** (32%) and **Theta decay** (14%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The option was driven first by a spot uptick, with the Taylor decomposition showing delta as the main modeled contributor and gamma only a smaller convexity add-on. That gain was offset by implied volatility drifting lower and by theta decay, while the remaining gap is best treated as truncation and revaluation noise rather than a separate catalyst story. No relevant headline set was available, so there is no Layer B event to layer onto the move; the run is a model explanation only. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by the observation lock, the lack of retrieved headlines, and the large residual band relative to the tiny model revaluation. The data still cleanly support delta as the dominant modeled driver, but the residual suggests higher-order curvature or quote noise may be material.

---

## 2. Observation Lock

* **As-of**: `2026-10-15` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 66.7%)
* **IV move**: -1.56 vol pts vs noise band ±7.27 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-14`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0142`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0142` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.2187` | +47.5% | Stock moved from $1.45 to $1.49 (+0.0400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0113` | +2.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.1493` | +32.4% | IV moved -2.20 vol pts (128.13% → 126.56%) |
| **Theta decay (Δt · Theta)** | `-$0.0666` | +14.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0142` | +3.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0142` (>1000% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0001`
* Combined: `-$0.0001` | Residual after: `+$0.0001`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0007`
* **spot**: `+$0.0022`
* **vol**: `-$0.0016`
* **rate**: `+$0.0000`
* Step sum: `+$0.0000` | Model ΔP: `+$0.0000` | Audit residual: `-$0.0000`

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
* Layer A: the close-to-close Taylor view may still be distorted by higher-order convexity and path effects, especially given the large residual band.
* Layer B: no relevant catalyst headlines were retrieved, so there is no borrow, squeeze, or IV-crush mechanism to verify from the tape.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0748 | level_proxy(t) = 0.1602
* Δskew = -0.0023 | Δlevel = -0.0009
* Put 715 delta=-0.1010 | Call 795 delta=0.2370
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
