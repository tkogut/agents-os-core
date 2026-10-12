# Troubleshooting
Source URL: https://antigravity.google/docs/cli/troubleshooting

Get Started
CLI
Troubleshooting
Markdown
Troubleshooting
Section titled “Troubleshooting”

Diagnose and resolve common anomalies with installation PATHs, local self-updating locks, keyring access permissions, and SSH clipboard forwarding.

Quick reference
Section titled “Quick reference”

Scan the following lookup table to identify symptoms and access immediate solutions:

Error Symptom	Potential Cause	Target Resolution
agy: command not found	Binary directory missing from shell environments.	Configure your shell PATH
keyring: secure lock out	Missing system service permissions or active lockouts.	Authorize keyring permissions
SSH Clipboard paste failures	Protocol streams blocked or missing forward configurations.	Enable emulator clipboard forwarding
Advisory lock / update failures	Locked self-updater thread or read-only directory paths.	Resolve self-updater locks and failures
Configure your shell PATH
Section titled “Configure your shell PATH”
Symptom
Section titled “Symptom”

Executing agy returns a shell terminal error:

bash: agy: command not found
Cause
Section titled “Cause”

The installation utility downloads the binary to ~/.local/bin (or C:\Users\<username>\AppData\Local\agy\bin), but your shell’s active $PATH environment doesn’t index this directory.

Resolution
Section titled “Resolution”

Ensure your terminal session loads the binary path.

macOS and Linux:

To add the binary directory to your path on macOS or Linux, follow these steps:

Open your shell configuration file (~/.bashrc or ~/.zshrc).
Verify or append the following line at the end of the file:
export PATH="~/.local/bin:$PATH"
Reload your profile configurations:
source ~/.zshrc

Windows (PowerShell):

To add the binary directory to your path on Windows, follow these steps:

Open a PowerShell terminal as an Administrator and execute the following command:
[System.Environment]::SetEnvironmentVariable("Path", [System.Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Program Files\Google\antigravity-cli", "User")
Restart your terminal emulator for the system registry environment to refresh.
Authorize keyring permissions
Section titled “Authorize keyring permissions”
Symptom
Section titled “Symptom”

When launching, the CLI hangs, prints D-Bus warnings, or throws keyring access exceptions:

Error: failed to retrieve token: secret keyring is locked
Cause
Section titled “Cause”

Antigravity CLI uses secure keychain libraries (Apple Keychain, Linux secret-service through D-Bus, or Windows Credential Manager) to encrypt your session tokens. If the background daemon is locked or headless, the CLI can’t read credentials.

Resolution
Section titled “Resolution”

macOS:

To authorize keychain access on macOS, follow these steps:

Open the Keychain Access app.
Search for the Antigravity CLI security item.
Right-click, select Get Info, choose the Access Control tab, and verify that agy is on the allowed applications list.
If you’re running inside a headless SSH session on macOS, enforce an auto-lock inactivity timeout (for example, 5 minutes) and unlock the keychain interactively:
security set-keychain-settings -l -u -t 300 ~/Library/Keychains/login.keychain-db
security unlock-keychain ~/Library/Keychains/login.keychain-db
When your session is finished, optionally re-lock the keychain immediately:
security lock-keychain ~/Library/Keychains/login.keychain-db

Linux:

Ensure your system keyring (such as GNOME Keyring or KWallet) is unlocked and accessible.

If you’re running in a headless environment or over SSH, ensure that a D-Bus session is active and that your keyring daemon is running. You can typically initialize a D-Bus session by running:

export $(dbus-launch)

If you still experience access issues, ensure your user account has the necessary permissions to access the keyring service or reach out to support.

Enable emulator clipboard forwarding
Section titled “Enable emulator clipboard forwarding”
Symptom
Section titled “Symptom”

Pasting screenshots or media files using Ctrl+V within an SSH terminal returns a failure notification:

Error: local pasteboard is empty or unreachable over SSH connection
Cause
Section titled “Cause”

Standard SSH streams don’t forward graphical clipboards. Graphic uploads require specific terminal multiplexer protocols.

Resolution
Section titled “Resolution”

Verify that you’re using supported terminal emulators and configurations:

Use iTerm2 or Ghostty: These emulators support advanced clip channels.
Configure iTerm2 forwarding: Enable clipboard access in your terminal settings:
Open iTerm2 Preferences (Cmd+,).
Go to General > Selection.
Select Applications in terminal may access clipboard (enabling OSC 52 write channels).
Bypass multiplexers: If running inside tmux, ensure your active configuration maps standard paste clips:
set -s set-clipboard on
Resolve self-updater locks and failures
Section titled “Resolve self-updater locks and failures”
Symptom
Section titled “Symptom”

Launching agy hangs, fails to apply upgrades, or returns an advisory lock warning:

Warning: another background updater process is already active (update.lock)
Cause
Section titled “Cause”

Antigravity CLI contains a native, statically linked self-updater that runs in the background. It uses a 15-minute Time-To-Live (TTL) debounce marker (last_check.timestamp) and an advisory lock (update.lock) inside ~/.gemini/antigravity-cli/updater/ to prevent concurrent process collisions. If a background updater process hangs, crashes without releasing the lock, or has insufficient user filesystem permissions inside the executable directory, subsequent updates are blocked.

Resolution
Section titled “Resolution”

Try any of the following steps to resolve the updater lock:

Release the advisory lock: Purge the background lock file manually:
rm -f ~/.gemini/antigravity-cli/updater/update.lock
Opt out or disable auto-updates: Set the AGY_CLI_DISABLE_AUTO_UPDATE environment variable to true inside your shell profile (~/.bashrc or ~/.zshrc):
export AGY_CLI_DISABLE_AUTO_UPDATE=true
Verify directory write permissions: Ensure your user profile owns and has write permissions inside the target installation directory (~/.local/bin/ on Unix, or %LOCALAPPDATA%\agy\bin on Windows).
Next steps
Section titled “Next steps”

Access the quick reference sheets or configure advanced permissions:

CLI reference: Reference tables listing all slash commands and visual settings keys.
Permissions: Configure fine-grained allowed and denied action policies.
Sandbox: Enforce OS-level container isolation boundaries.
Plugins and skills: Create your own custom skills.
Previous
Best practices
Next
CLI reference
About Google
Google Products
Privacy
Terms