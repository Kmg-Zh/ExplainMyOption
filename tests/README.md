# Tests

```bash
./scripts/run-tests.sh          # same as: python -m pytest
```

The suite is offline and keyless. `conftest.py` blanks every credential for
each test, so a local `.env` can never turn a test into a paid API call.
LLM roles are scripted (`support.py`); market data comes from committed
fixtures.

Two suites, one per folder. Which one a test belongs to depends on what it
protects, not on whether an LLM appears in it:

- `engineering/`: the code computes and wires correctly.
- `agent/`: the agent's rules: what an LLM role may say, which tools it may
  spend, when the run must stop and hand over to a person. The LLM roles are
  scripted, so each rule is checked deterministically.

```bash
pytest tests/agent              # one suite (or: pytest -m agent)
```

`conftest.py` marks each test by its folder and refuses a test outside both,
since CI runs the two folders as separate steps.

| Suite | Module | What it pins |
|-------|--------|--------------|
| engineering | `test_pricing.py` | Arbitrage and numerical invariants of the official American FDM engine, mark calibration, the analysis tools |
| engineering | `test_report.py` | Attribution shares (signed, gross basis only when components offset), residual drill at position size, reconciliation, blotter goldens |
| engineering | `test_market_data.py` | Market-data hygiene, real-chain quote rules, implied borrow, input guards, news sources |
| engineering | `test_workflow.py` | The graph as software: an end-to-end leg, input guards, book fan-out, CLI, topology, the desk-PnL example with the engine deleted |
| agent | `test_guardrails.py` | What the narrator may say: code checks before the verifier, code confirmation of LLM hard flags, untrusted-text containment, digest and critic |
| agent | `test_governed_runs.py` | Full legs through the graph: verifier outcomes, invented figures, required catalysts, coverage gaps |
| agent | `test_tool_budget.py` | The deterministic diagnostic pass: tool budget, deep-tool choice, follow-up revaluation, terminal break, regime rule |
| agent | `test_search_policy.py` | Search only material, reliably observed moves, with a bounded query plan |
| agent | `test_historical_cases.py` | The historical events, each pinned to its desk lesson, and the eval's no-lookahead rule |

Blotter goldens live in `fixtures/golden/`; regenerate them after an
intended blotter change with `EMO_UPDATE_GOLDEN=1 ./scripts/run-tests.sh -k golden`.

## Fixtures

| Folder | Contents |
|--------|----------|
| `fixtures/` | Synthetic market snapshots (also the CLI's `--fixture` names) |
| `fixtures/stress/` | Hand-chosen spot/IV that force a residual regime ([README](fixtures/stress/README.md)) |
| `fixtures/historical/` | Real-chain slices from DoltHub, quotes on both days ([README](fixtures/historical/README.md)) |
| `fixtures/quiet_days/` | The deterministic quiet-day selection ([README](fixtures/quiet_days/README.md)) |
| `fixtures/books/` | A demo multi-leg book |
| `fixtures/golden/` | Expected blotter Markdown |

## Evaluation harnesses (not part of pytest)

These run the product against live or archived data and need network and,
for the LLM roles, `OPENAI_API_KEY`. Their `output/` folders are gitignored.

| Folder | What | Command |
|--------|------|---------|
| `historical/` | The historical events with frozen as-of news, scored against a rubric | `python tests/historical/run.py` |
| `live_book/` | The pinned live book; the 21:00 scheduled job runs it daily | `python tests/live_book/portfolio_e2e.py --offline` |
| `redteam/` | The constructed attack set behind `docs/studies/redteam_results.md` | `python scripts/run_redteam.py` |

Agent-visible headlines in the historical eval are published on or before
`as_of`; later articles, papers and the case's `input_text` are ground truth
for scoring only and are never fed to the graph.
