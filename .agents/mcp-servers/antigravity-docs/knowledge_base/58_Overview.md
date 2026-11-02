# Overview
Source URL: https://antigravity.google/docs/settings

Settings2-0Antigravity AppFeaturesSettings Antigravity App FeaturesAntigravity AppAntigravity CLIAntigravity IDE
Features
Learn
Settings
Overview
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Antigravity IDE
Settings
Section titled “Settings”

Configure preferences, execution boundaries, command permissions, and tool telemetry across Antigravity surfaces.

Antigravity App
Antigravity CLI
Antigravity IDE
Antigravity CLI

Configure persistent preferences, customize keyboard shortcuts, toggle terminal display buffers, and manage runtime CLI parameter overrides.

Setting up preferences
Section titled “Setting up preferences”

Antigravity CLI stores user preferences in a minimal, forward-compatible JSON configuration profile.

Configuration file location
Section titled “Configuration file location”

The persistent settings are saved in a plain JSON format:

~/.gemini/antigravity-cli/settings.json

The CLI leverages sparse persistence by writing only values to disk that differ from their system defaults. This keeps your configuration file clean, minimal, and fully forward-compatible with future updates.

Editor autocomplete and validation
Section titled “Editor autocomplete and validation”

Antigravity publishes a JSON Schema for settings.json. Editors that support JSON Schema, such as VS Code and JetBrains IDEs, use it for autocomplete, hover descriptions, and validation. To turn it on, add a $schema key at the top of the file:

{
  "$schema": "https://antigravity.google/schemas/v1/settings.json",
  "agentMode": "accept-edits",
  "colorScheme": "tokyo night",
  "notifications": true
}

The CLI ignores $schema and keeps it when it saves the file.

Other configuration files
Section titled “Other configuration files”

Keyboard shortcuts, hooks, MCP servers, and plugins are configured in their own files:

Keyboard shortcuts: ~/.gemini/antigravity-cli/keybindings.json. /keybindings opens the file in your editor. Refer to Keybindings configuration.
Hooks: ~/.gemini/config/hooks.json for all workspaces, or <workspace>/.agents/hooks.json for one workspace. /hooks adds, edits, and turns hooks on or off, and saves new hooks to the global file. Hooks don’t go in settings.json: the CLI keeps a hooks key there but never loads it. Refer to Hooks.
MCP servers: ~/.gemini/config/mcp_config.json for all workspaces, which you can manage with /mcp, or <workspace>/.agents/mcp_config.json for one workspace. Use names that differ from your global servers: when two files use the same name, the server that is already running keeps it. Refer to MCP.
Plugins: Installed in ~/.gemini/config/plugins/<plugin>/, or in <workspace>/.agents/plugins/<plugin>/ for one workspace. Each plugin can have a plugin.json manifest, described by the plugin manifest schema. Refer to Plugins.
How the CLI reads and saves settings.json
Section titled “How the CLI reads and saves settings.json”
Only non-default values are saved. When you change a setting with /config, /model, /effort, /statusline, /title, or /permissions, or choose to always allow or deny an action at a permission prompt, the CLI saves only the keys whose values differ from the defaults. Setting an option back to its default removes its key. The CLI replaces the file in one step and makes it readable only by your user (0600).
The file is normalized at startup. When the CLI starts with a valid file, it rewrites the file in its own format, which also removes keys that are set to their default values.
Unknown keys are kept. The CLI ignores keys it doesn’t recognize, such as $schema or a setting from a newer version, and keeps them when it saves the file.
Problems are reported before your session starts. If a key has the wrong type or an unrecognized value, or the file isn’t valid JSON, the CLI opens a Settings Error screen that names the file and the problem. The file isn’t changed until you choose what to do.

For example, an unrecognized colorScheme value opens this screen:

The screen offers three choices:

