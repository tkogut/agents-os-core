# Status Line (/statusline)
Source URL: https://antigravity.google/docs/cli/commands/statusline

Antigravity CLI
>
Commands
>
Status Line (/statusline)
Status Line Command (/statusline)link

Toggle the TUI status line or configure a custom rendering command.

Overviewlink

The /statusline command allows you to quickly enable or disable the status line at the bottom of your TUI, or configure a custom shell command to render it dynamically, without manually editing your settings file.

For details on how to write custom status line scripts and the JSON state payload schema, see the conceptual Status Line Customization Guide.

Usagelink

Run the /statusline command with the following arguments to control its behavior:

Toggle Status Linelink

Type /statusline with no arguments to toggle the status line on and off:

text
content_copy
/statusline
Enable or Disable Explicitlylink

You can explicitly enable or disable the status line:

Enable: /statusline on or /statusline enable
Disable: /statusline off or /statusline disable
bash
content_copy
/statusline off
Configure a Custom Commandlink

To route the agent state JSON payload to a custom script and render its output in the status line, pass the command as an argument:

bash
content_copy
/statusline ~/.gemini/antigravity-cli/statusline.sh

This immediately updates your settings and starts running the script to render the status line.

Revert to Defaultlink

To delete your custom command configuration and revert to the built-in default status line:

bash
content_copy
/statusline delete

(Note: /statusline reset is also supported).

Show Helplink

To view the quick command reference:

bash
content_copy
/statusline help
Next stepslink
Status Line Guide: Learn how to write custom scripts and handle the JSON payload.
Window Title Command: Configure dynamic terminal window titles.
CLI Reference: See all available slash commands.
Resume Command (/resume)
Window Title Command (/title)