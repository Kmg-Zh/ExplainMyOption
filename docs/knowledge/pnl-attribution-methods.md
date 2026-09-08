# Two ways to split 1-day option PnL

## Takeaway

Do **not** lead with the vendor pair “PnL Predict” / “PnL Explain” — those names sound like forecasting vs storytelling. Say what the math does:

| Use this (product / code / reports) | Means | Residual |
|-------------------------------------|--------|----------|
| **Greek-based (Taylor) attribution** | T-1 Greeks × observed moves | **Expected** (truncation, cross-Greeks, path) |
| **Sequential full revaluation** | Move one market input, **reprice the engine**, repeat | **Zero vs model NPV** (telescoping sum). Not vs mark |

This is **not** FRTB PLA (Hypothetical PnL vs Risk-Theoretical PnL).

## Greek-based (Taylor) — shipped blotter

Close-to-close, order-independent. Official FDM identity (display may name Gamma; engine residual still absorbs American / skew / truncation):

```text
ΔP ≈ Δ·ΔS + ½Γ(ΔS)² + Vega·Δσ + Θ·Δt + ε
```

Use: first-pass blotter, hedge feedback (“did T-1 Delta/Vega earn what they should?”).

## Sequential full revaluation — diagnostic pass

Not Greeks × moves. After each step the **same official engine** is revalued; the dollar change of that step is that factor’s bucket. Sum of steps = model ΔP. Path-dependent: which factor moves **later** absorbs the cross term (e.g. Vanna).

When residual severity is high, `diagnostic_pass` may run this as `path_reprice`. Order:

```text
1. time (calendar / evaluation date)   →  Theta bucket
2. spot                                →  Delta / Gamma (full reprice, not ½Γ(ΔS)²)
3. implied vol (contract / parallel)   →  Vega bucket
4. rate                                →  Rho bucket (if the snapshot has a rate move)
```

Shorthand: **t → S → σ → r**.

Time is not a quote. Advancing the calendar first means later spot/vol shocks are priced on **today’s tenor**. Changing the order reallocates the same total into different buckets.

## Source

- `src/explain_my_option/pricing/risk.py` (Taylor)
- `src/explain_my_option/pricing/sequential_reval.py` (`path_reprice`)
