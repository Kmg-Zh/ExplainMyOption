# Option Price Movement Diagnostic Report

**Contract**: `AAPL 332.5C 2026-09-25`  
**Analysis Date**: `2026-09-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Theta decay** (47%) and **Delta PnL** (39%) and **Vega PnL** (9%).
* **Verdict**: The position gained value over the session; the largest attributed component is Theta / time decay. Residual and American effects are flagged when Taylor coverage is below desk thresholds.
* **Confidence**: **Low** — No OPENAI_API_KEY — narrative is rule-based; all dollar amounts are in the quant tables only.

---

## 2. Observation Lock

* **As-of**: `2026-09-17` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `unquoted`
* **IV move**: -0.32 vol pts vs noise band ±0.00 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000`
* **Explained ΔP (Taylor ex-residual)**: `+$0.0339`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0339` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (6582029380.9%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-15 and/or 2026-09-17, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.5200` | +39.4% | Stock moved from $331.34 to $332.41 (+1.0700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0157` | +1.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.1235` | +9.4% | IV moved +0.56 vol pts (0.42% → 0.10%) |
| **Theta decay (Δt · Theta)** | `-$0.6254` | +47.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0339` | +2.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0339` (6582029380.9% of |model|)
* _No deep diagnostic tools ran — residual may reflect truncation, American effects, or data gaps._

---

## 6. Root-Cause Market Intelligence

_Observation unreliable — event linkage suppressed; reconcile marks before catalyst stories._


---

## 7. Trading Desk Watchlist

* **Elevated residual (>6582029381%)**: Review American early-exercise boundary, discrete dividends, vol skew curvature, and mark quality. Model limitations flagged above.
