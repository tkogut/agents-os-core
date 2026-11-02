# Firebase Studio
Source URL: https://antigravity.google/docs/firebase-studio-migration

Firebase Studio migration2-0Antigravity AppGet StartedFirebase Studio migration Antigravity App Get StartedAntigravity App
Get Started
Migrations
Firebase Studio
Markdown
Firebase Studio migration
Section titled “Firebase Studio migration”

Antigravity is Google’s next-generation, agent-first platform. It’s designed to be the primary home for high-velocity, autonomous development workflows. Instead of relying on a cloud-based web editor, Antigravity brings the power of AI directly into your local development environment.

Why Antigravity?
Section titled “Why Antigravity?”

Antigravity offers significant enhancements over the web-based Code view in Firebase Studio:

Local environment control: Antigravity runs locally on your machine, which means you have full control over your filesystem, versions, and terminal.
True agentic development: Move beyond basic code completion. Antigravity provides agentic development workflows that can autonomously format, test, and implement entire tasks across your codebase.
Seamless Firebase support: You can still easily deploy your projects to Firebase, communicate with Firebase services using the Firebase CLI, and test your functions locally as you always have.
Learn how to navigate Antigravity
Section titled “Learn how to navigate Antigravity”

To help you settle in, here is where you can find your favorite Firebase Studio features in Antigravity:

Cloud IDE Code view

Enjoy the familiar interface of VS Code, enhanced with AI and running locally on your hardware.

Agentic chat

The AI chat you used in Firebase Studio is now natively integrated into your IDE, capable of taking autonomous actions across your local files.

App Hosting deployments

You can continue to deploy and manage your App Hosting URLs seamlessly using the Firebase CLI or built-in IDE integrations.

Browser-based emulators

Run the Firebase Local Emulator Suite directly on your machine for faster, offline testing.

Migrate your Firebase Studio project to Antigravity
Section titled “Migrate your Firebase Studio project to Antigravity”

Antigravity is a local, agent-first IDE that brings the power of AI into your local development environment.

Prerequisites
Section titled “Prerequisites”

Ensure you have the following installed locally and fully up to date:

Google Antigravity IDE
Node.js (version 20 or later)
Firebase CLI (version 15.10.0 or later)
Export and initialize your app
Section titled “Export and initialize your app”

Option 1: Automated migration

This workflow uses the Antigravity agent to autonomously handle project transformation:

In Firebase Studio, click the Move now button at the top of your workspace.

Follow the export method based on the window that appears:

If a Zip and Download button appears, click it.
Otherwise, open the Command Palette (Cmd+Shift+P on macOS or Ctrl+Shift+P on ChromeOS, Windows, or Linux) and run the Firebase Studio: Zip & Download command.

Extract the folder locally and open it in Antigravity.

In the Agent pane within Antigravity, enter the following prompt. To optimize your workflow and conserve tokens, we recommend selecting the Gemini Flash model, which is designed for speed and efficiency in high-volume transformation tasks like file conversion:

@fbs-to-agy-export

The Antigravity agent begins project migration, requesting your assistance along the way. Follow the agent’s guidance to complete the migration process. If you encounter any errors, prompt the agent to try again.

Note

If the download window doesn’t appear, check your browser’s address bar for a pop-up blocker icon and ensure pop-ups are allowed.

Option 2: Manual export

If you prefer to manage the migration yourself without using AI tokens, you can use the Firebase CLI to manually export your project. This method is direct and doesn’t require agent interaction.

Open your terminal and run the following command, replacing <path> with the file path to your extracted project folder or the original .zip file:

npx firebase-tools@latest studio:export <path>

Note

The studio:export command is currently optimized for Next.js, Flutter, and Angular workspaces. While you can use this command for other workspace types, the migration might not be fully successful. We’re actively working to improve the migration flow.

Preview your app
Section titled “Preview your app”

Once you have extracted your project and opened it within Antigravity, you can view your application locally:

In Antigravity, navigate to the Run and Debug menu in the left sidebar.
Click the play button to start your local development server.
Follow the instructions in the terminal to preview your app.

Note

To refine your app or troubleshoot issues, chat with the agent using natural language. If the agent pane is hidden, click the Toggle Agent icon at the top of the window to reopen it.

Publish your app
Section titled “Publish your app”

Antigravity uses agent skills to publish your app using Firebase best practices:

In the chat panel, enter the following prompt:

Publish my app

When prompted to run firebase deploy, choose Yes. The agent publishes to your existing URL if you’ve previously published to App Hosting. If this is your first time publishing to App Hosting, the agent walks you through the process.

For future updates, instruct the agent to publish my app in the Antigravity chat panel.

Continue your work
Section titled “Continue your work”

There are several ways you can continue your development in Antigravity:

Running workflows: In Antigravity, you can seamlessly execute workflows and continue your work with the model by typing @workflows <workflow_name> into the agentic chat panel.
App Hosting deployments: You can seamlessly deploy your apps directly through the agent using agent skills, or by using the platform-agnostic Firebase CLI and GitHub.
Troubleshooting: If you experience deployment issues, try re-authenticating with the Firebase CLI or verifying your project secrets.

Thank you for being part of the Firebase Studio journey. Your prototypes and feedback have directly shaped Google’s AI tools, and we look forward to seeing what you build next in Antigravity!

Need help?
Section titled “Need help?”

File any migration bugs in our GitHub Issues.

Previous
Gemini CLI
Next
Workflows to Skills
About Google
Google Products
Privacy
Terms