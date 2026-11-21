# Live book run — 2026-11-20

Run `2026-11-20-1795227601`. 3/8 legs diagnosed, 5 settled at expiry, 0 failed. `legs_narrated=3` `legs_silent=0` `llm_calls=4`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-20` | **Positions**: 3 | **Tickers**: JPM, PLUG

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$850.0000`
* **Total Model PnL**: `+$850.0000`
* **Aggregate model vs mark gap**: `-$0.0000`
* **Settled at expiry**: `-$2,787.0000` across 5 leg(s), not in the totals above (see Settled at expiry)

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `JPM 340P 2026-12-18` | `+$967.5000` |
| 2 | `JPM 340C 2026-12-18` | `-$117.5000` |
| 3 | `PLUG 4C 2026-12-18` | `-$0.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$623.7286` |
| Gamma | `+$126.5408` |
| Vega | `+$204.1727` |
| Theta | `-$17.3188` |
| Residual | `-$87.1232` |

### Notable underlyings

* **JPM**: `+$850.0000` aggregate option PnL
* **PLUG**: `-$0.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `JPM 340C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340C 2026-12-18`  
**Analysis Date**: `2026-11-20` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$117.5000` (-49.6%)
* **Model ΔP**: `-$117.5000`
* **Primary drivers**: **Delta PnL** (-166.9%) and **Gamma PnL** (+52.2%) and **Vega PnL** (+43.2%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is dominated by the underlying selloff, which pulled the call lower and was partially cushioned by convexity and the higher implied-vol mark. The residual is meaningful, so the close-to-close Taylor view is only a reference and the gap is consistent with higher-order path effects rather than a separate named catalyst. American early exercise is not a factor here because the dividend does not justify exercising early at current marks. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The dominant driver is clear from the factor stack, but observation reliability is flagged false and the residual band is high, so the decomposition is not fully clean. There are no retrieved headlines or microstructure tokens to support a Layer B catalyst, and the early-exercise premium is negligible.

---

## 2. Observation Lock

* **As-of**: `2026-11-20` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 39.3%)
* **IV move**: +3.14 vol pts vs noise band ±1.42 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-19`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$117.5000`
* **Model ΔP (engine)**: `-$117.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$94.8186`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$22.6814` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (19.3%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$196.1432` | -166.9% | Stock moved from $320.22 to $310.53 (-9.6900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$61.3410` | +52.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$50.8175` | +43.2% | IV moved +2.00 vol pts (23.90% → 25.89%) |
| **Theta decay (Δt · Theta)** | `-$10.8339` | -9.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$22.6814` | -19.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$117.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$22.6814` (19.3% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$18.8562` | Volga PnL: `+$1.5111`
* Combined: `-$17.3451` | Residual after: `-$5.3363`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$10.8411`
* **spot**: `-$137.7518`
* **vol**: `+$31.0343`
* **rate**: `-$0.0654`
* Step sum: `-$117.6241` | Model ΔP: `-$117.5000` | Audit residual: `+$0.1241`

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
* Residual size leaves room for Taylor truncation and other path effects, so the model split should be treated as a reference view rather than a precise explanation.
* With no retrieved catalyst tape, do not layer in borrow, squeeze, or IV-crush language; the observed move is adequately explained by the spot drop and the option’s own convexity.

---

### Position 2 — `JPM 340P 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 340P 2026-12-18`  
**Analysis Date**: `2026-11-20` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$967.5000` (+46.3%)
* **Model ΔP**: `+$967.5000`
* **Primary drivers**: **Delta PnL** (+84.8%) and **Vega PnL** (+15.8%) and **Gamma PnL** (+6.7%).
* **Verdict**: The position’s gain was driven primarily by the put benefiting from the drop in JPM’s spot price, with gamma adding a smaller convexity boost and vega contributing additional support as implied volatility rose. The residual is modest and consistent with second-order effects and path-dependent revaluation rather than a separate catalyst; there were no relevant headlines to add a Layer B event story.
* **Confidence**: **Medium** — Confidence is medium because the blotter provides a clean factor decomposition with high attribution coverage and reliable observation, but the residual is not zero and the move includes a meaningful implied-volatility component. The engine flags no relevant headlines, so there is no independent catalyst to anchor beyond the modeled spot and vol reprice.

---

## 2. Observation Lock

* **As-of**: `2026-11-20` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 7.4%)
* **IV move**: +9.89 vol pts vs noise band ±6.50 pts (exceeds noise band)
* **Prior observation**: `2026-11-19`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$967.5000`
* **Model ΔP (engine)**: `+$967.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$1,031.8791`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$64.3791` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (6.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$820.2007` | +84.8% | Stock moved from $320.22 to $310.53 (-9.6900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$65.1623` | +6.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$152.8927` | +15.8% | IV moved +7.25 vol pts (20.45% → 27.70%) |
| **Theta decay (Δt · Theta)** | `-$6.3766` | -0.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$64.3791` | -6.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$967.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$64.3791` (6.7% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$84.0085` | Volga PnL: `+$28.9817`
* Combined: `-$55.0269` | Residual after: `-$9.3522`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$6.3614`
* **spot**: `+$879.7902`
* **vol**: `+$94.0819`
* **rate**: `+$0.3369`
* Step sum: `+$967.8476` | Model ΔP: `+$967.5000` | Audit residual: `-$0.3476`

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

* Higher-order convexity and full-engine revaluation can still leave a modest residual versus the Taylor bucket, especially with a sharp spot move.
* Monitor the implied-volatility repricing and any dividend or carry checks that could alter the American-style early-exercise assessment, even though the premium here is small.

---

### Position 3 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-20` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (+46.3%) and **Delta PnL** (-32.9%) and **Theta decay** (-10.8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is led by the volatility revaluation, with spot weakness and time decay offsetting part of the gain from higher implied volatility. Because the observation is unreliable and the Vega narrative is suppressed, this should be read as a model reprice rather than a firm market-tape conclusion. With no relevant headlines or named microstructure tags, there is no supported Layer B catalyst to add beyond the factor story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Low** — Confidence is low because the observation is not reliable, the attribution coverage is limited, and the residual is sizable relative to the model move. The Vega narrative is also explicitly suppressed, and there are no relevant headlines to independently confirm a catalyst.

---

## 2. Observation Lock

* **As-of**: `2026-11-20` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `unquoted`
* **IV move**: +71.87 vol pts vs noise band ±78.61 pts (inside noise band — **Vega story not falsifiable**)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-19`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000`
* **Explained ΔP (Taylor ex-residual)**: `+$0.0628`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0628` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — today's option quote tier is `unquoted`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.3288` | -32.9% | Stock moved from $1.03 to $0.96 (-0.0740) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0375` | +3.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.4625` | +46.3% | IV moved +16.98 vol pts (236.07% → 253.05%) |
| **Theta decay (Δt · Theta)** | `-$0.1083` | -10.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0628` | -6.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **-0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0628` (>1000% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$0.0902` | Volga PnL: `+$0.0577`
* Combined: `-$0.0325` | Residual after: `-$0.0304`

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
* The attribution can still be distorted by higher-order effects and full-surface repricing when the spot and vol moves are both material.
* No named catalyst, borrow, or squeeze signal is present in the blotter; verify whether later headlines or cleaner marks add a supported Layer B explanation.

---

## Settled at expiry

| Contract | Outcome | Settlement | PnL ($) |
| :--- | :--- | ---: | ---: |
| `AAPL 325C 2026-11-20` | exercised | 17.5600 | `-$696.5000` |
| `AAPL 350C 2026-11-20` | expired worthless | 0.0000 | `+$217.5000` |
| `SPY 715P 2026-11-20` | assigned | 25.1900 | `-$2,374.0000` |
| `SPY 795C 2026-11-20` | expired worthless | 0.0000 | `-$1.0000` |
| `VZ 45C 2026-11-20` | exercised | 1.4800 | `+$67.0000` |

### Settled — `AAPL 325C 2026-11-20`

`AAPL 325C 2026-11-20` expired at the 2026-11-20 close (spot 342.56) and settles at intrinsic value, 17.5600 per option. No model, vol or news search is involved.

Prior mark: 24.5250 on 2026-11-19 (spot 349.21).

| Component | Per option | Position ($) |
| :--- | ---: | ---: |
| Intrinsic change from spot | `-$6.6500` | `-$664.9991` |
| Time value released | `-$0.3150` | `-$31.5009` |
| **Settlement PnL** | `-$6.9650` | `-$696.5000` |

* Exercised: the position buys 100 shares at 325. This report does not track the resulting stock position.

### Settled — `AAPL 350C 2026-11-20`

`AAPL 350C 2026-11-20` expired at the 2026-11-20 close (spot 342.56) and settles at intrinsic value, 0.0000 per option. No model, vol or news search is involved.

Prior mark: 2.1750 on 2026-11-19 (spot 349.21).

| Component | Per option | Position ($) |
| :--- | ---: | ---: |
| Intrinsic change from spot | `+$0.0000` | `+$0.0000` |
| Time value released | `-$2.1750` | `+$217.5000` |
| **Settlement PnL** | `-$2.1750` | `+$217.5000` |

* Expires worthless: no exercise, no stock delivery.

### Settled — `SPY 715P 2026-11-20`

`SPY 715P 2026-11-20` expired at the 2026-11-20 close (spot 689.81) and settles at intrinsic value, 25.1900 per option. No model, vol or news search is involved.

Prior mark: 1.4500 on 2026-11-18 (spot 730.20).

| Component | Per option | Position ($) |
| :--- | ---: | ---: |
| Intrinsic change from spot | `+$25.1900` | `-$2,519.0000` |
| Time value released | `-$1.4500` | `+$145.0000` |
| **Settlement PnL** | `+$23.7400` | `-$2,374.0000` |

* Assigned: the position buys 100 shares at 715. This report does not track the resulting stock position.

### Settled — `SPY 795C 2026-11-20`

`SPY 795C 2026-11-20` expired at the 2026-11-20 close (spot 689.81) and settles at intrinsic value, 0.0000 per option. No model, vol or news search is involved.

Prior mark: 0.0100 on 2026-11-19 (spot 715.87).

| Component | Per option | Position ($) |
| :--- | ---: | ---: |
| Intrinsic change from spot | `+$0.0000` | `+$0.0000` |
| Time value released | `-$0.0100` | `-$1.0000` |
| **Settlement PnL** | `-$0.0100` | `-$1.0000` |

* Expires worthless: no exercise, no stock delivery.

### Settled — `VZ 45C 2026-11-20`

`VZ 45C 2026-11-20` expired at the 2026-11-20 close (spot 46.48) and settles at intrinsic value, 1.4800 per option. No model, vol or news search is involved.

Prior mark: 0.8100 on 2026-11-19 (spot 45.74).

| Component | Per option | Position ($) |
| :--- | ---: | ---: |
| Intrinsic change from spot | `+$0.7400` | `+$73.9998` |
| Time value released | `-$0.0700` | `-$6.9998` |
| **Settlement PnL** | `+$0.6700` | `+$67.0000` |

* Exercised: the position buys 100 shares at 45. This report does not track the resulting stock position.


## Rolls

- **aapl_vertical_long**: `AAPL 325C 2026-11-20` settled at the 2026-11-20 close. Rolled into `AAPL 335C 2027-01-15` at the 2026-11-20 close (spot 342.56, mark 21.3750); its PnL starts with the next run.
- **aapl_vertical_short**: `AAPL 350C 2026-11-20` settled at the 2026-11-20 close. Rolled into `AAPL 360C 2027-01-15` at the 2026-11-20 close (spot 342.56, mark 7.8750); its PnL starts with the next run.
- **spy_reversal_put**: `SPY 715P 2026-11-20` settled at the 2026-11-20 close. Rolled into `SPY 655P 2027-01-15` at the 2026-11-20 close (spot 689.81, mark 16.1650); its PnL starts with the next run.
- **spy_reversal_call**: `SPY 795C 2026-11-20` settled at the 2026-11-20 close. Rolled into `SPY 725C 2027-01-15` at the 2026-11-20 close (spot 689.81, mark 13.3650); its PnL starts with the next run.
- **vz_div_call**: `VZ 45C 2026-11-20` settled at the 2026-11-20 close. Rolled into `VZ 42C 2027-01-15` at the 2026-11-20 close (spot 46.48, mark 5.0500); its PnL starts with the next run.
