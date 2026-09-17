# Live book run log (Task C3)

`book.json`: 8 real, live-discovered contracts (Task C3.1), all opened at
≥35 DTE so none expires inside a 30-day window — no roll policy needed.
Sizing rule is in the file itself (`sizing_rule` field).

`python scripts/daily_run.py` runs the book through the real graph once
per trading day, writes `YYYY-MM-DD/report.md`, and appends one line to
`metrics.jsonl` (schema: see the script's own docstring, matches the spec
verbatim). It also caches each leg's snapshot so the next trading day has
a real t-1 to compare against instead of the `hv20_proxy` fallback.

**Rule, enforced by hand, not by the script:** one entry per real trading
day, committed that day. No backfilling, no simulated days, no generated
entry for a day the script did not actually run. A gap in the log is
honest; a fabricated entry isn't recoverable trust.

Day 1 (2026-09-17) is necessarily noisy — a brand-new position has no
cached t-1, so every leg falls back to the HV20 proxy for `iv_prev`. Read
that day's report header before the numbers; it says so explicitly.

After 20+ real trading days, `docs/studies/runlog_summary.md` will cover:
distribution of daily cost/latency/both residuals, how many days abstained
vs stayed quiet and what they had in common, per-leg narrated-vs-silent
rates, and the skew-proxy time series for the SPY risk reversal. Not
written yet — there aren't 20 days of real entries yet.
