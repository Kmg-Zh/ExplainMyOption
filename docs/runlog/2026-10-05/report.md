# Live book run — 2026-10-05

Run `2026-10-05-1791250491`. 7/8 legs completed, 1 failed. `legs_narrated=5` `legs_silent=2` `llm_calls=8`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-05` | **Positions**: 7 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$21.5000`
* **Total Model PnL**: `+$21.5000`
* **Aggregate model vs mark gap**: `-$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `SPY 795C 2026-11-20` | `+$127.5000` |
| 2 | `AAPL 325C 2026-11-20` | `-$82.5000` |
| 3 | `SPY 715P 2026-11-20` | `+$58.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$151.7841` |
| Gamma | `+$7.9375` |
| Vega | `+$2.7818` |
| Theta | `-$136.7602` |
| Residual | `-$4.2433` |

### Notable underlyings

* **SPY**: `+$185.5000` aggregate option PnL
* **AAPL**: `-$82.5000` aggregate option PnL
* **JPM**: `-$67.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$82.5000` (-441.8%)
* **Model ΔP**: `-$82.5000`
* **Primary drivers**: **Delta PnL** (46%) and **Theta decay** (40%) and **Vega PnL** (12%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-10-05` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 7.8%)
* **IV move**: +0.18 vol pts vs noise band ±1.57 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-02`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$82.5000`
* **Model ΔP (engine)**: `-$82.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$81.6075`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.8925` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$51.3184` | +62.2% | Stock moved from $333.69 to $332.89 (-0.8000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.3622` | -0.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$13.7483` | -16.7% | IV moved +0.30 vol pts (30.44% → 30.62%) |
| **Theta decay (Δt · Theta)** | `-$44.3997` | +53.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.8925` | +1.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$82.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.8925` (1.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0008`
* Combined: `+$0.0008` | Residual after: `-$0.8258`

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
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-10-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$32.5000` (->1000%)
* **Model ΔP**: `-$32.5000`
* **Primary drivers**: **Theta decay** (77%) and **Vega PnL** (20%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is dominated by time decay in the model: with spot essentially unchanged, the option lost value primarily as expiry approached, and the small positive vol contribution did not offset that decay. The remaining gap is a minor model residual, consistent with normal Taylor truncation or quote noise rather than a separate named catalyst. No headline evidence or microstructure tag is available here, so the run reads as a carry/theta explanation rather than a news-driven reprice. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is limited by the observation lock and the lack of retrieved headlines, so there is no Layer B catalyst to confirm. The attribution is otherwise internally coherent: spot was flat, the dominant modeled factor was theta, and the residual is small relative to the model move.

---

## 2. Observation Lock

* **As-of**: `2026-10-05` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 20.2%)
* **IV move**: +0.79 vol pts vs noise band ±0.94 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-02`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$32.5000`
* **Model ΔP (engine)**: `-$32.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$31.0735`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.4265` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.4%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.0000` | -0.0% | Stock moved from $332.38 to $332.38 (+0.0000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0000` | -0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$10.7614` | -33.1% | IV moved +0.49 vol pts (25.03% → 25.82%) |
| **Theta decay (Δt · Theta)** | `-$41.8349` | +128.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.4265` | +4.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$32.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.4265` (4.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0008`
* Combined: `+$0.0008` | Residual after: `-$0.3258`

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
* Check whether the remaining move stays consistent with simple time decay versus higher-order truncation as expiry gets closer.
* Because there are no relevant headlines or microstructure tags, avoid forcing a borrow, squeeze, or IV-crush interpretation without new tape evidence.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.84 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-10-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$35.0000` (-165.9%)
* **Model ΔP**: `-$35.0000`
* **Primary drivers**: **Theta decay** (89%) and **Vega PnL** (9%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-10-05` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 14.9%)
* **IV move**: +3.73 vol pts vs noise band ±7.91 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-02`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$35.0000`
* **Model ΔP (engine)**: `-$35.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$34.2314`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.7686` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.2%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.0000` | +0.0% | Stock moved from $332.38 to $332.38 (+0.0000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0000` | -0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$4.0913` | -11.7% | IV moved +0.18 vol pts (33.97% → 37.70%) |
| **Theta decay (Δt · Theta)** | `-$38.3227` | +109.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.7686` | +2.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$35.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.7686` (2.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0001`
* Combined: `+$0.0001` | Residual after: `-$0.3501`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$0.0000` vs next cash dividend `+$1.5000` (gap `+$1.5000`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$20.7500` vs `+$19.6551` (gap `+$1.0949`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.1598` — material
* **Dividend PV effect** (European, same divs − no divs): `+$0.9346`
* **Dividend coverage** (dividend / time value): `0.48` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.0409`
* **Residual (Taylor ε)**: `-$0.0077`
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
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.48 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 4 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$58.0000` (+>1000%)
* **Model ΔP**: `+$58.0000`
* **Primary drivers**: **Delta PnL** (47%) and **Vega PnL** (25%) and **Theta decay** (23%).
* **Verdict**: The move is best explained by the put’s directional sensitivity to the higher underlying level, with gamma and theta secondary and vega offsetting part of the revaluation. The residual is small, so the Taylor breakdown is broadly consistent with the engine repricing rather than pointing to a separate catalyst. No relevant headlines were retrieved, so there is no Layer B mechanism to add beyond the modeled spot-driven move.
* **Confidence**: **Medium** — Confidence is tempered by the small spot move band and the fact that the position is still close enough to the money for second-order and carry effects to matter. The feed is reliable and the residual is low, but the diagnostic has no news corroboration and the observed IV change should be treated as part of the model revaluation rather than a standalone catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-10-05` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.7%)
* **IV move**: +0.65 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-10-02`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$58.0000`
* **Model ΔP (engine)**: `+$58.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$55.9086`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$2.0914` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$64.6141` | +111.4% | Stock moved from $769.64 to $774.83 (+5.1900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$5.2150` | -9.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$34.6274` | -59.7% | IV moved +0.60 vol pts (18.24% → 18.89%) |
| **Theta decay (Δt · Theta)** | `+$31.1369` | +53.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$2.0914` | +3.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$58.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$2.0914` (3.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0287`
* Combined: `-$0.0287` | Residual after: `-$0.5513`

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

* Watch whether the next repricing remains stable under a full-surface revaluation, since truncation and American boundary effects can still distort a Taylor read.
* No Layer B catalyst is supported here; if the tape later shows borrow, squeeze, or implied volatility stress, verify it against actual headlines rather than the model line.

---

### Position 5 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$127.5000` (+>1000%)
* **Model ΔP**: `+$127.5000`
* **Primary drivers**: **Delta PnL** (66%) and **Theta decay** (19%) and **Vega PnL** (8%).
* **Verdict**: The move is primarily explained by the option’s positive delta responding to a modest rise in the underlying, with gamma adding some convexity support and theta working against the gain. Residuals are small, so the Taylor decomposition is largely clean and there is no need to lean on a separate catalyst story. The American premium is negligible, so early exercise is not a material part of the diagnosis.
* **Confidence**: **Medium** — Confidence is supported by reliable observation, high attribution coverage, and a low residual band. The main limitation is that the spot move is only modest and there were no retrieved headlines, so the explanation should stay at the factor level rather than infer a news catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-10-05` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.6%)
* **IV move**: +0.22 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-10-02`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$127.5000`
* **Model ΔP (engine)**: `+$127.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$130.8213`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$3.3213` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$142.5078` | +111.8% | Stock moved from $769.64 to $774.83 (+5.1900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$12.7660` | +10.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$16.5399` | +13.0% | IV moved +0.18 vol pts (13.35% → 13.57%) |
| **Theta decay (Δt · Theta)** | `-$40.9924` | -32.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$3.3213` | -2.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$127.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$3.3213` (2.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0120`
* Combined: `+$0.0120` | Residual after: `+$1.2630`

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

* Taylor truncation does not appear to be a major distortion here, but the desk should still treat the attribution as a model reprice rather than a full mark-to-market.
* Watch for any future quote or surface changes that could alter the delta-led profile; no borrow, squeeze, or IV-crush mechanism is evidenced in the current tape.

---

### Position 6 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-06` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$14.0000` (-717.9%)
* **Model ΔP**: `-$14.0000`
* **Primary drivers**: **Vega PnL** (56%) and **Delta PnL** (28%) and **Theta decay** (16%).
* **Verdict**: The position’s move was driven mainly by a drop in implied volatility, with spot only a minor secondary input and theta adding carry drag. The residual is small, so the Taylor breakdown is behaving cleanly; there is no separate catalyst story to layer on from headlines because none were retrieved. The American-versus-European gap is not material, so this is not an early-exercise case.
* **Confidence**: **Medium** — The attribution is internally consistent and observation quality is reliable, but the news layer is empty and the market feed was incomplete enough that the diagnosis should stay at the factor level. The residual is low, which supports the vega-led read, while the small spot move and carry effects are clearly secondary.

---

## 2. Observation Lock

* **As-of**: `2026-10-06` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 14.4%)
* **IV move**: -7.05 vol pts vs noise band ±2.08 pts (exceeds noise band)
* **Prior observation**: `2026-10-05`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$14.0000`
* **Model ΔP (engine)**: `-$14.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$14.0774`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0774` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$3.9315` | +28.1% | Stock moved from $45.92 to $45.85 (-0.0700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0233` | -0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$7.9179` | +56.6% | IV moved -1.25 vol pts (30.00% → 22.95%) |
| **Theta decay (Δt · Theta)** | `-$2.2513` | +16.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0774` | -0.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$14.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0774` (0.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0001`
* Combined: `-$0.0001` | Residual after: `-$0.1399`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$0.0700` vs next cash dividend `+$0.7080` (gap `+$0.6380`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$1.8100` vs `+$2.0139` (gap `-$0.2039`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0004` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.2044`
* **Dividend coverage** (dividend / time value): `0.74` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$0.0792`
* **Residual (Taylor ε)**: `+$0.0008`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._
_News fetch failed and was skipped: tavily._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* Keep an eye on whether a full-surface reprice or higher-order convexity could widen the residual if spot or vol becomes more volatile.
* Monitor implied volatility and quote quality; with no relevant headlines, there is no separate borrow, squeeze, or liquidity mechanism to validate.
* **Assignment watch**: ex-div `2026-10-09` — Dividend coverage 0.74 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 7 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-06` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (50%) and **Theta decay** (26%) and **Delta PnL** (23%).
* **Verifier**: FAIL — hard policy violation (numeric_hallucination); the factor story is not reliable. The narrative states a number the code did not produce.
* **Verdict**: Verifier FAIL — terminal break escalation (numeric_hallucination). The narrative states a number the code did not produce.
* **Confidence**: **Low** — LLM synthesis failed — using rule-based summary. Quant sections remain engine-verified.

---

## 2. Observation Lock

* **As-of**: `2026-10-06` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: +0.00 vol pts vs noise band ±0.00 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-05`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0032`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0032` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.0879` | +23.5% | Stock moved from $1.90 to $1.89 (-0.0100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0009` | +0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.1862` | +49.8% | IV moved +1.36 vol pts (50.00% → 50.00%) |
| **Theta decay (Δt · Theta)** | `-$0.0961` | +25.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0032` | +0.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0032` (>1000% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0000`
* Combined: `+$0.0000` | Residual after: `-$0.0000`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0010`
* **spot**: `-$0.0008`
* **vol**: `+$0.0018`
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
* Verifier flags: numeric_hallucination; missing evidence: LLM prose must not contain percentage literals.
* **Terminal break**: diagnostic budget exhausted with a large unexplained residual; the story is not reliable and needs human review.
* **Quote quality**: IV move sits inside the bid-ask noise band — do not treat Vega as a falsifiable driver from this quote alone.
* **Elevated residual (>105636668%)**: Likely contributors are the American early-exercise boundary, discrete dividends, vol skew curvature, and mark quality. Model limitations flagged above.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0532 | level_proxy(t) = 0.1623
* Δskew = +0.0043 | Δlevel = +0.0044
* Put 715 delta=-0.1061 | Call 795 delta=0.3205
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **aapl_vertical_short** (AAPL): RuntimeError: No comparable observation. AAPL call was OK on t-1 and DAY_MISSING on 2026-10-05. A one-day attribution requires the same contract observed on both dates, so this run produces no attribution. This is a data coverage limitation, not an unexplained market move.
