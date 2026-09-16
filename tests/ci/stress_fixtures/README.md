# Stress fixtures (Task A4.6)

These use hand-chosen spot and implied vol to force specific residual
regimes. They are regression tests for the attribution code. They are not
evidence about any real trading day.

Relabeled out of `tests/ci/fixtures/` so the distinction from a real chain
(`tests/ci/test_historical_chain.py`, `src/explain_my_option/data/historical_chain.py`)
is visible in the repo layout, not just in prose. `load_fixture(name)` and
`list_fixtures()` (`src/explain_my_option/data/synthetic.py`) search both
directories, so every existing call site keeps working unchanged.

Why each one is not convertible to a real chain (A4.5 confirmed only two
cases are: `aapl_exdiv_2023` and `gme_squeeze_2021`, superseded in
production by the real `aapl_exdiv_2023_real` / `gme_squeeze_2021_real`
cases built from `HistoricalChainMarketLoader`):

| Fixture | Why it stays synthetic |
|---|---|
| `vow_float_squeeze_2008.json` | Porsche/VW float squeeze is a Eurex-listed (Frankfurt), pre-2019 event; the DoltHub source is US-listed-only and starts ~2019. No retail source found for Eurex 2008 at any price. |
| `vmw_htb_2008.json` | Pre-2019 (no DoltHub coverage) and VMware was delisted after Broadcom's 2023 acquisition -- yfinance returns nothing for the underlying. |
| `meta_earnings_gap.json` | 2022-02-03 is a dataset-wide missing day in this source -- confirmed 0 rows for AAPL, SPY and TSLA alike on that date, not just META/FB. |
| `aapl_exdiv_2023.json` | Superseded by the real case `aapl_exdiv_2023_real` (A4.5) -- kept as the pre-existing regression fixture for the attribution code, not because real data was unavailable. |
| `gme_squeeze_2021.json` | Superseded by the real case `gme_squeeze_2021_real` (A4.5) -- same reason. |
