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
* **Verdict**: The option move was dominated by the underlying’s downside spot gap, with the prior delta on the call doing most of the work. Gamma and theta helped shape the move, while the small residual is consistent with ordinary Taylor truncation rather than a distinct missing mechanism. The news flow is only sector-level background and does not supply a company-specific catalyst or a borrow/squeeze/IV-crush regime.
* **Confidence**: **Medium** — Confidence is medium because the attribution is cleanly concentrated in the modeled delta line, but the market feed is incomplete for a fuller catalyst read and the residual break is flagged for watchlist escalation. The relevant headlines are broad tech/chip context only, while the IV input was proxied from a historical source and the catalyst critic found no required Layer B mechanism.

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

_Intel note: The feed contains two sector-level tech/chip items that are background for Nvidia and one unrelated personal-finance article. No headline directly names Nvidia or a company-specific control, earnings, or borrow/squeeze event._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **Tech pulls back on AI concerns, cybersecurity takes a step up** _(Source: Yahoo Finance Video)_
2. **Chip stocks fall as oil prices gain, Treasury yields stay elevated: AlphaCheck** _(Source: Yahoo Finance)_
3. **Retirement Benchmark Revealed: Is Your 401(k) Balance Ahead of the Curve at 60?** _(Source: Motley Fool)_

---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* Reconcile the position with a spot-led full-surface reprice and keep the hedge aligned to the underlying move; the small residual is consistent with truncation, not a separate driver.
* Use the sector tape only as context; there is no supported NVDA-specific borrow, squeeze, or IV-crush narrative in the headlines.
