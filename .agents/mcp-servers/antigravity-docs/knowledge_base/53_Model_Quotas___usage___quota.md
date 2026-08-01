# Model Quotas (/usage, /quota)
Source URL: https://antigravity.google/docs/cli/commands/usage

Antigravity CLI
>
Commands
>
Model Quotas (/usage, /quota)
Model Quotas (/usage)link

View your active model quota usage and refresh your configuration.

Overviewlink

Antigravity CLI provides the /usage command (alias /quota) to help you monitor your resource consumption. When run, the command refreshes your model configuration and quota status from the backend and opens an interactive TUI panel.

Viewing your usagelink

To open the Model Quotas panel:

Type /usage (or /quota) in the prompt box.
Press Enter.
text
content_copy
/usage

Interactive Panel Featureslink

The panel displays:

Model Quotas: A breakdown of your usage limits and remaining requests/tokens for each supported model (e.g., Gemini 3.5 Flash, Gemini 3.1 Pro).
Active Refresh: The CLI automatically triggers a fresh check of your quotas on disk and from the backend service when you open this panel.
Navigation Controlslink

Use the following keyboard shortcuts to navigate the panel:

Key	Action
↑ / ↓ (or j / k)	Scroll up or down by one line.
PgUp / PgDn	Scroll up or down by one page.
g / G	Jump to the top or bottom of the list.
Esc (or q)	Close the panel and return to the prompt.
Next stepslink
CLI Reference: See all available slash commands and keybindings.
Settings & Rendering: Configure your default models and credit usage preferences.
Window Title Command (/title)
Best Practices