# MCP (Model Context Protocol) — curated references

MCP standardizes how apps expose **tools / resources / prompts** to LLMs. This repo does **not** use MCP in `src/`.

## Official docs — protocol & LangChain

- MCP introduction: https://modelcontextprotocol.io/introduction  
  Why: mental model (hosts, clients, servers, tools).
- LangChain + MCP (Python): https://docs.langchain.com/oss/python/langchain/mcp  
  Why: `langchain-mcp-adapters`, `MultiServerMCPClient`, LangGraph usage.
- Adapter repo: https://github.com/langchain-ai/langchain-mcp-adapters  
  Why: install notes, multi-server / stdio / HTTP examples.
- MCP transports: https://modelcontextprotocol.io/docs/concepts/transports  
  Why: stdio vs Streamable HTTP when connecting servers.

The diagnosis pipeline does not depend on `langchain-mcp-adapters`.

## Fit for this repo

No MCP in the diagnosis pipeline. Search uses Yahoo titles, optional Tavily, and optional SEC 8-K on the existing `search` node.

## Related

- LangGraph: [langgraph.md](langgraph.md)
- Web search without MCP: [tavily.md](tavily.md)
