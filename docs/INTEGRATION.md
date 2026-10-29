# Using the agent with your own PnL system

The product is the governed workflow, not the pricer: a deterministic diagnostic pass, a bounded search plan, four LLM roles, code checks that keep the last word, and a fixed-template report. The bundled QuantLib engine and the yfinance loader are one implementation of two ports. Supply your own and everything else runs unchanged.

A runnable version with no QuantLib or yfinance: [`examples/bring_your_own_pnl.py`](../examples/bring_your_own_pnl.py).

```python
from explain_my_option import ExplainMyOption
from explain_my_option.graph.deps import GraphDeps

agent = ExplainMyOption(deps=GraphDeps(market=YourMarketLoader(), pnl=YourPnlSource()))
result = agent.diagnose_leg(
    "ACME", option_type="call", strike=100.0, expiry="2026-11-20", quantity=10, multiplier=100
)
print(result.report)
```

A book runs the same way, one leg per position: `agent.diagnose_book("book.json")` (format: [`tests/fixtures/books/demo_book.json`](../tests/fixtures/books/demo_book.json)).

## What to copy

Copy `src/explain_my_option/`. With both adapters your own, you can delete the reference engine and loaders:

| Delete | What it is |
| --- | --- |
| everything in `pricing/` except `__init__.py`, `types.py`, `config.py` | the QuantLib engine and its analysis API |
| `data_loader.py`, `data/cache.py`, `data/dividends.py`, `data/historical_chain.py`, `data/rates.py`, `data/realized.py` | the yfinance and historical-chain loaders, the T-1 cache |
| `cli.py` | the CLI and Streamlit UI |

What remains needs `langgraph`, `langchain-core`, `langchain-openai` and `pydantic` (plus `tavily-python` for the Tavily news source). It does not need QuantLib, numpy, scipy, pandas or yfinance. `test_the_agent_runs_with_the_reference_engine_deleted` in [`tests/engineering/test_workflow.py`](../tests/engineering/test_workflow.py) deletes exactly these files and runs the example.

## Conventions

- Every figure is **per one option**. The report scales by `quantity × multiplier`. Those come from the leg (the `diagnose_leg` arguments or the book), as does `exercise_style` (American unless a book leg says otherwise), and they overwrite whatever the loader sets.
- Implied vol is a decimal (`0.28`). Delta is per $1 of spot, vega per vol point (0.01), theta per calendar day.
- The attribution uses **T-1 Greeks**: delta ≈ Δ·ΔS, gamma ≈ ½Γ·ΔS², vega ≈ ν·Δσ/0.01, theta ≈ Θ·Δt.

## Market loader

```python
def load(self, *, ticker, option_type, strike, expiry) -> LoadedData: ...
```

Return `LoadedData(snapshot=MarketSnapshot(...))`. The vol grids `surface` and `surface_prev` are optional; only the reference engine reads them.

| `MarketSnapshot` fields | What they drive |
| --- | --- |
| `ticker`, `option_type`, `strike`, `expiry` | contract identity |
| `spot_prev`, `spot_now`, `iv_prev`, `iv_now` | the market move and its materiality |
| `option_price_prev`, `option_price_now` | your marks (mid); `0.0` when you have none. With marks on both days the headline is mark-to-market and the report has a model residual (mark ΔP − model ΔP), the only residual a catalyst may explain. |
| `time_to_expiry_years`, `risk_free_rate` | the pre-pricing basis check (a call mid above spot stops the leg) and the blotter |
| `as_of`, `prev_as_of` | report dates. A headline published after `as_of` cannot be cited as evidence. |
| `bid`, `ask`, `volume`, `open_interest` | quote tier, IV noise band and the observation lock. With marks but no quote, confidence drops to low (`unquoted`). |
| `quote_tier_prev`, `quote_tier_now` | mark quality: `"reliable"`, `"tight"` or `"normal"`. Reliable marks on both dates make the model residual the escalation basis; otherwise the method residual is. `quote_tier_now` defaults to the tier computed from the quote. |
| `iv_prev_source` | `"chain_t1"` for a real T-1 mark; `"hv20_proxy"` or `"copied"` lowers confidence |
| `discrete_dividends`, `dividend_yield` | the ex-dividend window checks |
| `data_source`, `hv20_now`, `hv20_prev` | display only |

The fields in the first three rows and `time_to_expiry_years` are required; the rest have defaults.

## PnL source

```python
def attribute(self, snapshot, surface_data=None, surface_prev=None) -> PricingResult: ...
```

| `PricingResult` field | Contents |
| --- | --- |
| `greeks_prev`, `greeks_now` | `Greeks(price, delta, gamma, vega, theta)` at T-1 and T; `price` is your model price |
| `pnl` | `PnLAttribution`: `total_pnl` is model ΔP (`greeks_now.price − greeks_prev.price`); then the four buckets; `residual_pnl` is the total minus those four, so fold any other bucket you compute (rho, dividends) into it; `d_spot`; `d_vol` as a decimal |
| `diagnostics` | `PricingDiagnostics(data_source=..., exercise_style=..., engine=...)`, where `engine` names your pricer in the report |
| `surface_diagnostics` | optional; leave `None` |

