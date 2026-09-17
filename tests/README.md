# Tests layout

Three suites under `tests/`. Run the offline parts check with:

```bash
./scripts/run-tests.sh
```

`bootstrap.py` at this level is only import glue (`python tests/.../foo.py`). Not a fourth suite.

| Folder | What it is | Needs network / API key? |
|--------|------------|--------------------------|
| `ci/` | Parts check: engine, graph, report. Fake markets in `ci/fixtures/`, expected blotters in `ci/golden/` | No |
| `live_book/` | Recent real-data book (full diagnosis). Archives in `live_book/output/` (not on GitHub) | Live run yes; `--offline` and archive replay use frozen snapshots; `test_determinism_llm.py` needs `OPENAI_API_KEY` |
| `historical/` | Famous-event fixtures with frozen as-of news | `run.py` needs `OPENAI_API_KEY` |

Retired names (`tests/experiments`, `tests/benchmark_compare`, `tests/historical_benchmark`) must not come back — `ci/test_repo_layout.py` guards that.

## Parts check (`ci/`)

| Module | Covers |
|--------|--------|
| `test_pricing_facade`, `test_lsm_merton`, `test_ladder_regression` | Engine / analysis API |
| `test_data_pipeline`, `test_diagnostic_pass`, `test_report_*` | Data + blotter + 7-section report |
| `test_planner`, `test_intel`, `test_agent_graph` | Materiality / cues, Tavily+SEC ports, graph compile |
| `test_news_digest` | Headline labels (relevant / background / discarded) |
| `test_meta_earnings_gap` | Offline fixture + frozen news (stays in `ci/`; historical suite is live-LLM scoring) |
| `test_pipeline_*` | Book `Send`, residual loop, verifier, topology |
| `test_governance_scorecard` | Offline A1 gates: numeric hallucination, observation/vega lock, missing catalyst, terminal unexplained break, skipped tools |
| `test_exdiv_attribution` | Ex-div FO overlay (spot≈div, EE premium, vol, residual) + tool skip reasons |
| `test_repo_layout` | Paths, no stray root reports |

Governance scorecard fixtures (synthesis JSON, not market snapshots) live in
`tests/ci/fixtures/governance/`. Run the scoreboard with:

```bash
python tests/ci/test_governance_scorecard.py
```

## Historical events

Agent-visible headlines must have `published <= as_of`. Later papers, explainers,
and the JSON `input_text` scenario note are **eval ground truth only** — they are
not fed to the graph.

```bash
./scripts/run-benchmark-live.sh
python tests/historical/run.py
python tests/historical/run.py --case vow_float_squeeze_2008
```

Walkthroughs: [docs/case-studies/README.md](../docs/case-studies/README.md). Frozen product reports (not eval archives): [docs/samples/](../docs/samples/README.md).

## Live book

```bash
./scripts/run-portfolio-e2e.sh
python tests/live_book/portfolio_e2e.py --offline
python tests/live_book/replay_archives.py
python tests/live_book/test_determinism_llm.py  # needs OPENAI_API_KEY
```

Pin: `tests/live_book/pinned_books/book_2026-09-14.json`. Replay uses archived
snapshots + news (no live Yahoo). Presentation notebooks live in `notebooks/`
(committed). Suite `output/` folders are gitignored archives. Hiring/demo captures of the
product report live in [`docs/samples/`](../docs/samples/README.md) — not in `output/`.
