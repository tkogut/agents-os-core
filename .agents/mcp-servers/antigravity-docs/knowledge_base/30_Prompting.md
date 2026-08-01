# Prompting
Source URL: https://antigravity.google/docs/cli/prompting

Antigravity CLI
>
Prompting
Prompting & interactionlink

Master primary interaction patterns, multiline composition workflows, session interruption controls, and terminal media pasting.

The prompt boxlink

Antigravity CLI features a sticky prompt panel positioned at the bottom of your terminal screen. This panel handles standard user entries, multiline scripts, and direct media pasting.

text
content_copy
───────────────────────────────────────────────────────────────────────────
> Describe your next engineering task here...
───────────────────────────────────────────────────────────────────────────
Submitting promptslink

To initiate an agent turn, type your instruction into the prompt panel and press Enter. The agent immediately analyzes your current directory workspace, reads required configurations, and begins formulating an execution plan.

Interrupting active sessionslink

If the agent initiates an undesired task or loops during command execution, press Esc to immediately halt the session.

lightbulb
Universal Escape: The Esc key acts as a global escape hatch. Pressing Esc instantly cancels any active agent turn, closes overlay panels, and returns focus to a clean prompt box.
Multiline compositionlink

For complex directives, structured test scenarios, or multi-paragraph instructions, use our built-in multiline features.

Shorthand newline insertionslink
Standard: Press Shift+Enter or ctrl+j to insert a clean newline within your active prompt window without submitting.
macOS Terminal Fallback: If using Apple Terminal (which does not forward Shift+Enter by default), press Option+Enter. Ensure you check Use Option as Meta key in your Terminal Preferences profile.
Universal Slash Escape: Type a trailing backslash \ at the end of your active line and press Enter. The CLI automatically removes the backslash and inserts a newline.
Editing prompts in $EDITORlink

To draft or edit extensive prompt structures in your primary development editor:

Press ctrl+g inside the empty prompt panel.
The CLI launches your system’s default text editor (such as vim, nano, or code, configured via /config or your environment’s $EDITOR variable).
Draft your multi-line instruction inside the temporary editor buffer.
Save and exit the editor. The CLI automatically imports the edited buffer directly back into the terminal prompt.
Attaching medialink

Antigravity CLI supports pasting rich media formats directly from your system clipboard. Press ctrl+v (or native terminal paste) inside the prompt panel to attach screenshot mockups or video recordings.

Supported file typeslink
Images: PNG, JPEG, GIF, WebP, BMP, TIFF, and SVG.
Videos: MP4, MOV, WebM, and AVI.
Next stepslink

After mastering interaction patterns, explore how the agent presents actions and requests verification:

Reviewing Artifacts: Learn to inspect and manage file edits, plans, and test executions.
Managing Conversations: Resume prior threads and fork active sessions.
Background Tasks & Subagents: Monitor asynchronous background agents.
Migration
Headless mode