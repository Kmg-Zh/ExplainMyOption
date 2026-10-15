# Tests

```bash
./scripts/run-tests.sh          # same as: python -m pytest
```

The suite is offline and keyless. `conftest.py` blanks every credential for
each test, so a local `.env` can never turn a test into a paid API call.
LLM roles are scripted (`support.py`); market data comes from committed
fixtures.

| Module | What it pins |
|--------|--------------|
| `test_pricing.py` | Arbitrage and numerical invariants of the official American FDM engine, mark calibration, the analysis tools |
| `test_report.py` | Attribution shares (signed, gross basis only when components offset), residual drill at position size, reconciliation, blotter goldens |
| `test_diagnostics.py` | The deterministic diagnostic pass: tool budget, deep-tool choice, follow-up revaluation, terminal break, regime rule |
| `test_guardrails.py` | What the narrator may say: code checks before the verifier, code confirmation of LLM hard flags, untrusted-text containment, digest and critic |
| `test_pipeline.py` | The LangGraph workflow end to end: routing, coverage gaps, verifier outcomes, book fan-out, CLI, graph topology |
| `test_data.py` | Market-data hygiene, real-chain quote rules, implied borrow, input guards, search planning, news sources |
| `test_historical_cases.py` | The historical events, each pinned to its desk lesson, and the eval's no-lookahead rule |

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
