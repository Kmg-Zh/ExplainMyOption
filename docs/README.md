# docs/

Product notes and curated official-doc links. This folder explains what the app does. It is not a backlog and not a dump of research essays.

## Where things go

| Kind | Put it here | Example |
|------|-------------|---------|
| Official doc **links** + version pins | `references/` | LangGraph StateGraph docs URL |
| Short absorbed coding facts | `knowledge/` | “IV is decimal; Vega per vol point” |
| Case walkthroughs | `case-studies/` | VW 2008 squeeze; AAPL ex-div |
| Frozen product reports | `samples/` | Live / historical / unexplained-break |
| Long excerpts / PDFs (optional) | `references/raw/` (ignored by default) | Saved HTML dumps — prefer links instead |

## Rules of thumb

1. **Do not** paste entire official LangGraph / LangChain manuals into the repo.
2. **Do** keep a short curated link list in `references/` with the version you target.
3. **Do** keep `knowledge/` to facts already in `src/` — units, engine map, attribution identity.
4. **Never** copy notes from here into the diagnose prompt or the product report.

## Are curated links enough?

**Yes for `references/`.** A short index of *which* official pages matter for *this* repo is enough — not a full manual mirror.

Paste full official docs only if you truly need offline copies → `references/raw/` (ignored). Prefer links.

## Starter files

- [../ACKNOWLEDGMENTS.md](../ACKNOWLEDGMENTS.md) — third-party licenses
- [references/README.md](references/README.md) — coverage checklist
- [references/official-docs.md](references/official-docs.md) — LangGraph & LangSmith official URLs
- [references/langgraph.md](references/langgraph.md) — LangGraph / LangChain links
- [references/langsmith.md](references/langsmith.md) — LangSmith tracing
- [references/tavily.md](references/tavily.md) — Tavily app integration
- [references/mcp.md](references/mcp.md) — MCP notes
- [knowledge/README.md](knowledge/README.md) — absorbed facts
- [knowledge/pnl-units.md](knowledge/pnl-units.md) — Vega / IV conventions
- [knowledge/yfinance-iv.md](knowledge/yfinance-iv.md) — live chain + IV fallback
- [references/yfinance.md](references/yfinance.md) — yfinance links
- [references/quantlib.md](references/quantlib.md) — QuantLib links (in-tree `src/pricing/`)
- [samples/README.md](samples/README.md) — frozen product reports
