# Sandboxing
Source URL: https://antigravity.google/docs/sandbox-mode

Agent
>
Sandboxing
Sandboxing Terminal Commands

Sandboxing provides kernel-level isolation for terminal commands executed by the Agent. When enabled, commands run in a restricted environment with limited file system and network access, protecting your system from unintended modifications.

Sandboxing is currently disabled by default, but this may change in future releases. It is only available on macOS, where it leverages Seatbelt (sandbox-exec), Apple's kernel-level sandboxing mechanism. Linux support is coming soon.

Enabling Sandboxing

You can enable or disable sandboxing in Antigravity User Settings. Toggle "Enable Terminal Sandboxing" to turn sandboxing on or off. When enabled, you can also control network access separately using the "Sandbox Allow Network" toggle.

Restrictions

When sandboxing is enabled, the Agent's terminal commands are subject to the following restrictions:

File System: Commands can only write to your designated workspace directory and essential system locations. This prevents the Agent from accidentally deleting or modifying files outside your project.
Network Access: Network connectivity can be independently controlled. Use the "Sandbox Network Access" toggle in Antigravity User Settings to allow or deny network access while maintaining file system restrictions.

Here's an example of a command being blocked due to network restrictions:

Handling Sandbox Violations

If a command fails due to sandbox restrictions, you'll see a message indicating the failure may be sandbox-related. To resolve this, you can:

Disable Sandbox Permanently: Turn off sandboxing entirely in Antigravity User Settings.
Bypass for a Single Command: When using "Request Review" mode, you can choose to run an individual command with or without sandbox restrictions.

In "Request Review" mode, you'll see a "Bypass Sandbox" option when prompted to run a command:

Interaction with Strict Mode

When strict mode is enabled, sandboxing is automatically activated with network access denied. This ensures maximum protection when operating in a strict environment.

Strict Mode
MCP