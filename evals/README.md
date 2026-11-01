# Evals

[`tests/`](../tests/README.md) checks that the agent's rules are enforced, with
scripted LLM roles, on every push. The evals here run the agent with **real**
LLM roles and measure what it actually does. They need network and, for the
LLM roles, `OPENAI_API_KEY`. They cost money, and they are not part of pytest
or CI.

## What each eval measures

| Eval | Question | Cases | Command |
|------|----------|-------|---------|
| [`redteam/`](redteam/) | Does the verifier catch a narrative that breaks a rule, and leave clean ones alone? | 65 cases on real blotters: 47 rule-breaking narratives, 10 clean controls, 8 prompt-injection controls | `python scripts/run_redteam.py --live` (without `--live`: the code layer alone, $0) |
| [`historical/`](historical/) | On famous events, does the narrative meet the desk bar using only news published by `as_of`? | 5 events with frozen as-of news ([manifest](historical/historical_test_cases.json)) | `python evals/historical/run.py` |
| [`live_book/`](live_book/) | Does the agent hold up day over day on a pinned real book? | 10 pinned contracts | `python evals/live_book/portfolio_e2e.py --live --compare-to-baseline` |
| Run log | The same, as a public record: a committed report for each trading day it runs | 8 real legs ([`docs/runlog/book.json`](../docs/runlog/book.json)) | `python scripts/daily_run.py` |
| Model comparison | Does a larger model buy better governance? | The red team, the historical events and 20 archived live-book legs | `python scripts/compare_models.py` |
| Playbook replay | Does the terminal-break playbook record reach the Headline verdict? | The 36 archived live-run legs whose diagnostic pass ended in a terminal break, playbook off and on | `python evals/live_book/playbook_replay.py` |

`live_book/` and the run log are the two scheduled jobs (21:00 and 21:15 on
weekdays, [SCHEDULING.md](../docs/dev/SCHEDULING.md)). `portfolio_e2e.py
--offline` and `replay_archives.py` re-run archived days from their frozen
market and news.

## Latest results

Copied from the committed study reports; each line names the run behind it.

- **Red team, live verifier** (`gpt-5.4-mini`, 3 runs per case, 2026-10-05): detection 87.2% (41/47 violations), false alarms 0% (0/10 clean controls). The code layer alone catches 66.0% (31/47) at $0. [Live](../docs/studies/redteam_results.md) · [code only](../docs/studies/redteam_results_deterministic_only.md)
- **Model comparison** (one run per case, 2026-10-17): `gpt-5.4-mini`, `gpt-6-sol` and `gpt-5.5` all met the desk bar on 5/5 historical events, with no post-event knowledge in any narrative. Red-team detection was 85%, 77% and 81%, at $0.18, $0.54 and $1.92. [model_comparison.md](../docs/studies/model_comparison.md)
- **Playbook replay** (`gpt-5.4-mini`, one run per leg, verifier off, 2026-10-29): of 35 archived live-run terminal breaks, the narrator's verdict said the move is not explained or needs human review in 0 with the playbook off and 35 with it on, for at most $0.32 of API calls. [playbook_replay.md](../docs/studies/playbook_replay.md)
- **Cost and latency** (`gpt-5.4-mini`, 12 legs, 2026-09-17): median 5.56 s wall-clock per leg, $0.0667 for all 12. [agent_budget.md](../docs/studies/agent_budget.md)
- **Run log**: since 2026-09-17, a report and a metrics row for each trading day the job ran; a missed day stays a gap, never a backfill. [docs/runlog/](../docs/runlog/README.md)

Walkthroughs of two historical cases: [docs/case-studies/](../docs/case-studies/README.md).

## Rules every eval follows

- Agent-visible headlines are published on or before `as_of`. Later articles,
  papers and a case's `input_text` are ground truth for scoring only and are
  never fed to the graph (`tests/agent/test_historical_cases.py` pins this).
- Pass/fail is the contemporaneous desk bar, not keywords from later papers. A
  live model may still know the event from its weights: naming post-event
  knowledge is flagged as leakage, never required.
- Archives go to gitignored `output/` folders. Committed results live in
  `docs/studies/` and `docs/runlog/`.

## Layout

| Path | Contents |
|------|----------|
| `historical/` | Case manifest, runner, rubric scoring, governed-vs-baseline comparison |
| `live_book/` | Pinned books, the end-to-end runner, archive replay, desk-PnL reconciliation |
| `redteam/` | The attack set, written by `scripts/generate_redteam_cases.py` |
| `bootstrap.py` | Import glue for `python evals/...` and `scripts/` |
| `*/output/`, `output/` | Local run archives (gitignored); the scheduled jobs read `live_book/output/` |
