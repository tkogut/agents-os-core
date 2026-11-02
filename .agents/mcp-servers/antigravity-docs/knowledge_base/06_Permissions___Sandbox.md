# Permissions & Sandbox
Source URL: https://antigravity.google/docs/permissions

Permissions2-0Antigravity AppFeaturesPermissions Antigravity App FeaturesAntigravity AppAntigravity CLI
Features
Learn
Permissions
Overview
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Agent permissions
Section titled “Agent permissions”

Antigravity uses a unified fine-grained permission engine to evaluate sensitive tool operations across Deny, Ask, and Allow access lists. If you are using Antigravity with Gemini Enterprise, see Antigravity in Gemini Enterprise.

Antigravity App
Antigravity CLI
Antigravity App
Updated permission settings
Section titled “Updated permission settings”

Antigravity uses a robust, unified permission engine to secure your environment while enabling autonomous workflows. Every sensitive operation the agent performs is represented as a permission resource formatted as action(target).

Permissions are evaluated across three distinct access lists:

Deny: The action is blocked immediately.
Ask: The agent pauses and prompts for your explicit approval before proceeding.
Allow: The action is allowed without prompting.

Note

Precedence rule: Conflicting rules are strictly evaluated in priority order: Deny > Ask > Allow. For example, if you configure command(*) in Ask and command(git) in Allow, the Ask rule takes precedence and prompts before every command.

Permission presets
Section titled “Permission presets”

The permission preset controls how agent actions are approved. Your configured allow, deny, and ask rules are layered on top of the preset and always take precedence:

Preset	Terminal sandbox	Terminal Commands	File Access	MCP & Web
Request Review	Disabled	Always ask	Workspace only	Ask
Default	Enabled	Allowed in sandbox; ask outside	Workspace + temp dirs	Ask
Auto (Preview)	Enabled	Allowed in sandbox; checked automatically outside	Workspace + temp dirs	Ask
Turbo	Disabled	Allowed (unrestricted)	Full filesystem	Allowed

The two presets that use the sandbox work as follows:

Default (“Ask before sensitive operations.”): Terminal commands run inside the isolated Terminal sandbox with access restricted to your workspace and temp directories and no network access. When a command needs network connectivity or host resources, the agent requests to run it outside the sandbox—prompting for your approval unless covered by a command(...) allow rule.
Auto (Preview) (“Automatically decide if commands run.”): Commands also run inside the terminal sandbox by default. When a command needs to run outside the sandbox, Antigravity automatically evaluates it so safe, reversible commands run without prompting, while risky or irreversible commands still ask for your approval.

Refer to Agent settings for more detail on each preset.

Note

Auto (Preview) is available in v2.23.0+. It isn’t currently available for business or enterprise accounts, including Antigravity in Gemini Enterprise.

Change your permission preset
Section titled “Change your permission preset”

You can set a preset for all projects, override it for a single project, or switch presets from the message box.

For all projects
Section titled “For all projects”

To change the preset for all projects, open Settings > General > Global Permissions > Permission Preset:

The checkmark marks your current global preset.

For a single project
Section titled “For a single project”

To override the global preset for a single project, change the project’s preset under Settings > Projects. New projects default to Inherit Global, which follows your global preset.

From the message box
Section titled “From the message box”

In v2.23.0+, you can also choose a preset from the permissions picker in the message box:

The picker changes your global preset, or the project’s preset if the project overrides it. To remove a project override, choose Use Global Settings.

Supported actions and matching rules
Section titled “Supported actions and matching rules”

The following table lists the supported permission actions, their target formats, and their default behavior:

