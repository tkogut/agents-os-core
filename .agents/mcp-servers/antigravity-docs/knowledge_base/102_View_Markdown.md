# View Markdown
Source URL: https://antigravity.google/docs/getting-started.md

# Get started

Welcome to Google Antigravity! Follow the instructions in this guide to get started on your preferred surface.

## Choose your surface

## Download and install

### Antigravity App

1.  Download the Google Antigravity installer for your operating system (or view all builds at [antigravity.google/download](/download)):
    
    macOSmacOS 12 (Monterey) or later (Apple Silicon or 64-bit Intel)
    
    [Download for Apple Silicon](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.28.2-5937220255875072/darwin-arm/Antigravity.dmg)[Download for Intel](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.28.2-5937220255875072/darwin-x64/Antigravity.dmg)
    
    Open the downloaded `Antigravity.dmg` disk image and drag **Antigravity** into your **Applications** folder. If you are upgrading an existing installation, select **Replace** when prompted instead of **Keep Both**.
    
    WindowsWindows 10 (64-bit) or Windows 11
    
    [Download for x64](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.28.2-5937220255875072/windows-x64/Antigravity-x64.exe)[Download for ARM64](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.28.2-5937220255875072/windows-arm/Antigravity-arm64.exe)
    
    Run the downloaded `.exe` installer and follow the guided setup wizard.
    
    Linuxglibc >= 2.28, glibcxx >= 3.4.25 (Ubuntu 20+, Debian 10+, Fedora 36+, RHEL 8+)
    
    [Download for x64](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.28.2-5937220255875072/linux-x64/Antigravity.tar.gz)[Download for ARM64](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.28.2-5937220255875072/linux-arm/Antigravity.tar.gz)
    
    Extract the archive with `tar -xzf Antigravity.tar.gz` and launch `./Antigravity`.
    
    GooglebookGooglebook OS (pre-installed on Googlebooks; update or reinstall via Google Play)
    
    [Get it on Google Play](https://play.google.com/store/apps/details?id=com.google.android.apps.antigravity)
    
    Google Antigravity comes pre-installed on Googlebooks. Open Google Play to install updates or reinstall the application.
    
2.  Launch Google Antigravity from your applications launcher or menu.

### Antigravity CLI

1.  Install the Antigravity CLI (`agy`) binary using the automated installer for your operating system:
    
    **macOS / Linux / Googlebook:**
    
    ```bash
    curl -fsSL https://antigravity.google/cli/install.sh | bash
    ```
    
    Default binary location: `~/.local/bin/agy`
    
    **Windows (PowerShell):**
    
    ```powershell
    irm https://antigravity.google/cli/install.ps1 | iex
    ```
    
    Default binary location: `C:\Users\<username>\AppData\Local\agy\bin`
    
    **Windows (CMD):**
    
    ```cmd
    curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
    
    Default binary location: `C:\Users\<username>\AppData\Local\agy\bin`
    
2.  Open a terminal window and verify the installation:
    
    ```bash
    agy --version
    ```
    
3.  Complete the interactive terminal configuration on initial launch:
    
    *   **Color scheme**: Select your visual preference (Dark, Solarized Dark, Solarized Light, or terminal default).
    *   **Rendering mode**: Choose **Alt-Screen** mode (full-screen buffer) or **Inline** mode (sequential output in terminal history).
    *   **Workspace trust**: Confirm that you trust the repository directory before the agent begins file indexing.

Note

For authentication options or enterprise configurations, consult the **[Authenticate guide](/docs/install?tab=cli)** and **[Enterprise guide](/docs/enterprise)**.

### For IDEs

1.  Install the official Google Antigravity extension for your preferred editor, or download the standalone **Antigravity IDE**:
    
    **VS Code:**
    
    [Install from VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=Google.google-antigravity)
    
    **Requirements:** Visual Studio Code 1.90 or later on macOS, Linux, or Windows.
    
    Open the Extensions sidebar (Cmd+Shift+X on macOS or Ctrl+Shift+X on Windows/Linux), search for **Google Antigravity**, and click **Install**. See the [VS Code extension guide](/docs/ide/extensions/vscode).
    
    **JetBrains:**
    
    **Requirements:** Any IntelliJ-based IDE (IntelliJ IDEA, PyCharm, WebStorm, GoLand, CLion, Rider) version 2026.2.1 or later.
    
    Open **JetBrains AI** > **Settings** > **Agents**, search for **Antigravity**, and click **Install**. See the [IntelliJ-based IDEs guide](/docs/ide/extensions/jetbrains).
    
    **Visual Studio:**
    
    [Download from Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=Google.GoogleAntigravity)
    
    **Requirements:** Visual Studio 2026 (version 17.8 or higher) on Windows 10/11.
    
    Navigate to **Extensions** > **Manage Extensions**, search for **Google Antigravity**, click **Download**, and restart Visual Studio to complete the VSIX installation. See the [Visual Studio guide](/docs/ide/extensions/visual-studio).
    
    **Zed:**
    
    **Requirements:** Zed version 0.140.0 or later on macOS or Linux.
    
    Open the Command Palette (Cmd+Shift+P / Ctrl+Shift+P), run `agent: open settings`, and navigate to **External Agents** > **Add** > **Install from Registry** to install **Antigravity**. See the [Zed guide](/docs/ide/extensions/zed).
    
    **Xcode:**
    
    **Requirements:** Xcode 27 beta 6 or later on macOS.
    
    Open **Xcode** > **Settings** (Cmd+,), select the **Intelligence** panel, and click **Get** next to **Antigravity**. See the [Xcode guide](/docs/ide/extensions/xcode).
    
    **Eclipse:**
    
    [Install from Eclipse Marketplace](https://marketplace.eclipse.org/content/google-antigravity)
    
    **Requirements:** Eclipse 2026-06 or later on macOS, Linux, or Windows (Public Preview).
    
    Select **Help** > **Eclipse Marketplace…**, search for **Google Antigravity**, click **Install**, and restart Eclipse when prompted. Check out the [Eclipse guide](/docs/ide/extensions/eclipse).
    
    **Antigravity IDE:**
    
    [Download Antigravity IDE](/download#antigravity-ide)
    
    **Requirements:** macOS 12 (Monterey)+, Windows 10 (64-bit)+, or Linux / Googlebook (glibc >= 2.28, glibcxx >= 3.4.25).
    
    Download the standalone **Antigravity IDE** installer for your platform from [antigravity.google/download](/download). When a new version is available, Antigravity IDE downloads it in the background and prompts you to click **Restart to Update**:
    
    ![Restart to update notification in Antigravity IDE](/assets/image/docs/restart-to-update.png)
    
    **Basic navigation (Editor & Agent Manager):** Open the Agent Manager from the editor using the button on the top bar or Cmd+E (Ctrl+E on Windows/Linux):
    
    ![Open the Agent Manager from the Antigravity IDE editor](/assets/image/docs/editor-open-agent-manager.png)
    
    From the Agent Manager, open the editor from any workspace using **Focus Editor** in the workspace dropdown menu, the **Open Editor** buttons, or Cmd+E (Ctrl+E on Windows/Linux):
    
    ![Open the editor from the Agent Manager in Antigravity IDE](/assets/image/docs/agent-manager-open-editor.png)
    
2.  Sign in with your personal Google Account or **Gemini Enterprise** credentials (Enterprise support is available in IDE extensions—GA in VS Code and Visual Studio, and in **Preview** for JetBrains, Zed, Xcode, and Eclipse) when prompted in the Antigravity panel or settings.

### Antigravity SDK

1.  Install the official Antigravity Python package inside a Python 3.10+ virtual environment:
    
    ```bash
    pip install google-antigravity
    ```
    
    If you use Poetry or uv for package management:
    
    ```bash
    # Poetry
    poetry add google-antigravity
    
    # uv
    uv add google-antigravity
    ```
    
2.  Authenticate and configure your environment:
    
    Configure your API credentials in your environment before initializing the agent harness:
    
    ```bash
    export GEMINI_API_KEY="your_api_key_here"
    ```
    
    Note
    
    **Enterprise & Google Cloud**: To authenticate using Gemini Enterprise or Vertex AI, set your project configuration:
    
    ```bash
    export GOOGLE_GENAI_USE_VERTEXAI=True
    export GOOGLE_CLOUD_PROJECT="your-gcp-project"
    export GOOGLE_CLOUD_LOCATION="us-central1"
    gcloud auth application-default login
    ```

## Start a project

### Antigravity App

Agents operate within **Projects**, which define the repository boundaries, file scopes, and security permissions for your workspaces.

1.  Click the **New Project** icon (folder with a plus sign) in the left sidebar.
2.  Click **Add Folder** to select one or more local Git repositories or working directories.
3.  Click **Create**.
4.  Type your instruction in the prompt input (for example: `Add unit tests for the authentication handlers`) and press Enter.
5.  Choose a **Mode** in the setup modal to boot up your agent:
    *   **Local mode**: The agent operates directly in your active folders.
    *   **New worktree mode**: The agent operates in an isolated Git worktree.

### Antigravity CLI

Navigate to any codebase directory in your terminal and start a session:

1.  Create or navigate to a project directory and launch the TUI:
    
    ```bash
    mkdir agy-demo && cd agy-demo
    agy
    ```
    
2.  Enter your first task prompt and press Enter:
    
    ```text
    Write a simple python script to fetch web page text
    ```
    
    The agent indexes the workspace, develops an implementation plan, and displays proposed changes for your review.
    
3.  Open the **Artifact Review** screen to inspect the proposed code:
    
    Press Ctrl + R when notified to review generated artifacts:
    
    *   Navigate to the newly created `main.py` using ↑/↓, or press Tab from the main prompt to inspect inline diffs.
    *   Press Y to approve the creation of `main.py`.
    *   Press Esc to close the review panel and return to the primary prompt.
4.  Execute a test command with the agent to verify the output:
    
    ```text
    Run the python script and show me the output
    ```
    
    Press Y to confirm and execute `python3 main.py`. Once finished, press Ctrl + D (or type `/exit`) to close the TUI session.

### For IDEs

1.  Open your workspace folder, repository, or solution in your preferred editor.
2.  Open the Antigravity panel or agent view in your IDE (for example, click the Antigravity icon in the VS Code Activity Bar, press Ctrl+, Ctrl+A in Visual Studio, select **Antigravity** > **Toggle Chat** in Eclipse, or select Antigravity in JetBrains AI, Zed External Agents, or Xcode Intelligence).
3.  Enter a task prompt in the conversation panel to start an agent session that shares context and [customizations](/docs/skills) with the rest of the Antigravity ecosystem.
4.  Inspect interactive implementation plans, review granular inline diffs, and execute multi-step engineering tasks directly inside your editor.

### Antigravity SDK

1.  Create a file named `hello_agent.py` to instantiate and run an autonomous agent:
    
    ```python
    import asyncio
    from google.antigravity import Agent, LocalAgentConfig
    
    async def main():
        # Initialize the local agent harness
        config = LocalAgentConfig()
        async with Agent(config) as agent:
            response = await agent.chat("What files are in the current directory and what is their purpose?")
            print(await response.text())
    
    if __name__ == "__main__":
        asyncio.run(main())
    ```
    
2.  Execute the agent script in your terminal:
    
    ```bash
    python hello_agent.py
    ```
    
3.  Configure declarative tool policies:
    
    Use `LocalAgentConfig` and `google.antigravity.hooks.policy` to define explicit tool execution rules:
    
    ```python
    from google.antigravity import LocalAgentConfig
    from google.antigravity.hooks.policy import allow, deny
    
    config = LocalAgentConfig(
        policies=[
            deny("*"),
            allow("view_file"),
        ]
    )
    ```

## Shortcuts and commands

### Antigravity App

#### Navigation shortcuts

| Action | macOS | Windows / Linux | Description |
| :-- | :-- | :-- | :-- |
| **Conversation picker** | ⌘K | Ctrl + K | Search past conversations by title or full text and switch to one |
| **File search** | ⌘P | Ctrl + P | Search files in the current project by name and open one |
| **Commands** | ⌘⇧P | Ctrl + Shift + P | Search and run app commands |
| **Find** | ⌘F | Ctrl + F | Find text in the current conversation or open file |
| **Focus input** | ⌘L | Ctrl + L | Jump cursor focus directly into the message box |
| **New conversation** | ⌘N | Ctrl + N | Start a fresh autonomous agent session |
| **Previous or next conversation** | ⌥ Up / Down | Alt + Up / Down | Move to the previous or next conversation in the sidebar |

For more about searching conversations, files, and commands, see [Search and command palette](/docs/search).

#### Core slash commands

| Command | Description |
| :-- | :-- |
| [`/goal`](/docs/commands/goal) | Runs the task autonomously until completion without pausing for intermediate input. |
| [`/grill-me`](/docs/commands/grill-me) | Prompts the agent to interview you about requirements before beginning implementation. |
| [`/schedule`](/docs/commands/schedule) | Runs an instruction as a one-time delayed task or recurring cron schedule. |
| [`/browser`](/docs/commands/browser) | Initiates browser debugging and research actions in Google Chrome. |
| [`/plugin`](/docs/plugins) | Manages installed [Marketplace](/docs/marketplace) plugins or creates and configures custom plugin bundles. |

### Antigravity CLI

#### Common CLI commands

| Command | Description |
| :-- | :-- |
| `agy` | Launches the interactive TUI in the current directory. |
| `agy "prompt"` | Launches a session with an initial prompt. |
| `/agents` | Switches between active background subagents. |
| `/statusline` | Toggles or configures the terminal status line display. |
| `/usage` | Displays current model credit consumption and quota limits. |
| `/exit` | Closes the TUI and restores your original shell session. |

#### Keyboard shortcuts

| Shortcut | Action |
| :-- | :-- |
| Ctrl + R | Open the **Artifact Review** screen to inspect plans and diffs |
| Tab | Inspect file diffs and tool execution details |
| Ctrl + C | Interrupt current agent generation |
| Ctrl + O | Expand or collapse active tool execution pill |
| Ctrl + D | Exit the active Antigravity CLI session |
| Esc | Exit diff inspector or close active overlay |

### For IDEs

#### Editor commands and shortcuts

| IDE | Shortcut / Command | Action |
| :-- | :-- | :-- |
| **VS Code** | ⌘⇧X / Ctrl + Shift + X | Open Extensions sidebar to install or manage **Google Antigravity** |
| **Visual Studio** | Ctrl+, Ctrl+A | Open the Antigravity tool window |
| **Zed** | ⌘⇧P / Ctrl + Shift + P → `agent: open settings` | Open Agent settings to configure **External Agents** |
| **JetBrains** | **JetBrains AI** > **Settings** > **Agents** | Install or configure the **Antigravity** agent |
| **Xcode** | ⌘, → **Intelligence** | Manage and authenticate **Antigravity** in Xcode Settings |
| **Eclipse** | ⌘⌥E / Ctrl + Alt + K | Toggle the **Antigravity** chat view |

#### Authentication configuration

| Auth type (`auth.type`) | Account tier | Description |
| :-- | :-- | :-- |
| `"oauth-personal"` | Individual Google Accounts | Authenticates personal Free, Pro, and Ultra plans. |
| `"oauth-business"` | Gemini Enterprise (Preview) | Authenticates corporate identity with `gcp.project` and `gcp.location`. |
| `"gemini-api-key"` | Gemini API | Authenticates using a Gemini API key. |
| `"agent-platform"` | Agent Platform (Preview) | Authenticates with Gemini Enterprise Agent Platform via API key or ADC. |

### Antigravity SDK

#### Common SDK methods and configuration

| Method / Command | Description |
| :-- | :-- |
| `await agent.chat(prompt)` | Sends a user prompt to the agent and returns the turn response. |
| `LocalAgentConfig(policies=...)` | Configures declarative tool execution policies (`allow`, `deny`, `ask_user`). |
| `LocalAgentConfig(system_instructions=...)` | Customizes the agent persona and system instructions. |
| `export GEMINI_API_KEY="..."` | Sets Gemini API credentials in the environment. |

## Additional resources

### Antigravity App

[

Core

Features guide

Autonomous subagents, visual artifacts, and tool integrations.

](/docs/features/)[

Security

Permissions

Local security boundaries, sandboxing, and execution gates.

](/docs/permissions/)[

Config

Settings

Configuration options for projects, models, and agent behavior.

](/docs/settings/)[

Models

Choose a model

Reasoning effort levels, thinking budgets, and supported frontier models.

](/docs/models/)

### Antigravity CLI

[

Workflow

Best practices

Verification loops, rule files, and session checkpoints.

](/docs/cli/best-practices/)[

Debug

CLI troubleshooting

Path resolution, keyring authentication, and SSH forwarding.

](/docs/cli/troubleshooting/)[

Reference

CLI reference

Catalog of commands, keybindings, and JSON schemas.

](/docs/cli/reference/)[

Navigation

Vim editor mode

Modal navigation and keybindings within the terminal user interface.

](/docs/cli/vim-editor-mode/)

### For IDEs

[

Extensions

IDE extensions overview

Supported editors, unified authentication, and enterprise licensing across IDEs.

](/docs/ide/extensions/)[

VS Code

Visual Studio Code

Install from the VS Code Marketplace and configure your local workspace.

](/docs/ide/extensions/vscode/)[

JetBrains

IntelliJ-based IDEs

Set up the Antigravity agent in IntelliJ IDEA, PyCharm, WebStorm, GoLand, and Rider.

](/docs/ide/extensions/jetbrains/)[

Enterprise

Enterprise governance

Configure Gemini Enterprise sign-in, IAM policies, and VPC Service Controls.

](/docs/enterprise/)

### Antigravity SDK

[

Architecture

SDK overview

Architectural overview of the Python runtime harness and async session manager.

](/docs/sdk/overview/)[

Agent API

Personas and directives

System prompt configuration and specialized agent personas.

](/docs/sdk/personas/)[

Extensibility

Tools and skills API

Register custom Python tools, shell executors, and skills.

](/docs/sdk/tools/)[

MCP

Model Context Protocol

Integrate external MCP servers and resources into SDK pipelines.

](/docs/sdk/mcp/)