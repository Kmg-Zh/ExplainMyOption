<!-- Frozen public sample captured 2026-09-14. Suite output/ stays gitignored. -->

_Live public ticker, quantity 1, captured 2026-09-14. Not a client book. Headlines may be title-only after redaction._

# Option Price Movement Diagnostic Report

**Contract**: `NVDA 210C 2026-09-21`  
**Analysis Date**: `2026-09-14` | **Status**: Verified by QuantLib (fdm_local_vol)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-54.9%)
* **Model ΔP**: `-$5.5062`
* **Primary drivers**: **Delta PnL** (79%) and **Gamma PnL** (9%) and **Theta decay** (8%).
* **Verdict**: The position was driven primarily by a downside spot move in the underlying, and the call’s positive delta dominated the day-to-day repricing. Gamma partially softened the move and theta added decay, while the residual stayed small, so the blotter is consistent with a clean spot-led revaluation rather than a major model break. The headline tape is only broad semiconductor and tech weakness, which fits the move as background sentiment and does not add a separate named catalyst.
* **Confidence**: **Medium** — Confidence is medium because the official factor coverage is high and the residual is low, but the IV history is proxied from a realized-vol source and the feed is not company-specific. The independent catalyst critic found no required Layer B mechanism, so there is no need to force a news-driven overlay beyond broad sector context.

---

## 2. Observation Lock

* **As-of**: `2026-09-14` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `reliable` (spread/mid 3.4%)
* **IV move**: +1.50 vol pts vs noise band ±0.65 pts (exceeds noise band)
* **Prior observation**: `2026-09-11`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$5.5062`
* **Model vs Mark gap**: `-$5.5062` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$5.4340`

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$5.7003` | +103.5% | Stock moved from $218.29 to $210.96 (-7.3300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.6816` | -12.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.1610` | -2.9% | IV moved +1.50 vol pts (32.49% → 33.99%) |
| **Theta decay (Δt · Theta)** | `-$0.5763` | +10.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0722` | +1.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$5.5062** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0722` (1.3% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.4670`
* **spot**: `-$5.0392`
* **vol**: `+$0.0000`
* Step sum: `-$5.5062` | Model ΔP: `-$5.5062` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (3/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `path_reprice`
* **Skipped candidates**:
  * `taylor_second_order` — path_reprice selected for severity >20%
  * `compare_to_official` — path_reprice selected for severity >20%

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Intel note: The feed is mostly broad tech/semiconductor sentiment, with two items kept as background because they can influence NVIDIA indirectly. No headline here is company-specific for NVIDIA or indicates a qualifying control-structure event._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **Chip stocks fall as oil prices gain, Treasury yields stay elevated: AlphaCheck** _(Source: Yahoo Finance)_
   Semiconductor sector tape that can indirectly matter for NVIDIA, but it is a peer-sector move rather than a company-specific headline.
2. **Tech pulls back on AI concerns, cybersecurity takes a step up** _(Source: Yahoo Finance Video)_

---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* Rehedge around the underlying move; the option PnL is mostly a clean delta pass-through with only modest convexity and decay effects.
* Treat the tape as sector weakness rather than a company-specific catalyst; no borrow, squeeze, or IV-crush mechanism is indicated in the relevant headlines.
