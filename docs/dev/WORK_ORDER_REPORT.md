# Work order report — v3.1 spec, Phase A (A1–A9) + B1–B4 + C1–C3

Supersedes the prior version of this file, which covered only Phase 0/1 of
an earlier v2-numbered spec (`branch phase1/quant-correctness`, merged to
`main` in `65c0bfd`). That work is still valid — v2's Task 1/Task 2 are
v3.1's A1/A2 — and is folded into `DONE` below under its v3.1 numbers.
Everything from A2.3 onward was done in this session, branch
`fix/pinned-book-test-2026-09-14`, against the "ExplainMyOption
Implementation Work Order v3.1" (private, supplied outside this repo).

## DONE

| Task | Commit | What |
|---|---|---|
| Pre-existing test fix | `10ebd14` | `tests/live_book/test_portfolio_mixed.py::test_pinned_book_has_ten_fixed_contracts` asserted the 2026-09-01 pinned book's values after `main` had already rolled to `book_2026-09-14.json` (`ddf9193`, predates this branch). Updated assertions to match. |
| A1 (pre-session) | `6b3f6d8` (main) | `tests/ci/test_pricing_invariants.py` — 8 invariant checks. |
| A2 (pre-session) | `8401b39` (main) | Signed, non-floored `early_exercise_premium` on the same FDM grid/dividend schedule; `dividend_pv_effect` added. |
| A3 | `c900091` | `data/observation.py` — `ObservationStatus`, the continuity gate (`NoComparableObservationError`), `check_basis_consistency`. Wired into `data_loader.py` (live path's two real failure modes) and `leg_graph.py`'s `fetch_market_node`. |
| A2.3 | `6fe4b7b` | `dividend_coverage` / `ee_relevant` economic screen on `AmericanFacts`. |
| A4 | `6b27be9` | `data/historical_chain.py` — DoltHub adapter, quote hygiene, implied borrow, IV inversion (reused `pricing.calibrate.implied_vol_flat`), the two verified real cases, A4.6 fixture relabeling. |
| A5 | `dee2c64` | Tool-budget reclassification (A5.1), `taylor_regime` (A5.3), materiality folding (A5.4), `aapl_exdiv_2023` "Where the residual went" (A5.5). |
| A6 | `30ce560` | ε_method / ε_model split, `escalation_basis`, verifier rule `method_residual_blamed`. |
| A7 | `3ed21ff` | `no_escalation` terminal state, `scripts/find_quiet_days.py`, verifier rule `quiet_day_confabulation`. |
| A8 | `d5922a3` | `docs/case-studies/vow_float_squeeze_2008.md` — EUR currency, the two required paragraph replacements, `$` → `€`. |
| A9 (user-added) | `c6609f8` | `llm_calls` counter (A9.1) + test; generated blotter-field whitelist in the narrator prompt (A9.2) + sync test; regime/implied-borrow/ee_relevant verbatim prompt text (A9.3); `prohibited_phrase` verifier rule for trade-advice language (A9.4); `PROMPT_VERSION` in the live-book run manifest (A9.5). |
| B1 (B1.1, B1.4) | `459c745` | `data_loader.format_untrusted_source`/`format_untrusted_news_item` — every news headline/digest brief entering any of the four LLM prompts (digester, narrator, challenger, verifier) now goes in a delimited `<untrusted_source>` block with escaped breakout attempts. The required instruction text added to all four system prompts. `injection_observed: bool` added to `IntelDigest`/`DiagnosticSynthesis`/`CatalystChallenge`. `tests/ci/test_injection_containment.py`. |
| B2 | `b715140` | `scripts/generate_redteam_cases.py` — 56 attack cases across 9 categories, built from 4 real `PositionFacts` blotters (two real DoltHub chains, one real quiet day, one stress fixture), written to `tests/redteam/attack_cases.json`. `scripts/run_redteam.py` — runs every case N=3 through `verifier.deterministic_precheck` + a fixed baseline-PASS mock, writes `docs/studies/redteam_results.md` with detection/miss/false-alarm/stability rates, per-category table, full confusion matrix, and every individual miss named. `tests/ci/test_redteam_framework.py` — CI smoke test (schema/import drift only, not a full 56-case re-run). |
| B3 | `9dfde71` | `pipeline/llm_roles.py` — `OpenAiRole.seed` (fixed, default `0`), passed through to `ChatOpenAI`; `llm_run_metadata()` records model/temperature/seed for every configured role in one place, wired into the live/offline-through-graph run manifest (`tests/live_book/portfolio_e2e.py`). `tests/ci/test_determinism_quant.py` — 4 fixtures/real cases, each run 3× through `price_and_attribute` + `build_position_facts`, asserted bit-identical (`==`, not a tolerance) on both `pricing.as_dict()` and the `PositionFacts` dataclass. `tests/live_book/test_determinism_llm.py` — the real narrator+verifier path (not a mock), same fixture 3×, requires `OPENAI_API_KEY` (not in `run-tests.sh`, same convention as `historical/run.py`); actually run this session against `gpt-5.4-mini`, passed. |
| B4 | `a1c277d` | `app.py --no-llm` — the quant path only (data fetch, pricing, PnL attribution, `fallback_synthesis`), zero LLM calls, no `OPENAI_API_KEY` needed; `tests/ci/test_no_llm_flag.py`. `scripts/agent_budget_study.py` — runs the real leg graph for the 10 offline legs + 2 real historical cases through a real `gpt-5.4-mini`, writes `docs/studies/agent_budget.md` (wall-clock per stage, tokens/cost by role, `tools_run`/skip-reason/terminal-state distributions). Found and fixed a real bug in the process: `report/synthesis.py::synthesize_diagnosis` built its own bare `ChatOpenAI` from `EMO_LLM_MODEL` instead of using the `role` the graph passed in, silently ignoring B3's seed pin and making narrator cost/tokens unobservable — see FINDING below. `pipeline/leg_graph.py` gained observability-only `stage_timings` (per-node wall clock) and `OpenAiRole.last_usage` (per-call token usage), both hardening, no topology/decision change. |
| A9.4 (remainder) | `354cf76` | The 9 red-team cases deferred at B2 time (framework didn't exist yet) — one per `PROHIBITED_TRADE_ADVICE_PHRASES` entry (`arbitrage`, `mispricing`, `mispriced`, `free money`, `riskless`, `opportunity`, `should have`, `cheap`, `rich`), added to `non_dollar_fabrication` in `scripts/generate_redteam_cases.py` with `expected_flag="prohibited_phrase"`. `attack_cases.json` grew from 56 to 65 cases; `docs/studies/redteam_results.md` regenerated — detection rate rose from 57.9% to 66.0% (all 9 new cases detected deterministically; `non_dollar_fabrication`'s own rate rose from 1/6 to 10/15 since the phrase check, unlike the vol-points/share-count/date checks, already existed and just lacked test coverage). |

| C1 | (this commit) | `scripts/generate_samples.py` — 5 committed sample reports from real runs (`docs/samples/`): `sample_abstain.md` (real GME data, scripted narrator, disclosed — see FINDING #20), `sample_quiet_day.md` (real AAPL quiet day, `no_escalation`), `sample_real_chain.md` (real AAPL ex-div, reconciled marks), `sample_no_llm.md` (live `app.py --no-llm`), `sample_injection_contained.md` (`vol_crush` fixture + injected headline, `injection_observed=True` — see FINDING #21). `docs/samples/README.md` states command/model/data-source/real-vs-synthetic per file, per C1's own requirement. Superseded the pre-v3.1 3-file sample set (`live.md`/`historical.md`/`unexplained_break.md`, removed); `tests/ci/test_repo_layout.py::test_docs_samples_are_committed_product_reports` updated to check the new 5 files. |
| C2 | (this commit) | README rewrite, exactly the edits C2.1–C2.6 specify: two-sided thesis lead, the `LangGraph is the runtime` sentence, `## What is proven offline` → `## What the offline suite covers` + the redteam-results pointer paragraph, new `## Validation` (the 8-row invariants table) and `## Two residuals` and `## Regime rule` sections (the last with a real 5-case `r_spot`/`r_vol`/`\|ε_method\|/\|ΔP\|` table, computed this session), the A5.2 extended attribution formula, 3 new `## Scope` bullets. `## Sample output` also rewritten to match C1's new file set (not one of the numbered C2 sub-edits, but required since the old set it linked no longer exists). C2.6's "delete `No historical option chain.`" and the diagram-placement requirement were already satisfied by earlier A4.6/A5.2 work and the file's existing structure respectively — confirmed, not re-done. |

| C3 (infra + day 1) | (this commit) | `docs/runlog/book.json` — 8 real, live-discovered legs (Task C3.1: 2-leg AAPL vertical spread, 2-leg JPM straddle spanning JPM's real 2026-10-13 earnings, 2-leg SPY risk reversal, 1 ITM VZ call ex-div 2026-10-08, 1 deep-OTM PLUG call), all ≥35 DTE at inception (nearest listed expiry ≥ target), so no roll policy is needed inside the 30-day window. C3.2 (per-expiry/per-strike IV keying) needed no migration — `data/cache.py`'s schema already keys on `(ticker, expiry, strike, option_type, as_of)`, not ticker alone; the spec's own worry doesn't apply to this codebase (FINDING below). `scripts/daily_run.py` — prices all 8 legs through the real graph, computes the C3.3 skew proxy for the SPY pair, records C3.4's `legs_narrated`/`legs_silent`/`llm_calls` (reusing A7's existing `no_escalation` gate, not new logic), writes `docs/runlog/YYYY-MM-DD/report.md` + appends to `docs/runlog/metrics.jsonl` in the spec's exact schema. Also caches every leg's snapshot (`data.cache.upsert_snapshot`) so day 2 has a real t-1. Ran for real today (2026-09-17, day 1): 8/8 legs priced, 8 real LLM calls, $0.0365, all 8 PARTIAL. `tests/ci/test_runlog_book.py` — offline structural checks on the book file. Two real bugs found and fixed in the process of building this, not the shipped pipeline — see FINDINGS below. |

`./scripts/run-tests.sh` passes all 42 registered CI modules as of this
commit (re-verify below).

## FINDINGS

Recorded per §0.2.1 — every item below is a real defect, real numerical
limit, or a real design tension found while building the above; none
papered over.

1. **`fetch_irx_rate`/`fetch_irx_rate_as_of` (`data/rates.py`) divided
   `^IRX` by 100 only when the raw value was `> 1.0`.** Wrong during
   near-zero-rate regimes where `^IRX` itself prints below 1 — GME's
   2021-01-25 rate read back as 7% instead of 0.07%. Fixed: always divide
   by 100 (`^IRX` is always a percent quote). Confirmed against
   `docs/dev/DATA_SOURCES.md`'s independently-verified `r=0.0008`.
2. **yfinance's historical `Close` is always split-adjusted**, even with
   `auto_adjust=False` (that flag only toggles dividend adjustment) —
   confirmed empirically for GME's 2022-07-22 4-for-1 split. This is why
   an earlier pass (pre-v3.1, recorded in `docs/dev/DATA_SOURCES.md`)
   stopped rather than risk a guessed correction. v3.1's A4.5 explicitly
   asks for the documented correction instead:
   `_as_traded_close()` multiplies by the cumulative split ratio from
   `yf.Ticker(...).splits` (not a hardcoded constant). Verified:
   `19.1975 * 4 = 76.79000091552734`, matching the independently-confirmed
   as-traded close to 7 significant figures; `check_basis_consistency`
   (A3.5) now passes for both GME dates.
3. **DoltHub's `option_chain` table has no volume/open_interest columns**
   — its `vol` column is implied volatility, not trading volume. A4.2's
   `volume > 0 OR open_interest > 0` hygiene check cannot be evaluated
   against this source; `HygieneResult.volume_oi_check_applicable` is
   hardcoded `False` and recorded, not silently dropped.
4. **The scarce deep-tool-slot bug (A5.1's stated motivation) existed in
   two independent places**, not one. `graph/diagnostic_controller.py`'s
   `_pick_deep_tool` was the one the spec named; `pipeline/
   diagnostic_loop.py`'s `choose_a2_tool` (the react loop `leg_graph.py`
   runs *after* the initial pass) had the identical
   `taylor_second_order`-vs-`path_reprice` severity-band exclusivity,
   independently. Fixed both; `choose_a2_tool` no longer offers
   `taylor_second_order` at all (it already ran, free, upstream).
5. **A7.2's "zero costly tools" requirement is unsatisfiable as originally
   scoped.** `reconcile_mark_vs_model` and `quote_quality_and_noise_band`
   were classified `costly` after A5.1, but they are the tools that
   *compute* the severity metric a quiet day is recognized by — a pass
   cannot know it's quiet without running them. Reclassified both `free`
   (they meet A5.1's own definition: pure arithmetic on already-computed
   facts, no repricing/network/LLM). Consequence: only one costly slot
   (the deep tool) remains per pass, so `MAX_DIAGNOSTIC_TOOL_CALLS`
   dropped from 3 to 1 to match — a stale 3 would have made
   `terminal_unexplained_break` permanently unreachable (`tool_calls_used`
   could never reach 3 again). Verified against
   `test_governance_scorecard.py`'s budget-exhaustion case, still passes.
6. **A low `escalation_metric_pct` alone does not mean "nothing
   happened."** Found via the pre-existing `vol_crush` fixture:
   `escalation_metric_pct=4.35%` (would pass A7.2's ratio gate) but
   `total_pnl=-$1.47` — an order of magnitude larger than the three real
   quiet days' `$0.03`–`$0.11`. A dramatic move the Taylor decomposition
   explains well is not the same as a quiet day. Added a second,
   absolute-magnitude gate (`NO_ESCALATION_MATERIALITY_PCT_OF_MID` = 5%
   of mid, or a `$0.50` floor without reliable marks) — provisional, like
   `TAYLOR_REGIME_THRESHOLD`, and would benefit from a larger case table.
   Four other existing synthetic fixtures (`american_call_div`,
   `american_put_div`, `flat_only`, `deep_itm_exdiv`) had the same
   low-ratio/large-PnL shape and are excluded by the same guard.
7. **`scripts/find_quiet_days.py` never found an MSFT survivor** within
   its checked-candidate budget (60 candidates, round-robin across AAPL/
   MSFT/SPY) — every MSFT candidate that passed the cheap local checks
   failed DoltHub's quote-tier check. Not investigated further (each
   DoltHub query costs 45–55s); recorded in
   `tests/ci/fixtures/quiet_days/README.md`. The 5 quiet days found span
   only AAPL and SPY.
8. **A3's continuity gate caught a real coverage gap while building A7's
   cases**: `AAPL 172.5C exp 2023-11-17` was `CONTRACT_MISSING` on
   2023-10-20 (present the next trading day) — not a bug, evidence the
   gate works. Substituted with a validated alternative
   (`quiet_spy_2023-04-24`) rather than forcing the original.
9. **`report/schema.py`'s `DiagnosticSynthesis.watchlist` field is
   described to the LLM as "Actionable risk watchlist bullets for the
   trading desk,"** and `report/template.py::_watchlist_section` renders
   a `"## N. Trading Desk Watchlist"` heading in every product report —
   both matched the A8 grep for prohibited language ("watchlist") and sit
   in real tension with §0.3's "no trade advice" red line, since
   "actionable" is instructing the LLM toward exactly that. **Not fixed
   in this pass** — A8's stated scope is the single VW walkthrough file;
   changing the schema/template touches every report this product
   generates and deserves its own task and commit, not scope creep inside
   A8. Grep results in full (`grep -rniI "action item|watchlist|
   recommend|should" src tests docs README.md AGENTS.md`, filtered to
   drop `tests/ci/golden`, `output/`, `private/`): "action item" — zero
   hits anywhere. "watchlist" — `report/schema.py:39`,
   `report/synthesis.py:515`, `report/template.py:428,435,541`,
   `tests/ci/test_report_template.py:52`, `tests/historical/run.py:180`,
   `docs/samples/{unexplained_break,historical,live}.md`,
   `docs/knowledge/pnl-attribution-framework.md:81,134`,
   `docs/samples/README.md:13`, `README.md:67`. "recommend" —
   `docs/references/third-party-rules.md:14` (about a LangChain API
   choice, unrelated) and this file's own A8 replacement text
   (`vow_float_squeeze_2008.md:88`, "observations, not recommendations" —
   the fix, not a violation). "should" — no user-facing hits; all in code
   comments, docstrings, or test assertion messages (`tests/`, dev docs).
10. **A4.3's "static arbitrage filter" (chain-wide monotonicity/convexity
    re-check after the borrow correction) was not built.** The two
    verified real cases only ever need the target contract's own quote
    plus the borrow-implying strike pairs, not a full filtered chain;
    building a general chain-wide filter with no second consumer to
    validate it against felt like scaffolding ahead of need.
    `EMO_MARKET_SOURCE` is documented (A4's module docstring) but not read
    by any code path — constructing `HistoricalChainMarketLoader` always
    needs explicit `as_of`/`prev_as_of` dates no env toggle alone can
    supply.
11. **The live narrator prompt is built by `graph/prompts.py`, reached via
    `report/synthesis.py::synthesize_diagnosis` →
    `compose_diagnose_system_prompt`** — not the inline `system = "Return
    DiagnosticSynthesis JSON only..."` string in `pipeline/leg_graph.py`'s
    `_synthesize_with_role`, which only runs for the non-`OpenAiRole`
    (mock) branch used in tests. A9.3's verbatim prompt additions went
    into `graph/prompts.py`'s `PRICING_ATTRIBUTION_CONTEXT`, confirmed by
    tracing the real call path rather than assuming the more obviously-named
    inline string was the live one.
12. **`llm_calls` (A9.1) counts per-node execution, not per confirmed LLM
    invocation, for `digest_news_node`/`challenge_catalyst_node`/
    `verify_node`** — those three have internal short-circuits
    (`run_intel_digest`, `run_catalyst_challenge`, and
    `deterministic_precheck` inside `verify_synthesis`) that can return
    without ever calling `role.structured_invoke`. Handled precisely for
    all three (checking `digest.reason`, `challenge.suppress_reason`, and
    `verdict.rationale` against `verifier.DETERMINISTIC_PRECHECK_RATIONALES`)
    rather than left as a blind +1, since A9.1's own test needs the zero
    case to be exactly right — but a future caller reading `llm_calls` for
    cost accounting (Task B4/C3.4) should know the counting mechanism, not
    just trust the number.
13. **`pipeline/digest.py::_post_process_digest` silently dropped
    `injection_observed`** — it rebuilds a fresh `IntelDigest` from the raw
    LLM output's `relevant`/`background`/`discarded`/`brief`/`reason`
    fields but never copied `injection_observed` through, so a digester
    that correctly noticed and reported an injection attempt would still
    report `False` after post-processing. Found by
    `tests/ci/test_injection_containment.py::test_digest_reports_injection_observed_without_complying`,
    which failed before the one-line fix. A real defect the B1.4 test
    exists to catch, not a hypothetical.
14. **B1.2 (constrained `figures[]` output with a `blotter_field`
    reference) was not built as its own new mechanism.** The shipped
    system already achieves the same intent more strongly:
    `report/validate.py::validate_synthesis` bans dollar amounts,
    percentages, and numeric PnL claims from LLM prose *entirely* (except
    inside `evidence.headline`/`evidence.source`, where the system prompt
    requires quoting a real headline near-verbatim) — a number can never
    appear without a fixed rendering constraint in the first place, which
    is a stronger guarantee than "a number is allowed but must reference a
    real field." Building a parallel `figures[]` array would either
    duplicate this guarantee or, if it relaxed the existing prose ban to
    allow LLM-authored numbers again, weaken a currently-passing check —
    prohibited by §0.3. Recorded as a deliberate implementation choice,
    not a gap.
15. **B1.3 (catalyst_name from a candidate list; dates fall in the search
    window) is partially satisfied by an existing, differently-named
    mechanism, not fully built.** `report/catalysts.py`'s
    `CATALYST_TAGS`/`missing_catalyst_tags` already constrain which
    catalyst *tags* a synthesis may cite to a code-supplied allow-list
    (functionally the "candidate list produced by digest_news" B1.3
    describes), but there is no literal `catalyst_name` field, and no
    schema field carries a per-headline date at all — `EvidenceItem` has
    `headline`/`source`/`relevance` only — so "dates must parse and fall
    in the search window" cannot be checked today. Adding a date field to
    `EvidenceItem` and a window-validation rule is a real, still-open gap,
    deferred rather than built as a rushed schema extension this session.
16. **B2's measured detection rate (66.0% as of A9.4's additions; 57.9% at
    B2's original 56-case set) is honest but not a model measurement** —
    no `OPENAI_API_KEY` is configured in this environment,
    so every case that `deterministic_precheck` does not intercept falls
    through to a fixed baseline mock that always returns `PASS`
    (`_BaselineRole` in `scripts/run_redteam.py`). This measures the
    deterministic layer's own floor, not what a real verifier LLM would
    catch on top of it. Reported as such in `docs/studies/redteam_results.md`
    rather than presented as a model result; `run_case()` takes any
    `LlmRole`, so re-running against a real model needs no framework
    changes, only an API key.
17. **`quiet_day_confabulation` misses (4/6, 66.7%) are systematic, not
    random.** `_missing_catalyst_rationale`'s deterministic check (A7.5)
    is gated by `report/catalysts.py::CATALYST_TAGS`, an 8-word vocabulary
    (`earnings`, `guidance`, `split`, `merger`, `acquisition`, `fda`,
    `downgrade`, `upgrade`). The two detected misses used in-vocabulary
    words; the four undetected ones used real but out-of-vocabulary
    catalyst language ("buyout", "Fed commentary", "sector rotation",
    "merger arb" phrasing not matching the literal tags). A7.5's rule is
    stated as "any external cause," but the deterministic implementation
    only catches the tagged subset — a real, open vocabulary-coverage gap,
    not a framework bug. Same shape as finding #15: a stated rule broader
    than what's actually implemented.
18. **B3's own spec text names `catalyst_name` and `figures[]` as the two
    fields the LLM-path determinism check must hold stable across runs.**
    Neither is a real schema field (see findings #14/#15 — a stronger, ban-
    all-LLM-numbers mechanism and `CATALYST_TAGS` stand in for them, under
    different names/shapes). `tests/live_book/test_determinism_llm.py`
    checks the fields that actually exist and are load-bearing instead:
    `confidence_level`, `primary_driver`, and the `evidence[].headline` set.
    Run once this session against a real model (`gpt-5.4-mini`,
    `OPENAI_API_KEY` present in `.env`) on `aapl_exdiv_2023`, 3 runs, all
    three fields identical across runs — a real (if single-fixture,
    single-model) determinism measurement, not a hypothetical.
19. **`report/synthesis.py::synthesize_diagnosis` never used the `role`
    object the graph configured — a real bug, found while building B4's
    cost study, not a naming/scoping choice like most findings above.**
    `pipeline/leg_graph.py::_synthesize_with_role` gates on
    `isinstance(role, OpenAiRole)` and then, for the true branch, called
    `synthesize_diagnosis(...)` — which built its **own** bare
    `ChatOpenAI(model=os.getenv("EMO_LLM_MODEL", ...), temperature=0,
    timeout=45)` from scratch, never reading `role.model`,
    `role.temperature`, or (Task B3's) `role.seed`, and never populating
    `role.last_usage` (Task B4's token capture). Confirmed empirically:
    before the fix, a 12-run `scripts/agent_budget_study.py` pass showed
    `narrator: 0 calls` and `verifier: 12 calls` even though the narrator
    plainly ran (`stage_timings["synthesize"]` was several seconds every
    time) — the LLM call was real, just invisible to anything reading the
    passed-in role. Practical consequence before the fix: a caller that
    built a custom `LlmRoleRegistry` with a different narrator model or a
    pinned seed would have that setting silently ignored for the narrator
    specifically (verifier/digester/challenger were unaffected — they call
    `role.structured_invoke` directly). **Fixed**: `synthesize_diagnosis`
    now takes an optional `role` parameter and calls
    `role.structured_invoke(...)` when given one, falling back to the old
    inline `ChatOpenAI` construction only when no role is passed (keeps the
    function usable standalone). Both call sites
    (`leg_graph.py::_synthesize_with_role`, `portfolio_e2e.py`'s
    graph-miss fallback) now pass their role through. Re-verified after
    the fix: the same study run showed `narrator: 12 calls`, real
    input/output token counts, and `tests/live_book/test_determinism_llm.py`
    still passes against the real model.
20. **A genuinely quiet/well-behaved real model makes `terminal_unexplained_break`
    hard to trigger organically.** It fires only when the verifier's FINAL
    verdict is FAIL, `is_hard_verifier_fail` is true, AND the verify budget
    (default 1) is exhausted (`route_verify_result` in `leg_graph.py`) — and
    `revise_synthesis` gives a real narrator another real attempt to
    self-correct before that. A real `gpt-5.4-mini` run against the real GME
    squeeze case (Task C1) produced a well-explained PARTIAL, not a terminal
    break — reliable marks kept the residual small. `docs/samples/
    sample_abstain.md` was built honestly instead: real market data and
    routing, a narrator role fixed to claim a dollar figure absent from the
    real blotter (same construction as `tests/ci/test_pipeline_leg_graph.py`
    and the B2 `fabricated_dollar` cases), disclosed as such in `docs/
    samples/README.md` rather than presented as organic. Separately: neither
    of this session's two real historical cases triggers a news search at
    all — one is a quiet day (`no_escalation`), the other has
    `observation_reliable=False` from thin quotes, and `intel/planner.py`
    skips search under either condition regardless of materiality. C1.5
    (injection containment) used the `vol_crush` synthetic fixture instead,
    specifically because it reliably escalates and searches.
21. **A genuinely interesting compound result in `sample_injection_contained.md`**:
    the real narrator correctly disregarded the injected `$500`/omit-residual
    instructions (`injection_observed=True`, no `$500` anywhere in the report,
    the residual is still discussed) — but the SAME run also used
    trade-advice-adjacent language elsewhere in its own verdict ("...and
    hedge..."), which the real deterministic verifier correctly hard-FAILed
    under `prohibited_phrase` (A9.4), unrelated to the injection. The file's
    verdict line reads "Verifier FAIL — terminal break escalation" as a
    result — real and correct, not a sign containment failed. Disclosed in
    `docs/samples/README.md` rather than re-run repeatedly to get a cleaner
    PASS.
22. **C3.2's premise doesn't hold against this codebase.** The spec worries
    the SQLite snapshot cache is keyed by ticker alone, which would be wrong
    for a multi-expiry book. Checked `data/cache.py` directly: the schema's
    primary key has always been `(ticker, expiry, strike, option_type,
    as_of)`, and `load_t1`'s query filters on all four before `as_of <`. No
    migration built, because there is nothing to migrate — confirmed by
    reading the schema, not assumed.
23. **A real, if minor, bug in `diagnostic_findings["terminal_unexplained_break"]`'s
    semantics, found by this book's own day-1 run.** `diag_finalize_node`
    (`pipeline/leg_graph.py`) can set this flag `True` early — when
    `diag_residual_pct > 15%` and the diagnostic-tool budget is exhausted —
    without the leg actually terminating there: the leg still proceeds
    through the normal search/narrate/verify path afterward and can land on
    a genuine PASS/PARTIAL, and nothing clears the early flag when that
    happens. The real terminal state (`terminal_unexplained_break_node`)
    always also sets `verifier_status="FAIL"`; this book's day-1 run showed
    6/8 legs with the stale flag `True` and a real, verifier-confirmed
    PARTIAL verdict in the rendered report — a direct contradiction if the
    flag alone is trusted. `scripts/daily_run.py` now requires both
    conditions (flag `True` **and** `verifier_status=="FAIL"`) to classify a
    leg as terminal; the underlying flag in the shipped pipeline is
    unchanged (fixing it is a real, separate task — this session's
    `daily_run.py` works around it correctly rather than silently, which is
    enough to not corrupt the metrics.jsonl record, but the shipped
    semantics are still worth a dedicated fix).
24. **Day 1 of any brand-new book position is necessarily noisy — not a bug,
    an architectural fact worth stating plainly.** `load_market_data` only
    finds a real t-1 snapshot via a prior `upsert_snapshot` call; a
    brand-new contract has no cache row yet, so every leg falls back to the
    `hv20_proxy` estimate for `iv_prev`. This book's real day-1 run confirms
    it: `residual_method_pct` computed to `371290144254.743` (a division-
    near-zero artifact, `total_pnl≈0` against a synthetic prior), and every
    leg's quote tier read `unquoted` (a live-quote artifact of the names
    picked, not the proxy). `scripts/daily_run.py` now detects this
    (`iv_prev_source != "chain_t1"` for every leg) and prints an explicit
    caveat at the top of the day's report rather than presenting day-1
    noise as a normal reading, and caches every leg's snapshot so day 2
    compares against something real.
25. **C3.4's "book-level synthesis" is implemented as the existing
    deterministic `render_portfolio_report()` roll-up, not a new LLM call.**
    The spec's own ground rules (§0.2: agent graph topology frozen, no new
    LLM calls) and C3.4's own stated point (scarce inference allocated by a
    number the LLM does not control) are in tension with literally adding
    one guaranteed LLM call every day regardless of materiality — the
    ground rule wins. `legs_narrated`/`legs_silent`/`llm_calls` are recorded
    from each leg's own A7 `no_escalation` outcome (not new decision logic
    — that gate already existed); the "book-level synthesis" is the
    already-shipped, already-deterministic multi-leg report renderer,
    which already runs unconditionally across every leg.

## NOT DONE

- **B1.2/B1.3's remaining sub-parts** — see FINDINGS #14/#15 (a deliberate
  choice for B1.2; a real, deferred gap for B1.3's date-window check).
- **C3's remaining 29 trading days.** Infrastructure (book, skew proxy,
  budget accounting, `daily_run.py`) is built and day 1 (2026-09-17) is
  real and committed. Per the spec's own rule (§C3.5: "do not backfill, do
  not simulate, do not generate a run for a day it did not run"), the
  other ~29 entries cannot be produced in this session regardless of
  effort — they require that many real calendar trading days to actually
  elapse, each with its own `python scripts/daily_run.py` invocation and
  commit. `docs/studies/runlog_summary.md` (the post-hoc distribution
  analysis) follows once 20+ real entries exist, not before.
