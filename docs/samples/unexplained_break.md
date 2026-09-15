<!-- Frozen public sample captured 2026-09-14. Suite output/ stays gitignored. -->

_Historical fixture `vow_float_squeeze_2008` (synthetic 2008-10-27 VW squeeze). Diagnostic budget exhausted with a large residual → `terminal_unexplained_break`. Captured 2026-09-14._

# Option Price Movement Diagnostic Report

**Contract**: `VOW.DE 300C 2008-12-19`  
**Analysis Date**: `2008-10-27` | **Status**: Verified by QuantLib (fdm_flat)

---

## 1. Headline

* **Model PnL (no mark)**: `+$706.2085` (+11593.1%)
* **Model ΔP**: `+$706.2085`
* **Primary drivers**: **Gamma PnL** (60%) and **Delta PnL** (7%).
* **Verifier**: PARTIAL — narrative shipped with caveats (reflect applied).
* **Verdict**: Reflect (PARTIAL): The blotter is dominated by gamma: the option behaved like a high-convexity instrument into a very large spot jump, so the Taylor bucket is led by convexity rather than linear delta. Layer B adds an issuer-specific control-structure catalyst: Porsche’s large voting-stake disclosure and the resulting reduced free float support a float and squeeze tape, with borrow stress likely amplifying the move; the large residual is consistent with higher-order truncation on top of that tape. Caveats: The primary driver is correctly identified as gamma, which matches the code. The headline explicitly supports a float-reduction catalyst, and the narrative’s market-structure framing is directionally consistent. However, the independent critic requires both float and squeeze, and the supplied headline only directly names float; squeeze is not clearly evidenced. Per policy, this is a Layer B omission/under-support issue, so PARTIAL is the appropriate verdict rather than FAIL. Gaps: Headline mechanisms include squeeze, but the candidate only explicitly supports float/borrow stress and does not clearly substantiate the squeeze layer from the supplied headline.; Only one news title is provided, so Layer B support is thin even though the dominant gamma driver is consistent.
* **Confidence**: **Medium** — Confidence is medium because the dominant modeled driver is clear and the observation is reliable, but the spot move is extreme and the residual is large, so higher-order terms and market-structure effects matter. The single relevant headline directly supports the float and squeeze mechanisms, which strengthens the catalyst read without replacing the Greek decomposition.

---

## 2. Observation Lock

* **As-of**: `2008-10-27` | **Data**: `synthetic` | **IV prev**: `fixture`
* **Observation lock**: no live quote tier — model-only path.

---

## 3. Mark Reconciliation

* **Model ΔP (engine)**: `+$706.2085`
* **Mark ΔP**: unavailable — no valid marks on both dates.
* **Explained ΔP (Taylor ex-residual)**: `+$1,326.4530`

---

## 4. Quantitative PnL Attribution

Greek-based (Taylor) attribution (official FDM Greeks, T-1 sensitivities):

| Attribution Component | Value ($) | % Share | Quant Driver |
| :--- | ---: | ---: | :--- |
| **Delta PnL (ΔS · Delta)** | `+$145.0401` | +20.5% | Stock moved from $200.00 to $1,005.00 (+805.0000) |
| **Gamma PnL (½(ΔS)² · Gamma)** | `+$1,164.4252` | +164.9% | Convexity from the spot move |
| **Vega PnL (Δσ · Vega)** | `+$17.1675` | +2.4% | IV moved +85.00 vol pts (95.00% → 180.00%) |
| **Theta decay (Δt · Theta)** | `-$0.1799` | -0.0% | Calendar time decay (1 day) |
| **Unexplained residual (ε)** | `-$620.2445` | -87.8% | American EE, skew curvature, dividend discreteness, model gap |
| **Total Model PnL** | **+$706.2085** | **100.0%** | ΔP = P₁ − P₀ (model) |

---

## 5. Residual Drill

* **Taylor residual**: `-$620.2445` (87.8% of |model|)
* **Terminal break**: diagnostic budget exhausted with large unexplained residual/gap — escalate to human review before trading on factor stories.

### Sequential full revaluation (Layer 4, t → S → σ → r)
* **time**: `-$0.1799`
* **spot**: `+$700.7099`
* **vol**: `+$5.6785`
* Step sum: `+$706.2085` | Model ΔP: `+$706.2085` | Audit residual: `-$0.0000`

### Diagnostic tool summary

* **Tools run** (1/3): `path_reprice`
* **Skipped candidates**:
  * `taylor_second_order` — path_reprice selected for severity >20%
  * `compare_to_official` — path_reprice selected for severity >20%

---

## 6. Root-Cause Market Intelligence

_Targeted retrieval for dominant driver: **Gamma**._

_Intel note: The headline is a control-structure story tied directly to Volkswagen, with Porsche SE disclosing a very large voting-stake position and reduced free float. It is relevant as a related-issuer/ownership development for the target name._

_Yahoo `Ticker.news` returns ticker-level titles; the query string is not applied._

1. **Porsche disclosed 74.1% of VW voting stock via shares plus cash-settled options, collapsing free float** _(Source: Porsche SE)_

---

## 7. Trading Desk Watchlist

* **Escalate**: terminal unexplained break — pause model tuning; verify marks and data clock.
* **Verifier reflect**: The primary driver is correctly identified as gamma, which matches the code. The headline explicitly supports a float-reduction catalyst, and the narrative’s market-structure framing is directionally consistent. However, the independent cri
* Reprice on the full surface and review convexity exposure; the size of the spot jump means higher-order effects are material and the Taylor residual should not be treated as noise.
* Watch the float and squeeze setup, including borrow stress and cornered-flow risk, because the headline points to a market-structure catalyst that can overpower ordinary diffusion.
