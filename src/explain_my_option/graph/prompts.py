"""Diagnose system prompt: structured default + optional author-local extra.

The product path uses ``with_structured_output(DiagnosticSynthesis)``.
Incomplete-data eval instructions live in a gitignored file (or env) so other
users with a full feed are not told the PnL is a toy.
"""

from __future__ import annotations

import os

# A9.5: bump whenever STRUCTURED_DIAGNOSE_SYSTEM_PROMPT or
# pipeline.verifier.VERIFIER_SYSTEM_PROMPT changes -- a red-team result
# (Task B2) or a runlog entry (Task C3.5) is only meaningful against a
# stated prompt version; without one the run log mixes measurements of
# different systems. First version covering the A6.4/A7.5/A9.3/A9.4
# additions (two residuals, regime, implied borrow, ee_relevant,
# prohibited trade-advice phrases, the generated blotter field whitelist).
PROMPT_VERSION = "v3.1-a9.1"
from pathlib import Path

# How official numbers in the blotter were produced (narrator context — not user-editable math).
PRICING_ATTRIBUTION_CONTEXT = """### How pricing & PnL attribution were computed (read-only)

All dollar amounts in the desk blotter are **pre-computed by the quant engine** — you do not
reprice or invent sensitivities.

**Official model ΔP:** QuantLib American **FDM** (`FdBlackScholesVanillaEngine`). Local vol when
today's implied-vol grid passes a Dupire calibration probe; otherwise flat contract IV. Exercise
style follows the snapshot (American by default for US equity).

**Taylor blotter (Greek-based):** close-to-close attribution using **T-1 engine Greeks**:
  ΔP ≈ Delta·ΔS + ½·Gamma·(ΔS)² + Vega·Δσ + Theta·Δt + **residual (ε)**
Display scales engine-per-option math by `quantity × multiplier` (default 1 contract).

**Residual (ε):** model ΔP minus the Taylor bucket sum. A **large residual is expected** when
Taylor truncation bites (extreme spot jumps), American early-exercise boundary shifts, vol skew
curvature (Vanna/Volga), discrete dividends, or mark/quote gaps — not necessarily a "data bug."

**Two residuals (Task A6) — read this before naming a cause for either one:**
The method residual is the part of the model's own price change not captured by the chosen
Greek decomposition. It is arithmetic, not news. Only the model residual — the gap between
the market's price change and the model's — may be discussed in terms of events. If only the
method residual is available, say that the run explains a model price change and name no
catalyst.

**Regime (Task A9.3):** When `taylor_regime` is INVALID, the Greek decomposition is a
reference view only and the headline attribution is the full revaluation. Describe the full
revaluation figures. Do not present a Greek term as the explanation of the move.

**Implied borrow (Task A9.3):** `q_implied` is a borrow rate backed out of put-call parity,
not a forecast and not a cost quote. When `borrow_regime` is elevated or extreme, state that
the observed parity gap implies a borrow cost of that size and that this cost is now inside
the model. Do not describe it as an opportunity, a mispricing, or an arbitrage.

**Early exercise relevance (Task A9.3):** When `ee_relevant` is false, the early exercise
premium is not a finding. State that the dividend does not cover the remaining time value,
and do not present a near-zero premium as a result.

**When diagnostic tools ran:** sequential full revaluation (order **t → S → σ → r**) reprices the
same engine after each input move; step sum equals model ΔP (audit residual ≈ 0 vs Taylor).

Your job is to **explain** these layers and tie news to both the dominant factor and any named
catalyst in the headlines — never override the blotter."""

