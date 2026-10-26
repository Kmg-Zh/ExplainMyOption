# Live book run — 2026-10-23

Run `2026-10-23-1792804803`. 6/8 legs completed, 2 failed. `legs_narrated=6` `legs_silent=0` `llm_calls=9`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-23` | **Positions**: 6 | **Tickers**: AAPL, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$128.0000`
* **Total Model PnL**: `-$128.0000`
* **Aggregate model vs mark gap**: `+$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `-$77.5000` |
| 2 | `AAPL 350C 2026-11-20` | `+$67.5000` |
| 3 | `SPY 795C 2026-11-20` | `-$60.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$91.3513` |
| Gamma | `+$41.9711` |
| Vega | `-$111.5163` |
| Theta | `-$0.3939` |
| Residual | `+$33.2905` |

### Notable underlyings

* **SPY**: `-$90.5000` aggregate option PnL
* **VZ**: `-$30.0000` aggregate option PnL
* **AAPL**: `-$10.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$77.5000` (-281.3%)
* **Model ΔP**: `-$77.5000`
* **Primary drivers**: **Vega PnL** (52%) and **Delta PnL** (37%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter’s dominant modeled driver is vega: the option was marked against a lower implied-volatility level, and that more than offset the positive spot move and the smaller theta drag. However, observation quality is weak and the run is explicitly suppressing a fuller Vega narrative, so the attribution should be treated as a model reprice rather than a clean market-tape story. There are no retrieved headlines or relevant microstructure tags, so there is no supported Layer B catalyst beyond the full revaluation itself. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is limited by the observation flag and the suppressed Vega narrative, which means the data should be read conservatively. The residual is sizable relative to the modeled move, so higher-order convexity and path effects likely matter, but there is no headline evidence to attach a catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-10-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.9%)
* **IV move**: -0.47 vol pts vs noise band ±2.09 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$77.5000`
* **Model ΔP (engine)**: `-$77.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$138.6790`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$61.1790` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (78.9%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$301.2700` | -388.7% | Stock moved from $343.99 to $348.22 (+4.2300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$7.5086` | -9.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$420.9710` | +543.2% | IV moved -12.73 vol pts (35.12% → 34.65%) |
| **Theta decay (Δt · Theta)** | `-$26.4866` | +34.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$61.1790` | -78.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$77.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$61.1790` (78.9% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.5369`
* Combined: `+$0.5369` | Residual after: `-$1.3119`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2648`
* **spot**: `+$3.0968`
* **vol**: `-$3.6072`
* **rate**: `+$0.0020`
* Step sum: `-$0.7733` | Model ΔP: `-$0.7750` | Audit residual: `-$0.0017`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$4.2300` vs next cash dividend `+$0.2700` (gap `+$4.5000`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$26.7750` vs `+$26.9242` (gap `-$0.1492`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1501`
* **Dividend coverage** (dividend / time value): `0.08` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$4.2097`
* **Residual (Taylor ε)**: `+$0.6118`
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
* Watch for Taylor truncation and path effects to be the main distorter of the modeled attribution when the spot move is larger than the first-order decomposition suggests.
* Verify whether the implied volatility mark is stable and whether quote quality improves, since the current run does not support a cleaner catalyst-based explanation.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.08 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$67.5000` (+650.6%)
* **Model ΔP**: `+$67.5000`
* **Primary drivers**: **Vega PnL** (52%) and **Delta PnL** (41%).
* **Verdict**: The modeled move is led by a vega reset, with the option repriced lower as implied volatility fell while the stock also moved up and partly offset the decay. The residual is small, so the Taylor story is largely intact; the headline set is consistent with an earnings setup where calls can lose value on the implied-volatility reset, and that earnings / iv crush backdrop helps explain the tape.
* **Confidence**: **Medium** — Confidence is medium because the data-quality flags are good and the residual is low, but the event backdrop is still auxiliary rather than a direct pricing feed. The position is a call into an earnings-linked vol reset, so the modeled vega line is well supported, while the modest spot move and carry effects keep some attribution interaction in play.

---

## 2. Observation Lock

* **As-of**: `2026-10-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.1%)
* **IV move**: -0.68 vol pts vs noise band ±0.39 pts (exceeds noise band)
* **Prior observation**: `2026-10-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$67.5000`
* **Model ΔP (engine)**: `+$67.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$66.5711`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.9289` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$192.2062` | -284.7% | Stock moved from $343.99 to $348.22 (+4.2300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$11.1397` | -16.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$246.3592` | +365.0% | IV moved -6.41 vol pts (29.09% → 28.41%) |
| **Theta decay (Δt · Theta)** | `+$23.5578` | +34.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.9289` | +1.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$67.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.9289` (1.4% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0500`
* Combined: `-$0.0500` | Residual after: `-$0.6250`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: The tape is Apple-specific overall: one headline is directly about AAPL into earnings and the associated implied-volatility reset, while another is a general AAPL market-structure analysis. A Visa earnings headline is kept only as background sector context._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **AAPL Stock Before Earnings: Why Calls Lose on a ±5.8% Move** _(Source: earnings-watcher.com)_
   The headline ties Apple to its upcoming earnings event and frames the options move risk around post-earnings implied volatility compression.
2. **Apple (AAPL) Options Analysis & Market Structure — 2026-10-19 | Jason Wheel** _(Source: Jason Wheel)_
   This is an AAPL-specific options and market-structure piece focused on Apple rather than a peer or sector proxy.

_Peer / sector background (indirect context, not a required catalyst):_

3. **V Stock Before Earnings: Why Calls Lose on a ±4.0% Move** _(Source: earnings-watcher.com)_
   Visa is a peer large-cap earnings headline that may be useful as sector context, but it is not Apple-specific.

---

## 7. Risk Watchlist

* Watch whether the modeled attribution remains stable if the same engine is rerun through the full surface, since truncation and surface curvature can still shift the split between spot and vol terms.
* Track the earnings and iv crush backdrop, because a further implied-volatility reset would keep the event-driven repricing theme in focus.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$30.5000` (-995.1%)
* **Model ΔP**: `-$30.5000`
* **Primary drivers**: **Delta PnL** (50%) and **Vega PnL** (30%) and **Theta decay** (8%).
* **Verdict**: The move is dominated by the spot drop in the underlying, which the Taylor view identifies as the main modeled driver of the option revaluation. Gamma, vega, and theta partially offset that move, while the remaining gap is consistent with higher-order effects and path-dependent revaluation rather than a separate catalyst. With no relevant headlines retrieved, there is no supported Layer B mechanism to add beyond the model story.
* **Confidence**: **Medium** — Confidence is moderate because observation quality is reliable and the attribution coverage is high, but the residual is still meaningful and the spot move is categorized as small, so Taylor truncation and path effects can matter. There are no relevant headlines or microstructure tokens, so no external catalyst can be tied to the move.

---

## 2. Observation Lock

* **As-of**: `2026-10-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.8%)
* **IV move**: -0.13 vol pts vs noise band ±0.07 pts (exceeds noise band)
* **Prior observation**: `2026-10-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$30.5000`
* **Model ΔP (engine)**: `-$30.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$40.2984`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$9.7984` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (32.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$104.8286` | +343.7% | Stock moved from $773.09 to $763.96 (-9.1300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$15.2080` | +49.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$62.7026` | -205.6% | IV moved -1.48 vol pts (21.45% → 21.31%) |
| **Theta decay (Δt · Theta)** | `+$17.0357` | -55.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$9.7984` | -32.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$30.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$9.7984` (32.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0915`
* Combined: `-$0.0915` | Residual after: `+$0.3965`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1704`
* **spot**: `+$1.1782`
* **vol**: `-$0.7028`
* **rate**: `-$0.0008`
* Step sum: `+$0.3043` | Model ΔP: `+$0.3050` | Audit residual: `+$0.0007`

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

* Taylor truncation and path effects can still matter when the residual remains meaningful relative to the model move, so verify the full revaluation gap against the Greek buckets.
* No supported catalyst layer is available here; keep watching for any later evidence of implied volatility change, liquidity stress, or borrow-related tape if new headlines emerge.

---

### Position 4 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$60.0000` (->1000%)
* **Model ΔP**: `-$60.0000`
* **Primary drivers**: **Delta PnL** (46%) and **Vega PnL** (27%) and **Gamma PnL** (14%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model’s move is dominated by the downside spot gap, with the option’s sensitivity to the underlying doing most of the work in the revaluation. Gamma partly offset that move and theta was a smaller drag, but the remaining gap is consistent with Taylor truncation and path effects rather than a separate news catalyst. With no retrieved headlines and the observation lock in place, there is no Layer B mechanism to add beyond the model-based reprice. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is limited by the weak observation flag and the high residual share, so the Greek decomposition should be treated as a reference view rather than a perfect explanation. The market feed also shows no retrieved headlines, suppresses a Vega narrative, and provides no independent catalyst to challenge or refine the modeled attribution.

---

## 2. Observation Lock

* **As-of**: `2026-10-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.1%)
* **IV move**: +0.00 vol pts vs noise band ±0.04 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$60.0000`
* **Model ΔP (engine)**: `-$60.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$24.7446`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$35.2554` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (58.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$164.1611` | +273.6% | Stock moved from $773.09 to $763.96 (-9.1300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$51.4467` | -85.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$98.6860` | -164.5% | IV moved +1.73 vol pts (13.12% → 13.12%) |
| **Theta decay (Δt · Theta)** | `-$10.7162` | +17.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$35.2554` | +58.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$60.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$35.2554` (58.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.1849`
* Combined: `-$0.1849` | Residual after: `-$0.4151`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1071`
* **spot**: `-$1.1485`
* **vol**: `+$0.6560`
* **rate**: `+$0.0007`
* Step sum: `-$0.5989` | Model ΔP: `-$0.6000` | Audit residual: `-$0.0011`

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
* Model attribution may still be distorted by higher-order terms and path dependence given the large residual.
* No catalyst evidence was retrieved, so there is nothing to verify on borrow, squeeze, or implied volatility from the headline tape.

---

### Position 5 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$30.0000` (->1000%)
* **Model ΔP**: `-$30.0000`
* **Primary drivers**: **Vega PnL** (54%) and **Delta PnL** (37%) and **Gamma PnL** (5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is dominated by a volatility revaluation: the option was repriced lower as implied volatility eased, overwhelming the positive effect from the underlying rally. The spot move and second-order convexity helped offset some of that drag, but they did not overcome the vol reset; the small residual is consistent with truncation and path effects in the full revaluation. American early exercise is not a meaningful factor here because the premium versus European is negligible and the dividend does not cover remaining time value. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is limited by the observation lock and the explicit instruction to suppress a Vega narrative, even though the blotter’s coded dominant driver points to vol. There are no relevant headlines to support an auxiliary catalyst, and the residual is material enough that higher-order revaluation effects may be part of the gap.

---

## 2. Observation Lock

* **As-of**: `2026-10-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 10.0%)
* **IV move**: +0.44 vol pts vs noise band ±1.31 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$30.0000`
* **Model ΔP (engine)**: `-$30.0000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$26.1654`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$3.8346` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (12.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$68.7791` | -229.3% | Stock moved from $43.56 to $45.20 (+1.6400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$9.3562` | -31.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$100.6109` | +335.4% | IV moved -21.04 vol pts (30.32% → 30.76%) |
| **Theta decay (Δt · Theta)** | `-$3.6899` | +12.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$3.8346` | +12.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$30.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$3.8346` (12.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.1085`
* Combined: `-$0.1085` | Residual after: `-$0.1915`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0369`
* **spot**: `+$0.7796`
* **vol**: `-$1.0428`
* **rate**: `+$0.0001`
* Step sum: `-$0.2999` | Model ΔP: `-$0.3000` | Audit residual: `-$0.0001`

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
* Track whether the full revaluation remains sensitive to truncation and path-dependent effects rather than relying on the Taylor split alone.
* Watch for any later IV repricing or surface recalibration; no borrow, squeeze, or early-exercise catalyst is indicated in the current tape.

---

### Position 6 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-23` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$2.5000` (+>1000%)
* **Model ΔP**: `+$2.5000`
* **Primary drivers**: **Vega PnL** (75%) and **Delta PnL** (7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model move is dominated by the implied-volatility reset, with a smaller offset from the spot decline and decay. Because the observation is unreliable and the Vega narrative is suppressed, this should be read as a model reprice rather than a firm market tape explanation; the second-order residual is material enough to suggest truncation or surface effects may be part of the gap. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Low** — Confidence is low because observation quality is flagged as unreliable, the residual band is high, and the engine notes suppress the Vega narrative. There are no retrieved headlines or named microstructure mechanisms, so Layer B cannot be anchored to a catalyst, and the summary must stay at a coarse attribution level.

---

## 2. Observation Lock

* **As-of**: `2026-10-23` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 155.6%)
* **IV move**: +29.69 vol pts vs noise band ±31.78 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$2.5000`
* **Model ΔP (engine)**: `+$2.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$2.0259`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.4741` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (19.0%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.2045` | +6.6% | Stock moved from $1.41 to $1.38 (-0.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0072` | +0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$2.3178` | +74.8% | IV moved +31.62 vol pts (150.00% → 179.69%) |
| **Theta decay (Δt · Theta)** | `-$0.0947` | +3.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.4741` | +15.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$2.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.4741` (19.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0058`
* Combined: `+$0.0058` | Residual after: `+$0.0192`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0009`
* **spot**: `-$0.0019`
* **vol**: `+$0.0278`
* **rate**: `+$0.0000`
* Step sum: `+$0.0250` | Model ΔP: `+$0.0250` | Audit residual: `-$0.0000`

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
* Watch whether the residual remains elevated under a fuller surface reprice, since truncation and boundary effects can distort the Taylor split.
* Because there are no relevant headlines or microstructure tags, do not force a borrow, squeeze, or IV-crush interpretation without external confirmation.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0819 | level_proxy(t) = 0.1722
* Δskew = -0.0013 | Δlevel = -0.0006
* Put 715 delta=-0.1340 | Call 795 delta=0.1221
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **jpm_straddle_call** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-10-30, 2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
- **jpm_straddle_put** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-10-30, 2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
