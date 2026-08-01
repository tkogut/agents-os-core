# Window Title
Source URL: https://antigravity.google/docs/cli/title

Antigravity CLI
>
Customizations
>
Window Title
Terminal title customizationlink

Configure dynamic window titles, map custom scripting configurations, and format JSON state outputs to customize terminal headers.

info
To toggle or set the terminal title interactively, see the Window Title Command.
Overviewlink

The terminal window title feature displays agent details, active workspace basenames, and active conversation parameters inside your terminal emulator’s title bar. This lets you monitor agent progress even when the terminal window is minimized or unfocused.

Custom title scriptinglink

For customized window title formatting, you can route active TUI state details into a custom shell script.

Configurationlink

Add a title configuration block to your ~/.gemini/antigravity-cli/settings.json file:

json
content_copy
{
  "title": {
    "type": "command",
    "command": "~/.gemini/antigravity-cli/title.sh"
  }
}

Whenever the agent state changes, the TUI executes your command script, pipes a detailed state JSON payload directly to the script’s stdin, reads your formatted string from stdout, and updates your terminal window title. Non-printable characters and ANSI escape sequences are automatically stripped before rendering.

JSON state payload schemalink

The JSON state payload is the same as the one sent to the custom status line script. It includes detailed properties representing cwd, conversation_id, agent_state, vcs details, and more. See the Status Line Schema for the complete property list.

Example scriptlink

You can download a complete, layout-adaptive script from the official title.sh example on GitHub. This script extracts the active workspace folder basename and renders a structured terminal title containing live agent states and conversation session prefixes.

Save the script to ~/.gemini/antigravity-cli/title.sh and make it executable:

bash
content_copy
chmod +x ~/.gemini/antigravity-cli/title.sh
See alsolink
Window Title Command: Toggle or set the terminal title interactively.
Status Line Customization: Customize dynamic TUI status bars.
Settings, Rendering & Keybindings: Customize keyboard hotkeys and buffers.
Permissions & Sandbox: Manage secure directory permissions.
Status Line Customization
Agents Command (/agents)