Optional `PricingDiagnostics` fields:

- `early_exercise_premium`, `american_price`, `european_price`, `dividend_pv_effect`: the early-exercise facts. Without them the blotter has no early-exercise section and any early-exercise commentary is removed. If you pass `discrete_dividends`, supply these too: a dividend inside the window adds an ex-dividend overlay whose price comparison otherwise prints zeros.
- `effective_iv_prev`, `effective_iv_now`, `mark_calibrated`: set these when your PnL used vols other than the snapshot's (for example, calibrated to marks).
- `limitations`: short strings shown in the report. Any entry caps confidence at medium.

Optional attributes on the source itself, used when present:

| Attribute | Unlocks | Without it |
| --- | --- | --- |
| `methodology: str` | one paragraph telling the narrator how your official ΔP is computed | a generic sentence (`GENERIC_METHODOLOGY` in `graph/prompts.py`) |
| `second_order(snapshot, pricing) -> SecondOrderTaylorResult` | vanna and volga terms: the vol half of the regime rule, and the residual drill | skipped with a reason; the regime rule uses the spot ratio only |
| `path_reprice(snapshot, pricing, surface) -> SequentialRevalResult` | the costly audit, a full revaluation along t → S → σ → r | skipped with a reason. A residual or mark gap above 15% is then reported as an unexplained break instead of being audited. |

## Other plug points

| | Contract | Default |
| --- | --- | --- |
| `GraphDeps.intel` | `IntelRegistry({source_id: source})`; a source has `search(query, *, ticker) -> list[NewsItem]` | Yahoo news, Tavily (with `TAVILY_API_KEY`), SEC 8-K (with `EMO_SEC_USER_AGENT`) |
| `GraphDeps.planner` | `plan(snapshot, pricing, *, observation_reliable) -> SearchPlan` | the rule planner, which skips search below materiality or under the observation lock |
| `ExplainMyOption(roles=...)` | `LlmRoleRegistry(narrator=, verifier=, challenger=, digester=)`; a role has `structured_invoke(*, system, human, schema)` | OpenAI through `langchain-openai`; model `EMO_LLM_MODEL`, default `gpt-5.4-mini` |
| `GraphDeps.playbook` | a tuple of `PlaybookRecord(record_id, when, title, guidance)`; `when` names a boolean diagnostic finding, such as `terminal_unexplained_break` or `suppress_vega_narrative` | `DEFAULT_PLAYBOOK`, one record for a terminal break. Add yours with `playbook=(*DEFAULT_PLAYBOOK, record)` |

A playbook record is fixed narrator guidance for a case the diagnostic pass has detected. Code selects it when its finding is true, it goes into that leg's narrator prompt, and the report lists it. It never changes the search, the tools or the routing. Building `GraphDeps` refuses a record with digits, trade or hedge wording, an engine name, an unknown finding or a duplicate id. A record is LLM-facing text, so compare run-log rows only between runs with the same playbook.

The planner's queries name `yfinance_news`, `tavily` or `sec_8k`. Register your feed under one of those ids, or pass `IntelRegistry({})` for no news. Fill `NewsItem.published` so the as-of check can run.

`PipelineConfig(require_openai=False)` lifts the entry gate. A role without credentials then falls back to code-only output, and the verifier returns PARTIAL with the flag `verifier_unavailable`.

To test your adapters before paying for a model, pass scripted roles from `explain_my_option.testing`: `scripted_roles(ScriptedNarrator(verdict=...), ScriptedVerifier("FAIL", ("numeric_hallucination",)))`, `no_llm_roles()` (any LLM call raises), and `frozen_intel(news)` for fixed headlines. It needs none of the reference engine's dependencies. [`examples/governance/`](../examples/governance/README.md) uses them to make each role misbehave on purpose.

## What stays fixed

The workflow, the diagnostic thresholds, the code checks and the report template are the governance. The adapters above are the only seams you should need. If you edit any LLM-facing text, bump `PROMPT_VERSION` in `graph/prompts.py`; run-log rows and red-team results are only comparable within one version.

## Wording that names the reference engine

Your `engine` name replaces the reference engine's in the report header (`Priced by <engine>`) and in the attribution headings. A few sentences still name FDM. Adapt them if they don't hold for your pricer:

- Prompt text (bump `PROMPT_VERSION` after editing): the borrow and float rule in the narrator prompt (`graph/prompts.py`), the borrow takeaway and the catalyst-tag instruction (`report/synthesis.py`), and the critic's bullet (`pipeline/challenger.py`).
- Report text: the early-exercise section (`report/blotter.py`, shown when your source supplies an early-exercise premium) and the ex-dividend overlay (`report/template.py`, shown when a dividend falls inside the window).
