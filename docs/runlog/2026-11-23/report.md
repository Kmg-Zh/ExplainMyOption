# Live book run — 2026-11-23

Run `2026-11-23-1795487282`. 8/8 legs diagnosed, 0 settled at expiry, 0 failed. `legs_narrated=6` `legs_silent=2` `llm_calls=12`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-23` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$1,367.0000`
* **Total Model PnL**: `+$1,367.0000`
* **Aggregate model vs mark gap**: `-$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `SPY 725C 2027-01-15` | `+$984.5000` |
| 2 | `SPY 655P 2027-01-15` | `+$899.0000` |
| 3 | `JPM 340P 2026-12-18` | `-$652.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$1,746.0622` |
| Gamma | `+$93.5572` |
| Vega | `-$349.9066` |
| Theta | `-$62.2486` |
| Residual | `-$60.4642` |

### Notable underlyings

* **SPY**: `+$1,883.5000` aggregate option PnL
* **JPM**: `-$636.5000` aggregate option PnL
* **AAPL**: `+$130.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 335C 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 335C 2027-01-15`  
**Analysis Date**: `2026-11-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$207.5000` (+9.7%)
* **Model ΔP**: `+$207.5000`
* **Primary drivers**: **Delta PnL** (+193.4%) and **Vega PnL** (-86.5%) and **Theta decay** (-23.2%).
* **Verdict**: The revaluation was driven primarily by the higher underlying price, with gamma adding a smaller convexity lift while theta and the lower implied volatility offset part of that gain. The move is consistent with a clean spot-led repricing in the FDM engine, and the small residual suggests modest higher-order effects rather than a separate catalyst. With no relevant headlines or named microstructure tokens, there is no Layer B event story to add beyond the market move itself.
* **Confidence**: **Medium** — Confidence is medium because the attribution is supported by reliable observations and high coverage, but the residual is not negligible and the surface diagnostics note model limitations under the surface-based American run. There are no retrieved headlines, so there is no independent catalyst to confirm or challenge the factor story.

---

## 2. Observation Lock

* **As-of**: `2026-11-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.3%)
* **IV move**: -3.98 vol pts vs noise band ±1.07 pts (exceeds noise band)
* **Prior observation**: `2026-11-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$207.5000`
* **Model ΔP (engine)**: `+$207.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$193.4276`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$14.0724` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (6.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$401.3742` | +193.4% | Stock moved from $342.56 to $349.08 (+6.5200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$19.7185` | +9.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$179.4804` | -86.5% | IV moved -3.50 vol pts (30.67% → 27.17%) |
| **Theta decay (Δt · Theta)** | `-$48.1847` | -23.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$14.0724` | +6.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$207.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$14.0724` (6.8% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$4.2529` | other second-order: `+$0.3525`
* Combined: `+$4.6053` | Residual after: `+$9.4671`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$48.5402`
* **spot**: `+$421.6319`
* **vol**: `-$165.6570`
* **rate**: `+$0.7920`
* Step sum: `+$208.2268` | Model ΔP: `+$207.5000` | Audit residual: `-$0.7268`

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

* Watch whether a full-surface reprice or higher-order convexity could change the residual around the current mark path.
* No relevant headlines were retrieved, so there is no borrow, squeeze, or IV-crush tape to verify; keep the focus on spot and implied volatility changes.

---

### Position 2 — `AAPL 360C 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 360C 2027-01-15`  
**Analysis Date**: `2026-11-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$77.5000` (+9.8%)
* **Model ΔP**: `-$77.5000`
* **Primary drivers**: **Delta PnL** (-53.8%) and **Vega PnL** (+30.0%) and **Theta decay** (+9.0%).
* **Verdict**: The position was driven first by the adverse spot move for a short-dated call, with the Taylor view also showing gamma and vega working against that move in smaller secondary ways. The model revaluation was only modestly offset by theta, so the net picture remains a spot-led loss rather than a volatility or decay story. No relevant headlines were retrieved, and the residual is consistent with higher-order effects around the move rather than a separate catalyst.
* **Confidence**: **Medium** — The attribution is supported by the engine’s dominant driver, the high coverage band, and reliable observations, but the residual is not negligible and the spot move is only small in band terms. There are no relevant headlines or named microstructure mechanisms to anchor a Layer B catalyst, so the diagnosis stays centered on the modeled revaluation.

---

## 2. Observation Lock

* **As-of**: `2026-11-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 6.9%)
* **IV move**: -2.65 vol pts vs noise band ±0.58 pts (exceeds noise band)
* **Prior observation**: `2026-11-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$77.5000`
* **Model ΔP (engine)**: `-$77.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$85.8845`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$8.3845` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (10.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$229.8737` | -53.8% | Stock moved from $342.56 to $349.08 (+6.5200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$22.5710` | -5.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$128.1482` | +30.0% | IV moved -2.57 vol pts (26.06% → 23.48%) |
| **Theta decay (Δt · Theta)** | `+$38.4120` | +9.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$8.3845` | +2.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$77.5000** | **-18.1%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$8.3845` (10.8% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$9.0066` | Volga PnL: `-$0.9214`
* Combined: `+$8.0852` | Residual after: `+$0.2993`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$38.6137`
* **spot**: `-$249.2214`
* **vol**: `+$133.1577`
* **rate**: `-$0.4830`
* Step sum: `-$77.9330` | Model ΔP: `-$77.5000` | Audit residual: `+$0.4330`

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

* Higher-order convexity and Taylor truncation can still distort a short-dated call’s decomposition around the spot move, so the full reprice remains the cleaner check.
* With no relevant catalyst headlines or named microstructure tags, there is no separate borrow, squeeze, or IV-crush narrative to verify.

---

### Position 3 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$16.0000` (+13.4%)
* **Model ΔP**: `+$16.0000`
* **Primary drivers**: **Delta PnL** (+44.7%) and **Vega PnL** (-21.8%) and **Theta decay** (-15.0%).
* **Verdict**: The position was driven primarily by the upward spot move in JPM, with gamma adding to the directional revaluation and vega and theta offsetting part of the gain. The residual is consistent with higher-order effects and model truncation around the revaluation path rather than a separate market catalyst, and there are no relevant headlines in the digest to add a Layer B mechanism.
* **Confidence**: **Medium** — Confidence is medium because the blotter cleanly identifies the dominant modeled driver and the observation is reliable, but the residual share is elevated and the surface diagnostics show a failed American FD surface check. There are no relevant headlines, so no external catalyst can be used to sharpen the explanation beyond the model revaluation.

---

## 2. Observation Lock

* **As-of**: `2026-11-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 6.6%)
* **IV move**: -3.17 vol pts vs noise band ±0.25 pts (exceeds noise band)
* **Prior observation**: `2026-11-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$16.0000`
* **Model ΔP (engine)**: `+$16.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$28.5977`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$12.5977` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (78.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$69.6671` | +44.7% | Stock moved from $310.53 to $316.66 (+6.1300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$16.2266` | +10.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$33.9276` | -21.8% | IV moved -2.05 vol pts (25.90% → 23.85%) |
| **Theta decay (Δt · Theta)** | `-$23.3684` | -15.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$12.5977` | -8.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$16.0000** | **+10.3%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$12.5977` (78.7% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$11.5858` | Volga PnL: `+$1.8788`
* Combined: `-$9.7071` | Residual after: `-$2.8906`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$23.0468`
* **spot**: `+$78.4788`
* **vol**: `-$39.4394`
* **rate**: `+$0.0728`
* Step sum: `+$16.0654` | Model ΔP: `+$16.0000` | Audit residual: `-$0.0654`

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

* Monitor whether a full-surface reprice or higher-order convexity would materially reduce the residual on the same move path.
* No catalyst tape was retained, so there is no borrow, squeeze, or IV-crush storyline to verify from headlines.

---

### Position 4 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$652.5000` (-21.3%)
* **Model ΔP**: `-$652.5000`
* **Primary drivers**: **Delta PnL** (-82.4%) and **Vega PnL** (-14.8%).
* **Verdict**: The move is explained first by the put’s negative delta, with the higher underlying level driving the option lower and the second-order and carry terms only partially offsetting that revaluation. A concurrent drop in implied volatility also weighed on the premium, while the remaining gap is small and consistent with higher-order effects around the model reprice rather than a separate catalyst. No relevant headlines were retrieved, so there is no Layer B event overlay to add beyond the market-driven revaluation.
* **Confidence**: **Medium** — Observation is reliable and the attribution coverage is high, but the residual is not zero and the surface diagnostics note an American FD surface failure under Heston, so the run is best treated as a clean model revaluation with some approximation noise. There are no retrieved headlines or named microstructure mechanisms, so there is no independent catalyst to corroborate beyond the blotter.

---

## 2. Observation Lock

* **As-of**: `2026-11-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.8%)
* **IV move**: -7.23 vol pts vs noise band ±4.55 pts (exceeds noise band)
* **Prior observation**: `2026-11-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$652.5000`
* **Model ΔP (engine)**: `-$652.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$638.9689`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$13.5311` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$537.4431` | -82.4% | Stock moved from $310.53 to $316.66 (+6.1300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$17.3426` | +2.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$96.5240` | -14.8% | IV moved -5.58 vol pts (27.67% → 22.09%) |
| **Theta decay (Δt · Theta)** | `-$22.3444` | -3.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$13.5311` | -2.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$652.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$13.5311` (2.1% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$29.1223` | Volga PnL: `+$11.7220`
* Combined: `-$17.4003` | Residual after: `+$3.8692`

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

* Second-order effects and Taylor truncation can still distort the split between delta, gamma, and the residual when the spot move and volatility move arrive together.
* Verify the early-exercise and dividend carry setup if the contract is revisited, but the current premium looks small relative to the model reprice.

---

### Position 5 — `SPY 655P 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 655P 2027-01-15`  
**Analysis Date**: `2026-11-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$899.0000` (-55.6%)
* **Model ΔP**: `+$899.0000`
* **Primary drivers**: **Delta PnL** (+108.5%) and **Gamma PnL** (-25.7%) and **Vega PnL** (+11.9%).
* **Verdict**: The PnL is driven primarily by the bullish spot move against a put, with gamma trimming part of the gain and vega contributing modestly as implied volatility slipped. The residual is small, so the Taylor view is broadly consistent with the model revaluation rather than pointing to a separate catalyst. No relevant headlines were retrieved, so there is no Layer B mechanism to add beyond the market move and the existing carry/vol effects.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is high and the residual is low, but the surface diagnostics note model limitations and the quote set is not deep enough to justify a richer news-based explanation. The position also has a small early-exercise premium, which is not material enough to change the story.

---

## 2. Observation Lock

* **As-of**: `2026-11-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.0%)
* **IV move**: -1.10 vol pts vs noise band ±0.05 pts (exceeds noise band)
* **Prior observation**: `2026-11-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$899.0000`
* **Model ΔP (engine)**: `+$899.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$918.8907`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$19.8907` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$975.0039` | +108.5% | Stock moved from $689.81 to $722.29 (+32.4800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$231.1848` | -25.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$106.6287` | +11.9% | IV moved -1.14 vol pts (29.73% → 28.59%) |
| **Theta decay (Δt · Theta)** | `+$68.4429` | +7.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$19.8907` | -2.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$899.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$19.8907` (2.2% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$19.2007` | other second-order: `-$0.4653`
* Combined: `-$19.6660` | Residual after: `-$0.2247`

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

* The modeled split is stable, but higher-order convexity can still matter if spot keeps moving sharply away from the strike.
* No named catalyst was available; verify whether any later tape, quote-quality issue, or implied-vol change alters the revaluation story.
* **Assignment watch**: ex-div `2026-12-17` — Dividend coverage 0.26 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 6 — `SPY 725C 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 725C 2027-01-15`  
**Analysis Date**: `2026-11-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$984.5000` (+73.7%)
* **Model ΔP**: `+$984.5000`
* **Primary drivers**: **Delta PnL** (+108.7%) and **Gamma PnL** (+29.9%) and **Vega PnL** (-27.6%).
* **Verdict**: The move is dominated by the spot rally feeding through the position’s positive delta, with gamma adding convexity support as the underlying advanced. Vega was a drag because implied volatility eased, but the headline story is still the underlying repricing rather than a volatility event. There are no relevant headlines or named microstructure tags in the digest, so this is a clean factor-led revaluation rather than a news-driven gap story.
* **Confidence**: **Medium** — Confidence is moderate because the blotter shows strong attribution coverage and a low residual, but the run also notes model-calibration limitations and a reference-style Greek decomposition rather than a full market-mark explanation. No relevant headlines were retrieved, so there is no auxiliary catalyst to reinforce Layer B.

---

## 2. Observation Lock

* **As-of**: `2026-11-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.5%)
* **IV move**: -2.67 vol pts vs noise band ±0.05 pts (exceeds noise band)
* **Prior observation**: `2026-11-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$984.5000`
* **Model ΔP (engine)**: `+$984.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$1,021.5767`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$37.0767` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$1,069.7868` | +108.7% | Stock moved from $689.81 to $722.29 (+32.4800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$294.0167` | +29.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$271.6575` | -27.6% | IV moved -2.78 vol pts (24.06% → 21.28%) |
| **Theta decay (Δt · Theta)** | `-$70.5693` | -7.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$37.0767` | -3.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$984.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$37.0767` (3.8% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$60.9191` | other second-order: `+$3.3604`
* Combined: `-$57.5587` | Residual after: `+$20.4820`

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

* Layer A: the largest source of attribution remains the spot move; the second-order Taylor view can understate or overstate when the underlying jump is material, though the residual here is small.
* Layer B: no relevant headlines were retrieved, so there is no borrow, squeeze, or IV-crush mechanism to verify from the tape.
* **Assignment watch**: ex-div `2026-12-17` — Dividend coverage 0.08 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 7 — `VZ 42C 2027-01-15`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 42C 2027-01-15`  
**Analysis Date**: `2026-11-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$10.0000` (-2.0%)
* **Model ΔP**: `-$10.0000`
* **Primary drivers**: **Theta decay** (-43.0%) and **Vega PnL** (-33.3%) and **Delta PnL** (-25.9%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-11-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 10.1%)
* **IV move**: -3.32 vol pts vs noise band ±7.10 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$10.0000`
* **Model ΔP (engine)**: `-$10.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$10.2158`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.2158` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.2%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$2.5900` | -25.9% | Stock moved from $46.48 to $46.45 (-0.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0021` | +0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$3.3280` | -33.3% | IV moved -0.86 vol pts (27.46% → 26.60%) |
| **Theta decay (Δt · Theta)** | `-$4.3000` | -43.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.2158` | +2.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$10.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.2158` (2.2% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.0170`
* Combined: `+$0.0170` | Residual after: `+$0.1988`

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
* **Assignment watch**: ex-div `2027-01-07` — Dividend coverage 1.42 (dividend $0.7080 vs time value $0.5000); ex-div is 45d out, expiry 53d out — early exercise is economically relevant.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Theta decay** (-44.6%) and **Vega PnL** (+31.0%) and **Delta PnL** (+18.2%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Low** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-11-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: -46.87 vol pts vs noise band ±20.32 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000`
* **Explained ΔP (Taylor ex-residual)**: `+$0.0408`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0408` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.0%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.1371` | +18.2% | Stock moved from $0.96 to $0.99 (+0.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0064` | +0.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.2339` | +31.0% | IV moved +9.17 vol pts (252.33% → 261.50%) |
| **Theta decay (Δt · Theta)** | `-$0.3366` | -44.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0408` | -5.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **+0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0408` (0.0% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.0315` | Volga PnL: `+$0.0179`
* Combined: `+$0.0495` | Residual after: `-$0.0903`

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


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0573 | level_proxy(t) = 0.2523
* Δskew = +0.0157 | Δlevel = -0.0188
* Put 655 delta=-0.1645 | Call 725 delta=0.5145
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
