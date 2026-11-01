# Option Price Movement Diagnostic Report

**Contract**: `GME 55P 2021-02-19`  
**Analysis Date**: `2021-01-25` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$1.6000` (+12.1%)
* **Model ΔP**: `+$1.6000`
* **Primary drivers**: **Vega PnL** (+52.9%) and **Delta PnL** (-31.1%) and **Theta decay** (-8.7%).
* **Verifier**: FAIL — hard policy violation (prohibited_phrase); the factor story is not reliable. Trade-advice-adjacent language (arbitrage/mispricing/opportunity/riskless/cheap/rich/'should have') is out of scope regardless of context -- this product explains a price move, it does not advise a trade.
* **Verdict**: Verifier FAIL — terminal break escalation (prohibited_phrase). Trade-advice-adjacent language (arbitrage/mispricing/opportunity/riskless/cheap/rich/'should have') is out of scope regardless of context -- this product explains a price move, it does not advise a trade.
* **Confidence**: **Medium** — Vega dominated the Taylor decomposition.

---

## 2. Observation Lock

* **As-of**: `2021-01-25` | **Data**: `historical` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 8.4%)
* **IV move**: +50.08 vol pts vs noise band ±11.02 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2021-01-22`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$1.6000`
* **Model ΔP (engine)**: `+$1.6000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$1.8948`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.2948` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `model` (0.0%)

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (the components largely offset, so % Share is of the gross movement Σ|component|):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$3.3487` | -31.1% | Stock moved from $65.01 to $76.79 (+11.7800) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.4858` | +4.5% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$5.6937` | +52.9% | IV moved +95.50 vol pts (262.72% → 358.21%) |
| **Theta decay (Δt · Theta)** | `-$0.9358` | -8.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.2948` | -2.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$1.6000** | **+14.9%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.2948` (18.4% of |model|)
* **Terminal break**: the verifier's hard failure was confirmed by code (see Headline); the narrative is not reliable and needs human review.

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.3282` | Volga PnL: `-$0.1404`
* Combined: `+$0.1878` | Residual after: `-$0.4827`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.9542`
* **spot**: `-$2.9116`
* **vol**: `+$5.4658`
* Step sum: `+$1.6000` | Model ΔP: `+$1.6000` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* Verifier flags: prohibited_phrase; missing evidence: Prohibited trade-advice phrase: cheap
* Reprice on the full surface.
