# Lifecycle hooks
Source URL: https://antigravity.google/docs/hooks

Features
Extend
Lifecycle hooks
Markdown
AVAILABLE ON:
Antigravity 2.0
Antigravity CLI
Antigravity IDE
Hooks
Section titled “Hooks”

Hooks allow you to run custom scripts or shell commands at specific points during Antigravity’s execution loop to enforce rules, execute linters, or capture diagnostics.

Antigravity 2.0
Antigravity CLI
Antigravity IDE
Antigravity 2.0
Managing hooks in Antigravity 2.0
Section titled “Managing hooks in Antigravity 2.0”

In Antigravity 2.0, hooks are configured in a hooks.json file located in your customization directory:

Workspace level: .agents/hooks.json in your workspace root.
Global level: ~/.gemini/config/hooks.json.

You can also view and toggle hooks from Settings > Customizations > Hooks. For Antigravity 2.0, <app_data_dir> in hook payloads resolves to ~/.gemini/antigravity.

Schema and file format
Section titled “Schema and file format”

The hooks.json file maps hook names to their event configurations:

{
  "my-linter-hook": {
    "PostToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/lint.sh",
            "timeout": 10
          }
        ]
      }
    ]
  },
  "safety-gate": {
    "enabled": false,
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "command": "./scripts/safety-check.sh"
          }
        ]
      }
    ]
  },
  "reminder": {
    "PreInvocation": [
      {
        "type": "command",
        "command": "./scripts/reminder.sh"
      }
    ]
  }
}
Hook definition fields
Section titled “Hook definition fields”

Each hook definition supports the following fields:

Field	Type	Description
enabled	boolean	Optional. Set to false to disable the hook without removing it. Defaults to true.
PreToolUse	array	Handlers that run before a tool is executed.
PostToolUse	array	Handlers that run after a tool completes.
PreInvocation	array	Handlers that run before Antigravity calls the model.
PostInvocation	array	Handlers that run immediately after each model invocation completes.
Stop	array	Handlers that run when the execution loop terminates.
Supported events
Section titled “Supported events”

Antigravity supports the following hook events:

Event	Description	Matcher Target
PreToolUse	Fires before a tool is executed.	Tool name (for example, run_command)
PostToolUse	Fires after a tool completes.	Tool name
PreInvocation	Fires before the model is called.	N/A (matcher ignored)
PostInvocation	Fires immediately after each model invocation completes.	N/A (matcher ignored)
Stop	Fires when execution terminates.	N/A (matcher ignored)
Matcher
Section titled “Matcher”

For PreToolUse and PostToolUse, you can use a regular expression in the matcher field to specify which tools trigger the hook:

"" or "*": Match all tools.
"run_command": Match exactly run_command.
"run_command|view_file": Match either tool.
"browser_.*": Match any tool starting with browser_.

Note

Note: For PreInvocation, PostInvocation, and Stop, the structure is simpler (a list of handlers directly under the event key) and the matcher is ignored.

Supported tools
Section titled “Supported tools”

For PreToolUse and PostToolUse matchers, you can match against standard tool names, grouped by category.

File and directory operations
Section titled “File and directory operations”

The following tools manage files and directories:

view_file: View the contents of a file.
Arguments: AbsolutePath, StartLine (optional), EndLine (optional), IsSkillFile (optional)
write_to_file: Create new files.
Arguments: TargetFile, Overwrite, CodeContent, Description, IsArtifact (optional), ArtifactMetadata (optional)
replace_file_content: Edit a single contiguous block of text in a file.
Arguments: TargetFile, Instruction, Description, AllowMultiple, TargetContent, ReplacementContent, StartLine, EndLine, TargetLintErrorIds (optional)
multi_replace_file_content: Make multiple, non-contiguous edits to the same file.
Arguments: TargetFile, Instruction, Description, ReplacementChunks (array of chunks), TargetLintErrorIds (optional), ArtifactMetadata (optional)
list_dir: List the contents of a directory.
Arguments: DirectoryPath
find_by_name: Search for files and directories using glob patterns.
Arguments: SearchDirectory, Pattern, Type (optional), Excludes (optional), Extensions (optional), FullPath (optional), MaxDepth (optional)
Search and research
Section titled “Search and research”

The following tools search files and the web:

grep_search: Run fast text searches within specific paths.
Arguments: SearchPath, Query, IsRegex (optional), CaseInsensitive (optional), Includes (optional), MatchPerLine (optional)
search_web: Perform a general web search.
Arguments: query, domain (optional)
read_url_content: Fetch text content of a public URL.
Arguments: Url
System and execution
Section titled “System and execution”

The following tools execute commands and manage permissions:

