# Models
Source URL: https://antigravity.google/docs/models

Agent
>
Models
Models
Reasoning Model

For the core reasoning model, Antigravity offers leading frontier models from the Google Vertex Model Garden:

Gemini 3.1 Pro (high)
Gemini 3.1 Pro (low)
Gemini 3 Flash
Claude Sonnet 4.6 (thinking)
Claude Opus 4.6 (thinking)
GPT-OSS-120b

Users can select which reasoning model they want to use within the model selector drop down under the conversation prompt box:

The choice of reasoning model is sticky between user messages within a conversation, so if you change the reasoning model while the Agent is running, it will continue to use the previously selected reasoning model until it has completed its steps for that user turn (or until the user cancels the current execution).

Learn more about reasoning model rate limits in our plans page.

Additional Models

Antigravity uses a number of other models for various parts of the stack that are not customizable:

Nano Banana Pro 2: Used by the generative image tool when the Agent wants to produce a UI mockup, needs images to populate a web page or application, generate system or architecture diagrams, or other generative image tasks.
Gemini 2.5 Pro UI Checkpoint: Used by the browser subagent to actuate the browser, such as clicking, scrolling, or filling in input.
Gemini 2.5 Flash: Used in the background for checkpointing and context summarization.
Gemini 2.5 Flash Lite: Used by the codebase semantic search tool.
Agent
Agent Modes / Settings