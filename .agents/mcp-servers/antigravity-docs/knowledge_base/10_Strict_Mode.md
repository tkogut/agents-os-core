# Strict Mode
Source URL: https://antigravity.google/docs/strict-mode

Agent
>
Strict Mode
Strict Mode

Strict mode provides enhanced security controls for the Agent, allowing you to restrict its access to external resources and sensitive operations. When strict mode is enabled, several security measures are enforced to protect your environment.

Features
Browser URL Allowlist/Denylist

In strict mode, the Agent's ability to interact with external websites is governed by the browser's Allowlist and Denylist. This applies to:

External Markdown Images: The Agent will only render images from URLs that are allowed.
Read URL Tool: The Read URL tool will only auto-execute for allowed URLs.
Terminal, Browser, and Artifact Review Policies

Strict mode enforces the following behavior for terminal, browser, and artifact interactions:

Terminal Auto Execution: Set to "Request Review". The Agent will always prompt for permission before executing any terminal command. The terminal allowlist is ignored when strict mode is enabled.
Browser Javascript Execution: Set to "Request Review". The Agent will always prompt for permission before executing Javascript in the browser.
Artifact Review: Set to "Request Review". The Agent will always prompt for confirmation before acting on plans laid out in artifacts.
File System Access

Strict mode restricts the Agent's access to the file system to ensure it only interacts with authorized files:

Respect .gitignore: The Agent will respect .gitignore rules, preventing it from accessing ignored files.
Workspace Isolation: Access to files outside the workspace is disabled. The Agent can only view and edit files within the designated workspace.
Browser Subagent
Sandboxing Terminal Commands