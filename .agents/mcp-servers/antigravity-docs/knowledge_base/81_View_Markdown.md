# View Markdown
Source URL: https://antigravity.google/docs/getting-started.md

# Getting started

Welcome to Google Antigravity! Follow the instructions in this guide to get started on your preferred surface.

## Antigravity 2.0

### Download Antigravity 2.0

Visit [antigravity.google/download](/download) to download Google Antigravity 2.0. Select your operating system from the following table:

| Platform | Download |
| --- | --- |
| **macOS** | 
[Download for Apple Silicon](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.22.0-5446056071266304/darwin-arm/Antigravity.dmg)[Download for Intel](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.22.0-5446056071266304/darwin-x64/Antigravity.dmg)

**Requirements:** macOS versions with Apple security update support. This is typically the current and two previous versions. Minimum version 12 (Monterey); x86 is not supported.

 |
| **Windows** | 

[Download for x64](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.22.0-5446056071266304/windows-x64/Antigravity-x64.exe)[Download for ARM64](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.22.0-5446056071266304/windows-arm/Antigravity-arm64.exe)

**Requirements:** Windows 10 (64-bit)

 |
| **Linux** | 

[Download for x64](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.22.0-5446056071266304/linux-x64/Antigravity.tar.gz)[Download for ARM64](https://storage.googleapis.com/antigravity-public/antigravity-hub/2.22.0-5446056071266304/linux-arm/Antigravity.tar.gz)

**Requirements:** glibc >= 2.28, glibcxx >= 3.4.25 (for example, Ubuntu 20, Debian 10, Fedora 36, RHEL 8)

 |
| **Googlebook** | 

[Get it on Google Play](https://play.google.com/store/apps/details?id=com.google.android.apps.antigravity)

**Requirements:** Googlebook OS (pre-installed on Googlebooks; update or reinstall through the Google Play Store)

 |

### Installation

If you get a notification asking whether you want to â€œKeep Bothâ€ or â€œReplaceâ€ Antigravity, select **Replace**. You are prompted to reinstall the IDE during installation if you choose to do so. If you donâ€™t install it now and want to download it later, visit the [download page](/download).

When you launch Antigravity 2.0 and sign in, select your personal Google Account or choose **Business account** to connect with [Gemini Enterprise](/docs/enterprise#sign-in-and-license-selection).

### Creating a project

Agents work within projects, which define the boundaries of the folders and repositories they can access:

1.  Click the **folder with a â€+â€ icon** in the **left sidebar**.
2.  Click **New Project**.
3.  Click **Add Folder** to associate one or more local folders or Git repositories. Adding multiple folders provides your agent with full cross-repository context.
4.  Click **Create**.
5.  _(Optional)_ Configure your projectâ€™s settings. Each project maintains its own isolated settings and security policies that the agent respects.

### Starting an agent

Once your project is created, you can spawn an agent to start working on tasks:

1.  Type your goal or instruction in the chat input (for example, â€œHelp me add a new featureâ€) and press Enter.
2.  Choose a **Mode** in the setup modal to boot up your agent:
    *   **Local mode**: The agent operates directly in your active folders.
    *   **New worktree mode**: The agent operates in an isolated Git worktree.

### Basic navigation

Use the following keyboard shortcuts to navigate Antigravity 2.0:

| Action | macOS | Windows / Linux |
| :-- | :-- | :-- |
| **Open conversation picker** | âŒ˜K | Ctrl + K |
| **Open file search** | âŒ˜P | Ctrl + P |
| **Focus input** | âŒ˜L | Ctrl + L |
| **New conversation** | âŒ˜N | Ctrl + N |
| **Next/previous conversation** | âŒ¥ Up / Down | Alt + Up / Down |

### Slash commands

Use the following slash commands to control agent execution:

| Slash command | Description |
| :-- | :-- |
| `/goal` | Run until the specified task is completely finished, without asking for intermediate input. |
| `/grill-me` | Ask clarifying questions to align on the specific details of the plan before starting implementation. |
| `/schedule` | Run an instruction as a one-time timer in the future or on a recurring schedule using scheduled tasks. |
| `/browser` | Control browser debugging behaviors in Google Chrome. |
| [`/plugin`](/docs/plugins) | Manage installed [Marketplace](/docs/marketplace) plugins or create and configure custom plugin bundles. |

## Antigravity CLI

Welcome to Antigravity CLI! This guide provides a direct, high-level developer roadmap to install the client, launch the terminal user interface (TUI), and begin collaborating with autonomous agents.

### Roadmap checklist

Complete the following sequential steps to launch your first session:

1.  **Install the client (fast path)**
    
    Run the appropriate fast-path command for your operating system:
    
    **macOS / Linux / Googlebook**:
    
    ```
    curl -fsSL https://antigravity.google/cli/install.sh | bash
    ```
    
    **Windows (PowerShell)**:
    
    ```
    irm https://antigravity.google/cli/install.ps1 | iex
    ```
    
    **Windows (CMD)**:
    
    ```
    curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
    
    By default, the installer registers the `agy` binary to your platform-specific directory:
    
    *   **macOS / Linux / Googlebook**: `~/.local/bin/agy`
    *   **Windows**: `C:\Users\<username>\AppData\Local\agy\bin` (where `<username>` represents your active Windows profile name).
    
    Note
    
    **Advanced setup**: For [Gemini Enterprise authentication](/docs/enterprise#sign-in-and-license-selection), keyring permissions, API key setup, or troubleshooting installation issues, refer to the **[Installation and authentication guide](/docs/cli/install)**.
    
2.  **Launch the TUI inside a project**
    
    Open a fresh terminal window, navigate to your target project codebase directory, and execute the launcher command:
    
    ```
    agy
    ```
    
3.  **Complete the first-launch setup**
    
    On your very first launch, the TUI walks you through authentication and a brief interactive setup:
    
    *   **Sign in**: Authenticate in your browser with your personal Google Account, or choose **Business account** to sign in with [Gemini Enterprise](/docs/enterprise#sign-in-and-license-selection).
    *   **Color scheme**: Select your preferred visual theme (Solarized, Dark, Solarized Light, or standard terminal colors).
    *   **Rendering mode**: Choose Alt-Screen mode (alternate buffer with full-screen scrolling) or Inline mode (sequential stream integrated with your terminalâ€™s history).
    *   **Workspace trust**: Confirm that you trust the repository directory. Once confirmed, the agent indexes the files and stands ready.
4.  **Run your first agent task**
    
    Type the following instruction in the prompt box at the bottom of your TUI screen and press Enter:
    
    ```
    Write a simple python script to fetch web page text
    ```
    
    The agent reads the workspace, reasons about the task, and proposes a plan. For a detailed step-by-step tutorial on reviewing code and running test commands inside the TUI, follow the **[Tutorial guide](/docs/cli/tutorial)**.
    

### Related resources

Optimize your local environment configurations and master advanced collaboration tools:

*   **[Best practices](/docs/cli/best-practices)**: Master verification loops, planning phases, rule files, and session checkpoints.
*   **[Troubleshooting](/docs/cli/troubleshooting)**: Resolve common path, keyring, or SSH forwarding errors.
*   **[CLI reference](/docs/cli/reference)**: Review reference sheets cataloging all slash commands, shortcuts, and JSON keys.

## Antigravity IDE

### Download Antigravity IDE

Visit [antigravity.google/download](/download) to download Antigravity IDE. If you are using VS Code, JetBrains, Visual Studio, Zed, or Xcodeâ€”or connecting to [Gemini Enterprise](/docs/enterprise)â€”see [IDE extensions](/docs/ide/extensions).

Antigravity IDE supports the following platforms and minimum versions:

*   **macOS**: macOS versions with Apple security update support (typically the current and two previous versions). Minimum version 12 (Monterey); x86 is not supported.
*   **Windows**: Windows 10 (64-bit).
*   **Linux**: glibc >= 2.28, glibcxx >= 3.4.25 (for example, Ubuntu 20, Debian 10, Fedora 36, RHEL 8).

The application prompts you when updates are available:

![Update Available](/assets/image/docs/restart-to-update.png)