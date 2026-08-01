# Projects
Source URL: https://antigravity.google/docs/cli/projects

Antigravity CLI
>
Projects
Projectslink

Manage projects and organize conversation sessions in the Antigravity CLI.

Launching sessions with projectslink
1. Default project executionlink

When starting the CLI without any project flags, all conversations in the session will be in the default-cli-project:

bash
content_copy
agy
2. Opening a session in a specific projectlink

If you want to open a session attached to a specific existing project, pass the --project flag with the target project ID:

bash
content_copy
agy --project=<project_id>
3. Creating a new project on startuplink

If you want to create a brand new project and initialize your CLI session inside it, pass the --new-project flag:

bash
content_copy
agy --new-project
4. Resuming an existing conversationlink

If you resume a conversation (whether on startup via --conversation=<conv_id> or during a session using /resume), the conversation’s associated project will automatically be used.

Moving conversations between projects (/fork)link

While interacting in an active session, you can copy and continue your current conversation to a different project using the /fork slash command:

text
content_copy
/fork <project_id>

When executed, the CLI forks your current conversation and associates the newly created conversation with <project_id>.

Choose an execution mode
Background Tasks & Subagents