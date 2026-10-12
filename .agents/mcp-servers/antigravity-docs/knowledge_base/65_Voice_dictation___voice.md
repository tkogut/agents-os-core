# Voice dictation (/voice)
Source URL: https://antigravity.google/docs/cli/commands/voice

Features
Slash commands
Voice dictation (/voice)
Markdown
AVAILABLE ON:
Antigravity CLI
Voice dictation (/voice)
Section titled “Voice dictation (/voice)”

Speak your prompt instead of typing it.

Overview
Section titled “Overview”

The /voice command (alias /record) records audio from your microphone and streams real-time transcripts directly into the prompt box as you speak. You can also start dictation at any time using the F5 key.

Voice dictation writes text into the prompt box; it doesn’t automatically submit your prompt. When you stop recording, the transcript remains in the prompt box as if you had typed it, allowing you to edit, expand, and submit the text when you’re ready.

Caution

Sign out and sign back in first: Voice dictation requires an updated authentication permission granted at sign-in. If your active session was authenticated before voice dictation became available, transcription fails. Run /logout, sign in again, and retry. This is a one-time setup step.

Dictating a prompt
Section titled “Dictating a prompt”

To dictate a prompt into the terminal, follow these steps:

Press F5, or type /voice in the prompt box and press ENTER.
Wait for the status line below the prompt to transition from Connecting… to Recording.
Speak clearly into your microphone. Interim text appears in the prompt box and updates as the transcription service processes audio.
Press ENTER (or F5) to stop recording and retain the transcript in the prompt box.

While a recording session is active, the status line below the prompt displays the elapsed recording time and available shortcut actions:

● Recording 0:07  enter or f5 to insert · esc to discard
Dictation controls
Section titled “Dictation controls”

The following keyboard shortcuts control active dictation sessions. All other keystrokes are ignored during recording to prevent accidental input:

Key	Action
ENTER (or F5)	Stop recording and insert the transcript into the prompt.
ESC	Discard the recording and restore previous prompt contents.
CTRL+Z (after)	Revert the entire dictation as a single undo operation.

If the prompt box already contained text before starting dictation, the transcript is appended to the existing text rather than replacing it.

Note

The F5 key is remappable. Use /keybindings to bind voice.start_dictation to a different shortcut; the on-screen hint automatically updates to reflect your custom keybinding.

Availability
Section titled “Availability”

Voice dictation is subject to the following operating constraints:

Dictation requires an interactive TUI session and is disabled in non-interactive print mode (--print).
Dictation isn’t currently supported for business or enterprise accounts.
Voice over SSH
Section titled “Voice over SSH”

When the CLI runs on a remote machine over Secure Shell (SSH), the remote environment lacks direct access to your local audio hardware. The mic-serve subcommand resolves this by streaming audio from your local microphone over a local loopback socket, which is forwarded to the remote CLI through a reverse SSH tunnel.

The Antigravity CLI must be installed on both your local machine and the remote host.

Serve your local microphone
Section titled “Serve your local microphone”

Start the microphone server on your local machine:

agy mic-serve

Keep this process running while dictating. By default, mic-serve listens on 127.0.0.1:4713 and streams audio from your default input device to connected clients. You can run it inside a background job, a tmux pane, or a separate terminal window.

To bind to a custom port if port 4713 is already occupied, specify the --addr flag:

agy mic-serve --addr 127.0.0.1:<UNUSED_PORT>

Caution

Keep mic-serve on 127.0.0.1: The microphone server is intended for local connections forwarded through SSH tunnels. Keep it bound to loopback so external devices on your network can’t access the audio stream.

Open a reverse tunnel
Section titled “Open a reverse tunnel”

From your local machine, forward the local audio port to the remote machine by opening a reverse SSH tunnel:

ssh -R 24713:127.0.0.1:4713 <remote-machine>

The tunnel must remain active during dictation. To run the tunnel in the background without maintaining an interactive shell session, use the -f and -N flags with the ssh command. For example:

ssh -f -N -R 24713:127.0.0.1:4713 <remote-machine>
Start the CLI with ANTIGRAVITY_MIC
Section titled “Start the CLI with ANTIGRAVITY_MIC”

In your remote SSH session, launch the CLI with the ANTIGRAVITY_MIC environment variable set to the forwarded tunnel port. For example:

ANTIGRAVITY_MIC=127.0.0.1:24713 agy

If you’re using a Windows remote host with PowerShell, set the environment variable and start the CLI:

$env:ANTIGRAVITY_MIC = "127.0.0.1:24713"; agy

Alternatively, if you’re using a Windows remote host with Windows Command Prompt (cmd.exe), run the following command:

set ANTIGRAVITY_MIC=127.0.0.1:24713 && agy

In the CLI, press F5 or use /voice, and speak into your microphone. The local mic-serve process logs a confirmation when the CLI initiates an audio connection. For example:

Recording for 127.0.0.1:54134.
Verify the tunnel connection
Section titled “Verify the tunnel connection”

If no connection log appears in the mic-serve output when dictating, test whether the forwarded port is reachable by capturing a raw audio sample on the remote host. For example:

timeout 5 nc 127.0.0.1 24713 > /tmp/mic.raw

If /tmp/mic.raw accumulates data at approximately 32 kB/s, audio streaming across the reverse tunnel is operating properly.

Troubleshooting
Section titled “Troubleshooting”

If you encounter issues with voice dictation, review the following solutions:

Transcription fails with a permissions message: Your stored credentials predate voice dictation support. Execute /logout, sign in again to refresh permissions, and retry. Note that voice dictation isn’t available for business or enterprise accounts.
Nothing is transcribed and the recording is silent: The active terminal process lacks operating system microphone permissions (the terminal running the CLI for local sessions, or the terminal running agy mic-serve for SSH sessions):
macOS: Approve the system permission dialog, or grant access under System Settings > Privacy & Security > Microphone. Restart your terminal using CMD+Q to apply the updated permission.
Windows: Enable microphone access under Settings > Privacy & Security > Microphone, and ensure Let desktop apps access your microphone is enabled.
Connecting fails immediately over SSH: No process is listening on the forwarded port. Verify that both agy mic-serve on your local machine and the ssh -R reverse tunnel are running.
Dictation reports that the microphone server closed the connection: The server process terminated or the network tunnel dropped. Inspect the output of agy mic-serve on your local machine for detailed error diagnostics.
The wrong microphone is used: mic-serve captures audio from the system default input device. Verify your default input hardware under System Settings > Sound > Input (macOS) or Settings > System > Sound > Input (Windows).
The transcript is choppy or drops words: Audio is streamed uncompressed across the SSH tunnel; high latency or bandwidth saturation on the SSH connection can result in dropped audio packets.
Next steps
Section titled “Next steps”

Explore the following guides to learn more about CLI commands and interaction:

CLI reference: View all available slash commands and keybindings.
Prompting and interaction: Multiline editing, interrupts, and pasting media into the prompt.
Installation and auth: Sign-in flows, including the remote SSH OAuth loop.
Previous
Model quotas (/usage)
Next
MCP
About Google
Google Products
Privacy
Terms