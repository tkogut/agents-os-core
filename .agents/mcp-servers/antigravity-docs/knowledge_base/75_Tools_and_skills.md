# Tools and skills
Source URL: https://antigravity.google/docs/sdk/tools

Antigravity SDK
Tools and skills
Markdown
Custom tools and agent skills
Section titled “Custom tools and agent skills”

The SDK lets you extend your agent’s capabilities using custom Python functions, built-in web tools, built-in system tools, and agent skills.

For Model Context Protocol (MCP) server configuration, check out the MCP documentation.

Built-in tools reference
Section titled “Built-in tools reference”

The SDK provides identifiers for built-in system tools through the BuiltinTools enum (google.antigravity.types.BuiltinTools).

Identifier	Enum constant	Description
list_directory	BuiltinTools.LIST_DIR	List directory contents.
search_directory	BuiltinTools.SEARCH_DIR	Search within files.
find_file	BuiltinTools.FIND_FILE	Find files by pattern.
view_file	BuiltinTools.VIEW_FILE	Read file contents.
create_file	BuiltinTools.CREATE_FILE	Create a new file.
edit_file	BuiltinTools.EDIT_FILE	Edit an existing file.
run_command	BuiltinTools.RUN_COMMAND	Execute a shell command.
ask_question	BuiltinTools.ASK_QUESTION	Prompt user for input.
start_subagent	BuiltinTools.START_SUBAGENT	Invoke a child subagent.
generate_image	BuiltinTools.GENERATE_IMAGE	Generate or edit images.
search_web	BuiltinTools.SEARCH_WEB	Perform Google Search.
read_url_content	BuiltinTools.READ_URL_CONTENT	Fetch URL content.
finish	BuiltinTools.FINISH	Return final output.
Tool group helpers and filtering
Section titled “Tool group helpers and filtering”

In some cases you may want to restrict the tools that your agent can access. You can control the agent’s active tools in CapabilitiesConfig with enabled_tools or disabled_tools.

For example, you can configure your agent to only have access to read_only built-in tools:

from google.antigravity import LocalAgentConfig, CapabilitiesConfig
from google.antigravity.types import BuiltinTools

config = LocalAgentConfig(
    capabilities=CapabilitiesConfig(
        enabled_tools=BuiltinTools.read_only()
    )
)
Custom Python functions
Section titled “Custom Python functions”

In some cases you may want to create custom Python functions that your agent can leverage. You can register custom Python functions in LocalAgentConfig as tools for your agent.

For example, you can configure your agent to leverage a custom get_weather function:

from google.antigravity import Agent, LocalAgentConfig

def get_weather(city: str) -> str:
    """Returns the current weather for a city."""
    return f"It's sunny in {city}."

config = LocalAgentConfig(tools=[get_weather])

async with Agent(config) as agent:
    response = await agent.chat("What's the weather in Tokyo?")
    print(await response.text())
Built-in web tools
Section titled “Built-in web tools”

Web search (SEARCH_WEB) and URL fetching (READ_URL_CONTENT) tools are enabled by default.

For example, you can ask your agent to perform Google searches or read web pages:

from google.antigravity import Agent, LocalAgentConfig

config = LocalAgentConfig()

async with Agent(config) as agent:
    response = await agent.chat("Search for latest updates on Gemini.")
    print(await response.text())
Agent skills
Section titled “Agent skills”

In LocalAgentConfig, skills_paths accepts paths to individual skill directories containing a SKILL.md file, as well as parent directories containing multiple skill subdirectories.

For example, you can configure your agent to leverage a custom code-review skill:

from google.antigravity import Agent, LocalAgentConfig

config = LocalAgentConfig(
    skills_paths=["/path/to/skills/code-review"],
)

async with Agent(config) as agent:
    response = await agent.chat("Run a code quality audit.")
    print(await response.text())
Sample code
Section titled “Sample code”

For full working code examples, check out the GitHub repository:

custom_tools.py
web_tools.py
agent_skills.py
Previous
Personas
Next
MCP
About Google
Google Products
Privacy
Terms