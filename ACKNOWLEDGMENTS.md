# Acknowledgments

## Software

Runtime libraries are listed in `pyproject.toml` / `requirements.txt` (QuantLib,
LangChain / LangGraph, Streamlit, yfinance, pandas, SciPy, and others), each
under its own license.

## Data

- **Historical option chains** — the real-chain fixtures under
  `tests/ci/fixtures/historical/` are small slices of the DoltHub database
  [`post-no-preference/options`](https://www.dolthub.com/repositories/post-no-preference/options),
  licensed **CC BY-SA 4.0**
  (<https://creativecommons.org/licenses/by-sa/4.0/>). **Changes made:** rows
  were filtered to a few tickers and dates, reduced to the columns used here
  (quotes, strike, expiry; the source has no volume or open interest), and
  re-serialised as JSON. Those fixture files remain under CC BY-SA 4.0
  (share-alike); the source code in this repository is MIT (see `LICENSE`).
- **Live quotes and headlines** — fetched at run time through
  [`yfinance`](https://github.com/ranaroussi/yfinance), which reads Yahoo
  Finance. Yahoo's terms allow personal, non-commercial use; this project is a
  research / portfolio demo and does not redistribute that data. The run log
  under `docs/runlog/` contains only derived analytics, not raw quotes.
