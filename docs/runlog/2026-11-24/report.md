# Live book run — 2026-11-24

Run `2026-11-24-1795573027`. 7/8 legs diagnosed, 0 settled at expiry, 1 failed. `legs_narrated=6` `legs_silent=1` `llm_calls=8`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-24` | **Positions**: 7 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$31.5000`
* **Total Model PnL**: `-$31.5000`
* **Aggregate model vs mark gap**: `+$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `SPY 725C 2027-01-15` | `-$366.0000` |
| 2 | `AAPL 335C 2027-01-15` | `+$357.5000` |
| 3 | `VZ 42C 2027-01-15` | `+$60.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$136.0609` |
| Gamma | `+$15.7718` |
| Vega | `-$149.0390` |
| Theta | `-$39.5178` |
| Residual | `+$5.2241` |

### Notable underlyings

* **SPY**: `-$397.0000` aggregate option PnL
* **AAPL**: `+$357.5000` aggregate option PnL
* **VZ**: `+$60.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 335C 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 335C 2027-01-15`  
**Analysis Date**: `2026-11-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$357.5000` (+15.2%)
* **Model ΔP**: `+$357.5000`
* **Primary drivers**: **Delta PnL** (+96.7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained primarily by the stock’s upward drift, with the option’s prior-close delta doing most of the work in the model reprice. Gamma and theta are secondary within the Taylor view, while the small residual suggests the approximation was clean. With no retrieved headlines and observation locked, there is no separate Layer B catalyst to attach beyond the spot-driven revaluation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The dominant factor is clear from the blotter and the residual is small, but observation reliability is false and no relevant headlines were retrieved. Vega narrative is suppressed by the code, so the diagnosis should stay at the coarser spot-move level.

---

## 2. Observation Lock

* **As-of**: `2026-11-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 6.1%)
* **IV move**: +1.37 vol pts vs noise band ±1.90 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$357.5000`
* **Model ΔP (engine)**: `+$357.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$358.3375`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.8375` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$345.5743` | +96.7% | Stock moved from $349.08 to $354.07 (+4.9900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$12.1095` | +3.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$14.9580` | +4.2% | IV moved +0.32 vol pts (27.15% → 27.47%) |
| **Theta decay (Δt · Theta)** | `-$14.3044` | -4.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.8375` | -0.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$357.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.8375` (0.2% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.6682`
* Combined: `-$0.6682` | Residual after: `-$0.1692`

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
* Watch whether a full-surface reprice or higher-order convexity becomes relevant if spot keeps moving beyond the current Taylor band.
* No Layer B catalyst was retrieved, so there is no borrow, squeeze, or IV-crush mechanism to verify from the tape.

---

