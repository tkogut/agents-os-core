# Artifact review
Source URL: https://antigravity.google/docs/artifact-review

Features
Learn
Settings
Artifact review
Markdown
AVAILABLE ON:
Antigravity 2.0
Artifact review
Section titled “Artifact review”

When starting a new agent conversation, you can choose between two primary execution modes that determine how changes are proposed and reviewed:

Planning mode: The agent plans thoroughly before executing tasks. In this mode, the agent organizes its work in task groups, produces structured implementation plans called artifacts, and thoroughly researches the codebase for optimal quality.
Fast mode: The agent executes tasks directly without a dedicated planning phase. Use this for simple, highly localized tasks that can be completed quickly, such as variable renaming, running a specific Bash command, or small refactors.

When working in Planning mode, the artifact review policy controls how you interact with and approve these plans before changes are made to your codebase.

Artifact review policy
Section titled “Artifact review policy”

You can customize the review workflow in the Agent tab of the Settings pane. Choose between two policies:

Request review (recommended)
Section titled “Request review (recommended)”

The agent always halts and requests your explicit approval before proceeding with proposed changes:

When the agent generates an implementation plan or code diff, it pauses execution and notifies you.
This allows you to thoroughly review the proposed changes, add inline comments, and verify the plan in your workspace.
Once you’re satisfied, you can approve the plan to let the agent proceed.

Always proceed
Section titled “Always proceed”

The agent never halts for manual review and immediately proceeds with executing its plans:

When the agent decides to request a review, it immediately bypasses the pause and continues with the implementation.
Use this if you want a fully autonomous workflow and don’t need to manually verify plans before code is modified.

Previous
Agent settings
Next
Vim editor mode
About Google
Google Products
Privacy
Terms