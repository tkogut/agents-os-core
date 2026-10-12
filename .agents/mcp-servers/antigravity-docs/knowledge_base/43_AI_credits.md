# AI credits
Source URL: https://antigravity.google/docs/cli/credits

Features
Learn
Permissions
AI credits
Markdown
AVAILABLE ON:
Antigravity CLI
Managing AI credits and quotas
Section titled “Managing AI credits and quotas”

The Antigravity CLI integrates with your subscription to monitor and manage your AI Premium credits and usage quotas.

For a detailed explanation of baseline quotas, how credits are consumed, and plan eligibility, refer to the main Plans page.

Quota tracking
Section titled “Quota tracking”

You can monitor your active quota and credit consumption directly inside the CLI:

Statusline indicator: The right side of the CLI statusline displays your remaining credit count (for example, AI Credits: 42).
Low quota alert: When your remaining AI credits drop below the warning threshold, the statusline indicator highlights to warn you that your limits are near.
Slash commands and managing balance
Section titled “Slash commands and managing balance”

You can query your credits or buy additional quota directly from the CLI:

Query balance: Run the AI credits command to open the dedicated credits panel. This panel displays your detailed credit usage statistics.
Managing credits: You can purchase AI credits or upgrade your subscription, which opens a panel containing direct pricing and subscription portal links.
Settings configuration
Section titled “Settings configuration”

To control when and how your AI credits are used, you can toggle credit settings in your settings.json file:

{
    "useG1Credits": true
}

You can also configure this option interactively in the CLI:

Use AI credits option: Run /config or /settings to open the CLI settings panel. Set the Use G1 Credits field to on to allow the CLI to use your personal credits when plan quotas are exhausted, or set it to off to restrict fallback billing. To learn more, refer to the Plans overages section.
See also
Section titled “See also”

Explore related commands to monitor your usage and credits:

AI credits command: View and manage your credits interactively in the TUI.
Model quotas command: Monitor your model-specific API quotas.
Previous
Overview
Next
Tab completion
About Google
Google Products
Privacy
Terms