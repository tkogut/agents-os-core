# Agent Settings
Source URL: https://antigravity.google/docs/agent-settings

Antigravity 2.0
>
Settings
>
Agent Settings
Agent Settingslink
Terminal Command Auto Executionlink

Controls how the agent executes generated shell commands:

Request Review: The agent will never auto-execute terminal commands (except those explicitly added to your configurable Allow list).
Always Proceed: The agent will execute commands automatically without prompting (except those explicitly added to your configurable Deny list).
Agent Non-Workspace File Accesslink

Allows the agent to view and edit files outside of the active project folders.

By default, the agent only has access to the folders inside your Project and the application’s local app data directory ~/.gemini/antigravity/ (which contains Artifacts, Knowledge Items, etc.).
Enforcing this boundary protects your local sensitive data. Enable non-workspace access with caution.
Overview
Artifact Review