# llama-index-tools-xdataapi

LlamaIndex tool spec for [xdataapi.io](https://xdataapi.io): read-only public X (Twitter) data.
Profiles, posts, threads, replies, quotes, reposters, followers, and search with the x.com operators.

Read-only by design. No posting, no likes, no direct messages, no private data.
Not affiliated with X Corp.

```bash
pip install llama-index-tools-xdataapi
```

## Use

```python
from llama_index.tools.xdataapi import XdataapiToolSpec

# Reads XDATAAPI_KEY from the environment.
tool_spec = XdataapiToolSpec()
tools = tool_spec.to_tool_list()
```

With an agent:

```python
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.anthropic import Anthropic
from llama_index.tools.xdataapi import XdataapiToolSpec

agent = FunctionAgent(
    tools=XdataapiToolSpec(max_results=25).to_tool_list(),
    llm=Anthropic(model="claude-opus-5"),
)
print(await agent.run("What is @vercel posting about this week?"))
```

One call on its own:

```python
XdataapiToolSpec().search_tweets(q="from:vercel since:2026-09-01", count=10)
```

## Tools

| Tool | Reads | Credits |
|---|---|---|
| `search_tweets` | Search with the x.com operators | 1 per result |
| `get_user` | One profile | 1 |
| `get_users` | Up to 100 profiles in one call | 1 per profile |
| `get_user_tweets` | Latest posts of a user | 1 per post |
| `get_tweet` | One post | 1 |
| `get_tweets` | Up to 100 posts in one call | 1 per post |
| `get_thread` | A post with its thread and replies | 1 per post |
| `get_replies` | Direct replies to a post | 1 per reply |
| `get_quotes` | Posts that quote a post | 1 per post |
| `get_retweeters` | Accounts that reposted a post | 0.5 per profile |
| `get_followers` | Followers, as profiles | 0.1 per profile |
| `get_follower_ids` | Follower ids only | 0.02 per id |
| `get_following` | Accounts a user follows | 0.1 per profile |
| `get_balance` | Credits left and rate limit | free |

Empty results and failed requests cost nothing. A repeated read inside the cache window costs half.
Every response carries `credits_charged` and `balance_remaining`, so the model can watch the budget
and stop on its own.

## Spending guards

`max_results` caps the page size of every paging tool:

```python
tool_spec = XdataapiToolSpec(max_results=25)
```

Narrow the surface with the LlamaIndex argument:

```python
tools = XdataapiToolSpec().to_tool_list(spec_functions=["search_tweets", "get_user", "get_balance"])
```

## Errors

A failure the model can act on — no credits, not found, a search product X refused — comes back as a
dict with `error.code`, so the model can change plan. None of those are charged.
A missing or revoked key raises `XdataapiAuthError`, because no model can repair it.
Rate limits and upstream faults raise `XdataapiError`.

## MCP instead

An agent that speaks MCP needs no package. The hosted server is at `https://api.xdataapi.io/mcp`
(Streamable HTTP, OAuth or `x-api-key`), on the official MCP Registry as `io.xdataapi/xdataapi`.

## Keys and pricing

Get a key at [xdataapi.io/dashboard](https://xdataapi.io/dashboard). 5,000 credits to start, no card.
Prepaid packs from $10; credits never expire. Live status: [xdataapi.io/status](https://xdataapi.io/status).

MIT licensed.
