# Case study: Volkswagen float squeeze (Oct 2008)

**Contract:** `VOW.DE 300C 2008-12-19` (American call)  
**As-of:** 2008-10-27 · **Fixture:** `vow_float_squeeze_2008`  
**Historical context:** Porsche disclosed control over most VW shares; free float collapsed while short interest exceeded float — a classic cornered-market / squeeze setup.

This is a **synthetic benchmark case** in the historical anomaly suite (`tests/historical/historical_test_cases.json`). It is designed to stress the diagnostic workflow when standard Greek attribution breaks down.

---

## Setup

| Field | T−1 | T |
|-------|-----|---|
| Spot | €200 | €1,005 (+402%) |
| IV | 95% | 180% (+85 vol pts) |
| Option marks | unavailable | unavailable |

**Currency:** EUR (stress fixture; the engine is currency agnostic).
**Note:** this fixture compresses a multi-day move into one as-of day. It is a stress
fixture for residual behaviour, not a reproduction of the tape.

- **Moneyness:** Deep ITM after the spot gap (strike 300 vs spot 1,005).
- **Dominant sensitivities:** Large **Gamma** and **Delta** from the spot jump; modest **Vega** from the parallel IV spike.
- **Data mode:** Model-only path (no valid exchange marks on both dates) — the engine reprices from inputs; the blotter still runs.

Regenerate the full report:

```bash
python tests/historical/run.py --case vow_float_squeeze_2008
```

---

## What Taylor explains

Greek-based (Taylor) attribution uses **T−1 FDM Greeks** × observed market moves:

$$\Delta P \approx \Delta \cdot \Delta S + \tfrac{1}{2}\Gamma(\Delta S)^2 + \mathcal{V}\cdot\Delta\sigma + \Theta\cdot\Delta t + \varepsilon$$

For this day:

| Component | Approx. € | Share of \|explained\| |
|-----------|----------:|----------------------:|
| Delta PnL | +€145 | 20% |
| Gamma PnL | +€1,164 | 165% |
| Vega PnL | +€17 | 2% |
| Theta | −€0.2 | ~0% |
| **Taylor sum (ex-residual)** | **+€1,326** | — |
| **Official model ΔP** (engine) | **+€706** | 100% |

Taylor’s **explained** move (+€1,326) is **larger** than the official model repricing (+€706). That mismatch is the signal: a second-order expansion around yesterday’s sensitivities is overstating today’s convexity on a discontinuous, cornered move.

Sequential full revaluation telescopes to the model ΔP by construction, so a zero
residual there is an identity, not a validation. It confirms the engine is
self-consistent; it says nothing about whether the attribution is meaningful. On
this fixture the Taylor expansion is flagged `INVALID` (r_spot = 8.03) and the full
revaluation is the headline attribution.

---

## What the residual means

**Residual (ε): −€620 (~88% of |model ΔP|)** — the Taylor blotter cannot reconcile to the official repricing without a large offset.

In this case, residual is expected and **informative**, not a bug to hide:

1. **Cornered market / liquidity breakdown** — Continuous hedging and smooth spot paths are invalid. A 402% one-day gap is not a small perturbation around T−1 Greeks.
2. **Truncation & cross-Greeks** — Taylor keeps second-order spot convexity but drops higher-order and mixed terms (e.g. vanna) that matter when both spot and vol jump hard.
3. **American early exercise** — Deep ITM calls can carry early-exercise premium; T−1 Greeks on an American FDM grid do not fully capture the repricing path on a discontinuous move.
4. **Bad or missing marks** — Here marks are zero/unavailable; the workflow stays on the model path and flags **mark reconciliation unavailable** rather than inventing a market ΔP.

**Desk reading:** When |ε| is large vs |model ΔP|, treat the Taylor blotter as a **first-pass hedge feedback** (“Delta/Gamma would have implied X”) and escalate **model-gap / microstructure risk** — do not force the narrative to “explain away” the residual.

The diagnostic pass runs `path_reprice` when residual severity exceeds the threshold, surfacing the sequential buckets without replacing the shipped Taylor blotter.

---

## What search added (headline context only)

Search does **not** reprice the option. After the blotter flags a large residual, `plan_search` routes to ticker headlines; frozen benchmark news includes:

- *“VOW float squeeze intensifies as free float collapses in a cornered market setup”*
- *“Buy-in pressure and liquidity breakdown overwhelm continuous hedging assumptions”*

The LLM synthesis ties these headlines to the **cornered market** cue — qualitative context for *why* a second-order expansion around yesterday’s Greeks is the wrong story for a discontinuous move — while all figures remain engine-derived.

**What the run flags (observations, not recommendations):** continuous-hedging
assumptions are inconsistent with the observed gap; marks were unavailable on both
dates; the residual is large enough that the run is reported as unexplained rather
than narrated.

It demonstrates the product goal: **explain, not predict** — honest factor attribution, explicit residual, then targeted narrative.
