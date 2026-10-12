# Local models
Source URL: https://antigravity.google/docs/sdk/local-models

Antigravity SDK
Local models
Markdown
Run agents with local models
Section titled “Run agents with local models”

Run Antigravity agents on your machine using local models without an API key or internet connection.

Depending on your setup, you can configure local model execution using the following classes:

LiteRTAgentConfig: Runs .litertlm model checkpoints (such as Gemma 4 26B A4B) directly on-device using Google AI Edge’s LiteRT runtime.
LocalOpenAIAgentConfig: Connects to an external local server with an OpenAI-compatible API, such as Ollama, LM Studio, or vLLM.
On-device execution with LiteRT
Section titled “On-device execution with LiteRT”

LiteRTAgentConfig runs local models using the LiteRT runtime. When the agent starts, the SDK spins up and manages a local loopback server backed by your .litertlm checkpoint. Supported hardware backends (gpu for Apple Silicon Metal and NVIDIA CUDA, or npu) are detected automatically at startup.

Set up LiteRT and Gemma 4 26B A4B
Section titled “Set up LiteRT and Gemma 4 26B A4B”

Follow these steps to install the dependencies and import the model checkpoint:

Note: A machine with at least 24 GB of VRAM or unified memory is recommended to run the Gemma 4 26B A4B checkpoint (which downloads about 16.8 GB).

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install the SDK and the litert-lm package:

pip install google-antigravity litert-lm

Use the litert-lm CLI to import the Gemma 4 26B A4B checkpoint:

litert-lm import \
  --from-huggingface-repo=litert-community/gemma-4-26B-A4B-it-litert-lm \
  gemma-4-26B-A4B-it-gpu.litertlm \
  gemma4-26b

This command downloads about 16.8 GB and registers the checkpoint at ~/.litert-lm/models/gemma4-26b/model.litertlm.

Note: On macOS, if litert-lm import fails with an SSL certificate verification error, install certifi and export SSL_CERT_FILE before retrying:

pip install certifi
export SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")
Run a local LiteRT agent
Section titled “Run a local LiteRT agent”

Once you have configured LiteRT, run a local LiteRT agent by passing the .litertlm model file in LiteRTAgentConfig. For example:

Note: Use the full path to your model file or use os.path.expanduser() because tilde (~) isn’t expanded automatically.

import asyncio
import os

from google.antigravity import Agent, LiteRTAgentConfig

MODEL_PATH = os.path.expanduser(
    "~/.litert-lm/models/gemma4-26b/model.litertlm"
)


async def main():
    config = LiteRTAgentConfig(model_path=MODEL_PATH)

    async with Agent(config) as agent:
        response = await agent.chat("What files are in the current directory?")
        async for token in response:
            print(token, end="", flush=True)
        print()


if __name__ == "__main__":
    asyncio.run(main())

If you want to let the local agent edit files and run shell commands in a project directory, set workspaces and attach a tool policy. For example:

import asyncio
import os

from google.antigravity import Agent, LiteRTAgentConfig
from google.antigravity.hooks import policy


async def main():
    workspace = os.path.expanduser("~/my-local-project")
    os.makedirs(workspace, exist_ok=True)

    config = LiteRTAgentConfig(
        model_path=os.path.expanduser(
            "~/.litert-lm/models/gemma4-26b/model.litertlm"
        ),
        workspaces=[workspace],
        policies=[policy.allow_all()],
    )

    async with Agent(config) as agent:
        response = await agent.chat(
            "Create a static webpage index.html with a dark-mode toggle."
        )
        async for token in response:
            print(token, end="", flush=True)
        print()


if __name__ == "__main__":
    asyncio.run(main())
LiteRT configuration options
Section titled “LiteRT configuration options”

LiteRTAgentConfig automatically applies the .lightweight() preset when initialized. This preset restricts built-in tools to core coding operations, trims system instructions for smaller context windows, and sets a default context compaction threshold sized for the 64k LiteRT KV-cache.

In addition to standard AgentConfig fields (tools, policies, hooks, mcp_servers, subagents, workspaces, and system_instructions), LiteRTAgentConfig supports the following options:

model_path (string, required): Absolute path to a .litertlm model file.
backend (LiteRTBackend or string, optional): Hardware backend for inference ('gpu', 'npu', or 'cpu'). Defaults to LiteRTBackend.GPU.
enable_speculative_decoding (boolean, optional): Enables multi-token prediction for faster generation. Defaults to False.
cache_dir (string, optional): Directory path for caching compiled model graphs across launches.
compaction_config (CompactionConfig, optional): Overrides the default context compaction threshold.
External OpenAI-compatible servers
Section titled “External OpenAI-compatible servers”

To connect to an external local server that exposes an OpenAI-compatible API (such as Ollama, LM Studio, or vLLM), use LocalOpenAIAgentConfig. Call .lightweight() on the configuration to apply the tool and prompt optimizations designed for local models if needed.

Note: Don’t use LocalOpenAIAgentConfig to connect to litert-lm serve. Use LiteRTAgentConfig instead so the SDK manages the LiteRT server lifecycle for you.

For example, you can connect an agent to a local Ollama server running Gemma 4:

import asyncio
from google.antigravity import Agent, LocalOpenAIAgentConfig


async def main():
    config = LocalOpenAIAgentConfig(
        model="gemma4:26b",
        base_url="http://localhost:11434/v1",
    ).lightweight()

    async with Agent(config) as agent:
        response = await agent.chat("What files are in this directory?")
        async for token in response:
            print(token, end="", flush=True)
        print()


if __name__ == "__main__":
    asyncio.run(main())

LocalOpenAIAgentConfig supports all standard AgentConfig options along with these connection parameters:

model (string or ModelTarget, optional): Model identifier registered on your local server (such as "gemma4:26b" or "gemma-4-26B-A4B-it").
base_url (string, optional): URL of the local server’s OpenAI-compatible endpoint (such as "http://localhost:11434/v1" for Ollama or "http://localhost:1234/v1" for LM Studio).
Sample code
Section titled “Sample code”

To explore full working code examples, check out the following resources:

local_models.py: Getting-started script for LiteRTAgentConfig and LocalOpenAIAgentConfig.
Antigravity Hybrid Gauntlet: Hybrid workflow that pairs a cloud Gemini planner with local Gemma 4 26B agents for on-device code auditing and patching.
Previous
Overview and quickstart
Next
Personas
About Google
Google Products
Privacy
Terms