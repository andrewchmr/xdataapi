/**
 * One table for every read the node can do.
 *
 * Kept free of n8n imports so it can be unit tested on its own, and so the node
 * file stays a thin loop over this table.
 */

export type Resource = 'tweet' | 'user' | 'account';

export interface OperationSpec {
	/** Value stored in the `operation` parameter. */
	name: string;
	/** Label in the node's operation dropdown. */
	displayName: string;
	/** What the dropdown says under the label. */
	description: string;
	/** REST path. `id` and `user` are already url-encoded. */
	path: (p: Params) => string;
	/** Fixed query parameters built from the node's own fields. */
	query?: (p: Params) => Record<string, string | number | boolean | undefined>;
	/** Reads a page at a time and answers `next_cursor`. */
	paged?: boolean;
	/** Where the entities sit in the response body. */
	collection: 'data' | 'single';
	/** Shown in the field hints, so the cost is visible while building a flow. */
	credits: string;
}

export interface Params {
	q?: string;
	product?: string;
	tweetId?: string;
	tweetIds?: string;
	handle?: string;
	handles?: string;
	user?: string;
	count?: number;
	cursor?: string;
	fresh?: boolean;
}

/** Handles arrive from users in every shape. Take the @ off and trim. */
export function cleanHandle(value: string): string {
	return value.trim().replace(/^@/, '');
}

/** "a, @b ,c" -> "a,b,c". Empty entries are dropped. */
export function cleanList(value: string, handles: boolean): string {
	return String(value ?? '')
		.split(',')
		.map((entry) => (handles ? cleanHandle(entry) : entry.trim()))
		.filter((entry) => entry.length > 0)
		.join(',');
}

const paths = {
	user: (p: Params) => encodeURIComponent(cleanHandle(p.user ?? '')),
	tweet: (p: Params) => encodeURIComponent(String(p.tweetId ?? '').trim()),
};

export const OPERATIONS: Record<Resource, OperationSpec[]> = {
	tweet: [
		{
			name: 'search',
			displayName: 'Search',
			description: 'Search public posts with the x.com operators',
			path: () => '/v1/tweets/search',
			query: (p) => ({ q: p.q, product: p.product }),
			paged: true,
			collection: 'data',
			credits: '1 credit per post returned. An empty result is free.',
		},
		{
			name: 'get',
			displayName: 'Get',
			description: 'Get one post by id, with its author',
			path: (p) => `/v1/tweets/${paths.tweet(p)}`,
			collection: 'single',
			credits: '1 credit.',
		},
		{
			name: 'getMany',
			displayName: 'Get Many by ID',
			description: 'Get up to 100 posts by id in one request',
			path: () => '/v1/tweets/batch',
			query: (p) => ({ ids: cleanList(p.tweetIds ?? '', false) }),
			collection: 'data',
			credits: '1 credit per post found. Deleted and private posts cost nothing.',
		},
		{
			name: 'getThread',
			displayName: 'Get Thread',
			description: 'Get a post with its thread and replies, focal post first',
			path: (p) => `/v1/tweets/${paths.tweet(p)}/thread`,
			paged: true,
			collection: 'data',
			credits: '1 credit per post returned.',
		},
		{
			name: 'getReplies',
			displayName: 'Get Replies',
			description: 'Get the direct replies to a post',
			path: (p) => `/v1/tweets/${paths.tweet(p)}/replies`,
			paged: true,
			collection: 'data',
			credits: '1 credit per reply.',
		},
		{
			name: 'getQuotes',
			displayName: 'Get Quotes',
			description: 'Get the posts that quote a post, newest first',
			path: (p) => `/v1/tweets/${paths.tweet(p)}/quotes`,
			paged: true,
			collection: 'data',
			credits: '1 credit per post.',
		},
		{
			name: 'getRetweeters',
			displayName: 'Get Reposters',
			description: 'Get the accounts that reposted a post',
			path: (p) => `/v1/tweets/${paths.tweet(p)}/retweeters`,
			paged: true,
			collection: 'data',
			credits: '0.5 credit per profile. X refuses this to some reading accounts; a 403 is free.',
		},
	],
	user: [
		{
			name: 'get',
			displayName: 'Get',
			description: 'Get the public profile of one user',
			path: (p) => `/v1/users/${encodeURIComponent(cleanHandle(p.handle ?? ''))}`,
			collection: 'single',
			credits: '1 credit.',
		},
		{
			name: 'getMany',
			displayName: 'Get Many by Handle',
			description: 'Get up to 100 profiles in one request',
			path: () => '/v1/users/batch',
			query: (p) => ({ handles: cleanList(p.handles ?? '', true) }),
			collection: 'data',
			credits: '1 credit per profile found. Handles that do not exist cost nothing.',
		},
		{
			name: 'getTweets',
			displayName: 'Get Posts',
			description: 'Get the latest posts of a user, newest first',
			path: (p) => `/v1/users/${paths.user(p)}/tweets`,
			paged: true,
			collection: 'data',
			credits: '1 credit per post.',
		},
		{
			name: 'getFollowers',
			displayName: 'Get Followers',
			description: 'Get the followers of a user, as full profiles',
			path: (p) => `/v1/users/${paths.user(p)}/followers`,
			paged: true,
			collection: 'data',
			credits: '0.1 credit per profile. X refuses this to some reading accounts; a 403 is free.',
		},
		{
			name: 'getFollowerIds',
			displayName: 'Get Follower IDs',
			description: 'Get follower ids without the profiles, five times cheaper',
			path: (p) => `/v1/users/${paths.user(p)}/followers/ids`,
			paged: true,
			collection: 'data',
			credits: '0.02 credit per id.',
		},
		{
			name: 'getFollowing',
			displayName: 'Get Following',
			description: 'Get the accounts a user follows',
			path: (p) => `/v1/users/${paths.user(p)}/following`,
			paged: true,
			collection: 'data',
			credits: '0.1 credit per profile. X refuses this to some reading accounts; a 403 is free.',
		},
	],
	account: [
		{
			name: 'getBalance',
			displayName: 'Get Balance',
			description: 'Get the credits left on the key and its rate limit',
			path: () => '/v1/me',
			collection: 'single',
			credits: 'Free.',
		},
	],
};

export function findOperation(resource: string, operation: string): OperationSpec {
	const found = OPERATIONS[resource as Resource]?.find((spec) => spec.name === operation);
	if (!found) throw new Error(`Unknown operation "${operation}" for resource "${resource}"`);
	return found;
}

/** The API serves at most 50 per page, whatever the caller asks for. */
export const MAX_PAGE = 50;

/** A page size that neither over-fetches nor wastes a round trip. */
export function pageSize(remaining: number): number {
	return Math.max(1, Math.min(MAX_PAGE, remaining));
}
