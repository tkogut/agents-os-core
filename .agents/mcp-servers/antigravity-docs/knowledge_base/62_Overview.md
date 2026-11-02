# Overview
Source URL: https://antigravity.google/docs/slash-commands

Slash commands overview2-0Antigravity AppFeaturesSlash commands overview Antigravity App FeaturesAntigravity AppAntigravity CLI
Features
Slash commands
Overview
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Slash commands overview
Section titled “Slash commands overview”

Slash commands provide quick shortcuts for invoking specialized agent workflows, reasoning modes, interactive planning tools, and background automations. These commands operate consistently across both the Google Antigravity App (Desktop and Web) and the Antigravity CLI.

Note

Quick navigation: Type / in any chat input or terminal prompt to open the interactive command autocompletion menu.

Overview
Section titled “Overview”

Modern software development requires different modes of agent interaction depending on the complexity and scope of the task:

Everyday engineering: Standard prompts for interactive feature development, navigation, and refactoring.
Deep reasoning: Multi-agent exploration and independent verification.
Structured planning: Interactive requirement interviews and reviewable plans before modifying code.
Long-horizon campaigns: Collaborative multi-agent teams for repository-scale migrations.
Background tools: Sandboxed browser research, scheduled automations, and side queries.

Slash commands give you precise, instantaneous control over these capabilities.

Command catalog
Section titled “Command catalog”

The following table provides a complete reference for all public slash commands:

/boost
Reasoning
Multi-agent deep reasoning for complex bugs, race conditions, and algorithms.
Paid plans
Seconds to hours
/teamwork
Reasoning
Collaborative agent teams for repo-scale migrations, simulation, and research.
Paid plans
Hours to days
/goal
Reasoning
Autonomous execution until the goal is achieved without intermediate pauses.
All plans
Minutes to hours
/plan
Planning
Researches code, conducts requirement interviews, and drafts a reviewable plan artifact.
All plans
Minutes
/grill-me
Planning
Interviews you one question at a time, with a recommended answer for each, to align on design details and edge cases.
All plans
Minutes
/learn
Customization
Distills session feedback and corrections into persistent Rules or Skills.
All plans
Immediate
/plugin
Customization
Opens the interactive Plugins Manager or manages and creates plugins.
All plans
Immediate
/schedule
Automation
Schedules an instruction as a one-time timer or recurring cron job.
All plans
Scheduled
/browser
Tools
Launches a sandboxed browser subagent for web research and UI inspection.
All plans
Minutes
/btw
Tools
Asks a quick contextual question in the background without pausing work.
All plans
Immediate
/generative_ui
Tools
Builds interactive widgets, such as diagrams, charts, and explainers, as HTML artifacts or inline in the conversation. Antigravity App only.
All plans
Minutes
Reasoning and autonomy
Section titled “Reasoning and autonomy”
/boost
Section titled “/boost”

Activates the on-demand three-tier multi-agent reasoning hierarchy (Orchestrator -> DeepCoder / DeepInvestigator -> isolated workers). It explores multiple hypotheses, runs test suites, and independently verifies solutions before returning results.

To invoke Boost for an algorithmic optimization, run the following command:

/boost Optimize the sparse matrix multiplication routine using SIMD intrinsics and benchmark throughput.

For detailed architectural documentation and CLI keybindings, refer to the Boost deep reasoning guide and the CLI reference.

/teamwork
Section titled “/teamwork”

Initiates the multi-agent framework for multi-day engineering campaigns, subsystem rewrites, and open-ended scientific research. Begins with an interactive scoping interview led by the Sentinel to draft a binding specification plan.

To launch a multi-agent migration, run the following command:

/teamwork Migrate our REST backend from Express to Fastify with full test parity and benchmarks.

For complete multi-agent lifecycle documentation and engineering patterns, refer to the Teamwork agent teams guide.

/goal
Section titled “/goal”

Instructs the agent to work continuously until the specified objective is fully achieved. The agent autonomously runs builds, diagnoses errors, and applies corrective edits without pausing for turn-by-turn confirmations.

To run a test suite repair autonomously, run the following command:

/goal Fix all failing unit tests in the authentication package and ensure 100% pass rate.

For details on how goal mode intercepts stops, audits deliverables, and how to cancel a goal, refer to the Goal command guide.

Planning and requirements
Section titled “Planning and requirements”
/plan
Section titled “/plan”

