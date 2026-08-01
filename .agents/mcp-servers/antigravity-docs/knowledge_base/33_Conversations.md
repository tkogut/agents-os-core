# Conversations
Source URL: https://antigravity.google/docs/cli/conversations

Antigravity CLI
>
Conversations
Managing conversationslink

Resume prior development threads, scope active histories to local workspaces, and fork conversations to experiment with alternate architectures.

Workspace scopinglink

To maintain context hygiene, Antigravity CLI scopes conversation histories directly to your current working directory. When you launch agy from a specific directory, the agent only displays and resume sessions associated with that specific local repository or subdirectory.

This prevents context pollution, ensuring that the agent’s semantic memory and token limits remain focused solely on the relevant codebase.

Resuming sessionslink

You can return to a prior conversation at any time to continue an implementation, refine a solution, or recover from an interrupted session.

Antigravity CLI supports both an interactive Session Picker TUI overlay and direct command-line flags (agy -c / agy --continue) to resume threads instantly based on your active workspace.

For a complete walkthrough of the interactive picker, keyboard shortcuts, and details on how the directory-scoped session cache works, see the dedicated Resume Command Guide.

Branching with /forklink

When engineering a complex feature, you may want to explore multiple design alternatives without losing your progress. The /fork command enables safe, parallel experimentation.

text
content_copy
/fork

(Alias: /branch)

The /fork command clones your entire conversation history up to the current turn into a new, independent session.

Forking workflowlink
Type /fork inside the prompt panel and press Enter.
The CLI allocates a new unique session ID and duplicates your existing workspace state and agent thread.
Your active terminal switches immediately to the new branch.
If the experiment fails, run /resume to restore your original, stable conversation branch.
lightbulb
Branching Filesystems: Forking clones the conversation thread, not your local git checkout. To fully isolate files during parallel forks, use git branches or stash local changes before testing contrasting approaches.
Next stepslink

Explore how the agent handles complex, asynchronous operations and parallel tasks:

Background Tasks & Subagents: Monitor subagents and handle fast-path approvals.
Settings, Rendering & Keybindings: Configure rendering buffers and override JSON preferences.
Permissions & Sandbox: Manage security profiles and system command lists.
Reviewing Artifacts
Choose an execution mode