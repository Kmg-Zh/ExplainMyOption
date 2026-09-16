# Code map — discovery for the v2 work order, Phase 0 (§0.4)

Produced by reading the actual source in this session; every signature below
was read from the file at the stated line, not assumed from its name. This
covers what Phase 1 (Tasks 1–2) touches. It does not attempt to map Phases
2–9, which are not in scope for this pass (see `WORK_ORDER_REPORT.md`).

## QuantLib

- **Version installed**: `1.43` (`.venv/bin/python -c "import QuantLib; print(QuantLib.__version__)"`).
- **Discrete dividends**: passed as a `ql.DividendSchedule` built from a list
  of `ql.FixedDividend(amount, ex_date)`, via
  `_dividend_schedule()` in `src/explain_my_option/pricing/ql_engine.py:57-71`.
  `DividendVanillaOption` is not used anywhere in this repo (it is not on
  the deprecated path the spec asked to check for — the schedule is already
  passed as a constructor argument to the FD engine, not via a separate
  option type).
- **`FdBlackScholesVanillaEngine` construction** —
  `src/explain_my_option/pricing/engines/fdm.py:99-141` (`_attach_engine`):
  ```python
  engine = ql.FdBlackScholesVanillaEngine(
      process,
      dividends,                    # ql.DividendSchedule or None
      int(cfg.t_grid),
      int(cfg.x_grid),
      int(cfg.damping_steps),
      ql.FdmSchemeDesc.Douglas(),
      bool(local_vol),
      float(overwrite),
  )
  ```
  Falls back to the 2-arg `FdBlackScholesVanillaEngine(process, tGrid, xGrid)`
  (silently dropping dividends, flagged as `discrete_dividends_ignored`) if
  the 8-arg overload raises `TypeError` on this QuantLib build — has not been
  observed to trigger on 1.43 in this session, but the fallback path exists
  and is exercised by whatever caused it to be written.
- When a discrete-dividend schedule is present, the continuous dividend
  yield `q` fed into the `BlackScholesMertonProcess` is forced to `0.0`
  (`fdm.py:169`, `fdm.py:297`) so dividends aren't double-counted between
  the discrete schedule and a continuous yield curve.
- **American vs European exercise** is selected per-call by
  `PricingSpec.exercise_style` in `_make_option()`
  (`pricing/engines/fdm.py:90-96`):
  `"european"` → `ql.EuropeanExercise(exp)`, else
  `ql.AmericanExercise(eval_d, exp)`. **This means an FDM European price on
  the identical grid and identical discrete-dividend schedule as the
  American leg is already obtainable** by building a `PricingSpec` with
  `exercise_style="european"` and the same `discrete_dividends` — the fix in
  Task 2 needs no new engine code.

## The pricing facade — `src/explain_my_option/pricing/facade.py`

Single public entrypoint:

```python
def price_and_attribute(
    snapshot: MarketSnapshot,
    surface_data: Optional[VolSurfaceData] = None,
    surface_prev: Optional[VolSurfaceData] = None,
    *,
    config: Optional[EngineConfig] = None,
) -> PricingResult
```

