# /schedule
Source URL: https://antigravity.google/docs/commands/schedule

Schedule command (/schedule)2-0Antigravity AppFeaturesSchedule command (/schedule) Antigravity App FeaturesAntigravity AppAntigravity CLIAntigravity IDE
Features
Slash commands
/schedule
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Antigravity IDE
Schedule command (/schedule)
Section titled “Schedule command (/schedule)”

Set a one-time timer or a recurring cron schedule that wakes the agent with an instruction, without blocking the conversation while it waits.

Overview
Section titled “Overview”

Some tasks need the agent to come back later: check whether a CI run finished, poll a deployment every few minutes, or send you a status summary at a set time. The /schedule command asks the agent to create that timer or schedule using its built-in schedule tool.

A schedule runs as a background task in the current conversation:

Non-blocking: the agent ends its turn after creating the schedule rather than idling in a shell sleep, so you can keep chatting or let it work on other steps.
Wake-up prompt: when the timer fires or the cron triggers, the agent receives your instruction as a high-priority notification and acts on it.
Conversation-scoped: timers and schedules belong to the conversation that created them. For standing jobs that outlive a session, use a persistent sidecar or Automation instead.
Create a schedule
Section titled “Create a schedule”

Type /schedule followed by when the agent should wake up and what it should do. The agent interprets natural language, a duration, or a five-field cron expression and fills in the tool parameters for you.

Antigravity App
Antigravity CLI
Antigravity CLI

Type the command in the interactive prompt:

/schedule every weekday at 9am, run git fetch, list stale local branches, and summarize open PR reviews

Scheduled timers and recurring jobs appear alongside background shell commands in the /tasks panel and in the status line’s task count.

Schedule types
Section titled “Schedule types”

The schedule tool supports two mutually exclusive modes. The agent picks the mode from your instruction, but you can name the parameters directly if you want precise control.

One-shot timers
Section titled “One-shot timers”

A timer waits for a fixed duration and then fires once:

Parameter	Description
DurationSeconds	Seconds to wait before firing.
Prompt	Instruction delivered to the agent when the timer fires.
TimerCondition	Optional early-cancel condition: never (default), any (any incoming message), or the ID of a specific subagent or background task.

Timers are useful for “check back in N minutes” workflows. With a TimerCondition, the timer is cancelled early when a matching message arrives, such as a subagent finishing, and that message itself wakes the agent, so it doesn’t wait the full duration unnecessarily.

/schedule wait up to 5 minutes for the test subagent to report back, then check its results either way
Recurring cron schedules
Section titled “Recurring cron schedules”

A cron schedule fires repeatedly on a standard five-field cron expression:

Parameter	Description
CronExpression	Standard five-field cron expression, such as */5 * * * * for every five minutes.
Prompt	Instruction delivered on each trigger, suffixed with the iteration number.
MaxIterations	Optional cap on the number of triggers. Defaults to unlimited.
IsDaemon	Optional. When true, the schedule keeps firing after the agent’s current task is done.

Set IsDaemon only for an independent standing job. Non-daemon schedules are tied to the task that created them. When MaxIterations is reached, the agent is notified that the schedule completed.

/schedule every 2 minutes for the next 30 minutes, poll the CI status for PR #482 and tell me when it goes green
Manage active schedules
Section titled “Manage active schedules”

You can inspect and cancel schedules from either surface:

Ask the agent: tell the agent to list or cancel its schedules. It uses its task manager tool to show active timers and jobs and to kill the one you name.
CLI task panel: run /tasks to open the Task Manager. Use the arrow keys to select a timer or recurring job, press K to kill it, press X to remove finished entries, and press ENTER for details.
/schedule compared with Automations
Section titled “/schedule compared with Automations”

/schedule and Automations both run work on a schedule, but at different scopes:

	/schedule	Automations and sidecars
Lifetime	Current conversation	Persists across sessions and restarts
Context	Wakes the existing agent with its full conversation history	Starts a fresh agent conversation on each run
Definition	A tool call the agent makes for you	A sidecar.json manifest with a "builtin": "schedule" entry
Best for	Timers, CI polling, check-ins during a task	Daily reports, nightly maintenance, triage jobs

Use /schedule for anything the agent should do while you’re still working in the conversation. For unattended, recurring jobs that should keep running when no conversation is open, create a scheduled sidecar as described in the Sidecars and scheduled tasks guide.

Next steps
Section titled “Next steps”

Explore related documentation:

Sidecars and scheduled tasks: Define persistent scheduled jobs with the schedule sidecar builtin.
Goal command (/goal): Combine timers with long-running autonomous goals.
Subagents: Learn about the background work that a TimerCondition can wait on.
Slash commands overview: Browse every available slash command.
Previous
/resume
Next
/statusline
About Google
Google Products
Privacy
Terms