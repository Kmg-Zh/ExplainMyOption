# Live book run — 2026-11-04

Run `2026-11-04-1793844903`. 6/8 legs completed, 2 failed. `legs_narrated=6` `legs_silent=0` `llm_calls=11`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-11-04` | **Positions**: 6 | **Tickers**: AAPL, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$1,127.0000`
* **Total Model PnL**: `-$629.7290`
* **Aggregate model vs mark gap**: `-$1,756.7290`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `AAPL 350C 2026-11-20` | `-$542.5000` |
| 2 | `AAPL 325C 2026-11-20` | `-$364.2291` |
| 3 | `SPY 715P 2026-11-20` | `+$196.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$297.5388` |
| Gamma | `-$14.3314` |
| Vega | `-$289.4507` |
| Theta | `+$3.2168` |
| Residual | `-$31.6249` |

### Notable underlyings

* **AAPL**: `-$906.7290` aggregate option PnL
* **SPY**: `+$219.5000` aggregate option PnL
* **VZ**: `+$55.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-11-04` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$1,392.5000` (-21.5%)
* **Model ΔP**: `-$364.2291`
* **Primary drivers**: **Delta PnL** (-132.4%) and **Vega PnL** (+27.3%).
* **Verdict**: The position was driven first by the underlying dropping, which hit the long call through delta and was partially offset by gamma and vega. However, the attribution does not fully explain the move: there is a terminal unexplained break, so this needs human review rather than a single-factor story. With no relevant headline catalysts retrieved, there is no supported Layer B mechanism to add beyond the model revaluation.
* **Confidence**: **Medium** — Confidence is only medium because the dominant driver is clear, but the run flags a terminal unexplained break and the residual is not fully resolved by the Taylor view. News context is absent, so there is no independent catalyst to validate or refine the attribution.

---

## 2. Observation Lock

* **As-of**: `2026-11-04` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.1%)
* **IV move**: +4.30 vol pts vs noise band ±2.01 pts (exceeds noise band)
* **Prior observation**: `2026-11-03`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$1,392.5000`
* **Model ΔP (engine)**: `-$364.2291`
* **Model vs Mark gap**: `-$1,756.7291` (+482.3% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$375.6283`

* **Method residual (ε_method)**: `+$11.3993` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$1,756.7291` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (3.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$482.3910` | -132.4% | Stock moved from $338.32 to $331.90 (-6.4200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$30.2991` | +8.3% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$99.3769` | +27.3% | IV moved +4.30 vol pts (29.53% → 33.83%) |
| **Theta decay (Δt · Theta)** | `-$22.9133` | -6.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$11.3993` | +3.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$364.2291** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$11.3993` (3.1% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap; the factor story is not reliable and needs human review.

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$18.8491` | other second-order: `+$3.0297`
* Combined: `+$21.8788` | Residual after: `-$10.4796`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$22.9161`
* **spot**: `-$452.7286`
* **vol**: `+$111.4156`
* Step sum: `-$364.2291` | Model ΔP: `-$364.2291` | Audit residual: `+$0.0000`

### Ex-div attribution overlay (official PnL stays the American FDM Taylor blotter)
* **Spot drop vs dividend** (per share): spot `-$6.4200` vs next cash dividend `+$0.2700` (gap `-$6.1500`)
* **American FDM vs European analytic (no cash div, cross-check, per option)**: `+$13.3136` vs `+$13.4507` (gap `-$0.1371`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored, per option): `+$0.0000` — not material
* **Dividend PV effect** (European, same divs − no divs, per option): `-$0.1375`
* **Dividend coverage** (dividend / time value): `0.04` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `+$99.3769`
* **Residual (Taylor ε)**: `+$11.3993`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%
  * `american_dividend_exercise_check` — path_reprice outranks ex-div window
* **Playbook records** (selected by code for the narrator): `terminal-break` (`terminal_unexplained_break`)

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* Check whether the full reprice, truncation, or quote/mark effects are distorting the reference Greek attribution.
* Because no relevant headlines were retrieved, do not infer borrow, squeeze, or implied-volatility mechanisms from background tape; human review is needed for the unexplained gap.
* **Assignment watch**: ex-div `2026-11-12` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-11-04` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$542.5000` (+361.7%)
* **Model ΔP**: `-$542.5000`
* **Primary drivers**: **Vega PnL** (-120.0%) and **Delta PnL** (+24.3%) and **Gamma PnL** (-8.2%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The revaluation is dominated by the sharp jump in implied volatility, which overwhelms the smaller spot decline and explains most of the modeled option loss. The Taylor residual is small, so the Greek decomposition is behaving cleanly; with observation locked and no relevant headlines retrieved, there is no separate catalyst layer to add beyond the volatility shock itself. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is tempered because the observation flag is false and the system suppresses a Vega narrative, so the data quality is not strong enough for a more granular catalyst claim. Even so, the model, factor shares, and low residual all point to volatility as the main driver, and there are no relevant headlines to support an alternative mechanism.

---

## 2. Observation Lock

* **As-of**: `2026-11-04` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 5.1%)
* **IV move**: +0.24 vol pts vs noise band ±0.70 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-03`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$542.5000`
* **Model ΔP (engine)**: `-$542.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$551.4532`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$8.9532` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$132.0263` | +24.3% | Stock moved from $338.32 to $331.90 (-6.4200) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$44.4172` | -8.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$650.8966` | -120.0% | IV moved +31.33 vol pts (18.10% → 49.42%) |
| **Theta decay (Δt · Theta)** | `+$11.8344` | +2.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$8.9532` | +1.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$542.5000** | **-100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$8.9532` (1.7% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$150.3528` | Volga PnL: `-$180.9655`
* Combined: `-$30.6127` | Residual after: `+$39.5659`

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
* Check whether the revaluation remains stable under a full-surface repricing, since spot and vol both moved and the residual is small.
* Watch for any subsequent change in implied volatility or quote quality; no borrow, squeeze, or event headline context was retrieved here.
* **Assignment watch**: ex-div `2026-11-12` — Dividend coverage 0.04 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-11-04` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$196.5000` (-68.7%)
* **Model ΔP**: `+$196.5000`
* **Primary drivers**: **Vega PnL** (+98.5%) and **Delta PnL** (+16.6%) and **Theta decay** (+12.4%).
* **Verdict**: The modeled move was led by a sharp drop in implied volatility, with spot contributing only a secondary effect and theta helping offset part of the decay. The residual is consistent with higher-order effects around the volatility move and a market-wide IV crush backdrop rather than a clean single-factor reprice. The relevant market-structure headline context supports the iv crush mechanism, while the broad market overview item is only background.
* **Confidence**: **Medium** — Observation quality is good and the attribution coverage is strong, but the residual is still material and the news set is sparse. The available relevant headline is market-mechanism context rather than an issuer-specific catalyst, so the Layer B explanation is supportive rather than definitive.

---

## 2. Observation Lock

* **As-of**: `2026-11-04` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.1%)
* **IV move**: -2.09 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-11-03`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$196.5000`
* **Model ΔP (engine)**: `+$196.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$248.9713`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$52.4713` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (26.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$32.5330` | +16.6% | Stock moved from $752.10 to $754.35 (+2.2500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$1.5297` | -0.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$193.6057` | +98.5% | IV moved -5.25 vol pts (23.24% → 17.99%) |
| **Theta decay (Δt · Theta)** | `+$24.3623` | +12.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$52.4713` | -26.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$196.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$52.4713` (26.7% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `-$11.0495` | Volga PnL: `-$22.3732`
* Combined: `-$33.4227` | Residual after: `-$19.0487`

### Sequential full revaluation (t → S → σ → r)
* **time**: `+$24.3612`
* **spot**: `+$29.5509`
* **vol**: `+$142.5878`
* Step sum: `+$196.5000` | Model ΔP: `+$196.5000` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction**._

_Intel note: Only one headline is relevant to SPY, and it is a market-structure background item rather than a company-specific event. The other headlines are general education or unrelated META earnings content._
_Intel triage discarded 2 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Implied Volatility Explained for Options Traders | Vanquish**

_Peer / sector background (indirect context, not a required catalyst):_

2. **Today's SPY, QQQ & VIX Gamma, Dealer Positioning & Regime | FlashAlpha**

---

## 7. Risk Watchlist

* Monitor whether the residual stays elevated on a full-surface reprice, since higher-order convexity and truncation can still distort the reference Greek explanation.
* Watch for continued iv crush and broader implied-volatility regime shifts, because that mechanism is already present in the tape and in the relevant headline context.

---

### Position 4 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-11-04` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$23.0000` (+54.1%)
* **Model ΔP**: `+$23.0000`
* **Primary drivers**: **Vega PnL** (+74.2%) and **Delta PnL** (+43.3%) and **Theta decay** (-28.5%).
* **Verdict**: The modeled move was led by vega, with spot making only a modest contribution and theta partly offsetting the gain. The remaining gap is consistent with higher-order effects rather than a clean one-factor tape, and the relevant headline context supports an implied-volatility / iv crush framing even though the available SPY-specific headline is market-structure oriented rather than a direct event catalyst.
* **Confidence**: **Medium** — The attribution is supported by high coverage and a reliable observation, but the residual is not trivial and the news set is limited. The Layer B mechanism is present in the digest and should be named, yet the headlines are generic, so the catalyst story is supportive rather than definitive.

---

## 2. Observation Lock

* **As-of**: `2026-11-04` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 4.6%)
* **IV move**: -2.29 vol pts vs noise band ±0.08 pts (exceeds noise band)
* **Prior observation**: `2026-11-03`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$23.0000`
* **Model ΔP (engine)**: `+$23.0000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$21.4705`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.5295` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (6.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$9.9688` | +43.3% | Stock moved from $752.10 to $754.35 (+2.2500) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1.0012` | +4.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$17.0661` | +74.2% | IV moved +1.12 vol pts (14.58% → 15.70%) |
| **Theta decay (Δt · Theta)** | `-$6.5657` | -28.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.5295` | +6.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$23.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.5295` (6.6% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$3.3170` | Volga PnL: `+$1.9359`
* Combined: `+$5.2528` | Residual after: `-$3.7233`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$6.5637`
* **spot**: `+$9.8344`
* **vol**: `+$19.7292`
* Step sum: `+$23.0000` | Model ΔP: `+$23.0000` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction / implied-volatility repricing**._

_Intel note: Only one headline is directly SPY-related, and it is a market/positioning overview rather than a company-specific catalyst. The remaining items are generic education or unrelated issuer coverage._
_Intel triage discarded 2 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Implied Volatility Explained for Options Traders | Vanquish**

_Peer / sector background (indirect context, not a required catalyst):_

2. **Today's SPY, QQQ & VIX Gamma, Dealer Positioning & Regime | FlashAlpha**
3. **META Stock Before Earnings: Why Calls Lose on a ±7.0% Move**

---

## 7. Risk Watchlist

* Watch whether the residual stays elevated, since higher-order convexity and full-surface repricing can leave a Taylor-style decomposition incomplete.
* Monitor the implied-volatility / iv crush backdrop and dealer positioning context for confirmation that the vol repricing, not spot alone, is driving the option mark.

---

### Position 5 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-11-04` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$55.5000` (+46.6%)
* **Model ΔP**: `+$55.5000`
* **Primary drivers**: **Vega PnL** (+90.8%) and **Delta PnL** (+17.6%) and **Theta decay** (-6.1%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is dominated by the option’s sensitivity to the sharp rise in implied volatility, with spot only a secondary contributor and theta a modest drag. The small residual is consistent with ordinary truncation and quote/curve effects in a reference attribution, while the American early-exercise premium remains negligible and does not change the story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — The model attribution is clear, but observation reliability is flagged as weak and the run suppresses a Vega narrative, so the diagnosis should stay at a coarse level. There are no retrieved headlines or named microstructure mechanisms, and the residual is small, which limits the need for a more elaborate catalyst story.

---

## 2. Observation Lock

* **As-of**: `2026-11-04` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 9.7%)
* **IV move**: +0.78 vol pts vs noise band ±2.27 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-03`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$55.5000`
* **Model ΔP (engine)**: `+$55.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$56.9824`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.4824` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$9.7640` | +17.6% | Stock moved from $45.05 to $45.24 (+0.1900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.2422` | +0.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$50.3808` | +90.8% | IV moved +13.04 vol pts (30.66% → 43.70%) |
| **Theta decay (Δt · Theta)** | `-$3.4047` | -6.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.4824` | -2.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$55.5000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.4824` (2.7% of |model|)

### Second-order Taylor (vanna, volga)
* other second-order: `-$0.1706`
* Combined: `-$0.1706` | Residual after: `-$1.3118`

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
* Check whether the model’s residual stays small if the full surface is re-checked, since higher-order effects can still modestly distort the attribution.
* Verify any quote or surface discontinuity around the volatility move, because the run relies on a reference view rather than a fully stable observation set.

---

### Position 6 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-11-04` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$2.0000` (+133.3%)
* **Model ΔP**: `+$2.0000`
* **Primary drivers**: **Vega PnL** (+50.8%) and **Delta PnL** (+28.0%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model reprice was driven mainly by the spot move, with convexity helping as the underlying rose into a higher-volatility tape. The vega line is present in the blotter, but the observation lock and suppressed vega narrative mean the safe read is that the full revaluation was led by spot-related repricing rather than a clean implied-volatility story. There are no named catalyst headlines to layer in, and the residual is consistent with higher-order effects and path dependence rather than a separate event-driven explanation. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is only medium confidence because observation reliability is flagged false, the residual share is elevated, and the data package explicitly suppresses a Vega narrative despite vega being the largest modeled bucket. The absence of retrieved headlines also means there is no independent Layer B mechanism to anchor beyond the blotter.

---

## 2. Observation Lock

* **As-of**: `2026-11-04` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 142.9%)
* **IV move**: +23.44 vol pts vs noise band ±28.61 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-11-03`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$2.0000`
* **Model ΔP (engine)**: `+$2.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$1.5532`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.4468` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (22.3%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$0.5600` | +28.0% | Stock moved from $1.31 to $1.41 (+0.1000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0730` | +3.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$1.0163` | +50.8% | IV moved +19.58 vol pts (167.98% → 187.56%) |
| **Theta decay (Δt · Theta)** | `-$0.0962` | -4.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.4468` | +22.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$2.0000** | **+100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.4468` (22.3% of |model|)

### Second-order Taylor (vanna, volga)
* Vanna PnL: `+$0.2637` | Volga PnL: `+$0.1990`
* Combined: `+$0.4627` | Residual after: `-$0.0159`

### Sequential full revaluation (t → S → σ → r)
* **time**: `-$0.0961`
* **spot**: `+$0.6067`
* **vol**: `+$1.4894`
* Step sum: `+$2.0000` | Model ΔP: `+$2.0000` | Audit residual: `+$0.0000`

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
* Watch whether the full-surface repricer continues to differ from the Taylor buckets, since higher-order curvature and truncation are already material.
* With no relevant headlines retrieved, there is no borrow, squeeze, or IV-crush mechanism to verify from tape context; keep the focus on the model revaluation and quote quality.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0967 | level_proxy(t) = 0.1687
* Δskew = +0.0020 | Δlevel = -0.0219
* Put 715 delta=-0.0702 | Call 795 delta=0.0618
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.


## Errors

- **jpm_straddle_call** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-11, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
- **jpm_straddle_put** (JPM): RuntimeError: Expiration `2026-10-23` cannot be found. Available expirations are: [2026-11-06, 2026-11-13, 2026-11-20, 2026-11-27, 2026-12-04, 2026-12-11, 2026-12-18, 2027-01-15, 2027-03-19, 2027-06-17, 2027-09-17, 2027-12-17, 2028-01-21, 2028-12-15, 2029-01-19]
