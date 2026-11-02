# CLI commands
Source URL: https://antigravity.google/docs/cli/reference

CLI commands - Antigravity CLIcliAntigravity CLIGet StartedCLI commands - Antigravity CLI Antigravity CLI Get StartedAntigravity CLI
Get Started
CLI reference
CLI commands
Markdown
CLI commands
Section titled “CLI commands”

Review tables listing all TUI slash commands, default keyboard shortcuts, command-line flags, and JSON configuration parameters.

Core slash commands
Section titled “Core slash commands”

Type / inside the prompt box to open the typeahead command selection menu.

Command	Category	Alias	Execution Purpose
/add-dir <path>	Utilities	—	Add a directory path to the active workspace.
/agents	Tools & Tasks	—	Open the Agent Manager panel to switch custom agents and monitor background subagents.
/artifact	Tools & Tasks	—	Open the Artifact Review panel.
/boost <task>	Reasoning	—	Run on-demand multi-agent deep reasoning loops.
/browser <task>	Tools & Tasks	—	Delegate web browsing, UI verification, and in-browser debugging to the browser subagent.
/btw <query>	Utilities	—	Ask a side question in the background without interrupting the main conversation.
/changelog	Utilities	—	Open the interactive release notes viewer or print CLI changes in headless mode.
/clear	Utilities	/new	Clear the terminal and reset active conversation contexts.
/codesearch <query>	Utilities	/cs, /search	Open the interactive Code Search panel to search code across the workspace.
/config	Configurations	/settings	Open the interactive Settings Editor overlay.
/context	Utilities	—	Open the context usage visualization panel.
/copy [n|btw]	Utilities	—	Copy the last agent response, the n-th most recent response, or the latest /btw answer.
/credits	Account	—	View remaining G1 credits and purchase links.
/diff	Utilities	—	Open the interactive diff viewer to view changes, turns, and commits.
/effort [level]	Configurations	—	Set or inspect the active model’s reasoning effort level (low through max, depending on the model).
/exit	Core	/quit	Close the TUI session and restore your host shell.
/feedback	Utilities	—	Open the feedback submission panel.
/fork	Conversations	/branch	Clone the current conversation thread into a new parallel session.
/goal <objective>	Reasoning	—	Run autonomously until the goal is verified complete, without intermediate pauses.
/grill-me [task]	Planning	—	Have the agent interview you one question at a time, with a recommended answer for each, before it starts work.
/help	Utilities	—	Open the help panel showing commands and shortcuts.
/hooks	Tools & Tasks	—	Browse active pre-flight/post-format script hooks.
/keybindings	Configurations	—	Open the interactive Keyboard Shortcut Editor.
/learn [instruction]	Tools & Tasks	—	Capture session corrections as persistent rules or skills through a reviewable proposal.
/logout	Account	—	Disconnect your profile and purge authentication tokens from the secure keyring.
/mcp	Tools & Tasks	—	Open the Model Context Protocol (MCP) server manager.
/model	Configurations	—	Choose your preferred reasoning model (persists across sessions). To run a single prompt on another model without changing your default, use /model <model> <prompt>.
/open <path>	Utilities	—	Force the path to open inside your default system editor.
/permissions	Configurations	—	Open the interactive tool permissions manager panel.
/plan [task]	Planning	—	Explore the codebase, clarify requirements, and draft a reviewable Implementation Plan.
/plugin	Tools & Tasks	/plugins	Open the interactive Plugins Manager or run inline install, uninstall, enable, disable, and list commands.
/rename <name>	Conversations	—	Rename the current session thread.
/remote-control [on/off]	Utilities	—	Toggle Remote Control for the active terminal session.
/resume	Conversations	/switch, /conversation	Open the conversation picker overlay to select and load previous threads.
/rewind	Conversations	/undo	Roll back your conversation history to a previous message.
/schedule <when> <task>	Tools & Tasks	—	Set a one-shot timer or recurring cron schedule that wakes the agent with an instruction.
/skills	Tools & Tasks	—	Browse loaded local and global Agent Skills. Run /skills reload to reload skills from disk.
/statusline	Configurations	—	Open the Status Bar customization overlay.
/tasks	Tools & Tasks	—	Open the Task Manager panel to monitor background shell execution logs.
/teamwork <task>	Reasoning	—	Launch collaborative multi-agent teams for long-horizon projects (paid plans).
/title [on/off]	Configurations	—	Toggle or set terminal window title updates.
/usage	Utilities	/quota	Display model quota usage.
/voice	Utilities	/record	Dictate a prompt using your microphone.
Default keybindings
Section titled “Default keybindings”

