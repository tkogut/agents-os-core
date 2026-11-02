# Mentions and quoting
Source URL: https://antigravity.google/docs/at-mentions

Mentions and quoting2-0Antigravity AppFeaturesMentions and quoting Antigravity App FeaturesAntigravity AppAntigravity CLI
Features
Learn
Mentions and quoting
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Mentions and quoting
Section titled “Mentions and quoting”

Type @ to point the agent at specific files, folders, rules, or past conversations, or quote text that you select, so the agent starts from the right context instead of searching for it. You can also send a message straight to a subagent.

What you can add
Section titled “What you can add”

This table compares the Antigravity App and the Antigravity CLI:

Context	Antigravity App	Antigravity CLI
Files and folders	Type @ and part of the name	Type @ and part of the path
Rules	Type @, then choose Rules	Not available
Past conversations	Type @, then choose Conversation	Not available
Selected text	Select the text, then click Quote	Not available
Subagent messages	Open the subagent and use its message box	Start your prompt with @ and the subagent’s name
Antigravity App
Antigravity CLI
Antigravity CLI
Mention files and directories
Section titled “Mention files and directories”

Type @ in the prompt box to open path suggestions, and keep typing to filter them. Matching is fuzzy, so @bkjs finds src/routes/bookmarks.js. Each suggestion shows its path relative to the workspace, whether it’s a File or a Directory, and its full path. If the conversation has subagents, they’re listed first when @ starts your prompt:

Use these keys in the suggestions list:

Key	Action
↑	Move to the previous suggestion.
↓	Move to the next suggestion.
ENTER	Insert the highlighted path, followed by a space.
TAB	Insert the highlighted path. For a directory, the list then shows what’s inside it.
ESC	Close the suggestions and keep what you typed.

When you pick a path from the list, it stays in your prompt as text, such as @src/routes/bookmarks.js, and the agent also receives the item’s full path when you send the prompt. A path that you type or edit yourself is sent as plain text.

To mention a path outside your workspace, start the query with ~/ or /, for example @~/Develop/. Mentioning a path doesn’t grant access to it: your permission settings still decide whether the agent can read files outside your workspace.

Message a subagent
Section titled “Message a subagent”

To give a subagent new instructions without going through the parent agent, start your prompt with @ followed by the subagent’s name and your message, for example:

@research:API-Key-Header-Researcher Also check whether the tests cover a missing X-API-Key header.

The suggestions list shows each running or finished subagent by its <type>:<role> name, followed by its status, such as [running] or [done], and the start of its task.

Press ENTER to send. The CLI confirms with Sent message to followed by the subagent’s name and your message. A subagent that already finished picks up the message and continues with the context from its earlier work. The name must match a listed subagent exactly (case doesn’t matter); otherwise, the CLI sends the prompt to the parent agent. If you send only the name, the CLI asks you to enter a message.

To monitor subagents and open their full conversations, use the /agents panel.

What the agent receives
Section titled “What the agent receives”

Mentioning a file or folder doesn’t paste its contents into your prompt. This table shows what the agent gets for each kind of context. In the Antigravity CLI, you can add only files and directories.

You add	The agent receives
A file or folder	Its full path. The agent reads it when it needs to.
A line range	The file path and line numbers, not the selected text. The agent reads those lines when it needs to.
A rule	The rule’s full text.
A past conversation	The conversation’s title and ID. The agent reads that conversation’s saved transcript when it needs details.
Quoted text	The text that you quoted.
Terminal output	The output that you selected (up to the last 8 KB) and the terminal’s name.
Next steps
Section titled “Next steps”
Rules: Write rules, including manual rules that you attach with @.
Custom subagents: Learn how subagents run and how to monitor them.
Prompting and interaction: Compose multiline prompts and attach media in the Antigravity CLI.
Slash commands overview: Browse the commands that you can run with /.
Previous
Overview
Next
Remote Control
About Google
Google Products
Privacy
Terms