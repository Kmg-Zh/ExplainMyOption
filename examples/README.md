# Examples

| Example | What it shows | Needs |
|---------|---------------|-------|
| [`governance/`](governance/README.md) | Five scripts where an LLM role misbehaves on purpose, and what code lets through to the report | Nothing: offline, no key |
| [`bring_your_own_pnl.py`](bring_your_own_pnl.py) | The agent on a desk's own PnL explain, with no QuantLib and no yfinance ([docs/INTEGRATION.md](../docs/INTEGRATION.md)) | Nothing; with `OPENAI_API_KEY` the four LLM roles run |
