# LangSmith — curated references

Observability / tracing for LangChain & LangGraph runs. This repo does **not** require LangSmith to run; enable it when you want traces in the UI.

`langsmith` is typically pulled in transitively via `langchain-core` / `langchain-openai`. You usually only need env vars — not extra app code — for basic tracing of LangGraph + `ChatOpenAI`.

## Official docs (start here)

- **LangSmith docs (hub):** https://docs.smith.langchain.com/
- Observability quickstart: https://docs.langchain.com/langsmith/observability-quickstart  
  Why: fastest path to see traces.
- Trace with LangChain: https://docs.langchain.com/langsmith/trace-with-langchain  
  Why: env-var setup for LC / LG apps (what this project is).
- Trace with LangGraph: https://docs.langchain.com/langsmith/trace-with-langgraph  
  Why: graph-specific tracing notes.
- Log traces to a project: https://docs.langchain.com/langsmith/log-traces-to-project  
  Why: isolate this app’s runs under `LANGSMITH_PROJECT`.
- Create account / API key: https://docs.langchain.com/langsmith/create-account-api-key  
  Why: get `LANGSMITH_API_KEY`.
- Hub / app: https://smith.langchain.com/

## Env vars for this project (optional)

Put in `.env` (never commit secrets):

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_pt_...
LANGSMITH_PROJECT=explain-my-option   # optional; defaults to "default"
# LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com  # only if non-US region
```

Older docs may show `LANGCHAIN_TRACING_V2` / `LANGCHAIN_API_KEY`; prefer the `LANGSMITH_*` names above.

## What belongs elsewhere

| Content | Location |
|---------|----------|
| “How we debug a bad diagnose node with traces” | `docs/knowledge/` |
| Full page dumps | `docs/references/raw/` |

## Related

- LangGraph / LangChain links: [langgraph.md](langgraph.md)
