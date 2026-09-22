---
name: x-data
description: Read public X (Twitter) data through the xdataapi tools — profiles, posts, threads, replies, quotes, reposters, followers, and search. Use when the task needs what someone posted on X, who follows whom, how a post was received, or what X says about a topic, company or person. Covers the x.com search operators and how to keep a read cheap.
---

# Reading X data

The `xdataapi` MCP server reads public X (Twitter) data. Every tool is read-only: there is no
posting, no liking, no direct messages, and no private data.

Each call spends credits from the user's balance. Read the two rules below before the first call.

## Rule 1: batch, never loop

`get_users` takes up to 100 handles and `get_tweets` up to 100 ids, each in one request. Ten single
reads cost the same credits as one batch of ten but take ten round trips and ten rate-limit slots.

```
get_users(handles=["vercel", "github", "x"])      # one call
get_tweets(ids=["20", "21", "22"])                # one call
```

Reach for a single `get_user` or `get_tweet` only when there is genuinely one subject.

## Rule 2: ask for what you need

`count` decides the bill. A search with `count=10` costs about 10 credits; the same search left at
the default costs about 20. Start small and page with `next_cursor` only while the answer is still
missing.

`fresh=true` re-reads X and costs double. Leave it off unless the data must be seconds old — a
cached read costs half.

## Costs

| Tool | Cost |
|---|---|
| `search_tweets`, `get_tweet`, `get_tweets`, `get_user`, `get_users`, `get_user_tweets`, `get_thread`, `get_replies`, `get_quotes` | 1 credit per result |
| `get_retweeters` | 0.5 per profile |
| `get_followers`, `get_following` | 0.1 per profile |
| `get_follower_ids` | 0.02 per id |
| `get_balance` | free |

Empty results and failed requests are free. Every response carries `credits_charged` and
`balance_remaining` — watch the second one and tell the user before a large read empties it.

Before a job that could run to thousands of results, call `get_balance` and say what the plan will
cost.

## Search

`search_tweets` takes the x.com operators, the same ones the search box on x.com accepts:

| Operator | Finds |
|---|---|
| `from:handle` | posts by that account |
| `to:handle` | replies addressed to that account |
| `since:YYYY-MM-DD` `until:YYYY-MM-DD` | a date window |
| `min_faves:N` `min_retweets:N` | posts above an engagement floor |
| `lang:en` | one language |
| `"exact phrase"` | the phrase, not the words |
| `a OR b` | either term |
| `-term` `-filter:replies` | exclude |
| `filter:links` `filter:media` | only posts with links or media |

Combine them. Narrow first, widen only if the answer is thin:

```
from:vercel since:2026-09-01 -filter:replies
"model context protocol" min_faves:50 lang:en since:2026-09-01
(from:x OR from:xdevelopers) until:2026-09-20
```

`product` is `Latest` by default and always available. `Top` ranks by engagement but X refuses it to
some reading sessions; that refusal is HTTP 403 and costs nothing, so fall back to `Latest`.

## Choosing the tool

| The question | The tool |
|---|---|
| What is being said about X? | `search_tweets` |
| What did this account post? | `get_user_tweets` |
| Who is this account? | `get_user`, or `get_users` for several |
| What is in this thread? | `get_thread` — the whole conversation in one call |
| How did people answer this post? | `get_replies`, and `get_quotes` for commentary |
| Who spread this post? | `get_retweeters` |
| Who follows this account? | `get_followers` for profiles, `get_follower_ids` when ids are enough |
| How much budget is left? | `get_balance` |

`get_thread` returns the focal post first and then the conversation, so prefer it over walking
replies by hand.

Handles work with or without the leading `@`, and a numeric user id works anywhere a handle does.

## Paging

A response with `next_cursor` has more. Pass it back as `cursor` to continue. A page you have
already read costs half when you read it again inside the cache window, so re-reading a page to
re-check something is cheap; fetching a new page is not.

## When a call fails

Failures are free. Read `error.code` and act on it:

| Code | Meaning | Do |
|---|---|---|
| `no_credits` | the balance is empty | stop and tell the user to top up at https://xdataapi.io/dashboard |
| `not_found` | no such account or post, or it is private | say so; do not retry |
| `product_unavailable` | X refused this search product | retry once with `product=Latest` |
| `too_many_requests` | the per-key rate limit | wait, then retry once |
| `invalid_key` | the key is unknown or revoked | stop; the user must fix the key |

A 403 on `get_followers`, `get_following` or `get_retweeters` means the reading account X gave us
is not allowed that view. It is free. Report it rather than retrying in a loop.

## Reporting

Quote posts with the author's handle and the date. Link a post as
`https://x.com/<handle>/status/<id>`. Say when a figure came from a cached read rather than a fresh
one if the user is asking about something happening right now.
