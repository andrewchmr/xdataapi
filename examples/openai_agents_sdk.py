"""OpenAI Agents SDK against the hosted MCP server. pip install openai-agents

Two ways in. The first runs the MCP client in your process and works with any
model the SDK can drive. The second hands the server to OpenAI's own Responses
API, which calls it for you.
"""

import asyncio
import os

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

KEY = os.environ["XDATAAPI_KEY"]


async def main() -> None:
    # The MCP client runs here. Works with any model.
    async with MCPServerStreamableHttp(
        name="xdataapi",
        params={
            "url": "https://api.xdataapi.io/mcp",
            "headers": {"x-api-key": KEY},
        },
        # The catalog is stable; caching it saves a round trip per run.
        cache_tools_list=True,
    ) as server:
        agent = Agent(
            name="X researcher",
            instructions=(
                "You read public X data. Batch with get_users and get_tweets instead of "
                "looping single reads. Ask for the count you need: every result costs a "
                "credit. Check get_balance before a large read."
            ),
            mcp_servers=[server],
        )
        result = await Runner.run(agent, "What has @vercel posted this week? Summarise in five lines.")
        print(result.final_output)


# Hosted instead: OpenAI calls the server, so nothing MCP runs in your process.
#
# from agents import HostedMCPTool
#
# agent = Agent(
#     name="X researcher",
#     tools=[
#         HostedMCPTool(
#             tool_config={
#                 "type": "mcp",
#                 "server_label": "xdataapi",
#                 "server_url": "https://api.xdataapi.io/mcp",
#                 "headers": {"x-api-key": KEY},
#                 "require_approval": "never",
#             }
#         )
#     ],
# )

if __name__ == "__main__":
    asyncio.run(main())
