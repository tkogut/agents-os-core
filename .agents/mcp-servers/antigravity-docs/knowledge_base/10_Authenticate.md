# Authenticate
Source URL: https://antigravity.google/docs/install

Authenticate2-0Antigravity AppGet StartedAuthenticate Antigravity App Get StartedAntigravity AppAntigravity CLIIDE Extensions
Get Started
Authenticate
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
IDE extensions
Authenticate
Section titled “Authenticate”

Antigravity uses a unified authentication layer across Antigravity App, Antigravity CLI, Antigravity for IDEs, and the Antigravity SDK. Signing in on one local surface shares your credentials across your local environment.

Need to install Antigravity first?

Follow the Quickstart to download and install Antigravity App, Antigravity CLI, an IDE Extension, or the Antigravity SDK.

Sign in by surface
Section titled “Sign in by surface”

Select your surface below to authenticate your account, switch credentials, or configure headless and enterprise environments.

Antigravity App
Antigravity CLI
For IDEs
Antigravity SDK
Personal Google Account
Section titled “Personal Google Account”
Launch Antigravity App.
Click Sign in to open the browser authentication flow.
Complete the browser-based OAuth flow using your personal Google Account (Free, Pro, or Ultra plan).
Once authenticated, the browser redirects back to Antigravity App and initializes your workspace.
Gemini Enterprise & Google Cloud Account
Section titled “Gemini Enterprise & Google Cloud Account”

Google Antigravity uses a single sign-on (SSO) flow for corporate business accounts and automatically detects your assigned Gemini Enterprise license tier:

Start Antigravity App and select Sign in to open the browser authentication flow.
Choose Business account (subject to the Google Cloud Terms of Service).
Select Continue with Google Cloud (or select Advanced WIF Configuration and enter your organization’s WIF Configuration String for Bring Your Own Identity / Workforce Identity Federation).
Complete authentication in your browser.
Once authenticated, the License Selector displays your assigned licenses.
Confirm the project linked to your license and select it. Alternatively, select Other to self-assign a license by entering your Google Cloud Project ID and selecting a location (global, us, or eu).

Note

Project Switching & Governance: To switch to a different Google Cloud project or location, log out of Antigravity App and log back in to select your new project or region. Ensure the Gemini Enterprise API (aiplatform.googleapis.com) is enabled in your project. See the Enterprise guide for full administrator setup, BYOID/WIF, and VPC Service Controls details.

Application Default Credentials (ADC)
Section titled “Application Default Credentials (ADC)”

For automated or headless workflows, you can authenticate Antigravity App using Google Cloud Application Default Credentials:

Generate local Application Default Credentials for your project:
gcloud auth application-default login --project {GCP_PROJECT}
Enable ADC in Antigravity App using either option:
Launch from a terminal with export AGY_ADC_AUTH=true.
Or enable the enableAdc user setting in ~/.gemini/config/config.json:
{
  "userSettings": {
    "enableAdc": true
  }
}
Next steps
Section titled “Next steps”
GET STARTED
Quickstart

Install Antigravity and complete your first end-to-end agent workflow.

MODELS
Choose a model

Configure Gemini 4 Argon, Gemini 3.1 Pro, Gemini 3.8 Flash, Claude, and reasoning effort.

CLOUD & APIS
Build with Google

Connect Vertex AI, Cloud Run, Firebase, and Google Cloud MCP tools.

Previous
Quickstart
Next
Choose a model
About Google
Google Products
Privacy
Terms