# Status line (/statusline)
Source URL: https://antigravity.google/docs/cli/commands/statusline

Features
Slash commands
Status line (/statusline)
Markdown
AVAILABLE ON:
Antigravity CLI
Status line command (/statusline)
Section titled “Status line command (/statusline)”

Toggle the TUI status line or configure a custom rendering command.

Overview
Section titled “Overview”

The /statusline command allows you to quickly enable or disable the status line at the bottom of your TUI, or configure a custom shell command to render it dynamically, without manually editing your settings file.

For details on how to write custom status line scripts and the JSON state payload schema, refer to the conceptual Status line customization guide.

Usage
Section titled “Usage”

Run the /statusline command with the following arguments to control its behavior.

Toggle status line
Section titled “Toggle status line”

Type /statusline with no arguments to toggle the status line on and off:

/statusline
Enable or disable explicitly
Section titled “Enable or disable explicitly”

You can explicitly enable or disable the status line:

Enable: /statusline on or /statusline enable
Disable: /statusline off or /statusline disable
/statusline off
Configure a custom command
Section titled “Configure a custom command”

To route the agent state JSON payload to a custom script and render its output in the status line, pass the command as an argument:

/statusline ~/.gemini/antigravity-cli/statusline.sh

This immediately updates your settings and starts running the script to render the status line.

Revert to default
Section titled “Revert to default”

To delete your custom command configuration and revert to the built-in default status line, run the following command:

/statusline delete

(Note: /statusline reset is also supported.)

Show help
Section titled “Show help”

To view the quick command reference, run the following command:

/statusline help
Next steps
Section titled “Next steps”

Explore the following guides to further customize your terminal display:

Status line guide: Learn how to write custom scripts and handle the JSON payload.
Window title command: Configure dynamic terminal window titles.
CLI reference: View all available slash commands.
Previous
Resume (/resume)
Next
Window title (/title)
About Google
Google Products
Privacy
Terms