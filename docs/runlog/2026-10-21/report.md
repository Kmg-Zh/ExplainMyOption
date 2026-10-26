# Live book run — 2026-10-21

Run `2026-10-21-1792632514`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=10`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-21` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$352.0000`
* **Total Model PnL**: `+$146.4605`
* **Aggregate model vs mark gap**: `-$205.5395`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `+$322.5000` |
| 2 | `AAPL 350C 2026-11-20` | `-$170.0000` |
| 3 | `JPM 350P 2026-10-23` | `-$88.0394` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$236.8071` |
| Gamma | `+$6.9638` |
| Vega | `+$156.5932` |
| Theta | `-$61.5779` |
| Residual | `-$192.3256` |

### Notable underlyings

* **AAPL**: `+$152.5000` aggregate option PnL
* **SPY**: `+$127.5000` aggregate option PnL
* **JPM**: `-$93.5394` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$322.5000` (+>1000%)
* **Model ΔP**: `+$322.5000`
* **Primary drivers**: **Delta PnL** (90%) and **Theta decay** (5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is dominated by the option’s positive delta, with the underlying’s upward drift doing most of the work and gamma adding a smaller convexity boost. Theta offset some of the gain, while the residual is negligible, so the model story is clean and largely explained by the spot reprice rather than a vol or exercise effect. No catalyst headlines were retrieved, and the observation lock means there is no supported Layer B mechanism to add beyond the modeled factor story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is supported by high attribution coverage and a low residual band, but the observation is not fully reliable and the market feed is incomplete. The attribution is therefore best read as a model revaluation with limited news context, not as a fully confirmed tape-driven explanation.

---

## 2. Observation Lock

* **As-of**: `2026-10-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.1%)
* **IV move**: +0.02 vol pts vs noise band ±1.25 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$322.5000`
* **Model ΔP (engine)**: `+$322.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$322.4201`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0799` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$322.7417` | +100.1% | Stock moved from $339.50 to $343.99 (+4.4900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$11.6043` | +3.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$6.6174` | +2.1% | IV moved +0.20 vol pts (32.90% → 32.93%) |
| **Theta decay (Δt · Theta)** | `-$18.5432` | -5.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0799` | +0.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$322.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0799` (0.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0043`
* Combined: `-$0.0043` | Residual after: `+$3.2293`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$4.4900` vs next cash dividend `+$0.2700` (gap `+$4.7600`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$23.9250` vs `+$24.1274` (gap `-$0.2024`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.2032`
* **Dividend coverage** (dividend / time value): `0.05` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.0662`
* **Residual (Taylor ε)**: `+$0.0008`
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
* Watch whether a larger spot swing or stronger convexity starts to dominate the same contract’s next revaluation, since Taylor truncation can matter more if the move accelerates.
* Confirm whether any later tape or corporate-specific catalyst appears, because no relevant headlines were retrieved in this run.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.05 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$170.0000` (->1000%)
* **Model ΔP**: `-$170.0000`
* **Primary drivers**: **Delta PnL** (81%) and **Theta decay** (8%) and **Gamma PnL** (7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best explained by the position’s delta exposure to the underlying share rally, with gamma as a smaller reinforcing effect and theta partly offsetting the decline in value. The residual is minimal, so the Taylor decomposition is a clean fit; there is no named news catalyst in the blotter, and the observation lock means no auxiliary tape story should be invented. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the attribution is internally consistent and the residual is small, but observation reliability is flagged as false and there are no retrieved headlines to independently challenge the factor story. The move sits in the modeled spot-sensitivity bucket, while the reported volatility change is too small to justify a separate Vega narrative under the supplied suppressions.

---

## 2. Observation Lock

* **As-of**: `2026-10-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.5%)
* **IV move**: +0.25 vol pts vs noise band ±0.26 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$170.0000`
* **Model ΔP (engine)**: `-$170.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$170.7177`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.7177` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$165.8478` | +97.6% | Stock moved from $339.50 to $343.99 (+4.4900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$14.9630` | +8.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$6.8155` | +4.0% | IV moved +0.18 vol pts (26.81% → 27.06%) |
| **Theta decay (Δt · Theta)** | `+$16.9086` | -9.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.7177` | -0.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$170.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.7177` (0.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0038`
* Combined: `+$0.0038` | Residual after: `+$1.6962`

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
* Higher-order effects and the model’s chosen approximation can still slightly distort the attribution, but the residual is small here.
* No catalyst or microstructure mechanism is evidenced in the retrieved tape, so do not infer borrow, squeeze, or IV-crush dynamics from this run.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-10-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$5.5000` (->1000%)
* **Model ΔP**: `-$5.5000`
* **Primary drivers**: **Theta decay** (67%) and **Vega PnL** (20%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is dominated by time decay in the option’s value, with only a minor contribution from the small spot drift and limited gamma support. The residual is consistent with higher-order effects and the engine’s path-repricing gap, while the American feature is not adding meaningful early-exercise value at these marks. No headline catalyst is available here, so the tape reads as a pure model revaluation rather than a news-led move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is moderate because the dominant Taylor driver is clear, but observation quality is flagged as unreliable and the residual share is elevated. There are no retrieved headlines or named microstructure mechanisms to support a Layer B catalyst story, and the Vega narrative is suppressed by the data-quality settings.

---

## 2. Observation Lock

* **As-of**: `2026-10-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 40.0%)
* **IV move**: +0.10 vol pts vs noise band ±0.67 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$5.5000`
* **Model ΔP (engine)**: `-$5.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$4.4742`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.0258` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (18.7%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.1966` | +3.6% | Stock moved from $335.26 to $335.19 (-0.0700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0021` | -0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$1.8028` | -32.8% | IV moved +0.92 vol pts (26.07% → 26.17%) |
| **Theta decay (Δt · Theta)** | `-$6.0826` | +110.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.0258` | +18.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$5.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.0258` (18.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0008`
* Combined: `+$0.0008` | Residual after: `-$0.0558`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0606`
* **spot**: `-$0.0007`
* **vol**: `+$0.0063`
* **rate**: `-$0.0000`
* Step sum: `-$0.0550` | Model ΔP: `-$0.0550` | Audit residual: `+$0.0000`

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
* Watch whether the residual remains elevated versus the full revaluation path, since truncation and boundary effects can still distort the Greek attribution.
* No catalyst-specific follow-up is available from the digest; with no retrieved headlines, there is no borrow, squeeze, or IV-crush mechanism to verify.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-10-21` | **Status**: Verified by QuantLib (fdm_local_vol)

---

## 1. Headline

* **Mark MTM PnL**: `+$117.5000` (-558.7%)
* **Model ΔP**: `-$88.0394`
* **Primary drivers**: **Vega PnL** (37%) and **Theta decay** (13%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is dominated by the residual rather than a clean Greek bucket, with the Taylor decomposition leaving a large unexplained gap after spot, vega, and theta effects. The spot change was minimal, and the observation lock plus calibration limitations mean the full revaluation should be treated as the more reliable description than any single Greek line. Because the diagnostics suppress a vega narrative and no named catalyst was retrieved, there is no supported Layer B news mechanism to add. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is moderate because the desk run flags low attribution coverage, a high residual band, and multiple calibration limitations, while observation reliability is false. That makes the Greek split only a reference view and leaves the full revaluation as the safer read; there is also no headline evidence to anchor a catalyst story.

---

## 2. Observation Lock

* **As-of**: `2026-10-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 13.9%)
* **IV move**: +21.02 vol pts vs noise band ±66.57 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$117.5000`
* **Model ΔP (engine)**: `-$88.0394`
* **Model vs Mark gap**: `-$205.5394` (+233.5% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$104.8083`

* **Method residual (ε_method)**: `-$192.8477` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$205.5394` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (219.0%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$5.9395` | -6.7% | Stock moved from $335.26 to $335.19 (-0.0700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0042` | -0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$149.8387` | -170.2% | IV moved +21.02 vol pts (45.17% → 66.19%) |
| **Theta decay (Δt · Theta)** | `-$50.9742` | +57.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$192.8477` | +219.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$88.0394** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$192.8477` (219.0% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.3803`
* Combined: `+$0.3803` | Residual after: `-$1.2607`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.9482`
* **spot**: `+$0.0680`
* **vol**: `+$0.0000`
* **rate**: `+$0.0002`
* Step sum: `-$0.8801` | Model ΔP: `-$0.8804` | Audit residual: `-$0.0003`

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
* Treat the Taylor decomposition as reference only and lean on the full revaluation, since calibration and surface-shift limitations can distort the attribution.
* Watch for any later evidence of quote noise or surface recalibration that could explain the residual, but do not infer a squeeze, borrow, or implied-volatility story from the current tape.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$42.0000` (+>1000%)
* **Model ΔP**: `+$42.0000`
* **Primary drivers**: **Delta PnL** (63%) and **Theta decay** (19%) and **Vega PnL** (13%).
* **Verdict**: The position’s move was driven primarily by the underlying spot rise, which reduced the value of the put and was only modestly offset by time decay. Second-order effects were smaller: gamma and the slight implied-vol uptick both worked against the position, while the residual was negligible, so the Taylor decomposition is consistent with the model revaluation. The American early-exercise feature is not a meaningful contributor here because the premium versus the European cross-check is negligible.
* **Confidence**: **Medium** — The attribution is well covered by the blotter and the residual is tiny, but the move is still a Taylor decomposition rather than a full market-mark explanation. There are no relevant headlines to add a separate catalyst layer, and the early-exercise check indicates no material boundary effect.

---

## 2. Observation Lock

* **As-of**: `2026-10-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.1%)
* **IV move**: +0.24 vol pts vs noise band ±0.03 pts (exceeds noise band)
* **Prior observation**: `2026-10-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$42.0000`
* **Model ΔP (engine)**: `+$42.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$42.0849`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0849` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$40.7890` | +97.1% | Stock moved from $769.05 to $773.09 (+4.0400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$3.1104` | -7.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$8.1649` | -19.4% | IV moved +0.21 vol pts (20.26% → 20.50%) |
| **Theta decay (Δt · Theta)** | `+$12.5711` | +29.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0849` | -0.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$42.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0849` (0.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0076`
* Combined: `-$0.0076` | Residual after: `-$0.4124`

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

* Watch for higher-order truncation only if spot movement widens materially relative to the current move; otherwise the delta-led revaluation should remain the cleanest explanation.
* No layer-B catalyst is available from the feed, so there is no borrow, squeeze, or IV-crush narrative to verify from headlines.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$85.5000` (+>1000%)
* **Model ΔP**: `+$85.5000`
* **Primary drivers**: **Delta PnL** (70%) and **Theta decay** (12%) and **Vega PnL** (11%).
* **Verdict**: The position was led by a spot-driven revaluation, with the option’s directional exposure doing most of the work and second-order convexity adding a smaller lift. Vega also contributed modestly as implied volatility edged higher, while theta was a drag; the remaining gap is negligible and consistent with normal Taylor truncation.
* **Confidence**: **Medium** — The blotter’s factor decomposition is internally consistent and the residual is very small, so the modeled attribution is stable. Confidence is capped at medium because the feed is limited to a mark-based run with no retrieved headlines, so there is no external catalyst layer to corroborate beyond the price and volatility move.

---

## 2. Observation Lock

* **As-of**: `2026-10-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.1%)
* **IV move**: +0.24 vol pts vs noise band ±0.03 pts (exceeds noise band)
* **Prior observation**: `2026-10-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$85.5000`
* **Model ΔP (engine)**: `+$85.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$85.7511`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.2511` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.3%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$78.3988` | +91.7% | Stock moved from $769.05 to $773.09 (+4.0400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$8.3917` | +9.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$12.0255` | +14.1% | IV moved +0.20 vol pts (12.56% → 12.80%) |
| **Theta decay (Δt · Theta)** | `-$13.0649` | -15.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.2511` | -0.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$85.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.2511` (0.3% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0140`
* Combined: `+$0.0140` | Residual after: `+$0.8410`

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

* Monitor whether a larger spot continuation or reversal makes the current delta-led attribution less representative as higher-order terms become more important.
* Watch for any follow-up change in implied volatility, since the current move included a small vol uptick even though no catalyst headline set was available.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$43.0000` (->1000%)
* **Model ΔP**: `-$43.0000`
* **Primary drivers**: **Delta PnL** (84%) and **Gamma PnL** (9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven primarily by the downward move in the underlying, with the call’s positive delta producing the main model revaluation. Gamma softened the decline and theta added a smaller decay effect, while the residual stayed minor and consistent with a clean Taylor fit. There is no separate headline catalyst layer here; the observation lock and empty digest leave the move explained by the modeled spot shift rather than news. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The modeled attribution is well covered and the residual is small, but observation quality is flagged as unreliable and there are no retrieved headlines to test a catalyst overlay. Vega should be treated cautiously because the setup suppresses a volatility narrative and the IV change was small.

---

## 2. Observation Lock

* **As-of**: `2026-10-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 15.6%)
* **IV move**: +0.29 vol pts vs noise band ±1.40 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$43.0000`
* **Model ΔP (engine)**: `-$43.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$43.2101`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.2101` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.5%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$45.0726` | +104.8% | Stock moved from $44.54 to $43.56 (-0.9800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$5.0341` | -11.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.8521` | +2.0% | IV moved -0.17 vol pts (29.59% → 29.88%) |
| **Theta decay (Δt · Theta)** | `-$2.3194` | +5.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.2101` | -0.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$43.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.2101` (0.5% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0003`
* Combined: `+$0.0003` | Residual after: `-$0.4303`

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
* Spot-driven truncation risk remains the main check: if the move is larger than the linear approximation, the full revaluation can differ from the Taylor split.
* No catalyst layer was identified in the digest; verify quote quality and the official marks before leaning on any news-based explanation.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$3.0000` (+>1000%)
* **Model ΔP**: `+$3.0000`
* **Primary drivers**: **Vega PnL** (68%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position’s move was driven mainly by a sharp rise in implied volatility, with spot contributing only a small secondary effect and theta a modest drag. The remaining gap is consistent with higher-order convexity and model-path effects rather than a separate named catalyst. No relevant headlines were retrieved, so there is no supported Layer B event to add beyond the modeled revaluation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The dominant factor is clear from the blotter and the vol move is extreme, but observation reliability is flagged as weak and the attribution coverage is low. The residual is sizable enough that Taylor truncation or surface/path effects likely matter, so the diagnostic should stay at the modeled-revaluation level and avoid over-claiming a news cause.

---

## 2. Observation Lock

* **As-of**: `2026-10-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 155.6%)
* **IV move**: +35.94 vol pts vs noise band ±30.70 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-20`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$3.0000`
* **Model ΔP (engine)**: `+$3.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$2.1238`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.8762` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (29.2%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.0551` | +1.8% | Stock moved from $1.40 to $1.41 (+0.0100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0007` | +0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$2.1414` | +68.1% | IV moved +34.16 vol pts (137.50% → 173.44%) |
| **Theta decay (Δt · Theta)** | `-$0.0734` | +2.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.8762` | +27.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$3.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.8762` (29.2% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.01).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (Layer 3) — reference only, see Regime above
* other second-order: `+$0.0097`
* Combined: `+$0.0097` | Residual after: `+$0.0203`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0007`
* **spot**: `+$0.0005`
* **vol**: `+$0.0302`
* **rate**: `-$0.0000`
* Step sum: `+$0.0300` | Model ΔP: `+$0.0300` | Audit residual: `+$0.0000`

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
* Monitor whether the model residual remains elevated on the next revaluation, as convexity and path effects can stay material when the spot move is small but vol reprices sharply.
* With no supported headline set, do not force a borrow, squeeze, or IV-crush narrative; verify whether the implied-vol repricing persists in the next mark cycle.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0770 | level_proxy(t) = 0.1665
* Δskew = -0.0000 | Δlevel = +0.0024
* Put 715 delta=-0.0853 | Call 795 delta=0.2374
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