The following tables list the keyboard shortcut commands mapping global, prompt, navigation, and approval operations.

Global controls
Section titled “Global controls”

These hotkeys are always active regardless of which panel, overlay, or prompt is currently focused.

Key	TUI Command	Action Behavior
Esc	cli.escape	Closes active panels, halts active streams, or clears empty prompts.
Ctrl+C	cli.exit	Terminates the CLI session (prompts for confirmation if agent is working).
Ctrl+D	cli.exit	Exits the CLI session (only when the prompt box is empty).
Ctrl+L	cli.clear_screen	Refreshes and clears the visual terminal buffer.
Prompt focus keys
Section titled “Prompt focus keys”

These keys are active when writing instructions inside the prompt box.

Key	TUI Command	Action Behavior
Enter	cli.enter	Submits your prompt or active menu selection to the agent.
Shift+Enter / Ctrl+J	prompt.insert_newline	Inserts a clean newline without submitting.
Shift+Tab	cli.cycle_mode	Cycles between execution modes (default > accept-edits > auto > plan; auto only where available).
Ctrl+V	edit.paste	Pastes graphic media files or clipboard blocks into the prompt.
Ctrl+O	view.toggle_trajectory	Expands or collapses detailed tool reasoning outputs.
Ctrl+R	view.review_artifact	Opens the Artifact Review panel.
Ctrl+G	edit.open_editor	Launches your default $EDITOR shell to compose your prompt.
Alt+J	subagent.jump_to_waiting	Instantly switches focus to the next subagent awaiting confirmation.
Ctrl+K	subagent.approve_fast	Instantly approves the pending subagent action listed in the status alert.
Ctrl+A	—	Moves the prompt insertion cursor to the beginning of the line.
Ctrl+E	—	Moves the prompt insertion cursor to the end of the line.
Ctrl+_ / Ctrl+Shift+-	edit.undo	Reverts the last edit.
Ctrl+Shift+Z	edit.redo	Redoes the last undone text operation.
Ctrl+D	—	Forward delete (only when the prompt box is non-empty).
F5	voice.start_dictation	Starts or stops voice dictation.
Navigation and scrolling
Section titled “Navigation and scrolling”

These keys are active inside select panels, menus, and scrollable text boxes.

Key	TUI Command	Action Behavior
↑ / ↓	navigation.up / navigation.down	Scrolls highlighted selections up or down by one item.
PgUp / Shift+↑	navigation.page_up / navigation.half_page_up	Scrolls the active text viewport up by one page block.
PgDn / Shift+↓	navigation.page_down / navigation.half_page_down	Scrolls the active text viewport down by one page block.
← / →	navigation.left / navigation.right	Swaps pages inside multipage structures (like the Session Picker).
Tab	navigation.tab	Confirms the highlighted slash-command autofill option.
Tool confirmations
Section titled “Tool confirmations”

These keys are active during confirmation prompts.

Key	TUI Command	Action Behavior
y	confirm.yes	Authorizes the proposed tool, command, or active artifact.
n	confirm.no	Rejects the proposed tool, command, or active artifact.
A	—	(Inside Review panel) Approves all generated artifacts in one action (built-in shortcut).
Command-line flags
Section titled “Command-line flags”

Pass startup flags when launching agy to configure the session or run non-interactively:

