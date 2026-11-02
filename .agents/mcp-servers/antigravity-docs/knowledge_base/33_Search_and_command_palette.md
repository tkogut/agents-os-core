# Search and command palette
Source URL: https://antigravity.google/docs/search

Search and command palette2-0Antigravity AppFeaturesSearch and command palette Antigravity App FeaturesAntigravity AppAntigravity CLI
Features
Learn
Search and command palette
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Search and command palette
Section titled “Search and command palette”

Find a past conversation, a file, or a command without leaving the keyboard. In the Antigravity App, the command palette searches the full text of your conversations, including your prompts and the agent’s responses. In the Antigravity CLI, /resume finds past conversations and /codesearch searches the code in your workspace.

Antigravity App
Antigravity CLI
Antigravity CLI
Find past conversations
Section titled “Find past conversations”

Run /resume (or its aliases /switch and /conversation) in the prompt box to open the conversation picker:

/resume

Type to filter the list by conversation title, the first line of your first prompt, or conversation ID. The picker doesn’t search the full text of your conversations, so it doesn’t find words that appear only later in a conversation, such as in the agent’s responses. Press ENTER to resume the selected conversation.

To find a conversation that you started in the Antigravity App, press TAB to switch to the Other tab. Select the conversation, press ENTER, and then press Y to import a copy into the CLI.

You can also resume a conversation when you start the CLI:

Run agy -c to resume the most recent conversation in the current folder.
Run agy --conversation <conversation-id> to resume a specific conversation.

To learn how to rename, delete, and import conversations, see Resume command (/resume).

Search code
Section titled “Search code”

Run /codesearch (or its aliases /cs and /search) followed by your query to search the code in your workspace:

/codesearch requireApiKey

The Code Search panel lists the matches grouped by file. Press ENTER to open the selected match in the file viewer at the matching line. To learn about the query syntax, path filters, and line comments, see Code search command (/codesearch).

Next steps
Section titled “Next steps”

Explore related documentation:

Projects: Organize folders, settings, and conversations into projects.
Resume command (/resume): Browse, rename, delete, and import conversations in the Antigravity CLI.
Code search command (/codesearch): Search your workspace code from the Antigravity CLI.
Settings: Configure the Antigravity App and the Antigravity CLI.
Previous
Remote Control
Next
Marketplace
About Google
Google Products
Privacy
Terms