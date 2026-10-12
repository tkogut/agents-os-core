# Plugins
Source URL: https://antigravity.google/docs/plugins

Features
Learn
Plugins
Markdown
AVAILABLE ON:
Antigravity 2.0
Antigravity CLI
Antigravity IDE
Plugins
Section titled “Plugins”

Plugins package reusable skills, background subagents, linting rules, Model Context Protocol (MCP) servers, and lifecycle hooks into a single deployable asset.

Directory structure
Section titled “Directory structure”

A plugin is a directory containing a required manifest file (plugin.json) and optional subdirectories for different customization types:

plugins/<plugin-name>/
├── plugin.json       # Required marker and manifest file
├── mcp_config.json   # Optional MCP server definitions
├── hooks.json        # Optional hooks definition
├── skills/           # Optional skills directory
│   └── <skill-name>/
│       └── SKILL.md
├── agents/           # Optional subagent definition templates
│   └── <agent-name>.md
└── rules/            # Optional rules directory
    └── <rule-name>.md
Manifest file (plugin.json)
Section titled “Manifest file (plugin.json)”

Every plugin requires a plugin.json file at its root to identify the directory as a plugin and define its metadata:

{
  "$schema": "https://antigravity.google/schemas/v1/plugin.json",
  "name": "my-custom-plugin",
  "description": "A brief description of what my plugin does."
}
Field reference
Section titled “Field reference”
Field	Type	Required	Description
name	String	Yes (CLI) / Optional (2.0 and IDE)	The unique, machine-readable name of the plugin (matches ^[a-zA-Z0-9-_]+$). Required when managing plugins using Antigravity CLI commands; defaults to the folder name if omitted in Antigravity 2.0 or Antigravity IDE.
description	String	No	A brief human-readable description of the plugin’s purpose, displayed in plugin listings.
Automatic validation
Section titled “Automatic validation”

To enable automatic autocomplete and validation in editors like VS Code or JetBrains IDEs, include the $schema key pointing to the official schema URL:

"$schema": "https://antigravity.google/schemas/v1/plugin.json"
Full JSON schema
Section titled “Full JSON schema”
{
  "$schema": "https://antigravity.google/schemas/v1/plugin.json",
  "title": "Antigravity Plugin Manifest",
  "description": "Schema for Antigravity plugin manifest files (plugin.json)",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "The unique, machine-readable name of the plugin. Must contain only alphanumeric characters, hyphens, and underscores.",
      "pattern": "^[a-zA-Z0-9-_]+$"
    },
    "description": {
      "type": "string",
      "description": "A brief human-readable description of the plugin's purpose and capabilities."
    }
  },
  "required": ["name"],
  "additionalProperties": false
}
Supported components
Section titled “Supported components”

A plugin can contain any of the following components:

skills/: Subdirectories containing a SKILL.md file with instructions for the agent.
agents/: Markdown files defining custom subagents and persona configurations.
rules/: Markdown files defining behavioral constraints or style guidelines.
mcp_config.json: Declarations connecting Antigravity to external tool servers.
hooks.json: Event handlers executing shell commands before or after tool calls.
Managing plugins by surface
Section titled “Managing plugins by surface”

Follow the instructions below to install and manage plugins on your preferred surface:

Antigravity 2.0
Antigravity CLI
Antigravity IDE
Antigravity 2.0
Marketplace and bundled plugins
Section titled “Marketplace and bundled plugins”

Antigravity 2.0 provides curated plugins that you can browse and install directly from the application interface:

Open the Customizations tab, located below the Scheduled Tasks tab in the left sidebar.
Switch between the Marketplace view (which displays all plugins available to you) and the Installed tab (which displays only your installed plugins).
In the Marketplace tab, click the + button to install a plugin, or click a plugin’s name to view what is included in the bundle (such as skills, MCP servers, rules, and agents).

For a complete walkthrough of plugin discovery and cross-surface synchronization, refer to the Marketplace guide.

Note

Cross-surface synchronization: Plugins installed in Antigravity 2.0 are automatically updated and shown in the Antigravity CLI’s Installed tab.

Manual plugin installation
Section titled “Manual plugin installation”

You can install custom plugins by placing their directories in either of the following locations:

Workspace level: Place your plugin folder in .agents/plugins/ at the root of your workspace. The plugin activates only when working in that project.
Global level: Place your plugin folder in ~/.gemini/config/plugins/. The plugin activates across all workspaces on your workstation.
Previous
Marketplace
Next
Terminal sandbox
About Google
Google Products
Privacy
Terms