Action	Target Format	Default Fallback
read_file	read_file(/path), read_file(dir), or read_file(*)	Ask (Allowed in workspace)
write_file	write_file(/path) or write_file(*)	Ask (Allowed in workspace)
read_url	read_url(domain) or read_url(*)	Ask
execute_url	execute_url(domain) or execute_url(*)	Ask
command	command(prefix), command(regex:pattern), or command(*)	Ask (Allowed in sandbox under the Default and Auto presets)
mcp	mcp(server/tool), mcp(server/*), or mcp(*)	Ask

Each action matches its target as follows:

read_file: Matches absolute paths or paths relative to project workspace roots. Grants recursive read access to all contained files and folders. Using read_file(*) matches all files on the system.
write_file: Same as read_file. Implicitly grants read_file for the exact same target path.
read_url: Matches hostnames and subdomains (for example, google.com covers mail.google.com). Ignores URL path segments. Using read_url(*) matches any domain.
execute_url: Covers actuating on web elements (clicking, typing) or driving interactive browser workflows on a domain.
command: Matches by exact word or token prefix literally by default. To match by regular expression, start the target with the regex: prefix (each whitespace-separated token is evaluated as an anchored regular expression ^(?:pattern)$, for example, command(regex:npm run (build.*))). Covers execution both inside and outside the sandbox.
mcp: Matches exact MCP tools or all tools on a specified server (applies equally to local and remote MCP servers). Using mcp(*) matches any tool.

Note

Global wildcard syntax (*): Across all supported action types (such as read_file(*), command(*), and mcp(*)), passing the global wildcard * matches all targets within that entire action namespace.

When commands require an exact match
Section titled “When commands require an exact match”

Certain shell constructs can hide arbitrary command execution behind an otherwise benign prefix—for example, command or process substitution ($(...), backticks, <(...)), arithmetic contexts ($((...))), brace expansion ({a,b}), non-literal command names, network or file descriptor redirections, and developer-tool flags that execute subcommands (such as git -c core.pager=<cmd> or tar --to-command). When Antigravity detects any of these (or cannot cleanly parse the command), it disables prefix matching for the entire command line: the command runs without prompting only if a rule matches the full line character-for-character (or across the full raw line for regex: rules), and otherwise falls back to Ask.

Standard shell composition still prefix-matches normally: pipelines, &&/||/; chains, quoted literals, plain $VAR arguments, simple file redirects, and transparent wrappers (timeout, nohup, nice, env, whose inner command is evaluated on its own). For example, with command(git) in your Allow list, git status && git log runs without prompting, while git log $(whoami) prompts for approval.

Understanding read_url and execute_url across the platform
Section titled “Understanding read_url and execute_url across the platform”

The read_url permission governs outbound web connectivity across three distinct areas of Antigravity:

Web page reading: When the agent fetches web page Markdown for research, it checks your read_url grants.
Browser subagent and tool: When driving Chrome sessions, read_url authorizes loading and viewing the target domain. However, interactive UI actuation (clicking buttons, typing text) is governed independently by execute_url.
Terminal sandboxing: Any domain granted under read_url is compiled directly into the sandbox’s outbound network allowlist, permitting commands like curl or npm to connect to authorized hosts.
Cross-platform command and path matching
Section titled “Cross-platform command and path matching”

Antigravity ensures your permission rules work consistently whether you’re developing on macOS, Linux, or Windows. On macOS and Linux, paths use standard forward slashes (/). On Windows, Antigravity automatically normalizes paths prior to rule evaluation by stripping drive letters (for example, C:) and converting all backslashes (\) to forward slashes (/).

Implicit permission rules
Section titled “Implicit permission rules”

Antigravity applies the following implicit permission rules:

Write implies read: Allowing write_file on a path automatically grants read_file on that path.
Deny read implies deny write: Denying read_file on a path immediately blocks write_file on that path.
Interactive permission prompts
Section titled “Interactive permission prompts”

When the agent encounters an operation requiring approval (Ask mode), an interactive card appears in your editor. Before clicking Allow for file, URL, or MCP permissions, you can directly edit the target string in the prompt card to expand the granted scope (for example, broadening a single file request like /project/file.txt to the parent directory /project). Antigravity validates that your edited target safely covers the operation and applies the expanded grant for the remainder of the turn, preventing repeated prompts for related operations. (Note: Scope editing isn’t supported for terminal commands).

Terminal commands and the sandbox
Section titled “Terminal commands and the sandbox”

Under the Default and Auto (Preview) presets, the agent runs terminal commands inside an isolated Terminal sandbox, which by default has access only to your workspace and system temp directories, and no network access. Commands can run without manual approval in the sandbox, and your permission grants can further shape what the sandbox can reach:

Paths granted under read_file dynamically populate the sandbox’s read-only filesystem allowlist.
Paths granted under write_file dynamically populate the sandbox’s read-write filesystem allowlist.
Domains granted under read_url define outbound network access policies.

Because some commands cannot run in the sandbox—for example, those requiring network access—the agent can still choose to run commands outside the sandbox:

Default: Such commands prompt for your approval unless already allowed or denied by a command rule.
Auto (Preview) (v2.23.0+): Antigravity automatically evaluates commands that need to run outside the sandbox so safe, reversible commands proceed without prompting, while risky or irreversible commands still require approval.
Default system behaviors and guardrails
Section titled “Default system behaviors and guardrails”

When an action isn’t explicitly listed in your Allow, Deny, or Ask lists, Antigravity falls back to secure system defaults:

Commands: Under the Default preset, commands run without prompting inside the sandbox and require approval to run outside it. Under Auto (Preview), safe commands outside the sandbox run without prompting, while sensitive or irreversible commands pause for approval.
Workspace files: Reading and writing files inside your active project directory is allowed without prompting, while non-workspace files require approval.
Web browsing defaults to Ask: Actions for read_url and execute_url default to Ask. Before the agent navigates to or actuates on any web page, it pauses and prompts for your explicit approval unless an allow rule is configured.
MCP tools default to Ask: Unconfigured MCP tool calls prompt for approval.

Note

Explicit rules always take precedence over defaults. An Ask rule such as command(rm) prompts for approval even when the command would otherwise run without prompting in the sandbox.

Configuration examples
Section titled “Configuration examples”

The following examples show rules for the Allow list, which defines actions that run without prompting:

command(git)                             # Standard git commands
command(regex:npm run (build|lint|test)) # Allow safe npm scripts using regex
command(git push)                        # Allow git push, inside or outside the sandbox
read_file(/var/log/app)                  # Read external log paths
write_file(src/)                         # Edit relative src/ folder
read_url(google.com)                     # Fetch Google subdomains
mcp(linter/*)                            # Run linter MCP tools

The following examples show rules for the Deny list, which defines actions that are permanently blocked:

command(rm -rf)                    # Block destructive deletions
command(regex:curl .*)             # Block unvetted curl downloads
command(sudo)                      # Block sudo privileges
write_file(.git/)                  # Safeguard Git history
write_file(/home/user/.ssh)        # Safeguard SSH keys

The following examples show rules for the Ask list, which defines actions that pause for manual confirmation:

command(*)                         # Prompt all commands
execute_url(aws.amazon.com)        # Prompt AWS console actuation
mcp(sql/execute_mutation)          # Prompt modifying SQL queries
Previous permission settings
Section titled “Previous permission settings”

Note

Business and enterprise accounts use the permission system described in this section.

Antigravity uses a robust, unified permission engine to secure your environment while enabling autonomous workflows. Every sensitive operation the agent performs is represented as a permission resource formatted as action(target).

Permissions are evaluated across three distinct access lists:

Deny: The action is blocked immediately.
Ask: The agent pauses and prompts for your explicit approval before proceeding.
Allow: The action is allowed without prompting.

Note

Precedence rule: Conflicting rules are strictly evaluated in priority order: Deny > Ask > Allow. For example, if you configure command(*) in Ask and command(git) in Allow, the Ask rule takes precedence and prompts before every command.

Supported actions and matching rules
Section titled “Supported actions and matching rules”

The following table lists the supported permission actions in the previous permission settings, their target formats, and their default behavior:

Action	Target Format	Default Fallback
read_file	read_file(/path), read_file(dir), or read_file(*)	Ask (Allowed in workspace)
write_file	write_file(/path) or write_file(*)	Ask (Allowed in workspace)
read_url	read_url(domain) or read_url(*)	Ask
execute_url	execute_url(domain) or execute_url(*)	Ask
command	command(prefix), command(regex:pattern), or command(*)	Ask
unsandboxed	unsandboxed(prefix), unsandboxed(regex:pattern), or unsandboxed(*)	Ask
mcp	mcp(server/tool), mcp(server/*), or mcp(*)	Ask

Each action matches its target as follows:

read_file: Matches absolute paths or paths relative to project workspace roots. Grants recursive read access to all contained files and folders. Using read_file(*) matches all files on the system.
write_file: Same as read_file. Implicitly grants read_file for the exact same target path.
read_url: Matches hostnames and subdomains (for example, google.com covers mail.google.com). Ignores URL path segments. Using read_url(*) matches any domain.
execute_url: Covers actuating on web elements (clicking, typing) or driving interactive browser workflows on a domain.
command: Matches by exact word or token prefix literally by default. To match by regular expression, start the target with the regex: prefix (each whitespace-separated token is evaluated as an anchored regular expression ^(?:pattern)$, for example, command(regex:npm run (build.*))).
unsandboxed: Matches command prefixes word-by-word literally by default (or with regex:). Commands matching this grant execute outside container isolation when terminal sandboxing is enabled.
mcp: Matches exact MCP tools or all tools on a specified server (applies equally to local and remote MCP servers). Using mcp(*) matches any tool.

Note

Global wildcard syntax (*): Across all supported action types (such as read_file(*), command(*), and mcp(*)), passing the global wildcard * matches all targets within that entire action namespace.

When commands require an exact match
Section titled “When commands require an exact match”

Certain shell constructs can hide arbitrary command execution behind an otherwise benign prefix—for example, command or process substitution ($(...), backticks, <(...)), arithmetic contexts ($((...))), brace expansion ({a,b}), non-literal command names, network or file descriptor redirections, and developer-tool flags that execute subcommands (such as git -c core.pager=<cmd> or tar --to-command). On Windows shells like PowerShell or Command Prompt, commands whose syntax cannot be cleanly split into separate words also fall into this category. When Antigravity detects any of these, it disables prefix matching for the entire command line: the command runs without prompting only if a rule matches the full line character-for-character (or across the full raw line for regex: rules, such as command(regex:git .*)), and otherwise falls back to Ask.

Standard shell composition still prefix-matches normally: pipelines, &&/||/; chains, quoted literals, plain $VAR arguments, simple file redirects, and transparent wrappers (timeout, nohup, nice, env, whose inner command is evaluated on its own). For example, with command(git) in your Allow list, git status && git log runs without prompting, while git log $(whoami) prompts for approval.

Understanding read_url and execute_url across the platform
Section titled “Understanding read_url and execute_url across the platform”

The read_url permission governs outbound web connectivity across three distinct areas of Antigravity:

Web page reading: When the agent fetches web page Markdown for research, it checks your read_url grants.
Browser subagent and tool: When driving Chrome sessions, read_url authorizes loading and viewing the target domain. However, interactive UI actuation (clicking buttons, typing text) is governed independently by execute_url.
Terminal sandboxing: In sandbox mode, any domain granted under read_url is compiled directly into the container’s outbound network allowlist (AllowedDomains), permitting commands like curl or npm to connect to authorized hosts.
Cross-platform command and path matching
Section titled “Cross-platform command and path matching”

Antigravity ensures your permission rules work consistently whether you’re developing on macOS, Linux, or Windows. On macOS and Linux, paths use standard forward slashes (/). On Windows, Antigravity automatically normalizes paths prior to rule evaluation by stripping drive letters (for example, C:) and converting all backslashes (\) to forward slashes (/).

Implicit permission rules
Section titled “Implicit permission rules”

Antigravity applies the following implicit permission rules:

Write implies read: Allowing write_file on a path automatically grants read_file on that path.
Deny read implies deny write: Denying read_file on a path immediately blocks write_file on that path.
Interactive permission prompts
Section titled “Interactive permission prompts”

When the agent encounters an operation requiring approval (Ask mode), an interactive card appears in your editor. Before clicking Allow for file, URL, or MCP permissions, you can directly edit the target string in the prompt card to expand the granted scope (for example, broadening a single file request like /project/file.txt to the parent directory /project). Antigravity validates that your edited target safely covers the operation and applies the expanded grant for the remainder of the turn, preventing repeated prompts for related operations. (Note: Scope editing isn’t supported for terminal commands).

Terminal sandboxing (preview)
Section titled “Terminal sandboxing (preview)”

Permission grants also apply to commands when the sandbox is enabled:

Paths granted under read_file dynamically populate the sandbox’s read-only filesystem allowlist.
Paths granted under write_file dynamically populate the sandbox’s read-write filesystem allowlist.
Domains granted under read_url define outbound network access policies.

Note

Refer to Terminal sandbox for architecture, preset configurations, and security details.

Default system behaviors and guardrails
Section titled “Default system behaviors and guardrails”

When an action isn’t explicitly listed in your Allow, Deny, or Ask lists, Antigravity falls back to secure system defaults:

Commands default to Ask: Unconfigured terminal commands (command and unsandboxed) require manual approval unless configured to run without prompting in your settings.
Workspace files: Reading and writing files inside your active project directory is allowed without prompting, while non-workspace files require approval.
Web browsing defaults to Ask: Actions for read_url and execute_url default to Ask. Before the agent navigates to or actuates on any web page, it pauses and prompts for your explicit approval unless an allow rule is configured.
MCP tools default to Ask: Unconfigured MCP tool calls prompt for approval.

Note

Explicit rules always take precedence over defaults.

Configuration examples
Section titled “Configuration examples”

The following examples show rules for the Allow list, which defines actions that run without prompting:

command(git)                             # Standard git commands
command(regex:npm run (build|lint|test)) # Allow safe npm scripts using regex
unsandboxed(git push)                    # Allow git push outside sandbox
read_file(/var/log/app)                  # Read external log paths
write_file(src/)                         # Edit relative src/ folder
read_url(google.com)                     # Fetch Google subdomains
mcp(linter/*)                            # Run linter MCP tools

The following examples show rules for the Deny list, which defines actions that are permanently blocked:

command(rm -rf)                    # Block destructive deletions
command(regex:curl .*)             # Block unvetted curl downloads
command(sudo)                      # Block sudo privileges
write_file(.git/)                  # Safeguard Git history
write_file(/home/user/.ssh)        # Safeguard SSH keys

The following examples show rules for the Ask list, which defines actions that pause for manual confirmation:

command(*)                         # Prompt all commands
execute_url(aws.amazon.com)        # Prompt AWS console actuation
mcp(sql/execute_mutation)          # Prompt modifying SQL queries
Related resources
Section titled “Related resources”

Explore related documentation and guides:

Permissions command: Manage rules interactively in the TUI.
Sandbox customization: Enforce OS-level container isolation boundaries.
Plugins and skills: Create your own custom skills and slash commands.
Settings, rendering, and keybindings: Customize keyboard hotkeys and buffers.
Previous
Managing conversations
Next
Tab completion
About Google
Google Products
Privacy
Terms