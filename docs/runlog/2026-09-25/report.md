# Live book run — 2026-09-25

Run `2026-09-25-1790385305`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=12`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-09-25` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$144.0000`
* **Total Model PnL**: `+$144.0000`
* **Aggregate model vs mark gap**: `+$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `JPM 350P 2026-10-23` | `-$327.5000` |
| 2 | `AAPL 325C 2026-11-20` | `+$300.0000` |
| 3 | `AAPL 350C 2026-11-20` | `-$152.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$49.8621` |
| Gamma | `+$3.8110` |
| Vega | `+$192.5948` |
| Theta | `-$34.1791` |
| Residual | `+$31.6354` |

### Notable underlyings

* **SPY**: `+$195.0000` aggregate option PnL
* **JPM**: `-$177.5000` aggregate option PnL
* **AAPL**: `+$147.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-09-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$300.0000` (+1413.4%)
* **Model ΔP**: `+$300.0000`
* **Primary drivers**: **Vega PnL** (80%) and **Delta PnL** (16%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by a revaluation from the implied-volatility move, with spot drifting lower and theta contributing a smaller drag. Because the observation lock suppresses a stronger tape read and there are no retrieved headlines, the move is best read as a model reprice on the vol input rather than a news-led catalyst story. The residual is small, so higher-order effects are present but not the main explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is capped by the observation lock, the absence of retrieved headlines, and the note to suppress a Vega narrative, even though the coded dominant driver is vega and the residual band is low. The data support a clean model revaluation, but not a deeper event-based explanation.

---

## 2. Observation Lock

* **As-of**: `2026-09-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.3%)
* **IV move**: -0.35 vol pts vs noise band ±0.56 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$300.0000`
* **Model ΔP (engine)**: `+$300.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$292.6532`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$7.3468` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$74.8052` | -24.9% | Stock moved from $337.02 to $335.92 (-1.1000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.6409` | +0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$379.7727` | +126.6% | IV moved +7.97 vol pts (29.43% → 29.08%) |
| **Theta decay (Δt · Theta)** | `-$12.9552` | -4.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$7.3468` | +2.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$300.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$7.3468` (2.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.1019`
* Combined: `+$0.1019` | Residual after: `+$2.8981`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Review the full-surface reprice and confirm the volatility input change is the main source of the day’s option move rather than the mild spot drift.
* No catalyst mechanism is available from the digest, so treat the move as a model-driven repricing and avoid adding a news or microstructure story.
* 
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.02 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-09-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$152.5000` (-1815.5%)
* **Model ΔP**: `-$152.5000`
* **Primary drivers**: **Vega PnL** (78%) and **Delta PnL** (16%).
* **Verdict**: The move is dominated by the option’s sensitivity to the implied-volatility drop, with spot drifting lower only as a secondary effect. The residual is small, so the Taylor run is broadly consistent with the engine revaluation rather than a truncation or early-exercise problem. The Apple Pay India headline is company-specific background that fits the broader repricing of Apple optionality, but it does not replace the modeled vol driver.
* **Confidence**: **Medium** — The attribution is internally consistent and observation quality is reliable, but the run has a moderate vol move and a named company-specific headline that supports the backdrop more than a direct causal chain. The American feature does not look material here, and the residual is small, so the main uncertainty is only how much of the move was broader implied-vol repricing versus the specific Apple headline context.

---

## 2. Observation Lock

* **As-of**: `2026-09-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.5%)
* **IV move**: -0.80 vol pts vs noise band ±0.25 pts (exceeds noise band)
* **Prior observation**: `2026-09-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$152.5000`
* **Model ΔP (engine)**: `-$152.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$155.2530`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$2.7530` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$42.6486` | -28.0% | Stock moved from $337.02 to $335.92 (-1.1000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.7121` | +0.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$209.5278` | +137.4% | IV moved +4.11 vol pts (26.86% → 26.06%) |
| **Theta decay (Δt · Theta)** | `+$12.3383` | -8.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$2.7530` | -1.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$152.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$2.7530` (1.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0053`
* Combined: `-$0.0053` | Residual after: `+$1.5303`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: One headline is directly about Apple and its Apple Pay expansion ambitions in India. The remaining items are broad market or unrelated peer/context headlines, so they are treated as background rather than company-specific signals._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Apple (AAPL) Eyes an Apple Pay Launch in India. How Much can it Grow Without UPI?** _(Source: Insider Monkey)_
   The headline is about Apple and discusses a potential Apple Pay launch in India, making it directly relevant to the target company.

_Peer / sector background (indirect context, not a required catalyst):_

2. **Trump says China's Xi 'seemed to like' renaming AI as super intelligence** _(Source: Yahoo Finance)_
   Broad macro/tech policy commentary that could be background for large-cap tech sentiment, but it does not mention Apple directly.
3. **Over 30 CEOs scored an invite to the US-China state dinner — and these 4 got a spot at the head table** _(Source: Yahoo Finance)_
   General business and policy context involving major CEOs and US-China relations; potentially background for Apple as a large multinational, but not company-specific.
4. **Costco options flow analysis after earnings beat** _(Source: Investing.com)_
   Unrelated peer/market headline with no direct connection to Apple; kept as a general market reference.

---

## 7. Risk Watchlist

* Verify the full-surface reprice against the observed implied-vol move; the Greek decomposition is already close, so the main question is vol sensitivity rather than spot.
* Keep the Apple Pay India catalyst in the backdrop and monitor for implied-vol repricing in the chain; there is no separate borrow, squeeze, or early-exercise theme here.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-09-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$150.0000` (+3015.1%)
* **Model ΔP**: `+$150.0000`
* **Primary drivers**: **Vega PnL** (72%) and **Delta PnL** (18%) and **Theta decay** (9%).
* **Verdict**: The move is dominated by the model’s vega bucket: the option revalued higher as implied volatility fell, with spot contributing a smaller secondary lift and theta offsetting part of the gain. The headline set is mostly background, so the price change is best read as a volatility-led repricing rather than a news-driven directional move; the relevant JPM item is context, not a named microstructure event.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is strong, the residual is small, and the observation is reliable. The main limitation is that the available news does not supply a direct JPM-specific catalyst mechanism, so Layer B is thin and remains contextual rather than causal.

---

## 2. Observation Lock

* **As-of**: `2026-09-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 10.0%)
* **IV move**: -1.01 vol pts vs noise band ±0.93 pts (exceeds noise band)
* **Prior observation**: `2026-09-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$150.0000`
* **Model ΔP (engine)**: `+$150.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$148.5926`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.4074` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$32.9662` | +22.0% | Stock moved from $337.53 to $338.56 (+1.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.7653` | +0.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$131.6011` | +87.7% | IV moved +3.88 vol pts (26.83% → 25.82%) |
| **Theta decay (Δt · Theta)** | `-$16.7399` | -11.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.4074` | +0.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$150.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.4074` (0.9% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0480`
* Combined: `+$0.0480` | Residual after: `+$1.4520`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: There is one JPM-specific headline and two bank-sector peers/commentary items that may provide context. The remaining items are generic or unrelated and do not inform the JPM story._
_Intel triage discarded 3 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Higher Lithium Prices Strengthen J.P. Morgan’s Case, But Execution Still Matters** _(Source: Insider Monkey)_
   The headline explicitly references J.P. Morgan, making it relevant to JPM as a company-specific mention rather than a broad sector note.

_Peer / sector background (indirect context, not a required catalyst):_

2. **Bank of America Says Stocks Are Overdue for a Pullback. These 2 Financial Stocks Are Built for One.** _(Source: Motley Fool)_
   This is a financial-sector commentary piece that could be context for bank stocks, but it does not specifically identify JPM or a JPM-related control story.
3. **Citigroup targets over $3 billion Banamex IPO for January - Bloomberg** _(Source: Investing.com)_
   This is a peer-bank capital-markets headline and serves only as sector background for large U.S. banks.

---

## 7. Risk Watchlist

* Recheck the full-surface reprice and the volatility input path, since the modeled move is primarily explained by the vol bucket with only a minor residual.
* Treat the JPM-specific headline as background context only; there is no supported borrow, squeeze, or IV-crush mechanism to add from the digest.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.23 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-09-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$327.5000` (-1852.9%)
* **Model ΔP**: `-$327.5000`
* **Primary drivers**: **Vega PnL** (72%) and **Delta PnL** (20%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is best explained by the modeled vega leg, with the option marked lower as implied volatility fell while spot drifted only modestly higher. Delta and theta were secondary contributors, and the small residual leaves the bulk of the move accounted for by the revaluation. The American style note indicates carry and dividend effects are present, but this is not an early-exercise case. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — The blotter gives a clean factor breakdown and the dominant driver is internally consistent, but observation reliability is flagged false and Vega narrative is suppressed by the run, so the interpretation should stay coarse. There are no headlines to anchor a separate catalyst story, and the residual is low enough that a large unmodeled event is not suggested.

---

## 2. Observation Lock

* **As-of**: `2026-09-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 12.5%)
* **IV move**: -0.62 vol pts vs noise band ±3.22 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$327.5000`
* **Model ΔP (engine)**: `-$327.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$343.1255`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$15.6255` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.8%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$71.7828` | +21.9% | Stock moved from $337.53 to $338.56 (+1.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.7996` | -0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$259.7802` | +79.3% | IV moved -7.88 vol pts (30.66% → 30.04%) |
| **Theta decay (Δt · Theta)** | `-$12.3621` | +3.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$15.6255` | -4.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$327.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$15.6255` (4.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0322`
* Combined: `+$0.0322` | Residual after: `-$3.3072`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$1.0300` vs next cash dividend `+$1.5000` (gap `+$2.5300`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$14.4000` vs `+$13.4165` (gap `+$0.9835`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.2346` — material
* **Dividend PV effect** (European, same divs − no divs): `+$0.7485`
* **Dividend coverage** (dividend / time value): `0.51` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$2.5978`
* **Residual (Taylor ε)**: `+$0.1563`
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

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Verify the full-surface reprice and quote quality around the IV reset, since the model change is primarily explained by volatility rather than spot.
* Track dividend and carry effects in the American pricing framework; the dividend does not cover remaining time value, so early exercise is not the issue here.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.51 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-09-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$79.5000` (+1715.2%)
* **Model ΔP**: `+$79.5000`
* **Primary drivers**: **Vega PnL** (78%) and **Theta decay** (10%) and **Delta PnL** (9%).
* **Verdict**: The run is driven by the model’s sensitivity to implied volatility: the option gains on the back of the IV move dominate the day-to-day revaluation, while spot and gamma are secondary. The small residual is consistent with higher-order effects and truncation, not a competing story. Broad index-market tone in the headlines is only background for SPY here and does not override the modeled vega-led move.
* **Confidence**: **Medium** — Confidence is supported by the code-selected driver, high attribution coverage, and reliable observations, but the residual is not zero and the surface notes show a deferred calibration limitation. The news set is broad rather than SPY-specific, so it supports the index backdrop without providing a stronger catalyst than the model factor.

---

## 2. Observation Lock

* **As-of**: `2026-09-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.5%)
* **IV move**: -0.12 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-09-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$79.5000`
* **Model ΔP (engine)**: `+$79.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$82.3889`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$2.8889` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$9.4253` | -11.9% | Stock moved from $767.81 to $767.18 (-0.6300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.0800` | -0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$80.9753` | +101.9% | IV moved -1.15 vol pts (18.25% → 18.13%) |
| **Theta decay (Δt · Theta)** | `+$10.9191` | +13.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$2.8889` | -3.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$79.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$2.8889` (3.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0181`
* Combined: `+$0.0181` | Residual after: `-$0.8131`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: The headlines are mostly broad market or S&P 500 commentary that can frame SPY, with no SPY-specific corporate mechanism identified. No relevant issuer-level headlines were found; the remaining items are either generic ETF content or single-name stories._
_Intel triage discarded 4 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **S&P 500, Dow, Nasdaq End Week Higher On Chipmaker Strength, Easing Oil Amid Signs Of Easing US-Iran Conflict — META, COST, MSFT, CRWD, SKHY In Focus** _(Source: Stocktwits)_
   Broad U.S. equity-market tape was higher, which can provide context for SPY as the S&P 500 ETF.
2. **S&P 500: Ready For A Melt Up (Technical Analysis) (SP500) - Seeking Alpha** _(Source: Seeking Alpha)_
   Commentary focused directly on the S&P 500 index, which is the underlying benchmark for SPY.

---

## 7. Risk Watchlist

* Reconcile the move with a full-surface reprice and treat the small residual as higher-order truncation rather than a separate driver.
* Use the broad index headlines as backdrop only; there is no SPY-specific catalyst or named market-structure mechanism to layer onto the vega story.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-09-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$115.5000` (+1873.5%)
* **Model ΔP**: `+$115.5000`
* **Primary drivers**: **Vega PnL** (83%) and **Delta PnL** (10%) and **Theta decay** (7%).
* **Verdict**: The move is primarily explained by the model’s vega sensitivity: the option gained as implied volatility rose while spot was essentially flat and delta pressure was minor. The residual is negligible, so the Taylor decomposition is doing most of the work; there is no meaningful early-exercise effect in this setup. Background tape around broader index strength can fit the SPY context, but it is secondary to the volatility-driven revaluation.
* **Confidence**: **Medium** — Confidence is medium because the observation is reliable and the residual is low, but the news set is mostly broad-market background rather than SPY-specific catalyst flow. The dividend and early-exercise checks are also negligible, so the main uncertainty is simply that the tape does not supply a clean external catalyst for the vol move.

---

## 2. Observation Lock

* **As-of**: `2026-09-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.8%)
* **IV move**: +0.12 vol pts vs noise band ±0.03 pts (exceeds noise band)
* **Prior observation**: `2026-09-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$115.5000`
* **Model ΔP (engine)**: `+$115.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$115.7524`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.2524` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$17.3656` | -15.0% | Stock moved from $767.81 to $767.18 (-0.6300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1781` | +0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$145.5691` | +126.0% | IV moved +1.44 vol pts (13.41% → 13.53%) |
| **Theta decay (Δt · Theta)** | `-$12.6292` | -10.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.2524` | -0.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$115.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.2524` (0.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0144`
* Combined: `+$0.0144` | Residual after: `+$1.1406`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega expansion / implied volatility rise**._

_Intel note: The SPY tape here is mostly broad-market and index commentary rather than ETF-specific issuer news. I kept the S&P 500-related items as background and discarded unrelated single-name coverage._
_Intel triage discarded 4 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **S&P 500, Dow, Nasdaq End Week Higher On Chipmaker Strength, Easing Oil Amid Signs Of Easing US-Iran Conflict — META, COST, MSFT, CRWD, SKHY In Focus** _(Source: Stocktwits)_
   Broad U.S. equity index strength and sector rotation are market backdrop items for SPY; the headline centers on index and mega-cap moves rather than SPY-specific news.
2. **S&P 500: Ready For A Melt Up (Technical Analysis) (SP500) - Seeking Alpha** _(Source: Seeking Alpha)_
   This is direct S&P 500 commentary and is background for SPY because the ETF tracks the index; it is technical market commentary rather than an issuer event.

---

## 7. Risk Watchlist

* Use a full-surface reprice check for the option’s volatility sensitivity rather than forcing the small spot move to explain the change.
* Treat the broad-market headlines as supportive context only; there is no SPY-specific squeeze, borrow, or early-exercise angle to carry the narrative.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-09-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$21.0000` (-684.0%)
* **Model ΔP**: `-$21.0000`
* **Primary drivers**: **Vega PnL** (56%) and **Delta PnL** (35%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter’s modeled explanation is dominated by implied volatility moving lower, which more than offsets the positive spot move and leaves the option weaker on a full revaluation basis. Because observation is unreliable and the Vega narrative is suppressed, the run should be treated as a cautious model read rather than a firm economic claim. The residual is sizable enough to point to higher-order effects and American boundary behavior as part of the gap, and the dividend setup makes early exercise economically relevant. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Low** — Confidence is low because the observation is flagged unreliable, the Vega narrative is explicitly suppressed, and the residual share is large. There are no retrieved headlines to anchor an external catalyst, so the diagnostic rests on model revaluation and the American-vs-European dividend setup rather than news confirmation.

---

## 2. Observation Lock

* **As-of**: `2026-09-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 23.8%)
* **IV move**: +2.03 vol pts vs noise band ±6.07 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$21.0000`
* **Model ΔP (engine)**: `-$21.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$28.7272`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$7.7272` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (36.8%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$48.6873` | -231.8% | Stock moved from $46.52 to $47.32 (+0.8000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$2.1574` | -10.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$76.9146` | +366.3% | IV moved -11.14 vol pts (25.64% → 27.66%) |
| **Theta decay (Δt · Theta)** | `-$2.6573` | +12.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$7.7272` | -36.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$21.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$7.7272` (36.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0931`
* Combined: `+$0.0931` | Residual after: `-$0.3031`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0266`
* **spot**: `+$0.5079`
* **vol**: `-$0.6914`
* **rate**: `+$0.0001`
* Step sum: `-$0.2099` | Model ΔP: `-$0.2100` | Audit residual: `-$0.0001`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$0.8000` vs next cash dividend `+$0.7080` (gap `+$1.5080`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$2.8600` vs `+$2.9677` (gap `-$0.1077`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0795` — material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1874`
* **Dividend coverage** (dividend / time value): `1.31` — early exercise is economically relevant
* **Vol (Taylor Vega PnL)**: `-$0.7691`
* **Residual (Taylor ε)**: `+$0.0773`
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
* Recheck the full-surface revaluation and path-reprice output before leaning on the Greek split, since truncation and boundary shifts are material here.
* Keep the dividend and early-exercise boundary in view, because the remaining time value is close enough to make exercise economically relevant.
* **Assignment watch**: ex-div `2026-10-09` — Dividend coverage 1.31 (dividend $0.7080 vs time value $0.5400); ex-div is 14d out, expiry 56d out — early exercise is economically relevant.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-09-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (47%) and **Delta PnL** (41%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by the volatility revaluation in the option surface, with spot and time decay playing secondary roles. However, the observation lock and suppressed Vega narrative mean the tape does not support a stronger catalyst claim; the large residual instead points to higher-order model effects and surface fit limits rather than a clean news-driven explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is only medium because the observation is unreliable, the attribution coverage is low, and the residual band is high. The run also flags a suppressed Vega narrative and no retrieved headlines, so the diagnosis should stay at the modeled revaluation level rather than infer a specific event.

---

## 2. Observation Lock

* **As-of**: `2026-09-25` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 28.6%)
* **IV move**: -0.78 vol pts vs noise band ±3.08 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-24`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0833`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0833` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (170315461.3%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.7851` | +40.8% | Stock moved from $2.04 to $1.96 (-0.0800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0618` | +3.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.8993` | +46.8% | IV moved +5.28 vol pts (96.88% → 96.09%) |
| **Theta decay (Δt · Theta)** | `-$0.0927` | +4.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0833` | +4.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0833` (170315461.3% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0009`
* Combined: `-$0.0009` | Residual after: `+$0.0009`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0009`
* **spot**: `-$0.0071`
* **vol**: `+$0.0080`
* **rate**: `+$0.0000`
* Step sum: `+$0.0000` | Model ΔP: `-$0.0000` | Audit residual: `-$0.0000`

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
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Recheck the full-surface revaluation and quote quality before leaning on the Taylor split, since the residual is elevated and the run was not observation-reliable.
* Keep the explanation at the level of implied volatility and model fit; there is no supported catalyst mechanism to assign from headlines in this run.

---


## Skew proxy (Task C3.3, SPY risk reversal)

* skew_proxy(t) = +0.0460 | level_proxy(t) = 0.1583
* Δskew = -0.0024 | Δlevel = -0.0000
* Put 715 delta=-0.1365 | Call 795 delta=0.2911
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
