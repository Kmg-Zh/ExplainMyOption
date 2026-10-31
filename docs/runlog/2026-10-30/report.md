# Live book run — 2026-10-30

Run `2026-10-30-1793409306`. 6/8 legs completed, 2 failed. `legs_narrated=6` `legs_silent=0` `llm_calls=10`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-30` | **Positions**: 6 | **Tickers**: AAPL, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$248.5000`
* **Total Model PnL**: `+$572.0266`
* **Aggregate model vs mark gap**: `+$820.5266`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `+$523.0266` |
| 2 | `AAPL 350C 2026-11-20` | `+$150.0000` |
| 3 | `SPY 715P 2026-11-20` | `-$102.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$116.7466` |
| Gamma | `+$1.2037` |
| Vega | `+$456.9504` |
| Theta | `+$9.2452` |
| Residual | `-$12.1193` |

### Notable underlyings

* **AAPL**: `+$673.0266` aggregate option PnL
* **SPY**: `-$152.5000` aggregate option PnL
* **VZ**: `+$53.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$297.5000` (+>1000%)
* **Model ΔP**: `+$523.0266`
* **Primary drivers**: **Delta PnL** (65%) and **Vega PnL** (26%).
* **Verdict**: The move is primarily explained by delta, with spot lifting the call’s intrinsic sensitivity and gamma adding a smaller convexity boost. Vega also supported the revaluation because implied volatility moved higher, while theta was a modest drag; the remaining gap is consistent with model truncation and surface fit limits rather than a separate catalyst. No relevant headlines were retrieved, so there is no Layer B mechanism to add beyond the modeled revaluation.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is high and the observation is reliable, but the residual is not zero and the surface diagnostics show calibration limits. The news layer is empty, so there is no headline-based catalyst to reinforce or challenge the modeled driver, and the early-exercise premium is not material.

---

## 2. Observation Lock

* **As-of**: `2026-10-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 10.0%)
* **IV move**: +6.11 vol pts vs noise band ±4.91 pts (exceeds noise band)
* **Prior observation**: `2026-10-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$297.5000`
* **Model ΔP (engine)**: `+$523.0266`
* **Model vs Mark gap**: `+$820.5266` (+156.9% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$537.4626`

