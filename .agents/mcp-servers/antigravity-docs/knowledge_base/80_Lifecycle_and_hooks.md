# Lifecycle and hooks
Source URL: https://antigravity.google/docs/sdk/lifecycle

Antigravity SDK
Lifecycle and hooks
Markdown
Lifecycle hooks, triggers, and session persistence
Section titled “Lifecycle hooks, triggers, and session persistence”

The SDK provides mechanisms for background event scheduling, session state persistence, lifecycle hooks, and token cost auditing.

Lifecycle hooks and cost auditing
Section titled “Lifecycle hooks and cost auditing”

You can intercept agent turns, handle tool errors, and audit token usage using lifecycle hook decorators.

For example, you can configure hooks that log user prompts before execution, intercept or modify messages, or handle exceptions gracefully without crashing the agent:

from google.antigravity import Agent, LocalAgentConfig, hooks, types

@hooks.pre_turn
async def log_turn(prompt: str) -> types.HookResult:
    print(f"User prompt: {prompt}")
    return types.HookResult(allow=True)

@hooks.on_tool_error
async def handle_error(err: Exception) -> None:
    print(f"Tool execution failed: {err}")

config = LocalAgentConfig(hooks=[log_turn, handle_error])

async with Agent(config) as agent:
    response = await agent.chat("Analyze repository status.")
    print(await response.text())

    # Token usage auditing
    if response.usage_metadata:
        print(f"Turn tokens: {response.usage_metadata.total_token_count}")
Triggers
Section titled “Triggers”

Triggers allow you to run tasks automatically based on specific schedules or events.

For example, you can configure a trigger to monitor service status every 60 seconds:

import asyncio
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.triggers import every

async def check_status(ctx):
    print("Checking background service status...")

config = LocalAgentConfig(triggers=[every(60, check_status)])

async def main():
    async with Agent(config) as agent:
        print("Agent running. Monitoring status every 60 seconds...")
        await asyncio.sleep(120)

if __name__ == "__main__":
    asyncio.run(main())
Session persistence
Section titled “Session persistence”

Session persistence allows you to persist and restore stateful sessions across application restarts. Note that conversation_id must be at least 32 characters long and consist only of alphanumeric characters and hyphens (underscores are not allowed).

To configure storage directories and session identifiers for saving or loading a session:

from google.antigravity import LocalAgentConfig

# conversation_id persists or restores an existing session
conversation_id = "session-12345678901234567890123456789012"

config = LocalAgentConfig(
    save_dir="./sessions",
    conversation_id=conversation_id,
    app_data_dir="/path/to/custom/storage",
)
Sample code
Section titled “Sample code”

For full working code examples, check out the GitHub repository:

triggers.py
hooks.py
persistence.py
Previous
Structured output
About Google
Google Products
Privacy
Terms