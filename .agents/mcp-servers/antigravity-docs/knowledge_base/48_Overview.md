# Overview
Source URL: https://antigravity.google/docs/settings

Features
Learn
Settings
Overview
Markdown
AVAILABLE ON:
Antigravity 2.0
Antigravity CLI
Antigravity IDE
Settings
Section titled “Settings”

Configure preferences, execution boundaries, command permissions, and tool telemetry across Antigravity surfaces.

Antigravity 2.0
Antigravity CLI
Antigravity IDE
Antigravity 2.0
Settings architecture
Section titled “Settings architecture”

Antigravity features a hierarchical settings architecture designed to give you granular control over your development environment. Settings are split between global application preferences and isolated project-level boundaries to ensure robust security and flexible workspace configurations.

Accessing settings
Section titled “Accessing settings”

You can open the Settings panel using any of the following methods:

Keyboard shortcut: Press CMD + , on any active surface inside the application.
Sidebar navigation: Click Settings at the bottom of the left sidebar.
Project settings: Click the gear icon located next to a specific project.

Note

By default, if you have an active project open, clicking Settings automatically opens configurations for that specific project. Otherwise, it opens the global settings.

The four settings categories
Section titled “The four settings categories”

Settings are organized into four distinct scopes to keep configurations clean and isolated:

Global settings
Section titled “Global settings”

Global settings apply across all workspaces:

Account settings: Manage authentication sessions and toggle telemetry (enable or disable sharing interaction logs to improve models).
Global permissions: Centralized default tool boundaries that apply to all conversations.
Appearance: Customize visual themes and panel layouts.
Browser integration: Configure how the agent interacts with web surfaces.
Model usage: Choose and configure default reasoning models.
Customizations: Manage Model Context Protocol (MCP) servers, custom skills, and plugins.
Project settings
Section titled “Project settings”

Project settings apply exclusively within the scope of a specific project:

Folders: Define the list of local folders associated with the project. Antigravity automatically detects Git configurations for these folders to handle conversation targets:
Local: Select this in the new conversation view to work directly in the existing folders.
Worktree: Select this to start a new worktree in the folders. If a folder does not have Git, the existing local folder is used instead.
Agent settings: Configure project-specific agent behaviors:
Permission settings (macOS and Linux): Choose the project’s permission preset—Inherit General, Default, Request Review, or Turbo—controlling how the agent runs shell commands, accesses files, and uses the terminal sandbox (refer to Agent permissions).
Terminal execution policy (Windows): Control how the agent runs shell commands.
Outside of folder file access policy (Windows): Define how the agent accesses files outside the project boundary (Always Allow, Always Ask, or Always Deny).
Sandbox mode (Windows): Toggle the terminal sandbox container on or off within the custom security preset (refer to Terminal sandbox).
Project-level permissions: Configure permissions at the project level. As you interact with an agent, you accumulate permission requests that can be automatically added to project permissions.
Customizations: Derived from both global and project-specific customizations. You can view all skills originating from each folder added to the project.
Standalone conversations
Section titled “Standalone conversations”

You can also start conversations outside of a project:

Behavior: Standalone conversations do not have a configurable folder and instead run in a local scratch directory.
Settings: Standalone conversations can have their own settings (such as terminal execution, file access policies, and permissions) similar to projects, but operate independently of any project structure.
Miscellaneous
Section titled “Miscellaneous”

Access shortcuts and feedback tools:

Shortcuts: View and customize keyboard shortcut configurations.
Feedback: Access the feedback form to send reports directly to the team.
Data collection settings
Section titled “Data collection settings”

The Enable Telemetry setting is located in the Settings panel under the Account section. When toggled on, Antigravity collects interactions for use in evaluating, developing, and improving Antigravity and models that support Antigravity.

Previous
Task groups
Next
Agent settings
About Google
Google Products
Privacy
Terms