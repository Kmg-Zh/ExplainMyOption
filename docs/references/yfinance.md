# yfinance — curated references

Used in MVP by `src/data_loader.py` for spot history, live option chain, and headlines.

## Official / maintainer

- PyPI / README: https://github.com/ranaroussi/yfinance  
  Why: `Ticker.history`, `Ticker.options`, `Ticker.option_chain`, `Ticker.news`.
- Option-chain intro (maintainer): https://aroussi.com/post/download-options-data  
  Why: `calls` / `puts` DataFrames.

## Fit for this repo

| Today | Not in MVP |
|-------|------------|
| Live chain + current `impliedVolatility` | Historical IV surface |
| ATM row nearest spot | OTM-only smile calibration |
| Headlines via `Ticker.news` | Paid options data vendors |

Yahoo chain rows do not include Delta/Vega/Theta — compute in `src/pricing/`.

Project gotchas: [../knowledge/yfinance-iv.md](../knowledge/yfinance-iv.md).
