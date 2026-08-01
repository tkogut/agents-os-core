# Permissions (/permissions)
Source URL: https://antigravity.google/docs/cli/commands/permissions

Antigravity CLI
>
Commands
>
Permissions (/permissions)
Permissions Command (/permissions)link

Manage your fine-grained agent permission rules interactively within the TUI.

Overviewlink

Antigravity CLI uses a fine-grained permissions engine to secure your workstation. While you can configure these rules manually in your settings file, the /permissions command opens an interactive Permissions Manager TUI panel to view, add, edit, and delete rules live.

For details on how the permission engine works, supported actions, and manual configuration, see the conceptual Permissions Guide.

Managing permissions interactivelylink

To open the Permissions Manager:

Type /permissions in the prompt box.
Press Enter.
text
content_copy
/permissions
Navigation and controlslink

The Permissions Manager operates in three panels:

Scope Picker: Select the configuration scope you want to edit:

Project: Rules applying only to the active project (disabled if no project is open).
Shared: Rules shared across all Antigravity products.
Global: Global rules applying to all your sessions.

Use ↑/↓ (or j/k) to navigate, Enter to select, and Esc to exit.

Rule Viewer: View the rules configured for the selected scope.

Switch between allowlist, denylist, and asklist tabs using ←/→ (or Tab).
Scroll through the rules using ↑/↓ (or j/k).
Press a to add a new rule.
Press e (or Ctrl+G) to edit the highlighted rule.
Press d (or Backspace) to delete the highlighted rule.
Press Esc to return to the Scope Picker.

Add/Edit Rule: Type or edit a rule in the input field.

Rules must follow the action(target) format (e.g., command(git)).
Press Enter to validate and save the rule.
Press Esc to cancel.
Step-by-step walkthroughlink

Here is how to view, add, edit, and delete rules live in the TUI.

1. Selecting a scope and viewing ruleslink

When you run /permissions, you first see the Scope Picker. Select Global to manage your global rules:

Press Enter to open the Rule Viewer for the selected scope. You can use ←/→ to switch between the allow, deny, and ask tabs:

2. Adding a permission rulelink

To allow the agent to run git commands automatically without prompting:

In the Rule Viewer, press a. The Add Rule panel opens at the bottom:

Type command(git) in the input field:

Press Enter. The rule is validated and saved. You are returned to the Rule Viewer, and command(git) now appears in your allowlist:

3. Editing a permission rulelink

If you want to restrict the agent so it can only run git diff automatically, you can edit the rule:

In the Rule Viewer, use ↑/↓ to highlight command(git).
Press e (or Ctrl+G). The input panel opens, prefilled with command(git).
Modify the text to command(git diff).
Press Enter to save. The old rule is replaced by the new one.
4. Deleting a permission rulelink

To remove a rule and revert to prompting for those actions:

In the Rule Viewer, highlight the rule you want to delete (e.g., command(git diff)).
Press d (or Backspace).
The rule is immediately removed from the list.
Next stepslink
Permissions Guide: Learn about the security model, action types, and wildcard matching.
Sandbox & Security: Configure the native OS container for running commands.
CLI Reference: See all available slash commands and keybindings.
Diff Command (/diff)
Resume Command (/resume)