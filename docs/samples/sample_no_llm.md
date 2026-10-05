# Option Price Movement Diagnostic Report

**Contract**: `AAPL 332.5C 2026-10-12`  
**Analysis Date**: `2026-10-05` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Delta PnL** (46%) and **Theta decay** (35%) and **Vega PnL** (14%).
* **Verdict**: The position lost value over the session; the largest attributed component is Delta / spot move. Residual and American effects are flagged when Taylor coverage is below desk thresholds.
* **Confidence**: **Low** — No OPENAI_API_KEY — narrative is rule-based; all dollar amounts are in the quant tables only.

---

## 2. Observation Lock

* **As-of**: `2026-10-05` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `unquoted`
* **IV move**: +0.01 vol pts vs noise band ±0.00 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-01`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0283`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0283` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — prior-day vol is a `hv20_proxy` stand-in, not a chain mark, so the market-vs-model gap cannot be measured; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$1.5609` | +45.8% | Stock moved from $330.32 to $333.69 (+3.3700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1447` | +4.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.4665` | +13.7% | IV moved -2.05 vol pts (29.99% → 30.00%) |
| **Theta decay (Δt · Theta)** | `-$1.2108` | +35.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0283` | +0.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0283` (>1000% of |model|)
* _No deep diagnostic tools ran — residual may reflect truncation, American effects, or data gaps._

---

## 6. Root-Cause Market Intelligence

_Observation unreliable — event linkage suppressed; reconcile marks before catalyst stories._


---

## 7. Risk Watchlist

* **Elevated residual (>361291271%)**: Likely contributors are the American early-exercise boundary, discrete dividends, vol skew curvature, and mark quality. Model limitations flagged above.
