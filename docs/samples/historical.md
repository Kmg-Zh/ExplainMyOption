<!-- Frozen public sample captured 2026-09-14. Suite output/ stays gitignored. -->

_Historical fixture `meta_earnings_gap` with frozen as-of headlines (`published <= 2022-02-03`). Product graph, captured 2026-09-14._

# Option Price Movement Diagnostic Report

**Contract**: `META 320C 2022-03-18`  
**Analysis Date**: `2022-02-03` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Model PnL (no mark)**: `-$25.1782` (-99.7%)
* **Model ΔP**: `-$25.1782`
* **Primary drivers**: **Delta PnL** (54%) and **Gamma PnL** (26%) and **Vega PnL** (11%).
* **Verdict**: The blotter’s modeled driver is a sharp spot move, with delta doing the heavy lifting and gamma partially offsetting the swing while vega also adds downside pressure. The residual is consistent with higher-order truncation around an extreme move, and the news backdrop points to a post-earnings repricing with IV crush that helps explain the gap in addition to the Taylor buckets.
* **Confidence**: **Medium** — Confidence is medium because the dominant Greek attribution is clear, but the residual is sizable and the move occurred alongside an earnings catalyst and implied volatility compression. That combination supports the driver story while leaving some unmodeled convexity and surface effects in the gap.

---

## 2. Observation Lock

* **As-of**: `2022-02-03` | **Data**: `synthetic` | **IV prev**: `fixture`
* **Observation lock**: no live quote tier — model-only path.

---

## 3. Mark Reconciliation

* **Model ΔP (engine)**: `-$25.1782`
* **Mark ΔP**: unavailable — no valid marks on both dates.
* **Explained ΔP (Taylor ex-residual)**: `-$32.4947`

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$45.3927` | +180.3% | Stock moved from $320.19 to $237.76 (-82.4300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$21.9945` | -87.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$8.8012` | +35.0% | IV moved -20.00 vol pts (55.00% → 35.00%) |
| **Theta decay (Δt · Theta)** | `-$0.2952` | +1.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$7.3165` | -29.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$25.1782** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$7.3165` (29.1% of |model|)

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2953`
* **spot**: `-$23.5989`
* **vol**: `-$1.2840`
* Step sum: `-$25.1782` | Model ΔP: `-$25.1782` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (1/3): `path_reprice`
* **Skipped candidates**:
  * `taylor_second_order` — path_reprice selected for severity >20%
  * `compare_to_official` — path_reprice selected for severity >20%

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Intel note: The headlines are both Meta-specific and centered on the company’s earnings release. One highlights weak guidance and user decline, while the other notes elevated options volume and post-earnings implied volatility compression._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Meta options volume surged as implied volatility collapsed after earnings** _(Source: Reuters)_

_Peer / sector background (indirect context, not a required catalyst):_

2. **Meta shares plunged about 26% after weak revenue guidance and the first quarterly decline in daily active users** _(Source: CNBC)_

---

## 7. Trading Desk Watchlist

* Reprice on the full surface and treat the residual as higher-order convexity around an extreme gap, then reassess hedge balance after the spot shock.
* Keep the post-earnings IV crush in the tape read: the headline catalyst supports the volatility reset that compounded the downside in the call.