The /plan slash command facilitates structured planning, codebase exploration, and requirements discovery before jumping directly into execution. It makes sure complex tasks are well-understood, properly scoped, and organized before code changes are made.

How it works
Section titled “How it works”

When you invoke /plan, Antigravity runs a four-step workflow:

Analysis and discovery: The agent examines your prompt, analyzes the workspace, reads relevant source files, and discovers dependencies or potential roadblocks.
Clarification and interviewing: If details are underspecified or architectural decisions are ambiguous, the agent conducts a focused interview with you (leveraging interactive question prompts or structured options) to clarify requirements and trade-offs.
Structured plan creation: The agent creates a comprehensive Implementation Plan artifact detailing the high-level approach, step-by-step task breakdowns with verification gates, and potential risks.
User review and approval: The agent presents the plan artifact for your review. Once you review, comment on, or approve the plan, the agent transitions into execution mode.
When to use /plan
Section titled “When to use /plan”

Use /plan in the following scenarios:

Complex refactors: When refactoring architectural components across multiple files or packages.
Ambiguous requirements: When starting a feature with open questions, trade-offs, or missing specifications.
High-risk changes: For database migrations, core protocol changes, or security-sensitive updates where an upfront checklist and risk assessment are critical.
Collaborative alignment: When you want to review and guide the agent’s proposed steps before any code modifications occur.
Usage examples
Section titled “Usage examples”

To plan a specific task, run /plan with your objective:

/plan Refactor our authentication middleware to support OIDC token verification with JWKS caching

To begin an interactive discovery session for the current workspace context without a predefined prompt:

/plan

For complete workflow details, refer to the Plan slash command guide and the Implementation plan artifact guide.

/grill-me
Section titled “/grill-me”

Has the agent interview you about a task before it starts work. The agent asks one question at a time and recommends an answer for each. It explores the codebase instead of asking you anything the code can answer, and keeps going until you share the same understanding of the task.

To align on design constraints, run the following command:

/grill-me I want to redesign the notification dispatch queue to support priority scheduling.

To turn your answers into a reviewable plan, stack it with /plan (/plan /grill-me <task>). For complete workflow details, refer to the Grill me command guide.

Workflows and customization
Section titled “Workflows and customization”
/learn
Section titled “/learn”

