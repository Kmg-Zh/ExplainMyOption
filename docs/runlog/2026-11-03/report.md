# Live book run — 2026-11-03

Run `2026-11-03-1793758928`. 6/8 legs completed, 2 failed. `legs_narrated=5` `legs_silent=1` `llm_calls=8`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-03` | **Positions**: 6 | **Tickers**: AAPL, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `-$383.5000`
* **Total Model PnL**: `-$439.2852`
* **Aggregate model vs mark gap**: `-$55.7852`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 325C 2026-11-20` | `-$875.7852` |
| 2 | `AAPL 350C 2026-11-20` | `+$387.5000` |
| 3 | `SPY 715P 2026-11-20` | `+$42.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$194.3697` |
| Gamma | `-$12.1984` |
| Vega | `-$173.0090` |
| Theta | `+$8.9903` |
| Residual | `-$68.6985` |

### Notable underlyings

* **AAPL**: `-$488.2852` aggregate option PnL
* **SPY**: `+$47.0000` aggregate option PnL
* **VZ**: `+$2.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-03` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$820.0000` (-34.1%)
* **Model ΔP**: `-$875.7852`
* **Primary drivers**: **Delta PnL** (-53.4%) and **Vega PnL** (-44.5%).
* **Verdict**: The move is best explained by the contract’s positive delta being hit by the lower underlying, with a smaller assist from the concurrent implied volatility reset and normal time decay. The residual is small, so the Taylor view is broadly sufficient; the broader tape is consistent with IV crush, but the headlines provided are generic options and peer-earnings context rather than Apple-specific catalysts, so they support the volatility backdrop rather than a company-specific event.
* **Confidence**: **Medium** — Confidence is medium because the attribution is clean and the residual is low, but the feed also shows an extreme implied-vol move while the available headlines are not Apple-specific. The market data quality is usable, yet the disclosed limitations mean the volatility story should be treated as tape context rather than an issuer-news claim.

---

## 2. Observation Lock

* **As-of**: `2026-11-03` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.0%)
* **IV move**: -15.73 vol pts vs noise band ±1.30 pts (exceeds noise band)
* **Prior observation**: `2026-11-02`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$820.0000`
* **Model ΔP (engine)**: `-$875.7852`
* **Model vs Mark gap**: `-$55.7852` (+6.4% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$872.5144`

* **Method residual (ε_method)**: `-$3.2708` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$55.7852` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$467.4105` | -53.4% | Stock moved from $344.63 to $338.32 (-6.3100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$18.6274` | +2.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$389.7146` | -44.5% | IV moved -15.73 vol pts (45.26% → 29.53%) |
| **Theta decay (Δt · Theta)** | `-$34.0167` | -3.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$3.2708` | -0.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$875.7852** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$3.2708` (0.4% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$40.0324` | Volga PnL: `+$23.8341`
* Combined: `-$16.1983` | Residual after: `+$12.9275`

### Ex-div attribution overlay (official PnL stays the American FDM Taylor blotter)
* **Spot drop vs dividend** (per share): spot `-$6.3100` vs next cash dividend `+$0.2700` (gap `-$6.0400`)
* **American FDM vs European analytic (no cash div, cross-check, per option)**: `+$16.9545` vs `+$17.1175` (gap `-$0.1630`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored, per option): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs, per option): `-$0.1636`
* **Dividend coverage** (dividend / time value): `0.07` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$389.7146`
* **Residual (Taylor ε)**: `-$3.2708`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `american_dividend_exercise_check`
* **Skipped candidates**:
  * `compare_to_official` — american check outranks model-risk cross-check

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Intel note: The items are general options education and peer-earnings pieces rather than Apple-specific company news. No relevant Apple issuer or control-structure headline is present in the provided set._
_Intel triage discarded 3 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. [Implied Volatility Explained for Options Traders | Vanquish](https://www.vanquishtrader.com/implied-volatility)
2. [PEP Stock Before Earnings: Why Calls Lose on a ±3.5% Move](https://earnings-watcher.com/wiki/pep-stock-before-earnings)
3. [META Stock Before Earnings: Why Calls Lose on a ±7.0% Move](https://earnings-watcher.com/wiki/meta-stock-before-earnings)

---

## 7. Risk Watchlist

* Model attribution is dominated by spot sensitivity; the remaining slippage is small, so any larger discrepancy would more likely come from a fuller surface reprice or higher-order convexity than from the displayed residual.
* The tape supports an IV crush / implied-volatility reset backdrop, but the supplied headlines are not Apple-specific, so confirm whether the volatility move was event-driven or simply a broad repricing of option premiums.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.07 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-03` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$387.5000` (-72.1%)
* **Model ΔP**: `+$387.5000`
* **Primary drivers**: **Vega PnL** (+61.4%) and **Delta PnL** (+56.4%) and **Gamma PnL** (-7.9%).
* **Verdict**: The move is dominated by a revaluation of the option’s volatility component, with spot down only modestly while implied volatility fell sharply; that leaves the vega bucket as the main modeled driver of the daily change. The residual is sizable enough to reflect Taylor truncation and path effects, but it does not displace the core vol story. The tape also supports an IV crush narrative, and the peer-style earnings commentary is consistent only as background for that vol compression rather than as an Apple-specific catalyst.
* **Confidence**: **Medium** — Confidence is medium because the attribution is internally consistent and the observation is reliable, but the residual is elevated and the headlines are generic rather than issuer-specific. The dominant driver is clear from the blotter, while the auxiliary catalyst context is limited to an IV crush theme with no Apple-specific news mechanism.

---

## 2. Observation Lock

* **As-of**: `2026-11-03` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 8.0%)
* **IV move**: -9.09 vol pts vs noise band ±0.34 pts (exceeds noise band)
* **Prior observation**: `2026-11-02`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$387.5000`
* **Model ΔP (engine)**: `+$387.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$452.2926`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$64.7926` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (16.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$218.4237` | +56.4% | Stock moved from $338.32 to $331.90 (-6.4200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$30.5874` | -7.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$237.8138` | +61.4% | IV moved -8.64 vol pts (32.88% → 24.24%) |
| **Theta decay (Δt · Theta)** | `+$26.6424` | +6.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$64.7926` | -16.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$387.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$64.7926` (16.7% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$24.3644` | Volga PnL: `-$5.6858`
* Combined: `-$30.0502` | Residual after: `-$34.7424`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$26.6307`
* **spot**: `+$184.5861`
* **vol**: `+$176.1582`
* **rate**: `-$0.1076`
* Step sum: `+$387.2675` | Model ΔP: `+$387.5000` | Audit residual: `+$0.2325`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: The headlines are generic options education and peer earnings commentary, with no Apple-specific issuer or control-structure news. None of the items provides a direct Apple-linked catalyst or mechanism for AAPL._
_Intel triage discarded 3 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. [Implied Volatility Explained for Options Traders | Vanquish](https://www.vanquishtrader.com/implied-volatility)
2. [PEP Stock Before Earnings: Why Calls Lose on a ±3.5% Move](https://earnings-watcher.com/wiki/pep-stock-before-earnings)
3. [META Stock Before Earnings: Why Calls Lose on a ±7.0% Move](https://earnings-watcher.com/wiki/meta-stock-before-earnings)

---

## 7. Risk Watchlist

* Monitor whether the remaining gap is still best explained by Taylor truncation and path effects rather than a change in the underlying driver mix.
* Watch for continued implied volatility compression and any broader IV crush setup in the tape, since that is the named mechanism consistent with the revaluation.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.18 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-03` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$42.5000` (-12.9%)
* **Model ΔP**: `+$42.5000`
* **Primary drivers**: **Delta PnL** (+82.2%) and **Theta decay** (+59.6%) and **Vega PnL** (-38.9%).
* **Verdict**: The position moved mainly on the modeled spot-sensitive reprice, with the put losing value as the index edged higher. Theta provided a meaningful offset, while the small volatility uptick worked against the position; the residual is minimal and consistent with a clean attribution. There are no retrieved headlines or named catalyst tags, so the tape reads as a factor-driven move rather than a news-led one.
* **Confidence**: **Medium** — Confidence is medium because the blotter is well calibrated and the residual is low, but the move is still a reference revaluation rather than a direct mark-to-market tape. The news layer is empty, so there is no external catalyst to validate beyond the modeled spot and carry effects.

---

## 2. Observation Lock

* **As-of**: `2026-11-03` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.1%)
* **IV move**: +0.46 vol pts vs noise band ±0.08 pts (exceeds noise band)
* **Prior observation**: `2026-11-02`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$42.5000`
* **Model ΔP (engine)**: `+$42.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$42.2183`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.2817` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$34.9479` | +82.2% | Stock moved from $752.10 to $754.35 (+2.2500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$1.5292` | -3.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$16.5289` | -38.9% | IV moved +0.41 vol pts (23.70% → 24.12%) |
| **Theta decay (Δt · Theta)** | `+$25.3285` | +59.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.2817` | +0.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$42.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.2817` (0.7% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.8917` | other second-order: `-$0.1458`
* Combined: `+$0.7459` | Residual after: `-$0.4642`

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

* Watch for truncation from the Taylor view if spot movement becomes larger or the full-surface reprice starts to diverge from the reference decomposition.
* No Layer B catalyst is available here; there is no basis to invoke IV crush, borrow stress, squeeze, or liquidity effects from the digest.

---

### Position 4 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-03` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$4.5000` (+11.8%)
* **Model ΔP**: `+$4.5000`
* **Primary drivers**: **Delta PnL** (+204.9%) and **Theta decay** (-126.8%) and **Vega PnL** (+22.0%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is primarily a delta-led repricing of the call as spot edged higher, with gamma adding some convexity and theta working against the position. The residual is consistent with higher-order truncation and path effects in a short-dated American option, while the implied-vol move was small and the setup does not support a separate Vega narrative. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The blotter supplies a clear dominant Taylor driver and the headline set is empty, but observation reliability is limited and the residual share is elevated. That makes the factor read useful while keeping the catalyst layer intentionally coarse.

---

## 2. Observation Lock

* **As-of**: `2026-11-03` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 7.1%)
* **IV move**: +0.09 vol pts vs noise band ±0.10 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-02`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$4.5000`
* **Model ΔP (engine)**: `+$4.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$5.4646`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.9646` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (21.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$9.2217` | +204.9% | Stock moved from $752.10 to $754.35 (+2.2500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.9615` | +21.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.9895` | +22.0% | IV moved +0.07 vol pts (13.85% → 13.92%) |
| **Theta decay (Δt · Theta)** | `-$5.7080` | -126.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.9646` | -21.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$4.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.9646` (21.4% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.2067` | other second-order: `+$0.0074`
* Combined: `+$0.2141` | Residual after: `-$1.1787`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$5.6960`
* **spot**: `+$9.1423`
* **vol**: `+$1.0497`
* **rate**: `+$0.0686`
* Step sum: `+$4.5645` | Model ΔP: `+$4.5000` | Audit residual: `-$0.0645`

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
* Higher-order effects and full engine repricing can still account for part of the residual in a short-dated option.
* No named catalyst, squeeze, borrow, or IV-crush evidence was retrieved, so watch for any future headlines or quote changes before attaching a market-event explanation.

---

### Position 5 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-03` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$2.5000` (+2.1%)
* **Model ΔP**: `+$2.5000`
* **Primary drivers**: **Delta PnL** (+54.9%) and **Vega PnL** (-25.3%) and **Theta decay** (-17.7%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-11-03` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 13.4%)
* **IV move**: -1.22 vol pts vs noise band ±2.07 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-02`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$2.5000`
* **Model ΔP (engine)**: `+$2.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$2.3642`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.1358` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (5.4%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$9.7527` | +54.9% | Stock moved from $45.05 to $45.24 (+0.1900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.2473` | +1.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$4.4973` | -25.3% | IV moved -1.13 vol pts (29.21% → 28.07%) |
| **Theta decay (Δt · Theta)** | `-$3.1384` | -17.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.1358` | +0.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$2.5000** | **+14.1%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.1358` (5.4% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `+$0.0115`
* Combined: `+$0.0115` | Residual after: `+$0.1242`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Observation unreliable — event linkage suppressed; reconcile marks before catalyst stories._


---

## 7. Risk Watchlist

* No action needed; move is within theta/carry tolerance.

---

### Position 6 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-03` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$0.5000` (-25.0%)
* **Model ΔP**: `-$0.5000`
* **Primary drivers**: **Vega PnL** (-52.2%) and **Delta PnL** (+33.8%) and **Theta decay** (-5.7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by the option’s sensitivity to implied volatility: the mark fell as spot rose, but the vol reset was the main modeled drag on the revaluation. Delta and gamma helped offset some of that move, while the remaining gap is consistent with a larger higher-order residual in a low-confidence tape. There are no relevant headlines in the digest, so Layer B is limited to the observable vol move rather than an external catalyst story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation reliability is false, the residual band is high, and the surface diagnostics show a failed American surface check. The only clear explanatory evidence is the large implied-vol move in the blotter; there are no retrieved headlines or named microstructure tags to support a separate catalyst narrative.

---

## 2. Observation Lock

* **As-of**: `2026-11-03` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 66.7%)
* **IV move**: -15.62 vol pts vs noise band ±9.09 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-02`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$0.5000`
* **Model ΔP (engine)**: `-$0.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$0.4120`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0880` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (17.6%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.6948` | +33.8% | Stock moved from $1.31 to $1.41 (+0.1000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0821` | +4.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$1.0715` | -52.2% | IV moved -17.26 vol pts (174.86% → 157.61%) |
| **Theta decay (Δt · Theta)** | `-$0.1174` | -5.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0880` | -4.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.5000** | **-24.3%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0880` (17.6% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.2804` | Volga PnL: `+$0.1644`
* Combined: `-$0.1160` | Residual after: `+$0.0280`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.1174`
* **spot**: `+$0.7471`
* **vol**: `-$1.1297`
* **rate**: `+$0.0003`
* Step sum: `-$0.4996` | Model ΔP: `-$0.5000` | Audit residual: `-$0.0004`

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
* Higher-order curvature and full-surface repricing can still distort the modeled attribution when the residual band is high, so treat the Greek split as a reference view rather than a complete explanation.
* Watch the implied-vol reset and quote quality; with no named headline mechanism available, there is no separate borrow, squeeze, or IV-crush catalyst to validate.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0947 | level_proxy(t) = 0.1906
* Δskew = +0.0037 | Δlevel = +0.0027
* Put 715 delta=-0.1399 | Call 795 delta=0.0460
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **jpm_straddle_call** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-11, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
- **jpm_straddle_put** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-11, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
