# Overview
Source URL: https://antigravity.google/docs/projects

Projects2-0Antigravity AppFeaturesProjects Antigravity App FeaturesAntigravity AppAntigravity CLI
Features
Learn
Projects
Overview
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Projects
Section titled “Projects”

Projects organize multi-folder workspace configurations, isolated agent settings, and conversation histories across Antigravity surfaces.

Antigravity App
Antigravity CLI
Antigravity CLI
Launching sessions with projects
Section titled “Launching sessions with projects”
Default project execution
Section titled “Default project execution”

When starting the CLI without any project flags, all conversations in the session run in the default-cli-project:

agy
Opening a session in a specific project
Section titled “Opening a session in a specific project”

To open a session attached to a specific existing project, pass the --project flag with the target project ID:

agy --project=<project_id>
Creating a new project on startup
Section titled “Creating a new project on startup”

To create a new project and initialize your CLI session inside it, pass the --new-project flag:

agy --new-project
Resuming an existing conversation
Section titled “Resuming an existing conversation”

If you resume a conversation (whether on startup using --conversation=<conv_id> or during a session using /resume), the CLI automatically uses the conversation’s associated project.

Moving conversations between projects (/fork)
Section titled “Moving conversations between projects (/fork)”

While interacting in an active session, you can copy and continue your current conversation in a different project using the /fork slash command:

/fork <project_id>

When executed, the CLI forks your current conversation and associates the newly created conversation with <project_id>.

Previous
Reviewing artifacts (CLI)
Next
Prompting and interaction
About Google
Google Products
Privacy
Terms