### Position 2 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$29.5000` (-21.8%)
* **Model ΔP**: `-$29.5000`
* **Primary drivers**: **Vega PnL** (-95.9%) and **Theta decay** (-30.3%) and **Delta PnL** (+20.7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was mainly revalued lower because implied volatility fell, overwhelming the small benefit from the stock’s modest uptick and the limited gamma contribution. Theta also worked against the option over the day, while the residual is consistent with ordinary second-order effects and model-path differences rather than a separate catalyst. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — The blotter directly identifies vega as the dominant modeled driver, and the observation lock means the tape is not supported by a separate headline layer. Confidence is held to medium because the residual is only moderate and the run flags observation reliability limits, while the Vega narrative is also suppressed by the data-quality settings.

---

## 2. Observation Lock

* **As-of**: `2026-11-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 28.3%)
* **IV move**: -0.91 vol pts vs noise band ±0.91 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$29.5000`
* **Model ΔP (engine)**: `-$29.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$31.0179`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.5179` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (5.1%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$6.0984` | +20.7% | Stock moved from $316.66 to $317.10 (+0.4400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1083` | +0.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$28.2898` | -95.9% | IV moved -1.54 vol pts (23.84% → 22.29%) |
| **Theta decay (Δt · Theta)** | `-$8.9347` | -30.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.5179` | +5.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$29.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.5179` (5.1% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.7019` | Volga PnL: `+$1.0965`
* Combined: `+$0.3946` | Residual after: `+$1.1233`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$8.9299`
* **spot**: `+$5.9690`
* **vol**: `-$26.5296`
* **rate**: `+$0.0517`
* Step sum: `-$29.4388` | Model ΔP: `-$29.5000` | Audit residual: `-$0.0612`

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
* Watch whether the next reprice is sensitive to the local vol surface or a full-surface recalibration, since the Taylor view is only a reference under the current diagnostics.
* With no named catalyst layer retrieved, verify any new implied-vol move against fresh marks before reading it as a true volatility regime shift.

---

### Position 3 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$22.5000` (-0.9%)
* **Model ΔP**: `-$22.5000`
* **Primary drivers**: **Delta PnL** (-173.9%) and **Vega PnL** (+96.7%) and **Theta decay** (-25.6%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-11-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 9.4%)
* **IV move**: +3.42 vol pts vs noise band ±6.72 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$22.5000`
* **Model ΔP (engine)**: `-$22.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$23.0322`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.5322` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$39.1237` | -173.9% | Stock moved from $316.66 to $317.10 (+0.4400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1106` | +0.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$21.7474` | +96.7% | IV moved +1.41 vol pts (22.14% → 23.55%) |
| **Theta decay (Δt · Theta)** | `-$5.7665` | -25.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.5322` | +2.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$22.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.5322` (2.4% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.6786` | Volga PnL: `+$1.0218`
* Combined: `+$1.7004` | Residual after: `-$1.1682`

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

### Position 4 — `SPY 655P 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 655P 2027-01-15`  
**Analysis Date**: `2026-11-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$31.0000` (+4.3%)
* **Model ΔP**: `-$31.0000`
* **Primary drivers**: **Delta PnL** (-186.2%) and **Theta decay** (+55.2%) and **Vega PnL** (+34.6%).
* **Verdict**: The position’s one-day move is explained primarily by the drop in spot, with the modeled loss concentrated in the delta bucket and only minor help from gamma. The offset from theta and the small residual leave this as a clean spot-led revaluation rather than a broader volatility or microstructure story. Early exercise is not the issue here; the dividend does not cover the remaining time value, so this remains a carry and decay case for an American put.
* **Confidence**: **Medium** — The attribution coverage is high and the residual is small, so the model story is fairly clean. Confidence is capped at medium because the move is still a close-to-close revaluation and the feed notes local vol was deferred to mark calibration, but there are no relevant headlines or catalyst tags to support a Layer B overlay.

---

## 2. Observation Lock

* **As-of**: `2026-11-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.9%)
* **IV move**: -0.15 vol pts vs noise band ±0.05 pts (exceeds noise band)
* **Prior observation**: `2026-11-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$31.0000`
* **Model ΔP (engine)**: `-$31.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$31.8219`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.8219` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$57.7188` | -186.2% | Stock moved from $722.29 to $718.78 (-3.5099) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$1.9532` | -6.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$10.7273` | +34.6% | IV moved -0.16 vol pts (28.60% → 28.44%) |
| **Theta decay (Δt · Theta)** | `+$17.1228` | +55.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.8219` | +2.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$31.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.8219` (2.7% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.4199` | other second-order: `-$0.0262`
* Combined: `+$0.3937` | Residual after: `+$0.4282`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Watch whether further spot movement continues to dominate the revaluation, since the modeled attribution is still mostly first-order spot exposure.
* Monitor carry and decay around the dividend and time value; there is no material early-exercise premium to frame this as an assignment-driven event.
* **Assignment watch**: ex-div `2026-12-17` — Dividend coverage 0.25 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 5 — `SPY 725C 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 725C 2027-01-15`  
**Analysis Date**: `2026-11-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$366.0000` (-15.8%)
* **Model ΔP**: `-$366.0000`
* **Primary drivers**: **Delta PnL** (-49.4%) and **Vega PnL** (-45.4%) and **Theta decay** (-7.1%).
* **Verdict**: The position was driven primarily by the lower close in SPY, which reduced the call’s intrinsic sensitivity on the day. Vega also weighed on the mark as implied volatility eased, while theta was a smaller additional drag; gamma was too small to offset the move. The residual is minimal, so the Greek-based attribution is clean and there is no need to lean on a separate event explanation.
* **Confidence**: **Medium** — The feed is reliable and the residual is low, but the move is only a small spot decline with a concurrent volatility fade, so the attribution is straightforward rather than highly distinctive. The headline set is broad market context for SPY and does not supply a ticker-specific catalyst, so Layer B remains background only.

---

## 2. Observation Lock

* **As-of**: `2026-11-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.5%)
* **IV move**: -1.60 vol pts vs noise band ±0.05 pts (exceeds noise band)
* **Prior observation**: `2026-11-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$366.0000`
* **Model ΔP (engine)**: `-$366.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$368.6422`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$2.6422` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$180.6485` | -49.4% | Stock moved from $722.29 to $718.78 (-3.5099) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$4.2010` | +1.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$166.0619` | -45.4% | IV moved -1.52 vol pts (21.27% → 19.75%) |
| **Theta decay (Δt · Theta)** | `-$26.1328` | -7.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$2.6422` | +0.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$366.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$2.6422` (0.7% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.1052`
* Combined: `-$0.1052` | Residual after: `+$2.7473`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Intel note: Two headlines are broad market context for SPY, centered on correction-bottom conditions and a VIX-based bullish signal for the S&P 500. One Anthropic story is unrelated and discarded._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **Goldman watching for 3 conditions that could support a stock correction bottom - Seeking Alpha** _(Source: Seeking Alpha)_
   A market-structure commentary piece on conditions that could support a broader equity correction bottom.
2. **This VIX Signal Is Bullish For The S&P 500. - Investor's Business Daily** _(Source: Investor's Business Daily)_
   A volatility-signal article about the S&P 500 that can serve as broad market background for SPY.

---

## 7. Risk Watchlist

* The cleanest risk to recheck is whether the full revaluation stays close to the Greek decomposition if spot or implied volatility move more sharply than today.
* Monitor whether broad-market volatility tone remains consistent with the SPY backdrop; the headlines are context, not a separate single-name catalyst.
* **Assignment watch**: ex-div `2026-12-17` — Dividend coverage 0.10 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 6 — `VZ 42C 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 42C 2027-01-15`  
**Analysis Date**: `2026-11-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$60.0000` (+12.1%)
* **Model ΔP**: `+$60.0000`
* **Primary drivers**: **Delta PnL** (+103.6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move was dominated by the stock’s upward drift, which the option’s prior-close delta translated into the main source of the revaluation. Gamma added a small convexity boost, while the vol and decay lines were secondary drags; the remaining gap is consistent with ordinary Taylor truncation on a modest spot move. Early exercise is still economically relevant here, but it is a valuation feature of the contract rather than a separate catalyst for the day’s move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is well covered by the modeled Greeks and the residual is small, but observation quality is flagged as unreliable and there were no headlines to cross-check a catalyst. Vega narrative is suppressed by the run settings, so the interpretation should stay at the coarse factor level.

---

## 2. Observation Lock

* **As-of**: `2026-11-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 10.8%)
* **IV move**: +1.93 vol pts vs noise band ±11.02 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$60.0000`
* **Model ΔP (engine)**: `+$60.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$59.4044`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.5956` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$62.1500` | +103.6% | Stock moved from $46.45 to $47.16 (+0.7100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.1703` | +2.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$2.5389` | -4.2% | IV moved -0.72 vol pts (26.57% → 25.85%) |
| **Theta decay (Δt · Theta)** | `-$1.3770` | -2.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.5956` | +1.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$60.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.5956` (1.0% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.3388`
* Combined: `+$0.3388` | Residual after: `+$0.2569`

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
* Watch whether the full revaluation continues to line up with the delta-led move if spot keeps drifting, since higher-order effects can still matter around the strike.
* Keep the American exercise boundary in view because the dividend cover makes early exercise economically relevant even though it is not the day’s driver.
* **Assignment watch**: ex-div `2027-01-07` — Dividend coverage 1.82 (dividend $0.7080 vs time value $0.3900); ex-div is 44d out, expiry 52d out — early exercise is economically relevant.

---

### Position 7 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Vega PnL** (+47.2%) and **Delta PnL** (-30.5%) and **Theta decay** (-14.1%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by the volatility revaluation in the desk decomposition, with spot weakness and theta decay offsetting part of that lift. Because the observation is flagged unreliable and the Vega narrative is suppressed, the clean read is a full model repricing driven by the large IV shift rather than a confidence-heavy causal story. There are no relevant headlines or named microstructure mechanisms in the feed, so Layer B stays limited to the market inputs already in the blotter. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Low** — Confidence is low because the observation is unreliable, the Vega narrative is explicitly suppressed, and there are no retrieved headlines to validate a catalyst. The residual is also elevated enough that higher-order effects may be distorting the Taylor split, so the factor mix should be treated as reference-level attribution rather than a precise economic explanation.

---

## 2. Observation Lock

* **As-of**: `2026-11-24` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: +12.50 vol pts vs noise band ±21.62 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000`
* **Explained ΔP (Taylor ex-residual)**: `+$0.0482`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0482` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.2708` | -30.5% | Stock moved from $0.99 to $0.93 (-0.0600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0252` | +2.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.4189` | +47.2% | IV moved +17.02 vol pts (261.49% → 278.51%) |
| **Theta decay (Δt · Theta)** | `-$0.1252` | -14.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0482` | -5.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **+0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0482` (>1000% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.0692` | Volga PnL: `+$0.0481`
* Combined: `-$0.0211` | Residual after: `-$0.0271`

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
* Taylor truncation and higher-order convexity can distort the factor split when spot and vol both move materially; treat the decomposition as reference only.
* Verify any later tape for a true implied-vol repricing versus a transient quote effect, since no catalyst or borrow-related mechanism was supplied here.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0718 | level_proxy(t) = 0.2436
* Δskew = +0.0145 | Δlevel = -0.0087
* Put 655 delta=-0.1729 | Call 725 delta=0.4865
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **aapl_vertical_short** (AAPL): RuntimeError: No comparable observation. AAPL call was OK on t-1 and DAY_MISSING on 2026-11-24. A one-day attribution requires the same contract observed on both dates, so this run produces no attribution. This is a data coverage limitation, not an unexplained market move.
