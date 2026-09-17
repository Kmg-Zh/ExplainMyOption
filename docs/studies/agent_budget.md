# Agent cost, latency, and terminal-state study (Task B4)

Generated 2026-09-17T04:36:00+00:00 by `scripts/agent_budget_study.py`, run through the real leg graph (`agent_graph.run_pipeline`) for the 10 offline synthetic legs (`tests/live_book/portfolio_book.py::OFFLINE_LEGS`) and the 2 verified real historical cases (real DoltHub chains). Every number below is produced by this run, `n=12` (12 completed, 0 failed).

**Model**: `gpt-5.4-mini`, `temperature=0.0`, fixed `seed=0` (`pipeline.llm_roles.OpenAiRole`, Task B3).

## Wall-clock per stage (seconds)

IV inversion happens inside the `quant` node's `price_and_attribute()` call, not a separate graph node -- not separately measurable without invasive engine instrumentation, folded into `pricing` here.

| Stage | n | p50 | p95 | max |
|---|---:|---:|---:|---:|
| data_fetch | 12 | 0.0002 | 2.4716 | 3.0479 |
| pricing | 12 | 0.0234 | 1.8573 | 1.8668 |
| diagnostic_tools | 12 | 0.0127 | 0.0246 | 0.0248 |
| search | 10 | 0.0000 | 0.0001 | 0.0001 |
| llm_roles | 10 | 4.3850 | 6.6921 | 6.6921 |
| report_render | 12 | 0.0002 | 0.0002 | 0.0002 |
| **total wall (per run)** | 12 | 5.56 | 6.41 | 8.62 |

## Tokens and cost by role (summed across all runs)

| Role | Calls | Input tokens | Output tokens | Cost (USD, see pricing note) |
|---|---:|---:|---:|---:|
| narrator | 12 | 47527 | 3296 | $0.0505 |
| verifier | 12 | 12973 | 1450 | $0.0163 |
| challenger | 0 | 0 | 0 | $0.0000 |
| digester | 0 | 0 | 0 | $0.0000 |
| **total** | | | | **$0.0667** |

Pricing: gpt-5.4-mini standard (non-batch) rate, $0.75/1M input + $4.5/1M output tokens. OpenAI's own pricing page returned HTTP 403 to this session's fetch tool; this rate is from a third-party aggregator (web search, this session), not confirmed against OpenAI's page directly -- the token counts above are exact (from each call's real `usage_metadata`), the $ total is approximate to whatever that page currently says.

## `tools_run` count distribution

| tools_run count | runs |
|---:|---:|
| 1 | 3 |
| 2 | 7 |
| 3 | 1 |
| 4 | 1 |

p50=2.0, p95=3.0, max=4 (budget ceiling is `MAX_DIAGNOSTIC_TOOL_CALLS=1` costly slot per pass, Task A5/A7).

## Skip-reason histogram

| Reason | Count |
|---|---:|
| path_reprice selected for severity >10% | 3 |
| american check outranks model-risk cross-check | 3 |
| mark calibrated and gap small | 2 |
| budget exhausted or lower priority | 1 |

## Terminal-state distribution

| State | Count |
|---|---:|
| terminal_unexplained_break | 6 |
| completed | 3 |
| no_escalation | 2 |
| PARTIAL | 1 |

## Sample size and scope

- 10 offline synthetic legs (one real narrator+verifier call pair each unless a deterministic precheck or no-escalation gate short-circuits first) + 2 real historical cases (real DoltHub chains, 45-55s data-fetch latency each, dominating those two runs' `data_fetch` stage -- see `docs/dev/DATA_SOURCES.md`).
- `n=12` is small; p95 on a 12-sample set is really closer to a max. Treat percentiles here as directional, not a SLA.
- `--no-llm` (this task) is the zero-LLM-cost path for a reviewer without an API key; this study is the other half -- what a real run actually costs.
