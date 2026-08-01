# Feature Overview
Source URL: https://antigravity.google/docs/features

Antigravity 2.0
>
Feature Overview
Antigravity 2.0 Featureslink
Projectslink

In Antigravity 2.0, agents work in Projects (previously in Agent Manager, agents were strictly mapped to a single workspace folder).

Worktree Support: Projects natively support Git worktrees, allowing agents to operate in isolated background folders.
Scoped Settings: Settings are scoped, allowing you to have different security settings per project. This means you can have a more permissive setting for a trusted project and a more restrictive security setting for an untrusted folder. The main three presets are “Default”, “Full machine” and “Unrestricted” (see the settings tab for the full list).
Scoped Permissions: Attach permission grants to projects to control what the agents are allowed to access. Permissions manually granted during a conversation can persist, allowing the agent to learn trusted actions and enabling a more seamless experience over time.
Multi-Folder Access: A project can be configured to work in multiple folders, allowing agents to operate across different codebases within the same conversation.
Conversations outside of projectslink

Start quick, one-off conversations outside of any Project. These sessions run in an isolated local scratch folder. They have their own settings, and they also have their own permissions in addition to inheriting from global permissions.

Scheduled Taskslink

We’re introducing scheduled tasks, allowing users to plan ahead with their projects. Utilizing the newest Gemini 3.5 Flash model, users can schedule messages to be sent to their agents while they’re away.

Repeatable: Set up time-based triggers to start conversations periodically.
Tasks will be set to repeat on the minute you’ve set them.
Secure by Defaultlink

We put you in the driver’s seat with robust security controls:

Interactive Approvals: By default, agents will request your explicit permission before running any terminal commands.
Bounded Access: By default, your agent can only read and write within the provided folders of a project. If you change your security preset to “Full Machine” or “Unrestricted”, the agent will have read and write access over your full machine.
Voice transcriptionlink

Antigravity features a built-in live voice transcription, allowing you to prompt agents and leave feedback using natural speech.

How to Use:

Start/Stop: Click the mic button next to the text input box to start recording, click it again to stop.
Live View: As you speak, your words are transcribed in real-time directly into the input field.
Shortcut: You can start recording by pressing Ctrl + M. Once you’re done, press Ctrl + M to stop recording.

Key Features

Smart Cleanup: Speak naturally without worrying about pauses or perfect phrasing. Once you stop recording, the system automatically cleans up the transcription, resolving self-corrections, repetitions, and filler words into a cohesive prompt.
Conversational Awareness: The model will have context to your conversation, you can use project-specific terminology and expect accurate results.

Availability
Voice input is available across all primary interaction surfaces:

Agent Input: For starting conversations and sending prompt updates.
Artifact Comments: For leaving precise, inline feedback on plans, code diffs, and deliverables.
JSON Hookslink

JSON Hooks allow you to execute custom local shell scripts at critical stages of an Antigravity agent’s execution cycle. You can intercept and control the agent’s behavior before tool calls, after model responses, or at loop stopping conditions—configured globally or per-workspace via simple JSON files.

Explore the JSON Hooks & Rules Documentation

Browserlink

We reworked the browser subagent in Antigravity 2.0.

On-demand: Can be invoked through the /browser command.
Chrome DevTools integration: The browser subagent also integrates natively with Chrome DevTools MCP.
Video recording: Now supports recordings as webm videos.
Build with Google
Models