Flag	Default	Description
--mode	""	Set the agent execution mode for this session: accept-edits, auto (Preview; v1.3.5+ on macOS and Linux, v1.4.4+ on Windows; requires the terminal sandbox; not available for business or enterprise accounts), or plan.
--model	—	Select the model for the current CLI session (refer to agy models).
--effort	—	Set the reasoning effort for the current CLI session (low through max, depending on the model).
--agent	—	Select the agent for the current CLI session (refer to agy agents).
--add-dir	[]	Add a directory to the workspace (repeatable).
-c, --continue	false	Continue the most recent conversation.
--conversation	—	Resume a previous conversation by ID.
-i, --prompt-interactive	—	Run an initial prompt interactively and continue the session.
-p, --print, --prompt	—	Run a single prompt non-interactively in headless mode and print the response.
--output-format	text	Output format for print mode (text, json, stream-json).
--input-format	text	Input format for print mode (text, stream-json).
--json-schema	—	JSON schema string or path to a schema file to enforce structured output in print mode.
--print-timeout	0s	Optional time limit for print mode (0 waits until the turn completes).
--disable-slash-commands	false	Disable slash command and skill expansion in print mode.
--sandbox	false	Run in a terminal sandbox with OS containment restrictions enabled (in v1.4.4+, no effect if the sandbox isn’t available on your machine).
--dangerously-skip-permissions	false	Auto-approve all tool permission requests without prompting.
--remote-control	false	Create a Remote Control connection for the CLI session on startup.
--project	—	Project ID or project name for the current CLI session.
--new-project	false	Create a new project for this session.
--log-file	—	Override the CLI log file path.
Configuration keys (settings.json)
Section titled “Configuration keys (settings.json)”

This section lists every key you can set in ~/.gemini/antigravity-cli/settings.json, with its type and default. A key you leave out uses its default. For how the CLI reads and saves the file, and for the keys that take an object, refer to CLI settings.

Example settings.json
Section titled “Example settings.json”
{
    "agentMode": "auto",
    "colorScheme": "tokyo night",
    "altScreenMode": "always",
    "toolPermission": "proceed-in-sandbox",
    "notifications": true,
    "enableTerminalSandbox": true
}

To get autocomplete and validation in editors such as VS Code, add "$schema": "https://antigravity.google/schemas/v1/settings.json" at the top of the file. For details, refer to Editor autocomplete and validation.

