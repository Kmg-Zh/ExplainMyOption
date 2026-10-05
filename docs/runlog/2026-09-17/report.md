# Live book run — 2026-09-17

Run `2026-09-17-1789651307`. 8/8 legs completed, 0 failed. `legs_narrated=8` `legs_silent=0` `llm_calls=8`.

**No leg in this run has a cached t-1 snapshot yet** (`iv_prev_source` is `hv20_proxy` or `copied` for every leg below) -- this is the book's opening day, or the first run since a leg changed. Every `ΔP`/residual/terminal-state figure below is comparing today's quote against a statistically-derived proxy for yesterday, not a real prior trading day, and should be read as noisy. This run still caches each leg's snapshot (`data.cache.upsert_snapshot`), so tomorrow's run compares against today for real.


# Portfolio Option Diagnostic Report

**Analysis Date**: `2026-09-17` | **Positions**: 8 | **Tickers**: AAPL, JPM, PLUG, SPY, VZ

---

## Portfolio Executive Summary

* **Total Mark MTM PnL**: `+$0.0000`
* **Total Model PnL**: `-$169.9804`
* **Aggregate model vs mark gap**: `-$169.9804`

| Rank | Contract | PnL ($) |
| ---: | :--- | ---: |
| 1 | `VZ 45C 2026-11-20` | `-$169.9805` |
| 2 | `SPY 715P 2026-11-20` | `+$0.0000` |
| 3 | `SPY 795C 2026-11-20` | `-$0.0000` |

### Aggregate factor attribution

| Factor | Portfolio ($) |
| :--- | ---: |
| Delta | `-$317.9879` |
| Gamma | `+$22.4260` |
| Vega | `+$180.5958` |
| Theta | `-$53.3518` |
| Residual | `-$1.6626` |

### Notable underlyings

* **VZ**: `-$169.9805` aggregate option PnL
* **SPY**: `+$0.0000` aggregate option PnL
* **PLUG**: `+$0.0000` aggregate option PnL

---

## Position Detail

