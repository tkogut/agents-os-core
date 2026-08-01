# Rules
Source URL: https://antigravity.google/docs/ide/rules

Antigravity IDE
>
Customizations
>
Rules
Ruleslink

Rules are manually defined constraints for the Agent to follow, at both the local and global levels. Rules allow users to guide the agent to follow behaviors particular to their own use cases and style.

To get started with Rules:

Open the Customizations panel via the “…” dropdown at the top of the editor’s agent panel.
Navigate to the Rules panel.
Click + Global to create new Global Rules, or + Workspace to create new Workspace-specific rules.

A Rule itself is simply a Markdown file, where you can input the constraints to guide the Agent to your tasks, stack, and style.

Rules files are limited to 12,000 characters each.

Global Ruleslink

Global rules live in ~/.gemini/GEMINI.md and are applied across all workspaces.

Workspace Ruleslink

Workspace rules live in the .agents/rules folder of your workspace or git root.

At the rule level you can define how a rule should be activated:

Manual: The rule is manually activated via at mention in Agent’s input box.
Always On: The rule is always applied.
Model Decision: Based on a natural language description of the rule, the model decides whether to apply the rule.
Glob: Based on the glob pattern you define (e.g., .js, src/**/.ts), the rule will be applied to all files that match the pattern.

Note: Antigravity now defaults to .agents/rules, but still maintains backward support for .agent/rules.

@ Mentionslink

You can reference other files using @filename in a Rules file. If filename is a relative path, it will be interpreted relative to the location of the Rules file. If filename is an absolute path, it will be resolved as a true absolute path, otherwise it will be resolved relative to the repository. For example, @/path/to/file.md will first attempt to be resolved to /path/to/file.md, and if that file does not exist, it will be resolved to workspace/path/to/file.md.

Skills
Workflows