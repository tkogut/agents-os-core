# Terminal title customization
Source URL: https://antigravity.google/docs/cli/title

Terminal title customization - Antigravity CLIcliAntigravity CLIFeaturesTerminal title customization - Antigravity CLI Antigravity CLI FeaturesAntigravity CLI
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

To turn your custom title on or off from the TUI, refer to the Window title command.

Overview
Section titled “Overview”

When you configure a title command, the CLI sets your terminal window title from the command’s output, so you can follow the agent’s progress even when the terminal window is minimized or unfocused. Without a title command, the CLI doesn’t change the window title.

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

Whenever the agent state changes, the CLI runs your command with sh -c (cmd /c on Windows), pipes the session state as JSON to its stdin, and sets your terminal window title from what the command prints to stdout. If the command prints several lines, the CLI joins them with spaces. The CLI removes control characters, including tabs and the escape character, but doesn’t interpret ANSI color codes, so print a single line of plain text.

The title block accepts these properties:

command (string): Shell command that prints the window title.
type (string, default "command"): Optional. "command" is the only supported type.
enabled (boolean, default true): Set to false to stop updating the title. The command stays in settings.json.

Set title to an object, not to true or false. The CLI reads a boolean as an object without a command, so no script runs.

JSON state payload schema
Section titled “JSON state payload schema”

The JSON state payload is the same as the one sent to the custom status line script. It includes detailed properties representing cwd, conversation_id, agent_state, vcs details, and more. Refer to the Status line schema for the complete property list.

Example script
Section titled “Example script”

You can download a complete, layout-adaptive script from the official title.sh example on GitHub. This script sets the title to the agent state, with a matching emoji, followed by the name of your workspace folder.

Save the script to ~/.gemini/antigravity-cli/title.sh and make it executable:

chmod +x ~/.gemini/antigravity-cli/title.sh
See also
Section titled “See also”

Explore the following guides to customize other CLI elements:

Window title command: Turn your custom title on or off.
Status line customization: Customize dynamic TUI status bars.
Settings, rendering, and keybindings: Customize keyboard hotkeys and buffers, and see every title property.
CLI reference: Quick reference for slash commands, keybindings, and configuration keys.
Permissions and sandbox: Manage secure directory permissions.
Previous
Status line customization
Next
Overview
About Google
Google Products
Privacy
Terms