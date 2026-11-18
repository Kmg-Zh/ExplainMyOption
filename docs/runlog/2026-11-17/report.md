# Live book run — 2026-11-17

Run `2026-11-17-1794968842`. 8/8 legs diagnosed, 0 settled at expiry, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=12`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-17` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$102.5000`
* **Total Model PnL**: `-$83.0580`
* **Aggregate model vs mark gap**: `+$19.4420`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `JPM 340P 2026-12-18` | `+$485.0000` |
| 2 | `JPM 340C 2026-12-18` | `-$380.0000` |
| 3 | `SPY 715P 2026-11-20` | `-$122.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$140.9469` |
| Gamma | `+$86.4008` |
| Vega | `-$59.0530` |
| Theta | `+$26.3916` |
| Residual | `+$4.1496` |

### Notable underlyings

* **SPY**: `-$122.0000` aggregate option PnL
* **JPM**: `+$105.0000` aggregate option PnL
* **VZ**: `-$42.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$112.5000` (-3.2%)
* **Model ΔP**: `-$93.0580`
* **Primary drivers**: **Delta PnL** (-85.0%) and **Theta decay** (-49.2%) and **Vega PnL** (+46.7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The dominant modeled driver is the spot move flowing through delta, with theta also a meaningful drag and a smaller offset from vega. That said, the attribution does not fully explain this move: the residual is still material, so the story needs human review rather than a single-factor explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is only medium because observation is unreliable, the residual remains material, and the playbook flags a terminal unexplained break. The diagnostic tools and attribution budget do not fully close the gap, so the move should be treated as only partially explained by the model.

---

## 2. Observation Lock

* **As-of**: `2026-11-17` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 7.8%)
* **IV move**: +7.23 vol pts vs noise band ±20.15 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-16`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$112.5000`
* **Model ΔP (engine)**: `-$93.0580`
* **Model vs Mark gap**: `+$19.4420` (-20.9% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$81.2504`

