# Permissions
Source URL: https://antigravity.google/docs/permissions

Antigravity 2.0
>
Agent Capabilities
>
Permissions
Agent Permissionslink

Antigravity uses a robust, unified permission engine to secure your environment while enabling autonomous workflows. Every sensitive operation the Agent performs is represented as a permission resource formatted as action(target).

Permissions are evaluated across three distinct access lists:

Deny: The action is blocked immediately.
Ask: The Agent pauses and prompts for your explicit approval before proceeding.
Allow: The action is auto-approved without prompting.
warning
Precedence Rule: Conflicting rules are strictly evaluated in priority order: Deny > Ask > Allow. For example, if you configure command(*) in Ask and command(git) in Allow, the Ask rule takes precedence and prompts before every command.
Supported Actions & Matching Ruleslink
Action	Target Format	Matching Behavior	Default Fallback
read_file	read_file(/path), read_file(dir), or read_file(*)	Matches absolute paths or paths relative to project workspace roots. Grants recursive read access to all contained files/folders. Using read_file(*) matches all files on the system.	Ask (Auto-allowed in workspace)
write_file	write_file(/path) or write_file(*)	Same as read_file. Implicitly grants read_file for the exact same target path.	Ask (Auto-allowed in workspace)
read_url	read_url(domain) or read_url(*)	Matches hostnames and subdomains (e.g., google.com covers mail.google.com). Ignores URL path segments. Using read_url(*) matches any domain.	Ask
execute_url	execute_url(domain) or execute_url(*)	Actuating on web elements (clicking, typing) or driving interactive browser workflows on a domain.	Ask
command	command(prefix), command(regex), or command(*)	Matches by exact word/token prefix. Each whitespace-separated token is evaluated as an anchored regular expression (^(?:pattern)$). E.g., command(npm run (build.*)) matches npm run build and npm run build-prod.	Ask
unsandboxed	unsandboxed(prefix), unsandboxed(regex), or unsandboxed(*)	Matches commands by exact word/token prefix. Commands matching this grant will be executed outside of container isolation (only applicable when terminal sandboxing is enabled).	Ask
mcp	mcp(server/tool), mcp(server/*), or mcp(*)	Matches exact MCP tools or all tools on a specified server (applies equally to local mcpl servers and remote connections). Using mcp(*) matches any tool.	Ask
info
Global Wildcard Syntax (): Across all supported action types (e.g., read_file(), command(), mcp()), passing the global wildcard * matches all targets within that entire action namespace.
Understanding read_url vs execute_url Across the Platformlink

The read_url permission governs outbound web connectivity across three distinct areas of Antigravity:

The read_url Tool: When the Agent uses the internal read_url_content tool to fetch web page markdown for research, it checks your read_url grants.
Browser Subagent & Tool: When driving Chrome sessions, read_url authorizes loading and viewing the target domain. However, interactive UI actuation (clicking buttons, typing text) is governed independently by execute_url.
Terminal Sandboxing: In sandbox mode, any domain granted under read_url is compiled directly into the container’s outbound network allowlist (AllowedDomains), permitting commands like curl or npm to connect to authorized hosts.
Cross-Platform Command & Path Matchinglink

Antigravity ensures your permission rules work flawlessly whether you are developing on macOS, Linux, or Windows. On macOS and Linux, paths use standard forward slashes (/). On Windows, Antigravity automatically normalizes paths prior to rule evaluation by stripping drive letters (e.g., C:) and converting all backslashes (\) to forward slashes (/).

Implicit Permission Ruleslink
Write implies Read: Allowing write_file on a path automatically grants read_file on that path.
Deny Read implies Deny Write: Denying read_file on a path immediately blocks write_file on that path.
Interactive Permission Promptslink

When the Agent encounters an operation requiring approval (Ask mode), an interactive card appears in your editor. Before clicking Allow for file, URL, or MCP permissions, you can directly edit the target string in the prompt card to expand the granted scope (e.g., broadening a single file request like /project/file.txt to the parent directory /project). Antigravity validates that your edited target safely covers the operation and applies the expanded grant for the remainder of the turn, preventing repeated prompts for related operations. (Note: Scope editing is not supported for terminal commands).

Terminal Sandboxing (Preview)link

Permission grants also apply to commands when sandbox is enabled:

Paths granted under read_file dynamically populate the sandbox’s read-only filesystem allowlist.
Paths granted under write_file dynamically populate the sandbox’s read-write filesystem allowlist.
Domains granted under read_url define outbound network access policies.
info
Sandbox Availability: Terminal sandboxing is currently in preview on macOS / Linux, and coming soon to Windows.
Default System Behaviors & Guardrailslink

When an action is not explicitly listed in your Allow, Deny, or Ask lists, Antigravity falls back to secure system defaults:

Web Browsing Defaults to Ask: Actions for read_url and execute_url default to Ask. Before the Agent navigates to or actuates on any web page, it will pause and prompt for your explicit approval unless an allow rule is configured.
Workspaces are Auto-Allowed: In standard operation, reading and writing files inside your active project directory is automatically allowed. All other unconfigured actions (command, mcp, execute_url, non-workspace files) default to Ask.
Configuration Exampleslink

Allow list — actions that run without prompting:

text
content_copy
command(git)                       # Standard git commands
command(npm run (build|lint|test)) # Allow safe npm scripts via regex
unsandboxed(git push)              # Allow git push outside sandbox
read_file(/var/log/app)            # Read external log paths
write_file(src/)                   # Edit relative src/ folder
read_url(google.com)               # Fetch Google subdomains
mcp(linter/*)                      # Run linter MCP tools

Deny list — actions that are permanently blocked:

text
content_copy
command(rm -rf)                    # Block destructive deletions
command(curl .*)                   # Block unvetted curl downloads
command(sudo)                      # Block sudo privileges
write_file(.git/)                  # Safeguard Git history
write_file(/home/user/.ssh)        # Safeguard SSH keys

Ask list — actions that pause for manual confirmation:

text
content_copy
command(*)                         # Prompt all commands
execute_url(aws.amazon.com)        # Prompt AWS console actuation
mcp(sql/execute_mutation)          # Prompt modifying SQL queries
Sidecars
Subagents