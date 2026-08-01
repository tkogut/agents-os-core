# Permissions
Source URL: https://antigravity.google/docs/cli/permissions

Antigravity CLI
>
Agent Capabilities
>
Permissions
Permissionslink

Secure your local workstation, restrict absolute file paths, configure custom allow/deny/ask policies, and manage interactive approvals. You can also manage these rules interactively using the Permissions Command.

Fine-grained permissionslink

To secure your workstation while enabling autonomous workflows, Antigravity CLI integrates a robust Fine-Grained Permissions Engine. Every sensitive operation the agent performs is represented as a permission resource formatted as action(target).

Permissions are evaluated across three distinct access lists configured inside your global settings:

text
content_copy
~/.gemini/antigravity-cli/settings.json
deny: The action is blocked immediately.
ask: The agent pauses and prompts for your explicit approval before proceeding.
allow: The action is auto-approved without prompting.
warning
Precedence Rule: Conflicting rules are strictly evaluated in priority order: Deny > Ask > Allow. For example, if you configure command(*) in your ask list and command(git) in your allow list, the ask rule takes precedence and prompts before every command.
Supported actions & matching ruleslink

Fine-grained permissions follow a standard schema pattern:

text
content_copy
action(target)

The supported actions, target format specifications, and matching algorithms are:

Action	Target Format	Matching Behavior	Default Fallback
read_file	read_file(/path), read_file(dir), or read_file(*)	Matches absolute paths or paths relative to workspace roots. Grants recursive read access to all contained files/folders. read_file(*) matches all files on the system.	Ask (Auto-allowed in workspace)
write_file	write_file(/path) or write_file(*)	Same as read_file. Implicitly grants read_file for the exact same target path.	Ask (Auto-allowed in workspace)
read_url	read_url(domain) or read_url(*)	Matches hostnames and subdomains (e.g., google.com covers mail.google.com). Ignores URL path segments. read_url(*) matches any domain.	Ask
execute_url	execute_url(domain) or execute_url(*)	Actuating on web elements (clicking, typing) or driving interactive browser workflows on a domain.	Ask
command	command(prefix), command(regex), or command(*)	Matches commands by exact word/token prefix. Each whitespace-separated token is evaluated as an anchored regular expression (^(?:pattern)$).

For example, command(npm run (build|lint|test)) matches npm run build and npm run test.	Ask
unsandboxed	unsandboxed(prefix) or unsandboxed(*)	Matches commands by exact word/token prefix. Commands matching this grant will be executed outside of container isolation (only applicable when terminal sandboxing is enabled).	Ask
mcp	mcp(server/tool) or mcp(*)	Matches exact MCP tools or all tools on a specified server (applies to local mcp servers and remote connections). mcp(*) matches any tool.	Ask
Global wildcard syntaxlink

Across all supported action types, passing the global wildcard * (such as read_file(*), command(*), mcp(*)) matches all targets within that entire action namespace.

Implicit permission ruleslink
Write implies Read: Allowing write_file on a path automatically grants read_file on that path.
Deny Read implies Deny Write: Denying read_file on a path immediately blocks write_file on that path.
Cross-platform path normalizationlink

Antigravity ensures your permission rules work flawlessly whether you are developing on macOS, Linux, or Windows. On macOS and Linux, paths use standard forward slashes (/). On Windows, Antigravity automatically normalizes paths prior to rule evaluation by stripping drive letters (e.g., C:) and converting all backslashes (\) to forward slashes (/).

Default system behaviors & guardrailslink

When an action is not explicitly listed in your allow, deny, or ask lists, the system falls back to secure system defaults:

Workspaces are Auto-Allowed: In standard operation, reading and writing files inside your active project directory is automatically allowed.
Web Browsing Defaults to Ask: Actions for read_url and execute_url default to Ask. Before the agent navigates to or actuates on any web page, it will pause and prompt for your approval unless an allow rule is configured.
Unconfigured Actions Default to Ask: All other unconfigured actions (command, mcp, execute_url, non-workspace files) default to Ask.
Interactive permission promptslink

When the agent encounters an operation requiring approval (Ask mode), an interactive prompt card appears in your TUI.

Before confirming Allow for file, URL, or MCP permissions, you can directly edit the target string in the prompt card to expand the granted scope (e.g., broadening a single file request like /project/file.txt to the parent directory /project). The CLI validates that your edited target safely covers the operation and applies the expanded grant for the remainder of the turn, preventing repeated prompts for related operations. (Note: Scope editing is not supported for terminal commands).

Configuration exampleslink

Add these rules to your ~/.gemini/antigravity-cli/settings.json file:

json
content_copy
{
  "permissions": {
    "allow": [
      "command(git)",
      "command(npm run (build|lint|test))",
      "unsandboxed(git push)",
      "read_file(/var/log/app)",
      "write_file(src/)",
      "read_url(google.com)",
      "mcp(linter/*)"
    ],
    "deny": [
      "command(rm -rf)",
      "command(curl .*)",
      "command(sudo)",
      "write_file(.git/)",
      "write_file(/home/user/.ssh)"
    ],
    "ask": [
      "command(*)",
      "execute_url(aws.amazon.com)",
      "mcp(sql/execute_mutation)"
    ]
  }
}
See alsolink
Permissions Command: Manage rules interactively in the TUI.
Sandbox Customization: Enforce OS-level container isolation boundaries.
Plugins & Skills: Create your own custom skills slash commands.
Settings, Rendering & Keybindings: Customize keyboard hotkeys and buffers.
Plugins & Skills
Status Line Customization