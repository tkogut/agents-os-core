# Agents (/agents)
Source URL: https://antigravity.google/docs/cli/commands/agents

Features
Slash commands
Agents (/agents)
Markdown
AVAILABLE ON:
Antigravity CLI
Agents command (/agents)
Section titled “Agents command (/agents)”

Browse, select, and switch between custom agents, or monitor active and completed background subagents directly inside an interactive TUI panel.

Before you begin
Section titled “Before you begin”

Make sure you meet the following prerequisites:

Install Antigravity CLI.
Understand the asynchronous execution model.
Overview
Section titled “Overview”

The /agents command opens the interactive Agent Manager panel. This interface serves two distinct purposes:

Custom agent selection and discovery: Choose between the default agent and custom workflow-specific agents, or discover where to define new agents locally and globally.
Subagent monitoring and control: Track, inspect, or terminate background subagents running concurrently during your active session.

Note

Subagent specification: For complete details on subagent lifecycle states, inter-agent communication, and custom Markdown agent specifications (.md), refer to the Antigravity 2.0 subagents documentation and CLI subagents guide.

To open the panel inside the TUI, type /agents and press ENTER:

/agents

Custom agent selection and discovery
Section titled “Custom agent selection and discovery”

Antigravity CLI supports loading custom agent definitions with specialized system instructions and tool permissions. The Available Agents section lists all agents currently available to your session.

Switching between agents
Section titled “Switching between agents”

To switch between agents in the panel, use the following controls:

Select: Use ↑/↓ to highlight an agent (Default agent or a custom agent) under Available Agents, then press ENTER.
Status indicator: A green circle (●) indicates the active or prepared agent.
Apply and exit: Press ESC to close the panel and apply your selection.

Note

If you’re currently inside an active conversation, switching custom agents automatically forks your current session ([ Switch will fork the current conversation on exit ]) so you don’t lose context. If you start from a fresh session, the switch applies directly ([ Switch will create a new conversation on exit ]).

Creating custom agents
Section titled “Creating custom agents”

The header of the /agents panel displays template locations for creating new custom agents:

Create New Agents
  Workspace: {workspace}/.agents/agents/{agent_name}/agent.md
  Global: ~/.gemini/config/agents/{agent_name}/agent.md

To create a custom agent that is available across all your workspaces and projects, place it under your global customization directory (~/.gemini/config/agents/). Create a directory matching your agent name and add an agent.md file with YAML frontmatter:

mkdir -p ~/.gemini/config/agents/code-reviewer
cat << 'EOF' > ~/.gemini/config/agents/code-reviewer/agent.md
---
name: code-reviewer
description: Rigorous code review specialist focusing on edge cases and security.
---
You are an expert code reviewer. Analyze diffs carefully and verify edge cases.
EOF

When you reopen /agents, the CLI automatically discovers code-reviewer and lists it under Available Agents. If you need an agent scoped strictly to a single project repository, place it inside that workspace’s .agents/agents/ directory (for example, /home/user/projects/my-app/.agents/agents/code-reviewer/agent.md). You can also package and distribute custom agents inside plugins.

Subagent monitoring and control
Section titled “Subagent monitoring and control”

When your primary agent delegates tasks (such as running tests or querying large codebases), the spawned threads appear in the /agents panel under Subagents, grouped by their triggering prompt.

Inspecting subagent progress
Section titled “Inspecting subagent progress”

Use the following controls to monitor subagent status and logs:

Group toggling: Press ENTER on a subagent group header (▸ Subagents (1 running, 2 done)) to expand or collapse (▾) that group.
Status indicators: Each subagent row displays a live lifecycle state:
running: Actively executing tools or generating reasoning steps.
done: Completed its assigned background task.
error: Encountered a terminal failure during execution.
killed: Terminated manually by you or the parent process.
Detail view: Highlight a specific subagent row and press ENTER to open the full-screen Subagent Detail View. This view displays the subagent’s complete internal thoughts, tool calls, and execution stdout. Press ESC to return to the list.
Terminating active subagents
Section titled “Terminating active subagents”

If a background subagent loops or runs longer than needed, you can terminate it immediately without leaving your session:

Open /agents and highlight the running subagent row.
Press K to terminate the active subagent and all its child threads.
Inline tool approvals
Section titled “Inline tool approvals”

If a subagent attempts a protected operation (such as modifying a file or running a shell command in a sandboxed environment), the authorization prompt displays inline in the /agents panel. You can press A to approve or D to deny directly from the list.

Panel keybindings reference
Section titled “Panel keybindings reference”

When focused inside the /agents panel, the following keyboard shortcuts apply:

Key	Action	Behavior
↑ / ↓	Navigate	Move the cursor between headers, subagents, and available agents.
ENTER	Select / Toggle	Expand/collapse groups, open Subagent Detail View, or select a custom agent.
K	Kill Active Subagent	Instantly cancel (CancelSubagent) the highlighted running subagent.
ESC	Go Back	Exit the panel, return to the prompt box, and apply any prepared agent switch.
Common mistakes
Section titled “Common mistakes”
Mistake	Why it fails	Fix
Expecting custom agent switches to modify turn history	Switching agents forks the conversation to preserve historical integrity	Continue your workflow in the newly forked session
Placing agent files directly in config root	Scanner looks specifically inside agents/ directories	Move definition to .agents/agents/<name>/agent.md
Pressing K on completed subagents	Only targets active (running) subagent processes	Press ENTER to inspect completed logs instead
Next steps
Section titled “Next steps”

Explore the following guides to learn more about subagents and permissions:

Background tasks and subagents: Learn more about the multi-threaded asynchronous execution architecture.
Plugins and skills: Discover how to bundle custom agents, skills, and MCP configurations into shareable plugins.
Permissions and sandbox: Configure security guardrails and approval rules for background subagents.
Previous
Teamwork (/teamwork-preview)
Next
Code search (/codesearch)
About Google
Google Products
Privacy
Terms