# Live book run — 2026-10-28

Run `2026-10-28-1793236521`. 6/8 legs completed, 2 failed. `legs_narrated=6` `legs_silent=0` `llm_calls=9`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-28` | **Positions**: 6 | **Tickers**: AAPL, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$82.0000`
* **Total Model PnL**: `-$82.0000`
* **Aggregate model vs mark gap**: `-$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `-$280.0000` |
| 2 | `AAPL 350C 2026-11-20` | `+$180.0000` |
| 3 | `SPY 715P 2026-11-20` | `+$29.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$227.1155` |
| Gamma | `+$5.4560` |
| Vega | `-$520.9809` |
| Theta | `-$6.2714` |
| Residual | `+$212.6807` |

### Notable underlyings

* **AAPL**: `-$100.0000` aggregate option PnL
* **SPY**: `+$38.5000` aggregate option PnL
* **VZ**: `-$23.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-28` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$280.0000` (->1000%)
* **Model ΔP**: `-$280.0000`
* **Primary drivers**: **Vega PnL** (59%) and **Delta PnL** (20%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model move is dominated by an implied-volatility decline, with spot higher and theta a smaller drag. However, the observation is locked and the desk flags the Vega narrative as suppressed, so the cleanest read is a model revaluation led by the volatility reset rather than a news-driven catalyst story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is limited by the unreliable observation flag, the high residual share, and the fact that the surface diagnostics show a failed American FD surface under Heston. There are no retrieved headlines and the digest explicitly says not to invent a squeeze, borrow, or IV-crush narrative from outside the blotter, so the attribution should stay at the model-repricing level.

---

## 2. Observation Lock

* **As-of**: `2026-10-28` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 6.3%)
* **IV move**: -2.22 vol pts vs noise band ±8.53 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-27`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$280.0000`
* **Model ΔP (engine)**: `-$280.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$498.9377`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$218.9377` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (78.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$232.9236` | -83.2% | Stock moved from $343.91 to $347.10 (+3.1900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$4.7041` | -1.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$709.2623` | +253.3% | IV moved -24.34 vol pts (37.91% → 35.69%) |
| **Theta decay (Δt · Theta)** | `-$27.3031` | +9.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$218.9377` | -78.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$280.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$218.9377` (78.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$1.1741`
* Combined: `+$1.1741` | Residual after: `-$3.9741`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2733`
* **spot**: `+$2.3866`
* **vol**: `-$4.9113`
* **rate**: `-$0.0087`
* Step sum: `-$2.8067` | Model ΔP: `-$2.8000` | Audit residual: `+$0.0067`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$3.1900` vs next cash dividend `+$0.2700` (gap `+$3.4600`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$22.9250` vs `+$23.1163` (gap `-$0.1913`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1921`
* **Dividend coverage** (dividend / time value): `0.33` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$7.0926`
* **Residual (Taylor ε)**: `+$2.1894`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Watch whether the high residual reflects higher-order truncation or surface-repricing effects rather than a clean one-factor decomposition.
* Verify the dividend and ex-div setup, but treat this as a carry and theta case rather than an early-exercise case.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.33 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-28` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$180.0000` (+>1000%)
* **Model ΔP**: `+$180.0000`
* **Primary drivers**: **Vega PnL** (64%) and **Delta PnL** (30%) and **Theta decay** (5%).
* **Verdict**: The move is dominated by a modeled volatility reprice: the option benefited from a lower implied-volatility input even as the underlying drifted higher, while delta and gamma were secondary offsets and theta helped slightly. The residual is minimal, so the Greek decomposition is tight and the headline story stays on the full revaluation rather than any larger hidden effect. The only Apple-specific headline is an option-chain reference, which supports a surface-driven read but does not supply a separate event catalyst.
* **Confidence**: **Medium** — Confidence is medium because the attribution is clean and observation quality is reliable, but the news set is thin and does not provide a distinct issuer catalyst. The dominant driver is clear from the blotter, though the role of the headline is only contextual rather than causal.

---

## 2. Observation Lock

* **As-of**: `2026-10-28` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.7%)
* **IV move**: -0.70 vol pts vs noise band ±0.07 pts (exceeds noise band)
* **Prior observation**: `2026-10-27`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$180.0000`
* **Model ΔP (engine)**: `+$180.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$180.1621`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.1621` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$140.4380` | -78.0% | Stock moved from $343.91 to $347.10 (+3.1900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$7.1159` | -4.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$302.7281` | +168.2% | IV moved -8.71 vol pts (28.99% → 28.30%) |
| **Theta decay (Δt · Theta)** | `+$24.9879` | +13.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.1621` | -0.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$180.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.1621` (0.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0474`
* Combined: `-$0.0474` | Residual after: `-$1.7526`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: The only Apple-specific headline is an option-chain reference with no explicit event catalyst. The other items are sector/market background rather than direct Apple news._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Apple (AAPL) Option Chain | Market Chameleon** _(Source: Market Chameleon)_
   An option-chain page for Apple; it is directly about the target name but contains no standalone news catalyst in the headline.

_Peer / sector background (indirect context, not a required catalyst):_

2. **HubSpot options signal 12% move on Nov. 4 earnings report** _(Source: Investing.com)_
   A peer software name is mentioned in an options-activity context, which can serve as sector background but is not about Apple.
3. **High IV Stocks Today: Live Scan + 10 That Run Hot | ApexVol** _(Source: ApexVol)_
   A broad implied-volatility scan is market context only and does not specifically concern Apple.

---

## 7. Risk Watchlist

* Check whether the next reprice is still dominated by surface movement or whether spot sensitivity starts to outweigh the volatility effect.
* Verify that the Apple-specific options tape remains the relevant context, since the broader headlines are sector background rather than an issuer event.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-28` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$29.0000` (+>1000%)
* **Model ΔP**: `+$29.0000`
* **Primary drivers**: **Delta PnL** (49%) and **Vega PnL** (28%) and **Theta decay** (17%).
* **Verdict**: The position’s move was driven primarily by the underlying spot drift, with the modeled delta term dominating the day’s revaluation. Gamma offset some of that move, while the smaller volatility change and residual only added minor adjustment noise to the full reprice.
* **Confidence**: **Medium** — Confidence is supported by a high coverage attribution and a reliable observation set, but the run still carries a medium residual band and the surface diagnostics note an American surface limitation. There were no relevant headlines or named microstructure mechanisms to add a catalyst layer, and the early-exercise premium is negligible.

---

## 2. Observation Lock

* **As-of**: `2026-10-28` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.3%)
* **IV move**: +0.24 vol pts vs noise band ±0.04 pts (exceeds noise band)
* **Prior observation**: `2026-10-27`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$29.0000`
* **Model ΔP (engine)**: `+$29.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$27.1515`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.8485` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (6.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$39.6180` | +136.6% | Stock moved from $765.37 to $769.66 (+4.2900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$3.7051` | -12.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$22.3154` | -76.9% | IV moved +0.69 vol pts (21.81% → 22.05%) |
| **Theta decay (Δt · Theta)** | `+$13.5540` | +46.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.8485` | +6.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$29.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.8485` (6.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0217`
* Combined: `-$0.0217` | Residual after: `-$0.2683`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1354`
* **spot**: `-$0.3430`
* **vol**: `+$0.1887`
* **rate**: `+$0.0017`
* Step sum: `-$0.2880` | Model ΔP: `-$0.2900` | Audit residual: `-$0.0020`

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

* Watch for Taylor truncation and any path-dependent full-reprice effects if spot movement becomes larger or the surface remains unstable.
* No catalyst layer was identified from the digest; there is no borrow, squeeze, or implied-volatility headline to verify.

---

### Position 4 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-28` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$9.5000` (+418.5%)
* **Model ΔP**: `+$9.5000`
* **Primary drivers**: **Delta PnL** (48%) and **Vega PnL** (32%) and **Theta decay** (10%).
* **Verdict**: The position’s move was driven primarily by the favorable spot shift, with gamma adding some convexity support while vega and theta offset part of the gain. The remaining gap versus the modeled revaluation is consistent with Taylor truncation and higher-order effects rather than a separate catalyst, and there are no retrieved headlines to add a Layer B story.
* **Confidence**: **Medium** — Confidence is medium because the dominant modeled driver is clear, but the residual share is elevated and the surface diagnostics show the simpler approximation leaves meaningful unexplained move. Observation is reliable and the IV source is a complete chain mark, yet there are no relevant headlines or microstructure tokens to support an auxiliary event-based explanation.

---

## 2. Observation Lock

* **As-of**: `2026-10-28` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.1%)
* **IV move**: -0.43 vol pts vs noise band ±0.05 pts (exceeds noise band)
* **Prior observation**: `2026-10-27`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$9.5000`
* **Model ΔP (engine)**: `+$9.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$15.5664`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$6.0664` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (63.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$68.8473` | +724.7% | Stock moved from $765.37 to $769.66 (+4.2900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$8.2192` | +86.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$46.6952` | -491.5% | IV moved -0.98 vol pts (12.97% → 12.54%) |
| **Theta decay (Δt · Theta)** | `-$14.8049` | -155.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$6.0664` | -63.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$9.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$6.0664` (63.9% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0573`
* Combined: `-$0.0573` | Residual after: `+$0.1523`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1483`
* **spot**: `+$0.7503`
* **vol**: `-$0.5068`
* **rate**: `-$0.0038`
* Step sum: `+$0.0914` | Model ΔP: `+$0.0950` | Audit residual: `+$0.0036`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Higher-order convexity and truncation can still distort the Greek-based attribution when the residual remains elevated, so the full revaluation is the cleaner reference.
* No relevant catalyst, borrow, squeeze, or IV-crush signal was retrieved, so there is nothing event-driven to verify in the tape.

---

### Position 5 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-28` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$23.5000` (->1000%)
* **Model ΔP**: `-$23.5000`
* **Primary drivers**: **Vega PnL** (58%) and **Delta PnL** (32%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model repricing is dominated by a volatility reset on the call: the spot move helped, but it was outweighed by the drop in implied volatility, with second-order spot effects and decay playing smaller supporting roles. Because the observation is locked and no relevant headlines were retrieved, there is no separate catalyst layer to add beyond the blotter’s own volatility-driven explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is capped because observation quality is flagged as unreliable and the residual is not trivial, so the Taylor breakdown is only a reference view. The code also suppresses a Vega narrative, and there are no retrieved headlines to validate an external catalyst, so the explanation must stay anchored to the model repricing rather than a news claim.

---

## 2. Observation Lock

* **As-of**: `2026-10-28` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 34.0%)
* **IV move**: +1.86 vol pts vs noise band ±2.03 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-27`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$23.5000`
* **Model ΔP (engine)**: `-$23.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$20.7313`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$2.7687` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (11.8%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$25.9985` | -110.6% | Stock moved from $43.10 to $43.93 (+0.8300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$3.3472` | -14.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$47.4550` | +201.9% | IV moved -12.14 vol pts (26.61% → 28.47%) |
| **Theta decay (Δt · Theta)** | `-$2.6221` | +11.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$2.7687` | +11.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$23.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$2.7687` (11.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0345`
* Combined: `-$0.0345` | Residual after: `-$0.2005`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0262`
* **spot**: `+$0.2917`
* **vol**: `-$0.5005`
* **rate**: `-$0.0003`
* Step sum: `-$0.2353` | Model ΔP: `-$0.2350` | Audit residual: `+$0.0003`

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
* Check whether higher-order convexity and surface curvature are still distorting the Taylor split relative to the full revaluation.
* Verify the vol reset against the next surface mark; there is no verified borrow, squeeze, or IV-crush headline context to add here.

---

### Position 6 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-28` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$3.0000` (+>1000%)
* **Model ΔP**: `+$3.0000`
* **Primary drivers**: **Vega PnL** (64%) and **Delta PnL** (5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move was dominated by a revaluation of implied volatility in the option model, with spot contributing a smaller secondary lift and theta a modest drag. The remaining gap is consistent with higher-order effects and Taylor truncation around a large volatility move, while the American early-exercise feature was not a meaningful factor at these marks. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is capped by the unreliable observation flag and the high residual share, so the Greek split should be treated as a reference view rather than a complete explanation. There are no retrieved headlines or named microstructure mechanisms to add a separate catalyst layer, and the early-exercise premium is negligible.

---

## 2. Observation Lock

* **As-of**: `2026-10-28` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 155.6%)
* **IV move**: +37.50 vol pts vs noise band ±32.93 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-27`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$3.0000`
* **Model ΔP (engine)**: `+$3.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$2.1082`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.8918` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (29.7%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.1661` | +5.2% | Stock moved from $1.37 to $1.40 (+0.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0065` | +0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$2.0189` | +63.8% | IV moved +34.92 vol pts (146.88% → 184.38%) |
| **Theta decay (Δt · Theta)** | `-$0.0832` | +2.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.8918` | +28.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$3.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.8918` (29.7% of |model|)
* **Regime**: the move this day is outside the range where a Taylor expansion is valid (r_spot = 0.04).
  The Greek decomposition below is shown for reference; the headline attribution comes from full revaluation.

### Second-order Taylor (Layer 3) — reference only, see Regime above
* other second-order: `+$0.0096`
* Combined: `+$0.0096` | Residual after: `+$0.0204`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0008`
* **spot**: `+$0.0017`
* **vol**: `+$0.0292`
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
* Model attribution can still be distorted by truncation and full-surface repricing when volatility moves are extreme.
* No headline-backed borrow, squeeze, or IV-crush mechanism was retrieved, so there is no independent catalyst layer to verify from the tape.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0950 | level_proxy(t) = 0.1730
* Δskew = +0.0067 | Δlevel = -0.0010
* Put 715 delta=-0.0787 | Call 795 delta=0.1777
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **jpm_straddle_call** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-10-30, 2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
- **jpm_straddle_put** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-10-30, 2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
