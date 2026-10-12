# Custom subagents
Source URL: https://antigravity.google/docs/subagents

Features
Extend
Custom subagents
Markdown
AVAILABLE ON:
Antigravity 2.0
Antigravity CLI
Custom subagents
Section titled “Custom subagents”

Delegate parallel builds, multi-file code generation, and research sweeps to concurrent background subagents while maintaining your active programming flow.

Antigravity 2.0
Antigravity CLI
Antigravity 2.0
Invoking subagents
Section titled “Invoking subagents”

The parent agent calls the invoke_subagent tool to spawn a new concurrent session with a dedicated role and initial prompt:

Workspace options: The subagent can either inherit the same workspace as its parent (inherit), create an isolated Git worktree (branch), or share directory storage (share).
Context isolation: The subagent runs using the specified model tier but does not inherit the parent’s existing conversation history (context window), starting with a clean slate.
Execution: Once invoked, the subagent immediately begins executing its task. A parent agent can invoke multiple subagents concurrently.
Monitoring: You can directly monitor the progress of any subagent by clicking into its conversation in the subagent panel or pressing Alt+J in the CLI.
Built-in subagents
Section titled “Built-in subagents”

Antigravity comes pre-packaged with several specialized subagents out of the box:

research: Optimized for codebase research, file navigation, and structural exploration.
browser: Operates sandboxed web browsers to perform interactive browser testing (invoked exclusively using the /browser slash command).
self: A direct clone of the calling agent, sharing identical system instructions and toolsets.
Custom subagents
Section titled “Custom subagents”

You can define reusable custom subagents in Markdown format (.md) with YAML frontmatter, or create transient subagents during a session using the define_subagent tool.

Agent location and discovery
Section titled “Agent location and discovery”

Antigravity automatically discovers custom subagent .md files in the following locations:

Location	Path	Scope
Workspace Customizations	.agents/agents/<name>.md or .agents/agents/<name>/agent.md	Workspace / Repository Root
Global Customizations	~/.gemini/config/agents/<name>.md or .../agents/<name>/agent.md	Machine-wide / All Projects
Plugins	plugins/<plugin_name>/agents/	Bundled Plugin Package
Frontmatter configuration (YAML)
Section titled “Frontmatter configuration (YAML)”

Define agent metadata, capability limits, and execution policies using YAML frontmatter at the top of your .md file:

Property	Type	Default	Description
name	string	(Required)	The unique identifier for the custom agent.
description	string	(Required)	Detailed description used by the planner to determine when to delegate tasks to this agent.
tools	string[]	[]	Explicit list of tools permitted for this subagent (for example, view_file, replace_file_content, grep_search, run_command).
mainAgent	boolean	true	If true, allows selection as the primary agent in chat interfaces.
subagent	boolean	true	If true, allows invocation using the invoke_subagent tool.
model	string	inherit	Model tier used when invoked (inherit, flash, or pro).
commandExecutionPolicy	string	sandbox	Auto-execution policy for shell commands (off, auto, eager, sandbox).
mcpServers	object[]	[]	Custom Model Context Protocol servers configured for this subagent.
skills / plugins	string[]	[]	Skill paths (for example, skills/my-helper-skill) or plugin dependencies.

Known issue (tool validation): Specifying an unmapped or misspelled tool name in the tools list may cause the subagent process to hang during execution. Double-check exact tool names (such as view_file or run_command) when configuring custom subagents. Enhanced schema validation and a fix for this behavior are planned for an upcoming update.

System prompt and Markdown body
Section titled “System prompt and Markdown body”

