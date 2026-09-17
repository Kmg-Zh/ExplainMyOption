# Option Price Movement Diagnostic Report

**Contract**: `AAPL 180C 2023-11-24`  
**Analysis Date**: `2023-11-09` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$0.1500` (-3.4%)
* **Model ΔP**: `-$0.1500`
* **Primary drivers**: **Delta PnL** (47%) and **Vega PnL** (38%) and **Theta decay** (13%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2023-11-09` | **Data**: `historical` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 5.8%)
* **IV move**: -0.13 vol pts vs noise band ±0.91 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2023-11-08`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$0.1500`
* **Model ΔP (engine)**: `-$0.1500`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$0.1492`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0008` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `model` (0.0%)

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.3297` | +47.5% | Stock moved from $182.89 to $182.41 (-0.4800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0062` | +0.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.2661` | +38.3% | IV moved +1.96 vol pts (19.70% → 19.57%) |
| **Theta decay (Δt · Theta)** | `-$0.0918` | +13.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0008` | +0.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.1500** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0008` (0.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0103`
* Combined: `+$0.0103` | Residual after: `-$0.1603`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$0.4800` vs next cash dividend `+$0.2400` (gap `-$0.2400`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$4.2750` vs `+$4.2268` (gap `+$0.0482`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs): `+$0.0474`
* **Dividend coverage** (dividend / time value): `0.13` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.2661`
* **Residual (Taylor ε)**: `-$0.0008`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (0/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_Observation unreliable — event linkage suppressed; reconcile marks before catalyst stories._


---

## 7. Trading Desk Watchlist

* No action needed; move is within theta/carry tolerance.
* **Assignment watch**: ex-div `2023-11-10` — Dividend coverage 0.13 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.
