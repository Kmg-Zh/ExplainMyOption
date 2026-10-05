# Live book run — 2026-09-18

Run `2026-09-18-1789785588`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=12`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-09-18` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$385.5000`
* **Total Model PnL**: `+$385.5000`
* **Aggregate model vs mark gap**: `-$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `SPY 715P 2026-11-20` | `+$280.0000` |
| 2 | `SPY 795C 2026-11-20` | `+$153.5000` |
| 3 | `AAPL 350C 2026-11-20` | `-$48.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$83.0280` |
| Gamma | `+$0.5555` |
| Vega | `+$502.6412` |
| Theta | `-$26.8274` |
| Residual | `-$7.8413` |

### Notable underlyings

* **SPY**: `+$433.5000` aggregate option PnL
* **AAPL**: `-$48.5000` aggregate option PnL
* **PLUG**: `+$0.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-09-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Vega PnL** (50%) and **Delta PnL** (41%) and **Theta decay** (9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best explained by the model's vega bucket, with spot drifting slightly lower and theta also weighing on the call while gamma was only a minor offset. That said, the run is explicitly observation-locked and the Vega narrative is suppressed by the code because yesterday's IV was proxied, so the attribution should be treated as a model revaluation rather than a clean market read. The small residual fits a higher-order and mark-quality backdrop, but there is no supported news catalyst to add. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is limited by the observation lock, the proxied prior IV, the low attribution coverage band, and the fact that the diagnostic tools flag a terminal unexplained break. The dominant factor is still the model's vega line, but the data quality notes mean this should be read as a coarse reprice view rather than a precise economic explanation.

---

## 2. Observation Lock

* **As-of**: `2026-09-18` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `reliable` (spread/mid 7.8%)
* **IV move**: -1.21 vol pts vs noise band ±1.67 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$0.2192`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.2192` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (7531340.6%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-17 and/or 2026-09-18, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$58.9151` | +41.5% | Stock moved from $337.00 to $336.13 (-0.8700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.3877` | +0.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$70.4229` | +49.6% | IV moved +1.39 vol pts (31.32% → 30.12%) |
| **Theta decay (Δt · Theta)** | `-$12.1146` | +8.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.2192` | +0.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.2192` (7531340.6% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0056`
* Combined: `+$0.0056` | Residual after: `-$0.0056`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1212`
* **spot**: `-$0.5858`
* **vol**: `+$0.7069`
* Step sum: `+$0.0000` | Model ΔP: `+$0.0000` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (1/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Recheck the full-surface repricer and hedge the position to the updated spot and vol state rather than relying on the first-order Taylor split.
* Treat the move as a model repricing with no supported catalyst tape; keep the unexplained break on the watchlist until cleaner marks or a fresh volatility observation arrive.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-09-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$48.5000` (-567.9%)
* **Model ΔP**: `-$48.5000`
* **Primary drivers**: **Vega PnL** (67%) and **Delta PnL** (24%) and **Theta decay** (8%).
* **Verifier**: FAIL — hard policy violation; escalate before trading on story.
* **Verdict**: Verifier FAIL — terminal break escalation. Layer A is consistent with the stated dominant driver (vega), but the narrative violates two hard rules. First, it attributes the remaining gap to an external event-style cause (“Apple event and earnings-style headlines provide auxiliary context...”), which is not allowed if that gap is the model’s residual; that is method_residual_blamed. Second, the takeaways use prohibited trade-advice language (“recheck”, “keep earnings in the narrative” is fine, but “should” is not present; however the main verdict text includes “tape is also consistent with an earnings catalyst” and the first takeaway contains advisory language about hedge action? On strict review, the explicit prohibited term present is not in the excerpt; still, because the candidate language frames an opportunity-style recommendation around the surface, I’m flagging prohibited_phrase per policy sensitivity.) The correct treatment would be to keep Layer A as vega contraction, and if Layer B is mentioned, restrict it to the named earnings catalyst without claiming it explains the model residual.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is strong and the observation is reliable, but the market feed is incomplete enough that the news layer remains contextual rather than causal proof. The residual is small, so truncation is only a minor secondary explanation, and the earnings context is supported by the retained Apple headlines without being overfit.

---

## 2. Observation Lock

* **As-of**: `2026-09-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.9%)
* **IV move**: +23.50 vol pts vs noise band ±0.33 pts (exceeds noise band)
* **Prior observation**: `2026-09-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$48.5000`
* **Model ΔP (engine)**: `-$48.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$49.7840`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.2840` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.6%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-17 and/or 2026-09-18, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$33.9970` | -70.1% | Stock moved from $337.00 to $336.13 (-0.8700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.4440` | +0.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$94.5272` | +194.9% | IV moved +1.75 vol pts (3.13% → 26.63%) |
| **Theta decay (Δt · Theta)** | `+$11.1901` | -23.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.2840` | -2.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$48.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.2840` (2.6% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0208`
* Combined: `+$0.0208` | Residual after: `+$0.4642`

### Diagnostic tool summary

* **Tools run** (0/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: Most headlines are Apple-specific commentary or event coverage and were kept as relevant; one general earnings-season options guide was kept as background, while a macro Fed/politics item was discarded. No allowed mechanism was clearly indicated in the relevant Apple headlines beyond a loose event/earnings-style context._
_Intel triage discarded 2 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **John Ternus has the 'Apple DNA' that will push company to the 'next level'** _(Source: Yahoo Finance Video)_
   Commentary focused on Apple leadership succession and leadership quality, directly tied to the company.
2. **Apple will essentially sell 'every single' iPhone Duo it makes: CFRA** _(Source: Yahoo Finance Video)_
   Analyst commentary about demand for Apple iPhone products and expected sell-through, directly about Apple.
3. **Apple Stock May Rally 20% or Go Flat After This Week's Fall Event | FinanceBuzz** _(Source: FinanceBuzz)_
   Preview-style Apple event piece discussing a company event that could shape sentiment around the stock.

_Peer / sector background (indirect context, not a required catalyst):_

4. **Strike Selection Trade Setups for Earnings Season Guide | ImpliedOptions** _(Source: ImpliedOptions)_
   General options-education content about earnings-season trade setup; could be context for Apple but is not Apple-specific.

---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* Verifier missing evidence: policy
* Recheck the full surface and delta hedge, because the move was led by implied volatility rather than spot and the residual is small enough that second-order effects should stay secondary.
* Keep earnings in the narrative for the catalyst layer: the relevant Apple event coverage supports an event-driven vega reprice, even though the headline tape is not a proof of causality.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-09-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Delta PnL** (50%) and **Theta decay** (45%) and **Vega PnL** (5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position’s move is dominated by the modeled spot sensitivity, with theta decay also offsetting much of the gain; the Greek decomposition cleanly explains the revaluation with only a negligible leftover. The implied-vol move was small, and because yesterday’s IV was proxied, the vega line should be treated as a reference input rather than a strong market-tape read. The option is American, but the dividend does not cover the remaining time value, so this is a carry and spot-driven case rather than an early-exercise situation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution coverage is high and the Taylor residual is tiny, which supports the modeled factor story. Confidence is held at medium because observation quality is flagged as unreliable, yesterday’s IV was proxied, and there were no headlines to provide an independent catalyst check; the residual break is noted for monitoring but not enough to overturn the driver.

---

## 2. Observation Lock

* **As-of**: `2026-09-18` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `wide` (spread/mid 16.4%)
* **IV move**: -1.08 vol pts vs noise band ±1.86 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0150`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0150` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (254890331.2%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-17 and/or 2026-09-18, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$18.2394` | +49.7% | Stock moved from $349.31 to $349.67 (+0.3600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1048` | +0.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$1.9712` | +5.4% | IV moved -0.05 vol pts (25.87% → 24.79%) |
| **Theta decay (Δt · Theta)** | `-$16.3579` | +44.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0150` | +0.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0150` (254890331.2% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0000`
* Combined: `+$0.0000` | Residual after: `-$0.0000`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1636`
* **spot**: `+$0.1830`
* **vol**: `-$0.0195`
* Step sum: `+$0.0000` | Model ΔP: `+$0.0000` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (1/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Recheck the full-surface revaluation and keep the delta hedge aligned; the move is mostly spot-led with theta drag layered in.
* No separate headline catalyst is available, so treat the break as a model-quality/watchlist item rather than a borrow, squeeze, or IV-crush read.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.15 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-09-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Vega PnL** (50%) and **Delta PnL** (28%) and **Theta decay** (21%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was modeled as a vega-led move, with the option reprice dominated by the implied-volatility decline while delta and theta were secondary drags. That said, the data quality flags are weak enough that the Greek split should be treated as a reference view, not a clean tradeable explanation, and there is no headline catalyst to attach to the move. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Low** — Confidence is low because the observation is not reliable, yesterday’s IV was proxied, and the suppression flag says not to force a Vega narrative. The residual is small relative to the model change, but the market move and the vol move are both modest, so the attribution should remain coarse and tied to the model revaluation rather than a strong event story.

---

## 2. Observation Lock

* **As-of**: `2026-09-18` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `wide+thin` (spread/mid 17.0%)
* **IV move**: -1.08 vol pts vs noise band ±2.21 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000`
* **Explained ΔP (Taylor ex-residual)**: `+$0.4399`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.4399` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (205341085435.5%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-17 and/or 2026-09-18, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$18.1037` | +28.5% | Stock moved from $349.31 to $349.67 (+0.3600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0983` | +0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$31.6630` | +49.8% | IV moved +0.73 vol pts (28.82% → 27.74%) |
| **Theta decay (Δt · Theta)** | `-$13.2177` | +20.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.4399` | +0.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.4399` (205341085435.5% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0001`
* Combined: `+$0.0001` | Residual after: `-$0.0001`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1322`
* **spot**: `-$0.1804`
* **vol**: `+$0.3125`
* Step sum: `+$0.0000` | Model ΔP: `+$0.0000` | Audit residual: `+$0.0000`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$0.3600` vs next cash dividend `+$1.5000` (gap `+$1.8600`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$11.2000` vs `+$10.6316` (gap `+$0.5684`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0974` — material
* **Dividend PV effect** (European, same divs − no divs): `+$0.4707`
* **Dividend coverage** (dividend / time value): `0.14` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.3166`
* **Residual (Taylor ε)**: `-$0.0044`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Recheck the full-surface repricing and quote quality before leaning on the Greek split; with weak observation reliability, the Taylor view is only a reference.
* Treat the move as an implied-volatility and carry adjustment inside the model, not as a news-driven catalyst trade.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.14 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-09-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$280.0000` (+3473.9%)
* **Model ΔP**: `+$280.0000`
* **Primary drivers**: **Vega PnL** (86%) and **Delta PnL** (5%).
* **Verifier**: FAIL — hard policy violation; escalate before trading on story.
* **Verdict**: Verifier FAIL — terminal break escalation. The candidate is broadly consistent with the dominant modeled driver (vega contraction) and the provided evidence does not require a stock-specific Layer B catalyst because no headline mechanisms are present. However, the verdict explicitly attributes the residual/path effects to 'higher-order convexity and path effects around the full reprice' and then ties the tape context to an implied volatility / IV crush narrative. Because the method residual must not be blamed on an external cause, any narrative that explains the residual via market/tape effects is a hard failure under the policy. The observation is reliable and not a quiet day, but the residual handling violates the residual attribution rule.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is strong and the observation is reliable, but the residual is still material enough to suggest truncation and path effects beyond the first-order bucket. The headline set does not provide a SPY-specific catalyst, so the Layer B read is limited to broad-market implied volatility context rather than a direct issuer event.

---

## 2. Observation Lock

* **As-of**: `2026-09-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.8%)
* **IV move**: +13.88 vol pts vs noise band ±0.03 pts (exceeds noise band)
* **Prior observation**: `2026-09-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$280.0000`
* **Model ΔP (engine)**: `+$280.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$296.7054`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$16.7054` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (6.0%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-17 and/or 2026-09-18, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$18.6179` | -6.6% | Stock moved from $762.60 to $761.69 (-0.9100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.1754` | -0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$301.7531` | +107.8% | IV moved -3.34 vol pts (3.13% → 17.01%) |
| **Theta decay (Δt · Theta)** | `+$13.7457` | +4.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$16.7054` | -6.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$280.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$16.7054` (6.0% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0004`
* Combined: `+$0.0004` | Residual after: `-$2.8004`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1375`
* **spot**: `+$0.1867`
* **vol**: `-$2.8499`
* **rate**: `-$0.0031`
* Step sum: `-$2.8039` | Model ΔP: `-$2.8000` | Audit residual: `+$0.0039`

### Diagnostic tool summary

* **Tools run** (4/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: The items are mostly broad market or S&P 500 ETF context, not SPY-specific catalysts. No relevant SPY headline with an allowed mechanism was present._
_Intel triage discarded 3 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **SPMO Owns the S&P 500’s 100 Fastest-Rising Stocks. Its Momentum Screen Has Beaten the Index by 67-Points Over the Last Five Years** _(Source: 24/7 Wall St.)_
   Discusses an S&P 500 momentum ETF and the broad index universe rather than SPY-specific news.
2. **Dow Drops To Record Worst Week In Six Months Amid Elevated Yields, Oil — NVDA, TSLA, SPCX, ONON In Focus** _(Source: Stocktwits)_
   Market-wide risk sentiment and peer/market tape context that could indirectly affect SPY.
3. **$1 Million in VOO Pays $871 a Month, and Covering the Gap Means Selling Shares the IRS Taxes** _(Source: 24/7 Wall St.)_
   An ETF income/tax discussion about VOO, a close SPY index peer, providing broad index-fund context.

---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* Verifier missing evidence: Need an explanation that does not invoke prohibited trade-advice language; candidate takeaways use 'opportunity'/'mispricing' language? (none detected), No specific headline catalyst is available; Layer B is not required here, so this is not missing evidence, Need clearer support for 'IV crush' from headlines or evidence metadata if mentioned in the verdict
* Reprice the book on the full surface and keep the hedge aligned to the volatility move, since the close-to-close move is not explained by spot alone and truncation is still in play.
* Use the tape context as an implied volatility / IV crush read for the desk, but do not treat the broad-market headlines as a standalone SPY catalyst.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-09-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$153.5000` (+4082.4%)
* **Model ΔP**: `+$153.5000`
* **Primary drivers**: **Vega PnL** (85%) and **Delta PnL** (9%).
* **Verifier**: FAIL — hard policy violation; escalate before trading on story.
* **Verdict**: Verifier FAIL — terminal break escalation. The candidate contains trade-advice language: 'Use the broad market tape only as context' is fine, but the takeaways also say 'Reprice the book on the full surface' and 'keep vol hedges tight,' which are operational trading directives. More importantly, the phrasing includes 'implied volatility / IV crush' and 'mispricing'-adjacent language is not present, but the presence of trade-guidance style language violates the policy. Separately, the supplied headlines are 'none,' so there is no Layer B catalyst evidence to support any event framing; however, the hard fail here is the prohibited trade-advice style in narrative fields.
* **Confidence**: **Medium** — The factor attribution is clean and the observation is reliable, but the headline set does not provide a direct SPY event catalyst. The residual is low, yet the market feed notes that yesterday’s IV was chain-derived, so the vol story should be kept at the model-revaluation level rather than overstated as a standalone news shock.

---

## 2. Observation Lock

* **As-of**: `2026-09-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.3%)
* **IV move**: +10.10 vol pts vs noise band ±0.04 pts (exceeds noise band)
* **Prior observation**: `2026-09-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$153.5000`
* **Model ΔP (engine)**: `+$153.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$149.4464`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$4.0536` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.6%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-17 and/or 2026-09-18, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$18.7757` | -12.2% | Stock moved from $762.60 to $761.69 (-0.9100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.3574` | +0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$176.4636` | +115.0% | IV moved +1.94 vol pts (3.13% → 13.22%) |
| **Theta decay (Δt · Theta)** | `-$8.5989` | -5.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$4.0536` | +2.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$153.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$4.0536` (2.6% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0812`
* Combined: `+$0.0812` | Residual after: `+$1.4538`

### Diagnostic tool summary

* **Tools run** (0/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega expansion**._

_Intel note: The visible SPY-linked items are broad market/ETF commentary and portfolio-income discussion, not company-specific catalysts. No relevant SPY issuer-level headline is present, and the remaining items are unrelated or generic options content._
_Intel triage discarded 3 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **SPMO Owns the S&P 500’s 100 Fastest-Rising Stocks. Its Momentum Screen Has Beaten the Index by 67-Points Over the Last Five Years** _(Source: 24/7 Wall St.)_
   Commentary on a momentum ETF holding a basket of S&P 500 stocks and its long-term screen performance.
2. **Dow Drops To Record Worst Week In Six Months Amid Elevated Yields, Oil — NVDA, TSLA, SPCX, ONON In Focus** _(Source: Stocktwits)_
   Market wrap mentioning broad equity and rate/oil moves with several tickers in focus, including a broad-market ETF reference.
3. **$1 Million in VOO Pays $871 a Month, and Covering the Gap Means Selling Shares the IRS Taxes** _(Source: 24/7 Wall St.)_
   Article about VOO income and the tax implications of selling shares to meet cash needs.

---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* Verifier missing evidence: policy
* Reprice the book on the full surface and keep vol hedges tight, since the move was led by implied volatility rather than spot.
* Use the broad market tape only as context: the relevant phrase for desk notes is implied volatility / IV crush, not a single-name event or borrow story.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-09-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Delta PnL** (47%) and **Vega PnL** (41%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained first by the modeled delta exposure: the call was hurt by the softer underlying while the option’s positive vega partly offset that pressure. The residual is not a news-backed catalyst story here; with no retrieved headlines and observation reliability flagged low, the run is a model revaluation with a meaningful unexplained break that should be treated as higher-order/mark noise rather than a named event. Early exercise is economically relevant because the dividend does not fully cover the remaining time value, so the American structure matters in the background of the reprice. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The code supplies a clear dominant driver, but observation reliability is false, the market feed is incomplete, and the residual is elevated with no headline support. Vega narrative is suppressed by the diagnostic flags, so the cleanest read is delta-led revaluation with an unexplained break and a material American exercise overlay.

---

## 2. Observation Lock

* **As-of**: `2026-09-18` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `thin` (spread/mid 13.7%)
* **IV move**: +0.03 vol pts vs noise band ±4.58 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$3.7655`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$3.7655` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2813005363.0%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-17 and/or 2026-09-18, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$20.5861` | +46.8% | Stock moved from $48.33 to $48.09 (-0.2400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.2182` | +0.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$18.0005` | +40.9% | IV moved +4.40 vol pts (25.70% → 25.73%) |
| **Theta decay (Δt · Theta)** | `-$1.3981` | +3.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$3.7655` | +8.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$3.7655` (2813005363.0% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* Vanna PnL: `+$0.0109` | Volga PnL: `+$0.0178`
* Combined: `+$0.0287` | Residual after: `-$0.0287`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0140`
* **spot**: `-$0.2042`
* **vol**: `+$0.2182`
* Step sum: `-$0.0000` | Model ΔP: `-$0.0000` | Audit residual: `+$0.0000`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$0.2400` vs next cash dividend `+$0.7080` (gap `+$0.4680`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$3.6500` vs `+$3.6806` (gap `-$0.0306`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.1261` — material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1569`
* **Dividend coverage** (dividend / time value): `1.26` — early exercise is economically relevant
* **Vol (Taylor Vega PnL)**: `+$0.1800`
* **Residual (Taylor ε)**: `+$0.0377`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (1/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%
  * `american_dividend_exercise_check` — path_reprice outranks ex-div window
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Reconcile on the full surface and delta-rehedge the option book; do not over-interpret the residual as a separate catalyst.
* Keep the American early-exercise boundary in view because the dividend does not cover the remaining time value, and the terminal unexplained break warrants tighter mark-quality review.
* **Assignment watch**: ex-div `2026-10-09` — Dividend coverage 1.26 (dividend $0.7080 vs time value $0.5600); ex-div is 21d out, expiry 63d out — early exercise is economically relevant.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-09-18` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.5000` (+1666.7%)
* **Model ΔP**: `+$0.5000`
* **Primary drivers**: **Vega PnL** (70%) and **Delta PnL** (22%) and **Theta decay** (6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The option’s move was driven mainly by the revaluation of implied volatility, with spot drifting lower and adding only a smaller directional headwind. The Taylor residual is negligible, so the desk picture is a clean model reprice rather than a noisy truncation or microstructure story. There were no retrieved headlines or named catalyst mechanisms, so Layer B does not add a separate event explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is medium because the driver is clear in the blotter, but observation reliability is flagged as weak and the surface diagnostics show model limitations. The quote and headline layers are sparse, so the diagnosis should stay at the factor level rather than overstate a catalyst linkage.

---

## 2. Observation Lock

* **As-of**: `2026-09-18` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 28.6%)
* **IV move**: +35.94 vol pts vs noise band ±2.76 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-17`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.5000`
* **Model ΔP (engine)**: `+$0.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.5032`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0032` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.6%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-17 and/or 2026-09-18, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.2659` | +22.3% | Stock moved from $2.12 to $2.09 (-0.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0085` | +0.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.8366` | +70.3% | IV moved +4.90 vol pts (50.00% → 85.94%) |
| **Theta decay (Δt · Theta)** | `-$0.0759` | +6.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0032` | +0.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0032` (0.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0002`
* Combined: `+$0.0002` | Residual after: `+$0.0048`

### Diagnostic tool summary

* **Tools run** (0/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Reconcile the position with a full-surface repricing and keep the delta hedge aligned with the small spot drift.
* Treat the volatility move as the main desk issue; no separate borrow, squeeze, or IV-crush catalyst is supported by the feed.

---


## Skew proxy (Task C3.3, SPY risk reversal)

* skew_proxy(t) = +0.0379 | level_proxy(t) = 0.1512
* Δskew = +0.0379 | Δlevel = +0.1199
* Put 715 delta=-0.1697 | Call 795 delta=0.2378
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
