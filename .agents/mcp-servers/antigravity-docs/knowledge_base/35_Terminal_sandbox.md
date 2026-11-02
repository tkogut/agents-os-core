# Terminal sandbox
Source URL: https://antigravity.google/docs/sandbox

Terminal sandbox2-0Antigravity AppFeaturesTerminal sandbox Antigravity App FeaturesAntigravity AppAntigravity CLI
Features
Learn
Terminal sandbox
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Terminal sandbox
Section titled “Terminal sandbox”

The terminal sandbox isolates agent shell commands inside OS-level container boundaries to protect your workstation and sensitive files.

Antigravity App
Antigravity CLI
Antigravity CLI
How it works
Section titled “How it works”

With the terminal sandbox enabled, Antigravity CLI executes commands inside an OS-level isolation boundary. Commands can write to your workspace, temporary directories, and common build caches, and read system directories (such as /usr and /etc on macOS and Linux) so your tools keep working. Sensitive files such as ~/.ssh and .env are blocked, and network access is limited to domains you’ve approved. On macOS and Linux, anything not explicitly mounted is invisible inside the sandbox. On Windows, folders outside your user profile are readable but not writable inside the sandbox, and other files in your user profile and other users’ profiles stay hidden.

The sandbox is built on native operating system primitives, so there are no virtual machines or Docker images to manage and no startup delay:

Operating System	Technology	Details
Linux	Namespaces	Kernel namespaces isolate the filesystem, hide host processes, and cut off networking.
macOS	sandbox-exec	Seatbelt profiles (SBPL) restrict filesystem access and socket connections.
Windows	Process security environments	Commands run in an AppContainer inside a process security environment, which restricts filesystem and network access. Requires Windows 11 24H2 or later with the August 2026 update or later.
CLI configuration
Section titled “CLI configuration”

Enable the sandbox in ~/.gemini/antigravity-cli/settings.json, or interactively using /config:

{
    "enableTerminalSandbox": true,
    "toolPermission": "proceed-in-sandbox"
}

The configuration supports the following settings:

enableTerminalSandbox (boolean, default: false): Runs agent commands inside the sandbox.
toolPermission (string, default: "request-review"): Setting this to "proceed-in-sandbox" lets sandboxed commands run automatically, while commands that need to run outside the sandbox still prompt for review. Refer to Settings for the other modes.
agentMode (string, default: "", which is default mode): Setting "agentMode": "auto" (Preview) enables the terminal sandbox automatically so commands run inside the sandbox by default, and automatically evaluates commands that need to run outside the sandbox so safe, reversible commands run without prompting while risky or irreversible commands pause for approval. Refer to Choose an execution mode.

Note

auto mode is available in v1.3.5+ on macOS and Linux and v1.4.4+ on Windows.

CLI flags
Section titled “CLI flags”

You can also control sandboxing when launching the CLI:

# Force the sandbox on for this session
agy --sandbox

# Launch in auto mode (enables the sandbox and automatically evaluates commands that need to run outside it)
agy --mode=auto

The CLI supports the following sandbox and execution flags:

--sandbox: Turns the sandbox on for the session, overriding settings.json.
--mode=auto: Runs commands inside the sandbox by default and automatically checks commands that need to run outside the sandbox so safe, reversible commands proceed without prompting.
If the sandbox isn’t available
Section titled “If the sandbox isn’t available”

Starting in v1.4.4, the following applies if the sandbox isn’t available on your machine (for example, on Windows 10, earlier Windows 11 builds, or Linux hosts and some containers that block unprivileged user namespaces):

enableTerminalSandbox and --sandbox have no effect.
proceed-in-sandbox behaves like request-review.
auto mode isn’t offered.
/config hides Sandbox Mode, proceed-in-sandbox, and auto.

Your saved settings aren’t changed, so they take effect once the sandbox is available.

CLI permissions integration
Section titled “CLI permissions integration”

The sandbox derives its access boundaries from your Permissions configuration:

Filesystem: Workspace folders and paths allowed under write_file are mounted read-write. Paths allowed under read_file are mounted read-only, on top of the default system mounts. Denied paths are blocked, and everything else is inaccessible, except that on Windows, folders outside your user profile stay readable.
Network: Sandboxed commands run without network access by default. Domains allowed under read_url are added to the sandbox’s outbound allowlist.
Commands outside the sandbox: A command allow rule lets a matching command run without prompting, inside or outside the sandbox. This is useful for tools that can’t work inside the isolation boundary, such as Docker or commands that talk to system services. Business and enterprise accounts use an unsandboxed allow rule for this instead.

The agent can also request to run a command outside the sandbox on its own—for example, to retry a command that failed due to sandbox restrictions. On Windows, this includes some package installs and commands that connect to servers running outside the sandbox. How Antigravity CLI handles these requests depends on your mode:

Modes other than auto: These requests always require your approval unless the command matches a command allow rule (an unsandboxed allow rule for business and enterprise accounts).
auto mode (v1.3.5+ on macOS and Linux, v1.4.4+ on Windows): Antigravity CLI automatically evaluates commands that need to run outside the sandbox so safe, reversible commands run without prompting while irreversible commands still prompt for confirmation.
Example
Section titled “Example”

The following example configures sandbox allow and deny rules in settings.json:

{
    "permissions": {
        "allow": [
            "command(npm test)",
            "command(git diff)",
            "command(git push)",
            "read_file(/var/log/app)",
            "write_file(src/)"
        ],
        "deny": [
            "command(rm -rf /)",
            "command(sudo *)",
            "write_file(/home/user/.ssh)"
        ]
    }
}

With this configuration:

npm test and git diff run inside the sandbox.
git push runs without prompting, even when it needs to run outside the sandbox, through command(git push).
rm -rf / and sudo are always blocked.
Interactive prompts
Section titled “Interactive prompts”

When a command needs review, you can approve it once or turn the approval into a standing rule:

Do you want to proceed?
1. Yes
2. Yes, and always allow in this conversation for commands that start with 'npm test'
3. Yes, and always allow for commands that start with 'npm test' (Persist to settings.json)
4. No

For business and enterprise accounts, when the agent asks to bypass the sandbox, the prompt calls it out explicitly so you can judge the risk:

🔓 Allow sandbox bypass for command execution?
⚠️ Confirm the command is safe to run outside of the sandbox with full network and disk access.

Approving “always allow” here records an unsandboxed(...) rule instead of a plain command(...) rule.

For other accounts, these requests use the standard command prompt, and “always allow” records a command(...) rule.

Related resources
Section titled “Related resources”

Explore related documentation and guides:

Agent permissions: Configure allow, deny, and ask rules.
Agent settings: Command execution policies and file access controls.
Settings: Global application and CLI preferences.
Projects: Multi-folder configuration and per-project settings.
Previous
Marketplace
Next
Review changes
About Google
Google Products
Privacy
Terms