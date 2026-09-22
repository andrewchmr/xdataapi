import { describe, expect, it, vi } from 'vitest';

import { Xdataapi } from '../nodes/Xdataapi/Xdataapi.node';
import { OPERATIONS, cleanHandle, cleanList, findOperation, pageSize } from '../nodes/Xdataapi/operations';

type Body = Record<string, unknown>;

/** A stand-in for the n8n execution context, with a scripted sequence of responses. */
function context(params: Record<string, unknown>, responses: Body[], opts: { items?: number; continueOnFail?: boolean } = {}) {
	const requests: Array<Record<string, unknown>> = [];
	let call = 0;
	const ctx = {
		getInputData: () => Array.from({ length: opts.items ?? 1 }, () => ({ json: {} })),
		getNodeParameter: (name: string, _i: number, fallback?: unknown) =>
			name in params ? params[name] : fallback,
		continueOnFail: () => opts.continueOnFail ?? false,
		getNode: () => ({ name: 'xdataapi', type: 'xdataapi' }),
		helpers: {
			httpRequestWithAuthentication: vi.fn(async function (this: unknown, _cred: string, request: Record<string, unknown>) {
				requests.push(request);
				const next = responses[Math.min(call, responses.length - 1)];
				call += 1;
				if (next instanceof Error) throw next;
				return next;
			}),
		},
	};
	return { ctx, requests };
}

const run = async (ctx: unknown) => (await Xdataapi.prototype.execute.call(ctx as never))[0];

describe('the operation table', () => {
	it('strips the at sign and the spaces from a handle', () => {
		expect(cleanHandle('  @vercel ')).toBe('vercel');
	});

	it('folds a messy list into one comma separated string', () => {
		expect(cleanList('a, @b ,, c ', true)).toBe('a,b,c');
	});

	it('leaves ids alone but still trims them', () => {
		expect(cleanList(' 20 ,21', false)).toBe('20,21');
	});

	it('never asks for more than one page holds', () => {
		expect(pageSize(500)).toBe(50);
		expect(pageSize(7)).toBe(7);
		expect(pageSize(0)).toBe(1);
	});

	it('refuses an operation that does not exist', () => {
		expect(() => findOperation('user', 'delete')).toThrow(/Unknown operation/);
	});

	it('says what every operation costs, so the cost shows while building a flow', () => {
		for (const specs of Object.values(OPERATIONS)) {
			for (const spec of specs) {
				expect(spec.credits.toLowerCase()).toMatch(/credit|free/);
			}
		}
	});

	it('offers every read the API has', () => {
		const names = Object.values(OPERATIONS).flat().length;
		expect(names).toBe(14);
	});
});

describe('reading one object', () => {
	it('unwraps data and returns a single item', async () => {
		const { ctx, requests } = context(
			{ resource: 'user', operation: 'get', handle: '@vercel' },
			[{ data: { handle: 'vercel', followers: 12 }, credits_charged: 1 }],
		);
		const out = await run(ctx);
		expect(requests[0].url).toBe('/v1/users/vercel');
		expect(out).toHaveLength(1);
		expect(out[0].json).toEqual({ handle: 'vercel', followers: 12 });
	});

	it('adds _meta only when asked', async () => {
		const { ctx } = context(
			{ resource: 'user', operation: 'get', handle: 'x', options: { includeMetadata: true } },
			[{ data: { handle: 'x' }, credits_charged: 1, balance_remaining: 4678, cache: 'miss' }],
		);
		const out = await run(ctx);
		expect((out[0].json as Body)._meta).toMatchObject({ credits_charged: 1, balance_remaining: 4678 });
	});

	it('reads the balance with no query at all', async () => {
		const { ctx, requests } = context({ resource: 'account', operation: 'getBalance' }, [
			{ balance: 4679.87, qps: 25 },
		]);
		const out = await run(ctx);
		expect(requests[0].url).toBe('/v1/me');
		expect(out[0].json).toMatchObject({ balance: 4679.87 });
	});
});

describe('searching', () => {
	it('sends the operators through untouched and caps the page at the limit', async () => {
		const { ctx, requests } = context(
			{ resource: 'tweet', operation: 'search', q: 'from:x since:2026-09-01', product: 'Latest', limit: 5 },
			[{ data: [{ id: '1' }, { id: '2' }] }],
		);
		const out = await run(ctx);
		expect(requests[0].qs).toMatchObject({ q: 'from:x since:2026-09-01', product: 'Latest', count: 5 });
		expect(out).toHaveLength(2);
	});

	it('leaves fresh out unless the option is on', async () => {
		const { ctx, requests } = context(
			{ resource: 'tweet', operation: 'search', q: 'hello', limit: 5 },
			[{ data: [] }],
		);
		await run(ctx);
		expect(requests[0].qs).not.toHaveProperty('fresh');
	});

	it('sends fresh when the option is on', async () => {
		const { ctx, requests } = context(
			{ resource: 'tweet', operation: 'search', q: 'hello', limit: 5, options: { fresh: true } },
			[{ data: [] }],
		);
		await run(ctx);
		expect(requests[0].qs).toMatchObject({ fresh: true });
	});
});

