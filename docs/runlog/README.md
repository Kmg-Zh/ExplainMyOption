# Live book run log

`book.json`: 8 real, live-discovered contracts, all opened at
≥35 DTE so none expires inside a 30-day window — no roll policy needed.
Sizing rule is in the file itself (`sizing_rule` field).

`python scripts/daily_run.py` runs the book through the real graph once
per trading day, writes `YYYY-MM-DD/report.md`, and appends one line to
`metrics.jsonl` (schema: see the script). It also caches each leg's snapshot so the next trading day has
a real t-1 to compare against instead of the `hv20_proxy` fallback.

**Rule, enforced by hand, not by the script:** one entry per real trading
day, committed that day. No backfilling, no simulated days, no generated
entry for a day the script did not actually run. A gap in the log is
honest; a fabricated entry isn't recoverable trust.

Day 1 (2026-09-17) is necessarily noisy — a brand-new position has no
cached t-1, so every leg falls back to the HV20 proxy for `iv_prev`. Read
that day's report header before the numbers; it says so explicitly.

**Prompt version.** Each `metrics.jsonl` line records `prompt_version`
(`explain_my_option.graph.prompts.PROMPT_VERSION`) — bumped whenever the
narrator or verifier system prompt changes, so a behavior shift partway
through the log (fewer/more `terminal_unexplained_break`s, say) is legible
as "the prompt changed here," not a silent discontinuity. **The field
itself was only added on 2026-09-27** (after the 09-17 through 09-25
entries were already written); those seven rows predate it and don't have
it, all under what was `v3.1-b1.1`. From 2026-09-27 on, every row has it.

Two verifier prompt fixes landed this way, both found by reading the real
`terminal_unexplained_break` rationale text in this log, not by inspection
alone: `v3.1-b1.2` stopped the verifier hard-failing correct model-language
("higher-order effects", "path effects") as `method_residual_blamed`
(which caused 2 of the first 4 escalations in this log); `v3.1-b1.3`
narrowed `prohibited_phrase` to the literal trade-advice word list instead of any
hedge-adjacent phrasing (which caused a 3rd). `v3.1-b1.4` (2026-10-05) changed the verifier's *decision logic*, not only
its wording: a hard LLM FAIL (numeric / prohibited phrase / quiet-day /
method-residual) now stays a FAIL only if a deterministic code check
reproduces the violation; otherwise it is downgraded to PARTIAL
(`unconfirmed_hard_flag`), so escalate-or-not is decided by code. Hedge or
sizing directives are a soft `hedge_advice` PARTIAL, and cited evidence must
be a supplied headline published on or before `as_of` (`evidence_provenance`).
From this version each row also records `verifier_downgraded` (legs where the
LLM said FAIL and code overruled it) and `residual_pct_excluded_legs`
(legs whose |total PnL| was too small to give a meaningful percent;
`residual_method_pct` is now the median over the rest), and each day writes
`audit.json` (per leg: candidate synthesis, every verifier verdict, terminal
cause) so any escalation can be explained afterwards.

`v3.2` (2026-10-15) is a cleanup release with no change to the verdict
logic. Four things change in later rows. (1) The narrator's desk packet and
the report give attribution shares the sign of their dollar amount, and use
gross movement as the base only when the components largely offset.
(2) Ticket tags are gone from the prompt text. (3) Quiet days no longer run
a costly follow-up revaluation. (4) `verifier_downgraded` is now counted from
`audit.json`'s verifier trace. Before v3.2 it read a key the pipeline never
returned, so every row logged 0. The 2026-10-05 to 10-14 audit files record
3 downgrades in 58 verifier verdicts.

`v3.3` (2026-10-29) adds playbook records: fixed narrator guidance that code
selects from the diagnostic findings (`graph/playbook.py`). The first one tells
the narrator that a diagnostic-pass terminal break must show in the verdict.
The verdict logic is unchanged. The report and `audit.json` list the records a
leg got (`playbook_records`).

### Stale spot, 2026-09-17 to 2026-11-04

The live loader took "the last two valid daily closes" as spot. At 21:15 ET
Yahoo usually lists the session's daily bar with no close yet, so the run
paired that session's option marks with the previous session's spot move.
Checked against published closes, 167 of the 246 cached leg-days in this
window carry the previous session's close, and 26 of the 33 days have at
least one such leg. On those legs the mark PnL is right (the option quotes are
the session's own), but the Greek attribution is not, and neither is any
narrative built on it: mark calibration put the wrong day's spot move into
vega. The clearest case is 2026-11-04: AAPL closed +5.3% (331.90 → 349.51), the
report used −1.9% (338.32 → 331.90), the 325C escalated on a 482% mark gap,
and the 350C was narrated as a +31 vol pt "volatility shock". With the session
closes its vol moved −0.3 pts and delta plus gamma explain 95% of the move.

Since the data-check fix (after the 2026-11-04 run) spot is dated to the
quotes, and a mark that fails its
no-arbitrage bounds or calibrates far from the quote source's IV ends the leg
as a data break ([README](../../README.md#data-checks)). The 33 entries above
stay as they were written.

Days before the relevant fix landed keep their real outcome, including any
escalation that fix would have prevented; the incident write-ups are in
[`docs/archive/WORK_ORDER_REPORT.md`](../archive/WORK_ORDER_REPORT.md).
Nothing is backfilled or rewritten.

After 20+ real trading days, `docs/studies/runlog_summary.md` will cover:
distribution of daily cost/latency/both residuals, how many days abstained
vs stayed quiet and what they had in common, per-leg narrated-vs-silent
rates, and the skew-proxy time series for the SPY risk reversal. Not
written yet — there aren't 20 days of real entries yet.
