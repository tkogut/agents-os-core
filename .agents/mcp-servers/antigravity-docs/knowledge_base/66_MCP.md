# MCP
Source URL: https://antigravity.google/docs/mcp

Features
Extend
MCP
Markdown
AVAILABLE ON:
Antigravity 2.0
Antigravity CLI
Antigravity IDE
Model Context Protocol (MCP)
Section titled “Model Context Protocol (MCP)”

Antigravity supports the Model Context Protocol (MCP), an open standard that lets AI agents and editors securely connect to local developer tools, databases, file parsers, and external remote APIs. This integration provides the AI model with real-time context and execution capabilities beyond your immediate workspace.

In this guide, you’ll learn how to connect and configure MCP servers across Antigravity products.

What is MCP?
Section titled “What is MCP?”

MCP acts as a universal bridge between Antigravity and your broader development environment. Instead of manually copying and pasting database schemas, logs, or API specifications into prompts or chat panels, MCP lets Antigravity fetch structured context directly or execute safe actions on your behalf when needed.

Add context
Section titled “Add context”

With MCP, Antigravity can use live data from connected MCP servers to inform its reasoning and suggestions:

When writing a SQL query, Antigravity can inspect your live Neon, Supabase, or AlloyDB schema to suggest correct table and column names.
When debugging deployment failures, Antigravity can pull recent build logs directly from Netlify or Heroku.
Add custom tools
Section titled “Add custom tools”

With MCP, Antigravity can execute specific, safe actions defined by your connected servers:

Create a Linear issue for a TODO item.
Search Notion or GitHub for authentication patterns.
Getting started by surface
Section titled “Getting started by surface”
Antigravity 2.0
Antigravity CLI
Antigravity IDE
Antigravity 2.0

In Antigravity 2.0, you can manage your MCP servers through the Installed MCP Servers section of your Settings.

To view and update your MCP servers:

Click the Settings button on the bottom left of your screen.
Select Customizations and review the Installed MCP Servers section.

To install an MCP server from the Installed MCP Servers section:

Click Add MCP. This connects you to the MCP Store, a searchable list of available MCP servers.
Search or scroll down to an MCP server you’d like to install.
Click Add.

To manage your MCP servers from this screen:

Uninstall: Click the trash can icon next to the MCP server in the list.
Disable or enable: Click the toggle switch next to the MCP server in the list.
Refresh: Click the refresh button.

Antigravity SDK

In Python applications built using the Antigravity SDK, you can connect MCP servers (stdio, SSE, or HTTP) programmatically under a unified execution pipeline alongside built-in tools and custom Python functions. The SDK automatically discovers servers configured in your workspace’s .agents/mcp_config.json file. For dedicated documentation and examples, refer to the Antigravity SDK MCP guide.

MCP configuration structure
Section titled “MCP configuration structure”

Whether configuring custom servers for Antigravity 2.0, Antigravity IDE, or Antigravity CLI, the configuration file follows a standardized format. The file contains a single mcpServers object where you define each server you want to connect to:

{
  "mcpServers": {
    "sqlite-explorer": {
      "command": "node",
      "args": ["/usr/local/bin/sqlite-mcp-server.js"],
      "env": {
        "SQLITE_DB_PATH": "/var/data/app.db"
      }
    },
    "my-remote-server": {
      "serverUrl": "https://api.example.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
MCP configuration properties
Section titled “MCP configuration properties”

Each server entry under mcpServers supports the following properties.

Require one of the following transport properties:

command (string): Path to the executable for stdio transport.
serverUrl (string): URL for remote Streamable HTTP or SSE servers.

Configure any of the following optional properties:

args (array of strings): Command-line arguments for stdio transport.
env (object): Environment variables for the stdio server process.
cwd (string): Working directory for stdio servers.
headers (object): Custom HTTP headers for remote servers.
authProviderType (string): Authentication provider. Supports "google_credentials" for Google Application Default Credentials (ADC).
oauth (object): OAuth client credentials (clientId, clientSecret).
disabled (boolean): Temporarily disable a server without removing its configuration.
disabledTools (array of strings): Tool names to withhold from the model.
MCP authentication
Section titled “MCP authentication”

Connected MCP servers can securely authenticate against external services using built-in Google credentials, automatic OAuth flows, or custom HTTP headers.

Google credentials
Section titled “Google credentials”

Set authProviderType to "google_credentials" to use Google Application Default Credentials (ADC):

{
  "mcpServers": {
    "my-gcp-service": {
      "serverUrl": "https://example.googleapis.com/mcp/",
      "authProviderType": "google_credentials"
    }
  }
}

This requires Application Default Credentials to be configured locally. To set them up, run:

gcloud auth application-default login

If you previously logged in, ensure your quota project is set by running:

gcloud auth application-default set-quota-project {QUOTA_PROJECT}
OAuth
Section titled “OAuth”

Antigravity automatically handles OAuth for servers that support dynamic client registration (DCR). For these servers, no additional configuration is needed:

{
  "mcpServers": {
    "oauth-server": {
      "serverUrl": "https://api.example.com/mcp/"
    }
  }
}

If the server doesn’t support dynamic client registration, you can provide your client credentials manually:

{
  "mcpServers": {
    "oauth-server": {
      "serverUrl": "https://api.example.com/mcp/",
      "oauth": {
        "clientId": "your-client-id",
        "clientSecret": "your-client-secret"
      }
    }
  }
}

If you provide client credentials manually, ensure the following URL is registered as a redirect URI in your OAuth provider:

https://antigravity.google/oauth-callback

To connect to an OAuth-enabled server:

Open Agent settings with CMD + , (macOS) or CTRL + , (Windows and Linux).

Navigate to the Customizations tab and click Authenticate next to the server.

Complete authentication in your browser and copy the authorization code.

Paste the code back into the settings panel and click Submit.

Once authenticated, the server reconnects automatically.

Access tokens are stored in ~/.gemini/antigravity/mcp_oauth_tokens.json. Expired tokens are refreshed automatically, and invalid tokens are removed.

Custom headers
Section titled “Custom headers”

For remote servers that require custom HTTP headers (such as API keys or bearer tokens), add them to the headers object. For example:

{
  "mcpServers": {
    "my-remote-server": {
      "serverUrl": "https://api.example.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
MCP permissions and access control
Section titled “MCP permissions and access control”

Access to Model Context Protocol tools and resources is governed by Antigravity’s permissions system. By default, unconfigured MCP tools run in Ask mode, requiring your approval before execution. You can allow specific tools or entire servers in your policy configuration:

mcp(server/tool): Matches a specific tool on a specific server.
mcp(server/*): Matches all tools on a specified server.
mcp(*): Global wildcard matching any MCP tool across all connected servers.
Supported MCP servers
Section titled “Supported MCP servers”

The MCP Store features direct integrations for a wide variety of developer platforms, databases, and productivity services:

Databases and storage (15 servers)
AlloyDB for PostgreSQL
BigQuery
Bigtable Admin remote MCP
ClickHouse
Cloud SQL (MySQL, PostgreSQL, SQL Server, Managed)
Dataplex
MCP Toolbox for Databases
MongoDB
Neo4j
Neon
Pinecone
Prisma
Redis
Spanner
Supabase
Developer tools and CI/CD (17 servers)
Apigee MCP
Atlassian
Cloud CLI Execution
Forge
GitHub
GitLab Orbit
GKE OneMCP
Harness
Heroku
Home Developer MCP
Linear
mabl
Netlify
Opsera AI Agents
Postman
SonarQube
Vercel
Frontend and design (8 servers)
Canva
Chrome DevTools
Dart
Figma Dev Mode MCP
Locofy
Lovable MCP
Miro
Mobbin MCP
Security (4 servers)
CrowdStrike
Endor Labs
Splunk
Wiz
Analytics, AI, and cloud (32 servers)
Airweave
Antimetal
Arize
Cloud Audit Manager
Courtroom5
Daloopa
Docusign
Exa
FactSet AI-Ready Data
Finnhub
Firebase
Fiscal.ai
Google Cloud Quotas
Grafana Cloud
Guidepoint
Harvey
iManage
LegalZoom
Looker
LSEG
NetDocuments
Notion
Parallel Search
PayPal
Perplexity Ask
PostHog
Relativity
S&P Global
Salesforce
Sequential Thinking
Stripe
Windsor AI
Previous
Voice dictation (/voice)
Next
Agent skills
About Google
Google Products
Privacy
Terms