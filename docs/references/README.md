# references/ — coverage index

Curated official links for this project. Status = whether a starter page exists here (not whether the feature is coded in `src/`).

| Topic | File | In MVP code? | Notes |
|-------|------|--------------|--------|
| Official doc entry points | [official-docs.md](official-docs.md) | — | LangGraph + LangSmith hub URLs |
| LangGraph + LangChain core | [langgraph.md](langgraph.md) | Yes | `StateGraph`, messages, `ChatOpenAI` |
| LangSmith | [langsmith.md](langsmith.md) | Optional env | Tracing via env vars |
| Tavily | [tavily.md](tavily.md) | Optional env | `TavilyNewsSource` on `search` |
| SEC EDGAR 8-K | [sec-edgar.md](sec-edgar.md) | `EMO_SEC_USER_AGENT` | `SecEdgar8KSource` on `search` (residual cue) |
| MCP | [mcp.md](mcp.md) | No | Optional adapters |
| yfinance | [yfinance.md](yfinance.md) | Yes | Live chain; no historical IV surface |
| QuantLib | [quantlib.md](quantlib.md) | Yes | Facade in `src/pricing/`; American FDM + LSM/Merton analysis API |

## Enough?

**Yes** — short link lists with *why* + env pins.

Not enough if you need offline dumps → `raw/` (ignored). Project conventions (units, engines) live in `../knowledge/`.
