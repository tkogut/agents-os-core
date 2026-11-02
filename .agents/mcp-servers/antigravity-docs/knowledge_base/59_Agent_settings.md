# Agent settings
Source URL: https://antigravity.google/docs/agent-settings

Agent settings2-0Antigravity AppFeaturesAgent settings Antigravity App FeaturesAntigravity AppAntigravity CLI
Features
Learn
Settings
Agent settings
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Agent settings
Section titled “Agent settings”

Configure how the Antigravity agent executes terminal commands, modifies files, and uses the terminal sandbox across the desktop application and CLI.

Antigravity App
Antigravity CLI
Antigravity CLI
Agent execution and permission settings
Section titled “Agent execution and permission settings”

Antigravity CLI lets you configure how the agent edits files, runs shell commands, and enforces workspace boundaries through /config (/settings), ~/.gemini/antigravity-cli/settings.json, or command-line flags:

Agent Mode (agentMode / --mode): Controls the session execution mode (cycle during a session with SHIFT + TAB):
default (the default; leave agentMode unset): Prompts for interactive diff review before modifying or creating files.
accept-edits: Automatically approves workspace file edits and creations.
auto (Preview): Automatically approves workspace file edits, runs terminal commands inside the Terminal sandbox by default, and automatically evaluates commands that need to run outside the sandbox so safe, reversible commands run without prompting while risky or irreversible commands pause for approval. When active, the bottom-right status bar shows auto and the prompt input displays Auto mode: edits & safe commands auto-approved (shift+tab to cycle).
plan: Analyzes the codebase and outlines a plan before making edits.
Tool Permission (toolPermission): Controls the baseline authorization policy for tools:
request-review (default): Prompts for approval before running write, shell, or web tools.
proceed-in-sandbox: Automatically runs sandboxed terminal commands and prompts when commands need to run outside the sandbox.
strict: Prompts before all non-read tool calls (overrides auto mode).
always-proceed: Runs all tools without prompting (overrides auto mode; also activated by --dangerously-skip-permissions).
Sandbox Mode (enableTerminalSandbox / --sandbox): Restricts agent shell commands to an OS-level container boundary (false by default, and enabled automatically in auto mode).
Non-Workspace Access (allowNonWorkspaceAccess): Controls whether the agent can read or write files outside your active workspace directories (false by default).

Note

auto mode is available in v1.3.5+ on macOS and Linux and v1.4.4+ on Windows. Starting in v1.4.4, if the terminal sandbox isn’t available on your machine, auto and proceed-in-sandbox aren’t offered, and Sandbox Mode has no effect. To learn more, refer to Terminal sandbox.

Example configuration
Section titled “Example configuration”

Configure your preferred agent execution settings in ~/.gemini/antigravity-cli/settings.json:

{
    "agentMode": "auto"
}

To learn more, refer to Choose an execution mode, Settings, Agent permissions, and Terminal sandbox.

Previous
Overview
Next
Artifact review
About Google
Google Products
Privacy
Terms