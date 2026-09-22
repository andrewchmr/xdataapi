# langchain-xdataapi

LangChain tools for [xdataapi.io](https://xdataapi.io): read-only public X (Twitter) data.
Profiles, posts, threads, replies, quotes, reposters, followers, and search with the x.com operators.

Read-only by design. No posting, no likes, no direct messages, no private data.
Not affiliated with X Corp.

```bash
pip install langchain-xdataapi
```

## Use

```python
from langchain_xdataapi import XdataapiToolkit

# Reads XDATAAPI_KEY from the environment.
tools = XdataapiToolkit.from_api_key().get_tools()
```

With an agent:

```python
from langchain.agents import create_agent
from langchain_xdataapi import XdataapiToolkit

agent = create_agent(
    "anthropic:claude-opus-5",
    tools=XdataapiToolkit.from_api_key(max_results=25).get_tools(),
)
result = agent.invoke({"messages": [{"role": "user", "content": "What is @vercel posting about this week?"}]})
```

One tool on its own:

```python
from langchain_xdataapi import SearchTweets, XdataapiClient

search = SearchTweets(client=XdataapiClient())
print(search.invoke({"q": "from:vercel since:2026-09-01", "count": 10}))
```

## Tools

| Tool | Reads | Credits |
|---|---|---|
| `x_search_tweets` | Search with the x.com operators | 1 per result |
| `x_get_user` | One profile | 1 |
| `x_get_users` | Up to 100 profiles in one call | 1 per profile |
| `x_get_user_tweets` | Latest posts of a user | 1 per post |
| `x_get_tweet` | One post | 1 |
| `x_get_tweets` | Up to 100 posts in one call | 1 per post |
| `x_get_thread` | A post with its thread and replies | 1 per post |
| `x_get_replies` | Direct replies to a post | 1 per reply |
| `x_get_quotes` | Posts that quote a post | 1 per post |
| `x_get_retweeters` | Accounts that reposted a post | 0.5 per profile |
| `x_get_followers` | Followers, as profiles | 0.1 per profile |
| `x_get_follower_ids` | Follower ids only | 0.02 per id |
| `x_get_following` | Accounts a user follows | 0.1 per profile |
| `x_get_balance` | Credits left and rate limit | free |

Empty results and failed requests cost nothing. A repeated read inside the cache window costs half.
Every response carries `credits_charged` and `balance_remaining`, so the model can see the budget shrink
and stop on its own.

## Spending guards

`max_results` caps the page size of every paging tool, so one agent step cannot ask for more than you allow:

```python
toolkit = XdataapiToolkit.from_api_key(max_results=25)
```

Narrow the surface with `include` or `exclude`:

```python
toolkit = XdataapiToolkit.from_api_key(include=["x_search_tweets", "x_get_user", "x_get_balance"])
```

## Errors

A failure the model can act on — no credits, not found, a search product X refused — comes back as JSON
with `error.code`, so the model can change plan. None of those are charged.
A missing or revoked key raises `XdataapiAuthError`, because no model can repair it.
Rate limits and upstream faults raise `XdataapiError`, so your framework's retry policy sees them.

## MCP instead

An agent that speaks MCP needs no package. Connect the hosted server:

```bash
claude mcp add --transport http xdataapi https://api.xdataapi.io/mcp
```

It signs in with OAuth on first use. It is on the official MCP Registry as `io.xdataapi/xdataapi`.

## Keys and pricing

Get a key at [xdataapi.io/dashboard](https://xdataapi.io/dashboard). 5,000 credits to start, no card.
Prepaid packs from $10; credits never expire. Live status: [xdataapi.io/status](https://xdataapi.io/status).

MIT licensed.
