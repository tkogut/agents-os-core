# Structured output
Source URL: https://antigravity.google/docs/sdk/structured-output

Antigravity SDK
Structured output
Markdown
Outputs, inputs, and streaming
Section titled “Outputs, inputs, and streaming”

The SDK supports multimodal input attachments, real-time response streaming, and Pydantic schema validation for structured JSON output.

Streaming responses and reasoning
Section titled “Streaming responses and reasoning”

In a conversational turn with extended reasoning, the model emits thoughts before generating text response tokens. You can stream internal model thoughts and text tokens as they occur:

import sys
from google.antigravity import Agent, LocalAgentConfig

config = LocalAgentConfig()

async with Agent(config) as agent:
    response = await agent.chat("Solve this riddle and explain your reasoning:")

    # Stream internal model thoughts in real time
    print("Reasoning:")
    async for thought in response.thoughts:
        sys.stdout.write(thought)
        sys.stdout.flush()
    print("\n")

    # Stream conversational response tokens
    print("Response:")
    async for token in response:
        sys.stdout.write(token)
        sys.stdout.flush()
    print("\n")
Multimodal attachments
Section titled “Multimodal attachments”

If you are building a multimodal agentic application, you can also include images and PDFs along with your text prompts.

For example, you can attach a PDF specification and an image using from_file() or Image.from_file():

from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.types import Image, from_file

config = LocalAgentConfig()

async with Agent(config) as agent:
    pdf_spec = from_file("spec.pdf")
    chart_image = Image.from_file("chart.png")
    prompt = [
        "Analyze this chart against the specification:",
        chart_image,
        pdf_spec,
    ]
    response = await agent.chat(prompt)
    print(await response.text())
Structured output with Pydantic
Section titled “Structured output with Pydantic”

In some cases, you may want your agentic application to always output its response in a specific format.

For example, you can enforce typed JSON responses matching Pydantic schemas using response_schema:

import pydantic
from google.antigravity import Agent, LocalAgentConfig

class TaskSummary(pydantic.BaseModel):
    summary: str
    action_items: list[str]

config = LocalAgentConfig(response_schema=TaskSummary)

async with Agent(config) as agent:
    response = await agent.chat("Summarize the meeting notes.")
    data = await response.structured_output()
    print(data["action_items"])
Sample code
Section titled “Sample code”

For full working code examples, check out the GitHub repository:

structured_output.py
streaming.py
multimodal.py
Previous
Subagents
Next
Lifecycle and hooks
About Google
Google Products
Privacy
Terms