Analyzes recent corrections, user feedback, and debugging resolutions from your active session, distilling them into persistent project rules (AGENTS.md, GEMINI.md, or .agents/rules/*.md) or reusable agent skills (.agents/skills/<name>/SKILL.md). The agent proposes changes in a learning_proposal.md artifact and writes files only after you approve.

To capture recent session patterns into persistent rules, run the following command:

/learn Save our database transaction retry pattern as a project rule for all future database changes.

For the proposal workflow and the full list of rule and skill locations, refer to the Learn command guide and the Rules documentation.

/plugin
Section titled “/plugin”

Manages installed plugins, browses the Marketplace, and packages reusable skills, rules, subagents, MCP servers, and hooks into a single deployable plugin bundle.

In the Antigravity CLI, running /plugin (or its alias /plugins) opens the interactive Plugins Manager panel with Installed and Discover tabs, or executes inline subcommands directly (<marketplace-name> supports the official marketplace, antigravity-plugins-official):

/plugin
/plugin install <plugin-name>@antigravity-plugins-official
/plugin install <local-path>
/plugin list

In the Antigravity App, you can also invoke /plugin with natural-language instructions to enable, disable, install, or scaffold custom plugins.

For complete plugin manifest and marketplace documentation, refer to the Plugins guide and the Marketplace guide.

Automation and scheduling
Section titled “Automation and scheduling”
/schedule
Section titled “/schedule”

Configures the agent to execute a prompt at a specified future time or on a recurring cron schedule using background scheduled tasks.

To set up a daily cleanup routine, run the following command:

/schedule "0 9 * * 1-5" Run git fetch, prune stale local branches, and summarize pending PR reviews.

For timer and cron parameters, managing active schedules, and how /schedule differs from persistent Automations, refer to the Schedule command guide and the Sidecars and scheduled tasks guide.

Tools and context
Section titled “Tools and context”
/browser
Section titled “/browser”

Spawns a sandboxed Chrome browser subagent capable of navigating web pages, reading documentation, inspecting DOM elements, capturing visual screenshots, and verifying frontend layouts.

To verify a local web server layout, run the following command:

/browser Open http://localhost:3000/dashboard, verify that the analytics charts render, and capture a screenshot.

For the subagent’s full tool set, session recordings, and example tasks, refer to the Browser command guide.

/btw
Section titled “/btw”

Submits an out-of-band query that runs in a lightweight background thread without interrupting or pausing the primary agent’s active execution.

To ask an aside while an implementation is running, run the following command:

/btw Which file did you say defines the UserSession interface?

For CLI card navigation, history browsing, and /copy btw clipboard support, refer to the Side question (/btw) command guide.

/generative_ui
Section titled “/generative_ui”

Has the agent build an interactive widget, such as a diagram, chart, or step-by-step explainer, as an HTML artifact that you open in the side panel. Compact widgets can also appear inline in the conversation. Available in the Antigravity App only.

To see how a request moves through your middleware, run the following command:

/generative_ui Show a simple left-to-right diagram of a request going from the client through requireApiKey and the bookmarks router to the database, with a toggle for a valid or invalid API key. Use icons, short labels, and no code.

For placement, sizing, and sandbox details, refer to the Generative UI command guide.

Command selection guide
Section titled “Command selection guide”

The following decision guide outlines when to use each command based on your task requirements:

Primary Objective	Recommended Command	Key Capability
Complex bug, race condition, or algorithmic puzzle	/boost	Multi-agent deep reasoning with isolated verification loops.
Multi-day project, repository migration, or research	/teamwork	Collaborative agent teams with scoping interviews and milestone roadmaps.
Feature requiring review before making code edits	/plan	Researches code, interviews requirements, and generates a reviewable plan.
Vague requirements needing architectural alignment	/grill-me	Conducts a step-by-step interview to clarify edge cases and constraints.
Task that should run continuously until 100% complete	/goal	Autonomous execution without turn-by-turn confirmation pauses.
Distill recent corrections into permanent project rules	/learn	Analyzes session patterns and writes persistent rules and skills.
Discover, install, or manage plugins and marketplace bundles	/plugin	Interactive Plugins Manager in the CLI and conversational plugin management.
Web research, UI validation, and layout inspection	/browser	Sandboxed Chrome browser subagent for live page interactions.
One-shot countdown timer or recurring background schedule	/schedule	Runs instructions in the background on cron schedules.
Quick side query without pausing primary agent work	/btw	Lightweight out-of-band query executed in the background.
Visual explanation, diagram, chart, or clickable prototype	/generative_ui	Interactive HTML widgets in the side panel or inline in the conversation (Antigravity App only).
Cross-surface compatibility
Section titled “Cross-surface compatibility”

Public slash commands are supported across Antigravity developer surfaces:

Surface	Input Method	Navigation and Management
Antigravity App (Desktop and Web)	Type / in the prompt input or select from the command menu.	Model selector dropdown, Artifact review panel, Visual diff viewer.
Antigravity CLI	Type / in the interactive prompt box.	/agents panel, ALT+J (switch threads), CTRL+O (trajectory).
Next steps
Section titled “Next steps”

Explore related documentation and guides:

Boost deep reasoning (/boost): Dive deep into the three-tier multi-agent reasoning hierarchy.
Plan slash command (/plan): Conduct structured planning, requirement discovery, and interactive interviews.
Teamwork agent teams (/teamwork): Learn how collaborative agent teams tackle large-scale migrations.
Side question command (/btw): Ask quick background questions without adding to your conversation history.
Goal command (/goal): Run long-horizon tasks autonomously until every deliverable is verified.
Learn command (/learn): Persist session corrections as rules and skills through a reviewable proposal.
Schedule command (/schedule): Set one-shot timers and recurring cron schedules within a conversation.
Browser command (/browser): Delegate web tasks and UI verification to the browser subagent.
Generative UI command (/generative_ui): Have the agent show answers as interactive widgets in the Antigravity App.
Implementation plans artifact guide: Master reviewable planning artifacts and structured workflows.
Rules: Persist project-wide patterns and conventions.
Plugins (/plugin) and Marketplace: Discover, install, and package reusable agent extensions.
Sidecars and scheduled tasks (/schedule): Automate routine maintenance with cron expressions.
Previous
Vim editor mode
Next
/agents
About Google
Google Products
Privacy
Terms