describe('paging', () => {
	it('stops at the limit instead of buying a whole page', async () => {
		const { ctx, requests } = context(
			{ resource: 'user', operation: 'getTweets', user: 'x', limit: 3 },
			[{ data: [{ id: '1' }, { id: '2' }, { id: '3' }], next_cursor: 'c1' }],
		);
		const out = await run(ctx);
		expect(requests).toHaveLength(1);
		expect(requests[0].qs).toMatchObject({ count: 3 });
		expect(out).toHaveLength(3);
	});

	it('asks for a second page only when the first did not fill the limit', async () => {
		const { ctx, requests } = context(
			{ resource: 'user', operation: 'getTweets', user: 'x', limit: 4 },
			[
				{ data: [{ id: '1' }, { id: '2' }], next_cursor: 'c1' },
				{ data: [{ id: '3' }, { id: '4' }], next_cursor: 'c2' },
			],
		);
		const out = await run(ctx);
		expect(requests).toHaveLength(2);
		expect(requests[1].qs).toMatchObject({ cursor: 'c1', count: 2 });
		expect(out).toHaveLength(4);
	});

	it('follows the cursor to the end when Return All is on', async () => {
		const { ctx, requests } = context(
			{ resource: 'user', operation: 'getTweets', user: 'x', returnAll: true },
			[
				{ data: [{ id: '1' }], next_cursor: 'c1' },
				{ data: [{ id: '2' }], next_cursor: 'c2' },
				{ data: [{ id: '3' }] },
			],
		);
		const out = await run(ctx);
		expect(requests).toHaveLength(3);
		expect(requests[0].qs).toMatchObject({ count: 50 });
		expect(out.map((item) => (item.json as Body).id)).toEqual(['1', '2', '3']);
	});

	it('stops at Max Pages even when the cursor keeps going', async () => {
		const { ctx, requests } = context(
			{ resource: 'user', operation: 'getTweets', user: 'x', returnAll: true, options: { maxPages: 2 } },
			[{ data: [{ id: '1' }], next_cursor: 'always' }],
		);
		await run(ctx);
		expect(requests).toHaveLength(2);
	});

	it('stops on an empty page even when a cursor comes back', async () => {
		const { ctx, requests } = context(
			{ resource: 'user', operation: 'getTweets', user: 'x', returnAll: true },
			[{ data: [], next_cursor: 'c1' }],
		);
		const out = await run(ctx);
		expect(requests).toHaveLength(1);
		expect(out).toHaveLength(0);
	});

	it('never pages a single read', async () => {
		const { ctx, requests } = context({ resource: 'tweet', operation: 'get', tweetId: '20' }, [
			{ data: { id: '20' }, next_cursor: 'c1' },
		]);
		await run(ctx);
		expect(requests).toHaveLength(1);
	});
});

describe('shapes the API returns', () => {
	it('wraps bare follower ids into objects n8n can carry', async () => {
		const { ctx } = context(
			{ resource: 'user', operation: 'getFollowerIds', user: 'x', limit: 2 },
			[{ data: ['111', '222'] }],
		);
		const out = await run(ctx);
		expect(out.map((item) => item.json)).toEqual([{ id: '111' }, { id: '222' }]);
	});

	it('folds a comma separated batch into one request', async () => {
		const { ctx, requests } = context(
			{ resource: 'user', operation: 'getMany', handles: '@x, github ,vercel' },
			[{ data: [{ handle: 'x' }] }],
		);
		await run(ctx);
		expect(requests[0].url).toBe('/v1/users/batch');
		expect(requests[0].qs).toMatchObject({ handles: 'x,github,vercel' });
	});

	it('reports the inputs a batch skipped, with the metadata option on', async () => {
		const { ctx } = context(
			{ resource: 'tweet', operation: 'getMany', tweetIds: '20,999', options: { includeMetadata: true } },
			[{ data: [{ id: '20' }], errors: [{ input: '999', code: 'not_found' }] }],
		);
		const out = await run(ctx);
		expect((out[1].json as Body)._errors).toEqual([{ input: '999', code: 'not_found' }]);
	});

	it('url-encodes a user id so a path cannot be escaped', async () => {
		const { ctx, requests } = context(
			{ resource: 'user', operation: 'getTweets', user: '../../me', limit: 1 },
			[{ data: [] }],
		);
		await run(ctx);
		expect(requests[0].url).toBe('/v1/users/..%2F..%2Fme/tweets');
	});
});

describe('failures', () => {
	it('carries on with an error item when the node is set to continue', async () => {
		const { ctx } = context(
			{ resource: 'user', operation: 'get', handle: 'x' },
			[new Error('balance is zero') as never],
			{ continueOnFail: true },
		);
		const out = await run(ctx);
		expect(out[0].json).toMatchObject({ error: 'balance is zero' });
	});

	it('throws otherwise', async () => {
		const { ctx } = context({ resource: 'user', operation: 'get', handle: 'x' }, [
			new Error('balance is zero') as never,
		]);
		await expect(run(ctx)).rejects.toThrow();
	});

	it('keeps one output item per input item', async () => {
		const { ctx } = context({ resource: 'user', operation: 'get', handle: 'x' }, [{ data: { handle: 'x' } }], {
			items: 3,
		});
		const out = await run(ctx);
		expect(out).toHaveLength(3);
		expect(out.map((item) => item.pairedItem)).toEqual([{ item: 0 }, { item: 1 }, { item: 2 }]);
	});
});
