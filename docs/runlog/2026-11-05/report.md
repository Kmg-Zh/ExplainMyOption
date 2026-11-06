# Live book run — 2026-11-05

Run `2026-11-05-1793938153`. 6/8 legs diagnosed, 2 settled at expiry, 0 failed. `legs_narrated=5` `legs_silent=1` `llm_calls=8`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-05` | **Positions**: 6 | **Tickers**: AAPL, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$1,035.0000`
* **Total Model PnL**: `-$1,035.0000`
* **Aggregate model vs mark gap**: `-$0.0000`
* **Settled at expiry**: `+$430.0013` across 2 leg(s), not in the totals above (see Settled at expiry)

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `SPY 715P 2026-11-20` | `-$809.0000` |
| 2 | `AAPL 325C 2026-11-20` | `-$297.5000` |
| 3 | `AAPL 350C 2026-11-20` | `+$117.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$674.1648` |
| Gamma | `+$239.2623` |
| Vega | `+$10.6877` |
| Theta | `+$9.3968` |
| Residual | `-$620.1820` |

### Notable underlyings

* **SPY**: `-$862.0000` aggregate option PnL
* **AAPL**: `-$180.0000` aggregate option PnL
* **VZ**: `+$7.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$297.5000` (-11.5%)
* **Model ΔP**: `-$297.5000`
* **Primary drivers**: **Delta PnL** (-160.8%) and **Vega PnL** (+44.2%).
* **Verdict**: The position was driven mainly by the lower underlying price, which worked against a long call with high delta and dominated the full revaluation. The large volatility increase helped offset some of that damage, but it was not enough to overcome the spot move; the remaining gap is consistent with higher-order convexity and model truncation rather than a separate catalyst. No relevant headline catalyst was retained, so this is a model-led repricing story rather than a news-led one.
* **Confidence**: **Medium** — Confidence is medium because the attribution is internally consistent and the diagnostic tools ran, but the residual is sizable and the spot move is not large enough to fully explain the convexity gap on its own. IV moved sharply and the feed uses a prior-chain IV source, so the Vega contribution should be treated as a model input shift rather than a standalone market narrative. No relevant headlines were available, so there is no independent catalyst layer to corroborate or challenge the move.

---

## 2. Observation Lock

