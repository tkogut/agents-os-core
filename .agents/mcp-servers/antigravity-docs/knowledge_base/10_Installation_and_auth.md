# Installation and auth
Source URL: https://antigravity.google/docs/cli/install

Get Started
CLI
Installation and auth
Markdown
Installation and auth
Section titled “Installation and auth”

Install Antigravity CLI (agy), configure your environment, and establish secure authenticated sessions.

Installation
Section titled “Installation”

Antigravity CLI runs natively on macOS, Linux, Googlebook, and Windows. Use the following platform-specific scripts to install or upgrade the binary on your system.

macOS, Linux, and Googlebook
Section titled “macOS, Linux, and Googlebook”

Execute the native installer script to download and install the executable to ~/.local/bin/agy:

curl -fsSL https://antigravity.google/cli/install.sh | bash
Windows
Section titled “Windows”

The installation script registers the agy binary to your local user directory: C:\Users\<username>\AppData\Local\agy\bin (where <username> represents your active Windows user profile).

PowerShell: Open PowerShell and execute the following installation script:

irm https://antigravity.google/cli/install.ps1 | iex

CMD: Open a standard Command Prompt and execute the following command:

curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
Verify installation and version
Section titled “Verify installation and version”

Verify the installed version (or run agy update to update an existing installation):

agy --version
Installation flags
Section titled “Installation flags”

When executing the installation scripts, you can append the following customization flags:

--skip-aliases: Bypasses shell profile alias purging (prevents the script from purging or updating legacy agy or antigravity shell aliases).
--skip-path: Bypasses shell profile PATH appending (prevents the script from modifying your shell profile’s dynamic environment variables).
Authentication workflows
Section titled “Authentication workflows”

Antigravity CLI uses secure credentials and token profiles to communicate with the shared agent harness.

Local silent keyring sign-in
Section titled “Local silent keyring sign-in”

When launching agy on your local machine, the CLI attempts to access your operating system’s native secure keyring (such as Apple Keychain, Linux Secret Service/D-Bus, or Windows Credential Manager). If a valid token profile is found, the CLI authenticates your session silently without opening a browser.

If no saved session is found, complete the sign-in flow:

The CLI automatically launches your local default web browser.
Sign in using your personal Google Account, or select Business account to authenticate with Gemini Enterprise.
Remote SSH OAuth flow
Section titled “Remote SSH OAuth flow”

When running over SSH, the CLI detects the remote connection environment. Because it can’t launch a local web browser, the CLI initiates a manual URL loop:

Launch agy in your remote terminal session.
The CLI detects the SSH environment and prints a unique, secure authorization URL.
Copy this URL and paste it into a web browser on your local machine.
Sign in with your approved credentials and complete the authentication.
The browser displays a unique alphanumeric authorization code.
Copy this code, return to your remote SSH terminal, and paste it into the prompt.
Gemini Enterprise authentication
Sign in with Google Cloud SSO, Workforce Identity Federation (BYOID/WIF), or Application Default Credentials (ADC).
Using a Gemini API key
Section titled “Using a Gemini API key”

Run Antigravity CLI with your own Gemini API key instead of a signed-in Google account. Model requests go directly to the Gemini API, and the CLI never establishes an account session. This suits headless and CI runs, where no browser is available to complete a sign-in. Create a key in Google AI Studio.

To use a Gemini API key, you must set a provider and an environment variable with the API key. Setting a GEMINI_API_KEY environment variable on its own has no effect.

Enable the Gemini API key
Section titled “Enable the Gemini API key”

To enable authentication with a Gemini API key, follow these steps:

Set modelProvider to gemini in ~/.gemini/antigravity-cli/settings.json:

{
    "modelProvider": "gemini"
}

Export your key as GEMINI_API_KEY:

export GEMINI_API_KEY="your-api-key"

This applies to the current shell only. Add the same line to your shell profile, such as ~/.zshrc or ~/.bashrc, to persist it across sessions.

Start the CLI:

agy

The CLI skips the sign-in screen and opens the main interface directly. The header shows Gemini API key instead of your account email:

Note: When you authenticate with a GEMINI_API_KEY, /logout has no effect because there is no stored session to clear.

Point the CLI to a custom endpoint
Section titled “Point the CLI to a custom endpoint”

To send model requests to a different Gemini-compatible endpoint, set the GOOGLE_GEMINI_BASE_URL environment variable:

export GOOGLE_GEMINI_BASE_URL="https://your-endpoint.example.com"
Revert to default authentication
Section titled “Revert to default authentication”

If you want to revert to using the default account-based authentication, follow these steps:

Remove modelProvider from ~/.gemini/antigravity-cli/settings.json.
Restart the CLI to sign in to your account.

Note: The CLI can’t start if you unset the GEMINI_API_KEY environment variable while modelProvider is still set to gemini.

Troubleshooting
Section titled “Troubleshooting”
Symptom	Cause	Resolution
The CLI exits at startup reporting that GEMINI_API_KEY is not set	modelProvider is gemini but the key is missing from the environment	Export GEMINI_API_KEY, or remove modelProvider to use the default authentication
The CLI signs in normally and ignores the setting	modelProvider holds an unrecognized value	gemini is the only accepted value. Check the spelling and restart the CLI
A key set through GOOGLE_API_KEY or a .env file has no effect	The CLI reads the credential only from GEMINI_API_KEY in the environment, and does not load .env files	Export GEMINI_API_KEY in your shell or shell profile
Requests fail mid-session with a generic model error	The key is invalid, revoked, or lacks access to the requested model	Verify the key in Google AI Studio. The CLI checks only that the key is non-empty at startup, so an unusable key only surfaces on the first conversation
Managing your session
Section titled “Managing your session”

Terminating your session clears active credentials and local cache directories.

Logging out
Section titled “Logging out”

To disconnect your account and purge saved authentication profiles from your operating system’s keyring, run the following command in the CLI prompt box:

/logout
Next steps
Section titled “Next steps”

Once you complete installation and authentication, start interacting with your local agent:

Tutorial: Create and run a basic Python project with an agent.
Prompting and interaction: Explore multiline text editing, interrupt commands, and terminal media pasting.
Permissions and sandbox: Configure secure filesystem directories and command limits.
Previous
CLI overview
Next
Tutorial
About Google
Google Products
Privacy
Terms