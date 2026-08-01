# Plugins
Source URL: https://antigravity.google/docs/ide/plugins

Antigravity IDE
>
Customizations
>
Plugins
Pluginslink

Plugins are namespaced bundles that allow you to extend Antigravity’s capabilities by grouping skills, rules, MCP servers, and hooks into a single package.

Directory Structurelink

If you want to create your own plugins or inspect existing ones, they follow a specific directory structure. A plugin is a directory containing a plugin.json file and optional subdirectories for different customization types:

text
content_copy
plugins/<plugin-name>/
├── plugin.json       # Required marker file
├── mcp_config.json   # Optional MCP server definitions
├── hooks.json        # Optional hooks definition
├── skills/           # Optional skills
│   └── <skill-name>/
│       └── SKILL.md
└── rules/            # Optional rules
    └── <rule-name>.md
Manifest File (plugin.json)link

Every plugin must have a plugin.json file at its root. This file identifies the directory as a plugin.

json
content_copy
{
  "name": "my-custom-plugin"
}

The name field is optional and defaults to the directory name if omitted.

Supported Componentslink

A plugin can contain the following components:

Skills: Located in the skills/ subdirectory. Each skill must have a SKILL.md file containing instructions for the agent.
Rules: Located in the rules/ subdirectory. These are markdown files that define constraints or guidelines for the agent’s behavior.
MCP Servers: Configured via mcp_config.json at the plugin root. This allows you to connect Antigravity to external tools and services.
Hooks: Configured via hooks.json at the plugin root. These allow you to run scripts or commands when specific events occur.
How to Add Pluginslink

There are two ways to add plugins to Antigravity:

1. Using Bundled Plugins (Build with Google)link

Antigravity comes with a variety of bundled plugins created by Google. You can browse and add these plugins directly from the user interface:

Navigate to the Customizations page.
For more details about the available Google-built plugins, see the Build with Google Page.
2. Manually Adding Pluginslink

You can also add custom plugins by placing your plugin folders in one of the designated plugin locations. Antigravity automatically scans these directories to discover and load your customizations:

Workspace Level: Place your plugin folder inside a .agents/plugins/ or _agents/plugins/ directory at the root of your opened workspace. This makes the plugin available only when working in this specific workspace.
Global Level: Place your plugin folder inside ~/.gemini/config/plugins/ in your user home directory. This makes the plugin active across all workspaces.
Workflows
Hooks