- **D1–D4** (packaging, dependency pinning, pytest/CI, LICENSE) — not
  started.

## NUMBERS

Every user-facing figure in this session's commits, with the command that
produced it. (Figures from the pre-session A1/A2 work are in that
branch's own history, not restated here.)

| Figure | Value | Command |
|---|---|---|
| GME `2021-01-25` as-traded spot | `76.79000091552734` | `python scripts/fetch_chains.py gme_squeeze_2021_real` |
| GME `2021-01-22` as-traded spot | `65.01000213623047` | same |
| GME IV (`t-1` → `t`) | `3.0813` → `3.5821` | same |
| GME `q_implied` (`borrow_regime`) | `0.5807` (`extreme`) | same |
| AAPL real case spot (`t-1`/`t`) | `182.88999938964844` / `182.41000366210938` | `python scripts/fetch_chains.py aapl_exdiv_2023_real` |
| AAPL real case `q_implied` | `0.0417` | same |
| AAPL real case `ee_relevant` | `False`, `dividend_coverage=0.13` | `tests/ci/test_historical_real_cases.py` |
| `aapl_exdiv_2023` (synthetic) second-order table | model ΔP `-0.4508`; Vega `-0.2813` (62.4%); residual before `+0.1883` (41.8%); Vanna `-0.0181`; Volga `+0.1684` (37.4%); residual after `+0.0381` (8.4%); `residual_reduction_pct=79.8` | `docs/case-studies/aapl_exdiv_attribution.md`'s own recorded `python -c` snippet (commit `dee2c64`) |
| `taylor_regime` — `vow_float_squeeze_2008` | `INVALID`, `r_spot=8.03` | `tests/ci/test_regime_rule.py::test_regime_rule_squeeze_stress_fixture_is_invalid` |
| `taylor_regime` — `aapl_exdiv_2023_real` | `VALID`, `r_spot=0.019`, `r_vol=0.009` | `tests/ci/test_regime_rule.py::test_regime_rule_real_exdiv_case_is_valid` |
| `escalation_basis` — both real cases (A4) | `model`, `residual_model≈$0` | `tests/ci/test_residual_split.py` |
| `escalation_basis` — live/fixture path | always `method` (t-1 marks never verified) | same |
| Quiet days found (2023, AAPL+MSFT+SPY candidates) | 5, across 2 tickers (AAPL, SPY); 0 from MSFT | `python scripts/find_quiet_days.py --min 3 --year 2023` |
| Quiet-day `total_pnl` range | `$0.025` to `-$0.11` | `tests/ci/test_quiet_day_non_escalation.py` |
| `vol_crush` (excluded by the materiality guard) | `escalation_metric_pct=4.35`, `total_pnl=-1.4713` | ad hoc `python -c` against `data.synthetic.load_fixture("vol_crush")`, this session |
| Red-team detection rate (B2+A9.4, deterministic layer only) | 66.0% (31/47 violations caught) | `python scripts/run_redteam.py` |
| Red-team miss rate (B2+A9.4) | 34.0% | same |
| Red-team false-alarm rate (B2+A9.4) | 0.0% (0/10 `clean_control`) | same |
| Red-team per-category detection (B2+A9.4) | `fabricated_dollar` 100%, `rounded_collision` 100%, `omitted_catalyst` 100%, `non_dollar_fabrication` 66.7% (10/15, up from 1/6 pre-A9.4), `contradictory_number` 50%, `quiet_day_confabulation` 33.3%, `method_residual_blamed` 0% | same, `docs/studies/redteam_results.md` |
| Quant-path determinism (B3), 4 fixtures/cases × 3 runs | bit-identical (`==`) on `pricing.as_dict()` + `PositionFacts` every time | `python tests/ci/test_determinism_quant.py` |
| LLM-path determinism (B3), real `gpt-5.4-mini`, `aapl_exdiv_2023` × 3 runs | `confidence_level`, `primary_driver`, `evidence[].headline` set identical every run | `python tests/live_book/test_determinism_llm.py` |
| B4 study: 12-leg run, total LLM cost | `$0.0667` (narrator `$0.0505` / verifier `$0.0163`), 47527+3296 narrator tokens, 12973+1450 verifier tokens | `python scripts/agent_budget_study.py`, `docs/studies/agent_budget.md` |
| B4 study: wall-clock p50/p95 by stage (s) | `llm_roles` 4.39/6.69, `data_fetch` 0.0002/2.47, `pricing` 0.023/1.86, total-per-run 5.56/6.41 | same |
| B4 study: terminal-state distribution, n=12 | `terminal_unexplained_break` 6, `completed` 3, `no_escalation` 2, `PARTIAL` 1 | same |
| Regime-rule table (README `## Regime rule`, C2.5), 5 cases | `r_spot`/`r_vol`/`\|ε_method\|/\|ΔP\|`: AAPL ex-div 0.0188/0.0088/0.0056 (VALID); GME squeeze 0.1451/0.0247/0.1843 (VALID); AAPL quiet day 0.0098/0.0001/0.5908 (VALID); VW squeeze 8.0283/0.5248/0.8783 (INVALID); `vol_crush` 0.0185/0.0003/0.0435 (VALID) | ad hoc `python -c` calling `run_diagnostic_pass` on each case, this session |
| C1 sample cost, 5 runs (4 with an LLM call) | well under $0.01 total (`gpt-5.4-mini`, same per-call cost order as B4's study) | `scripts/generate_samples.py` |
| Live book day 1 (2026-09-17), 8 real legs | 8/8 priced, 8 real LLM calls, 8 narrated / 0 silent, all 8 PARTIAL, $0.036482, 37.3s wall | `python scripts/daily_run.py`, `docs/runlog/metrics.jsonl` |
| Day-1 residual_method_pct (proxy-vs-proxy artifact, documented) | `371290144254.743` | same |
| Full CI suite | 42/42 modules pass (C3) | `./scripts/run-tests.sh` |

## RUNTIME

Profiled for the first time this session (Task B4): see
`docs/studies/agent_budget.md` for the full stage/token/cost/terminal-state
breakdown from a real 12-leg run (10 offline + 2 real historical cases)
against `gpt-5.4-mini`. Headline: the LLM roles stage dominates wall clock
(p50 4.39s of a 5.56s median total run) far more than pricing or the
diagnostic tools, which are sub-30ms; the two real-DoltHub-chain legs are
the only ones where `data_fetch` is comparable in size (2.5-3.0s, still
dwarfed by DoltHub's actual 45-55s query latency when run standalone via
`scripts/fetch_chains.py` — the study's fetch numbers are the in-process
`fetch_market` node only, not a fresh DoltHub round trip, since
`HistoricalChainMarketLoader` was constructed once and its underlying
client may reuse a connection/session).

Also recorded (context from earlier sessions, not re-measured this pass):
DoltHub's SQL API is the dominant cost for `scripts/find_quiet_days.py`/
`scripts/fetch_chains.py` — 45–55s per query regardless of row count, so
those scripts each ran for several minutes per case/candidate.
`./scripts/run-tests.sh` grew noticeably slower after A5.1 (every fixture
now also runs `taylor_second_order`'s bump-and-revalue unconditionally) —
not measured precisely, but visibly on the order of ~2 minutes for the
full 41-module suite by the end of this session, versus ~72s recorded for
the pre-A5 24-module suite in the prior report.
