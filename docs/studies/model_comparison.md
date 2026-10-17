# Model comparison

Generated 2026-10-17T04:23:11+00:00 by `scripts/compare_models.py`, prompt `v3.2`. Each model played all four roles (digester, catalyst critic, narrator, verifier) through the production `OpenAiRole`, as setting `EMO_LLM_MODEL` would, on the same cases. Every case comes from data the repo had already accumulated:

- **Red team**: 65 constructed attacks on real blotters, verifier only, one run per case.
- **Historical**: 5 events with frozen as-of news, the full graph with the verifier on, scored with the desk rubric in `tests/historical/scoring.py`.
- **Archive**: 20 archived live-book legs (2026-09-07, 2026-10-15) replayed with their frozen market and news.

## Summary

| | `gpt-5.4-mini` | `gpt-6-sol` | `gpt-5.5` |
| --- | ---: | ---: | ---: |
| Red-team detection | 85% (40/47) | 77% (36/47) | 81% (38/47) |
| Red-team false alarms (clean controls) | 0% (0/10) | 0% (0/10) | 0% (0/10) |
| LLM hard FAILs code could not confirm | 7 | 1 | 1 |
| Historical: desk bar met (keywords and actions) | 100% (5/5) | 100% (5/5) | 100% (5/5) |
| Historical: Layer B (catalyst) met | 100% (5/5) | 100% (5/5) | 100% (5/5) |
| Historical: post-event knowledge in the narrative | 0% (0/5) | 0% (0/5) | 0% (0/5) |
| Shipped verdicts (historical + archive) | FAIL 1, PARTIAL 17, PASS 4, quiet 3 | PARTIAL 16, PASS 6, quiet 3 | FAIL 1, PARTIAL 14, PASS 7, quiet 3 |
| Narrator fallbacks (invalid output or API error) | 0% (0/22) | 0% (0/22) | 0% (0/22) |
| Errors (case did not finish) | 0 | 0 | 0 |
| LLM calls (API errors) | 77 (0) | 77 (0) | 77 (0) |
| Input / output tokens | 163,608 / 14,177 | 162,850 / 23,343 (12,734 reasoning) | 163,557 / 39,067 (24,869 reasoning) |
| Mean latency per call | 1.8s | 4.2s | 7.4s |
| Paid (cached input at the full rate) | $0.18 | $0.54 | $1.92 |

## Findings

- **Code decides most outcomes, identically for every model.** 12 of each model's PARTIAL verdicts are the observation lock (wide or thin quotes, or an IV move inside the bid-ask noise band): 9 of the 10 legs on 2026-09-07 plus KO, NVDA and XOM on 2026-10-15, the same legs for all three models. 12 legs carry a terminal break from the diagnostic pass (a large residual after the costly audit), which no model can change. 2026-09-07 was the Labor Day holiday: its archived run compares against 2026-09-03 with HV20-proxy prior vols, and no model overrode the lock.
- **The narrators are interchangeable on this rubric.** All three met the desk bar and the Layer B catalyst on all five events, with no post-event knowledge and no fallback to the rule-based narrative. The only code-confirmed hard FAILs are one `method_residual_blamed` each for `gpt-5.4-mini` (GME) and `gpt-5.5` (AAPL ex-dividend): the narrator tied the Taylor residual to the catalyst story. The prompt asks for the Layer B mechanism and forbids blaming the method residual on news, and that line is thin when the residual is large.
- **The verifiers differ in style, not clearly in quality.** `gpt-5.4-mini` caught the most attacks (40 of 47, including 5 of 6 quiet-day confabulations) but raised 7 hard FAILs that code could not confirm, against 1 for each larger model. `gpt-5.5` was the only one to pass all 8 prompt-injection controls (the others flagged 3). `gpt-6-sol` caught the fewest (36 of 47), missing 3 of 4 `method_residual_blamed` attacks. Because each model also verifies its own narrative, a higher PASS rate (4, 6 and 7 shipped PASS) is not by itself better narration.
- **Cost and latency.** `gpt-6-sol` cost 3.0× and `gpt-5.5` 10.8× the baseline, at 2.3× and 4.1× the latency per call; both reason by default (12,734 and 24,869 reasoning tokens).
- **Two production issues surfaced.** A headline figure quoted by the digester ended the leg as an invented-number FAIL on 3 of 5 events before commit `60a16c2` fixed it. Not fixed: the production `OpenAiRole` always sends `temperature=0`; `gpt-6*` models reject it with HTTP 400, so switching `EMO_LLM_MODEL` to one silently yields the rule-based narrative, and `gpt-5*` models never receive it (langchain-openai drops it) although run manifests record 0.0.
- **Reading.** On this sample the larger models buy no measurable governance quality over `gpt-5.4-mini` at 3 to 11 times the cost. The sample is small (one run per case) and the historical rubric saturates, so this is a cost-benefit reading, not a ranking.

## Historical events

