# Policies
Source URL: https://antigravity.google/docs/sdk/policies

Antigravity SDK
Policies
Markdown
Safety policies and permissions
Section titled “Safety policies and permissions”

The SDK provides a declarative policy engine for controlling tool execution and requesting human approval.

By default, custom Python functions and standard read-only tools are allowed, while high-risk system operations (such as executing shell commands using run_command) require explicit permission or policy rules.

Declarative policy engine
Section titled “Declarative policy engine”

Define explicit rules to allow, deny, or request human approval for tool calls.

For example, you can configure the SDK to require approval when an agent attempts to execute shell commands:

from google.antigravity import LocalAgentConfig
from google.antigravity.hooks.policy import deny, allow, ask_user

async def my_handler(tool_call):
    print(f"Tool approval requested for: {tool_call.name}")
    return True

policies = [
    deny("*"),                                     # Deny all tools by default
    allow("view_file"),                            # Allow file viewing
    ask_user("run_command", handler=my_handler),   # Ask approval for shell
]

config = LocalAgentConfig(policies=policies)
Interactive loop with human approval
Section titled “Interactive loop with human approval”

In CLI applications, you can prompt the user interactively before high-risk tools are executed.

For example, use run_interactive_loop combined with policy.safe_defaults to start a console session that prompts for user approval whenever any write tool (file creation, editing, or shell execution) is requested:

import asyncio
from google.antigravity import LocalAgentConfig
from google.antigravity.hooks import policy
from google.antigravity.utils import interactive
from google.antigravity.utils.interactive import run_interactive_loop

# safe_defaults allows read-only tools and asks user for write operations
policies = policy.safe_defaults(handler=interactive.ask_user_handler)
config = LocalAgentConfig(policies=policies)

if __name__ == "__main__":
    asyncio.run(run_interactive_loop(config))

During execution, interactive approval prompts appear in the console:

Starting interactive loop. Type 'exit' or 'quit' to end.
User: Run the 'ls' command to see what is in this directory.

Policy check: Tool execution requested: run_command
Arguments: {'CommandLine': 'ls -la'}
Allow execution? (y/n) [n]:
Sample code
Section titled “Sample code”

For full working code examples, check out the GitHub repository:

policies.py
human_in_the_loop.py
Previous
MCP
Next
Subagents
About Google
Google Products
Privacy
Terms