* **As-of**: `2026-11-05` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 7.9%)
* **IV move**: +9.89 vol pts vs noise band ±4.39 pts (exceeds noise band)
* **Prior observation**: `2026-11-04`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$297.5000`
* **Model ΔP (engine)**: `-$297.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$349.4538`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$51.9538` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (17.5%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$478.4665` | -160.8% | Stock moved from $349.51 to $344.17 (-5.3400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$12.2995` | +4.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$131.6051` | +44.2% | IV moved +9.96 vol pts (28.62% → 38.59%) |
| **Theta decay (Δt · Theta)** | `-$14.8919` | -5.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$51.9538` | +17.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$297.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$51.9538` (17.5% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$34.4937` | Volga PnL: `+$25.9388`
* Combined: `+$60.4325` | Residual after: `-$8.4787`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$14.9178`
* **spot**: `-$468.4207`
* **vol**: `+$185.7451`
* **rate**: `-$0.3849`
* Step sum: `-$297.9784` | Model ΔP: `-$297.5000` | Audit residual: `+$0.4784`

### Ex-div attribution overlay (official PnL stays the American FDM Taylor blotter)
* **Spot drop vs dividend** (per share): spot `-$5.3400` vs next cash dividend `+$0.2700` (gap `-$5.0700`)
* **American FDM vs European analytic (no cash div, cross-check, per option)**: `+$22.9000` vs `+$23.0733` (gap `-$0.1733`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored, per option): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs, per option): `-$0.1741`
* **Dividend coverage** (dividend / time value): `0.07` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$131.6051`
* **Residual (Taylor ε)**: `+$51.9538`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. [​Post-Earnings Black Swan: $INTC 28% Crash - moomoo Community](https://www.moomoo.com/community/feed/post-earnings-black-swan-intc-28-crash-117536277004294)

---

## 7. Risk Watchlist

* Watch whether the remaining model gap is just Taylor truncation versus a fuller engine revaluation effect from the surface and path-dependent boundary.
* Keep an eye on implied volatility and the quoted surface quality, since the move included a large IV re-mark but no retained headline catalyst.
* **Assignment watch**: ex-div `2026-11-12` — Dividend coverage 0.07 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$117.5000` (-17.0%)
* **Model ΔP**: `+$117.5000`
* **Primary drivers**: **Delta PnL** (+54.8%) and **Vega PnL** (-31.5%) and **Gamma PnL** (-6.6%).
* **Verdict**: The move is best explained by the option’s delta exposure to the underlying decline, with gamma and theta partly offsetting and vega adding additional pressure from the higher implied volatility backdrop. The residual is modest, so the Taylor run is broadly consistent with the full revaluation; there is no separate headline catalyst to layer on top of the blotter story.
* **Confidence**: **Medium** — Confidence is limited only by the medium residual band and the fact that the spot move was not extreme, so some higher-order curvature remains in the gap. The feed is otherwise clean: IV history is available from the chain, the observation is reliable, and there are no relevant headlines or named microstructure mechanisms to override the modeled driver.

---

## 2. Observation Lock

* **As-of**: `2026-11-05` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 8.7%)
* **IV move**: +5.52 vol pts vs noise band ±0.92 pts (exceeds noise band)
* **Prior observation**: `2026-11-04`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$117.5000`
* **Model ΔP (engine)**: `+$117.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$106.6971`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$10.8029` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (9.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$270.5522` | +54.8% | Stock moved from $349.51 to $344.17 (-5.3400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$32.4225` | -6.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$155.5234` | -31.5% | IV moved +5.33 vol pts (23.98% → 29.31%) |
| **Theta decay (Δt · Theta)** | `+$24.0908` | +4.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$10.8029` | +2.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$117.5000** | **+23.8%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$10.8029` (9.2% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$2.5418` | other second-order: `+$0.0063`
* Combined: `-$2.5355` | Residual after: `+$13.3385`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$24.1119`
* **spot**: `+$236.4830`
* **vol**: `-$143.0206`
* **rate**: `+$0.2090`
* Step sum: `+$117.7834` | Model ΔP: `+$117.5000` | Audit residual: `-$0.2834`

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

* Higher-order curvature can still distort the Greek split versus the full revaluation, especially with short-dated options.
* No relevant catalyst or microstructure tag was retrieved, so there is no separate borrow, squeeze, or IV-crush storyline to verify.
* **Assignment watch**: ex-div `2026-11-12` — Dividend coverage 0.05 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$809.0000` (+903.9%)
* **Model ΔP**: `-$809.0000`
* **Primary drivers**: **Delta PnL** (-24.3%) and **Gamma PnL** (-23.3%) and **Vega PnL** (-15.3%).
* **Verdict**: The dominant modeled driver is the residual, with spot, gamma, and vega all contributing to the revaluation but leaving a large unexplained bucket. The move is therefore best read as a full model repricing where higher-order effects and path dependence mattered more than the first-pass Taylor terms; no named catalyst was retrieved, so there is no Layer B headline mechanism to attach. The American-vs-European gap is negligible, so early exercise is not a material feature of the move.
* **Confidence**: **Medium** — Confidence is limited by low attribution coverage and a large residual share, so the Greek decomposition is only a reference view. The feed is otherwise reliable, the IV source is current chain data, and there were no relevant headlines to support a separate catalyst story.

---

## 2. Observation Lock

* **As-of**: `2026-11-05` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.9%)
* **IV move**: +6.54 vol pts vs noise band ±0.16 pts (exceeds noise band)
* **Prior observation**: `2026-11-04`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$809.0000`
* **Model ΔP (engine)**: `-$809.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$496.7261`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$312.2739` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (38.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$196.7527` | -24.3% | Stock moved from $766.81 to $733.00 (-33.8100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$188.5293` | -23.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$123.6559` | -15.3% | IV moved +6.62 vol pts (21.99% → 28.61%) |
| **Theta decay (Δt · Theta)** | `+$12.2119` | +1.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$312.2739` | -38.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$809.0000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$312.2739` (38.6% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.96).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (vanna, volga) — reference only, see Regime above
* Vanna PnL: `-$163.2401` | Volga PnL: `-$44.9088`
* Combined: `-$208.1488` | Residual after: `-$104.1251`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$12.1983`
* **spot**: `-$480.9391`
* **vol**: `-$339.9907`
* **rate**: `-$0.3410`
* Step sum: `-$809.0725` | Model ΔP: `-$809.0000` | Audit residual: `+$0.0725`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Residual / model revaluation gap**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._
_SEC EDGAR lists recent Form 8-K filings (official API; set `EMO_SEC_USER_AGENT` locally — free, no API key)._
_News fetch failed and was skipped: sec_8k._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* Higher-order convexity and Taylor truncation can still distort the attribution when spot and volatility move together.
* With no relevant headlines retrieved, there is no supported borrow, squeeze, or IV-crush narrative to verify.

---

### Position 4 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$53.0000` (-80.9%)
* **Model ΔP**: `-$53.0000`
* **Primary drivers**: **Gamma PnL** (+36.3%) and **Delta PnL** (-21.5%) and **Vega PnL** (+11.6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by gamma, with the Taylor view showing the option behaving as a convexity trade around a sharp spot decline. The large residual means the second-order decomposition does not fully capture the full revaluation, so higher-order curvature and path effects are doing meaningful work beyond the named Greek bucket. There are no retrieved headlines or named microstructure tags, so there is no supported Layer B catalyst to add beyond the model move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is limited by the low attribution coverage band, the high residual share, and observation unreliable status. The engine also notes a surface limitation, so the Greek split should be treated as a reference view rather than a complete explanation.

---

## 2. Observation Lock

* **As-of**: `2026-11-05` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 24.0%)
* **IV move**: +6.23 vol pts vs noise band ±0.29 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-04`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$53.0000`
* **Model ΔP (engine)**: `-$53.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$317.1866`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$370.1866` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (698.5%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$265.0205` | -21.5% | Stock moved from $766.81 to $733.00 (-33.8100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$447.7818` | +36.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$143.2697` | +11.6% | IV moved +6.10 vol pts (11.64% → 17.73%) |
| **Theta decay (Δt · Theta)** | `-$8.8444` | -0.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$370.1866` | -30.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$53.0000** | **-4.3%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$370.1866` (698.5% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 1.69).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (vanna, volga) — reference only, see Regime above
* Vanna PnL: `-$397.0730` | Volga PnL: `+$73.8822`
* Combined: `-$323.1909` | Residual after: `-$46.9957`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$8.8573`
* **spot**: `-$56.5785`
* **vol**: `+$12.3522`
* **rate**: `-$0.0155`
* Step sum: `-$53.0991` | Model ΔP: `-$53.0000` | Audit residual: `+$0.0991`

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
* Second-order Taylor terms and higher-order curvature can still distort the modeled attribution when spot gaps and the residual are large.
* No supported headline or microstructure catalyst was retrieved, so do not infer borrow, squeeze, or IV-crush dynamics from background memory.

---

### Position 5 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$7.0000` (+4.0%)
* **Model ΔP**: `+$7.0000`
* **Primary drivers**: **Vega PnL** (+194.6%) and **Delta PnL** (-48.0%) and **Theta decay** (-42.6%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-11-05` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 13.8%)
* **IV move**: +5.13 vol pts vs noise band ±3.64 pts (exceeds noise band)
* **Prior observation**: `2026-11-04`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$7.0000`
* **Model ΔP (engine)**: `+$7.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$7.2960`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.2960` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$3.3613` | -48.0% | Stock moved from $46.17 to $46.12 (-0.0500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0165` | +0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$13.6249` | +194.6% | IV moved +3.92 vol pts (28.59% → 32.51%) |
| **Theta decay (Δt · Theta)** | `-$2.9841` | -42.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.2960` | -4.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$7.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.2960` (4.2% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.0988` | Volga PnL: `+$0.1427`
* Combined: `+$0.2415` | Residual after: `-$0.5375`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Theta / carry**._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* No action needed; move is within theta/carry tolerance.

---

### Position 6 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (+46.1%) and **Delta PnL** (-37.6%) and **Theta decay** (-6.2%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best read as a full revaluation dominated by the spot drop in the context of a high-volatility tape, with the Greek decomposition showing the spot effect offset by positive vega and a smaller theta drag. Because the observation is unreliable and the Vega narrative is suppressed by the desk flags, the cleanest diagnosis is that the model reprice was driven by the underlying move, while the higher-vol regime helped cushion the option’s value. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is limited by the low attribution coverage, the high residual band, and the observation reliability flag. The desk also suppresses a Vega narrative, so the decomposition should be treated as a reference view rather than a precise causal split.

---

## 2. Observation Lock

* **As-of**: `2026-11-05` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 142.9%)
* **IV move**: +14.06 vol pts vs noise band ±29.96 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-04`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000`
* **Explained ΔP (Taylor ex-residual)**: `+$0.1822`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.1822` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$1.1160` | -37.6% | Stock moved from $1.46 to $1.35 (-0.1100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1164` | +3.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$1.3672` | +46.1% | IV moved +15.21 vol pts (181.82% → 197.03%) |
| **Theta decay (Δt · Theta)** | `-$0.1854` | -6.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.1822` | -6.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **-0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.1822` (>1000% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.3146` | Volga PnL: `+$0.1381`
* Combined: `-$0.1765` | Residual after: `-$0.0057`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.1854`
* **spot**: `-$0.9623`
* **vol**: `+$1.1477`
* **rate**: `-$0.0005`
* Step sum: `-$0.0005` | Model ΔP: `-$0.0000` | Audit residual: `+$0.0005`

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
* Higher-order curvature and truncation can still distort the Taylor split when spot moves are sizable relative to the option’s time value.
* No catalyst tape was retrieved, so there is no validated news or microstructure mechanism to layer onto the model move.

---

## Settled at expiry

| Contract | Outcome | Settlement | PnL ($) |
| :--- | :--- | ---: | ---: |
| `JPM 350C 2026-10-23` | expired worthless | 0.0000 | `-$2.0000` |
| `JPM 350P 2026-10-23` | exercised | 18.4200 | `+$432.0013` |

### Settled — `JPM 350C 2026-10-23`

`JPM 350C 2026-10-23` expired at the 2026-10-23 close (spot 331.58) and settles at intrinsic value, 0.0000 per option. No model, vol or news search is involved.

Prior mark: 0.0200 on 2026-10-22 (spot 336.54).

| Component | Per option | Position ($) |
| :--- | ---: | ---: |
| Intrinsic change from spot | `+$0.0000` | `+$0.0000` |
| Time value released | `-$0.0200` | `-$2.0000` |
| **Settlement PnL** | `-$0.0200` | `-$2.0000` |

* Expires worthless: no exercise, no stock delivery.

### Settled — `JPM 350P 2026-10-23`

`JPM 350P 2026-10-23` expired at the 2026-10-23 close (spot 331.58) and settles at intrinsic value, 18.4200 per option. No model, vol or news search is involved.

Prior mark: 14.1000 on 2026-10-22 (spot 336.54).

| Component | Per option | Position ($) |
| :--- | ---: | ---: |
| Intrinsic change from spot | `+$4.9600` | `+$496.0022` |
| Time value released | `-$0.6400` | `-$64.0009` |
| **Settlement PnL** | `+$4.3200` | `+$432.0013` |

* Exercised: the position sells 100 shares at 350. This report does not track the resulting stock position.


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0999 | level_proxy(t) = 0.2326
* Δskew = +0.0031 | Δlevel = +0.0639
* Put 715 delta=-0.3169 | Call 795 delta=0.0137
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Rolls

- **jpm_straddle_call**: `JPM 350C 2026-10-23` settled at the 2026-10-23 close. It expired before this run's session; this is the first run to settle it. Rolled into `JPM 340C 2026-12-18` at the 2026-11-05 close (spot 337.34, mark 11.5500); its PnL starts with the next run.
- **jpm_straddle_put**: `JPM 350P 2026-10-23` settled at the 2026-10-23 close. It expired before this run's session; this is the first run to settle it. Rolled into `JPM 340P 2026-12-18` at the 2026-11-05 close (spot 337.34, mark 12.4750); its PnL starts with the next run.