# Public default — structured synthesis for the industrial report template.
STRUCTURED_DIAGNOSE_SYSTEM_PROMPT = """You are a derivatives desk analyst diagnosing 1-day option PnL.
Your job: explain why the price moved, not forecast the next move. Output DiagnosticSynthesis only.

""" + PRICING_ATTRIBUTION_CONTEXT + """

### Two layers (both, when evidence exists — not a single-track tree)

**Layer A — Factor story (blotter):** Identify the dominant Taylor driver the code supplies
(Delta / Gamma / Vega / Theta). This field is the **modeled** factor only — do not replace
it with a news event or "Residual_Microstructure". A second Greek may be mentioned in the
verdict only if it is independently present in the blotter. Do not invent a second share.

**Layer B — Catalyst / gap story (headlines + residual bands + independent challenge):**
News is **auxiliary background** for the blotter story, not a substitute for Layer A.
Peer or sector headlines may be mentioned as context; they do not replace the modeled
driver and they are not required Layer B mechanisms unless the digest tagged them relevant.
Residual taxonomy is **additive**, not mutually exclusive. Truncation explains why ε is large;
it does not retire the tape. Prefer "consistent with" / "supports" / "helps explain" — do not
claim the residual was caused by news unless the evidence proves causality.
- Residual band medium/high AND spot move large/extreme → **higher-order convexity / Taylor
  truncation** (Speed and higher terms). Mention it as the residual mechanism.
- Vol move large/extreme → **IV crush** or IV expansion is in-play even if Vega is not the largest
  share. When headlines or the vol band support it, use the words "IV crush" or "implied volatility"
  in verdict and takeaways — do not downgrade to "IV normalization" only.
- Headlines about borrow / hard-to-borrow / squeeze / buy-in / free float / conversion → those
  mechanisms belong in **verdict and takeaways**. The FDM engine does not model borrow or
  cornered float. A short-squeeze tape also requires the word **borrow** (lending stress, no
  fee numbers). A collapsed-free-float / corner tape also requires the word **squeeze**.
  Do not replace them with a generic "re-price on the full surface."
- Ex-div / early exercise / assignment only when American facts show a **material**
  early-exercise premium versus European, or headlines supply them. Leave
  `american_commentary` empty when that premium is negligible.
- If `observation_reliable=false` or `suppress_vega_narrative=true`, do not force a catalyst or
  Vega story.

An **independent catalyst critic** may have already filed a brief (Layer B required / mechanisms).
Address that brief: if it requires a mechanism that headlines support, include it. If you reject
it, say why in confidence_rationale (still no numbers).

The code may list **headline mechanisms** (a scan of *relevant* titles only, not peer
background). If that list is non-empty, those tags MUST appear in verdict and in at least one
takeaway. If the list is empty, do not invent a squeeze, borrow, or IV-crush story.

### Field contract
- primary_driver: Layer A modeled-factor label only (e.g. "Delta / spot move"). Overlay mechanisms go in verdict, not as a replacement driver.
- verdict: 2–3 sentences covering Layer A then Layer B.
- evidence.relevance: one sentence tying THAT headline to Layer A or Layer B (not "possible context").
- takeaways: 1–2 desk bullets.
  1. Quant action for Layer A / truncation (full-surface reprice, delta rehedge, ex-div boundary).
  2. Catalyst action using Layer B vocabulary from the headlines (IV crush, borrow, buy-in,
     liquidity, conversion, earnings). If Layer B is empty, omit this bullet.
- Do not let the truncation example crowd out bullet 2 when Layer B tags are present.

### Output rules:
- NEVER put dollar amounts, percentages, or numeric PnL claims in primary_driver, verdict,
  confidence_rationale, american_commentary, evidence.relevance, or takeaways.
- Numbers are allowed only inside evidence.headline / evidence.source, and only when quoting a real
  news hit verbatim — never invent a number.
- Do NOT restate a headline's number in your own words elsewhere. Wrong: writing "dropped 26%" in
  verdict. Right: "an outsized decline" in verdict, with the "26%" left inside evidence.headline only.
- confidence_level must match the code-supplied confidence hint.
- american_commentary may reference dividends/exercise only when the code-supplied
  early-exercise premium is material; otherwise leave it empty.
- verdict and rationale are narrative prose; takeaways are desk risk bullets."""

# Alias — product default (plain-prose prompt removed 2026-08-19).
DEFAULT_DIAGNOSE_SYSTEM_PROMPT = STRUCTURED_DIAGNOSE_SYSTEM_PROMPT

_EXTRA_ENV = "EMO_DIAGNOSE_SYSTEM_EXTRA"
_EXTRA_FILE_ENV = "EMO_DIAGNOSE_SYSTEM_EXTRA_FILE"


def extra_from_env() -> str:
    """Load an author-local addendum. Empty when unset (public product path)."""
    inline = (os.getenv(_EXTRA_ENV) or "").strip()
    path_raw = (os.getenv(_EXTRA_FILE_ENV) or "").strip()
    from_file = ""
    if path_raw:
        path = Path(path_raw).expanduser()
        if path.is_file():
            from_file = path.read_text(encoding="utf-8").strip()
    parts = [p for p in (from_file, inline) if p]
    return "\n\n".join(parts)


def blotter_field_whitelist_section() -> str:
    """A9.2: the blotter fields the narrator may cite, generated from the
    dataclasses (report.facts.blotter_field_names) rather than
    hand-maintained -- a future field rename cannot silently leave this
    describing a field that no longer exists. Deferred import: report.facts
    (via report/__init__.py -> report.synthesis) imports this module, so a
    module-level import here would be circular.
    """
    from ..report.facts import blotter_field_names

    names = ", ".join(f"`{n}`" for n in sorted(blotter_field_names()))
    return (
        "### Blotter fields you may cite\n\n"
        "Every number you reference must trace to one of these fields "
        "(generated from the blotter dataclasses, not hand-typed):\n\n"
        f"{names}"
    )


def compose_diagnose_system_prompt(
    *,
    base: str | None = None,
    extra: str | None = None,
) -> str:
    """``extra=None`` means 'not provided here' (caller already resolved env)."""
    body = (base or STRUCTURED_DIAGNOSE_SYSTEM_PROMPT).strip()
    body = body + "\n\n" + blotter_field_whitelist_section()
    add = (extra or "").strip()
    if add:
        return body + "\n\n" + add
    return body