Exit and fix manually: Quits the CLI so you can edit the file.
Continue with defaults this session: Starts the session without changing the file. For an invalid value, the CLI uses the default for that key and applies the rest of your settings, and the next time it saves a setting, it drops the invalid value. If the file isn’t valid JSON, the CLI uses all defaults and doesn’t save any setting changes until you fix the file.
Overwrite the file with defaults: After you confirm, saves a copy of the file next to it as settings.json.corrupted.<timestamp> and resets every setting to its default, including the permission rules in the file.
The interactive settings panel
Section titled “The interactive settings panel”

To edit settings directly inside your active terminal session without opening raw JSON files:

Type /config (or its alias /settings) inside the prompt panel and press ENTER. The Settings panel opens below the prompt and lists each setting with its current value:

Navigate between available options using ↑/↓, or start typing to filter the list in Search.

Press ←/→ to change the highlighted setting, or press ENTER to open its options, highlight a value, and press ENTER to save. Changes are saved right away.

Press ESC to close the panel. If you’ve typed in Search, the first ESC clears it. In an open option list, ESC cancels.

Command-line overrides
Section titled “Command-line overrides”

You can temporarily override persistent preferences for individual terminal sessions using CLI command flags:

agy --sandbox --model="Gemini 3.8 Flash"

When a flag overrides a setting, /config names the flag after that setting’s value. For example, with --sandbox:

Sandbox Mode                 on (overridden by --sandbox)

Flag overrides apply only to the current session and aren’t saved to settings.json.

Visual rendering modes
Section titled “Visual rendering modes”

The TUI renders in one of two visual modes, set by the Rendering Mode (altScreenMode) option in /config.

Alt-screen mode (always)
Section titled “Alt-screen mode (always)”

This mode opens a dedicated display screen using the terminal’s alternate buffer, creating an immersive, standalone app interface:

Key features: Integrated scrollback, mouse-wheel scrolling support, custom rendered scrollbar, and clean terminal state restoration on exit.
Best used for: Standard local development sessions in advanced terminal emulators (such as iTerm2, Ghostty, or WezTerm).
Inline mode (never)
Section titled “Inline mode (never)”

This mode renders output sequentially directly within your terminal’s standard stdout pipeline:

Key features: Preserves entire session history inside your emulator’s native scrollback buffer, does not capture mouse inputs, and works seamlessly alongside standard command outputs.
Best used for: Remote SSH terminals, terminal multiplexers such as tmux or screen, and low-bandwidth remote sessions.

Note

Default rendering: With Rendering Mode set to default (native terminal (inline) in /config), the conversation renders inline, and full-screen views such as the diff viewer, the artifact viewer, and /help open in the alternate screen. Setting altScreenMode to never in settings.json keeps those views inline too. If your terminal doesn’t support the alternate screen, the CLI always renders inline.

Configuration options reference
Section titled “Configuration options reference”

The interactive settings panel (/config) and settings.json allow you to customize the CLI’s behavior across several categories. Each option lists its settings.json key in parentheses. For one table of every key with its type and default, refer to the CLI reference.

Safety and permissions
Section titled “Safety and permissions”

Manage how the agent interacts with your system and codebase:

