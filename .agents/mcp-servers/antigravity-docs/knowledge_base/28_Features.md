# Features
Source URL: https://antigravity.google/docs/cli/features

Antigravity CLI
>
Features
Antigravity CLI Featureslink
Pluginslink

How Plugins Work
Plugins are namespaced bundles that can contain skills, agents, rules, MCP servers, and hooks as a single deployable unit.

When you install a plugin, the CLI stages the files in your home directory under ~/.gemini/antigravity-cli/plugins/<plugin_name>/. The Antigravity Agent automatically discovers and loads these staged customizations.

content_copy
~/.gemini/antigravity-cli/
├── plugins/
│   └── <plugin_name>/
│       ├── plugin.json         # Required marker file
│       ├── mcp_config.json     # Optional MCP server definitions
│       ├── hooks.json          # Optional event hooks definition
│       ├── skills/             # Optional skills
│       ├── agents/             # Optional subagents
│       └── rules/              # Optional rules
└── import_manifest.json        # Tracking manifest

Accessing Plugin Components
Once staged and loaded, you can interact with the plugin components inside the CLI using slash commands.

Terminal Sandboxlink

The Terminal Sandbox is a lightweight security isolation mechanism that protects your host system from potentially destructive file manipulations or unauthorized outbound network requests when the agent executes local shell commands.

Rather than running heavy virtual machines or containers, the CLI leverages native operating system features (nsjail on Linux, sandbox-exec on macOS, and AppContainer on Windows) to enforce strict containment boundaries with zero startup overhead.

Configuration
You can configure the sandbox behavior in your settings.json file (located at ~/.gemini/antigravity-cli/settings.json):

json
content_copy
{
  "enableTerminalSandbox": true
}
enableTerminalSandbox (boolean, default: false): Enables general execution containment barriers on all local agent processes.

Interactive Approvals
When the agent proposes a terminal command that requires your confirmation, the CLI prompt adapts dynamically based on your settings:

When the Sandbox is Enabled: The confirmation prompt will include a specific option to Yes, and run without sandbox restrictions if you need to temporarily bypass the containment boundary for a single trusted command.
When the Sandbox is Disabled: The prompt will include an option to Yes, and run in sandbox if you want to force a specific, potentially risky command to execute within the safety boundary.
CLI Slash Commands Referencelink

The Antigravity CLI supports a variety of slash commands typed directly into the prompt box to manage conversations, configure settings, and inspect agent capabilities.

Core Slash Commandslink
Command	Category	Purpose
/resume (alias /switch)	Conversation	Open the conversation picker to resume or switch sessions.
/rewind (alias /undo)	Conversation	Roll back conversation history to a previous checkpoint.
/rename <name>	Conversation	Rename the active conversation thread for easier tracking.
/permissions	Configuration	Select agent autonomy level (request-review, always-proceed, or strict).
/model	Configuration	Select the default reasoning model (persists across sessions).
/keybindings	Configuration	Open the interactive keyboard shortcut editor.
/statusline	Configuration	Customize real-time indicators displayed in the CLI status bar.
/tasks	Tools & Monitoring	Monitor, view logs for, or terminate active background tasks.
/skills	Tools & Monitoring	Browse local and global encapsulated agent workflows.
/mcp	Tools & Monitoring	Open the panel to configure and manage Model Context Protocol servers.
/open <path>	Utility	Immediately open a file in your preferred external editor.
/diff	Utility	Open the interactive diff viewer to review changes and steer the agent.
/usage	Utility	Open the inline interactive help manual inside the terminal.
/logout	Account	Log out of your Google session and clear cached credentials.
Advanced Customization via settings.jsonlink

For power users, several slash commands support deep customization via your ~/.gemini/antigravity-cli/settings.json configuration:

Fine-Grained Permissions: Instead of global levels, define specific allowed/denied commands:
json
content_copy
"permissions": {
  "allow": ["command(git)", "command(npm test)"],
  "deny": ["command(rm -rf)"]
}
Custom Status Line & Window Titles: You can pipe live agent metadata (JSON format containing CWD, active model, token usage, state, etc.) directly into your own custom shell scripts to generate dynamic status bars or terminal window titles.
Subagents in Antigravity CLIlink

Antigravity CLI features an asynchronous subagents framework that allows the main agent to delegate parallel work, perform background research, and run system tests without blocking your active conversation.

What are Subagents?
Subagents are independent, concurrent agent sessions designed to tackle specific background tasks in parallel with the main conversation.

Purpose: The main agent automatically spawns subagents to perform background operations such as looking up documentation, running builds, or validating a fix.
Capabilities: Subagents have full access to tools such as code search, file editing, terminal commands, and web searches to complete their assigned tasks.
The main agent decides what tools and permissions subagents get, including whether they can use MCP tools and if they can write files.
Managing Agents: The /agents Panellink

Antigravity CLI provides an interactive terminal UI to view, manage, and approve actions for running subagents.

Access: Type /agents in the prompt to open the subagents panel.
Overview: The panel shows a list of active and completed subagents, including surface-level details such as their status (running, done, killed, etc.) and the current step they are executing.
info
Selecting a subagent from the panel opens a full-screen detail view. This view shows the entirety of the subagent’s conversation, including its steps, thoughts, and tool execution logs.

Tool Confirmations & Approvals
When a subagent wants to execute a tool that requires user permissions (such as running a local command or writing a file), it will surface the request. You can manage approvals in two ways:

Detail View Approvals
The Subagent Detail View features an interaction section containing all pending approvals, where you can selectively approve or deny requests.

lightbulb
Tip: Use the keyboard shortcut ctrl+j to “teleport” from the main conversation directly to the detailed view of the next subagent waiting for your approval.

Fast Path Alerts
To keep you in your flow, Antigravity CLI displays a Fast Path Alert directly above your prompt box when a subagent requests permission.

lightbulb
Tip: You can approve a pending subagent permission instantly using ctrl+k without ever having to switch away from the main conversation.
Using AGY CLI
Migration