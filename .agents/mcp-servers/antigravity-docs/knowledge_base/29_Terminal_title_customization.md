# Terminal title customization
Source URL: https://antigravity.google/docs/cli/title

Features
Learn
Terminal
Terminal title customization
Markdown
AVAILABLE ON:
Antigravity CLI
Terminal title customization
Section titled “Terminal title customization”

Configure dynamic window titles, map custom scripting configurations, and format JSON state outputs to customize terminal headers.

Note

To toggle or set the terminal title interactively, refer to the Window title command.

Overview
Section titled “Overview”

The terminal window title feature displays agent details, active workspace basenames, and active conversation parameters inside your terminal emulator’s title bar. This lets you monitor agent progress even when the terminal window is minimized or unfocused.

Custom title scripting
Section titled “Custom title scripting”

For customized window title formatting, you can route active TUI state details into a custom shell script.

Configuration
Section titled “Configuration”

Add a title configuration block to your ~/.gemini/antigravity-cli/settings.json file:

{
    "title": {
        "type": "command",
        "command": "~/.gemini/antigravity-cli/title.sh"
    }
}

Whenever the agent state changes, the TUI executes your command script, pipes a detailed state JSON payload directly to the script’s stdin, reads your formatted string from stdout, and updates your terminal window title. Non-printable characters and ANSI escape sequences are automatically stripped before rendering.

JSON state payload schema
Section titled “JSON state payload schema”

The JSON state payload is the same as the one sent to the custom status line script. It includes detailed properties representing cwd, conversation_id, agent_state, vcs details, and more. Refer to the Status line schema for the complete property list.

Example script
Section titled “Example script”

You can download a complete, layout-adaptive script from the official title.sh example on GitHub. This script extracts the active workspace folder basename and renders a structured terminal title containing live agent states and conversation session prefixes.

Save the script to ~/.gemini/antigravity-cli/title.sh and make it executable:

chmod +x ~/.gemini/antigravity-cli/title.sh
See also
Section titled “See also”

Explore the following guides to customize other CLI elements:

Window title command: Toggle or set the terminal title interactively.
Status line customization: Customize dynamic TUI status bars.
Settings, rendering, and keybindings: Customize keyboard hotkeys and buffers.
Permissions and sandbox: Manage secure directory permissions.
Previous
Status line customization
Next
Overview
About Google
Google Products
Privacy
Terms