# Overview
Source URL: https://antigravity.google/docs/settings

Antigravity 2.0
>
Settings
>
Overview
Settingslink
Antigravity 2.0 Settingslink

Antigravity 2.0 features a hierarchical settings architecture designed to give you granular control over your development environment. Settings are split between Global application preferences and isolated Project-level boundaries to ensure robust security and flexible workspace configurations.

Accessing Settingslink

You can open the Settings panel in Antigravity 2.0 using the following methods:

Keyboard Shortcut: Press Cmd + , on any active surface inside the application.
Sidebar Navigation: Click Settings at the bottom of the left sidebar.
Project Settings: Click the Gear Icon located next to a specific project.
info
Note: By default, if you have an active project open, clicking Settings will automatically open the configurations for that specific project. Otherwise, it will open the global settings.
The Four Settings Categorieslink

Settings are organized into four distinct scopes to keep configurations clean and isolated:

1. Global Settings

These are global settings that apply to everything:

Account Settings: Manage authentication sessions and toggle Telemetry (enable/disable sharing interaction logs to improve models).
Global Permissions: Centralized default tool boundaries that apply to all conversations.
Appearance: Customize visual themes and panel layouts.
Browser Integration: Configure how the agent interacts with web surfaces.
Model Usage: Choose and configure default reasoning models.
Customizations: Manage Model Context Protocol (MCP) servers, custom skills, and “Build with Google” plugins.

2. Project Settings

These settings apply exclusively within the scope of a specific Project:

Folders: Define the list of local folders associated with the project. Antigravity automatically detects Git configurations for these folders to handle conversation targets:
Local: Select this in the new conversation view to work directly in the existing folders.
Worktree: Select this to start a new worktree in the folders. (Note: If a folder does not have Git, the existing local folder is used instead).
Agent Settings: Configure project-specific agent behaviors:
Terminal Execution Policy: Control how the agent runs shell commands.
Outside of Folder File Access Policy: Define how the agent accesses files outside the project boundary (Always Allow, Always Ask, or Always Deny).
Sandbox Mode: Toggle the terminal sandbox container on or off within the custom security preset.
Project-level Permissions: Configure permissions at the project level. As you interact with an agent, you will accumulate permission requests that can be automatically added to the project permissions.
Customizations: Derived from both global customizations and project-specific ones. You can view all skills originating from each folder added to the project.

3. Conversations Outside of a Project

You can also start conversations outside of a project (standalone conversations):

Behavior: These conversations do not have a configurable folder and instead run in a local scratch directory.
Settings: They can have their own settings (such as terminal execution, file access policies, and permissions) similar to projects, but operate independently of any project structure.

4. Miscellaneous

Shortcuts: View and customize keyboard shortcut configurations.
Feedback: Access the feedback form to send reports directly to the team.
Data Collection Settingslink

The “Enable Telemetry” setting can be found in the Settings panel under the “Account” section. When toggled on, Antigravity collects interactions for use in evaluating, developing, and improving Antigravity and models that support Antigravity.

Projects
Agent Settings