# Artifact Review
Source URL: https://antigravity.google/docs/artifact-review

Antigravity 2.0
>
Settings
>
Artifact Review
Artifact Reviewlink

When starting a new Agent conversation, you can choose between two primary execution modes that determine how changes are proposed and reviewed:

Planning Mode: The agent plans thoroughly before executing tasks. In this mode, the agent organizes its work in task groups, produces structured implementation plans called Artifacts, and thoroughly researches the codebase for optimal quality.
Fast Mode: The agent executes tasks directly without a dedicated planning phase. Use this for simple, highly localized tasks that can be completed quickly, such as variable renaming, running a specific bash command, or small refactors.

When working in Planning Mode, the Artifact Review Policy controls how you interact with and approve these plans before changes are made to your codebase.

Artifact Review Policylink

You can customize the review workflow in the Agent tab of the Settings pane. Choose between two policies:

1. Request Review (Recommended)link

The agent always halts and requests your explicit approval before proceeding with proposed changes.

When the agent generates an implementation plan or code diff, it will pause execution and notify you.
This allows you to thoroughly review the proposed changes, add inline comments, and verify the plan in your workspace.
Once you are satisfied, you can approve the plan to let the agent proceed.

2. Always Proceedlink

The agent never halts for manual review and immediately proceeds with executing its plans.

When the agent decides to request a review, it will immediately bypass the pause and continue with the implementation.
Use this if you want a fully autonomous workflow and do not need to manually verify plans before code is modified.

Agent Settings
MCP