# Tavily — curated references

App news search on the product `search` node: `src/intel/sources.py` (`TavilyNewsSource`). Uses `TAVILY_API_KEY`. No key → skip, keep Yahoo titles.

App search uses `tavily-python` (`TavilyClient.search`, `topic="news"`).

## Official docs

- Tavily docs home: https://docs.tavily.com/  
  Why: Search params (`topic=news`, `time_range`).
- Search best practices: https://docs.tavily.com/documentation/best-practices/best-practices-search  
  Why: news topic + date filters.
- API key / dashboard: https://app.tavily.com/

## Env vars

```bash
TAVILY_API_KEY=tvly-...
```

Paste into local `.env` only. Never commit the key.

## Fit for this repo

Yahoo ticker titles always; Tavily when the key is set (vega / event cue).

## Related

- Graph conventions: [langgraph.md](langgraph.md)
- Tracing searches in LangSmith: [langsmith.md](langsmith.md)