run_command: Propose a Bash command to run.
Arguments: CommandLine, Cwd, WaitMsBeforeAsync, RunPersistent (optional), RequestedTerminalID (optional)
manage_task: Interact with background tasks.
Arguments: Action ('list', 'kill', 'status', 'send_input'), TaskId (optional), Input (optional)
schedule: Set timers or recurring cron jobs.
Arguments: DurationSeconds (optional), CronExpression (optional), MaxIterations (optional), Prompt
list_permissions: View current resource access grants.
Arguments: None
ask_permission: Request additional scoped permissions.
Arguments: Action, Target, Reason
Agent collaboration
Section titled “Agent collaboration”

The following tools coordinate subagents:

invoke_subagent: Spawn specialized subagents.
Arguments: Subagents (array of specs with Prompt, Role, TypeName, Workspace (optional))
define_subagent: Create a custom subagent.
Arguments: name, description, system_prompt, enable_mcp_tools (optional), enable_write_tools (optional), enable_subagent_tools (optional)
send_message: Communicate with other agents.
Arguments: Recipient, Message
manage_subagents: List or terminate active subagents.
Arguments: Action ('list', 'kill', 'kill_all'), ConversationIds (optional)
Interaction and media
Section titled “Interaction and media”

The following tools handle user interaction and media generation:

ask_question: Ask multiple-choice questions.
Arguments: questions (array of questions with question, options, is_multi_select)
generate_image: Create or edit images.
Arguments: Prompt, ImageName, ImagePaths (optional)
Hook handler configuration
Section titled “Hook handler configuration”

Each item in the hooks array supports the following fields:

Field	Type	Description
type	string	Optional. Currently only "command" is supported. Defaults to "command".
command	string	Required. The shell command to execute.
timeout	integer	Optional. Timeout in seconds. Defaults to 30.
Input and output contract
Section titled “Input and output contract”

Hooks receive input through stdin as JSON and return output through stdout as JSON. Field names use camelCase.

Common input fields
Section titled “Common input fields”

All hooks receive the following system metadata fields in their input payload on stdin:

Field	Type	Description
conversationId	string	The unique UUID of the active agent conversation.
workspacePaths	array of strings	Absolute directory paths representing your mounted workspaces.
transcriptPath	string	The absolute path to the persistent transcript.jsonl conversation logs.
Note: This file lives in <app_data_dir>/brain/<conversationId>/.system_generated/logs/transcript.jsonl where <app_data_dir> is:
~/.gemini/antigravity for Antigravity 2.0
~/.gemini/antigravity-cli for Antigravity CLI
~/.gemini/antigravity-ide for Antigravity IDE

artifactDirectoryPath	string	The absolute path to the directory containing all conversation artifacts and screenshots.
modelName	string	The name or identifier of the model handling the invocation (for example, gemini-3.6-flash-medium).
PreToolUse
Section titled “PreToolUse”

Fires before a tool is executed.

Input fields (stdin):

Field	Type	Description
toolCall	object	Details of the proposed tool call.
toolCall.name	string	The name of the tool being executed (for example, run_command).
toolCall.args	object	Arguments passed to the tool call.
stepIdx	integer	The 0-based index of the current step in the trajectory.
(Common fields)		Includes conversationId, workspacePaths, transcriptPath, artifactDirectoryPath, modelName.

Output fields (stdout):

Field	Type	Description
decision	string	Required. Controls how the tool call is gated:
- "allow": Automatically allows the tool execution.
- "deny": Hard blocks execution immediately.
- "ask": Prompts you for approval, but respects “Always Allow” settings.
- "force_ask": Always prompts you for approval, ignoring cached permissions.
- "deny_unless_prior_grant": Denies execution unless the resource was previously approved in a prior grant.
reason	string	Optional. The explanation shown to the agent or to you for the decision.
permissionOverrides	array of strings	Optional. A list of resource strings (for example, ["read_file(/path)", "command(args)"]) to override default tool permissions.

Example:

Input (stdin):
{
  "toolCall": {
    "name": "run_command",
    "args": {
      "CommandLine": "npm test",
      "Cwd": "/workspace/project",
      "WaitMsBeforeAsync": 5000
    }
  },
  "stepIdx": 19,
  "conversationId": "ec33ebf9-0cba-4100-8142-c61503f6c587",
  "workspacePaths": ["/workspace/project"],
  "transcriptPath": "~/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587/.system_generated/logs/transcript.jsonl",
  "artifactDirectoryPath": "~/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587",
  "modelName": "gemini-3.6-flash-medium"
}
Output (stdout):
{
  "decision": "ask",
  "reason": "Requires confirmation for test execution.",
  "permissionOverrides": ["command(npm test)"]
}
PostToolUse
Section titled “PostToolUse”

