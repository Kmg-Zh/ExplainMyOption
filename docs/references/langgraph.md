# LangGraph / LangChain — curated references

Pin versions to what this repo actually uses (`requirements.txt`). Update links when you bump deps.

## Versions (from requirements)

- `langgraph>=0.2.0`
- `langchain-openai>=0.2.0`
- `langchain-core>=0.3.0`

## Official docs (start here)

- LangGraph overview: https://langchain-ai.github.io/langgraph/  
  Why: top-level concepts for this repo’s graph.
- Graph API / `StateGraph`: https://langchain-ai.github.io/langgraph/concepts/low_level/  
  Why: nodes, edges, state — matches `src/agent_graph.py`.
- LangChain Core messages / runnables: https://python.langchain.com/docs/concepts/  
  Why: `SystemMessage` / `HumanMessage` in `diagnose_node`.
- `ChatOpenAI` (langchain-openai): https://python.langchain.com/docs/integrations/chat/openai/  
  Why: LLM backend when `OPENAI_API_KEY` is set.

## Post-MVP (when you invoke Academy / HITL skills)

- `Command` (route + update): https://langchain-ai.github.io/langgraph/concepts/low_level/#command  
  Why: branching without a separate router node.
- Persistence / threads: https://langchain-ai.github.io/langgraph/concepts/persistence/  
  Why: imported `langgraph-persistence`.
- Human-in-the-loop / interrupt: https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/  
  Why: imported `langgraph-human-in-the-loop`.
- LangChain Academy deep research: https://github.com/langchain-ai/deep_research_from_scratch  
  Why: source of gated skill `langgraph-academy-patterns` — do not apply unbounded ReAct to the product graph.

## Related

- Tracing / LangSmith: [langsmith.md](langsmith.md)
- Web search / Tavily: [tavily.md](tavily.md)
- MCP (app vs Cursor IDE): [mcp.md](mcp.md)
- Coverage index: [README.md](README.md)

## What belongs elsewhere

| Content | Location |
|---------|----------|
| Debugging notes | `docs/knowledge/` |
| Full page mirrors / PDF dumps | `docs/references/raw/` (optional, ignored) |

## How to add a link

1. Add a bullet with title + URL.
2. One line on *why* it matters for this project.
3. Prefer stable concept pages over random blog posts; put blogs under `docs/knowledge/`.