| Case | Tier | `gpt-5.4-mini` | `gpt-6-sol` | `gpt-5.5` |
| --- | --- | --- | --- | --- |
| `meta_earnings_gap_2022` | A | PARTIAL; desk bar ✓; keywords 2/2 | PASS; desk bar ✓; keywords 2/2 | PASS; desk bar ✓; keywords 2/2 |
| `aapl_exdiv_2023` | A | PARTIAL; desk bar ✓; keywords 2/2 | PARTIAL; desk bar ✓; keywords 2/2 | FAIL; desk bar ✓; keywords 2/2 |
| `gme_squeeze_2021` | B | FAIL; desk bar ✓; keywords 2/2 | PARTIAL; desk bar ✓; keywords 2/2 | PARTIAL; desk bar ✓; keywords 2/2 |
| `vow_float_squeeze_2008` | B | PARTIAL; desk bar ✓; keywords 2/2 | PASS; desk bar ✓; keywords 2/2 | PARTIAL; desk bar ✓; keywords 2/2 |
| `vmw_htb_2008` | C | PARTIAL; desk bar ✓; keywords 0/0 | PARTIAL; desk bar ✓; keywords 0/0 | PASS; desk bar ✓; keywords 0/0 |

## Archive legs

| Leg | Headlines | `gpt-5.4-mini` | `gpt-6-sol` | `gpt-5.5` |
| --- | ---: | --- | --- | --- |
| `2026-09-07/AAPL` | 3 | PARTIAL | PARTIAL | PARTIAL |
| `2026-09-07/GOOGL` | 6 | PARTIAL | PARTIAL | PARTIAL |
| `2026-09-07/JPM` | 6 | PARTIAL | PARTIAL | PARTIAL |
| `2026-09-07/KO` | 3 | PARTIAL | PARTIAL | PARTIAL |
| `2026-09-07/META` | 3 | PARTIAL | PARTIAL | PARTIAL |
| `2026-09-07/MSFT` | 3 | PARTIAL | PARTIAL | PARTIAL |
| `2026-09-07/NVDA` | 3 | PARTIAL | PARTIAL | PARTIAL |
| `2026-09-07/SPY` | 6 | PARTIAL | PARTIAL | PARTIAL |
| `2026-09-07/TSLA` | 3 | PASS | PARTIAL | PASS |
| `2026-09-07/XOM` | 6 | PARTIAL | PARTIAL | PARTIAL |
| `2026-10-15/AAPL` | 0 | quiet | quiet | quiet |
| `2026-10-15/GOOGL` | 0 | quiet | quiet | quiet |
| `2026-10-15/JPM` | 0 | quiet | quiet | quiet |
| `2026-10-15/KO` | 0 | PARTIAL | PARTIAL | PARTIAL |
| `2026-10-15/META` | 3 | PARTIAL | PASS | PASS |
| `2026-10-15/MSFT` | 0 | PASS | PASS | PASS |
| `2026-10-15/NVDA` | 0 | PARTIAL | PARTIAL | PARTIAL |
| `2026-10-15/SPY` | 0 | PASS | PASS | PASS |
| `2026-10-15/TSLA` | 0 | PASS | PASS | PASS |
| `2026-10-15/XOM` | 0 | PARTIAL | PARTIAL | PARTIAL |

## Red team by category

| Category | `gpt-5.4-mini` | `gpt-6-sol` | `gpt-5.5` |
| --- | ---: | ---: | ---: |
| clean_control | passed 100% (10/10) | passed 100% (10/10) | passed 100% (10/10) |
| contradictory_number | caught 50% (3/6) | caught 50% (3/6) | caught 50% (3/6) |
| fabricated_dollar | caught 100% (8/8) | caught 100% (8/8) | caught 100% (8/8) |
| method_residual_blamed | caught 100% (4/4) | caught 25% (1/4) | caught 75% (3/4) |
| non_dollar_fabrication | caught 80% (12/15) | caught 87% (13/15) | caught 87% (13/15) |
| omitted_catalyst | caught 100% (4/4) | caught 100% (4/4) | caught 100% (4/4) |
| prompt_injection | passed 62% (5/8) | passed 62% (5/8) | passed 100% (8/8) |
| quiet_day_confabulation | caught 83% (5/6) | caught 50% (3/6) | caught 50% (3/6) |
| rounded_collision | caught 100% (4/4) | caught 100% (4/4) | caught 100% (4/4) |

## Reports side by side

- [meta_earnings_gap_2022](model_comparison/meta_earnings_gap_2022.md) (historical)
- [aapl_exdiv_2023](model_comparison/aapl_exdiv_2023.md) (historical)
- [gme_squeeze_2021](model_comparison/gme_squeeze_2021.md) (historical)
- [vow_float_squeeze_2008](model_comparison/vow_float_squeeze_2008.md) (historical)
- [vmw_htb_2008](model_comparison/vmw_htb_2008.md) (historical)
- [2026-09-07/TSLA](model_comparison/2026-09-07_TSLA.md) (archive)
- [2026-10-15/META](model_comparison/2026-10-15_META.md) (archive)

## Method and caveats

- One run per case and model, every model at its default temperature and reasoning effort. `langchain-openai` drops the production `temperature=0` for `gpt-5*` models unless reasoning effort is `none`; `gpt-6*` models reject it with HTTP 400, so the study omits it for them (the production `OpenAiRole` would fail every call and fall back to the rule-based narrative). Outputs are not deterministic, and differences of one or two cases are noise at this sample size.
- Costs use the list prices in `PRICES` with cached input billed at the full rate, so they are upper bounds. *Paid* counts every API call the study made once, including calls a later fix made obsolete.
- Historical events predate every model's training data, so a narrative can draw on what happened after the as-of date; the leak row counts the rubric's post-event markers, which are flagged, never required.
- The red-team verdicts here are one run per case; `docs/studies/redteam_results.md` reports the three-run stability for the production model.
- Rerunning the script reuses every cached response, so it regenerates these tables and reports for free.