* **Method residual (ε_method)**: `-$14.4360` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$820.5266` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$388.7431` | +74.3% | Stock moved from $343.83 to $348.91 (+5.0800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$13.5540` | +2.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$158.3473` | +30.3% | IV moved +6.11 vol pts (34.66% → 40.77%) |
| **Theta decay (Δt · Theta)** | `-$23.1818` | -4.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$14.4360` | -2.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$523.0266** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$14.4360` (2.8% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.1146`
* Combined: `-$0.1146` | Residual after: `+$5.3449`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2320`
* **spot**: `+$4.0396`
* **vol**: `+$1.4226`
* **rate**: `-$0.0035`
* Step sum: `+$5.2267` | Model ΔP: `+$5.2303` | Audit residual: `+$0.0036`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$5.0800` vs next cash dividend `+$0.2700` (gap `+$5.3500`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$28.7604` vs `+$28.9189` (gap `-$0.1585`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1595`
* **Dividend coverage** (dividend / time value): `0.06` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$1.5835`
* **Residual (Taylor ε)**: `-$0.1444`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%
  * `american_dividend_exercise_check` — path_reprice outranks ex-div window
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* Watch whether the model remains stable under full-surface reprice and whether the residual persists, since truncation and surface-fit issues can still distort the Greek split.
* Monitor the implied volatility move and quote quality for signs of IV crush or further expansion, but no named catalyst is available from the retrieved tape.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.06 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$150.0000` (+>1000%)
* **Model ΔP**: `+$150.0000`
* **Primary drivers**: **Vega PnL** (57%) and **Delta PnL** (35%).
* **Verdict**: The move is dominated by the model’s vega bucket: the option lost value as implied volatility rose sharply in the blotter’s prior-to-current comparison, while the spot rise was not large enough to offset that revaluation on its own. Delta and gamma were secondary drags, and the small residual is consistent with a clean Taylor explanation rather than a meaningful unexplained gap. With no relevant headlines or named catalyst tokens in the digest, this is best read as a volatility-led reprice inside the model, not a news-driven microstructure story.
* **Confidence**: **Medium** — Confidence is medium because the attribution is internally consistent and the residual is small, but the surface diagnostics note a failed American surface under Heston and the feed has no relevant news catalyst to independently challenge the model. The IV move is the clearest driver in the blotter, while the spot move is comparatively modest, so the factor story is strong but not fully corroborated by external tape.

---

## 2. Observation Lock

* **As-of**: `2026-10-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.1%)
* **IV move**: +2.48 vol pts vs noise band ±0.60 pts (exceeds noise band)
* **Prior observation**: `2026-10-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$150.0000`
* **Model ΔP (engine)**: `+$150.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$148.5161`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.4839` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$225.1436` | -150.1% | Stock moved from $343.83 to $348.91 (+5.0800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$17.0822` | -11.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$362.0990` | +241.4% | IV moved -10.87 vol pts (29.32% → 31.81%) |
| **Theta decay (Δt · Theta)** | `+$28.6430` | +19.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.4839` | +1.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$150.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.4839` (1.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.1060`
* Combined: `-$0.1060` | Residual after: `-$1.3940`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. [Decoding GOOGL Implied Volatility & Term Structure Metrics o... - moomoo Community](https://www.moomoo.com/community/feed/decoding-googl-implied-volatility-term-structure-metrics-on-moomoo-117510901137414)

---

## 7. Risk Watchlist

* Verify whether the clean Taylor fit remains stable if the full surface or alternative surface calibration is used, since the current run relied on the model reprice and not a fresh independent mark.
* Watch for any subsequent implied volatility normalization or expansion in the absence of a named catalyst, since the current move was dominated by the volatility revaluation inside the model.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$102.5000` (->1000%)
* **Model ΔP**: `-$102.5000`
* **Primary drivers**: **Vega PnL** (62%) and **Delta PnL** (19%) and **Theta decay** (11%).
* **Verdict**: The move is explained first by the modeled volatility reprice: the put gained on the implied-volatility decline, with spot and gamma playing smaller supporting roles and theta partly offsetting the loss. The remaining gap is consistent with higher-order truncation on a short-dated option, while the news layer offers only generic options education and an iv crush backdrop rather than a SPY-specific catalyst.
* **Confidence**: **Medium** — Confidence is supported by the code-designated dominant driver, reliable observation, and a high attribution coverage band. Confidence is not higher because the residual is medium, the vol move is only modest, and the kept headline set is generic rather than SPY-specific, so the catalyst layer is background rather than a direct proof of causality.

---

## 2. Observation Lock

* **As-of**: `2026-10-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.4%)
* **IV move**: -0.90 vol pts vs noise band ±0.06 pts (exceeds noise band)
* **Prior observation**: `2026-10-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$102.5000`
* **Model ΔP (engine)**: `-$102.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$93.5001`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$8.9999` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (8.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$24.6225` | +24.0% | Stock moved from $772.31 to $769.36 (-2.9500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$1.4870` | +1.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$82.4380` | +80.4% | IV moved +2.83 vol pts (22.56% → 21.66%) |
| **Theta decay (Δt · Theta)** | `+$15.0473` | -14.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$8.9999` | +8.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$102.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$8.9999` (8.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.1624`
* Combined: `+$0.1624` | Residual after: `+$0.8626`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1504`
* **spot**: `+$0.2480`
* **vol**: `+$0.9271`
* **rate**: `+$0.0012`
* Step sum: `+$1.0259` | Model ΔP: `+$1.0250` | Audit residual: `-$0.0009`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: No SPY-linked headlines were present. The items provided are either unrelated issuer content or generic options/volatility discussion, so they were not tagged as relevant or background for SPY._
_Intel triage discarded 3 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. [V Stock Before Earnings: Why Calls Lose on a ±3.4% Move](https://earnings-watcher.com/wiki/v-stock-before-earnings)
2. [How a Volatility Crush Can Derail an Earnings Trade](https://www.schaeffersresearch.com/content/education/2026/10/28/how-a-volatility-crush-can-derail-an-earnings-trade)
3. [How do you handle high implied volatility when trading F&O?](https://www.facebook.com/groups/2750702498288374/posts/40543601425238341)

---

## 7. Risk Watchlist

* Monitor whether short-dated truncation and the full-surface reprice remain the main source of any remaining attribution gap.
* Keep watching the iv crush backdrop and implied volatility behavior, since the kept tape did not provide a SPY-specific catalyst.

---

### Position 4 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$50.0000` (->1000%)
* **Model ΔP**: `-$50.0000`
* **Primary drivers**: **Delta PnL** (50%) and **Vega PnL** (23%) and **Theta decay** (12%).
* **Verdict**: The position was driven primarily by the option’s delta exposure to a modest lower spot, with gamma partly offsetting and theta adding decay. A smaller lower implied volatility also weighed on the mark, while the remaining gap is consistent with higher-order model effects rather than a separate catalyst. There were no relevant headlines in the digest, so the run is a model-based attribution only.
* **Confidence**: **Medium** — Confidence is moderate because the attribution is supported by reliable marks and a high-coverage Taylor breakdown, but the residual is in the medium band and the spot and vol changes are both relatively small, leaving some room for truncation and path effects. No relevant headlines were retrieved, so there is no independent catalyst layer to confirm or challenge the model story.

---

## 2. Observation Lock

* **As-of**: `2026-10-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.4%)
* **IV move**: +2.40 vol pts vs noise band ±0.06 pts (exceeds noise band)
* **Prior observation**: `2026-10-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$50.0000`
* **Model ΔP (engine)**: `-$50.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$56.0172`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$6.0172` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (12.0%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$35.8156` | +71.6% | Stock moved from $772.31 to $769.36 (-2.9500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$4.9331` | -9.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$16.3018` | +32.6% | IV moved -0.43 vol pts (10.80% → 13.20%) |
| **Theta decay (Δt · Theta)** | `-$8.8329` | +17.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$6.0172` | -12.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$50.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$6.0172` (12.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0302`
* Combined: `+$0.0302` | Residual after: `-$0.5302`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0885`
* **spot**: `-$0.2946`
* **vol**: `-$0.1175`
* **rate**: `-$0.0008`
* Step sum: `-$0.5014` | Model ΔP: `-$0.5000` | Audit residual: `+$0.0014`

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

* Watch whether the remaining gap is just Taylor truncation and path dependence versus a fuller revaluation effect in the same engine.
* No named catalyst was retrieved, so there is no borrow, squeeze, or IV-crush mechanism to verify from headlines.

---

### Position 5 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$53.5000` (+>1000%)
* **Model ΔP**: `+$53.5000`
* **Primary drivers**: **Vega PnL** (65%) and **Delta PnL** (23%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model revaluation is driven first and foremost by a volatility re-mark, with spot contributing a smaller lift and theta only partially offsetting the move. Because the observation is unreliable and there are no retrieved headlines, the tape supports a clean factor read but not a named external catalyst; the residual is consistent with higher-order effects around the surface reprice and the option’s short-dated convexity. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The factor decomposition is clear and the dominant driver is internally consistent with the model revaluation, but the run flags observation reliability concerns and a medium residual. No relevant headlines were retrieved, so there is no independent catalyst confirmation beyond the market move itself.

---

## 2. Observation Lock

* **As-of**: `2026-10-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 15.2%)
* **IV move**: +3.66 vol pts vs noise band ±2.00 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$53.5000`
* **Model ΔP (engine)**: `+$53.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$50.1672`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$3.3328` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (6.2%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$13.5851` | +25.4% | Stock moved from $43.18 to $43.66 (+0.4800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.2859` | +2.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$37.5629` | +70.2% | IV moved +10.49 vol pts (25.68% → 29.35%) |
| **Theta decay (Δt · Theta)** | `-$2.2666` | -4.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$3.3328` | +6.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$53.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$3.3328` (6.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0741`
* Combined: `+$0.0741` | Residual after: `+$0.4609`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0227`
* **spot**: `+$0.1470`
* **vol**: `+$0.4107`
* **rate**: `-$0.0002`
* Step sum: `+$0.5348` | Model ΔP: `+$0.5350` | Audit residual: `+$0.0002`

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
* Watch whether the residual stays contained on a full-surface reprice, since short-dated convexity can make the Taylor view understate the model move.
* Verify whether the implied volatility re-mark persists in later marks, because the current run has no headline support and the observation is flagged as unreliable.

---

### Position 6 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$2.0000` (->1000%)
* **Model ΔP**: `-$2.0000`
* **Primary drivers**: **Vega PnL** (78%) and **Theta decay** (6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is dominated by the sharp drop in implied volatility, which the blotter shows as the main Taylor driver for the option revaluation. Spot was unchanged, so delta and gamma did not materially contribute, while time decay was secondary and the remaining gap sits in the residual from higher-order effects and model limitations. With no retrieved headlines and no named catalyst tags, this is a model-led reprice rather than a news-led event, and the large residual is consistent with a noisy short-dated, high-vol regime. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is limited because observation is unreliable, the residual is large, and the surface diagnostics show failed American surface fits. The only clear driver supported by the blotter is the volatility move; there is no headline evidence to attribute a specific external catalyst, and the IV history is taken from the prior chain snapshot.

---

## 2. Observation Lock

* **As-of**: `2026-10-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 66.7%)
* **IV move**: -18.75 vol pts vs noise band ±8.66 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$2.0000`
* **Model ΔP (engine)**: `-$2.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$2.4828`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.4828` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (24.1%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.0000` | +0.0% | Stock moved from $1.42 to $1.42 (+0.0000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0000` | +0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$2.3190` | +78.2% | IV moved -24.75 vol pts (175.00% → 156.25%) |
| **Theta decay (Δt · Theta)** | `-$0.1638` | +5.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.4828` | +16.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$2.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.4828` (24.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0040`
* Combined: `+$0.0040` | Residual after: `-$0.0240`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0016`
* **spot**: `+$0.0000`
* **vol**: `-$0.0184`
* **rate**: `-$0.0000`
* Step sum: `-$0.0200` | Model ΔP: `-$0.0200` | Audit residual: `+$0.0000`

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
* Watch whether the residual remains elevated if the full surface is rechecked, since truncation and surface limitations can distort the modeled attribution.
* Verify whether the implied-vol move is being carried by the chain snapshot rather than a live news catalyst, because no relevant headlines were retrieved.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0847 | level_proxy(t) = 0.1743
* Δskew = -0.0329 | Δlevel = +0.0075
* Put 715 delta=-0.1136 | Call 795 delta=0.0755
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **jpm_straddle_call** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
- **jpm_straddle_put** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
