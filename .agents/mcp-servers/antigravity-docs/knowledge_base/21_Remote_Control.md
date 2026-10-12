# Remote Control
Source URL: https://antigravity.google/docs/remote-control

Features
Learn
Remote Control
Markdown
AVAILABLE ON:
Antigravity 2.0
Antigravity CLI
Remote Control
Section titled “Remote Control”

Antigravity Remote Control allows you to securely connect to and drive your Antigravity desktop sessions and CLI instances running across your machines from any web browser.

As AI agents take on larger-scope tasks—such as full-subsystem refactorings, extensive test suite runs, and complex dependency migrations—operations can run for extended periods. Remote Control untethers you from your physical desk while preserving your entire local development environment.

Antigravity 2.0
Antigravity CLI
Antigravity 2.0
Enabling Remote Control in Antigravity 2.0
Section titled “Enabling Remote Control in Antigravity 2.0”

You can enable Remote Control directly from the Antigravity 2.0 settings:

Open the Settings panel by pressing Cmd + , (or Ctrl + , on Linux and Windows), or click Settings at the bottom of the left sidebar.
Navigate to the App section.
Toggle Enable Remote Control to On.
(Optional) Set a custom Nickname (for example, workstation-primary or server-machine) to easily identify this machine in your instance list.
Connecting from a web browser
Section titled “Connecting from a web browser”

To access your remote Antigravity instance:

Open your web browser on any device and navigate to the Antigravity Remote Control Dashboard. (Tip: On mobile devices, you can optionally install the web app to your home screen to receive push notifications when agents complete tasks or request input.)
Sign in with the same Google Account that you used on your desktop application.
In the instance switcher, select the machine you want to control.
You now have full access to view active conversations, start new agent tasks, review implementation plans, and inspect artifacts.
Desktop troubleshooting
Section titled “Desktop troubleshooting”
Antigravity 2.0 desktop
Section titled “Antigravity 2.0 desktop”

If you encounter issues connecting to your desktop instance, review the following troubleshooting steps:

Machine does not appear in the web UI:
Ensure that Enable Remote Control is toggled on in Antigravity 2.0 settings on your host machine.
Verify that your host machine has an active internet connection and is not asleep or suspended.
Check that you are signed in with the same Google Account in both the desktop app and the web browser.
Reconnection and disconnects:
If your local network connectivity drops temporarily, the web interface automatically tries to reconnect. Any running background agent tasks and shell commands continue executing on your host machine uninterrupted as long as the host maintains an internet connection.
Next steps
Section titled “Next steps”

Explore related documentation and guides:

Settings overview: Explore configuration options across Antigravity.
Permissions and security: Configure permission presets and tool access rules.
Previous
Overview
Next
Marketplace
About Google
Google Products
Privacy
Terms