* **Method residual (ε_method)**: `-$11.8076` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$19.4420` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (12.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$79.1457` | -85.0% | Stock moved from $352.78 to $351.91 (-0.8700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.2769` | +0.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$43.4394` | +46.7% | IV moved +7.23 vol pts (60.23% → 67.46%) |
| **Theta decay (Δt · Theta)** | `-$45.8210` | -49.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$11.8076` | -12.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$93.0580** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$11.8076` (12.7% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$2.0596` | Volga PnL: `+$4.4518`
* Combined: `+$6.5115` | Residual after: `-$18.3191`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$45.7816`
* **spot**: `-$81.3269`
* **vol**: `+$34.0609`
* **rate**: `+$0.0312`
* Step sum: `-$93.0164` | Model ΔP: `-$93.0580` | Audit residual: `-$0.0416`

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
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Check whether higher-order convexity or a full-surface reprice is distorting the modeled attribution given the residual break.
* Verify the mark quality and surface fit, since the run is flagged as an unexplained break and observation reliability is weak.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$70.0000` (-11.8%)
* **Model ΔP**: `+$70.0000`
* **Primary drivers**: **Theta decay** (+82.6%) and **Delta PnL** (+76.1%) and **Vega PnL** (-66.3%).
* **Verdict**: The modeled move is led by time decay, with spot drift and the vol uptick both working against the long call while the Greek decomposition still nets to a positive model revaluation. The small residual is consistent with higher-order effects and path dependence in the full reprice, but there is no headline-backed catalyst to add beyond the blotter mechanics. Early exercise is not a meaningful contributor here because the American premium is negligible at the current marks.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is strong and the observation is reliable, but the residual is not trivial and the surface diagnostics indicate model limitations. There are no relevant headlines or named microstructure mechanisms, so Layer B is intentionally empty and the story rests on the factor decomposition.

---

## 2. Observation Lock

* **As-of**: `2026-11-17` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 7.6%)
* **IV move**: +2.66 vol pts vs noise band ±1.61 pts (exceeds noise band)
* **Prior observation**: `2026-11-16`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$70.0000`
* **Model ΔP (engine)**: `+$70.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$63.3411`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$6.6589` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (9.5%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$53.2624` | +76.1% | Stock moved from $352.78 to $351.91 (-0.8700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$1.3300` | -1.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$46.4329` | -66.3% | IV moved +3.28 vol pts (29.51% → 32.80%) |
| **Theta decay (Δt · Theta)** | `+$57.8416` | +82.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$6.6589` | +9.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$70.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$6.6589` (9.5% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$1.1778` | other second-order: `-$0.1443`
* Combined: `-$1.3221` | Residual after: `+$7.9810`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$57.8748`
* **spot**: `+$52.9112`
* **vol**: `-$40.7947`
* **rate**: `-$0.0213`
* Step sum: `+$69.9701` | Model ΔP: `+$70.0000` | Audit residual: `+$0.0299`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Theta decay**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* Higher-order curvature and full-surface repricing can still move the final attribution versus the reference Greeks, especially with the remaining time to expiry.
* No named catalyst, borrow, or squeeze signal is present in the digest; verify any future move against fresh headlines before layering in a news explanation.

---

### Position 3 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$380.0000` (-39.0%)
* **Model ΔP**: `-$380.0000`
* **Primary drivers**: **Delta PnL** (-107.9%) and **Gamma PnL** (+13.8%).
* **Verdict**: The move is explained primarily by the stock's decline hitting a call with positive delta, with gamma partly cushioning the revaluation and a smaller theta drag layered in. The residual is minimal, so the modeled move is well captured by the Taylor decomposition; there is no separate headline catalyst to add, and the early-exercise premium is negligible at these marks.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is high, the residual is small, and the market move is straightforward, but the market feed has no retrieved headlines to provide an external catalyst check. The American-versus-European premium is negligible, so there is no meaningful early-exercise layer to discuss.

---

## 2. Observation Lock

* **As-of**: `2026-11-17` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.7%)
* **IV move**: -0.70 vol pts vs noise band ±0.14 pts (exceeds noise band)
* **Prior observation**: `2026-11-16`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$380.0000`
* **Model ΔP (engine)**: `-$380.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$382.1263`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$2.1263` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$409.9161` | -107.9% | Stock moved from $338.21 to $329.96 (-8.2500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$52.4421` | +13.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$7.5454` | -2.0% | IV moved -0.19 vol pts (25.81% → 25.62%) |
| **Theta decay (Δt · Theta)** | `-$17.1069` | -4.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$2.1263` | +0.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$380.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$2.1263` (0.6% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.0471`
* Combined: `+$0.0471` | Residual after: `+$2.0792`

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

* Watch for any larger spot gap or full-surface reprice, since the current attribution is dominated by delta with some second-order cushioning.
* No Layer B catalyst is available here; with no retrieved headlines, there is nothing to verify on borrow, squeeze, or implied volatility narratives.

---

### Position 4 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$485.0000` (+48.5%)
* **Model ΔP**: `+$485.0000`
* **Primary drivers**: **Delta PnL** (+86.4%) and **Gamma PnL** (+12.0%).
* **Verdict**: The position’s move was driven primarily by the lower spot price, which helped the put revalue higher under the official FDM engine. Gamma added a smaller convexity boost and vega was a minor tailwind, while theta was a small drag; the residual is negligible, so the Taylor view is close to the full revaluation.
* **Confidence**: **Medium** — Confidence is medium because the blotter is internally consistent and observation quality is reliable, but there are no retrieved headlines or named catalysts to add a Layer B explanation. The residual is small, so the dominant driver is clear, though the move is still a model revaluation rather than a market mark explanation.

---

## 2. Observation Lock

* **As-of**: `2026-11-17` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.0%)
* **IV move**: -0.51 vol pts vs noise band ±0.42 pts (exceeds noise band)
* **Prior observation**: `2026-11-16`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$485.0000`
* **Model ΔP (engine)**: `+$485.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$485.9900`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.9900` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$419.0644` | +86.4% | Stock moved from $338.21 to $329.96 (-8.2500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$58.3613` | +12.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$22.3333` | +4.6% | IV moved +0.56 vol pts (23.47% → 24.03%) |
| **Theta decay (Δt · Theta)** | `-$13.7691` | -2.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.9900` | -0.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$485.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.9900` (0.2% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.1640`
* Combined: `-$0.1640` | Residual after: `-$0.8260`

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

* Monitor whether spot continues to move enough to keep convexity terms relevant, since truncation can matter more if the next move is larger.
* Early exercise remains a secondary check only; compare remaining time value against upcoming dividends and carry, but the premium is currently small.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$122.0000` (+90.0%)
* **Model ΔP**: `-$122.0000`
* **Primary drivers**: **Delta PnL** (-75.0%) and **Vega PnL** (-57.1%) and **Theta decay** (+44.2%).
* **Verdict**: The position was led by the spot decline, with the modeled PnL dominated by the delta bucket and reinforced by second-order convexity from the same move. The volatility lift added to the move, but there are no relevant headlines or named microstructure mechanisms here, so the tape is best read as a clean model revaluation rather than a catalyst-driven gap story.
* **Confidence**: **Medium** — Confidence is supported by high attribution coverage and reliable observations, but the residual is still material enough to reflect higher-order effects and the market feed is not complete enough to over-interpret the secondary buckets. There are no relevant headlines to anchor a separate Layer B mechanism, and the American premium is negligible.

---

## 2. Observation Lock

* **As-of**: `2026-11-17` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.9%)
* **IV move**: +4.48 vol pts vs noise band ±0.13 pts (exceeds noise band)
* **Prior observation**: `2026-11-16`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$122.0000`
* **Model ΔP (engine)**: `-$122.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$132.8235`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$10.8235` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (8.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$91.4552` | -75.0% | Stock moved from $739.95 to $732.44 (-7.5100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$25.6224` | -21.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$69.7163` | -57.1% | IV moved +4.45 vol pts (28.74% → 33.19%) |
| **Theta decay (Δt · Theta)** | `+$53.9704` | +44.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$10.8235` | +8.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$122.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$10.8235` (8.9% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$24.6495` | Volga PnL: `-$7.2022`
* Combined: `-$31.8517` | Residual after: `+$42.6752`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$53.9537`
* **spot**: `-$96.0629`
* **vol**: `-$79.8937`
* **rate**: `+$0.0154`
* Step sum: `-$121.9876` | Model ΔP: `-$122.0000` | Audit residual: `-$0.0124`

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

* Residual size leaves room for truncation and path effects from the full reprice, so the Taylor split should be treated as directional rather than exact.
* With no relevant headline set, there is no borrow, squeeze, or IV-crush catalyst to verify; keep the focus on the spot and implied-vol inputs used by the model.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Vega PnL** (+39.1%) and **Delta PnL** (-16.6%) and **Gamma PnL** (+10.9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by a reprice from the implied-vol move in the option model, with spot and time decay playing smaller offsetting roles. Because the observation is not reliable and the surface diagnostics are weak, the large residual is best treated as model-truncation and surface-fit noise rather than a separate economic signal. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because the observation is flagged unreliable, the surface diagnostics are limited, and the residual is large relative to the model change. There are no relevant headlines or confirmed catalyst tags to support a Layer B story, and the early-exercise premium is negligible.

---

## 2. Observation Lock

* **As-of**: `2026-11-17` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: +7.03 vol pts vs noise band ±1.37 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-16`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000`
* **Explained ΔP (Taylor ex-residual)**: `+$2.0410`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$2.0410` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$1.4290` | -16.6% | Stock moved from $739.95 to $732.44 (-7.5100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.9397` | +10.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$3.3691` | +39.1% | IV moved +7.18 vol pts (23.47% → 30.65%) |
| **Theta decay (Δt · Theta)** | `-$0.8388` | -9.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$2.0410` | -23.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **+0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$2.0410` (>1000% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.66).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (vanna, volga) — reference only, see Regime above
* Vanna PnL: `-$7.5594` | Volga PnL: `+$4.3171`
* Combined: `-$3.2422` | Residual after: `+$1.2012`

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
* The modeled attribution can still be distorted by second-order effects, surface-fit error, or a full-surface reprice rather than the simple Taylor buckets.
* With no relevant headlines or named microstructure tags, do not force a catalyst read; the move should be treated as a model revaluation only.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$42.0000` (-26.0%)
* **Model ΔP**: `-$42.0000`
* **Primary drivers**: **Delta PnL** (-74.2%) and **Theta decay** (-18.4%) and **Vega PnL** (-8.5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was led by the model’s delta exposure, with the lower close in the underlying driving the main revaluation. Gamma softened the move slightly, while theta and a smaller vol reprice added to the decline; the residual is minor and consistent with truncation rather than a separate story. There are no relevant headlines or named microstructure tags here, so the run is a factor-led revaluation rather than a catalyst-driven gap. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by the observation lock and the fact that the market feed is incomplete, so the diagnosis should stay coarse. The attribution is still clear because the dominant factor is explicit, the residual is low, and the headline set is empty, but the vol narrative is suppressed and should not be overstated.

---

## 2. Observation Lock

* **As-of**: `2026-11-17` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 32.6%)
* **IV move**: +1.37 vol pts vs noise band ±14.10 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-16`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$42.0000`
* **Model ΔP (engine)**: `-$42.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$41.1512`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.8488` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.0%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$31.1790` | -74.2% | Stock moved from $46.34 to $45.93 (-0.4100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.3295` | +3.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$3.5859` | -8.5% | IV moved -2.38 vol pts (40.61% → 38.23%) |
| **Theta decay (Δt · Theta)** | `-$7.7159` | -18.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.8488` | -2.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$42.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.8488` (2.0% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.3530`
* Combined: `-$0.3530` | Residual after: `-$0.4958`

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
* Watch for any further distortion from Taylor truncation if spot moves widen or the reprice becomes more path-dependent.
* With no retrieved headlines or named microstructure tags, there is no separate catalyst layer to verify beyond the underlying and implied-vol marks.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$1.0000` (-50.0%)
* **Model ΔP**: `-$1.0000`
* **Primary drivers**: **Vega PnL** (-91.4%) and **Theta decay** (-16.9%) and **Delta PnL** (-14.9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is dominated by the model’s vega line: the option was repriced lower as implied volatility fell, with spot’s small decline and theta decay contributing secondary pressure. The remaining gap is consistent with a high residual on a short-dated, high-volatility name where Taylor truncation and surface effects can matter, but there is no named headline catalyst to attach as a separate Layer B mechanism. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is limited because observation is flagged unreliable, the residual is high, and there are no retrieved headlines or digest mechanisms to independently confirm a catalyst. The prevailing interpretation rests on the engine’s factor decomposition and the large volatility move, while the residual may reflect higher-order convexity or surface-repricing effects.

---

## 2. Observation Lock

* **As-of**: `2026-11-17` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: -46.87 vol pts vs noise band ±17.52 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-16`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$1.0000`
* **Model ΔP (engine)**: `-$1.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$1.2283`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.2283` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (22.8%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.1488` | -14.9% | Stock moved from $1.07 to $1.05 (-0.0200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0036` | +0.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.9143` | -91.4% | IV moved -20.52 vol pts (245.69% → 225.17%) |
| **Theta decay (Δt · Theta)** | `-$0.1688` | -16.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.2283` | +22.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$1.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.2283` (22.8% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.0519` | Volga PnL: `+$0.1197`
* Combined: `+$0.1716` | Residual after: `+$0.0567`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.1688`
* **spot**: `-$0.1357`
* **vol**: `-$0.6954`
* **rate**: `+$0.0000`
* Step sum: `-$0.9999` | Model ΔP: `-$1.0000` | Audit residual: `-$0.0001`

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
* Taylor attribution can still be distorted by truncation and surface effects in a short-dated, high-volatility contract; verify the full revaluation remains consistent with the factor sum.
* No Layer B catalyst was supplied, so there is no headline-backed IV crush, borrow, or squeeze mechanism to monitor from the digest.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0265 | level_proxy(t) = 0.3179
* Δskew = -0.0255 | Δlevel = +0.0576
* Put 715 delta=-0.2050 | Call 795 delta=0.0017
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