Internal helper `_spec(snapshot, *, spot, vol, eval_date, surface)` builds a
`PricingSpec` that always inherits `snapshot.exercise_style` (i.e. always
`"american"` for this repo's option positions) — Task 2's fix cannot reuse
`_spec()` unmodified for the European legs and instead builds its own
`PricingSpec(..., exercise_style="european", ...)`.

**There is no dedicated "price a European option with a given dividend
schedule" facade entrypoint.** The closest thing,
`ql_engine.price_european_flat(..., discrete_dividends=(...))`
(`ql_engine.py:118-142`), accepts a `discrete_dividends` argument but
**discards it**: `build_bsm_process()` computes a `DividendSchedule` and
returns it as `_divs`, but `price_european_flat` never attaches it to
anything — the `AnalyticEuropeanEngine` it uses only ever consumes the
continuous-yield curve. **This is a second, independent defect**, separate
from the one the spec asked to fix, and is recorded in `FINDINGS`. Task 2
routes around it by using the FDM engine (European exercise style) for both
`P_eu_div` and `P_eu_nodiv`, per spec §2.1's own instruction to use "the
same FDM engine (European exercise, identical grids)".

## Dataclasses (`src/explain_my_option/pricing/types.py`, full file)

```python
@dataclass
class Greeks:
    # price, delta, gamma, vega, theta
    # Delta: per $1 underlying move. Vega: per 1 vol POINT (0.01), i.e.
    #   already the "per vol point" convention from §0.5, not per 1.00 of
    #   vol — enforced in code by "* 0.01" scaling in ql_engine.py:104 and
    #   fdm.py:240 (_vega_bump). Theta: per CALENDAR DAY (theta()/365 or
    #   thetaPerDay()), i.e. already "per day" per §0.5, not per year.

@dataclass
class PnLAttribution:
    # total_pnl, delta_pnl, gamma_pnl, vega_pnl, theta_pnl, residual_pnl,
    # d_spot, d_vol

@dataclass
class DiscreteDividend:
    ex_date: str   # ISO "YYYY-MM-DD"
    amount: float

@dataclass
class MarketSnapshot:
    # ticker, option_type, strike, expiry, spot_now, spot_prev, iv_now,
    # iv_prev, option_price_now, option_price_prev, time_to_expiry_years,
    # risk_free_rate=0.045, dividend_yield=0.0,
    # discrete_dividends: list[DiscreteDividend] = [],
    # exercise_style: "american"|"european" = "american",
    # data_source: "synthetic"|"yfinance" = "yfinance",
    # as_of, prev_as_of, risk_free_rate_prev,
    # iv_prev_source: "fixture"|"chain_t1"|"hv20_proxy"|"copied",
    # hv20_now, hv20_prev, bid, ask, mid, volume, open_interest,
    # risk_free_rate_source: "fixture"|"irx"|"default",
    # quantity=1.0, multiplier=1.0
    def position_scale(self) -> float: ...  # quantity * multiplier

@dataclass
class PricingSpec:
    # spot, strike, rate, dividend_yield, vol, expiry, eval_date,
    # option_type="call", exercise_style="american",
    # discrete_dividends: Sequence[DiscreteDividend] = (), surface=None

@dataclass
class PricingDiagnostics:
    # data_source, exercise_style, engine="fdm_flat", ql_version,
    # iv_prev_source, local_vol_used=False, mark_calibrated=False,
    # effective_iv_now, effective_iv_prev, european_price, american_price,
    # early_exercise_premium, limitations=[]
    # Task 2 adds: dividend_pv_effect (Optional[float]),
    #              ee_premium_anomaly (bool, default False)

@dataclass
class PricingResult:
    # greeks_prev, greeks_now, pnl, diagnostics, surface_diagnostics
```

`DataSource` is currently `Literal["synthetic", "yfinance"]` — adding a
third source later (Phase 2's real historical chains) will need this
`Literal` widened; noted for whoever picks up Phase 2, not touched here.

## The market-data port (relevant to later phases, verified now for the record)

`src/explain_my_option/graph/deps.py:18-38` — the port already exists as two
`typing.Protocol`s, both already swappable via `GraphDeps`:

```python
class MarketLoader(Protocol):
    def load(self, *, ticker, option_type, strike, expiry) -> LoadedData: ...

class PnlSource(Protocol):
    def attribute(self, snapshot, surface_data=None, surface_prev=None) -> PricingResult: ...
```

Two implementations exist today: `YFinanceMarketLoader` (wraps
`data_loader.load_market_data`) and `FixtureMarketLoader` (wraps
`data.synthetic.load_fixture`, used by `fixture_deps(name)` for the offline
product path). **This means Task 2.0 from the spec (extracting a port) is
already done** — a future historical-chain data source only needs a third
`MarketLoader` implementation returning `LoadedData`, wired via
`GraphDeps(market=...)`. No `as_of`/`t-1` "historical chain" source exists
yet anywhere in the repo — confirmed by grep; `data_source` only ever takes
the values `"synthetic"` or `"yfinance"`.

## Early exercise premium — the actual defect (facade.py:279-314)

There is no standalone `american_dividend_exercise_check`-style pricing
function; the computation is inline in `price_and_attribute`:

```python
eu_g = price_european_flat(
    spot=snapshot.spot_now, strike=snapshot.strike, rate=snapshot.risk_free_rate,
    dividend_yield=snapshot.dividend_yield, vol=iv_now, expiry=snapshot.expiry,
    eval_date=as_of, option_type=snapshot.option_type,
    discrete_dividends=(),                      # <- no dividends, and inert anyway (see above)
)
eu_price = eu_g.price
...
am_flat = ...                                   # American FDM WITH snapshot.discrete_dividends
ee_prem = max(0.0, am_flat - eu_price)           # <- floored, wrong comparator
```

`am_flat` (American, with the real discrete cash dividend) is compared
against a European price computed with **no dividends at all**, not the
"European with the same schedule" the spec (and basic put-call-parity
reasoning) requires. Because a cash dividend lowers the American price
relative to a no-dividend European, the raw difference is frequently
negative, and `max(0.0, ...)` reports **$0** even when a real early-exercise
premium exists — exactly what `aapl_exdiv_2023` and `deep_itm_exdiv` show
today per `docs/case-studies/aapl_exdiv_attribution.md`.

`graph/diagnostic_tools.american_dividend_exercise_check()`
(`diagnostic_tools.py:92-118`) is a read-only wrapper around
`report/facts.py::_american_facts()` — it does not compute its own premium,
it surfaces whatever `diag.early_exercise_premium` already holds. Same for
`graph/diagnostic_tools.ex_div_attribution_split()`
(`diagnostic_tools.py:124-161`), which additionally exposes
`pricing.diagnostics.european_price` under the (accurately named) key
`"european_analytic_no_div"`.

### Everything that reads `early_exercise_premium` (exhaustive, via repo-wide grep)

- `pricing/types.py:174` — the field itself.
- `graph/diagnostic_tools.py:114,135,153-154` — `american_dividend_exercise_check`,
  `ex_div_attribution_split`, `_EE_MATERIAL_USD = 0.01` threshold.
- `report/facts.py:32,219,242` — `AmericanFacts.early_exercise_premium`,
  and the "is it negligible" text branch at line 219
  (`diag.early_exercise_premium < 0.01`).
- `report/synthesis.py:224-258` — `_EE_MATERIAL_USD = 0.01`,
  `ee_premium_material()` (`prem >= 0.01`), `apply_american_commentary_policy()`
  (suppresses/emits the "early exercise" narrative sentence).
- `report/template.py:178-187` — renders the "Ex-div attribution overlay"
  Markdown block, currently labelled
  `"Early-exercise premium (floored at 0 in diagnostics)"`.
- `report_generator.py:178-185` — renders the "### Early exercise" block in
  the plain quant report.
- `graph/prompts.py:69,93,99` — narrator/verifier prompt text referencing
  `american_commentary` materiality (frozen per §0.1 — not touched).

## Where `as_of` / T-1 snapshots come from today

- **Live**: `data_loader.load_market_data()` — pulls `yfinance` history for
  spot, `tk.option_chain(...)` for the chain, `data/dividends.py::project_dividends()`
  for a best-effort ≤2-entry discrete dividend projection, `data/rates.py::fetch_irx_rate()`
  (`^IRX`) for the risk-free rate. `iv_prev` here is the live path this spec's
  Task 11 is about — either a cached SQLite mark or an HV20 proxy; no real
  historical option-chain source exists.
- **Fixture (synthetic)**: `data/synthetic.py::load_fixture(name)` reads
  `tests/ci/fixtures/{name}.json`, validated against
  `_REQUIRED_SNAPSHOT_KEYS`; forces `data_source="synthetic"`. This is what
  every stress fixture (`gme_squeeze_2021`, `vow_float_squeeze_2008`,
  `aapl_exdiv_2023`, `deep_itm_exdiv`, etc.) uses — hand-chosen spot/IV, not
  a real quoted chain.
- **Historical (real chain)**: does not exist yet anywhere in this repo —
  confirmed by grep across `src/` and `tests/`. This is Phase 2 of the v2
  spec, out of scope for this pass.

## Repo guardrails relevant to where new files can go

- `paths.py`: `ROOT_MARKDOWN_ALLOWLIST = {"README.md", "AGENTS.md", "ACKNOWLEDGMENTS.md"}`
  — no other root-level `.md` is permitted; hence this file lives under
  `docs/dev/`.
- `tests/ci/test_repo_layout.py::test_no_stray_report_markdown_in_repo_root`
  enforces the above at test time.
- CI tests run as plain scripts (`python tests/ci/test_x.py`) via
  `scripts/run-tests.sh`'s hardcoded `TESTS` array — not pytest. New test
  modules must be added to that array to run in CI.
