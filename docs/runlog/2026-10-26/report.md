# Live book run — 2026-10-26

Run `2026-10-26-1793063708`. 6/8 legs completed, 2 failed. `legs_narrated=6` `legs_silent=0` `llm_calls=11`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-26` | **Positions**: 6 | **Tickers**: AAPL, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$103.0000`
* **Total Model PnL**: `+$153.4838`
* **Aggregate model vs mark gap**: `+$256.4838`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 350C 2026-11-20` | `+$210.0000` |
| 2 | `SPY 715P 2026-11-20` | `+$97.0000` |
| 3 | `AAPL 325C 2026-11-20` | `-$93.5162` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$144.8307` |
| Gamma | `+$4.8914` |
| Vega | `+$296.6727` |
| Theta | `+$18.2842` |
| Residual | `-$21.5339` |

### Notable underlyings

* **SPY**: `+$121.0000` aggregate option PnL
* **AAPL**: `+$116.4838` aggregate option PnL
* **VZ**: `-$81.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-26` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$350.0000` (-331.2%)
* **Model ΔP**: `-$93.5162`
* **Primary drivers**: **Theta decay** (56%) and **Delta PnL** (36%) and **Vega PnL** (7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best explained by time decay in the option’s model revaluation, with the spot drift and modest volatility uptick playing secondary roles. The remaining gap is small and consistent with higher-order truncation and the path reprice audit, while the American exercise overlay is not material enough to change the story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The blotter provides a clear dominant Taylor driver and high attribution coverage, but observation quality is flagged as unreliable and the run notes a terminal unexplained break. That keeps the diagnosis at medium confidence even though the residual is small and no relevant headlines were retrieved.

---

## 2. Observation Lock

* **As-of**: `2026-10-26` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.4%)
* **IV move**: +0.25 vol pts vs noise band ±2.39 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$350.0000`
* **Model ΔP (engine)**: `-$93.5162`
* **Model vs Mark gap**: `+$256.4838` (-274.3% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$91.9753`

* **Method residual (ε_method)**: `-$1.5409` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$256.4838` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$38.4888` | +41.2% | Stock moved from $348.22 to $347.73 (-0.4900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1049` | -0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$7.0411` | -7.5% | IV moved +0.25 vol pts (34.65% → 34.90%) |
| **Theta decay (Δt · Theta)** | `-$60.6325` | +64.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.5409` | +1.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$93.5162** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.5409` (1.6% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0009`
* Combined: `+$0.0009` | Residual after: `-$0.9360`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.6117`
* **spot**: `-$0.3890`
* **vol**: `+$0.0654`
* **rate**: `-$0.0012`
* Step sum: `-$0.9365` | Model ΔP: `-$0.9352` | Audit residual: `+$0.0013`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$0.4900` vs next cash dividend `+$0.2700` (gap `-$0.2200`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$27.2968` vs `+$27.4468` (gap `-$0.1500`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1509`
* **Dividend coverage** (dividend / time value): `0.06` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.0704`
* **Residual (Taylor ε)**: `-$0.0154`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%
  * `american_dividend_exercise_check` — path_reprice outranks ex-div window
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Watch whether higher-order revaluation effects or quote noise are distorting the modeled attribution around the small residual.
* Keep an eye on the ex-div window and confirm the early-exercise premium stays immaterial as the contract approaches expiry.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.06 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-26` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$210.0000` (+>1000%)
* **Model ΔP**: `+$210.0000`
* **Primary drivers**: **Vega PnL** (59%) and **Theta decay** (27%) and **Delta PnL** (11%).
* **Verdict**: The move is dominated by the model’s volatility revaluation, with theta carry also helping and spot contributing only a minor offset. The only relevant headline is Apple’s upcoming earnings context, so the tape reads as earnings-linked repricing rather than a pure spot-led move; the small residual is consistent with higher-order effects around a short-dated options surface. Namechecked catalyst mechanisms here are earnings and implied volatility.
* **Confidence**: **Medium** — The attribution is supported by the dominant modeled driver, the vol move band, and reliable observations, but the headline set is sparse and the residual is not zero. Because the note is tied to earnings context and the model uses a flat-vol FDM rather than a full event surface, some of the move may reflect earnings-related repricing that is only partially captured by the Taylor view.

---

## 2. Observation Lock

* **As-of**: `2026-10-26` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.6%)
* **IV move**: +0.48 vol pts vs noise band ±0.28 pts (exceeds noise band)
* **Prior observation**: `2026-10-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$210.0000`
* **Model ΔP (engine)**: `+$210.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$216.6757`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$6.6757` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$24.4723` | +11.7% | Stock moved from $348.22 to $347.73 (-0.4900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.1880` | -0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$131.9763` | +62.8% | IV moved -3.43 vol pts (28.41% → 28.89%) |
| **Theta decay (Δt · Theta)** | `+$60.4151` | +28.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$6.6757` | -3.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$210.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$6.6757` (3.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0003`
* Combined: `+$0.0003` | Residual after: `-$2.1003`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega revaluation**._

_Intel note: The only headline is directly about Apple and its upcoming earnings report, so it is relevant. No other issuer, peer, or unrelated items are present._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Apple Earnings Options: A Beginner's Guide to the Nov 2 Report Guide - MenthorQ** _(Source: MenthorQ)_
   A guide focused on Apple’s upcoming Nov. 2 earnings report and how options traders may frame it.

---

## 7. Risk Watchlist

* Watch whether higher-order Taylor effects remain visible as expiry approaches, since short-dated surfaces can make the reference decomposition less stable.
* Keep the earnings and implied volatility context in view, because that is the named catalyst mechanism most consistent with the headline tape.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-26` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$97.0000` (+>1000%)
* **Model ΔP**: `+$97.0000`
* **Primary drivers**: **Vega PnL** (48%) and **Theta decay** (24%) and **Delta PnL** (24%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter’s dominant modeled driver is Vega, with the full revaluation also helped by Theta and partly offset by Delta and Gamma. The headline layer is consistent with an implied-volatility move and an IV crush theme in the broader options tape, which fits the fact that the residual is small and the session is not purely diffusion-driven. Caveats: Layer B omitted mechanisms present in headlines; residual truncation does not replace those catalysts. Gaps: Headline catalyst not used in narrative: earnings
* **Confidence**: **Medium** — Confidence is medium because the attribution is internally coherent and observation quality is reliable, but the news set does not contain a SPY-specific catalyst. The residual is modest, and the market move is small enough that second-order effects and surface effects can still matter.

---

## 2. Observation Lock

* **As-of**: `2026-10-26` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.8%)
* **IV move**: +0.51 vol pts vs noise band ±0.03 pts (exceeds noise band)
* **Prior observation**: `2026-10-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$97.0000`
* **Model ΔP (engine)**: `+$97.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$101.3206`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$4.3206` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.5%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$53.4646` | -55.1% | Stock moved from $763.96 to $759.97 (-3.9901) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$3.5500` | -3.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$104.6571` | +107.9% | IV moved -2.29 vol pts (21.31% → 21.83%) |
| **Theta decay (Δt · Theta)** | `+$53.6782` | +55.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$4.3206` | -4.5% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$97.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$4.3206` (4.5% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0222`
* Combined: `-$0.0222` | Residual after: `-$0.9478`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega**._

_Intel note: No SPY-specific issuer or structure headline is present. The remaining items are earnings/options context for other names and broad market noise, so they are kept only as background or discarded._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **NFLX Earnings: Implied Moves and IV Crush Netflix | Market Chameleon** _(Source: marketchameleon.com)_
   Netflix earnings and implied-move/IV-crush content; useful only as market-wide options context, not SPY-specific.

_Peer / sector background (indirect context, not a required catalyst):_

2. **MU Stock Before Earnings: Why Calls Lose on a ±7.4% Move** _(Source: earnings-watcher.com)_
   Micron earnings-related options commentary; relevant as broader sector/options context but not tied to SPY directly.

---

## 7. Risk Watchlist

* **Verifier reflect**: Layer B omitted mechanisms present in headlines; residual truncation does not replace those catalysts. Gaps: Headline catalyst not used in narrative: earnings
* Check whether the Taylor split is being nudged by higher-order truncation or a broader full-surface reprice rather than treating the residual as a separate event.
* Watch for continued implied volatility compression and any broader IV crush behavior in the options complex, since that mechanism is part of the tape context.

---

### Position 4 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-26` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$24.0000` (+>1000%)
* **Model ΔP**: `+$24.0000`
* **Primary drivers**: **Vega PnL** (53%) and **Delta PnL** (24%) and **Theta decay** (14%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The dominant modeled driver is a vega-led revaluation: the option’s price rose as implied volatility lifted, while the spot move and theta drag partly offset that gain. The remaining gap is consistent with Taylor truncation and higher-order convexity on a large residual day. Layer B is cautious but present: the relevant headline context supports an implied volatility / IV crush framing as the mechanism behind the unmodeled repricing, even though the tape is not SPY-specific. Caveats: Layer B omitted mechanisms present in headlines; residual truncation does not replace those catalysts. Gaps: Headline catalyst not used in narrative: earnings
* **Confidence**: **Medium** — Confidence is medium because the attribution is clear on the blotter, but the residual is sizable and the headline set is only indirect background rather than a direct SPY catalyst. The feed is reliable enough to use the modeled factor story, yet the unmodeled gap means the narrative should stay cautious about exact causal structure.

---

## 2. Observation Lock

* **As-of**: `2026-10-26` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.8%)
* **IV move**: -0.27 vol pts vs noise band ±0.04 pts (exceeds noise band)
* **Prior observation**: `2026-10-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$24.0000`
* **Model ΔP (engine)**: `+$24.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$37.7019`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$13.7019` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (57.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$48.7272` | -203.0% | Stock moved from $763.96 to $759.97 (-3.9901) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$6.6386` | +27.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$108.2253` | +450.9% | IV moved +2.53 vol pts (13.12% → 12.85%) |
| **Theta decay (Δt · Theta)** | `-$28.4347` | -118.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$13.7019` | -57.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$24.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$13.7019` (57.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0502`
* Combined: `-$0.0502` | Residual after: `+$0.2902`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2804`
* **spot**: `-$0.3677`
* **vol**: `+$0.8880`
* **rate**: `-$0.0004`
* Step sum: `+$0.2395` | Model ΔP: `+$0.2400` | Audit residual: `+$0.0005`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega revaluation**._

_Intel note: The feed contains no SPY-specific company or structure headline. Two items are kept as background peer/market volatility references, while one generic navigation item is discarded._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **NFLX Earnings: Implied Moves and IV Crush Netflix | Market Chameleon** _(Source: marketchameleon.com)_
   Netflix earnings is a peer-level event and volatility reference, relevant only as broader market background rather than a SPY-specific catalyst.

_Peer / sector background (indirect context, not a required catalyst):_

2. **MU Stock Before Earnings: Why Calls Lose on a ±7.4% Move** _(Source: earnings-watcher.com)_
   Micron before earnings is a peer event that may inform broader semiconductor/market sentiment, but it is not a SPY-specific headline.

---

## 7. Risk Watchlist

* **Verifier reflect**: Layer B omitted mechanisms present in headlines; residual truncation does not replace those catalysts. Gaps: Headline catalyst not used in narrative: earnings
* Higher-order convexity and Taylor truncation can still distort the one-day Greek split when the residual stays large.
* Watch for implied volatility / IV crush context in related tape and headlines, since that mechanism is explicitly tagged in the digest.

---

### Position 5 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-26` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$81.0000` (->1000%)
* **Model ΔP**: `-$81.0000`
* **Primary drivers**: **Vega PnL** (56%) and **Delta PnL** (31%) and **Theta decay** (7%).
* **Verdict**: The modeled move was driven primarily by implied volatility falling, with spot weakness and time decay adding smaller negative pressure and a modest second-order offset. The headline backdrop is consistent with a Verizon-specific telecom competition story involving SpaceX, but the option repricing itself is best read through the large volatility move rather than the stock drift alone.
* **Confidence**: **Medium** — The attribution is well covered by the engine and the vol move is the dominant model input, but the residual is not zero and the surface diagnostics show some calibration limitations. Headlines provide a plausible Verizon-specific context, yet they do not prove causality for the revaluation, so the story should stay at the modeled vol-driven level.

---

## 2. Observation Lock

* **As-of**: `2026-10-26` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 14.4%)
* **IV move**: -3.66 vol pts vs noise band ±0.77 pts (exceeds noise band)
* **Prior observation**: `2026-10-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$81.0000`
* **Model ΔP (engine)**: `-$81.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$84.7635`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$3.7635` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$28.6223` | +35.3% | Stock moved from $45.20 to $44.66 (-0.5400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.8859` | -2.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$51.8144` | +64.0% | IV moved -10.46 vol pts (30.76% → 27.10%) |
| **Theta decay (Δt · Theta)** | `-$6.2128` | +7.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$3.7635` | -4.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$81.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$3.7635` (4.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0037`
* Combined: `-$0.0037` | Residual after: `-$0.8063`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: One headline is directly about Verizon and a related telecom competitive-structure story involving SpaceX. The remaining items are either another source on the same broader telecom theme or unrelated Netflix coverage, so they are not treated as direct Verizon news._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **SpaceX Cell Site Report Hits Verizon, AT&T, Lifts These Tower Plays - Investor's Business Daily**
2. **'It's not something that gets done overnight': SpaceX's telecom ambitions will be hard-won, CEOs and analysts say - Yahoo Finance**
3. **Traders are betting Netflix's stock drama may be coming to an end - CNBC**

---

## 7. Risk Watchlist

* Watch whether the modeled move remains stable under a fuller surface reprice, since truncation and surface fit can still distort the attribution.
* Monitor the Verizon/SpaceX telecom competition tape for whether implied volatility stays under pressure or re-expands; that is the relevant Layer B check.
* No material early-exercise premium is indicated here, so American exercise is not a separate explanatory factor.

---

### Position 6 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-26` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$3.0000` (->1000%)
* **Model ΔP**: `-$3.0000`
* **Primary drivers**: **Vega PnL** (70%) and **Theta decay** (11%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is dominated by a sharp revaluation from the implied-volatility reset while the spot price was unchanged, so the modeled loss is primarily a volatility story rather than a directionals story. The remaining gap is consistent with higher-order effects and Taylor truncation, which is plausible given the extreme vol move and the small residual share, but there is no headline catalyst to anchor a separate news explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is limited because observation is not reliable, there are no retrieved headlines, and the residual band is high. The market feed does show a clean vol reset with spot flat, but the surface diagnostics also flag limitations in the American surface and the decomposition leaves a meaningful method gap.

---

## 2. Observation Lock

* **As-of**: `2026-10-26` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 66.7%)
* **IV move**: -29.69 vol pts vs noise band ±8.52 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-23`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$3.0000`
* **Model ΔP (engine)**: `-$3.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$3.9418`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.9418` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (31.4%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.0000` | +0.0% | Stock moved from $1.38 to $1.38 (+0.0000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0000` | +0.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$3.4128` | +69.9% | IV moved -30.99 vol pts (179.69% → 150.00%) |
| **Theta decay (Δt · Theta)** | `-$0.5290` | +10.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.9418` | +19.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$3.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.9418` (31.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0063`
* Combined: `+$0.0063` | Residual after: `-$0.0363`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0052`
* **spot**: `+$0.0000`
* **vol**: `-$0.0248`
* **rate**: `-$0.0000`
* Step sum: `-$0.0300` | Model ΔP: `-$0.0300` | Audit residual: `+$0.0000`

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
* Watch whether the full-surface reprice or higher-order convexity continues to dominate the modeled attribution rather than the first-order Greek split.
* Verify whether the implied-vol reset persists in subsequent marks, since there is no headline-supported catalyst to attach to the move.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0897 | level_proxy(t) = 0.1734
* Δskew = +0.0078 | Δlevel = +0.0012
* Put 715 delta=-0.1168 | Call 795 delta=0.1240
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **jpm_straddle_call** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-10-30, 2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
- **jpm_straddle_put** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-10-30, 2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
