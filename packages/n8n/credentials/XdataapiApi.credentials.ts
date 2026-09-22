import type {
	IAuthenticateGeneric,
	ICredentialTestRequest,
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class XdataapiApi implements ICredentialType {
	name = 'xdataapiApi';

	displayName = 'xdataapi API';

	documentationUrl = 'https://xdataapi.io/docs';

	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: { password: true },
			default: '',
			required: true,
			placeholder: 'xd_live_...',
			description:
				'Key from <a href="https://xdataapi.io/dashboard" target="_blank">xdataapi.io/dashboard</a>. New keys start with 5,000 free credits, no card.',
		},
	];

	authenticate: IAuthenticateGeneric = {
		type: 'generic',
		properties: {
			headers: {
				'x-api-key': '={{$credentials.apiKey}}',
			},
		},
	};

	/** Free call. It reports the balance, so a green tick also proves there are credits. */
	test: ICredentialTestRequest = {
		request: {
			baseURL: 'https://api.xdataapi.io',
			url: '/v1/me',
		},
	};
}
