import type {
	IDataObject,
	IExecuteFunctions,
	IHttpRequestOptions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
} from 'n8n-workflow';
import { NodeApiError, NodeOperationError } from 'n8n-workflow';

import { MAX_PAGE, OPERATIONS, findOperation, pageSize, type Params } from './operations';

const BASE_URL = 'https://api.xdataapi.io';

/** Operations that page with a cursor, by resource, for displayOptions. */
const paged = (resource: keyof typeof OPERATIONS) =>
	OPERATIONS[resource].filter((spec) => spec.paged).map((spec) => spec.name);

const tweetIdOperations = ['get', 'getThread', 'getReplies', 'getQuotes', 'getRetweeters'];
const userOperations = ['getTweets', 'getFollowers', 'getFollowerIds', 'getFollowing'];

export class Xdataapi implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'xdataapi',
		name: 'xdataapi',
		icon: { light: 'file:xdataapi.svg', dark: 'file:xdataapi.dark.svg' },
		group: ['input'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["resource"]}}',
		description: 'Read public X (Twitter) data: profiles, posts, threads, followers and search',
		defaults: { name: 'xdataapi' },
		inputs: ['main'] as unknown as INodeTypeDescription['inputs'],
		outputs: ['main'] as unknown as INodeTypeDescription['outputs'],
		usableAsTool: true,
		credentials: [{ name: 'xdataapiApi', required: true }],
		properties: [
			{
				displayName: 'Resource',
				name: 'resource',
				type: 'options',
				noDataExpression: true,
				default: 'tweet',
				options: [
					{ name: 'Post', value: 'tweet' },
					{ name: 'User', value: 'user' },
					{ name: 'Account', value: 'account' },
				],
			},
			...(['tweet', 'user', 'account'] as const).map((resource) => ({
				displayName: 'Operation',
				name: 'operation',
				type: 'options' as const,
				noDataExpression: true,
				displayOptions: { show: { resource: [resource] } },
				default: OPERATIONS[resource][0].name,
				options: OPERATIONS[resource].map((spec) => ({
					name: spec.displayName,
					value: spec.name,
					description: `${spec.description}. ${spec.credits}`,
					action: `${spec.displayName} ${resource === 'tweet' ? 'post' : resource}`,
				})),
			})),
			{
				displayName: 'Query',
				name: 'q',
				type: 'string',
				required: true,
				default: '',
				placeholder: 'from:vercel since:2026-09-01 -filter:replies',
				description:
					'x.com search syntax. Operators: from:, to:, since:YYYY-MM-DD, until:, min_faves:, lang:, "exact phrase", OR, and - to exclude.',
				displayOptions: { show: { resource: ['tweet'], operation: ['search'] } },
			},
			{
				displayName: 'Product',
				name: 'product',
				type: 'options',
				default: 'Latest',
				description:
					'Latest is always available. Top is refused to some reading sessions, and the refusal is free.',
				options: ['Latest', 'Top', 'People', 'Photos', 'Videos'].map((value) => ({
					name: value,
					value,
				})),
				displayOptions: { show: { resource: ['tweet'], operation: ['search'] } },
			},
			{
				displayName: 'Post ID',
				name: 'tweetId',
				type: 'string',
				required: true,
				default: '',
				placeholder: '1968000000000000000',
				description: 'Numeric id of the post',
				displayOptions: { show: { resource: ['tweet'], operation: tweetIdOperations } },
			},
			{
				displayName: 'Post IDs',
				name: 'tweetIds',
				type: 'string',
				required: true,
				default: '',
				placeholder: '20,21,22',
				description: 'Numeric post ids, comma separated. At most 100 in one request.',
				displayOptions: { show: { resource: ['tweet'], operation: ['getMany'] } },
			},
			{
				displayName: 'Handle',
				name: 'handle',
				type: 'string',
				required: true,
				default: '',
				placeholder: 'vercel',
				description: 'X handle, with or without the leading @',
				displayOptions: { show: { resource: ['user'], operation: ['get'] } },
			},
			{
				displayName: 'Handles',
				name: 'handles',
				type: 'string',
				required: true,
				default: '',
				placeholder: 'x,github,vercel',
				description: 'X handles, comma separated. At most 100 in one request.',
				displayOptions: { show: { resource: ['user'], operation: ['getMany'] } },
			},
			{
				displayName: 'User',
				name: 'user',
				type: 'string',
				required: true,
				default: '',
				placeholder: 'vercel',
				description: 'X handle (with or without @) or numeric user id',
				displayOptions: { show: { resource: ['user'], operation: userOperations } },
			},
			{
				displayName: 'Return All',
				name: 'returnAll',
				type: 'boolean',
				default: false,
				description:
					'Whether to follow the cursor until the data runs out. Every page costs credits, so set a Limit while you are building the flow.',
				displayOptions: {
					show: { resource: ['tweet', 'user'], operation: [...paged('tweet'), ...paged('user')] },
				},
			},
			{
				displayName: 'Limit',
				name: 'limit',
				type: 'number',
				typeOptions: { minValue: 1 },
				default: 20,
				description: 'Max number of results to return',
				displayOptions: {
					show: {
						resource: ['tweet', 'user'],
						operation: [...paged('tweet'), ...paged('user')],
						returnAll: [false],
					},
				},
			},
			{
				displayName: 'Options',
				name: 'options',
				type: 'collection',
				placeholder: 'Add option',
				default: {},
				displayOptions: { show: { resource: ['tweet', 'user'] } },
				options: [
					{
						displayName: 'Skip Cache',
						name: 'fresh',
						type: 'boolean',
						default: false,
						description:
							'Whether to bypass the cache and read X again. Costs double. Leave it off unless the data must be seconds old.',
					},
					{
						displayName: 'Include Response Metadata',
						name: 'includeMetadata',
						type: 'boolean',
						default: false,
						description:
							'Whether to add _meta to every item with credits_charged, balance_remaining, cache and next_cursor',
					},
					{
						displayName: 'Max Pages',
						name: 'maxPages',
						type: 'number',
						typeOptions: { minValue: 1 },
						default: 50,
						description:
							'Safety stop for Return All. The node stops after this many pages even if the cursor continues.',
					},
				],
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const out: INodeExecutionData[] = [];

		for (let i = 0; i < items.length; i++) {
			try {
				const resource = this.getNodeParameter('resource', i) as string;
				const operation = this.getNodeParameter('operation', i) as string;
				const spec = findOperation(resource, operation);
				const options = this.getNodeParameter('options', i, {}) as IDataObject;

				const params: Params = {
					q: this.getNodeParameter('q', i, '') as string,
					product: this.getNodeParameter('product', i, '') as string,
					tweetId: this.getNodeParameter('tweetId', i, '') as string,
					tweetIds: this.getNodeParameter('tweetIds', i, '') as string,
					handle: this.getNodeParameter('handle', i, '') as string,
					handles: this.getNodeParameter('handles', i, '') as string,
					user: this.getNodeParameter('user', i, '') as string,
					fresh: options.fresh === true ? true : undefined,
				};

				const base: IDataObject = {};
				for (const [key, value] of Object.entries(spec.query?.(params) ?? {})) {
					if (value !== undefined && value !== '') base[key] = value;
				}
				if (params.fresh) base.fresh = true;

				const returnAll = spec.paged
					? (this.getNodeParameter('returnAll', i, false) as boolean)
					: false;
				const limit = spec.paged ? (this.getNodeParameter('limit', i, 20) as number) : 0;
				const maxPages = Math.max(1, (options.maxPages as number) ?? 50);
				const includeMetadata = options.includeMetadata === true;

				let cursor: string | undefined;
				let collected = 0;
				let pages = 0;

				do {
					const qs: IDataObject = { ...base };
					if (spec.paged) {
						if (!returnAll) qs.count = pageSize(limit - collected);
						else qs.count = MAX_PAGE;
					}
					if (cursor) qs.cursor = cursor;

					const request: IHttpRequestOptions = {
						method: 'GET',
						baseURL: BASE_URL,
						url: spec.path(params),
						qs,
						headers: { accept: 'application/json' },
						json: true,
					};
					const body = (await this.helpers.httpRequestWithAuthentication.call(
						this,
						'xdataapiApi',
						request,
					)) as IDataObject;

					const meta = includeMetadata
						? {
								_meta: {
									credits_charged: body.credits_charged,
									balance_remaining: body.balance_remaining,
									cache: body.cache,
									next_cursor: body.next_cursor,
									request_id: body.request_id,
								},
							}
						: {};

					if (spec.collection === 'single') {
						const single = (body.data as IDataObject) ?? body;
						out.push({ json: { ...single, ...meta }, pairedItem: { item: i } });
						break;
					}

					const rows = Array.isArray(body.data) ? (body.data as IDataObject[]) : [];
					for (const row of rows) {
						// Follower ids come back as bare strings, not objects.
						const json =
							row !== null && typeof row === 'object' ? { ...row, ...meta } : { id: row, ...meta };
						out.push({ json, pairedItem: { item: i } });
					}
					collected += rows.length;
					pages += 1;

					// Errors for a batch request name the inputs that were skipped.
					if (Array.isArray(body.errors) && body.errors.length > 0 && includeMetadata) {
						out.push({ json: { _errors: body.errors }, pairedItem: { item: i } });
					}

					cursor = typeof body.next_cursor === 'string' ? body.next_cursor : undefined;
					if (rows.length === 0) break;
				} while (
					spec.paged &&
					cursor &&
					pages < maxPages &&
					(returnAll || collected < limit)
				);
			} catch (error) {
				if (this.continueOnFail()) {
					out.push({
						json: { error: (error as Error).message },
						pairedItem: { item: i },
					});
					continue;
				}
				if (error instanceof NodeOperationError || error instanceof NodeApiError) throw error;
				throw new NodeApiError(this.getNode(), error as never, { itemIndex: i });
			}
		}

		return [out];
	}
}
