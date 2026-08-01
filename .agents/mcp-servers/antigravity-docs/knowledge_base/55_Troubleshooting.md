# Troubleshooting
Source URL: https://antigravity.google/docs/cli/troubleshooting

Antigravity CLI
>
Troubleshooting
Troubleshootinglink

Diagnose and resolve common anomalies with installation PATHs, local self-updating locks, keyring access permissions, and SSH clipboard forwarding.

Quick referencelink

Scan the lookup table below to identify symptoms and access immediate solutions:

Error Symptom	Potential Cause	Target Resolution
agy: command not found	Binary directory missing from shell environments.	Configure your shell PATH
keyring: secure lock out	Missing system service permissions or active lockouts.	Authorize keyring permissions
SSH Clipboard paste failures	Protocol streams blocked or missing forward configurations.	Enable emulator clipboard forwarding
Advisory lock / update failures	Locked self-updater thread or read-only directory paths.	Resolve self-updater locks and failures
Configure your shell PATHlink
Symptomlink

Executing agy returns a shell terminal error:

bash
content_copy
bash: agy: command not found
Causelink

The installation utility downloads the binary to ~/.local/bin (or C:\Users\<Username>\AppData\Local\agy\bin), but your shell’s active $PATH environment does not index this directory.

Resolutionlink

Ensure your terminal session loads the binary path.

macOS & Linux:

Open your shell configuration file (~/.bashrc or ~/.zshrc).
Verify or append the following line at the end of the file:
bash
content_copy
export PATH="~/.local/bin:$PATH"
Reload your profile configurations:
bash
content_copy
source ~/.zshrc

Windows (PowerShell):

Open a PowerShell terminal as an Administrator and execute:
powershell
content_copy
[System.Environment]::SetEnvironmentVariable("Path", [System.Environment]::GetEnvironmentVariable("Path", "User") + ";C:\Program Files\Google\antigravity-cli", "User")
Restart your terminal emulator for the system registry environment to refresh.
Authorize keyring permissionslink
Symptomlink

When launching, the CLI hangs, prints DBUS warnings, or throws keyring access exceptions:

text
content_copy
Error: failed to retrieve token: secret keyring is locked
Causelink

Antigravity CLI utilizes secure keychain libraries (Apple Keychain, Linux secret-service via dbus, or Windows Credential Manager) to encrypt your session tokens. If the background daemon is locked or headless, the CLI cannot read credentials.

Resolutionlink

macOS:

Open Keychain Access app.
Search for the Antigravity CLI security item.
Right-click, select Get Info, choose the Access Control tab, and verify that agy is on the allowed applications list.
If running inside a headless SSH session on Mac, run the following unlock sequence:
bash
content_copy
security unlock-keychain -p "your_keychain_password" login.keychain

Linux:

Ensure your system keyring (such as GNOME Keyring or KWallet) is unlocked and accessible.

If you are running in a headless environment or over SSH, ensure that a D-Bus session is active and that your keyring daemon is running. You can typically initialize a D-Bus session by running:

bash
content_copy
export $(dbus-launch)

If you still experience access issues, ensure your user account has the necessary permissions to access the keyring service or reach out to support.

Enable emulator clipboard forwardinglink
Symptomlink

Pasting screenshots or media files via Ctrl+V within an SSH terminal returns a failure notification:

text
content_copy
Error: local pasteboard is empty or unreachable over SSH connection
Causelink

Standard SSH streams do not forward graphical clipboards. Graphic uploads require specific terminal multiplexer protocols.

Resolutionlink

Verify that you are utilizing supported terminal emulators and configurations.

Use iTerm2 or Ghostty: These emulators support advanced clip channels.
Configure iTerm2 Forwarding:
Open iTerm2 Preferences (Cmd+,).
Go to the General tab, select Selection submenu.
Check Applications in terminal may access clipboard (enabling OSC 52 write channels).
Bypass Multiplexers: If running inside tmux, ensure your active configuration maps standard paste clips correctly:
text
content_copy
set -s set-clipboard on
Resolve self-updater locks and failureslink
Symptomlink

Launching agy hangs, fails to apply upgrades, or returns an advisory lock warning:

text
content_copy
Warning: another background updater process is already active (update.lock)
Causelink

Antigravity CLI contains a native, statically linked self-updater that runs in the background. It uses a 15-minute Time-To-Live (TTL) debounce marker (last_check.timestamp) and an advisory lock (update.lock) inside ~/.gemini/antigravity-cli/updater/ to prevent concurrent process collisions. If a background updater process hangs, crashes without releasing the lock, or has insufficient user filesystem permissions inside the executable directory, subsequent updates are blocked.

Resolutionlink
Release the advisory lock: Purge the background lock file manually:
bash
content_copy
rm -f ~/.gemini/antigravity-cli/updater/update.lock
Opt-out/Disable auto-updates: Set the AGY_CLI_DISABLE_AUTO_UPDATE environment variable to true inside your shell profile (~/.bashrc or ~/.zshrc):
bash
content_copy
export AGY_CLI_DISABLE_AUTO_UPDATE=true
Verify directory write permissions: Ensure your user profile owns and has write permissions inside the target installation directory (~/.local/bin/ on Unix, or %LOCALAPPDATA%\agy\bin on Windows).
Next stepslink

Access our quick reference sheets or configure advanced permissions:

CLI Reference: Dense tables listing all slash commands and visual settings keys.
Permissions: Configure fine-grained allowed and denied action policies.
Sandbox: Enforce OS-level container isolation boundaries.
Plugins & Skills: Create your own custom skills.
Best Practices
CLI Reference