# MCP
Source URL: https://antigravity.google/docs/sdk/mcp

Antigravity SDK
MCP
Markdown
Model Context Protocol (MCP) integration
Section titled “Model Context Protocol (MCP) integration”

Connect external Model Context Protocol (MCP) servers to your Antigravity SDK agents.

In Python applications built using the Antigravity SDK, MCP servers (stdio or Streamable HTTP) are connected programmatically under a unified execution pipeline alongside built-in tools and custom Python functions.

Programmatic MCP server setup
Section titled “Programmatic MCP server setup”

You can define MCP servers programmatically in your application’s LocalAgentConfig using McpStdioServer or McpStreamableHttpServer.

For example, you can configure an agent to connect to an external SQLite MCP server using stdio:

import asyncio
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.types import McpStdioServer

config = LocalAgentConfig(
    mcp_servers=[
        McpStdioServer(
            name="sqlite-explorer",
            command="node",
            args=["/usr/local/bin/sqlite-mcp-server.js"],
            env={"SQLITE_DB_PATH": "/var/data/app.db"},
        )
    ]
)

async def main():
    async with Agent(config) as agent:
        response = await agent.chat("Query database metrics.")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())

For more details on MCP protocol capabilities across the Antigravity suite, check out the central Model Context Protocol guide.

Sample code
Section titled “Sample code”

For full working code examples, check out the GitHub repository:

mcp_tools.py
Previous
Tools and skills
Next
Policies
About Google
Google Products
Privacy
Terms