Agent Mode (agentMode): Controls the session execution mode for file edits, command evaluation, and planning (can also be set per session with --mode or cycled with SHIFT + TAB; refer to Choose an execution mode):
default (the default; leave agentMode unset): Prompts for interactive diff review before modifying or creating files.
accept-edits: Automatically approves workspace file edits and creations.
auto (Preview): Automatically approves workspace file edits, runs terminal commands inside the terminal sandbox by default, and automatically evaluates commands that need to run outside the sandbox so safe, reversible commands run without prompting while risky or irreversible commands pause for approval (shown as auto in the bottom-right status bar and Auto mode: edits & safe commands auto-approved (shift+tab to cycle) in the prompt input box).
plan: Prepends /plan so the agent analyzes the codebase and outlines a plan before making edits.
Tool Permission (toolPermission): Controls when the agent asks for your approval before it uses a tool, such as running a terminal command. Deny rules in your permissions block an action in every mode:
request-review (default): Prompts for your approval before running write, bash, web, or MCP tools, unless an allow rule covers the action.
proceed-in-sandbox: Runs terminal commands without prompting when Sandbox Mode is on and the command runs inside the terminal sandbox; otherwise prompts for review.
strict: Prompts before every tool action, including file reads, even when an allow rule matches (overrides auto mode).
always-proceed: Runs terminal commands, web requests, and MCP tools without prompting, except actions that match an ask or deny rule (highest risk, use with caution; overrides auto mode).
Artifact Review (artifactReviewPolicy): Controls whether the agent stops for your review when it asks for feedback on an artifact, such as an implementation plan, before it continues. It doesn’t affect file edits, which Agent Mode controls:
asks-for-review (default; asks for review in /config): The agent always waits for your review.
agent-decides (agent decides): Currently works the same as asks-for-review.
always-proceed (always proceeds): The agent continues without waiting for your review.
Sandbox Mode (enableTerminalSandbox): When enabled (on), restricts all agent-initiated terminal commands to a secure OS container. When agentMode is set to auto, the terminal sandbox is enabled automatically and only commands that need to run outside the sandbox are evaluated for automatic approval.
Non-Workspace Access (allowNonWorkspaceAccess): When enabled (on), lets the agent read and edit files outside your workspace folders, subject to your Tool Permission, Agent Mode, and permission rules. Set to off by default for safety.

Note

auto mode is available in v1.3.5+ on macOS and Linux and v1.4.4+ on Windows, except for business and enterprise accounts. If agentMode is set to auto where auto isn’t available, the CLI starts in default mode. Starting in v1.4.4, if the sandbox isn’t available on your machine (for example, on Windows 10, earlier Windows 11 builds, or Linux hosts and some containers that block unprivileged user namespaces), Sandbox Mode has no effect, /config hides it along with proceed-in-sandbox and auto, and a saved proceed-in-sandbox behaves like request-review.

Display and rendering
Section titled “Display and rendering”

Customize the visual experience of the TUI:

Rendering Mode (altScreenMode): Controls how the TUI uses your terminal:
default (native terminal (inline)): Renders the conversation inline in your terminal’s scrollback and opens full-screen views, such as the diff viewer, in the alternate screen.
always (no flickering (altscreen)): Runs the whole TUI in the alternate screen, with its own scrollback, mouse-wheel scrolling, and scrollbar.
never (settings.json only): Never uses the alternate screen, even for full-screen views.
Color Scheme (colorScheme): Selects the visual theme: terminal (default; uses your terminal’s colors), light, solarized light, colorblind-friendly light, dark, solarized dark, colorblind-friendly dark, or tokyo night.
Animation Speed (runningLightSpeed): Adjusts the speed of the progress indicator animation (fast, medium (default), slow, or off).
Verbosity (verbosity): Controls how much of the agent’s work the conversation shows:
high: Shows every tool call, command, and thought in full.
medium (default): Groups related tool calls and thoughts into short summaries while keeping commands and responses visible.
low: Shows only the agent’s responses and collapses tool activity into a token usage summary.
Show Active Tasks (hideActiveItems): Shows active subagents and background tasks below the prompt box. On by default; turning it off saves "hideActiveItems": true.
Copy on Select (copyOnSelect): In alt-screen mode, copies text to the clipboard when you release a mouse selection. On by default. When it’s off, the artifact viewer uses your terminal’s own text selection.
Editor and notifications
Section titled “Editor and notifications”

Configure integrations with your host environment:

