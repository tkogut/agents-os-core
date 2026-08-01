# Subagents
Source URL: https://antigravity.google/docs/cli/subagents

Antigravity CLI
>
Agent Capabilities
>
Subagents
Background tasks & subagentslink

Delegate slow builds, multi-file code generation, and research sweeps to parallel background agents while maintaining your active programming flow.

Antigravity 2.0 & Hub Docs: For core platform capabilities, subagent lifecycle state diagrams, inter-agent messaging, and nesting depth limits, see the Antigravity 2.0 Subagents Documentation.

Asynchronous execution modellink

To maximize developer velocity, Antigravity CLI leverages a multi-threaded asynchronous execution architecture. Instead of locking your terminal session during long-running builds, massive codebase search sweeps, or complex multi-file edits, the primary agent delegates these operations to parallel Subagents or background Tasks.

This delegation model ensures you never have to wait on high-latency AI processes. You can continue drafting code, submitting prompts, or inspecting files while multiple autonomous background threads execute validation tasks in parallel.

Managing agents: The /agents panellink

The active agent-hierarchy and custom agent selection menu are fully transparent and manageable through the interactive Agent Manager Panel (/agents).

Opening the panellink

Type /agents in the prompt and press Enter to open the interactive Agent Manager Panel.

Panel overviewlink

The panel displays a live checklist of all active, completed, killed, or failed background agents:

Identifier: The unique target subagent ID.
Role: The specialized role of the agent (such as “Codebase Researcher” or “Database Debugger”).
State: Live status indicators (running, done, killed, or error).
Step: A real-time summary of the tool or reasoning step currently being executed.

Tip: You can also select and switch between custom agents (or fork conversations) from this panel. See the /agents command reference for full details on custom agent discovery and panel keybindings.

Custom Agents (Markdown Format)link

In addition to built-in agents, the CLI automatically discovers custom agents defined in Markdown format (.md) with YAML frontmatter:

Workspace Agents: .agents/agents/<name>.md or .agents/agents/<name>/agent.md
Global Agents: ~/.gemini/config/agents/

When a custom agent has subagent: true set in its YAML frontmatter, the primary agent can invoke it via invoke_subagent. You can also select custom agents directly as your primary agent in the /agents panel menu.

For the complete schema, frontmatter parameters, and code examples, see Custom Subagents Specification.

Deep-dive monitoringlink

To inspect the inner reasoning, thoughts, and logs of a specific background agent:

Open the /agents panel and highlight the target agent using ↑/↓.
Press Enter to open the Subagent Detail View.
This full-screen view reveals the subagent’s entire reasoning log, including its private internal thoughts, tool calls, and execution outputs.
Press Esc to exit and return to the main Agent Manager list.
Monitoring background tasks with /taskslink

For non-agentic background operations, such as direct shell commands, testing suites, or simple background queries initiated via /btw, use the /tasks command.

text
content_copy
/tasks

The tasks tracking list lets you:

Track standard non-interactive background processes.
Select a task using ↑/↓ and press Enter to view stdout logs.
Terminate runaway terminal processes safely.
Keyboard ergonomicslink

To reduce context-switching friction when subagents require manual interaction or tool authorizations, Antigravity CLI integrates high-efficiency shortcut paths.

Detailed “Teleport” navigation (Alt+J)link

When a subagent encounters a tool requiring approval (e.g. writing a file or running a database migration), a status bar notification blinks.

Press Alt+J inside the main prompt panel to instantly “teleport” from your current conversation directly into the Detail View of the next subagent awaiting your approval.
Confirm or reject the action, and press Esc to teleport back to your primary thread.
“Fast-Path” confirmations (Ctrl+K)link

To authorize an agent action instantly without leaving your active workspace:

Look at the inline status notification displayed right above your active prompt box. It summarizes the pending action (e.g., Subagent 12 asks to run "npm test").
Press Ctrl+K to instantly approve the pending fast-path action without switching panels or opening overlays.
Next stepslink

Configure the visual shell behavior and customize your configuration profiles:

Settings, Rendering & Keybindings: Customize key maps, buffering, and JSON rules.
Permissions & Sandbox: Enforce security containment rings on background processes.
Plugins & Skills: Create your own custom skills and slash commands.
Projects
Sandbox