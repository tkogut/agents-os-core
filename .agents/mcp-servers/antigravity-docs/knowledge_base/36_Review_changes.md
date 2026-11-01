# Review changes
Source URL: https://antigravity.google/docs/review-changes

Review changes2-0Antigravity AppFeaturesReview changes Antigravity App FeaturesAntigravity AppAntigravity CLI
Features
Learn
Review changes
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Review changes
Section titled “Review changes”

Check what the agent changed before you keep it. Review the diffs file by file, send line-by-line feedback to the agent, and, in the Antigravity App, commit the result to Git without leaving Antigravity.

Antigravity App
Antigravity CLI
Antigravity CLI

In the Antigravity CLI, the /diff command opens a full-screen diff viewer for the changes in your workspace and conversation.

Open the diff viewer
Section titled “Open the diff viewer”

Type /diff in the prompt box and press ENTER. The viewer opens in the All Changes view. Select a file and press ENTER to open its diff, and press ESC to go back.

Switch views
Section titled “Switch views”

Press ←/→ to switch between these views:

View	Shows
All Changes	Uncommitted changes in your workspace. This is the default.
Per Turn	The changes from each turn of the conversation.
Commit Tree	Your repository’s commit history. Press ENTER on a commit to list the files that it changed.
Comment on lines
Section titled “Comment on lines”

To give the agent feedback, open a file’s diff, move the cursor to a line, press C, type your comment, and press ENTER.

When you exit /diff with unsent comments, the Unsent Comments screen appears. Press Y to send the comments to the agent as your next prompt, or press N to exit without sending them.

For every key, see Diff command (/diff).

Next steps
Section titled “Next steps”

Explore related documentation:

Diff command (/diff): Review changes, turns, and commits in the Antigravity CLI.
Artifacts: Review and comment on plans, walkthroughs, and other deliverables from the agent.
Projects: Choose whether the agent works in your local checkout or in a new Git worktree.
Feature overview: Explore other Antigravity App features.
Previous
Terminal sandbox
Next
Execution modes
About Google
Google Products
Privacy
Terms