# Projects
Source URL: https://antigravity.google/docs/projects

Antigravity 2.0
>
Projects
Projectslink

In Antigravity 2.0, we are transitioning from the legacy repository-centric workspace model to a more flexible and secure Project-centric model. This document outlines what Projects are, how they work, and how they differ from the original workspace structure.

What is a Project?link

A Project is a configuration of folders defining the environment and the scope of your agent. Instead of forcing an agent to operate within a single folder, a project can work with one folder or multiple folders (e.g., a frontend and a backend repo), providing your agents with all of the context required for your codebase. All projects have their own isolated agent settings, allowing you to customize different projects’ security settings independently.

Key Differences: Workspace vs. Projectslink
Feature	Original Model (Workspace)	New Model (Project)
Organization Scope	Tightly coupled to a single local repository.	Projects are a configuration of all of the context and folders that your agents should work with.
Directory Boundaries	Agent is strictly confined to one folder structure.	A single Project can span multiple folders at once.
Settings Isolation	Settings inherited globally from the machine.	Projects have their own settings. Agents in a project use the project’s settings.
Permissions	Broad, global permissions.	Global permissions are inherited. Projects can have their own permissions in addition to global permissions.
Customizations	Skills/MCPs managed globally or per-workspace.	Reusable skills, MCPs, and hooks are managed globally.
Core Project Conceptslink

1. Folders
A Project is composed of folders, which define the directories and repositories the agent is allowed to access:

Local Folders: A folder that doesn’t have git configured.
Local Git Checkout: A folder that is a Git repository checkout.

2. Worktree Selection (Local vs. New Worktree)
When starting a new conversation in a Project, you choose how the agent should interact with your folders via the worktree selector:

Local Mode: The agent works directly in your active local folders or Git checkouts. (Best for quick, interactive edits in your current working folder).
New Worktree Mode: Creates a new Git worktree for the conversation. (Best for complex tasks, keeping your active working folder untouched and preventing parallel subagents from conflicting).

3. Scoped Settings and Permissions
Settings and permissions are both scoped at the project level:

Settings: When a Project is created, it always starts with the default security preset where it has read and write access to all of your project’s folders and will ask for permission to run all terminal commands. These settings can be modified and apply to all agents within this project.
Permissions: Projects inherit global permissions but allow you to augment them at the Project level, ensuring agents only have the exact access required for that specific project’s tasks.
Workflows Using Projectslink
Working in a Single Folder: Create a project with a folder and then configure its settings.
Working in Multiple Folders: Add all related folders into a single Project so the agent has full context across your codebases.
Running Parallel Agents on the Same Folder: Choose Local Mode when starting an agent so that all of your agents work in the same active folders.
Isolating Concurrent Agents: Choose New Worktree Mode when starting an agent so that separate, isolated Git worktrees are provisioned for each agent session, avoiding conflicts between agents.
Mixed Checkouts & Local Folders: Working locally operates directly in the existing folders. Using “New Worktree Mode” will spawn a new Git worktree for all active Git checkouts, allowing the agent to operate inside the new worktrees and the existing non-git local folders simultaneously.
Models
Overview