The content following the YAML --- delimiter defines the subagent’s system prompt. You can organize instructions using standard Markdown H1 headings (# System Prompt, # Review Guidelines).

Example Markdown custom agent (code-auditor.md)
Section titled “Example Markdown custom agent (code-auditor.md)”

The following example defines a custom security auditor subagent:

---
name: code-auditor
description: Specialized subagent for security audits, static analysis, and code quality reviews.
tools:
  - view_file
  - grep_search
  - run_command
subagent: true
mainAgent: false
model: pro
commandExecutionPolicy: sandbox
skills:
  - skills/security-checklist
---

# System Prompt
You are an expert security auditor and code reviewer. Your primary objective is to inspect source code for security vulnerabilities, memory leaks, and anti-patterns.

# Review Guidelines
1. Perform thorough static analysis without altering files unless explicitly asked.
2. Flag potential injection flaws, unvalidated inputs, or hardcoded secrets.
3. Provide concise, actionable remediation steps for each finding.
Subagent lifecycle and states
Section titled “Subagent lifecycle and states”

Subagents run asynchronously in the background. At any point during a session, a subagent exists in one of three states.

Running
Section titled “Running”

The subagent is actively executing its task, calling tools, and generating responses:

Cancellation: You can cancel a running subagent by clicking Stop Subagent in the subagent panel (or pressing k in the CLI).
Parent control: The parent agent can interrupt a subagent by sending a message or terminating it.
Idle
Section titled “Idle”

The subagent has completed its task, sent a result message to its parent agent, and paused execution:

Re-awakening: An idle agent automatically re-awakens to the Running state upon receiving a message from another agent.
Context retention: When awoken, the agent retains all context from its prior execution turns.
Killed
Section titled “Killed”

The subagent is permanently terminated and cannot be re-awoken:

Cleanup: Any temporary Git worktrees generated for the subagent are automatically cleaned up.
Visibility: Historical conversation transcripts remain readable in JSONL logs.
Inter-agent communication and nesting limits
Section titled “Inter-agent communication and nesting limits”

Agents communicate by sending messages to each other using unique agent conversation IDs:

Flexible routing: Agents can communicate with parent agents, subagents, or peer agents whose ID is known.
Auto-wake: Sending a message to an idle subagent automatically re-awakens it to process incoming instructions.
Shared transcripts: Agents can read each other’s conversation transcripts to audit multi-step workflows.

Note

Nesting depth limit: A maximum nesting depth of 10 levels (layers of subagents beneath the primary agent) is strictly enforced to prevent runaway recursion or resource exhaustion.

Permissions and configuration inheritance
Section titled “Permissions and configuration inheritance”

Subagents inherit safety configurations from their parent agent to maintain security boundaries:

Inherited scopes: Subagents automatically inherit the parent’s allowed terminal command prefixes, file read/write directory scopes, and sandbox settings.
Workspace access: Parent agents retain full access to their subagents’ workspaces, including isolated Git worktrees.
Permission bubbling: If a subagent encounters a tool execution requiring user authorization, the request automatically bubbles up to the main UI or subagent panel.
Multi-agent orchestrators
Section titled “Multi-agent orchestrators”

Antigravity provides two advanced multi-agent orchestrators designed for different task scales and execution horizons.

Boost deep reasoning (/boost)
Section titled “Boost deep reasoning (/boost)”

Note

Plan availability: Available on Google One AI Premium (Pro and Ultra tiers) and Enterprise plans across Antigravity 2.0 and the Antigravity CLI.

Invoking /boost launches a three-tier multi-agent reasoning hierarchy (Orchestrator -> DeepCoder / DeepInvestigator coordinators -> isolated execution workers). It tackles tough concurrency bugs, algorithmic challenges, and non-trivial refactoring within interactive coding sessions (seconds to hours) with independent verification loops. Learn more in the Boost documentation.

Multi-agent teamwork (/teamwork-preview)
Section titled “Multi-agent teamwork (/teamwork-preview)”

Note

Plan availability: The /teamwork-preview command is available on paid plans across Google Antigravity 2.0 and the Antigravity CLI.

Using /teamwork-preview coordinates a team of specialized AI agents designed for large software projects, multi-file refactoring, and complex research. The team handles milestone decomposition, parallel implementation, and independent verification checks, allowing you to define the high-level goals while the platform manages agent coordination. Learn more in the Teamwork documentation.

Next steps
Section titled “Next steps”

Explore related documentation and guides:

Boost deep reasoning (/boost): Explore on-demand multi-agent reasoning.
Teamwork agent teams (/teamwork-preview): Launch collaborative multi-agent teams for long-horizon projects.
Settings, rendering, and keybindings: Customize key maps, buffering, and JSON rules.
Permissions and sandbox: Enforce security containment rings on background processes.
Plugins and skills: Create your own custom skills and slash commands.
Slash commands catalog: Review all available slash commands across Antigravity surfaces.
Previous
IDE workflows
Next
Lifecycle hooks
About Google
Google Products
Privacy
Terms