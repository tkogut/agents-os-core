# /goal
Source URL: https://antigravity.google/docs/commands/goal

Goal command (/goal)2-0Antigravity AppFeaturesGoal command (/goal) Antigravity App FeaturesAntigravity AppAntigravity CLIAntigravity IDE
Features
Slash commands
/goal
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Antigravity IDE
Goal command (/goal)
Section titled “Goal command (/goal)”

Run a complex, long-running engineering objective autonomously. The agent keeps working, verifying, and fixing until it’s confident the goal is completely fulfilled, instead of yielding back to you after each intermediate step.

Overview
Section titled “Overview”

By default, the agent ends its turn whenever it believes it has answered your request. For long tasks, such as an overnight migration or a sweep that fixes every failing test, that means the agent might stop early, report partial progress, and wait for you to say “keep going.”

The /goal command puts the agent in goal mode for the current request:

No premature stops: whenever the agent tries to end its turn before the goal is complete, Antigravity blocks the stop and prompts the agent to audit its own work and continue.
Evidence-based completion: before concluding, the agent is instructed to map every deliverable in your original request to concrete evidence, such as file contents, test results, and build logs.
Runs until done or cancelled: there’s no iteration cap. The goal ends only when the agent declares it complete or when you ask the agent to stop.
Waits for helpers: goal mode doesn’t force the agent to continue while subagents or background tasks it depends on are still running, so delegated work finishes normally.

Goal mode changes only the agent’s stopping behavior. It doesn’t change your tool permissions or artifact review policies, so any approvals you’d normally be asked for still apply.

Start a goal
Section titled “Start a goal”

Type /goal followed by the objective you want the agent to pursue. Write the objective with explicit, verifiable completion criteria, so the agent knows what evidence to check before it concludes.

Antigravity App
Antigravity CLI
Antigravity CLI

Type the command in the interactive prompt:

/goal Migrate the auth package from session cookies to OAuth2 and make sure all unit and integration tests pass

The agent keeps working across turns in the terminal. Use /tasks to monitor any background shell commands, timers, or subagents it starts along the way.

Note

Only one goal is active at a time in a conversation. Starting a new /goal cancels the previous one.

How goal mode works
Section titled “How goal mode works”

When you start a goal, Antigravity tracks it across every turn until it ends:

Your objective is recorded. The text after /goal becomes the goal, and the agent is told the task is intended to run for a long time without further input.
Stops are intercepted. Each time the agent attempts to finish, a goal stop hook checks whether the goal is still active. If it is, the agent receives a reminder with the time spent so far, the continuation count, and the original request.
The agent audits its work. The reminder instructs the agent to re-read the request, build a checklist of deliverables, and confirm each one against real output rather than assuming effort equals completion.
The goal ends. The agent signals completion when every deliverable is verified, or cancels the goal if you explicitly asked it to stop.
Cancel a goal
Section titled “Cancel a goal”

To stop a running goal, tell the agent to stop or cancel in a follow-up message, for example:

Stop the current goal. I'll take it from here.

The agent marks the goal Cancelled and ends its turn normally. Starting a new /goal also cancels the active one.

Write effective goals
Section titled “Write effective goals”

Goal mode is only as good as the completion criteria you give it. The following patterns help the agent know when it’s genuinely done:

Name the evidence: “all tests in packages/api pass,” “npm run build exits with zero errors,” or “p95 latency in the benchmark is under 50 ms.”
Scope the work: list the packages, services, or files in scope so the agent doesn’t stop early or expand indefinitely.
Plan first for big changes: run /plan or /grill-me before /goal to align on the approach, then hand the approved plan to goal mode for execution.
Pair with a timer: for recurring check-ins during a long goal, use /schedule to have the agent report progress on an interval.
Next steps
Section titled “Next steps”

Explore related documentation:

Plan command (/plan): Draft a reviewable implementation plan before running a long goal.
Schedule command (/schedule): Set timers and recurring check-ins during long-running work.
Subagents: Learn how the agent delegates work that goal mode waits for.
Slash commands overview: Browse every available slash command.
Previous
/generative_ui
Next
/grill-me
About Google
Google Products
Privacy
Terms