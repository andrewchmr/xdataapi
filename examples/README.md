# Examples

An agent that speaks MCP needs none of these: connect `https://api.xdataapi.io/mcp` directly.
Everything else has either an installable package or an example here.

## Installable packages

| Framework | Install | Source |
|---|---|---|
| LangChain, LangGraph | `pip install langchain-xdataapi` | [../packages/langchain](../packages/langchain) |
| LlamaIndex | `pip install llama-index-tools-xdataapi` | [../packages/llama-index](../packages/llama-index) |
| n8n | community node `n8n-nodes-xdataapi` | [../packages/n8n](../packages/n8n) |
| Claude Code | `claude plugin install xdataapi@xdataapi` | [../plugins/xdataapi](../plugins/xdataapi) |

## Copy and paste

| File | Framework | Goes through |
|---|---|---|
| `crewai_tool.py` | CrewAI | the REST API |
| `vercel-ai-sdk.ts` | Vercel AI SDK | the `xdataapi` npm package |
| `vercel-ai-sdk-mcp.ts` | Vercel AI SDK | the hosted MCP server |
| `openai_agents_sdk.py` | OpenAI Agents SDK | the hosted MCP server |

Set `XDATAAPI_KEY` from https://xdataapi.io/dashboard. New keys start with 5,000 free credits, no card.

## Two rules worth putting in your system prompt

1. **Batch, never loop.** `get_users` takes 100 handles and `get_tweets` 100 ids, each in one request.
2. **Ask for what you need.** `count` decides the bill; empty results and failures are free, and a
   cached read costs half. `fresh=true` costs double.
