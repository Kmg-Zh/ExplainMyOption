# Option PnL Attribution Framework

**Quick reference** for how we decompose 1-day option PnL. Based on institutional trading desk standards.

**Names and sequential order (t → S → σ → r):** [pnl-attribution-methods.md](pnl-attribution-methods.md). This file is the Taylor identity + residual taxonomy.

---

## Core Equation (Taylor — Greek-based attribution)

```
ΔP ≈ Δ·ΔS + ½Γ·(ΔS)² + Vega·Δσ + Θ·Δt + ε_residual
```

Where:
- **Δ (Delta)**: Per-$1 spot move
- **Γ (Gamma)**: Convexity; ½Γ·(ΔS)² is the "realized convexity gain/loss"
- **Vega**: Per 1 vol point (0.01); e.g., Vega=45 means +$45 if IV rises 1%
- **Θ (Theta)**: Per calendar day decay
- **ε (Residual)**: Unexplained after 2nd-order expansion

**Three pillars** (do not mix):

| Pillar | Meaning |
|--------|---------|
| **Mark / MTM ΔP** | Official book PnL from mids |
| **Model ΔP** | Engine reprice (FDM); factor decomposition |
| **Model vs Mark gap** | Day-over-day change in (model − mark); **not** Taylor ε |

---

## Why This Decomposition Matters

### 1. Validates Investment Thesis
- Did we make money from **our intended bet** (e.g., short vega into earnings)?
- Or did we get lucky from **unmodeled risk** (e.g., American early exercise, stock borrow cost spike)?

### 2. Detects Model Failures
- Large residual → suspect:
  - **Convexity miss** (Gamma dominates; Speed / higher-order terms matter)
  - **Skew curvature** (Vanna / Volga cross-Greeks; "Sticky Delta" vol evolution)
  - **Discrete jumps** (dividend/ex-date boundary crossing; mark age / timestamp mismatch)
  - **Data quality** (bid-ask spread, illiquidity, quote stale)

### 3. Guides Risk Rebalancing
- Delta hedges stale? → Rehedge before next session
- Vega dominant going into earnings? → Lock in profits or hedge volatility
- ITM near ex-div? → Monitor assignment risk; check time value vs dividend

---

## Residual Taxonomy (When Large)

| Signal | Suspect Root Cause | Desk Action |
|--------|-------------------|-------------|
| Large ΔS + high residual | **Gamma / Convexity** miss (Speed, higher-order terms) | Review net gamma exposure; rehedge |
| Large Δσ + high residual | **Skew / Smile curvature** (Vanna / Volga) or sticky-delta assumption wrong | Check curve state; re-estimate vol surface |
| Residual + ex-div ≤30 days | **American boundary** shift or **dividend discreteness** | Verify ex-date schedule; check assignment risk |
| None of above | **Data quality** (mark age, timestamp mismatch, illiquidity) | Verify market source; check bid-ask in data |

---

## Applied: How "Explain My Option" Uses This

### Quantitative Layer (`fetch_market → quant → blotter`)
- Code (QuantLib FDM) outputs exact Delta, Gamma, Vega, Theta.
- **No LLM**, no guessing. Numbers are ground truth.
- Blotter is Markdown table of factor PnL + % share.

### Cue-Driven Search (`plan_search`)
- If **Vega dominant or large** → query "implied volatility earnings event" (Tavily)
- If **Gamma dominant + spot moved > 0.5** → query "earnings gap news event" (Tavily)
- If **Residual large + ex-div ≤30 days** → query "8-K dividend special" (SEC EDGAR)
- Otherwise → ticker headlines only

### Narrative & Risk (`diagnose + report`)
- **Four-step CoT** in prompt:
  1. Identify dominant driver
  2. Classify residual (convexity? skew? American? data?)
  3. Match news to driver
  4. Emit risk watchlist
- **Executive Summary** highlights "Taylor covers X% (residual Y%)" upfront
- **Takeaways** use risk severity labels: warning (Vega, high residual, assignment), metrics (Gamma dynamics, rehedging), calendar (Ex-dividend / corporate actions), process (Reconciliation, mark checks)
- **American section** flags early-exercise risk if ITM + ex-div near

---

## Units & Conventions

| Metric | Unit | Example |
|--------|------|---------|
| **Delta** | Per $1 spot | Δ = 0.65 means +$0.65 if spot +$1 |
| **Gamma** | Per $1² | Γ = 0.008; realized convexity = ½ × 0.008 × (2)² = $0.016 |
| **Vega** | Per 1 vol point | Vega = 45; if IV moves +1% (= +0.01), PnL = +$0.45 |
| **Theta** | Per calendar day | Θ = -0.03 means -$0.03 per day (if nothing else changes) |
| **IV / Spot / Price** | Decimals | IV = 0.25 (25%), Spot = $150.00, Price = $3.50 |

---

## When Residual Is High: The Decision Tree

```
Residual > 5% of |total PnL|?
├─ YES
│  ├─ Spot moved > 1%? + Gamma is dominant driver?
│  │  └─ YES → Gamma term or higher-order miss. Check Vanna/Volga.
│  ├─ IV moved > 2 vol pts? + Vega not the story?
│  │  └─ YES → Skew deformation or surface evolution assumption.
│  ├─ American? + ITM? + ex-div date ≤ 30 days?
│  │  └─ YES → Early-exercise boundary crossed or dividend schedule changed.
│  └─ Otherwise → Mark quality, timestamp async, or illiquidity.
└─ NO → Residual within acceptable band; Taylor explains the move.
```

---

## Institutional Standards We Adopt

### ✅ From Hedge Fund / Prop Desk Practice

1. **Numbers from code, narratives from LLM**
   - Greeks / PnL = deterministic (C++ / QuantLib)
   - "Why did IV move?" = LLM synthesis of news + priors
   - Never invent a Greek or dollar amount in prose

2. **Residual as a diagnostic tool, not a stop**
   - Large residual = "investigate these hypotheses," not "the model is broken"
   - Desk actions are specific: rehedge delta, lock vega, check assignment

3. **Transparency over brevity**
   - Report must show "Taylor covers 85%, residual 15%"
   - Desk decision-maker needs that context upfront

4. **Risk watchlist, not trading advice**
   - "Monitor IV crush if it comes" ≠ "sell now"
   - "ITM near ex-div, check assignment" ≠ "exercise early"

---

## References

- **Internal**: `src/pricing/risk.py` (Greeks calculation); `src/report/facts.py` (attribution row assembly)
- **Primer**: `pnl-units.md` (Greeks unit conventions); `pricing-engine.md` (FDM vs analysis methods)
