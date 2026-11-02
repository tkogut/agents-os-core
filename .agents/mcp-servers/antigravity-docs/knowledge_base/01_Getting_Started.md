# Getting Started
Source URL: https://antigravity.google/docs/getting-started

Get started2-0Antigravity AppGet StartedGet started Antigravity App Get StartedAntigravity App
Get Started
Quickstart
Markdown
Get started
Section titled “Get started”

Welcome to Google Antigravity! Follow the instructions in this guide to get started on your preferred surface.

Choose your surface
Section titled “Choose your surface”
v2.5+
Antigravity App
Desktop application
agy · v1.2+
Antigravity CLI
Terminal client
5 IDEs
For IDEs
Editor extensions
Python
Antigravity SDK
Programmatic runtime
Download and install
Section titled “Download and install”
Antigravity App
Antigravity CLI
For IDEs
Antigravity SDK

Download the Google Antigravity installer for your operating system (or view all builds at antigravity.google/download):

macOS
macOS 12 (Monterey) or later (Apple Silicon or 64-bit Intel)
Download for Apple Silicon
Download for Intel

Open the downloaded Antigravity.dmg disk image and drag Antigravity into your Applications folder. If you are upgrading an existing installation, select Replace when prompted instead of Keep Both.

Windows
Windows 10 (64-bit) or Windows 11
Download for x64
Download for ARM64

Run the downloaded .exe installer and follow the guided setup wizard.

Linux
glibc >= 2.28, glibcxx >= 3.4.25 (Ubuntu 20+, Debian 10+, Fedora 36+, RHEL 8+)
Download for x64
Download for ARM64

Extract the archive with tar -xzf Antigravity.tar.gz and launch ./Antigravity.

Googlebook
Googlebook OS (pre-installed on Googlebooks; update or reinstall via Google Play)
Get it on Google Play

Google Antigravity comes pre-installed on Googlebooks. Open Google Play to install updates or reinstall the application.

Launch Google Antigravity from your applications launcher or menu.

Start a project
Section titled “Start a project”
Antigravity App
Antigravity CLI
For IDEs
Antigravity SDK

Agents operate within Projects, which define the repository boundaries, file scopes, and security permissions for your workspaces.

Click the New Project icon (folder with a plus sign) in the left sidebar.
Click Add Folder to select one or more local Git repositories or working directories.
Click Create.
Type your instruction in the prompt input (for example: Add unit tests for the authentication handlers) and press ENTER.
Choose a Mode in the setup modal to boot up your agent:
Local mode: The agent operates directly in your active folders.
New worktree mode: The agent operates in an isolated Git worktree.
Shortcuts and commands
Section titled “Shortcuts and commands”
Antigravity App
Antigravity CLI
For IDEs
Antigravity SDK
Navigation shortcuts
Section titled “Navigation shortcuts”
Action	macOS	Windows / Linux	Description
Conversation picker	⌘K	CTRL + K	Search past conversations by title or full text and switch to one
File search	⌘P	CTRL + P	Search files in the current project by name and open one
Commands	⌘⇧P	CTRL + SHIFT + P	Search and run app commands
Find	⌘F	CTRL + F	Find text in the current conversation or open file
Focus input	⌘L	CTRL + L	Jump cursor focus directly into the message box
New conversation	⌘N	CTRL + N	Start a fresh autonomous agent session
Previous or next conversation	⌥ UP / DOWN	ALT + UP / DOWN	Move to the previous or next conversation in the sidebar

For more about searching conversations, files, and commands, see Search and command palette.

Core slash commands
Section titled “Core slash commands”
Command	Description
/goal	Runs the task autonomously until completion without pausing for intermediate input.
/grill-me	Prompts the agent to interview you about requirements before beginning implementation.
/schedule	Runs an instruction as a one-time delayed task or recurring cron schedule.
/browser	Initiates browser debugging and research actions in Google Chrome.
/plugin	Manages installed Marketplace plugins or creates and configures custom plugin bundles.
Additional resources
Section titled “Additional resources”
Antigravity App
Antigravity CLI
For IDEs
Antigravity SDK
CORE
Features guide

Autonomous subagents, visual artifacts, and tool integrations.

SECURITY
Permissions

Local security boundaries, sandboxing, and execution gates.

CONFIG
Settings

Configuration options for projects, models, and agent behavior.

MODELS
Choose a model

Reasoning effort levels, thinking budgets, and supported frontier models.

Previous
Overview
Next
Authenticate
About Google
Google Products
Privacy
Terms