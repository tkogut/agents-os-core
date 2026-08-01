# Getting Started
Source URL: https://antigravity.google/docs/cli/getting-started

Antigravity CLI
>
Getting Started
Getting Started with Antigravity CLIlink

Welcome to Antigravity CLI! This guide provides a direct, high-level developer roadmap to install the client, launch the Terminal User Interface (TUI), and begin collaborating with autonomous agents.

Roadmap checklistlink

Complete the following sequential steps to launch your first session:

Install the client (fast path)

Run the appropriate fast-path command for your operating system:

macOS / Linux:

bash
content_copy
curl -fsSL https://antigravity.google/cli/install.sh | bash

Windows (PowerShell):

powershell
content_copy
irm https://antigravity.google/cli/install.ps1 | iex

Windows (CMD):

cmd
content_copy
curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd

By default, the installer registers the agy binary to your platform-specific directory:

macOS / Linux: ~/.local/bin/agy
Windows: C:\Users\<Username>\AppData\Local\agy\bin (where <Username> represents your active Windows profile name).
info
Advanced Setup: For detailed enterprise credentials configuration, secure keyring auth permissions, proxy setups, or troubleshooting installation issues, consult the Installation & Auth Guide.

Launch the TUI inside a project

Open a fresh terminal window, navigate to your target project codebase directory, and execute the launcher command:

bash
content_copy
agy

Complete the first-launch setup

On your very first launch, the TUI walks you through a brief interactive setup:

Color Scheme: Select your preferred visual theme (Solarized, Dark, Solarized Light, or standard Terminal colors).
Rendering Mode: Choose Alt-Screen mode (alternate buffer with full-screen scrolling) or Inline mode (sequential stream integrated with your terminal’s history).
Workspace Trust: Confirm that you trust the repository directory. Once confirmed, the agent indexes the files and stands ready.

Run your first agent task

Type the following instruction in the prompt box at the bottom of your TUI screen and press Enter:

text
content_copy
Write a simple python script to fetch web page text

The agent reads the workspace, reasons about the task, and proposes a plan. For a detailed step-by-step tutorial on reviewing code and running test commands inside the TUI, follow the Tutorial Guide.

Related resourceslink

Optimize your local environment configurations and master advanced collaboration tools:

Best Practices: Master verification loops, planning phases, rule files, and session checkpoints.
Troubleshooting: Resolve common path, keyring, or SSH forwarding errors.
CLI Reference: Dense reference sheets cataloging all slash commands, shortcuts, and JSON keys.
Overview
Installation & Auth