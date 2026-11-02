# Marketplace
Source URL: https://antigravity.google/docs/marketplace

Marketplace2-0Antigravity AppFeaturesMarketplace Antigravity App FeaturesAntigravity AppAntigravity CLI
Features
Learn
Marketplace
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Marketplace
Section titled “Marketplace”

The Marketplace lets you discover, install, and manage curated plugins that extend your agent with reusable skills, MCP servers, rules, and subagents.

Note

Cross-surface synchronization: Plugins installed in the Antigravity App are automatically updated and displayed in the Antigravity CLI’s Installed tab.

Antigravity App
Antigravity CLI
Antigravity CLI
Open the plugin manager in the CLI
Section titled “Open the plugin manager in the CLI”

In the Antigravity CLI, open the interactive plugin manager using the /plugin slash command (or its alias /plugins):

/plugin
/plugin
—
Antigravity CLI
Plugins
Installed (6)
Discover (15)
(tab to cycle)
  
[enabled]  
firebase
Prototype, build & run modern apps that users love with Firebase's backend, AI, and operational infrastructure.
> 
[enabled]  
flutter
Official plugin for Dart and Flutter that installs Flutter/Dart Skills, Rules, Custom Agents, and Dart MCP server for building natively compiled, visually...
Description: 
Official plugin for Dart and Flutter that installs Flutter/Dart Skills, Rules, Custom Agents, and Dart MCP server for building natively compiled, visually stunning applications for mobile, web, desktop, and embedded devices from a single codebase
Skills:      
dart-add-unit-test, dart-build-cli-app, dart-collect-coverage, dart-fix-runtime-errors, dart-generate-test-mocks, dart-migrate-to-checks-package, dart-resolve-package-conflicts, dart-run-static-analysis, dart-setup-ffi-assets, dart-use-ffigen, dart-use-pattern-matching, dart-use-primary-constructors, dart-write-documentation, flutter-add-integration-test, flutter-add-widget-preview, flutter-add-widget-test, flutter-apply-architecture-best-practices, flutter-build-responsive-layout, flutter-fix-layout-issues, flutter-implement-json-serialization, flutter-setup-declarative-routing, flutter-setup-localization, flutter-use-http-package
Agents:      
a11y_agent.md
MCP:         
dart-mcp-server
Marketplace: 
antigravity-plugins-official
Path:        
/usr/local/google/home/developer/.gemini/config/plugins/flutter
Version:     
1.0.5
  
[disabled] 
gdocs
Work with Google Docs from your AI tools: read document content, draft and edit docs, and keep local markdown in sync with a doc.
  
[enabled]  
google_slides
Google Slides MCP plugin for Antigravity providing presentation inspection and structural update capabilities.
  
[enabled]  
gsheets
Work with Google Sheets from your AI tools: read and write cell data, create and format spreadsheets, and export results.
  
[enabled]  
workspace
A curated set of tools for tasks that involve Google Workspace products.
Keyboard:
↑/↓
Navigate
←/→
Page
tab
Cycle Tabs
enter
Expand Details
space
Toggle Enable
ctrl+s
Uninstall
esc
Exit

Interactive CLI Plugins Manager — press Tab (or click a tab) to switch between Installed and Discover, ↑/↓ to navigate, Enter to expand details, Space to toggle enable/disable, and Ctrl+S to install or uninstall.

Press TAB to switch between the Installed tab and the Discover tab.

Discover tab
Section titled “Discover tab”

Use the Discover tab to browse the Marketplace catalog and install new plugins:

Search plugins: Start typing to search and filter for specific plugins.
Install from a local directory: Highlight Install from local directory and press ENTER to provide a local filesystem path for plugin installation.
View plugin details: Highlight a plugin and press ENTER to expand its details view. The details view displays the following information:
Description
Included components (MCP servers, skills, rules, agents, and more)
Marketplace name
Version
Install or uninstall: Press CTRL + S on an uninstalled plugin to install it, or press CTRL + S on an installed plugin to uninstall it.

The following example shows the Discover tab with the details of a selected plugin expanded:

After installation
Section titled “After installation”

Once a plugin is installed, the interface updates as follows:

Discover tab: A green dot (●) appears beside the plugin name indicating its installed status.
Installed tab: The plugin name appears in the Installed tab list.
Installed tab
Section titled “Installed tab”

Use the Installed tab to inspect and manage the plugins you have installed:

Search installed plugins: Start typing to filter your installed plugins.
Enable or disable: Press SPACE on an installed plugin to toggle it between enabled and disabled. If the plugin declares required MCP credentials (variables), pressing SPACE opens an interactive prompt to fill in those values before enabling the plugin.
View plugin details: Press ENTER on an installed plugin to expand its details view. The details view displays the following information:
Description
Skills (if applicable)
MCP servers (if applicable)
Rules (if applicable)
Agents (if applicable)
Marketplace name
Local installation path
Version
Uninstall: Press CTRL + S on an installed plugin to uninstall it.
Keyboard shortcuts
Section titled “Keyboard shortcuts”

The following keyboard shortcuts are available in the plugin manager:

Key	Tab	Action
TAB	Both	Switch between the Installed tab and Discover tab.
ANY KEY	Both	Search and filter plugins in the active tab.
ENTER	Both	Expand plugin details (or select Install from local directory in Discover).
CTRL + S	Both	Install an uninstalled plugin, or uninstall an installed plugin.
SPACE	Installed	Toggle enable or disable on an installed plugin.
Inline /plugin commands
Section titled “Inline /plugin commands”

In addition to the interactive panel, /plugin supports inline commands to install, uninstall, enable, disable, and list plugins directly from the prompt without opening the plugin manager UI:

Install from the official marketplace or a local directory: Run the following commands (<marketplace-name> supports the official marketplace, antigravity-plugins-official):

/plugin install <plugin-name>@antigravity-plugins-official
/plugin install <local-path>

For example, running /plugin install firebase@antigravity-plugins-official outputs:

Successfully installed plugin "firebase" from "antigravity-plugins-official".

Manage and list plugins inline: Run the following commands:

/plugin uninstall <plugin-name>
/plugin enable <plugin-name>
/plugin disable <plugin-name>
/plugin list
Install from your shell (agy plugin)
Section titled “Install from your shell (agy plugin)”

Outside an interactive TUI session, you can install and manage plugins directly from your shell using agy plugin:

Install from the official marketplace: Once signed in to agy, specify <plugin-name>@antigravity-plugins-official (<marketplace-name> only supports the official marketplace, antigravity-plugins-official), or pass a bare <plugin-name>, which defaults to <plugin-name>@antigravity-plugins-official:
agy plugin install firebase@antigravity-plugins-official
agy plugin install firebase
Running either command outputs:
Installed plugin "firebase" from antigravity-plugins-official
Install from a GitHub link: Clone and stage a plugin directly from a GitHub repository URL:
agy plugin install https://github.com/<owner>/<repo>
Install from a local directory: Stage a local plugin folder into your profile:
agy plugin install </path/to/local/plugin>
List installed plugins: Run agy plugin list for a human-readable summary of installed plugins and their component counts, or pass --json to output a JSON array with installation paths and component names:
agy plugin list
agy plugin list --json
Enable, disable, or uninstall plugins:
agy plugin enable <plugin-name>
agy plugin disable <plugin-name>
agy plugin uninstall <plugin-name>
Using installed plugins
Section titled “Using installed plugins”

Once a plugin is installed and enabled, its bundled capabilities are available in your workspace automatically:

Component	How to use it in your workflow
Starter prompts	In the Antigravity App (Customizations > Installed), open a plugin’s detail view and click any suggested prompt chip to start a guided task immediately.
Skills	Ask for a task in natural language—Antigravity loads relevant plugin skills on demand using progressive disclosure—or invoke a skill explicitly in chat with /<skill-name>.
MCP servers	Ask the agent to query or act on the connected service (such as Jira, Figma, Datadog, Stripe, or Firebase). Bundled MCP tools (namespaced as <plugin-name>_<server-name>) are available automatically while the plugin is enabled.
Custom agents & subagents	The main agent delegates specialized tasks (such as security reviews or accessibility audits) to bundled subagents automatically. You can also run a plugin’s custom agent directly as your primary session agent via the agent selector in the App, /agents in the CLI, or agy --agent <agent-name> from your terminal (run agy agents to list all available agents).
Rules & Hooks	Run automatically in the background while the plugin is enabled—enforcing coding conventions, SDK standards, and pre- or post-tool policy checks without manual invocation.
Next steps
Section titled “Next steps”

Explore related documentation and guides:

Plugins: Learn how to configure, use, and manage installed plugins across the Antigravity App, Antigravity CLI, and Antigravity IDE.
Build plugins: Author plugin.json manifests, bundle skills, MCP servers, custom agents, rules, and hooks, and validate your plugin locally with agy plugin validate --strict.
Get your plugin in the marketplace: Fill out this interest form to submit your validated plugin to the Antigravity Marketplace.
Build with Google: Explore curated Google plugins for Firebase, Android, Flutter, Chrome DevTools, BigQuery, and more.
CLI reference: View all slash commands and keyboard shortcuts in the Antigravity CLI.
Previous
Search and command palette
Next
Terminal sandbox
About Google
Google Products
Privacy
Terms