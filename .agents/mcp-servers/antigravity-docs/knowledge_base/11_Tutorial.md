# Tutorial
Source URL: https://antigravity.google/docs/cli/tutorial

Get Started
CLI
Tutorial
Markdown
Antigravity CLI tutorial
Section titled “Antigravity CLI tutorial”

Learn how to launch Antigravity CLI, collaborate with an autonomous local agent, review generated files, and execute terminal test commands.

Overview
Section titled “Overview”

This guide walks you through a rapid onboarding exercise. In this exercise, you direct an autonomous agent to create a Python utility script, review the changes, and verify its execution.

Step-by-step
Section titled “Step-by-step”

Follow these steps to create and verify a Python script with the agent:

Create a clean project directory and launch the Antigravity TUI:

mkdir agy-demo && cd agy-demo
agy

Note

First launch: If you’re running agy for the first time, follow the terminal instructions to complete silent authentication. Refer to Installation and auth for troubleshooting details.

Prompt the agent to generate a Python scraping script:

Type the following instruction in the prompt box at the bottom of your screen and press ENTER:

Write a simple python script to fetch web page text

The agent reads the workspace, determines that no files exist, and formulates a plan to create a script. You receive real-time updates as the agent performs reasoning and schedules actions.

Open the artifact review screen to inspect the proposed code:

Once the agent finishes generating the file, a notification appears. Press CTRL + R to enter the Artifact Review screen and complete the review:

Navigate to the newly created main.py using ↑/↓.
Review the complete file content and diff.
Press Y to approve the creation of main.py.
Press ESC to close the review panel and return to the primary prompt.

Execute a test command with the agent to verify the output:

Direct the agent to run the Python script to verify its behavior. Type the following command in the prompt box and press ENTER:

Run the python script and show me the output

The agent proposes to run python3 main.py. Press Y to confirm and execute the command. The agent runs the script locally and streams the standard output directly into your terminal screen.

Exit the Antigravity session:

Once you complete your task, press CTRL + D (or type /exit) in the prompt box to close the TUI and restore your original shell session.

Next steps
Section titled “Next steps”

Now that you’ve executed your first agent-assisted workflow, learn how to configure the CLI and master core concepts:

Installation and auth: Detailed instructions on installing agy and setting up SSH profiles.
Prompting and interaction: Best practices for multiline inputs, pasting media files, and active interrupt controls.
Reviewing artifacts: Deep dive into the artifact review workflow.
Previous
Installation and auth
Next
Using Antigravity CLI
About Google
Google Products
Privacy
Terms