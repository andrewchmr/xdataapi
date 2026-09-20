# xdataapi

Read-only public X (Twitter) data for developers and AI agents. Profiles, tweets, timelines, threads,
followers, and search with the x.com operators. One credit per tweet or profile returned. Empty results
and errors are free.

- Site and docs: https://xdataapi.io/docs
- API: `https://api.xdataapi.io` (OpenAPI 3.1: [openapi.yaml](openapi.yaml), also at https://api.xdataapi.io/openapi.yaml)
- Hosted MCP server: `https://api.xdataapi.io/mcp` (Streamable HTTP, OAuth or `x-api-key`)
- Status, checked every minute from outside: https://xdataapi.io/status
- Docs for agents: https://xdataapi.io/llms.txt

Not affiliated with X Corp. Public data only. No write endpoints.

## MCP

Claude Code:

```bash
claude mcp add --transport http xdataapi https://api.xdataapi.io/mcp
```

The server signs you in with OAuth on first use. Clients without OAuth pass a key instead:

```json
{
  "mcpServers": {
    "xdataapi": {
      "url": "https://api.xdataapi.io/mcp",
      "headers": { "x-api-key": "xd_live_..." }
    }
  }
}
```

Stdio-only clients can bridge with `mcp-remote`:

```json
{
  "mcpServers": {
    "xdataapi": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.xdataapi.io/mcp", "--header", "x-api-key:${XDATAAPI_KEY}"],
      "env": { "XDATAAPI_KEY": "xd_live_..." }
    }
  }
}
```

Tools: `get_user`, `get_users`, `get_user_tweets`, `get_followers`, `get_following`, `get_follower_ids`,
`search_tweets`, `get_tweet`, `get_tweets`, `get_thread`, `get_replies`, `get_quotes`, `get_retweeters`,
`get_balance`. All read-only. Listed on the official MCP Registry as `io.xdataapi/xdataapi`.

## REST

```bash
curl "https://api.xdataapi.io/v1/tweets/search?q=from:x%20since:2026-09-01&count=20" \
  -H "x-api-key: xd_live_..."
```

Every response carries `credits_charged` and `balance_remaining`. Pages return `next_cursor`; pass it back as `cursor`.

## SDKs

TypeScript, `npm install xdataapi`:

```ts
import { xdataapi } from 'xdataapi';
const api = xdataapi({ apiKey: process.env.XDATAAPI_KEY! });
const { data } = await api.searchTweets({ query: { q: 'from:x', count: 20 } });
```

Python, `pip install xdataapi`:

```python
from xdataapi import AuthenticatedClient
from xdataapi.api.tweets import search_tweets
client = AuthenticatedClient(base_url="https://api.xdataapi.io", token=KEY, prefix="", auth_header_name="x-api-key")
page = search_tweets.sync(client=client, q="from:x", count=20)
```

Both are generated from `openapi.yaml`. See [examples/](examples/) for LangChain, CrewAI, and Vercel AI SDK tools.

## Pricing

Prepaid credit packs from $10. Credits never expire. No per-call minimum. Rate limit rises with lifetime spend.
Details: https://xdataapi.io/#pricing

## Support

hello@xdataapi.io. Security reports: https://xdataapi.io/.well-known/security.txt