Editor (editor): The external editor the CLI opens for artifacts and files, and for composing prompts (CTRL + G). Defaults to auto, which uses $EDITOR and, if it isn’t set, falls back to vim on macOS and Linux or to edit and then notepad on Windows. You can also choose vim or emacs, or enter another command with other….
Editor Mode (editorMode): The editing model used inside the CLI prompt itself. Defaults to default (flat text editing); set it to vim for modal editing. Refer to Vim editor mode. This is independent of the editor setting above, which only selects an external program.
Editor Mode › Insert First (vimInsertFirst): Appears when Editor Mode is vim. When enabled, the prompt starts in Insert mode and a bare ENTER submits. Off by default.
Notifications (notifications): When enabled (on), rings the terminal bell and shows a desktop notification when the agent needs your approval or an answer, or finishes its turn. Off by default.
Conversations
Section titled “Conversations”

Control how follow-up messages are sent and how past conversations are listed:

Queued Messages (queuedMessages): Controls what happens to a message you send while the agent is working. queue (default, Queue) holds it until the current turn ends, and send-immediately (Send Immediately) interrupts the agent and sends it right away. Press ALT + M to send one message the other way.
Conversation Picker Grouping (pickerGrouping): Controls how the /resume picker lists conversations. none (default) shows one list, most recent first, and grouped groups conversations by workspace. Press CTRL + F in the picker to switch views for that session only.
AI credits and feedback
Section titled “AI credits and feedback”

Manage usage, tips, and telemetry:

Use AI Credits (useG1Credits): When enabled (on), allows the CLI to use your AI credits for model requests after your plan’s quota runs out. Off by default. This option isn’t shown for business accounts.
Enable Telemetry: When enabled (on), the CLI collects usage data to help Google improve Antigravity. This choice is saved with your account instead of in settings.json, and it’s always off for business accounts.
Show Tips (showTips): Toggles the display of helpful usage tips while the agent is generating responses. On by default.
Show Feedback Survey (showFeedbackSurvey): Enables periodic brief surveys after task completions to help improve the experience. On by default.
Settings available only in settings.json
Section titled “Settings available only in settings.json”

The following keys don’t have a /config option. Add them to settings.json to change them:

clearScrollbackOnResize (boolean, default true): In inline rendering, clears your terminal’s scrollback when the CLI redraws the conversation, such as after you resize the window. Set to false to keep earlier terminal output.
disableSlashCommands (boolean, default false): In headless mode (-p), sends prompts that start with / to the model as typed instead of running them as slash commands or skills. Same as the --disable-slash-commands flag.
historySize (integer, default 2000): Number of prompt history entries kept on disk. The CLI trims the history when it exits: -1 keeps every entry, and 0 clears the history.
model (string, default ""): The model you chose with /model, saved by its label. If that model is no longer available, the CLI uses the default model and shows a warning.
modelProvider (string, default ""): Set to "gemini" to send model requests directly to the Gemini API with the key in GEMINI_API_KEY. Refer to Using a Gemini API key.
trustedWorkspaces (string[], default []): Folders you chose to trust when the CLI asked. The CLI adds entries for you.
useTerminalCursor (boolean, default false): Uses your terminal’s own cursor shape instead of a block cursor.

For the keys that take an object, such as permissions, refer to Object settings.

Object settings
Section titled “Object settings”

These keys take a JSON object as their value.

permissions
Section titled “permissions”

Allow, ask, and deny rules for the agent’s tools. Each rule is an action(target) string, such as command(git status) or read_url(github.com), with no space before the opening parenthesis. A deny rule takes precedence over an ask rule, and an ask rule takes precedence over an allow rule. The CLI ignores rules it can’t parse. For the supported actions and how targets match, refer to Agent permissions.

{
  "permissions": {
    "allow": ["command(git status)", "read_url(github.com)"],
    "ask": ["command(git push)"],
    "deny": ["write_file(.env)"]
  }
}

These are the rules in the Global scope of /permissions. The CLI combines them with the rules in the Project and Shared scopes.

statusLine and title
Section titled “statusLine and title”

Run your own script to draw the status line below the prompt box, or to set the terminal window title. Both keys take an object with these properties:

