# Live book run — 2026-09-21

Run `2026-09-21-1790039706`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=12`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-09-21` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$556.0000`
* **Total Model PnL**: `+$556.0000`
* **Aggregate model vs mark gap**: `+$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `SPY 795C 2026-11-20` | `+$374.5000` |
| 2 | `AAPL 325C 2026-11-20` | `+$215.0000` |
| 3 | `JPM 350P 2026-10-23` | `-$185.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$82.3680` |
| Gamma | `+$0.5442` |
| Vega | `+$735.9377` |
| Theta | `-$98.9574` |
| Residual | `+$0.8435` |

### Notable underlyings

* **SPY**: `+$501.0000` aggregate option PnL
* **AAPL**: `+$97.5000` aggregate option PnL
* **JPM**: `-$22.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-09-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$215.0000` (+986.2%)
* **Model ΔP**: `+$215.0000`
* **Primary drivers**: **Vega PnL** (76%) and **Delta PnL** (14%) and **Theta decay** (9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model reprice is led by the volatility update in the official Taylor view, with the spot drift and theta decay acting as smaller offsets. The residual is minimal, so the close-to-close move is well explained by the quant engine’s decomposition rather than by a separate gap story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is moderated by the observation lock and the fact that the vega narrative is suppressed by the run metadata, so the diagnosis should stay coarse even though the model attribution is clean. There are no relevant headlines or microstructure mechanisms to support a separate catalyst explanation, and the residual is low.

---

## 2. Observation Lock

* **As-of**: `2026-09-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.5%)
* **IV move**: +0.29 vol pts vs noise band ±0.59 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$215.0000`
* **Model ΔP (engine)**: `+$215.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$216.4900`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$1.4900` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$58.8659` | -27.4% | Stock moved from $337.00 to $336.13 (-0.8700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.3873` | +0.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$311.8568` | +145.0% | IV moved +6.20 vol pts (30.12% → 30.40%) |
| **Theta decay (Δt · Theta)** | `-$36.8882` | -17.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$1.4900` | -0.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$215.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$1.4900` (0.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0561`
* Combined: `+$0.0561` | Residual after: `+$2.0939`

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
* Reconcile the position on the full surface and keep the focus on the model revaluation rather than over-reading the small residual.
* No catalyst-specific desk action is supported here because the feed supplied no relevant headlines or named mechanism.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.02 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-09-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$117.5000` (-1301.9%)
* **Model ΔP**: `-$117.5000`
* **Primary drivers**: **Vega PnL** (72%) and **Theta decay** (13%) and **Delta PnL** (13%).
* **Verdict**: The position was driven mainly by the move in implied volatility, with spot drift and higher-order curvature playing only a secondary role. The revaluation is broadly consistent with a vega-led option repricing, while the small residual fits the engine’s clean attribution and the limited spot change. The Apple-specific headlines provide context for the tape, but they do not override the modeled factor story or support a separate microstructure mechanism.
* **Confidence**: **Medium** — Attribution coverage is high and the residual is low, which supports the modeled vega story. Confidence is held at medium because the market feed is incomplete enough that the headlines are only contextual, and the surface diagnostics show a surface limitation even though the run is reliable overall.

---

## 2. Observation Lock

* **As-of**: `2026-09-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 2.9%)
* **IV move**: +0.71 vol pts vs noise band ±0.28 pts (exceeds noise band)
* **Prior observation**: `2026-09-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$117.5000`
* **Model ΔP (engine)**: `-$117.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$123.0069`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$5.5069` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.7%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$34.4422` | -29.3% | Stock moved from $337.00 to $336.13 (-0.8700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.4286` | +0.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$192.4074` | +163.8% | IV moved +3.57 vol pts (26.63% → 27.34%) |
| **Theta decay (Δt · Theta)** | `+$35.3870` | -30.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$5.5069` | -4.7% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$117.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$5.5069` (4.7% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0029`
* Combined: `-$0.0029` | Residual after: `+$1.1779`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction / implied volatility move**._

_Intel note: Two Apple-specific headlines were kept: one on a new iPhone product and one on Apple Pay expansion in India. One peer-tech headline was retained as background; the remaining items were generic options/volatility content and discarded._
_Intel triage discarded 3 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Apple’s new iPhone Duo: Will consumers bite?** _(Source: Yahoo Finance Video)_
   A consumer-demand discussion about a new Apple iPhone model, directly tied to Apple’s product cycle.
2. **Apple (AAPL) Eyes India Payments With Apple Pay Debut Next Month** _(Source: Simply Wall St.)_
   Reports Apple is planning an Apple Pay launch in India next month, a company-specific expansion story.

_Peer / sector background (indirect context, not a required catalyst):_

3. **Meta stock jumps as Wells Fargo raises price target** _(Source: Yahoo Finance Video)_
   A mega-cap tech peer headline that may matter only as sector context for Apple.

---

## 7. Risk Watchlist

* Recheck the full-surface revaluation and the prior-close volatility input, since the move was dominated by implied volatility rather than spot.
* Use the Apple-specific news as context only; there is no supported borrow, squeeze, or early-exercise storyline in this tape.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-09-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$162.5000` (+1666.7%)
* **Model ΔP**: `+$162.5000`
* **Primary drivers**: **Vega PnL** (72%) and **Theta decay** (18%) and **Delta PnL** (6%).
* **Verdict**: The move is led by a higher implied-volatility mark, with the option’s model price rising primarily on the volatility reprice rather than the small spot change. Theta works against the position, but the vol lift dominates the one-day model change; the remaining gap is consistent with normal truncation and model-path effects rather than a separate catalyst.
* **Confidence**: **Medium** — The attribution is well-covered and the market feed is reliable, but the residual is not negligible and the position is near the money, so second-order effects can matter. Headlines are mostly sector background, and the only relevant item is an analyst note on a different issuer, so there is no strong company-specific catalyst to override the blotter.

---

## 2. Observation Lock

* **As-of**: `2026-09-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 6.6%)
* **IV move**: +1.01 vol pts vs noise band ±0.91 pts (exceeds noise band)
* **Prior observation**: `2026-09-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$162.5000`
* **Model ΔP (engine)**: `+$162.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$171.9899`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$9.4899` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (5.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$18.2089` | +11.2% | Stock moved from $349.31 to $349.67 (+0.3600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.1045` | +0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$204.0739` | +125.6% | IV moved +4.76 vol pts (24.79% → 25.81%) |
| **Theta decay (Δt · Theta)** | `-$50.3973` | -31.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$9.4899` | -5.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$162.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$9.4899` (5.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0008`
* Combined: `+$0.0008` | Residual after: `+$1.6242`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.5106`
* **spot**: `+$0.1818`
* **vol**: `+$1.9538`
* **rate**: `+$0.0005`
* Step sum: `+$1.6256` | Model ΔP: `+$1.6250` | Audit residual: `-$0.0006`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega revaluation**._

_Intel note: Most items are sector context for financials, while one headline is relevant because it mentions JPMorgan as the broker on a T-Mobile target cut. No allow-list mechanism is directly indicated by the relevant headline._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **T-Mobile Stock Slips To More Than Two-Year Low — JPMorgan Cuts Target Ahead Of Q3 Citing Softer Service Revenue Outlook** _(Source: Stocktwits)_
   JPMorgan is cited as the broker cutting its price target on T-Mobile ahead of Q3, reflecting a softer service revenue outlook.

_Peer / sector background (indirect context, not a required catalyst):_

2. **Sector Update: Financial Stocks Rise Late Afternoon** _(Source: MT Newswires)_
   Financial-sector shares were broadly higher in late-afternoon trade, which can provide background sentiment for JPMorgan.
3. **Sector Update: Financial Stocks Advance Monday Afternoon** _(Source: MT Newswires)_
   Financial stocks advanced in afternoon trading, offering sector context for JPMorgan.

---

## 7. Risk Watchlist

* Recheck the full-surface repricing around the volatility move and residual, since the Taylor split leaves a noticeable gap versus the model move.
* No direct JPM-specific catalyst is evident in the kept headlines; treat the factor change as a vol-led repricing with only broad financials-sector background.
* Dividend coverage is not a material early-exercise case, so this remains a carry and theta check rather than an assignment watch.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.13 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-09-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$185.0000` (-1651.8%)
* **Model ΔP**: `-$185.0000`
* **Primary drivers**: **Vega PnL** (67%) and **Theta decay** (21%) and **Delta PnL** (9%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is primarily a model revaluation driven by implied volatility dropping, with theta decay the next-largest modeled contributor and spot only a minor offset. The small residual is consistent with ordinary truncation and quote noise rather than a separate event story. There are no relevant headlines, so the run supports a volatility-led repricing rather than a news-led catalyst. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution is supported by high coverage and a low residual band, but observation reliability is false and the market feed is incomplete. There are no retrieved headlines and the critic did not require a catalyst, so Layer B adds no independent mechanism. The American-versus-European premium exists, but the dividend does not cover remaining time value, so early exercise is not the driver.

---

## 2. Observation Lock

* **As-of**: `2026-09-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 7.5%)
* **IV move**: -1.95 vol pts vs noise band ±0.85 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$185.0000`
* **Model ΔP (engine)**: `-$185.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$189.8308`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$4.8308` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.6%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$18.1211` | +9.8% | Stock moved from $349.31 to $349.67 (+0.3600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0985` | -0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$130.9197` | +70.8% | IV moved -3.05 vol pts (27.74% → 25.79%) |
| **Theta decay (Δt · Theta)** | `-$40.8884` | +22.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$4.8308` | -2.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$185.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$4.8308` (2.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0004`
* Combined: `-$0.0004` | Residual after: `-$1.8496`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$0.3600` vs next cash dividend `+$1.5000` (gap `+$1.8600`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$9.3500` vs `+$8.7879` (gap `+$0.5621`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0938` — material
* **Dividend PV effect** (European, same divs − no divs): `+$0.4681`
* **Dividend coverage** (dividend / time value): `0.17` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$1.3092`
* **Residual (Taylor ε)**: `+$0.0483`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Recheck the full-surface revaluation and quote quality, since the move was dominated by model repricing rather than spot.
* Keep the focus on implied volatility and time decay; there is no supported borrow, squeeze, or other headline mechanism to add here.
* **Assignment watch**: ex-div `2026-10-06` — Dividend coverage 0.17 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-09-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$126.5000` (+2404.9%)
* **Model ΔP**: `+$126.5000`
* **Primary drivers**: **Vega PnL** (69%) and **Theta decay** (18%) and **Delta PnL** (9%).
* **Verdict**: The position’s move is dominated by the vega term in the desk blotter, with smaller help from time decay and a minor drag from spot and second-order effects. The headline set is broad market context rather than a SPY-specific event, so the tape reads more like an index-level implied volatility move than a stock-specific catalyst; the run is also consistent with iv crush being present in the background. The remaining gap is consistent with higher-order truncation rather than a discrete new information shock.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is high and the observation is reliable, but the move is still accompanied by a medium residual and the headline set is mostly generic market context. The digest does not show a discrete SPY event, so the catalyst layer is limited to the observed implied volatility backdrop and iv crush language from the relevant tape.

---

## 2. Observation Lock

* **As-of**: `2026-09-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.8%)
* **IV move**: +1.17 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-09-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$126.5000`
* **Model ΔP (engine)**: `+$126.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$133.5771`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$7.0771` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (5.6%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$15.2941` | -12.1% | Stock moved from $762.60 to $761.69 (-0.9100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.1839` | -0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$117.9689` | +93.3% | IV moved -1.48 vol pts (17.01% → 18.18%) |
| **Theta decay (Δt · Theta)** | `+$31.0862` | +24.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$7.0771` | -5.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$126.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$7.0771` (5.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0296`
* Combined: `+$0.0296` | Residual after: `-$1.2946`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.3118`
* **spot**: `+$0.1505`
* **vol**: `-$1.1038`
* **rate**: `-$0.0007`
* Step sum: `-$1.2658` | Model ΔP: `-$1.2650` | Audit residual: `+$0.0008`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction / implied volatility move**._

_Intel note: The item set is mostly index/market context and unrelated single-name tape. No discrete SPY issuer event is present; SPY-relevant items were kept as background, while generic educational and unrelated headlines were discarded._
_Intel triage discarded 2 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **Opendoor Gains 5% but Is Still Down 24% in a Month. Will the Bulls or Bears Win?** _(Source: 24/7 Wall St.)_
   A single-name housing/tech stock move that can sit in the broader tape, but it is not specific to SPY.
2. **AMC Spikes 7% as Refinancing Pushes Maturities From 2029 to 2031; Cinemark and IMAX Edge Higher** _(Source: 24/7 Wall St.)_
   Single-name cinema-sector news that may affect market sentiment at the margin, but it is not specific to SPY.
3. **Today's SPY, QQQ & VIX Gamma, Dealer Positioning & Regime | FlashAlpha** _(Source: FlashAlpha)_
   This is SPY-related market-structure commentary and is relevant as context for the index ETF, but it does not describe a discrete issuer event.
4. **Nasdaq Ends Nearly 3% Higher As AI Stocks Pop, AMD Enters $1 Trillion Club —  AMD, ARM, META, AMZN, PSKY In Focus** _(Source: Stocktwits)_

---

## 7. Risk Watchlist

* Recheck the full-surface revaluation around the implied volatility move and the small residual, since the Taylor view is only approximate and higher-order effects are present.
* Keep the catalyst framing at the index-volatility level: the tape is consistent with iv crush / implied volatility dynamics, not a discrete SPY corporate event.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-09-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$374.5000` (+7072.7%)
* **Model ΔP**: `+$374.5000`
* **Primary drivers**: **Vega PnL** (87%) and **Theta decay** (7%).
* **Verdict**: The position was driven primarily by the move in implied volatility, with the option’s revaluation dominated by the volatility lift rather than the small spot drift. Delta and theta were secondary drags, while the residual stayed small enough to be consistent with normal Taylor truncation and quote noise rather than a distinct unexplained event. The relevant tape context supports an implied volatility / IV crush-style narrative, but there is no ticker-specific issuer catalyst here; for SPY, the broader index and vol regime backdrop is the appropriate Layer B frame.
* **Confidence**: **Medium** — Confidence is medium because the attribution is clear and the feed is marked reliable, but the news set is broad market context rather than a direct SPY event. The residual is low, which supports the vega-led read, while the supplied digest explicitly says no direct ticker mechanism tags were applied; therefore the catalyst layer is limited to implied volatility context rather than a stronger event claim.

---

## 2. Observation Lock

* **As-of**: `2026-09-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.4%)
* **IV move**: +0.79 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-09-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$374.5000`
* **Model ΔP (engine)**: `+$374.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$365.9715`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$8.5285` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2.3%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$21.9168` | -5.9% | Stock moved from $762.60 to $761.69 (-0.9100) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.3374` | +0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$420.2285` | +112.2% | IV moved +4.26 vol pts (13.22% → 14.02%) |
| **Theta decay (Δt · Theta)** | `-$32.6776` | -8.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$8.5285` | +2.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$374.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$8.5285` (2.3% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.2553`
* Combined: `+$0.2553` | Residual after: `+$3.4897`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction / implied volatility move**._

_Intel note: I kept broad market/index-structure items that can inform SPY context and discarded unrelated single-name or educational headlines. No headline here was a direct SPY issuer event, so no mechanism tags were applied._
_Intel triage discarded 4 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **Nasdaq Ends Nearly 3% Higher As AI Stocks Pop, AMD Enters $1 Trillion Club —  AMD, ARM, META, AMZN, PSKY In Focus** _(Source: Stocktwits)_
   Broad market technology/AI strength in the Nasdaq session could matter indirectly for SPY sentiment and index-level flow.
2. **Today's SPY, QQQ & VIX Gamma, Dealer Positioning & Regime | FlashAlpha** _(Source: FlashAlpha)_
   This is directly about SPY market structure and index positioning.

---

## 7. Risk Watchlist

* Reconcile the move as a vega-led full-surface repricing, with spot and decay as secondary effects and the small residual left to normal truncation / noise.
* Use the broader index-vol backdrop, including IV crush / implied volatility context, as the explanatory layer for the tape rather than any single-name catalyst.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-09-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$20.0000` (-547.9%)
* **Model ΔP**: `-$20.0000`
* **Primary drivers**: **Delta PnL** (69%) and **Vega PnL** (15%) and **Theta decay** (15%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is explained primarily by the underlying drifting lower, which hit the call through its positive delta. Gamma only slightly cushioned the move, while vega and theta offset part of the decline but did not change the dominant spot-led story. The residual is negligible, so this run is a clean model revaluation with no separate catalyst layer identified. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — The attribution coverage is strong and the residual is low, which supports the modeled driver. Confidence is held at medium because observation quality is flagged as unreliable and the surface diagnostics note limitations, so the run should be read as a clean revaluation but not over-interpreted beyond the blotter.

---

## 2. Observation Lock

* **As-of**: `2026-09-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 20.3%)
* **IV move**: +3.71 vol pts vs noise band ±7.73 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$20.0000`
* **Model ΔP (engine)**: `-$20.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$20.0577`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0577` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.3%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$20.5254` | +102.6% | Stock moved from $48.33 to $48.09 (-0.2400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.2202` | -1.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$4.5687` | -22.8% | IV moved +1.11 vol pts (25.73% → 29.44%) |
| **Theta decay (Δt · Theta)** | `-$4.3213` | +21.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0577` | -0.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$20.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0577` (0.3% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0040`
* Combined: `+$0.0040` | Residual after: `-$0.2040`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$0.2400` vs next cash dividend `+$0.7080` (gap `+$0.4680`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$3.4500` vs `+$3.4749` (gap `-$0.0249`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.1570` — material
* **Dividend PV effect** (European, same divs − no divs): `-$0.1820`
* **Dividend coverage** (dividend / time value): `1.97` — early exercise is economically relevant
* **Vol (Taylor Vega PnL)**: `+$0.0457`
* **Residual (Taylor ε)**: `+$0.0006`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Recheck the full revaluation path and hedge against further spot sensitivity; the move is overwhelmingly a delta story.
* Early exercise is economically relevant here because the dividend does not fully cover remaining time value, so the American boundary matters even without a separate headline catalyst.
* **Assignment watch**: ex-div `2026-10-09` — Dividend coverage 1.97 (dividend $0.7080 vs time value $0.3600); ex-div is 18d out, expiry 60d out — early exercise is economically relevant.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-09-21` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Vega PnL** (49%) and **Delta PnL** (26%) and **Theta decay** (22%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by a vega revaluation: the option model held flat while the implied-vol move was the largest positive contributor, with smaller offsetting impacts from spot drift and theta. Because the observation is not reliable and the Vega narrative is suppressed by the code, this should be read as a model reprice driven by the vol change rather than a conviction news explanation. The residual is small relative to the total move, so higher-order truncation and quote noise are present but not the main story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* **Confidence**: **Medium** — Confidence is only medium because observation quality is flagged as unreliable, the Vega narrative is explicitly suppressed, and there are no retrieved headlines to connect the revaluation to a specific catalyst. The dominant factor is still clear from the blotter, but the terminal unexplained break means the watchlist should remain open.

---

## 2. Observation Lock

* **As-of**: `2026-09-21` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 28.6%)
* **IV move**: +1.56 vol pts vs noise band ±2.81 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-18`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0233`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0233` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (198391181.4%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.2957` | +25.6% | Stock moved from $2.12 to $2.09 (-0.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0088` | +0.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.5680` | +49.2% | IV moved +3.09 vol pts (85.94% → 87.50%) |
| **Theta decay (Δt · Theta)** | `-$0.2579` | +22.3% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0233` | +2.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0233` (198391181.4% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0001`
* Combined: `-$0.0001` | Residual after: `+$0.0001`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0026`
* **spot**: `-$0.0027`
* **vol**: `+$0.0053`
* **rate**: `+$0.0000`
* Step sum: `+$0.0000` | Model ΔP: `+$0.0000` | Audit residual: `-$0.0000`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Vega story not falsifiable from quote Gaps: Vega narrative suppressed by quote noise band
* Reconcile the position with a full-surface reprice and confirm the vega move against the stored prior-IV source, since the model story is volatility-led rather than spot-led.
* No named catalyst was recovered; with the observation lock in place, treat any vol interpretation as provisional until better tape or quote evidence appears.

---


## Skew proxy (Task C3.3, SPY risk reversal)

* skew_proxy(t) = +0.0416 | level_proxy(t) = 0.1610
* Δskew = +0.0038 | Δlevel = +0.0098
* Put 715 delta=-0.1480 | Call 795 delta=0.2944
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
