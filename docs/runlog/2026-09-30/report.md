# Live book run — 2026-09-30

Run `2026-09-30-1790817308`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=10`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-09-30` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$146.5000`
* **Total Model PnL**: `+$146.5000`
* **Aggregate model vs mark gap**: `-$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `+$230.0000` |
| 2 | `JPM 350P 2026-10-23` | `+$200.0000` |
| 3 | `JPM 350C 2026-10-23` | `-$125.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$474.4837` |
| Gamma | `+$7.7652` |
| Vega | `+$248.4989` |
| Theta | `-$33.8344` |
| Residual | `+$398.5540` |

### Notable underlyings

* **AAPL**: `+$130.0000` aggregate option PnL
* **JPM**: `+$74.5000` aggregate option PnL
* **SPY**: `-$66.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-09-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$230.0000` (+1402.4%)
* **Model ΔP**: `+$230.0000`
* **Primary drivers**: **Delta PnL** (43%) and **Vega PnL** (35%).
* **Verdict**: The position’s move was driven first by the spot decline in the underlying, which pushed the call lower in a delta-led way. That effect was partially offset by the higher implied volatility, so the overall model revaluation stayed positive even though the spot leg was adverse. The large unexplained piece is consistent with higher-order curvature and model truncation around a larger price/vol swing, while the Apple-specific headlines provide context but do not override the modeled driver.
* **Confidence**: **Medium** — Confidence is tempered by the high residual share and the fact that attribution coverage is limited, so the Greek split should be treated as a guide rather than a complete explanation. The data quality is otherwise reliable, IV prev source is current chain data, and the retained Apple headlines support issuer-specific context without forcing a different mechanism.

---

## 2. Observation Lock