### Position 1 — `AAPL 325C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 325C 2026-11-20`  
**Analysis Date**: `2026-09-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Delta PnL** (49%) and **Vega PnL** (30%) and **Theta decay** (20%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The position’s modeled change was led by the spot move, with delta as the dominant Taylor driver and gamma only a minor positive offset. Vega and theta worked against the call, but the overall model revaluation stayed essentially flat because the move was small and the run is flagged as low-confidence with weak observation quality. The large residual is best treated as Taylor truncation and model/mark noise rather than a separate news-led catalyst, and there are no retrieved headlines to support a Layer B mechanism. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — The run is explicitly marked with low confidence, low attribution coverage, and unreliable observation quality. The residual band is high while the spot and vol moves are small, so the Greek decomposition is only a reference view and higher-order effects or quote noise can dominate the gap. No relevant headlines were retrieved, so there is no independent catalyst to anchor a stronger narrative.

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
* **Explained ΔP (Taylor ex-residual)**: `-$0.7474`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.7474` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (2082812722715.0%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-15 and/or 2026-09-17, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$65.0477` | +49.0% | Stock moved from $331.34 to $332.41 (+1.0700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.5534` | +0.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$39.1757` | +29.5% | IV moved -0.72 vol pts (0.32% → 0.00%) |
| **Theta decay (Δt · Theta)** | `-$27.1728` | +20.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.7474` | +0.6% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.7474` (2082812722715.0% of |model|)

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0001`
* Combined: `+$0.0001` | Residual after: `-$0.0001`

### Diagnostic tool summary

* **Tools run** (0/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Reconcile on the full revaluation and treat the Taylor split as a rough reference only; the gap is consistent with truncation and data-quality limits.
* No Layer B catalyst is available from the blotter, so avoid adding a borrow, squeeze, or IV-crush story without fresh evidence.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.02 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 2 — `AAPL 350C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `AAPL 350C 2026-11-20`  
**Analysis Date**: `2026-09-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Delta PnL** (49%) and **Theta decay** (31%) and **Vega PnL** (19%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The model attributes the day mainly to delta exposure, with smaller offsetting contributions from theta and vega around a near-flat revaluation. Because the observation is unreliable and the residual band is high, the Taylor split should be treated as a reference view rather than a precise explanation of the move; the terminal unexplained break also warrants caution. No headline set was retrieved, so there is no Layer B catalyst to layer on top of the modeled driver. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because the observation is flagged unreliable, the feed used a copied or proxied prior IV, and the diagnostic run shows a high residual with a terminal unexplained break. The dominant factor is still the code-supplied delta driver, but there is no news evidence to support a separate catalyst story.

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
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$0.3386`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$0.3386` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (25105818518.2%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-15 and/or 2026-09-17, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$38.0937` | +49.3% | Stock moved from $331.34 to $332.41 (+1.0700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.5668` | +0.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$14.6281` | +18.9% | IV moved -0.28 vol pts (3.44% → 3.13%) |
| **Theta decay (Δt · Theta)** | `+$23.6937` | +30.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.3386` | +0.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.3386` (25105818518.2% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0026`
* Combined: `-$0.0026` | Residual after: `+$0.0026`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2375`
* **spot**: `+$0.3829`
* **vol**: `-$0.1454`
* Step sum: `+$0.0000` | Model ΔP: `+$0.0000` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (1/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Recheck the position through a full-surface reprice and delta hedge review, since the Taylor split is only a reference view under the current data quality flags.
* No catalyst overlay is supported by the retrieved tape, so keep the watchlist focused on quote quality and reconciliation rather than a borrow, squeeze, or IV-crush narrative.
* **Assignment watch**: ex-div `2026-11-08` — Dividend coverage 0.03 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 3 — `JPM 350C 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350C 2026-10-23`  
**Analysis Date**: `2026-09-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (47%) and **Delta PnL** (43%) and **Theta decay** (6%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter points to a vega-led revaluation, with the option’s price change driven mainly by the IV move rather than by the spot drift. Delta also leaned against the position, while gamma and theta only partially offset the move, leaving a small method residual around the Taylor bucket. Because the observation is not reliable and no headlines were retrieved, this is a model-based explanation of the move rather than a news-linked catalyst story. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because the observation is flagged unreliable, the attribution coverage is weak, and the residual band is high. IV prior was proxied, so the vega line should be treated as a model reprice explanation rather than a fully observed market fact. There are no retrieved headlines, and the independent catalyst critic was skipped under the observation lock, so no catalyst mechanism can be asserted.

---

## 2. Observation Lock

* **As-of**: `2026-09-17` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `unquoted`
* **IV move**: +0.05 vol pts vs noise band ±0.00 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$3.9329`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$3.9329` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (76824422365.6%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-15 and/or 2026-09-17, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$202.0807` | +43.4% | Stock moved from $352.49 to $348.92 (-3.5700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$12.5904` | +2.7% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$220.0024` | +47.3% | IV moved +4.95 vol pts (0.35% → 0.39%) |
| **Theta decay (Δt · Theta)** | `-$26.5793` | +5.7% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$3.9329` | +0.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$3.9329` (76824422365.6% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `+$0.0102`
* Combined: `+$0.0102` | Residual after: `-$0.0102`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2674`
* **spot**: `-$1.8870`
* **vol**: `+$2.1544`
* Step sum: `-$0.0000` | Model ΔP: `-$0.0000` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (1/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Reprice the book with a fresh surface and verify the vega bucket against the current IV regime before leaning on the Taylor decomposition.
* Keep the position on watch for unexplained break behavior, but do not force a news or microstructure explanation without retrieved evidence.
* **Assignment watch**: ex-div `2026-10-04` — Dividend coverage 0.16 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 4 — `JPM 350P 2026-10-23`

# Option Price Movement Diagnostic Report

**Contract**: `JPM 350P 2026-10-23`  
**Analysis Date**: `2026-09-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Delta PnL** (46%) and **Vega PnL** (42%) and **Theta decay** (8%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter’s modeled driver is delta: the put gained from the lower spot, with gamma adding a smaller convexity support while theta and the vol move partially offset it. Because observation quality is weak and the Taylor residual is elevated, treat the Greek split as a reference view and rely on the full revaluation as the headline number rather than over-reading the decomposition. There are no relevant headlines, so no separate catalyst layer is supported here. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because the observation is marked unreliable, the IV proxy was used from a copied prior source, and the residual band is high relative to the modeled move. The independent catalyst check was skipped and no relevant headlines were retrieved, so there is no external event evidence to sharpen the story beyond the blotter. The American-versus-European gap is material, but the dividend does not cover remaining time value, so this is not an early-exercise finding.

---

## 2. Observation Lock

* **As-of**: `2026-09-17` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `unquoted`
* **IV move**: -0.01 vol pts vs noise band ±0.00 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000`
* **Explained ΔP (Taylor ex-residual)**: `-$4.9193`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$4.9193` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (784958827462.7%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-15 and/or 2026-09-17, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$162.6961` | +46.2% | Stock moved from $352.49 to $348.92 (-3.5700) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$8.4675` | +2.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$147.3800` | +41.8% | IV moved -3.28 vol pts (0.01% → 0.00%) |
| **Theta decay (Δt · Theta)** | `-$28.7029` | +8.2% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$4.9193` | +1.4% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$4.9193` (784958827462.7% of |model|)

### Second-order Taylor (Layer 3)
* Vanna PnL: `-$0.0390` | Volga PnL: `+$0.0631`
* Combined: `+$0.0242` | Residual after: `-$0.0242`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2893`
* **spot**: `+$1.7165`
* **vol**: `-$1.4272`
* Step sum: `-$0.0000` | Model ΔP: `-$0.0000` | Audit residual: `+$0.0000`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$3.5700` vs next cash dividend `+$1.5000` (gap `-$2.0700`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$10.9500` vs `+$10.3701` (gap `+$0.5799`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.1084` — material
* **Dividend PV effect** (European, same divs − no divs): `+$0.4713`
* **Dividend coverage** (dividend / time value): `0.15` — carry/theta case, not an early-exercise case
* **Vol (Taylor Vega PnL)**: `-$1.4738`
* **Residual (Taylor ε)**: `+$0.0492`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (4/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `deep_diagnostics` — mark calibrated and gap small
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Reprice the full surface and keep delta hedging tight; the Taylor split is only a reference when residuals are elevated.
* Do not force a catalyst read: no relevant headline or borrow / squeeze / IV-crush mechanism is present in the digest.
* **Assignment watch**: ex-div `2026-10-04` — Dividend coverage 0.15 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 5 — `SPY 715P 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 715P 2026-11-20`  
**Analysis Date**: `2026-09-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Delta PnL** (48%) and **Vega PnL** (33%) and **Theta decay** (16%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The run is dominated by the modeled delta response to a modest downside spot move, with gamma and theta providing smaller offsetting contributions and vega also helping cushion the move. Because the observation is unreliable and the residual band is high, the Taylor view should be treated as a coarse explanation rather than a precise one; the full revaluation is effectively flat and the unexplained break warrants caution. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because the observation is marked unreliable, attribution coverage is weak, the residual band is high, and the effective price change is flat despite several competing Greek contributions. There are no retrieved headlines, the catalyst brief is skipped under observation lock, and the terminal unexplained break means the desk should not force a tighter story than the data supports.

---

## 2. Observation Lock

* **As-of**: `2026-09-17` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `unquoted`
* **IV move**: -0.17 vol pts vs noise band ±0.00 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$1.2734`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `+$1.2734` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (14791169.3%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-15 and/or 2026-09-17, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$72.7532` | +48.2% | Stock moved from $757.39 to $754.05 (-3.3400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$2.6569` | +1.8% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$49.4321` | +32.8% | IV moved -0.52 vol pts (3.29% → 3.13%) |
| **Theta decay (Δt · Theta)** | `+$24.7046` | +16.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$1.2734` | +0.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$1.2734` (14791169.3% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0001`
* Combined: `-$0.0001` | Residual after: `+$0.0001`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.2477`
* **spot**: `+$0.7462`
* **vol**: `-$0.4985`
* Step sum: `-$0.0000` | Model ΔP: `-$0.0000` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (1/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Recheck the position with a full-surface repricing and delta hedge review rather than leaning on the truncated Taylor split.
* Keep the unexplained break on watch; with no validated catalyst and weak observation quality, avoid over-interpreting the factor mix.
* **Assignment watch**: ex-div `2026-10-17` — Dividend coverage 0.24 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 6 — `SPY 795C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `SPY 795C 2026-11-20`  
**Analysis Date**: `2026-09-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-0.0%)
* **Model ΔP**: `-$0.0000`
* **Primary drivers**: **Vega PnL** (48%) and **Delta PnL** (37%) and **Theta decay** (10%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter’s dominant modeled driver is Vega, with spot and gamma contributing in the opposite direction and theta a smaller drag. Because the IV input was proxied from historical volatility and observation quality is flagged unreliable, this reads as a model revaluation driven mainly by the volatility input rather than a clean tape-confirmed market move. The small unexplained break and the high residual are consistent with truncation and data-quality limits rather than a separate named catalyst. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation reliability is false, the IV history was proxied, headline support is absent, and the residual band is high. The critic was skipped under observation lock, and there is no basis to add a borrow, squeeze, or IV-crush mechanism.

---

## 2. Observation Lock

* **As-of**: `2026-09-17` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `unquoted`
* **IV move**: -0.17 vol pts vs noise band ±0.00 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$0.0000`
* **Model vs Mark gap**: `-$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$5.0817`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$5.0817` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (367932848.8%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-15 and/or 2026-09-17, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$63.5395` | +36.6% | Stock moved from $757.39 to $754.05 (-3.3400) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$4.1253` | +2.4% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$82.6665` | +47.6% | IV moved +0.95 vol pts (3.29% → 3.13%) |
| **Theta decay (Δt · Theta)** | `-$18.1706` | +10.5% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$5.0817` | +2.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$5.0817` (367932848.8% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* Vanna PnL: `-$0.0473` | Volga PnL: `+$0.0150`
* Combined: `-$0.0323` | Residual after: `+$0.0323`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1815`
* **spot**: `-$0.5783`
* **vol**: `+$0.7597`
* Step sum: `-$0.0000` | Model ΔP: `-$0.0000` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (1/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Recheck the position with a fuller surface reprice and delta hedge once a cleaner mark is available, because the current Taylor view is only a reference under weak observation quality.
* Do not force a catalyst narrative here; keep the move framed as a volatility-driven revaluation with truncation and quote-quality caveats.
* **Assignment watch**: ex-div `2026-10-17` — Dividend coverage 0.51 — the dividend does not exceed remaining time value, or the ex-div date does not land before expiry. This is a carry/theta case, not an early-exercise case, even if a premium is reported above.

---

### Position 7 — `VZ 45C 2026-11-20`

# Option Price Movement Diagnostic Report

**Contract**: `VZ 45C 2026-11-20`  
**Analysis Date**: `2026-09-17` | **Status**: Verified by QuantLib (fdm_local_vol)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (-2588.4%)
* **Model ΔP**: `-$169.9805`
* **Primary drivers**: **Delta PnL** (99%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The move is dominated by the call behaving like stock, so the lower underlying price flowed through almost one-for-one into the option revaluation. Smaller convexity and time decay effects were present, but the diagnostic picture is still a straightforward spot-driven repricing with a very small method residual. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation quality is flagged as not reliable, the IV history is proxied from a prior source, and the IV calibration path hit limitations. The residual is small, but the run still notes a terminal unexplained break and the market-feed constraints mean the diagnosis should stay coarse. No named headline catalyst was retrieved, so there is no validated Layer B mechanism to add.

---

## 2. Observation Lock

* **As-of**: `2026-09-17` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `unquoted`
* **IV move**: -0.01 vol pts vs noise band ±0.00 pts (exceeds noise band)
* **Deep OTM/ITM**: Vega near zero — treat IV moves with caution.
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `-$169.9805`
* **Model vs Mark gap**: `-$169.9805` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `-$170.0698`

* **Method residual (ε_method)**: `+$0.0893` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `+$169.9805` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (0.1%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-15 and/or 2026-09-17, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$168.9998` | +99.4% | Stock moved from $51.45 to $49.76 (-1.6900) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `-$0.0953` | +0.1% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `-$0.0000` | +0.0% | IV moved -0.01 vol pts (0.01% → 0.00%) |
| **Theta decay (Δt · Theta)** | `-$0.9747` | +0.6% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `+$0.0893` | -0.1% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **-$169.9805** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `+$0.0893` (0.1% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0000`
* Combined: `-$0.0000` | Residual after: `-$1.6998`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0000`
* **spot**: `-$1.6998`
* **vol**: `+$0.0000`
* Step sum: `-$1.6998` | Model ΔP: `-$1.6998` | Audit residual: `+$0.0000`

### Ex-div attribution overlay (FO; official PnL stays American FDM Taylor)
* **Spot drop vs dividend**: spot `-$1.6900` vs next cash dividend `+$0.7080` (gap `-$0.9820`)
* **American FDM vs European analytic (no cash div, cross-check)**: `+$4.8673` vs `+$4.5776` (gap `+$0.2897`)
* **Early-exercise premium** (American vs European, same dividend schedule, signed, not floored): `+$0.5006` — material
* **Dividend PV effect** (European, same divs − no divs): `-$0.2109`
* **Dividend coverage** (dividend / time value): `6.60` — early exercise is economically relevant
* **Vol (Taylor Vega PnL)**: `-$0.0000`
* **Residual (Taylor ε)**: `+$0.0009`
* _Overlay only — not a trading edge. LSM/Heston stay diagnostic-only._

### Diagnostic tool summary

* **Tools run** (1/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%
  * `american_dividend_exercise_check` — path_reprice outranks ex-div window
  * `american_dividend_exercise_check` — budget exhausted or lower priority

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Reprice the position on the full model surface and check the delta hedge first, since the contract is acting nearly linearly with spot.
* Treat the early-exercise boundary as live because the dividend does not leave much time value cushion; keep assignment risk in the desk check, even without a separate catalyst tape.
* **Assignment watch**: ex-div `2026-10-09` — Dividend coverage 6.60 (dividend $0.7080 vs time value $0.1073); ex-div is 22d out, expiry 64d out — early exercise is economically relevant.

---

### Position 8 — `PLUG 4C 2026-12-18`

# Option Price Movement Diagnostic Report

**Contract**: `PLUG 4C 2026-12-18`  
**Analysis Date**: `2026-09-17` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Mark MTM PnL**: `+$0.0000` (+0.0%)
* **Model ΔP**: `+$0.0000`
* **Primary drivers**: **Vega PnL** (49%) and **Delta PnL** (31%) and **Theta decay** (17%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter points to a vega-led model reprice, with the option’s value most sensitive to the implied-vol move rather than the modest spot drift. Delta and theta worked in the opposite direction, while gamma added only a small offset; the remaining gap is consistent with higher-order truncation and quote noise rather than a separate market theme. There are no retrieved headlines or named microstructure tokens, so there is no supported Layer B catalyst to overlay. Caveats: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV noise band
* **Confidence**: **Low** — Confidence is low because observation is not reliable, the IV baseline was proxied from historical volatility, and the diagnostic notes flag a high residual with a terminal unexplained break. The catalyst challenge was skipped and no relevant headlines were retrieved, so there is no independent news-based confirmation of the factor story.

---

## 2. Observation Lock

* **As-of**: `2026-09-17` | **Data**: `yfinance` | **IV prev**: `hv20_proxy`
* **Quote tier**: `unquoted`
* **IV move**: -3.02 vol pts vs noise band ±0.00 pts (exceeds noise band)
* **Observation lock**: downgrade factor narratives; prefer gap/residual classification over news.
* **Prior observation**: `2026-09-15`

---

## 3. Mark Reconciliation

* **Mark ΔP (MTM)**: `+$0.0000`
* **Model ΔP (engine)**: `+$0.0000`
* **Model vs Mark gap**: `+$0.0000` (+100.0% of model)
* **Explained ΔP (Taylor ex-residual)**: `+$0.0161`
* **Mark calibration**: active (`diagnostics.mark_calibrated`)

* **Method residual (ε_method)**: `-$0.0161` — arithmetic, not news (ΔP_model minus the Taylor components).
* **Model residual (ε_model)**: `-$0.0000` — ΔP_market − ΔP_model; the only residual a catalyst may explain.
* **Escalation basis**: `method` (236638958.3%)
  Escalation basis: method residual — reliable option marks were unavailable on 2026-09-15 and/or 2026-09-17, so this run explains a model price change, not a market price change.

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities) (% shares use sum-of-|components| because |total PnL| is near zero):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `-$0.2648` | +30.7% | Stock moved from $2.05 to $2.02 (-0.0300) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$0.0083` | +1.0% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$0.4224` | +49.0% | IV moved +2.54 vol pts (53.02% → 50.00%) |
| **Theta decay (Δt · Theta)** | `-$0.1498` | +17.4% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$0.0161` | +1.9% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$0.0000** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$0.0161` (236638958.3% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Second-order Taylor (Layer 3)
* other second-order: `-$0.0000`
* Combined: `-$0.0000` | Residual after: `+$0.0000`

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.0015`
* **spot**: `-$0.0025`
* **vol**: `+$0.0040`
* Step sum: `+$0.0000` | Model ΔP: `+$0.0000` | Audit residual: `+$0.0000`

### Diagnostic tool summary

* **Tools run** (1/3): `reconcile_mark_vs_model`, `quote_quality_and_noise_band`, `taylor_second_order`, `path_reprice`
* **Skipped candidates**:
  * `compare_to_official` — path_reprice selected for severity >10%

---

## 6. Root-Cause Market Intelligence

_No catalyst search — move below materiality / observation lock._


---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: Quote/IV observation lock limits how strongly we can attribute this move to a single Greek. Direction may be OK, but quote quality limits falsifiability; treat factor attribution as indicative. Gaps: Observation lock — quote tier or IV nois
* Recheck the full-surface revaluation and hedge slippage around the spot and vol move; the Greek split is only a reference view when truncation is material.
* No catalyst overlay is supported from the retrieved tape; keep the focus on model/quote quality and the unexplained break rather than forcing a news explanation.

---


## Skew proxy (Task C3.3, SPY risk reversal)

* skew_proxy(t) = +0.0000 | level_proxy(t) = 0.0313
* Δskew = +0.0000 | Δlevel = -0.0017
* Put 715 delta=-0.2262 | Call 795 delta=0.1817
* Nearest-listed-strike approximation of 25-delta, not a fit or a surface -- actual deltas recorded above, not assumed.
