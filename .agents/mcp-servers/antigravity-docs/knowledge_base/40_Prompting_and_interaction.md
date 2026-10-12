# Prompting and interaction
Source URL: https://antigravity.google/docs/cli/prompting

Features
Learn
Projects
Prompting and interaction
Markdown
AVAILABLE ON:
Antigravity CLI
Prompting and interaction
Section titled “Prompting and interaction”

Master primary interaction patterns, multiline composition workflows, session interruption controls, and terminal media pasting.

The prompt box
Section titled “The prompt box”

Antigravity CLI features a sticky prompt panel positioned at the bottom of your terminal screen. This panel handles standard user entries, multiline scripts, and direct media pasting.

───────────────────────────────────────────────────────────────────────────
> Describe your next engineering task here...
───────────────────────────────────────────────────────────────────────────
Submitting prompts
Section titled “Submitting prompts”

To initiate an agent turn, type your instruction into the prompt panel and press Enter. The agent immediately analyzes your current directory workspace, reads required configurations, and begins formulating an execution plan.

Interrupting active sessions
Section titled “Interrupting active sessions”

If the agent initiates an undesired task or loops during command execution, press Esc to immediately halt the session.

Note

Universal escape: The Esc key acts as a global escape hatch. Pressing Esc instantly cancels any active agent turn, closes overlay panels, and returns focus to a clean prompt box.

Multiline composition
Section titled “Multiline composition”

For complex directives, structured test scenarios, or multi-paragraph instructions, use the built-in multiline features.

Shorthand newline insertions
Section titled “Shorthand newline insertions”

You can insert newlines using any of the following shortcuts:

Standard: Press Shift+Enter or ctrl+j to insert a clean newline within your active prompt window without submitting.
macOS Terminal fallback: If you’re using Apple Terminal (which doesn’t forward Shift+Enter by default), press Option+Enter. Ensure you check Use Option as Meta key in your Terminal Preferences profile.
Universal slash escape: Type a trailing backslash \ at the end of your active line and press Enter. The CLI automatically removes the backslash and inserts a newline.
Editing prompts in $EDITOR
Section titled “Editing prompts in $EDITOR”

To draft or edit extensive prompt structures in your primary development editor, follow these steps:

Press ctrl+g inside the empty prompt panel.
The CLI launches your system’s default text editor (such as vim, nano, or code, configured using /config or your environment’s $EDITOR variable).
Draft your multi-line instruction inside the temporary editor buffer.
Save and exit the editor. The CLI automatically imports the edited buffer directly back into the terminal prompt.
Attaching media
Section titled “Attaching media”

Antigravity CLI supports pasting rich media formats directly from your system clipboard. Press ctrl+v (or native terminal paste) inside the prompt panel to attach screenshot mockups or video recordings.

Supported file types
Section titled “Supported file types”

The prompt box supports the following media file formats:

Images: PNG, JPEG, GIF, WebP, BMP, TIFF, and SVG.
Videos: MP4, MOV, WebM, and AVI.
Next steps
Section titled “Next steps”

After mastering interaction patterns, explore how the agent presents actions and requests verification:

Reviewing artifacts: Learn to inspect and manage file edits, plans, and test executions.
Managing conversations: Resume prior threads and fork active sessions.
Background tasks and subagents: Monitor asynchronous background agents.
Previous
Overview
Next
Managing conversations
About Google
Google Products
Privacy
Terms