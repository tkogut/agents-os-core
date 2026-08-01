# Getting Started
Source URL: https://antigravity.google/docs/getting-started

Antigravity 2.0
>
Getting Started
Getting Started with Antigravity 2.0link
Downloadlink

Visit antigravity.google/download to download Google Antigravity 2.0.

macOS: macOS versions with Apple security update support. This is typically the current and two previous versions. Min Version 12 (Monterey), X86 is not supported.
Windows: Windows 10 (64 bit)
Linux: glibc >= 2.28, glibcxx >= 3.4.25 (e.g. Ubuntu 20, Debian 10, Fedora 36, RHEL 8)
Installationlink

You may get a notification asking whether you want to “Keep Both” or “Replace” Antigravity, select “Replace.” You will be prompted to re-install the IDE during installation, should you choose to. If you do not install it now and would like to re-download it later, you can do so here.

Creating a Projectlink

Agents work within Projects, which define the boundaries of the folders and repositories they can access.

Click the folder with a “+” icon in the left sidebar.
Click on “New Project”.
Click Add Folder to associate one or more local folders or Git repositories. Adding multiple folders provides your agent with full cross-repository context.
Click Create.
(Optional) Configure your Project’s settings. Each Project maintains its own isolated settings and security policies that the agent respects.
Starting an Agentlink

Once your Project is created, you can spawn an agent to start working on tasks.

Type your goal or instruction in the chat input (e.g., “Help me add a new feature”) and press Enter.
Choose a Mode in the setup modal to boot up your agent:
Local Mode: The agent operates directly in your active folders.
New Worktree Mode: The agent operates in an isolated Git worktree.
Basic Navigationlink
Action	macOS	Windows / Linux
Open Conversation Picker	⌘K	Ctrl + K
Open File Search	⌘P	Ctrl + P
Focus Input	⌘L	Ctrl + L
New Conversation	⌘N	Ctrl + N
Next/Previous Conversation	⌥ Up / Down	Alt + Up / Down
Slash Commandslink
/goal: Run until the specified task is completely finished, not asking for intermediate input from the user.
/grill-me: Before starting to implement, ask questions back to align on the specific details of the plan.
/schedule: Run an instruction as a one-time timer in the future or on some recurring schedule (via Scheduled Tasks)
/browser: We heard the feedback that the agents were still not capable enough to determine exactly when to be using the browser. So for now, we’ve made it such that an explicit slash command controls these behaviors. When used, the agent diligently uses the browser primitives. This requires both Google Chrome and the user to provide permission in Google Chrome to start a debugging session.
Overview
Build with Google