# Get Started
Source URL: https://antigravity.google/docs/getting-started

Get Started
Getting started
Markdown
Getting started
Section titled “Getting started”

Welcome to Google Antigravity! Follow the instructions in this guide to get started on your preferred surface.

Antigravity 2.0
Antigravity CLI
Antigravity IDE
Antigravity 2.0
Download Antigravity 2.0
Section titled “Download Antigravity 2.0”

Visit antigravity.google/download to download Google Antigravity 2.0. Select your operating system from the following table:

Platform	Download
macOS	
Download for Apple Silicon
Download for Intel

Requirements: macOS versions with Apple security update support. This is typically the current and two previous versions. Minimum version 12 (Monterey); x86 is not supported.


Windows	
Download for x64
Download for ARM64

Requirements: Windows 10 (64-bit)


Linux	
Download for x64
Download for ARM64

Requirements: glibc >= 2.28, glibcxx >= 3.4.25 (for example, Ubuntu 20, Debian 10, Fedora 36, RHEL 8)


Googlebook	
Get it on Google Play

Requirements: Googlebook OS (pre-installed on Googlebooks; update or reinstall through the Google Play Store)

Installation
Section titled “Installation”

If you get a notification asking whether you want to “Keep Both” or “Replace” Antigravity, select Replace. You are prompted to reinstall the IDE during installation if you choose to do so. If you don’t install it now and want to download it later, visit the download page.

When you launch Antigravity 2.0 and sign in, select your personal Google Account or choose Business account to connect with Gemini Enterprise.

Creating a project
Section titled “Creating a project”

Agents work within projects, which define the boundaries of the folders and repositories they can access:

Click the folder with a ”+” icon in the left sidebar.
Click New Project.
Click Add Folder to associate one or more local folders or Git repositories. Adding multiple folders provides your agent with full cross-repository context.
Click Create.
(Optional) Configure your project’s settings. Each project maintains its own isolated settings and security policies that the agent respects.
Starting an agent
Section titled “Starting an agent”

Once your project is created, you can spawn an agent to start working on tasks:

Type your goal or instruction in the chat input (for example, “Help me add a new feature”) and press ENTER.
Choose a Mode in the setup modal to boot up your agent:
Local mode: The agent operates directly in your active folders.
New worktree mode: The agent operates in an isolated Git worktree.
Basic navigation
Section titled “Basic navigation”

Use the following keyboard shortcuts to navigate Antigravity 2.0:

Action	macOS	Windows / Linux
Open conversation picker	⌘K	CTRL + K
Open file search	⌘P	CTRL + P
Focus input	⌘L	CTRL + L
New conversation	⌘N	CTRL + N
Next/previous conversation	⌥ UP / DOWN	ALT + UP / DOWN
Slash commands
Section titled “Slash commands”

Use the following slash commands to control agent execution:

Slash command	Description
/goal	Run until the specified task is completely finished, without asking for intermediate input.
/grill-me	Ask clarifying questions to align on the specific details of the plan before starting implementation.
/schedule	Run an instruction as a one-time timer in the future or on a recurring schedule using scheduled tasks.
/browser	Control browser debugging behaviors in Google Chrome.
/plugin	Manage installed Marketplace plugins or create and configure custom plugin bundles.
Previous
Home
Next
Overview
About Google
Google Products
Privacy
Terms