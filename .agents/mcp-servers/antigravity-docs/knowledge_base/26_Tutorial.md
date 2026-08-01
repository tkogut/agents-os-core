# Tutorial
Source URL: https://antigravity.google/docs/cli/tutorial

Antigravity CLI
>
Tutorial
Antigravity CLI Tutoriallink

Learn how to launch Antigravity CLI, collaborate with an autonomous local agent, review generated files, and execute terminal test commands.

Overviewlink

This guide walks you through a rapid onboarding exercise. You will direct an autonomous agent to create a Python utility script, review the changes, and verify its execution.

Step-by-steplink

Create a clean project directory and launch the Antigravity TUI

bash
content_copy
mkdir agy-demo && cd agy-demo
agy
info
First Launch: If running agy for the first time, follow the terminal instructions to complete silent authentication. See Installation & Auth for troubleshooting details.

Prompt the agent to generate a Python scraping script

Type the following instruction in the prompt box at the bottom of your screen and press Enter:

text
content_copy
Write a simple python script to fetch web page text

The agent reads the workspace, determines that no files exist, and formulates a plan to create a script. You will see real-time updates as the agent performs reasoning and schedules actions.

Open the artifact review screen to inspect the proposed code

Once the agent finishes generating the file, a notification appears. Press ctrl+r to enter the Artifact Review screen.

Navigate to the newly created main.py using ↑/↓.
Review the complete file content and diff.
Press y to approve the creation of main.py.
Press Esc to close the review panel and return to the primary prompt.

Execute a test command with the agent to verify the output

Direct the agent to run the Python script to verify its behavior. Type the following command in the prompt box and press Enter:

text
content_copy
Run the python script and show me the output

The agent proposes to run python3 main.py. Press y to confirm and execute the command. The agent runs the script locally and streams the standard output directly into your terminal screen.

Exit the Antigravity session

Once you complete your task, press ctrl+d (or type /exit) in the prompt box to close the TUI and restore your original shell session.

Next stepslink

Now that you have executed your first agent-assisted workflow, learn how to configure the CLI and master core concepts:

Installation & Auth: Detailed instructions on installing agy and setting up SSH profiles.
Prompting & Interaction: Best practices for multiline inputs, pasting media files, and active interrupt controls.
Reviewing Artifacts: Deep dive into the “Trust through Transparency” architectural pattern.
Installation & Auth
Using AGY CLI