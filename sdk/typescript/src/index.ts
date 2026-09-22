// xdataapi: typed client for https://api.xdataapi.io.
// Everything under ./generated comes from openapi.yaml; regenerate with `pnpm generate`.
import { createClient, createConfig, type Client } from './generated/client/index.js';
import * as ops from './generated/sdk.gen.js';

export * from './generated/types.gen.js';
export * from './generated/sdk.gen.js';
export { client } from './generated/client.gen.js';

export interface XdataapiOptions {
  /** Your key from https://xdataapi.io/dashboard, `xd_live_...`. */
  apiKey: string;
  /** Override for tests or a private deployment. */
  baseUrl?: string;
  /** Custom fetch, for example an instrumented one. */
  fetch?: typeof globalThis.fetch;
}

/**
 * Build a client bound to one API key. The returned object carries every
 * operation from the API reference as a method, already pointed at this client:
 *
 *   const api = xdataapi({ apiKey: process.env.XDATAAPI_KEY! });
 *   const { data } = await api.getUser({ path: { handle: 'x' } });
 *   console.log(data?.data?.followers, data?.credits_charged);
 */
export function xdataapi(o: XdataapiOptions) {
  const client: Client = createClient(createConfig({
    baseUrl: o.baseUrl ?? 'https://api.xdataapi.io',
    headers: { 'x-api-key': o.apiKey },
    ...(o.fetch ? { fetch: o.fetch } : {}),
  }));
  const bind = <F extends (opts: any) => any>(f: F) =>
    ((opts?: Parameters<F>[0]) => f({ ...(opts ?? {}), client })) as unknown as
      (opts?: Omit<NonNullable<Parameters<F>[0]>, 'client'>) => ReturnType<F>;
  return {
    client,
    getMe: bind(ops.getMe),
    listPacks: bind(ops.listPacks),
    createCheckout: bind(ops.createCheckout),
    getUser: bind(ops.getUser),
    getUsers: bind(ops.getUsers),
    getUserTweets: bind(ops.getUserTweets),
    getFollowers: bind(ops.getFollowers),
    getFollowerIds: bind(ops.getFollowerIds),
    getFollowing: bind(ops.getFollowing),
    searchTweets: bind(ops.searchTweets),
    getTweet: bind(ops.getTweet),
    getTweets: bind(ops.getTweets),
    getThread: bind(ops.getThread),
    getReplies: bind(ops.getReplies),
    getQuotes: bind(ops.getQuotes),
    getRetweeters: bind(ops.getRetweeters),
  };
}

export type Xdataapi = ReturnType<typeof xdataapi>;
