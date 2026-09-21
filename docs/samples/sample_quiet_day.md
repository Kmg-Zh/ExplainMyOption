# Option Price Movement Diagnostic Report

**Contract**: `AAPL 165C 2023-05-19`  
**Analysis Date**: `2023-04-24` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0250` (+0.5%)
* **Model ΔP**: `+$0.0250`
* **Primary drivers**: **Theta decay** (46%) and **Vega PnL** (26%) and **Delta PnL** (26%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2023-04-24` | **Data**: `historical` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 3.0%)
* **IV move**: +1.46 vol pts vs noise band ±0.44 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2023-04-21`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0250`
* **Model ΔP (engine)**: `+$0.0250`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0398`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0148` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `model` (0.0%)

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.1641` | +25.8% | Stock moved from $165.02 to $165.33 (+0.3100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0016` | +0.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.1644` | +25.9% | IV moved +0.90 vol pts (25.35% → 26.81%) |
| **Theta decay (Δt · Theta)** | `-$0.2903` | +45.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0148` | +2.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0250** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0148` (59.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0003`
* Combined: `-$0.0003` | Residual after: `+$0.0253`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2959`
* **spot**: `+$0.1651`
* **vol**: `+$0.1554`
* **rate**: `-$0.0041`
* Step sum: `+$0.0205` | Model ΔP: `+$0.0250` | Audit residual: `+$0.0045`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$0.3100` vs next cash dividend `+$0.2400` (gap `+$0.5500`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$4.9750` vs `+$4.9973` (gap `-$0.0223`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0078` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.0310`
* **Dividend coverage** (dividend / time value): `0.05` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$0.1644`
* **Residual (Taylor ε)**: `-$0.0148`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_Observation unreliable — event linkage suppressed; reconcile marks before catalyst stories._


---

## 7. Risk Watchlist

* No action needed; move is within theta/carry tolerance.
* **Assignment watch**: ex-div `2023-05-12` — Dividend coverage 0.05 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.
