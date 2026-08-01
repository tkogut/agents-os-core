# Sidecars
Source URL: https://antigravity.google/docs/sidecars

Antigravity 2.0
>
Customizations
>
Sidecars
Sidecarslink

Sidecars are background processes that run alongside Antigravity. Antigravity manages the lifecycle of sidecars, automatically launching them and restarting them if they crash or error.
They are useful for persistent background scripts, scheduled recurring tasks, and reacting to events.

Configurationlink

Sidecars are discovered by searching for sidecar.json configuration files. They can be defined in two locations:

Global sidecars: Under ~/.gemini/config/sidecars/
Plugin sidecars: Under ~/.gemini/config/plugins/<pluginName>/sidecars/

Each sidecar has its own directory and the directory name is used as the sidecar’s ID. Sidecars loaded from plugins have the ID <pluginName>/<sidecarName>.

The sidecar’s directory must contain a sidecar.json file and may also contain other helper files like scripts to run. The sidecar’s directory also acts as the current working directory for the sidecar’s command.

Example directory structure

content_copy
~/.gemini/config/sidecars/
├── sidecar1/
│   ├── sidecar.json
│   └── script.py
└── sidecar2/
    └── sidecar.json

~/.gemini/config/plugins/
└── my-plugin/
      └── sidecars/
            └── plugin-sidecar/
                  └── sidecar.json
Config Schema (sidecar.json)link
command (string): Command/executable (e.g., python3 or /bin/bash ). Mutually exclusive with builtin.
builtin (string): Builtin command to execute. Currently supports schedule. Mutually exclusive with command.
args (string[]): Optional. Arguments passed to the command or builtin function.
restart_policy (string): Optional. Restart behavior. One of always, on-failure, or never. Defaults to always.
description (string): Optional. Human-readable description of what the sidecar does.
env (object): Optional. Map of environment variables to set for the sidecar process.
display_name (string): Optional. Display name used in the UI.

One of command or builtin must be set.

Examples:

json
content_copy
{
  "description": "Background worker",
  "command": "python3",
  "args": [
    "worker.py"
  ],
  "restart_policy": "on-failure"
}
json
content_copy
{
  "description": "Hourly agent to triage review requests.",
  "builtin": "schedule",
  "args": [
    "0 * * * *",
    "agentapi",
    "new-conversation",
    "Give me a summary of incoming review requests."
  ]
}
User Configuration (config.json)link

Sidecars are disabled unless explicitly enabled by the user in the global configuration file, located at ~/.gemini/config/config.json.

enabled (boolean): Whether the sidecar is enabled.
projectId (string): Optional. The ID of the project agentapi will create conversations in.

Example:

json
content_copy
{
  "sidecars": {
    "sidecar1": {
      "enabled": true
    },
    "my-plugin/plugin-sidecar": {
      "enabled": true,
      "projectId": "<projectId>"
    }
  }
}
Runtime Datalink

Runtime data produced by sidecars are stored in ~/.gemini/antigravity/sidecar_data/<sidecarId>/.

This includes:

data/: Subdirectory for any persistent data. This path is available via the ANTIGRAVITY_EXECUTABLE_DATA_DIR environment variable.
logs/: Auto-generated timestamped logs from stdout and stderr.
events/: JSON files recorded for agentapi calls.
schedule builtinlink

schedule is a simple builtin scheduler for running recurring commands.

json
content_copy
{
  "builtin": "schedule",
  "args": [
    "* * * * *",
    "<command>",
    "<arg1>",
    "<arg2>"
  ]
}

The first argument is a standard 5-field cron expression. The remaining arguments are the command and arguments to run on the specified schedule.

agentapilink

Sidecars can use the agentapi CLI to programmatically interact with Antigravity. The executable is automatically added to the sidecar’s path and available as agentapi.

agentapi new-conversation <prompt>
Sidecars creating conversations must have a projectId set.
agentapi send-message <conversation_id> <prompt>
Hooks
Permissions