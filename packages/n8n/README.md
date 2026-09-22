# n8n-nodes-xdataapi

An [n8n](https://n8n.io) community node for [xdataapi.io](https://xdataapi.io): read-only public X (Twitter)
data. Profiles, posts, threads, replies, quotes, reposters, followers, and search with the x.com operators.

Read-only by design. No posting, no likes, no direct messages, no private data.
Not affiliated with X Corp.

## Install

In n8n: **Settings → Community nodes → Install**, then enter `n8n-nodes-xdataapi`.

Self-hosted, by hand:

```bash
npm install n8n-nodes-xdataapi
```

## Credentials

Get a key at [xdataapi.io/dashboard](https://xdataapi.io/dashboard). New keys start with 5,000 free credits
and no card. In n8n add an **xdataapi API** credential and paste the key. The credential test calls
`/v1/me`, which is free and reports the balance, so a green tick also proves the key has credits.

## Operations

**Post**

| Operation | Reads | Credits |
|---|---|---|
| Search | Search with the x.com operators | 1 per post |
| Get | One post by id, with its author | 1 |
| Get Many by ID | Up to 100 posts in one request | 1 per post found |
| Get Thread | A post with its thread and replies | 1 per post |
| Get Replies | Direct replies to a post | 1 per reply |
| Get Quotes | Posts that quote a post | 1 per post |
| Get Reposters | Accounts that reposted a post | 0.5 per profile |

**User**

| Operation | Reads | Credits |
|---|---|---|
| Get | One profile by handle | 1 |
| Get Many by Handle | Up to 100 profiles in one request | 1 per profile found |
| Get Posts | Latest posts of a user | 1 per post |
| Get Followers | Followers, as full profiles | 0.1 per profile |
| Get Follower IDs | Follower ids only, five times cheaper | 0.02 per id |
| Get Following | Accounts a user follows | 0.1 per profile |

**Account**

| Operation | Reads | Credits |
|---|---|---|
| Get Balance | Credits left and the rate limit | free |

Empty results and failed requests cost nothing. A repeated read inside the cache window costs half.

## What the node does for you

- **One item per result.** A search that returns 20 posts gives 20 n8n items, ready for the next node.
- **Limit means limit.** Ask for 3 and the node asks the API for 3, not for a page of 50 you then throw
  away. Every credit you spend is one you asked for.
- **Return All** follows the cursor to the end, with a **Max Pages** stop (50 by default) so a runaway
  flow cannot empty the balance.
- **Include Response Metadata** adds `_meta` to every item with `credits_charged`, `balance_remaining`,
  `cache` and `next_cursor`, for flows that track spend.
- **Skip Cache** is off by default. Turn it on only when the data must be seconds old; it costs double.

## As an AI tool

The node is marked `usableAsTool`, so an **AI Agent** node can call it directly. Give the agent the
Account → Get Balance operation as well, and it can check the budget before a large read.

An agent that speaks MCP needs no node at all. The hosted MCP server is at `https://api.xdataapi.io/mcp`
(Streamable HTTP, OAuth or `x-api-key`), listed on the official MCP Registry as `io.xdataapi/xdataapi`.

## Search syntax

`Query` takes x.com search syntax:

```
from:vercel since:2026-09-01 -filter:replies
"model context protocol" min_faves:50 lang:en
(from:x OR from:xdevelopers) until:2026-09-20
```

`Product` is `Latest` by default and always available. `Top` is refused to some reading sessions; that
refusal is free.

## Pricing and status

Prepaid packs from $10. Credits never expire. No per-call minimum.
Live status, checked every minute from outside the network: [xdataapi.io/status](https://xdataapi.io/status).

## Links

- Docs: https://xdataapi.io/docs
- API reference: https://xdataapi.io/reference
- Source: https://github.com/xdataapi/xdataapi
- Support: hello@xdataapi.io

MIT licensed.
