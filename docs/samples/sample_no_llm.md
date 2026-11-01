# Option Price Movement Diagnostic Report

**Contract**: `AAPL 345C 2026-10-23`  
**Analysis Date**: `2026-10-15` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Delta PnL** (+44.6%) and **Vega PnL** (-38.1%) and **Theta decay** (-11.9%).
* **Verdict**: The position lost value over the session; the largest attributed component is Delta / spot move. Residual and American effects are flagged when Taylor coverage is below desk thresholds.
* **Confidence**: **Medium** — No OPENAI_API_KEY — narrative is rule-based; all dollar amounts are in the quant tables only.

---

## 2. Observation Lock

* **As-of**: `2026-10-15` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `reliable` (spread/mid 7.7%)
* **IV move**: -0.36 vol pts vs noise band ±1.11 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-14`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$0.0604`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0604` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (>1000%)
  Escalation basis: method residual — prior-day vol is a `hv20_proxy` stand-in, not a chain mark, so the market-vs-model gap cannot be measured; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$1.4758` | +44.6% | Stock moved from $342.96 to $346.11 (+3.1500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1186` | +3.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$1.2611` | -38.1% | IV moved -5.89 vol pts (30.88% → 24.99%) |
| **Theta decay (Δt · Theta)** | `-$0.3938` | -11.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0604` | +1.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **-0.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0604` (>1000% of |model|)
* _No deep diagnostic tools ran — residual may reflect truncation, American effects, or data gaps._

---

## 6. Root-Cause Market Intelligence

_Observation unreliable — event linkage suppressed; reconcile marks before catalyst stories._


---

## 7. Risk Watchlist

* **Quote quality**: IV move sits inside the bid-ask noise band — do not treat Vega as a falsifiable driver from this quote alone.
* **Elevated residual**: Likely contributors are the American early-exercise boundary, discrete dividends, vol skew curvature, and mark quality. Model limitations flagged above (the residual size is in the quantitative sections; prose carries no figures).