* **As-of**: `2026-09-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 10.2%)
* **IV move**: +1.99 vol pts vs noise band ±1.98 pts (exceeds noise band)
* **Prior observation**: `2026-09-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$230.0000`
* **Model ΔP (engine)**: `+$230.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$86.9429`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$316.9429` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (137.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$753.3861` | -327.6% | Stock moved from $338.40 to $329.40 (-9.0000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$62.3562` | +27.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$610.8303` | +265.6% | IV moved +19.43 vol pts (29.22% → 31.21%) |
| **Theta decay (Δt · Theta)** | `-$6.7432` | -2.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$316.9429` | +137.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$230.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$316.9429` (137.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$1.2996`
* Combined: `+$1.2996` | Residual after: `+$1.0004`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0677`
* **spot**: `-$6.8057`
* **vol**: `+$9.1685`
* **rate**: `-$0.0085`
* Step sum: `+$2.2867` | Model ΔP: `+$2.3000` | Audit residual: `+$0.0133`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Intel note: Two headlines are directly about Apple and its product/senior leadership narrative, so they are kept as relevant. One AI/tech sector item is kept as background, while the Costco item is unrelated and discarded._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Apple's new CEO John Ternus plans on making some changes** _(Source: Yahoo Finance Video)_
   A video segment about leadership changes at Apple, the target company.
2. **Apple Predicted To Sell 6 Million iPhone Duo Handsets This Year** _(Source: Investor's Business Daily)_
   A report about Apple’s iPhone sales outlook and product demand.

_Peer / sector background (indirect context, not a required catalyst):_

3. **OpenAI is releasing newer models faster. Is that a good thing?** _(Source: Yahoo Finance Video)_
   A technology-sector discussion that could matter only indirectly to large-cap tech sentiment.

---

## 7. Risk Watchlist

* Reconcile the move with a full-surface reprice and hedge review, since the Taylor residual is large enough to suggest higher-order effects beyond the first-pass Greeks.
* Keep the Apple news flow on watch as context for sentiment, but treat it as background unless it becomes a clearer issuer-specific catalyst in the tape.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.02 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-09-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$100.0000` (-1793.7%)
* **Model ΔP**: `-$100.0000`
* **Primary drivers**: **Vega PnL** (49%) and **Delta PnL** (36%) and **Gamma PnL** (7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter’s modeled driver is Vega, but the observation lock means the IV line should be treated as proxied rather than narrated as a clean market repricing. The move also shows a large residual, so higher-order curvature and full-surface revaluation effects are part of the explanation rather than a pure single-Greek story. With no retrieved headlines or named mechanism tags, there is no separate Layer B catalyst to add. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is medium because the engine flags a strong residual and the observation is not reliable, so the Greek decomposition is only a reference view. The IV input is sourced from the prior chain and the blotter explicitly suppresses a Vega narrative, while there are no retrieved headlines to anchor a catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-09-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.8%)
* **IV move**: -0.00 vol pts vs noise band ±0.29 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$100.0000`
* **Model ΔP (engine)**: `-$100.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$161.6451`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$61.6451` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (61.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$320.3834` | -320.4% | Stock moved from $338.40 to $329.40 (-9.0000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$62.8228` | +62.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$429.1145` | +429.1% | IV moved +9.02 vol pts (26.58% → 26.58%) |
| **Theta decay (Δt · Theta)** | `+$9.9087` | -9.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$61.6451` | -61.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$100.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$61.6451` (61.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.2729`
* Combined: `-$0.2729` | Residual after: `+$1.2729`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0992`
* **spot**: `-$2.5842`
* **vol**: `+$3.6824`
* **rate**: `-$0.0047`
* Step sum: `+$0.9943` | Model ΔP: `+$1.0000` | Audit residual: `+$0.0057`

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
* Use a full-surface reprice / second-order check rather than relying on a linear Greek read, since the decomposition leaves a sizable unexplained remainder.
* No Layer B mechanism is available from the digest, so do not force an IV-crush, borrow, squeeze, or earnings-style catalyst story.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-09-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$125.5000` (-3560.3%)
* **Model ΔP**: `-$125.5000`
* **Primary drivers**: **Vega PnL** (52%) and **Delta PnL** (30%) and **Theta decay** (11%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by the volatility revaluation layer, with delta and theta also contributing and the residual remaining modest enough to fit Taylor truncation and path effects. However, observation reliability is off and the run explicitly suppresses a Vega narrative, so this should be treated as a model-based decomposition rather than a strong market-tape read. There are no relevant headlines or named microstructure mechanisms in the digest, and the American structure does not point to an early-exercise event. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is only medium because the observation is marked unreliable, the residual sits in a middle band, and the diagnostics suppress a stronger Vega story. The blotter still shows clean factor decomposition from the official engine, but there is no headline support to add a catalyst layer.

---

## 2. Observation Lock

* **As-of**: `2026-09-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 19.4%)
* **IV move**: -0.61 vol pts vs noise band ±0.89 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$125.5000`
* **Model ΔP (engine)**: `-$125.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$134.8113`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$9.3113` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (7.4%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$44.1009` | +35.1% | Stock moved from $336.59 to $334.98 (-1.6100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.9969` | -1.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$76.5420` | +61.0% | IV moved -2.67 vol pts (27.05% → 26.44%) |
| **Theta decay (Δt · Theta)** | `-$16.1654` | +12.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$9.3113` | -7.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$125.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$9.3113` (7.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0435`
* Combined: `+$0.0435` | Residual after: `-$1.2985`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1618`
* **spot**: `-$0.4126`
* **vol**: `-$0.6811`
* **rate**: `-$0.0015`
* Step sum: `-$1.2570` | Model ΔP: `-$1.2550` | Audit residual: `+$0.0020`

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
* Recheck the full-surface reprice and Greeks path if you need to separate volatility effect from spot and decay contributions; the residual is consistent with higher-order effects rather than a broken model.
* No catalyst overlay is supported by the digest, so do not force an IV-crush, borrow, or squeeze interpretation without new evidence.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.66 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-09-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$200.0000` (+1029.6%)
* **Model ΔP**: `+$200.0000`
* **Primary drivers**: **Delta PnL** (45%) and **Vega PnL** (45%) and **Theta decay** (7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained first by the put’s negative delta responding to the lower spot print, with gamma adding only a small convexity assist. Vega also contributed materially in the Taylor view, but the run is explicitly suppression-limited on Vega narrative and the observation lock means the headline tape does not supply a separate catalyst story. The remaining gap is small and consistent with higher-order truncation and quote noise rather than a new event. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The dominant driver is clear from the blotter, but observation reliability is false and the residual is not zero, so the attribution should stay coarse. There are no retrieved headlines to support a Layer B mechanism, and the data notes say not to invent one; the American-versus-European premium is present but the dividend does not cover remaining time value, so this is not an early-exercise case.

---

## 2. Observation Lock

* **As-of**: `2026-09-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 10.0%)
* **IV move**: -1.89 vol pts vs noise band ±3.65 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$200.0000`
* **Model ΔP (engine)**: `+$200.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$204.2605`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$4.2605` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$110.8159` | +55.4% | Stock moved from $336.59 to $334.98 (-1.6100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.7636` | +0.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$109.5238` | +54.8% | IV moved +3.61 vol pts (31.74% → 29.85%) |
| **Theta decay (Δt · Theta)** | `-$17.8428` | -8.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$4.2605` | -2.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$200.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$4.2605` (2.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0152`
* Combined: `-$0.0152` | Residual after: `+$2.0152`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$1.6100` vs next cash dividend `+$1.5000` (gap `-$0.1100`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$21.4250` vs `+$20.5517` (gap `+$0.8733`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.1255` — material
* **Dividend PV effect** (European, same divs − no divs): `+$0.7472`
* **Dividend coverage** (dividend / time value): `0.23` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$1.0952`
* **Residual (Taylor ε)**: `-$0.0426`
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
* Reconcile the move with the full revaluation view and keep the delta-led spot explanation front and center; the residual is small enough to read as truncation / mark noise.
* No catalyst overlay is supported by the digest, so do not force an IV-crush, borrow, squeeze, or conversion narrative from background tape.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.23 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-09-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$20.0000` (-468.4%)
* **Model ΔP**: `-$20.0000`
* **Primary drivers**: **Delta PnL** (49%) and **Theta decay** (26%) and **Vega PnL** (24%).
* **Verdict**: The move is dominated by the put's negative delta against a small downside spot move, with gamma and theta only partially offsetting that effect. The Taylor residual is small, so the modeled revaluation is internally consistent and does not need a separate news or microstructure explanation. With no relevant headlines retrieved, there is no Layer B catalyst to add beyond the spot-led repricing.
* **Confidence**: **Medium** — Confidence is medium because the blotter marks and observation are reliable and the residual is low, but the move is still a close blend of delta, theta, and a non-trivial vega contribution. There are no catalyst headlines to challenge or enrich the factor story, so the diagnosis rests on the engine attribution and the observed spot/vol move only.

---

## 2. Observation Lock

* **As-of**: `2026-09-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.9%)
* **IV move**: +0.12 vol pts vs noise band ±0.03 pts (exceeds noise band)
* **Prior observation**: `2026-09-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$20.0000`
* **Model ΔP (engine)**: `-$20.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$20.1588`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.1588` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$20.7509` | +103.8% | Stock moved from $765.61 to $764.20 (-1.4100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.4208` | +2.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$10.1866` | +50.9% | IV moved +0.15 vol pts (17.90% → 18.02%) |
| **Theta decay (Δt · Theta)** | `+$11.1996` | -56.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.1588` | -0.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$20.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.1588` (0.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0031`
* Combined: `+$0.0031` | Residual after: `+$0.1969`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* Recheck the full-surface revaluation and hedge alignment around the spot move; the Taylor break is small, so the factor story is stable.
* No catalyst layer to monitor from headlines here; focus on quote quality and the model-versus-mark reconciliation already shown in the blotter.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-09-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$46.5000` (-919.0%)
* **Model ΔP**: `-$46.5000`
* **Primary drivers**: **Delta PnL** (70%) and **Theta decay** (25%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is primarily explained by the position’s positive spot sensitivity as SPY slipped lower, with a smaller contribution from time decay. The higher-order terms are minor and the residual is low, so the revaluation is mostly a straightforward delta-led mark move rather than a convexity or volatility event. Early exercise is not a factor here because the American premium is negligible at the current marks. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is moderate because the attribution is internally consistent and the residual is small, but observation reliability is flagged as false and there were no headlines to validate any catalyst layer. Vega narration is suppressed by the code, and the data support a coarse spot-led diagnosis rather than a finer news-linked story.

---

## 2. Observation Lock

* **As-of**: `2026-09-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.5%)
* **IV move**: +0.01 vol pts vs noise band ±0.04 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$46.5000`
* **Model ΔP (engine)**: `-$46.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$46.9386`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.4386` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$34.4769` | +74.1% | Stock moved from $765.61 to $764.20 (-1.4100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.8732` | -1.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$1.0346` | +2.2% | IV moved -0.01 vol pts (13.61% → 13.62%) |
| **Theta decay (Δt · Theta)** | `-$12.3002` | +26.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.4386` | -0.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$46.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.4386` (0.9% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0002`
* Combined: `+$0.0002` | Residual after: `-$0.4652`

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
* Recheck the hedge against spot drift; the mark is behaving like a mostly directional option move with limited residual noise.
* No headline-backed catalyst layer is available, so do not force a volatility, borrow, or squeeze explanation from this run.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-09-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$7.0000` (+355.3%)
* **Model ΔP**: `+$7.0000`
* **Primary drivers**: **Delta PnL** (45%) and **Vega PnL** (38%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move was dominated by the modeled delta exposure as the stock drifted lower, which pulled the call’s revaluation against the position. Gamma and theta were smaller offsetting layers in the Taylor view, while the large residual means the close-to-close decomposition is only a rough guide here rather than a complete explanation. With observation quality flagged weak and no relevant headlines retrieved, there is no supported Layer B catalyst to add beyond the model-based revaluation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The code supplies a clear dominant Taylor driver, but attribution coverage is low, observation reliability is false, and the residual band is high. Vega is suppressed in the narrative by the diagnostic flags, and there are no retrieved headlines to support an auxiliary catalyst story.

---

## 2. Observation Lock

* **As-of**: `2026-09-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 14.7%)
* **IV move**: -2.20 vol pts vs noise band ±2.29 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$7.0000`
* **Model ΔP (engine)**: `+$7.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$7.1636`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$14.1636` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (202.3%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$53.4080` | -763.0% | Stock moved from $46.68 to $45.98 (-0.7000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$3.9963` | +57.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$44.0497` | +629.3% | IV moved +9.17 vol pts (27.59% → 25.39%) |
| **Theta decay (Δt · Theta)** | `-$1.8017` | -25.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$14.1636` | +202.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$7.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$14.1636` (202.3% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0607`
* Combined: `+$0.0607` | Residual after: `+$0.0093`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0180`
* **spot**: `-$0.4919`
* **vol**: `+$0.5801`
* **rate**: `-$0.0011`
* Step sum: `+$0.0692` | Model ΔP: `+$0.0700` | Audit residual: `+$0.0008`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$0.7000` vs next cash dividend `+$0.7080` (gap `+$0.0080`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$2.0400` vs `+$2.2064` (gap `-$0.1664`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0110` — material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1775`
* **Dividend coverage** (dividend / time value): `0.67` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.4405`
* **Residual (Taylor ε)**: `+$0.1416`
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

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Reconcile the move with a full-surface revaluation view rather than leaning on the truncated Taylor split alone, since the residual is large relative to the modeled change.
* Because no relevant catalyst headlines were retrieved, keep the desk explanation centered on the spot-driven revaluation and do not infer borrow, squeeze, or IV-crush mechanics.
* The dividend does not cover the remaining time value, so this is not an early-exercise case despite the American style setup.
* **Assignment watch**: ex-div `2026-10-09` — Dividend coverage 0.67 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-09-30` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$1.5000` (+5000.0%)
* **Model ΔP**: `+$1.5000`
* **Primary drivers**: **Vega PnL** (58%) and **Delta PnL** (26%) and **Theta decay** (5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by the change in implied volatility in the official Taylor view, with spot contributing a smaller positive lift and theta offsetting part of the move. Because the observation is flagged unreliable and Vega narration is suppressed, the safer read is that the model revaluation was driven by the vol repricing embedded in the surface rather than a clean tape-confirmed catalyst. The residual is consistent with higher-order effects and surface noise rather than a separate news event. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is only medium because the observation is flagged unreliable, the residual is not trivial, and the surface diagnostics show limitations in the American FD surface. There are no headlines or named catalysts to anchor a Layer B explanation, and the Vega narrative is explicitly suppressed, so the diagnosis should stay at a coarse model-repricing level.

---

## 2. Observation Lock

* **As-of**: `2026-09-30` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 111.1%)
* **IV move**: +8.59 vol pts vs noise band ±14.37 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-29`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$1.5000`
* **Model ΔP (engine)**: `+$1.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$1.3458`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.1542` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (10.3%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.4396` | +26.2% | Stock moved from $1.86 to $1.91 (+0.0500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0226` | +1.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.9729` | +58.0% | IV moved +7.00 vol pts (99.22% → 107.81%) |
| **Theta decay (Δt · Theta)** | `-$0.0893` | +5.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.1542` | +9.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$1.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.1542` (10.3% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0018`
* Combined: `+$0.0018` | Residual after: `+$0.0132`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0009`
* **spot**: `+$0.0045`
* **vol**: `+$0.0114`
* **rate**: `-$0.0000`
* Step sum: `+$0.0150` | Model ΔP: `+$0.0150` | Audit residual: `+$0.0000`

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
* Watch the full-surface reprice versus the prior-close Greek approximation, since the residual and surface limitations suggest second-order effects matter.
* No catalyst layer is available here; do not force an IV-crush, borrow, or squeeze narrative without supporting headlines.

---


## Skew proxy (Task C3.3, SPY risk reversal)

* skew_proxy(t) = +0.0440 | level_proxy(t) = 0.1582
* Δskew = +0.0011 | Δlevel = +0.0007
* Put 715 delta=-0.1531 | Call 795 delta=0.2292
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
