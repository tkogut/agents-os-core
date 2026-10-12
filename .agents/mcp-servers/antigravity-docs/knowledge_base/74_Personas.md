# Personas
Source URL: https://antigravity.google/docs/sdk/personas

Antigravity SDK
Personas
Markdown
Personas and system instructions
Section titled “Personas and system instructions”

The SDK allows you to customize your agent’s identity, behavioral constraints, and instructions using templated or custom system instructions.

Templated system instructions
Section titled “Templated system instructions”

Templated system instructions are recommended for most applications. This approach preserves default SDK scaffolding and environment context while overriding the persona identity and appending custom structured sections.

For example, you can template system instructions to define an agent that focuses on reviewing a pull request for code quality:

from google.antigravity import Agent, LocalAgentConfig, types

identity = "You are an expert Code Quality Reviewer."
review_criteria = types.SystemInstructionSection(
    title="review_criteria",
    content="- Focus on readability and maintainability.",
)

templated_si = types.TemplatedSystemInstructions(
    identity=identity,
    sections=[review_criteria],
)

config = LocalAgentConfig(system_instructions=templated_si)

async with Agent(config) as agent:
    response = await agent.chat("Review the latest pull request.")
    print(await response.text())
Custom system instructions
Section titled “Custom system instructions”

For complete control, custom system instructions bypass all default SDK scaffolding and environment context, allowing you to pass raw system prompts directly.

For example, you can customize the system instructions to set an identity of a “Custom Code Reviewer”:

from google.antigravity import Agent, LocalAgentConfig, types

custom_si = types.CustomSystemInstructions(
    text="<identity>Custom Code Reviewer</identity>"
)

config = LocalAgentConfig(system_instructions=custom_si)

async with Agent(config) as agent:
    response = await agent.chat("Audit this file.")
    print(await response.text())
Sample code
Section titled “Sample code”

For full working code examples, check out the GitHub repository:

persona_config.py
Previous
Local models
Next
Tools and skills
About Google
Google Products
Privacy
Terms