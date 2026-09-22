# xdataapi

Typed TypeScript client for [xdataapi.io](https://xdataapi.io), the read-only X (Twitter) data API.
Generated from the API's OpenAPI document, so every endpoint, parameter and response type is here.

```bash
npm install xdataapi
```

```ts
import { xdataapi } from 'xdataapi';

const api = xdataapi({ apiKey: process.env.XDATAAPI_KEY! });

const { data: profile } = await api.getUser({ path: { handle: 'x' } });
console.log(profile?.data?.followers, profile?.credits_charged);

const { data: page } = await api.searchTweets({ query: { q: 'from:x since:2026-09-01', count: 20 } });
for (const t of page?.data ?? []) console.log(t.id, t.text);

const { data: many } = await api.getUsers({ body: { handles: ['x', 'github', 'vercel'] } });
console.log(many?.items, many?.errors);
```

Every call returns `{ data, error, response }`. On a non-2xx status `data` is undefined and `error` holds the
API error with its `code` (`no_credits`, `not_found`, `rate_limited`, ...). Works in Node 18+, Bun, Deno,
browsers and edge runtimes; it uses `fetch`.

Methods: `getMe`, `listPacks`, `createCheckout`, `getUser`, `getUsers`, `getUserTweets`, `getFollowers`,
`getFollowing`, `searchTweets`, `getTweet`, `getTweets`, `getThread`, `getReplies`, `getQuotes`,
`getRetweeters`. Pagination: pass `next_cursor` from a page back as `query.cursor`.

Docs: https://xdataapi.io/docs. API reference: https://xdataapi.io/reference.
