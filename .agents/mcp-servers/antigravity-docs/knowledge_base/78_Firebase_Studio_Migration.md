# Firebase Studio Migration
Source URL: https://antigravity.google/docs/firebase-studio-migration

Migration
>
Firebase Studio Migration
Firebase Studio Migrationlink

Antigravity is Google’s next-generation, agent-first platform. It’s designed to be the primary home for high-velocity, autonomous development workflows. Instead of relying on just a cloud-based web editor, Antigravity brings the power of AI right into your local development environment.

Why Antigravity?link

Antigravity offers significant enhancements over the web-based Code view in Firebase Studio:

Local environment control: Antigravity runs locally on your machine, which means you have full control over your filesystem, versions, and terminal.
True agentic development: Move beyond basic code completion. Antigravity provides agentic development workflows that can autonomously format, test, and implement entire tasks across your codebase.
Seamless Firebase support: You can still easily deploy your projects to Firebase, communicate with Firebase services via the Firebase CLI, and test your functions locally as you always have.
Learn how to navigate Antigravitylink

To help you settle in, here is where you can find your favorite Firebase Studio features in Antigravity:

code

Cloud IDE Code view
keyboard_arrow_right

Enjoy the familiar interface of VS Code, but supercharged with AI and running locally on your hardware.

auto_awesome

Agentic chat
keyboard_arrow_right

The AI chat you used in Firebase Studio is now natively integrated into your IDE, capable of taking autonomous actions across your local files.

rocket_launch

App Hosting deployments
keyboard_arrow_right

You can continue to deploy and manage your App Hosting URLs seamlessly using the Firebase CLI or built-in IDE integrations.

important_devices

Browser-based emulators
keyboard_arrow_right

Run the Firebase Local Emulator Suite directly on your machine for faster, offline testing.

Migrate your Firebase Studio project to Antigravitylink

Antigravity is a local, agent-first IDE that brings the power of AI into your local development environment.

Prerequisiteslink

Ensure you have the following installed locally and fully up-to-date:

Google Antigravity IDE
Node.js (version 20 or higher)
Firebase CLI (version 15.10.0 or higher)
Step 1: Export and initialize your applink

Option 1: Automated migration

This workflow uses the Antigravity agent to autonomously handle project transformation.

In Firebase Studio, click the Move now button at the top of your workspace.
Follow the export method based on the window that appears:
If you see a Zip and Download button, click it.
Otherwise, open the command palette (Cmd + Shift + P on Mac or Ctrl + Shift + P on ChromeOS, Windows, or Linux) and run the Firebase Studio: Zip & Download command.
Extract the folder locally and open it in Antigravity.
In the Agent pane within Antigravity, enter the following prompt. To optimize your workflow and conserve tokens, we recommend selecting the Gemini Flash model. It’s designed for speed and efficiency in high-volume transformation tasks like file conversion.
content_copy
@fbs-to-agy-export

The Antigravity agent will then begin project migration, requesting your assistance along the way. Follow the agent’s guidance to complete the migration process. If you encounter any errors, prompt the agent to try again.

info
If the download window doesn’t appear, check your browser’s address bar for a pop-up blocker icon and ensure pop-ups are allowed.

Option 2: Manual export

If you prefer to manage the migration yourself without using AI tokens, you can use the Firebase CLI to manually export your project. This method is direct and does not require agent interaction.

Open your terminal and run the following command, replacing <path> with the file path to your extracted project folder or the original .zip file:

bash
content_copy
npx firebase-tools@latest studio:export <path>
warning
The studio:export command is currently optimized for Next.js, Flutter, and Angular workspaces. While you can use this command for other workspace types, the migration may not be fully successful. We’re actively working to improve the migration flow.
Step 2: Preview your applink

Once you have extracted your project and opened it within Antigravity, you can view your application locally:

In Antigravity, navigate to the Run and Debug menu located in the left sidebar.
Click the play button to start your local development server.
Follow the instructions in the terminal to preview your app.
lightbulb
To refine your app or troubleshoot issues, simply chat with the agent using natural language. If the agent pane is hidden, click the Toggle Agent icon at the top of the window to reopen it.
Step 3: Publish your applink

Antigravity uses agent skills to publish your app using Firebase best practices.

In the chat panel, enter the following prompt: simply instruct the agent:
content_copy
Publish my app
When prompted to run firebase deploy, choose Yes. The agent will publish to your existing URL if you’ve previously published to App Hosting. If this is your first time publishing to App Hosting, the agent will walk you through the process.
For future updates, simply instruct the agent to publish my app in the Antigravity chat panel.
Continue your worklink

There are several ways you can continue your development in Antigravity.

Running workflows: In Antigravity, you can seamlessly execute workflows and continue your work with the model by typing @workflows <workflow_name> into the agentic chat panel.
App Hosting deployments: You can seamlessly deploy your apps directly through the agent using agent skills, or by using the platform-agnostic Firebase CLI and GitHub.
Troubleshooting: If you experience deployment issues, try re-authenticating with the Firebase CLI or verifying your project secrets.

Thank you for being part of the Firebase Studio journey. Your prototypes and feedback have directly shaped Google’s AI tools, and we can’t wait to see what you build next in Antigravity!

Need help?link

File any migration bugs in our GitHub Issues.

Settings
Enterprise