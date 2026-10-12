# Managing conversations
Source URL: https://antigravity.google/docs/cli/conversations

Features
Learn
Projects
Managing conversations
Markdown
AVAILABLE ON:
Antigravity CLI
Managing conversations
Section titled “Managing conversations”

Resume prior development threads, scope active histories to local workspaces, and fork conversations to experiment with alternate architectures.

Workspace scoping
Section titled “Workspace scoping”

To maintain context hygiene, Antigravity CLI scopes conversation histories directly to your current working directory. When you launch agy from a specific directory, the agent only displays and resumes sessions associated with that specific local repository or subdirectory.

This prevents context pollution, ensuring that the agent’s semantic memory and token limits remain focused solely on the relevant codebase.

Resuming sessions
Section titled “Resuming sessions”

You can return to a prior conversation at any time to continue an implementation, refine a solution, or recover from an interrupted session.

Antigravity CLI supports both an interactive Session Picker TUI overlay and direct command-line flags (agy -c / agy --continue) to resume threads instantly based on your active workspace.

For a complete walkthrough of the interactive picker, keyboard shortcuts, and details on how the directory-scoped session cache works, refer to the dedicated Resume command guide.

Branching with /fork
Section titled “Branching with /fork”

When engineering a complex feature, you might want to explore multiple design alternatives without losing your progress. The /fork command enables safe, parallel experimentation.

/fork

(Alias: /branch)

The /fork command clones your entire conversation history up to the current turn into a new, independent session.

Forking workflow
Section titled “Forking workflow”

To fork an active conversation into a new branch, follow these steps:

Type /fork inside the prompt panel and press Enter.
The CLI allocates a new unique session ID and duplicates your existing workspace state and agent thread.
Your active terminal switches immediately to the new branch.
If the experiment fails, run /resume to restore your original, stable conversation branch.

Note

Branching filesystems: Forking clones the conversation thread, not your local Git checkout. To fully isolate files during parallel forks, use Git branches or stash local changes before testing contrasting approaches.

Next steps
Section titled “Next steps”

Explore how the agent handles complex, asynchronous operations and parallel tasks:

Background tasks and subagents: Monitor subagents and handle fast-path approvals.
Settings, rendering, and keybindings: Configure rendering buffers and override JSON preferences.
Permissions and sandbox: Manage security profiles and system command lists.
Previous
Prompting and interaction
Next
Overview
About Google
Google Products
Privacy
Terms