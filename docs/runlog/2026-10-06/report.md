# Live book run — 2026-10-06

Run `2026-10-06-1791335710`. 8/8 legs completed, 0 failed. `legs_narrated=6` `legs_silent=2` `llm_calls=8`.

# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-10-06` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$75.5000`
* **Total Model PnL**: `+$75.5000`
* **Aggregate model vs mark gap**: `+$0.0000`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `SPY 795C 2026-11-20` | `+$145.0000` |
| 2 | `JPM 350P 2026-10-23` | `-$130.0000` |
| 3 | `SPY 715P 2026-11-20` | `+$52.5000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `+$274.1289` |
| Gamma | `+$8.0085` |
| Vega | `-$212.8427` |
| Theta | `-$43.9452` |
| Residual | `+$50.1504` |

### Notable underlyings

* **SPY**: `+$197.5000` aggregate option PnL
* **JPM**: `-$125.5000` aggregate option PnL
* **AAPL**: `+$12.5000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-10-06` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$17.5000` (-98.0%)
* **Model ΔP**: `-$17.5000`
* **Primary drivers**: **Vega PnL** (44%) and **Delta PnL** (41%) and **Theta decay** (14%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-10-06` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.1%)
* **IV move**: -2.02 vol pts vs noise band ±0.63 pts (exceeds noise band)
* **Prior observation**: `2026-10-05`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$17.5000`
* **Model ΔP (engine)**: `-$17.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$18.5196`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.0196` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (5.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$46.8490` | -267.7% | Stock moved from $332.89 to $333.63 (+0.7400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.3197` | -1.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$50.2822` | +287.3% | IV moved -1.13 vol pts (30.62% → 28.60%) |
| **Theta decay (Δt · Theta)** | `-$15.4062` | +88.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.0196` | -5.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$17.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.0196` (5.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0031`
* Combined: `+$0.0031` | Residual after: `-$0.1781`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1540`
* **spot**: `+$0.4721`
* **vol**: `-$0.4931`
* **rate**: `+$0.0046`
* Step sum: `-$0.1704` | Model ΔP: `-$0.1750` | Audit residual: `-$0.0046`

### Diagnostic tool summary

* **Tools run** (4 total; costly 1/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Theta / carry**._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* No action needed; move is within theta/carry tolerance.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-10-06` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$30.0000` (+495.9%)
* **Model ΔP**: `+$30.0000`
* **Primary drivers**: **Vega PnL** (53%) and **Delta PnL** (30%) and **Theta decay** (16%).
* **Verdict**: The position was driven first by the modeled volatility move, with theta also helping and spot delta partly offsetting the gain. The small residual and high attribution coverage indicate the Greek decomposition is doing most of the work, so the run reads as a clean full revaluation rather than a noisy tape. The available headlines are only peer and sector context, not an Apple-specific catalyst, so they support the broader tech/semiconductor backdrop but do not replace the modeled driver.
* **Confidence**: **Medium** — Confidence is medium because the blotter is reliable and the residual is tiny, but the headlines do not name the issuer or a direct event for this contract. The market feed is also incomplete on direct company news, so the catalyst layer remains limited to indirect context.

---

## 2. Observation Lock

* **As-of**: `2026-10-06` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 3.5%)
* **IV move**: +22.67 vol pts vs noise band ±0.24 pts (exceeds noise band)
* **Prior observation**: `2026-10-05`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$30.0000`
* **Model ΔP (engine)**: `+$30.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$30.0376`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0376` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.1%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$23.8803` | -79.6% | Stock moved from $332.89 to $333.63 (+0.7400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.3257` | -1.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$41.3107` | +137.7% | IV moved -0.97 vol pts (3.13% → 25.80%) |
| **Theta decay (Δt · Theta)** | `+$12.9329` | +43.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0376` | -0.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$30.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0376` (0.1% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0016`
* Combined: `-$0.0016` | Residual after: `-$0.2984`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Vega contraction / implied volatility move**._

_Intel note: No Apple-specific headline is present. The kept items are Micron earnings/sentiment context that could matter indirectly for the semiconductor tape, while the gold-miner note is unrelated._
_Intel triage discarded 1 low-relevance headline(s)._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_Peer / sector background (indirect context, not a required catalyst):_

1. **Dow Jones Futures: Micron Earnings Crush Views, S&P 500 At Critical Level As Treasury Yields Rise - Investor's Business Daily** _(Source: Investor's Business Daily)_
   Micron’s earnings beat and forward outlook were the focus; this is sector/tape context rather than an Apple-specific headline.
2. **Micron tops Q4 estimates on top and bottom lines, offers strong Q1 outlook - finance.yahoo.com** _(Source: finance.yahoo.com)_
   Micron reported strong results and guidance, which can influence semiconductor sentiment but does not directly reference Apple.

---

## 7. Risk Watchlist

* Layer A: keep in mind the attribution is a model reprice; a full-surface recalibration or higher-order convexity around the spot and vol move could still slightly alter the split.
* Layer B: watch whether the broader tech / semiconductor tape keeps implied volatility firm or lets it compress further; the headlines here are indirect and do not provide an Apple-specific microstructure cue.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.05 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-10-06` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$4.5000` (+252.8%)
* **Model ΔP**: `+$4.5000`
* **Primary drivers**: **Vega PnL** (52%) and **Delta PnL** (26%) and **Theta decay** (18%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was modeled as driven primarily by implied volatility, with the option revaluing higher as the IV move dominated the close-to-close change. Spot drifted lower and theta was a headwind, but those effects were secondary to the vega contribution; the small residual is consistent with higher-order effects and model truncation rather than a separate catalyst. Early exercise is not a meaningful factor here, and the American price sits essentially on the European cross-check. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by unreliable observation tags and the absence of news headlines, so the run is best read as a model attribution rather than a tape-driven event story. The residual is present but not large enough on its own to overturn the dominant vega read, and there is no evidence of borrow, squeeze, or dividend-driven early exercise effects.

---

## 2. Observation Lock

* **As-of**: `2026-10-06` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 30.1%)
* **IV move**: +2.54 vol pts vs noise band ±1.46 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-05`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$4.5000`
* **Model ΔP (engine)**: `+$4.5000`
* **Model vs Mark gap**: `-$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$6.6868`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$2.1868` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (48.6%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$20.2505` | +26.3% | Stock moved from $332.38 to $331.28 (-1.1000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.8859` | +1.2% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$39.8113` | +51.8% | IV moved +2.03 vol pts (25.82% → 28.36%) |
| **Theta decay (Δt · Theta)** | `-$13.7599` | +17.9% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$2.1868` | +2.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$4.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$2.1868` (48.6% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0079`
* Combined: `-$0.0079` | Residual after: `+$0.0529`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1376`
* **spot**: `-$0.1855`
* **vol**: `+$0.3681`
* **rate**: `+$0.0005`
* Step sum: `+$0.0456` | Model ΔP: `+$0.0450` | Audit residual: `-$0.0006`

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
* Higher-order convexity and Taylor truncation can still account for the remaining gap versus the full revaluation.
* Monitor whether the implied volatility move persists or mean-reverts on the next marks; no borrow, squeeze, or dividend exercise signal is present here.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-10-06` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$130.0000` (-626.5%)
* **Model ΔP**: `-$130.0000`
* **Primary drivers**: **Vega PnL** (61%) and **Delta PnL** (21%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The modeled move is dominated by the drop in implied volatility, with spot contributing in the opposite direction and theta adding additional decay. Because the spot change was small and the residual is sizable, the Greek breakdown should be read as a coarse explanation with higher-order convexity and path effects filling the gap. There are no relevant headlines, and the feed notes no named microstructure or event catalyst to attach beyond the modeled vol repricing. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is only medium because observation is unreliable, the residual share is high, and the engine notes local vol was deferred to mark calibration. The only clear driver signal is the large implied-vol move in the blotter; there is no headline support for a separate catalyst, and the independent critic did not require one.

---

## 2. Observation Lock

* **As-of**: `2026-10-06` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `thin` (spread/mid 10.3%)
* **IV move**: -11.27 vol pts vs noise band ±6.98 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-05`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$130.0000`
* **Model ΔP (engine)**: `-$130.0000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$182.4150`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$52.4150` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (40.3%)
  Escalation basis: method residual — today's option quote tier is `thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$82.6820` | -63.6% | Stock moved from $332.38 to $331.28 (-1.1000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.8179` | -0.6% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$246.1385` | +189.3% | IV moved -10.57 vol pts (37.70% → 26.42%) |
| **Theta decay (Δt · Theta)** | `-$19.7763` | +15.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$52.4150` | -40.3% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$130.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$52.4150` (40.3% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.2039`
* Combined: `+$0.2039` | Residual after: `-$1.5039`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1979`
* **spot**: `+$0.8428`
* **vol**: `-$1.9452`
* **rate**: `-$0.0016`
* Step sum: `-$1.3019` | Model ΔP: `-$1.3000` | Audit residual: `+$0.0019`

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
* Layer A: verify whether the residual is coming from truncation, path revaluation, or the American boundary rather than treating the Taylor split as exact.
* Layer B: no headline-based catalyst is available here; if new tape appears, confirm whether implied volatility stays the key repricing channel.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-10-06` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$52.5000` (+>1000%)
* **Model ΔP**: `+$52.5000`
* **Primary drivers**: **Delta PnL** (74%) and **Theta decay** (16%) and **Gamma PnL** (5%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position moved בעיקר by the modeled delta exposure to the higher SPY spot, with theta helping and gamma partly offsetting the move. The residual is small, so the Taylor view is already close to the full revaluation, and there is no headline-backed Layer B catalyst to add. Because observation quality is weak and the vol narrative is suppressed, this should be read as a clean spot-led repricing rather than a news-driven event. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Medium** — Confidence is tempered by the observation lock and the fact that the market feed is incomplete, so the run is best treated as a model revaluation rather than a fully validated mark story. Even so, the dominant driver is clearly the spot move, the residual is low, and there are no relevant headlines or mechanism tags to support an alternate explanation.

---

## 2. Observation Lock

* **As-of**: `2026-10-06` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 1.3%)
* **IV move**: +0.02 vol pts vs noise band ±0.03 pts (inside noise band — **Vega story not falsifiable**)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-05`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$52.5000`
* **Model ΔP (engine)**: `+$52.5000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$53.4698`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.9698` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.8%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$45.1941` | +86.1% | Stock moved from $774.83 to $779.09 (+4.2600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$3.1125` | -5.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$1.3994` | +2.7% | IV moved -0.03 vol pts (18.89% → 18.91%) |
| **Theta decay (Δt · Theta)** | `+$9.9887` | +19.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.9698` | -1.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$52.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.9698` (1.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0013`
* Combined: `+$0.0013` | Residual after: `-$0.5263`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Watch whether Taylor-style attribution stays stable if the full surface is refreshed or the mark calibration changes; higher-order terms and early-exercise boundary shifts can still nudge the reconciliation.
* No Layer B catalyst was supplied, so there is no borrow, squeeze, or IV-crush check to track from the digest on this run.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-10-06` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$145.0000` (+>1000%)
* **Model ΔP**: `+$145.0000`
* **Primary drivers**: **Delta PnL** (77%) and **Theta decay** (9%) and **Vega PnL** (8%).
* **Verdict**: The option’s move was driven primarily by the underlying’s spot advance, with gamma providing a smaller convexity assist and theta offsetting part of the gain. The residual was negligible, so the Taylor view is a clean fit to the model revaluation rather than a sign of an additional mechanism. There were no relevant headlines, borrow cues, or IV-crush tags to add a separate catalyst layer.
* **Confidence**: **Medium** — Confidence is medium because the attribution coverage is high and the residual is low, but the run also notes a calibrated-mark limitation and the available news layer is empty. The American early-exercise premium is negligible, so there is no meaningful dividend or assignment overlay to explain.

---

## 2. Observation Lock

* **As-of**: `2026-10-06` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `reliable` (spread/mid 0.5%)
* **IV move**: +0.21 vol pts vs noise band ±0.02 pts (exceeds noise band)
* **Prior observation**: `2026-10-05`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$145.0000`
* **Model ΔP (engine)**: `+$145.0000`
* **Model vs Mark gap**: `+$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$145.2658`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.2658` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.2%)
  Escalation basis: method residual — the prior-day option quote is not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$136.5897` | +94.2% | Stock moved from $774.83 to $779.09 (+4.2600) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$9.3369` | +6.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$14.8895` | +10.3% | IV moved +0.15 vol pts (13.57% → 13.78%) |
| **Theta decay (Δt · Theta)** | `-$15.5502` | -10.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.2658` | -0.2% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$145.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.2658` (0.2% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0065`
* Combined: `+$0.0065` | Residual after: `+$1.4435`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Delta / spot move**._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

_No corroborating headlines retrieved for this window._

---

## 7. Risk Watchlist

* Watch whether a larger spot gap or sharper surface move would start to make the higher-order convexity terms more important than the current linear delta read.
* With no relevant headlines or microstructure tags, there is no borrow, squeeze, or IV-crush signal to verify from the tape; continue to treat the move as a spot-led model reprice.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-10-06` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$8.5000` (-435.9%)
* **Model ΔP**: `-$8.5000`
* **Primary drivers**: **Vega PnL** (58%) and **Delta PnL** (31%) and **Theta decay** (10%).
* **Verdict**: Nothing to explain. The move is accounted for by carry and a small spot move; the unexplained portion is within tolerance. No news search was performed.
* **Confidence**: **Medium** — Escalation metric is at or below the quiet-day threshold; see the Mark Reconciliation section for the exact figures.

---

## 2. Observation Lock

* **As-of**: `2026-10-06` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide` (spread/mid 19.8%)
* **IV move**: -6.32 vol pts vs noise band ±2.96 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-05`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$8.5000`
* **Model ΔP (engine)**: `-$8.5000`
* **Model vs Mark gap**: `-$0.0000` (+0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$8.6532`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.1532` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (1.8%)
  Escalation basis: method residual — today's option quote tier is `wide`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$7.2085` | -84.8% | Stock moved from $45.85 to $45.98 (+0.1300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0782` | -0.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$13.6618` | +160.7% | IV moved -2.16 vol pts (30.00% → 23.68%) |
| **Theta decay (Δt · Theta)** | `-$2.2780` | +26.8% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.1532` | -1.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$8.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.1532` (1.8% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0004`
* Combined: `+$0.0004` | Residual after: `-$0.0854`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `+$0.1300` vs next cash dividend `+$0.7080` (gap `+$0.8380`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$1.8650` vs `+$2.0726` (gap `-$0.2076`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.0006` — not material
* **Dividend PV effect** (European, same divs − no divs): `-$0.2082`
* **Dividend coverage** (dividend / time value): `0.80` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$0.1366`
* **Residual (Taylor ε)**: `+$0.0015`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_Observation unreliable — event linkage suppressed; reconcile marks before catalyst stories._


---

## 7. Risk Watchlist

* No action needed; move is within theta/carry tolerance.
* **Assignment watch**: ex-div `2026-10-09` — Dividend coverage 0.80 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-10-06` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `-$0.5000` (->1000%)
* **Model ΔP**: `-$0.5000`
* **Primary drivers**: **Delta PnL** (47%) and **Vega PnL** (30%) and **Theta decay** (17%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position was driven first by the lower underlying price, with the option’s directional exposure doing most of the work in the model revaluation. Vega and theta also added to the decline, while gamma was a small offset; the remaining gap is consistent with normal second-order truncation rather than a distinct event-driven mechanism. There are no retrieved headlines or named microstructure tokens to add a separate catalyst story, and the American early-exercise premium is negligible. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — The attribution is mechanically clear in the blotter, but observation quality is weak and the model run explicitly flags unreliable observation and a failed surface diagnostic. Residuals are modest, yet there is no news tape to independently challenge or confirm the move, so the diagnosis should stay coarse.

---

## 2. Observation Lock

* **As-of**: `2026-10-06` | **Data**: `yfinance` | **IV prev**: `chain_t1`
* **Quote tier**: `wide+thin` (spread/mid 40.0%)
* **IV move**: +53.12 vol pts vs noise band ±4.15 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-10-05`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `-$0.5000`
* **Model ΔP (engine)**: `-$0.5000`
* **Model vs Mark gap**: `+$0.0000` (-0.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$0.5227`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.0227` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (4.5%)
  Escalation basis: method residual — today's option quote tier is `wide+thin`, not reliable; this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.2636` | +46.9% | Stock moved from $1.89 to $1.86 (-0.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0081` | +1.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.1711` | +30.5% | IV moved -1.26 vol pts (50.00% → 103.13%) |
| **Theta decay (Δt · Theta)** | `-$0.0961` | +17.1% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0227` | +4.0% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.5000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0227` (4.5% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0000`
* Combined: `+$0.0000` | Residual after: `-$0.0050`

### Diagnostic tool summary

* **Tools run** (3 total; costly 0/1, free tools do not use the budget): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Risk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Monitor whether a fuller revaluation changes the mix between directional and higher-order effects if the spot path stays choppy.
* Verify marks and surface calibration when more reliable quotes are available; do not infer a squeeze, borrow, or implied-volatility narrative from this run.

---


## Skew proxy (SPY risk reversal)

* skew_proxy(t) = +0.0513 | level_proxy(t) = 0.1635
* Δskew = -0.0019 | Δlevel = +0.0012
* Put 715 delta=-0.0898 | Call 795 delta=0.3649
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
