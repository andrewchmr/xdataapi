// Vercel AI SDK against the hosted MCP server, so the tool list comes from the
// server and stays current when endpoints are added.
// npm install ai @ai-sdk/anthropic @modelcontextprotocol/sdk
//
// The server speaks Streamable HTTP, not SSE, so pass the transport object
// rather than the { type: 'sse' } shorthand.
import { anthropic } from '@ai-sdk/anthropic';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
import { experimental_createMCPClient as createMCPClient, generateText, stepCountIs } from 'ai';

const mcp = await createMCPClient({
  transport: new StreamableHTTPClientTransport(new URL('https://api.xdataapi.io/mcp'), {
    requestInit: { headers: { 'x-api-key': process.env.XDATAAPI_KEY! } },
  }),
});

try {
  const { text } = await generateText({
    model: anthropic('claude-opus-5'),
    tools: await mcp.tools(),
    stopWhen: stepCountIs(10),
    system:
      'You read public X data. Batch with get_users and get_tweets instead of looping single ' +
      'reads. Ask for the count you need: every result costs a credit.',
    prompt: 'What has @vercel posted this week? Summarise in five lines.',
  });
  console.log(text);
} finally {
  await mcp.close();
}