Fires after a tool completes.

Input fields (stdin):

Field	Type	Description
toolCall	object	Details of the executed tool call (name and args).
stepIdx	integer	The 0-based index of the completed step.
error	string	Optional. The detailed runtime error message if the tool call failed. Empty if successful.
(Common fields)		Includes conversationId, workspacePaths, transcriptPath, artifactDirectoryPath, modelName.

Output fields (stdout): Returns an empty JSON object {}.

Example:

Input (stdin):
{
  "toolCall": {
    "name": "run_command",
    "args": {
      "CommandLine": "npm test",
      "Cwd": "/workspace/project",
      "WaitMsBeforeAsync": 5000
    }
  },
  "stepIdx": 5,
  "error": "exit status 1",
  "conversationId": "ec33ebf9-0cba-4100-8142-c61503f6c587",
  "workspacePaths": ["/workspace/project"],
  "transcriptPath": "~/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587/.system_generated/logs/transcript.jsonl",
  "artifactDirectoryPath": "~/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587",
  "modelName": "gemini-3.6-flash-medium"
}
Output (stdout): {}
PreInvocation
Section titled “PreInvocation”

Fires before the model is called.

Input fields (stdin):

Field	Type	Description
invocationNum	integer	The 0-indexed sequence number of the current model invocation (the first invocation is 0).
initialNumSteps	integer	The number of steps currently in the trajectory.
(Common fields)		Includes conversationId, workspacePaths, transcriptPath, artifactDirectoryPath, modelName.

Output fields (stdout):

Field	Type	Description
injectSteps	array of objects	Optional. List of steps to inject into the conversation trajectory before the model is called.

Each object in the injectSteps array can have one of the following fields:

toolCall (object): A tool call to execute.
userMessage (string): A message from you.
ephemeralMessage (string): A transient system message.

Example:

Input (stdin):
{
  "invocationNum": 3,
  "initialNumSteps": 10,
  "conversationId": "ec33ebf9-0cba-4100-8142-c61503f6c587",
  "workspacePaths": ["/workspace/project"],
  "transcriptPath": "~/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587/.system_generated/logs/transcript.jsonl",
  "artifactDirectoryPath": "~/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587",
  "modelName": "gemini-3.6-flash-medium"
}
Output (stdout):
{
  "injectSteps": [{"ephemeralMessage": "Remember to lint"}]
}
PostInvocation
Section titled “PostInvocation”

Fires immediately after each model invocation completes.

Input fields (stdin): Same as PreInvocation input fields (invocationNum and initialNumSteps).

Output fields (stdout):

Field	Type	Description
injectSteps	array of objects	Optional. List of steps to inject after the invocation completes (same schema as PreInvocation inject steps).
terminationBehavior	string	Optional. Controls the execution flow after injection:
- "force_continue": Forces the loop to continue.
- "terminate": Forces the loop to terminate.
- "" (or omitted): Default behavior.

Example:

Input (stdin): Same as PreInvocation.
Output (stdout):
{
  "injectSteps": [],
  "terminationBehavior": ""
}
Stop
Section titled “Stop”

Fires when the execution loop terminates.

Input fields (stdin):

Field	Type	Description
executionNum	integer	The sequence number of the execution attempt.
terminationReason	string	The reason why the execution is stopping (for example, "model_stop", "max_steps_exceeded", "error").
error	string	Optional. The error message if termination was caused by a system error.
fullyIdle	boolean	Required. true if the agent is completely finished and all background commands or asynchronous tasks have completed. false if active background tasks are still running.
(Common fields)		Includes conversationId, workspacePaths, transcriptPath, artifactDirectoryPath, modelName.

Output fields (stdout):

Field	Type	Description
decision	string	Required. Set to "continue" to prevent the agent from stopping and re-enter the execution loop. Any other value allows the stop.
reason	string	Optional. If decision is "continue", this message is injected as a system message into the conversation.

Example:

Input (stdin):
{
  "executionNum": 1,
  "terminationReason": "model_stop",
  "error": "",
  "fullyIdle": true,
  "conversationId": "ec33ebf9-0cba-4100-8142-c61503f6c587",
  "workspacePaths": ["/workspace/project"],
  "transcriptPath": "~/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587/.system_generated/logs/transcript.jsonl",
  "artifactDirectoryPath": "~/.gemini/antigravity/brain/ec33ebf9-0cba-4100-8142-c61503f6c587",
  "modelName": "gemini-3.6-flash-medium"
}
Output (stdout):
{
  "decision": "continue",
  "reason": "Not done yet"
}
Previous
Custom subagents
Next
Sidecars
About Google
Google Products
Privacy
Terms