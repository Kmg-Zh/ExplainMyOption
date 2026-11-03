# Live book run — 2026-11-02

Run `2026-11-02-1793672104`. 6/8 legs completed, 2 failed. `legs_narrated=6` `legs_silent=0` `llm_calls=9`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-02` | **Positions**: 6 | **Tickers**: AAPL, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$183.5000`
* **Total Model PnL**: `-$108.9147`
* **Aggregate model vs mark gap**: `+$74.5853`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `-$305.4147` |
| 2 | `AAPL 350C 2026-11-20` | `+$252.5000` |
| 3 | `SPY 715P 2026-11-20` | `-$50.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$338.7532` |
| Gamma | `+$38.8987` |
| Vega | `+$233.8175` |
| Theta | `+$20.8334` |
| Residual | `-$63.7111` |

### Notable underlyings

* **SPY**: `-$68.0000` aggregate option PnL
* **AAPL**: `-$52.9147` aggregate option PnL
* **VZ**: `+$11.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-02` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$380.0000` (-10.6%)
* **Model ΔP**: `-$305.4147`
* **Primary drivers**: **Delta PnL** (-110.1%) and **Vega PnL** (+35.9%) and **Theta decay** (-26.1%).
* **Verdict**: The modeled move is led by spot weakness against a high positive delta book, so the call revalued lower on the day. Gamma helped soften part of the move and the higher implied volatility offset some of the downside, but the terminal break means the attribution does not fully explain the price change and needs human review.
* **Confidence**: **Medium** — The blotter shows reliable observation quality and the dominant modeled driver is clear, but the residual is not fully explained and the playbook explicitly flags a terminal break. There are no relevant headlines to support a Layer B catalyst, and the attribution gap remains unexplained rather than tied to news.

---

## 2. Observation Lock

* **As-of**: `2026-11-02` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 8.4%)
* **IV move**: +4.49 vol pts vs noise band ±3.43 pts (exceeds noise band)
* **Prior observation**: `2026-10-30`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$380.0000`
* **Model ΔP (engine)**: `-$305.4147`
* **Model vs Mark gap**: `+$74.5853` (-24.4% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$298.1980`

* **Method residual (ε_method)**: `-$7.2167` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$74.5853` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$336.1109` | -110.1% | Stock moved from $348.91 to $344.63 (-4.2800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$7.8422` | +2.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$109.7250` | +35.9% | IV moved +4.49 vol pts (40.77% → 45.26%) |
| **Theta decay (Δt · Theta)** | `-$79.6543` | -26.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$7.2167` | -2.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$305.4147** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$7.2167` (2.4% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$9.6297` | Volga PnL: `+$3.3079`
* Combined: `+$12.9376` | Residual after: `-$20.1543`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$80.5476`
* **spot**: `-$334.0351`
* **vol**: `+$109.1930`
* **rate**: `+$0.1018`
* Step sum: `-$305.2878` | Model ΔP: `-$305.4147` | Audit residual: `-$0.1269`

### Ex-div attribution overlay (official PnL stays the American FDM Taylor blotter)
* **Spot drop vs dividend** (per share): spot `-$4.2800` vs next cash dividend `+$0.2700` (gap `-$4.0100`)
* **American FDM vs European analytic (no cash div, cross-check, per option)**: `+$25.7075` vs `+$25.8644` (gap `-$0.1569`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored, per option): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs, per option): `-$0.1578`
* **Dividend coverage** (dividend / time value): `0.04` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$109.7250`
* **Residual (Taylor ε)**: `-$7.2167`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%
  * `american_dividend_exercise_check` — path_reprice outranks ex-div window
* **Playbook records** (selected by code for the narrator): `terminal-break` (`terminal_unexplained_break`)

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* Watch whether the unexplained gap persists after a fuller review of the revaluation path and market quotes.
* Check for any hidden quote, calibration, or boundary effect before treating the modeled delta story as complete.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-02` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$252.5000` (-32.0%)
* **Model ΔP**: `+$252.5000`
* **Primary drivers**: **Delta PnL** (+84.9%) and **Theta decay** (+25.6%) and **Gamma PnL** (-7.1%).
* **Verdict**: The position’s move was driven primarily by the drop in the underlying, which reduced call value and dominated the one-day revaluation. Gamma and the small vol uptick worked against the position as secondary effects, while theta partially offset the move; the tiny residual is consistent with a clean model fit. There are no relevant headlines or named microstructure tags, so this is a factor-led repricing rather than a catalyst-led gap.
* **Confidence**: **Medium** — The engine output is internally consistent and observation quality is reliable, with a low residual and high attribution coverage. Confidence is not higher because the move is a standard model repricing rather than a headline-anchored event, and the market feed contains no relevant news to corroborate a Layer B catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-11-02` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 6.5%)
* **IV move**: +2.18 vol pts vs noise band ±0.59 pts (exceeds noise band)
* **Prior observation**: `2026-10-30`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$252.5000`
* **Model ΔP (engine)**: `+$252.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$253.2887`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.7887` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.3%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$214.3657` | +84.9% | Stock moved from $348.91 to $344.63 (-4.2800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$17.8420` | -7.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$7.8138` | -3.1% | IV moved +0.23 vol pts (24.48% → 24.72%) |
| **Theta decay (Δt · Theta)** | `+$64.5788` | +25.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.7887` | -0.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$252.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.7887` (0.3% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.0059`
* Combined: `-$0.0059` | Residual after: `-$0.7828`

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

* Watch whether the remaining move is still better explained by spot sensitivity or whether a larger residual appears on a fresh full-surface revaluation.
* No catalyst tags were retrieved, so there is no borrow, squeeze, or IV-crush narrative to verify from the tape.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.05 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-02` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$50.5000` (+18.2%)
* **Model ΔP**: `-$50.5000`
* **Primary drivers**: **Delta PnL** (-46.6%) and **Theta decay** (+19.5%) and **Vega PnL** (+15.7%).
* **Verdict**: The move is dominated by the put’s negative delta responding to the lower spot, with gamma reinforcing the directionally adverse reprice. Vega and theta partially offset that move, while the remaining gap is consistent with higher-order model effects and revaluation noise rather than a separate catalyst. Early exercise is not a material theme here because the dividend does not justify immediate exercise at current marks.
* **Confidence**: **Medium** — Confidence is moderate because the dominant driver is clearly identified, but the residual is sizable relative to the model change and the desk notes say the local-vol path was deferred to mark calibration. There are no relevant headlines or microstructure tokens to support a Layer B catalyst, so the diagnosis stays centered on the revaluation mechanics.

---

## 2. Observation Lock

* **As-of**: `2026-11-02` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.5%)
* **IV move**: +1.67 vol pts vs noise band ±0.06 pts (exceeds noise band)
* **Prior observation**: `2026-10-30`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$50.5000`
* **Model ΔP (engine)**: `-$50.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$74.3322`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$23.8322` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (47.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$154.9749` | -46.6% | Stock moved from $769.36 to $755.72 (-13.6400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$36.5807` | -11.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$52.2081` | +15.7% | IV moved -1.47 vol pts (26.56% → 25.09%) |
| **Theta decay (Δt · Theta)** | `+$65.0152` | +19.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$23.8322` | +7.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$50.5000** | **-15.2%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$23.8322` (47.2% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$16.5382` | Volga PnL: `-$2.6015`
* Combined: `+$13.9367` | Residual after: `+$9.8955`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$64.4202`
* **spot**: `-$173.5104`
* **vol**: `+$58.5865`
* **rate**: `+$0.0477`
* Step sum: `-$50.4559` | Model ΔP: `-$50.5000` | Audit residual: `-$0.0441`

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

* Higher-order convexity and path effects can still distort the Taylor split versus the full revaluation.
* No relevant headlines were retrieved, so there is no supported borrow, squeeze, or implied-volatility narrative to verify.

---

### Position 4 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-02` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$17.5000` (-31.5%)
* **Model ΔP**: `-$17.5000`
* **Primary drivers**: **Delta PnL** (-27.0%) and **Vega PnL** (+26.7%) and **Gamma PnL** (+21.0%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best explained by the blotter’s dominant delta exposure as the underlying fell, with gamma partly cushioning the move and theta adding a small drag. The residual is large relative to the model change, so the Taylor split is only a reference view and the run should be read as a full revaluation with higher-order convexity and path effects left in the gap. No headline catalyst is available, and the observation lock means there is no supported Layer B mechanism to add beyond the modeled repricing. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the dominant modeled driver is clear, but observation reliability is false and the residual band is high, so the Greek decomposition is only approximate. There are no retrieved headlines, and the surface diagnostics show model limitations, so the tape does not support a more granular catalyst read.

---

## 2. Observation Lock

* **As-of**: `2026-11-02` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.3%)
* **IV move**: +1.04 vol pts vs noise band ±0.06 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-30`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$17.5000`
* **Model ΔP (engine)**: `-$17.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$61.3475`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$78.8475` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (450.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$103.0173` | -27.0% | Stock moved from $769.36 to $755.72 (-13.6400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$80.1091` | +21.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$102.1397` | +26.7% | IV moved +3.89 vol pts (8.95% → 12.84%) |
| **Theta decay (Δt · Theta)** | `-$17.8840` | -4.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$78.8475` | -20.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$17.5000** | **-4.6%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$78.8475` (450.6% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.78).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (vanna, volga) — reference only, see Regime above
* Vanna PnL: `-$91.7317` | Volga PnL: `+$25.5317`
* Combined: `-$66.2001` | Residual after: `-$12.6474`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$17.1637`
* **spot**: `-$34.9652`
* **vol**: `+$34.6443`
* **rate**: `+$0.0144`
* Step sum: `-$17.4702` | Model ΔP: `-$17.5000` | Audit residual: `-$0.0298`

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
* The modeled attribution may still be distorted by truncation, surface fit limits, and path-dependent effects, so treat the Greek split as directional rather than exact.
* No named catalyst was retrieved, so there is no supported Layer B mechanism to verify from headlines or microstructure.

---

### Position 5 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-02` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$11.5000` (+11.0%)
* **Model ΔP**: `+$11.5000`
* **Primary drivers**: **Delta PnL** (+50.5%) and **Vega PnL** (-28.8%) and **Theta decay** (-13.4%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The option’s revaluation was driven primarily by the higher underlying, with gamma reinforcing the move while theta and the lower implied volatility offset part of the gain. The residual is small relative to the model change, so this reads as a mostly clean spot-led repricing rather than a separate event-driven dislocation. There are no retrieved headlines or named microstructure tokens to add a catalyst layer, and the observation lock means the tape should be treated as a model-based attribution only. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is limited by the unreliable observation flag and the fact that the surface diagnostics show a failed American FD surface under Heston, so the full revaluation should be read cautiously. That said, the driver ranking is internally consistent, the residual is modest, and the absence of headlines or relevant digest tags prevents a stronger catalyst claim.

---

## 2. Observation Lock

* **As-of**: `2026-11-02` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 14.6%)
* **IV move**: +1.37 vol pts vs noise band ±2.15 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-30`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$11.5000`
* **Model ΔP (engine)**: `+$11.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$12.1554`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.6554` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (5.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$41.2586` | +50.5% | Stock moved from $43.66 to $44.73 (+1.0700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$5.3523` | +6.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$23.4972` | -28.8% | IV moved -5.88 vol pts (39.10% → 33.21%) |
| **Theta decay (Δt · Theta)** | `-$10.9583` | -13.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.6554` | -0.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$11.5000** | **+14.1%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.6554` (5.7% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$3.2101` | Volga PnL: `+$0.4479`
* Combined: `-$2.7621` | Residual after: `+$2.1068`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$11.2231`
* **spot**: `+$45.9354`
* **vol**: `-$23.2128`
* **rate**: `+$0.0079`
* Step sum: `+$11.5074` | Model ΔP: `+$11.5000` | Audit residual: `-$0.0074`

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
* Verify whether the spot-led move remains stable under a full-surface reprice, since the residual and surface diagnostics indicate some model sensitivity.
* Watch for any later-retrieved VZ-specific news or borrow/IV context, but do not infer a catalyst from the current feed because no relevant headlines were captured.

---

### Position 6 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-02` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.5000` (+33.3%)
* **Model ΔP**: `+$0.5000`
* **Primary drivers**: **Vega PnL** (+211.1%) and **Delta PnL** (-54.9%) and **Theta decay** (-52.8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by a vega revaluation: the option was marked higher as implied volatility rose while spot drifted lower and theta also worked against the position. The residual is modest, so the Greek decomposition is directionally coherent, but the large volatility move and weak observation quality mean the run should be treated as a model-based explanation rather than a clean market-tape read. There are no relevant headlines in the digest, so there is no separate catalyst layer to add beyond the vol-driven repricing. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation reliability is flagged false, the residual is not zero, and the market feed is incomplete enough that the quote quality limits how tightly the move can be tied to a single tape event. The prior IV source is the chain mark, not a copied proxy, so the vega line is usable, but there are no retained headlines or mechanism tags to support an external catalyst story.

---

## 2. Observation Lock

* **As-of**: `2026-11-02` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 100.0%)
* **IV move**: +18.75 vol pts vs noise band ±15.55 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-30`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.5000`
* **Model ΔP (engine)**: `+$0.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.5351`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0351` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (7.0%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.2744` | -54.9% | Stock moved from $1.42 to $1.37 (-0.0500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0178` | +3.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$1.0557` | +211.1% | IV moved +18.27 vol pts (150.04% → 168.31%) |
| **Theta decay (Δt · Theta)** | `-$0.2640` | -52.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0351` | -7.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0351` (7.0% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.1569` | Volga PnL: `+$0.2228`
* Combined: `+$0.0659` | Residual after: `-$0.1010`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.2570`
* **spot**: `-$0.2220`
* **vol**: `+$0.9790`
* **rate**: `+$0.0001`
* Step sum: `+$0.5001` | Model ΔP: `+$0.5000` | Audit residual: `-$0.0001`

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
* Check whether the next run still shows a broad full-surface repricing rather than a one-off mark shift, since truncation and surface shape can distort the modeled split.
* Watch for any fresh headlines or quote-quality improvement that would confirm whether the implied-vol move was a true repricing rather than a noisy chain update.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0910 | level_proxy(t) = 0.1878
* Δskew = +0.0063 | Δlevel = +0.0135
* Put 715 delta=-0.1476 | Call 795 delta=0.0436
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **jpm_straddle_call** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-11, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
- **jpm_straddle_put** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-11, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