agentMode
string
"" (default mode)
Default startup execution mode: "" (standard default mode), "accept-edits" (auto-approve workspace file edits), "auto" (Preview; v1.3.5+ on macOS and Linux, v1.4.4+ on Windows; requires the terminal sandbox; auto-approves edits, runs commands in the terminal sandbox by default, and automatically checks any command that needs to run outside the sandbox so safe, reversible commands run without prompting while irreversible actions still prompt; not available for business or enterprise accounts), or "plan" (research and outline steps before writing code). Can be overridden per session with --mode.
colorScheme
string
"terminal"
Color theme: "light", "solarized light", "colorblind-friendly light", "dark", "solarized dark", "colorblind-friendly dark", "tokyo night", or "terminal" (inherits native shell colors).
altScreenMode
string
"default"
Screen buffer usage: "default" (renders the conversation inline and opens full-screen views in the alternate screen), "always" (runs the whole TUI in the alternate screen), or "never" (never uses the alternate screen; available only in settings.json).
toolPermission
string
"request-review"
Global safety presets: "request-review" (prompts for write, bash, web, and MCP tools unless an allow rule covers them), "proceed-in-sandbox" (runs terminal commands without prompting when the sandbox is on and the command runs inside it; in v1.4.4+, behaves like "request-review" if the sandbox isn’t available), "always-proceed" (runs commands, web requests, and MCP tools without prompting unless an ask or deny rule matches), or "strict" (prompts before every tool action, including file reads, even if an allow rule matches). Deny rules apply in every mode.
artifactReviewPolicy
string
"asks-for-review"
Whether the agent waits for your review when it asks for feedback on an artifact, such as an implementation plan: "asks-for-review" (always waits), "agent-decides" (currently the same as "asks-for-review"), or "always-proceed" (never waits). Doesn’t affect file edits.
notifications
boolean
false
Rings the terminal bell and shows a desktop notification when the agent needs your approval or an answer, or finishes its turn.
showTips
boolean
true
Displays helpful usage tips while the agent is generating responses.
showFeedbackSurvey
boolean
true
Displays periodic quality feedback surveys upon active task completions.
editor
string
"auto"
External editor for opening artifacts and files and for composing prompts (Ctrl+G): "auto" (uses $EDITOR, then falls back to vim, or to edit and notepad on Windows), "vim", "emacs", or any other editor command.
editorMode
string
"default"
Prompt editing model: "default" (flat text editing) or "vim" (modal editing). Distinct from editor, which selects an external program. Refer to Vim editor mode.
vimInsertFirst
boolean
false
Starts Vim editing in Insert mode and makes a bare Enter submit. Requires editorMode set to "vim".
allowNonWorkspaceAccess
boolean
false
Lets the agent read and edit files outside your workspace folders, subject to toolPermission, agentMode, and your permission rules.
enableTerminalSandbox
boolean
false
Restricts all local execution commands launched by agents to OS containment rings (in v1.4.4+, no effect if the sandbox isn’t available on your machine).
useG1Credits
boolean
false
Uses your AI credits for model requests after your plan’s quota runs out. Not available for business accounts.
verbosity
string
"medium"
Visual verbosity level: "high" (renders every tool call, command, and thought in full), "medium" (groups related tool calls and thoughts into summaries while keeping commands and responses visible), or "low" (renders only responses and collapses tool activity into a token usage summary).
runningLightSpeed
string
"medium"
Visual running light progress animation speed: "fast", "medium", "slow", or "off".
copyOnSelect
boolean
true
In alt-screen mode, copies text to the clipboard when you release a mouse selection. When false, the artifact viewer uses your terminal’s own text selection.
hideActiveItems
boolean
false
Hides the list of active subagents and background tasks below the prompt box (Show Active Tasks in /config).
pickerGrouping
string
"none"
How the /resume picker lists conversations: "none" (one list, most recent first) or "grouped" (grouped by workspace).
queuedMessages
string
"queue"
What happens to a message you send while the agent is working: "queue" (held until the current turn ends) or "send-immediately" (interrupts the agent and sends it right away).
clearScrollbackOnResize
boolean
true
In inline rendering, clears your terminal’s scrollback when the CLI redraws the conversation, such as after you resize the window.
disableSlashCommands
boolean
false
In headless mode (-p), sends prompts that start with / as typed instead of running slash commands or skills. Same as --disable-slash-commands.
historySize
integer
2000
Prompt history entries kept on disk, trimmed when the CLI exits: -1 keeps every entry, and 0 clears the history.
model
string
""
The model you chose with /model, saved by its label.
modelProvider
string
""
"gemini" sends model requests directly to the Gemini API with the key in GEMINI_API_KEY (Using a Gemini API key).
trustedWorkspaces
string[]
[]
Folders you chose to trust when the CLI asked. The CLI adds entries for you.
useTerminalCursor
boolean
false
Uses your terminal’s own cursor shape instead of a block cursor.
permissions
object
—
Allow, ask, and deny rules for the agent’s tools. Refer to permissions.
statusLine
object
—
Custom status line script. Refer to statusLine and title.
title
object
—
Custom terminal title script. Refer to statusLine and title.
sandboxProxy
object
—
HTTP proxy for sandboxed terminal commands. Refer to sandboxProxy.
customModelsConfig
object
—
Extra models for the Gemini API key setup. Refer to customModelsConfig and gcp.
gcp
object
—
Saved by the Use a Google Cloud project sign-in. Refer to customModelsConfig and gcp.

Enable Telemetry in /config has no settings.json key: the CLI saves that choice with your account.

Next steps
Section titled “Next steps”

Learn how to safely deploy permission policies, sandboxes, and customize plugins:

CLI settings: Use the interactive /config panel, choose a rendering mode, and see how the CLI reads and saves settings.json.
Permissions and sandbox: Enforce command-line containment rules.
Plugins and skills: Create your own custom skills slash commands.
Installation and auth: Update your CLI installation.
Previous
Eclipse
Next
CLI features
About Google
Google Products
Privacy
Terms