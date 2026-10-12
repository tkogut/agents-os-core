# Terminal sandbox
Source URL: https://antigravity.google/docs/sandbox

Features
Learn
Terminal sandbox
Markdown
AVAILABLE ON:
Antigravity 2.0
Antigravity CLI
Terminal sandbox
Section titled “Terminal sandbox”

The terminal sandbox isolates agent shell commands inside OS-level container boundaries to protect your workstation and sensitive files.

Antigravity 2.0
Antigravity CLI
Antigravity 2.0

Note

Antigravity’s updated permission system is currently available on macOS and Linux, where the sandbox is enabled by default. On Windows, Antigravity continues to use the previous behavior—refer to the Windows section below.

macOS and Linux
Section titled “macOS and Linux”
Overview
Section titled “Overview”

Antigravity includes a terminal sandbox that isolates shell commands executed by agents. Sandboxed commands can write to your project folders, temporary directories, and common build caches, and read system directories such as /usr and /etc so your tools keep working. Sensitive files such as ~/.ssh and .env are blocked, anything not explicitly mounted is invisible inside the sandbox, and network access is limited to domains you’ve approved.

The sandbox is built on native operating system primitives, so there are no virtual machines or Docker images to manage and no startup delay:

Operating System	Technology	Details
Linux	Namespaces	Kernel namespaces isolate the filesystem, hide host processes, and cut off networking.
macOS	sandbox-exec	Seatbelt profiles (SBPL) restrict filesystem access and socket connections.
Configuration
Section titled “Configuration”

Your permission preset controls whether the sandbox is used. Configure your preset under Settings > General > Permission Settings:

Preset	Sandbox	Commands
Default	On	Allowed in sandbox; ask outside
Request Review	Off	Always ask
Turbo	Off	Allowed without prompting, unrestricted

You can override the global preset in an individual project under Settings > Projects. Projects default to Inherit General upon creation, which follows your global preset.

Refer to Agent permissions for the full preset behavior, including file access, MCP tools, and web page reads.

Unsandboxed commands
Section titled “Unsandboxed commands”

Some commands cannot work inside the sandbox—for example, those needing network access or talking to system services. The agent can request to run such commands outside the sandbox, where they run on your host with full privileges. These requests always pause for your approval, unless the command is already covered by a command allow or deny rule.

To let a specific command run without prompting—inside or outside the sandbox—add a command allow rule:

command(git push)
command(regex:docker compose .*)
Permissions integration
Section titled “Permissions integration”

The sandbox derives its access boundaries from your Permissions configuration:

Filesystem: Your project folders are mounted read-write. Paths allowed under read_file are mounted read-only, and paths allowed under write_file are mounted read-write, on top of the default system mounts. Everything else is inaccessible.
Network: Sandboxed commands run without network access by default. Domains allowed under read_url are added to the sandbox’s outbound allowlist.
Windows
Section titled “Windows”

Note

Windows currently uses the behavior described in this section. A future release updates Windows to the unified permission system.

Overview
Section titled “Overview”

Antigravity includes a terminal sandbox that isolates shell commands executed by agents. Sandboxed commands can write to your project folders, temporary directories, and common build caches, and read system directories so your tools keep working. Sensitive files such as .env are blocked, anything not explicitly mounted is invisible inside the sandbox, and network access is limited to domains you’ve approved.

Configuration
Section titled “Configuration”

You can configure the sandbox globally or per project.

Global settings
Section titled “Global settings”

In Settings > General, under Agent Settings, configure the following options:

Enable Sandbox Mode (Preview): Runs agent terminal commands inside the sandbox.
Terminal Command Auto Execution: Set to Proceed in Sandbox to let sandboxed commands run without approval; commands that need to run outside the sandbox still ask first. The other options are Require Review and Always Proceed.
Project settings
Section titled “Project settings”

Select a project under Settings > Projects to override these settings for that project. Each setting gains an Inherit General option, and Enable Sandbox Mode becomes a dropdown: Inherit General, Enabled, or Disabled.

Security presets
Section titled “Security presets”

The Security Preset dropdown in the same settings section bundles the terminal and file access policies:

Preset	Terminal Command Auto Execution	Outside-of-folders file access
Default	Require Review	Always Ask
Full machine	Require Review	Allow
Turbo mode	Always Proceed	Allow

None of the presets turn the sandbox on. Enabling Enable Sandbox Mode switches the preset to Custom, where you set each option yourself—a common combination is the sandbox with Proceed in Sandbox.

Unsandboxed commands
Section titled “Unsandboxed commands”

When a command needs to run outside the sandbox—because it matches an unsandboxed(...) rule, the agent requested it, or the sandbox is disabled—the command runs on your host with full privileges. Depending on your execution policy, the agent pauses for your approval first.

Permissions integration
Section titled “Permissions integration”

The sandbox derives its access boundaries from your Permissions configuration:

Filesystem: Your project folders are mounted read-write. Paths allowed under read_file are mounted read-only, and paths allowed under write_file are mounted read-write, on top of the default system mounts. Everything else is inaccessible.
Network: When network access is enabled, domains allowed under read_url are added to the sandbox’s outbound allowlist.
Escape hatches (unsandboxed): To let specific commands run outside the sandbox without disabling it entirely, add an unsandboxed allow rule:
unsandboxed(git push)
unsandboxed(docker compose .*)
Related resources
Section titled “Related resources”

Explore related documentation and guides:

Agent permissions: Configure allow, deny, and ask rules.
Agent settings: Command execution policies and file access controls.
Settings: Global application and CLI preferences.
Projects: Multi-folder configuration and per-project settings.
Previous
Plugins
Next
Review changes
About Google
Google Products
Privacy
Terms