command (string): Shell command to run, through sh -c (cmd /c on Windows). It receives the session state as JSON on stdin. A leading ~ expands to your home directory.
type (string, default "command"): Optional. "command" is the only supported type.
enabled (boolean, default true): false stops running command but keeps it in settings.json. For statusLine, the built-in status line shows instead.
padding (integer, default 0): statusLine only. Blank lines above the status line.
stack_with_default (boolean, default false): statusLine only. When true, shows your status line below the built-in one instead of replacing it.

Don’t set these keys to true or false. The CLI reads a boolean as {"enabled": true} or {"enabled": false} without a command, so no script runs. To turn a script off and keep it, set "enabled": false inside the object. For script examples and the JSON that scripts receive, refer to Status line customization and Terminal title customization.

sandboxProxy
Section titled “sandboxProxy”

Sends network traffic from sandboxed terminal commands through your own HTTP proxy instead of the CLI’s built-in proxy. It applies only while the terminal sandbox is on, and your proxy then has to enforce any read_url rules.

{
  "sandboxProxy": {
    "http": {
      "address": "proxy.example.com:3128",
      "certFile": "/etc/ssl/certs/proxy-ca.pem"
    }
  }
}

Set address (the proxy’s host:port) together with certFile (the proxy’s CA certificate), and username together with password if your proxy needs them. If either pair is incomplete, the CLI ignores sandboxProxy.

customModelsConfig and gcp
Section titled “customModelsConfig and gcp”
customModelsConfig: Adds models to /model when you use a Gemini API key. The CLI reads it only when modelProvider is "gemini" and GEMINI_API_KEY is set, and ignores it when you sign in with a Google Account. Each entry under customModels needs a modelName in the form gemini-api://<base_url>/models/<model>, and can set a label for /model.
gcp: Saved by the Use a Google Cloud project sign-in option: project is the project ID, and location is global, us, or eu. The CLI uses them to fill in the next sign-in, so you don’t need to edit them.
Custom status lines and terminal titles
Section titled “Custom status lines and terminal titles”

For advanced TUI environment integrations, you can toggle active metrics or deploy custom scripts to generate dynamic status bars and modify your terminal window titles:

Status line customization: Learn how to manage the status indicator panel and construct custom formatted status line shell scripts.
Terminal title customization: Learn how to toggle window title outputs and pipe live agent states into your window headers.
Keybindings configuration
Section titled “Keybindings configuration”

You can customize almost all keyboard shortcuts in the TUI by mapping keys to specific workspace commands.

Keybindings file location
Section titled “Keybindings file location”

Custom maps are stored alongside your primary settings profile:

~/.gemini/antigravity-cli/keybindings.json
Format and customization
Section titled “Format and customization”

The JSON structure maps a single TUI command action to an array of hotkey sequences:

{
  "cli.clear_screen": ["ctrl+l"],
  "prompt.insert_newline": ["shift+enter", "ctrl+j"],
  "edit.open_editor": ["ctrl+g"]
}

To completely disable a default hotkey, map its action to an empty array []. If your JSON schema is malformed or invalid, the CLI falls back to system defaults for those specific actions and loads the remaining valid mappings.

Note

Protected keys: Crucial navigation shortcuts such as cli.exit (CTRL + D / CTRL + C) and cli.enter (ENTER) are protected by the system and cannot be disabled.

Restoring defaults
Section titled “Restoring defaults”

To revert all keys back to system defaults, delete the keybindings profile:

rm ~/.gemini/antigravity-cli/keybindings.json
Next steps
Section titled “Next steps”

Now that you configured your environment, review security controls and extensibility options:

Permissions and sandbox: Manage secure execution containment boundaries.
Plugins and skills: Create your own custom skills and import legacy plugins.
CLI reference: Access quick reference sheets listing all configuration options, commands, and default key maps.
Previous
Review changes in the editor
Next
Agent settings
About Google
Google Products
Privacy
Terms