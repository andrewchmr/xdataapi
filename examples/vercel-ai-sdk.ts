// Vercel AI SDK tools over the xdataapi REST API. npm install ai zod xdataapi
import { tool } from 'ai';
import { z } from 'zod';
import { xdataapi } from 'xdataapi';

const api = xdataapi({ apiKey: process.env.XDATAAPI_KEY! });

export const xTools = {
  searchX: tool({
    description:
      'Search public X (Twitter) posts. q takes the x.com operators: from:, to:, since:YYYY-MM-DD, until:, min_faves:, lang:, "phrase", OR, -.',
    inputSchema: z.object({ q: z.string(), count: z.number().int().min(1).max(50).default(20) }),
    execute: async ({ q, count }) => (await api.searchTweets({ query: { q, count } })).data,
  }),
  xProfile: tool({
    description: 'Public profile of one X user by handle.',
    inputSchema: z.object({ handle: z.string() }),
    execute: async ({ handle }) => (await api.getUser({ path: { handle: handle.replace(/^@/, '') } })).data,
  }),
  xUserTweets: tool({
    description: 'Latest posts of one X user, newest first.',
    inputSchema: z.object({ handle: z.string(), count: z.number().int().min(1).max(50).default(20) }),
    execute: async ({ handle, count }) =>
      (await api.getUserTweets({ path: { user: handle.replace(/^@/, '') }, query: { count } })).data,
  }),
};
