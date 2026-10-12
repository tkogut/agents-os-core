# Enterprise overview
Source URL: https://antigravity.google/docs/enterprise

Get Started
Resources
Enterprise overview
Markdown
Antigravity in Gemini Enterprise
Section titled “Antigravity in Gemini Enterprise”

To deploy Google Antigravity using models hosted directly within your organization’s Google Cloud infrastructure, you can integrate with Gemini Enterprise. Every session runs under Google Cloud’s enterprise security controls, data residency guarantees, and the Google Cloud Terms of Service.

Supported products: Antigravity 2.0 Antigravity CLI Visual Studio Code Visual Studio JetBrains (Preview) Zed (Preview) Xcode (Preview)

Note

Enterprise integration is supported for Antigravity 2.0, Antigravity CLI, and Antigravity IDE extensions. Antigravity IDE (standalone) is not supported for enterprise deployments, and legacy Gemini Code Assist IDE extensions support only first-party Gemini models.

Developer sign-in and models
Sign in with Google Cloud SSO, Workforce Identity Federation (WIF), or ADC and select enterprise models.
Administrator and network setup
Provision a Google Cloud project, enable third-party models, and configure firewall and mTLS allowlists.
Overview and key benefits
Section titled “Overview and key benefits”

You can connect Antigravity to Gemini Enterprise in two ways:

Google Cloud project and API: Connect directly using a Google Cloud project with an invoiced Cloud Billing account and the roles/discoveryengine.agentspaceUser Identity and Access Management (IAM) role for consumption-based billing.
Gemini Enterprise license: Connect with your Gemini Enterprise Standard or Gemini Enterprise Plus seat license to get access to included first-party quotas, managed overages, and centralized administrative controls across Antigravity 2.0, Antigravity CLI (agy), and Antigravity IDE extensions. No separate per-user Antigravity license is required.

By connecting Google Antigravity to your Google Cloud project, your organization gains:

Enterprise governance

Operates under your existing Google Cloud Terms of Service with centralized administrative controls.

Data residency and security

Satisfies private networking (VPC Service Controls). Regional data residency constraints apply to first-party Gemini models; third-party model inference runs in global, us, and eu locations (in-country regions are not supported; see Anthropic’s Supported countries and regions).

Sign in and license selection
Section titled “Sign in and license selection”

After installing Antigravity 2.0, the Antigravity CLI (agy), or a supported IDE extension, choose your organization’s authentication method to connect to Gemini Enterprise:

Google Cloud SSO
BYOID and WIF
ADC (Headless)
Google Cloud SSO
Sign-in workflow
Section titled “Sign-in workflow”

Google Antigravity uses a single sign-on (SSO) flow that automatically detects your assigned license tier:

Launch Antigravity 2.0, run agy (or /login) in the Antigravity CLI, or open your IDE extension.
Select Sign in to open the browser authentication flow.
Choose Business account (subject to the Google Cloud Terms of Service).
Select Continue with Google Cloud and complete authentication in your browser.
In the License Selector, confirm the Google Cloud project linked to your license and select it. Alternatively, select Other to self-assign a license by entering your project ID and selecting a location (global, us, or eu; saved to ~/.gemini/antigravity-cli/settings.json in the CLI), or pass agy --project PROJECT_ID when launching the CLI.

Note

Data-sharing and project logging notice: Your customer telemetry and model interactions are logged directly to the Google Cloud project corresponding to the license you select. You can maintain one license per project and location.

Supported models in Gemini Enterprise
Section titled “Supported models in Gemini Enterprise”

Antigravity in Gemini Enterprise supports included first-party Gemini models and administrator-enabled third-party partner models:

Model	CLI / API Identifier	Enterprise
Gemini 3.8 Flash	gemini-3.8-flash	✅
Gemini 3.7 Flash	gemini-3.7-flash	✅
Gemini 3.6 Flash	gemini-3.6-flash	✅
Gemini 3.1 Pro	gemini-3.1-pro-preview	✅
Claude Sonnet 5.5 (thinking)	claude-sonnet-5-5-<level>*	✅**
Claude Opus 5.5 (thinking)	claude-opus-5-5-<level>*	✅**
Claude Sonnet 4.6 (thinking)	—	❌
Claude Opus 4.6 (thinking)	—	❌
GPT-OSS-120b	—	❌

* Available at four thinking levels (<level>): low, medium (default), high, and max (for example, claude-opus-5-5-high or claude-sonnet-5-5-max).

** Third-party partner models require administrator opt-in in the Google Cloud Console and are billed by token consumption. First-party Gemini models are enabled by default and draw from pooled edition seat credits ($10/month Standard, $15/month Plus).

Selecting models and thinking levels
Section titled “Selecting models and thinking levels”

Once enabled for your project, models appear in your client shortly after your administrator enables them:

Antigravity 2.0 and IDE extensions: Open the Model picker in the chat composer and select your preferred model (third-party models appear under Other Models). Anthropic Claude Opus 5.5 and Anthropic Claude Sonnet 5.5 are available at four thinking levels—Low, Medium (default), High, and Max—and each level appears as a separate entry in the model picker (for example, Claude Opus 5.5 (High)). Higher levels give the model more room to reason on complex tasks, but use more tokens.
Antigravity CLI (agy): Start a session with --model or switch mid-session with the /model slash command:
agy --model claude-opus-5-5-medium
agy --model claude-sonnet-5-5-medium
You can also specify a base model ID and use the --effort flag (or /effort mid-session, requires agy v1.2.11 or later) to set the reasoning level (low, medium, high, max):
agy --model claude-opus-5-5-medium --effort high
agy --model claude-sonnet-5-5-medium --effort max
Architectural transparency: Hybrid execution
Section titled “Architectural transparency: Hybrid execution”

When you select Anthropic Claude Opus 5.5 or Anthropic Claude Sonnet 5.5 in Antigravity, your selected third-party model executes all primary reasoning, planning, tool orchestration, and code generation turns.

Antigravity uses a hybrid execution architecture: lightweight first-party Gemini models continue to run in the background to handle high-frequency client-side coordination—such as context management and summaries. These background models consume first-party tokens, which can incur charges.

Autonomous tool permissions and human-in-the-loop controls
Section titled “Autonomous tool permissions and human-in-the-loop controls”

Autonomous tool execution in Antigravity supports human-in-the-loop confirmation when using either first-party Gemini models or administrator-enabled third-party Anthropic models (claude-opus-5-5 and claude-sonnet-5-5):

Antigravity 2.0: Keep Default (isolated terminal sandbox) or Request Review enabled in Settings > General > Permission Settings so unsandboxed shell commands, external file modifications, and MCP tool calls require explicit developer approval. Use unrestricted auto-approval (Turbo / Always proceed) only in isolated development containers or disposable branches.
Antigravity CLI (agy): Keep interactive tool permissions and --sandbox=true enabled (seatbelt on macOS, bubblewrap on Linux), or use read-only plan mode (--mode plan) before approving edits. Configure policies with /permissions or /config.
Agent permissions
Configure allow, ask, and deny rules and permission presets in Antigravity 2.0 and the CLI.
Terminal sandbox
Learn how OS-level sandboxing isolates shell commands and network access.
Administrator setup guide
Section titled “Administrator setup guide”
Gemini Enterprise subscription setup
Section titled “Gemini Enterprise subscription setup”

To set up Gemini Enterprise subscriptions, follow the official Google Cloud onboarding guide.

Gemini Enterprise Documentation
Google Cloud project and API setup
Section titled “Google Cloud project and API setup”

New to Gemini Enterprise Agent Platform?

If you are a new customer connecting via API, you will need an API key to authenticate. Visit the API Key Quickstart Guide to create your key first.

Complete the following steps to provision your Google Cloud project and enable API access:

Select or create a Google Cloud project: Select an existing project or create a dedicated project for your team’s Antigravity workloads.

Note

Project switching note: To switch to a different Google Cloud project or location, log out of the Antigravity CLI or Antigravity 2.0, then log back in to select your new project or region.

Go to GCP Project Selector

Verify Cloud Billing: Ensure that Cloud Billing is active for your selected Google Cloud project. You can inspect your project’s billing status in the Google Cloud Console.

Open Google Cloud Billing Console

Enable the API: Enable the Gemini Enterprise API (aiplatform.googleapis.com) to allow Antigravity clients to connect to your project’s model endpoints.

Enable API in Cloud Console

Enable third-party partner models (optional): To allow developers to use Anthropic Claude Opus 5.5 or Anthropic Claude Sonnet 5.5, enable third-party models in Gemini Enterprise > Settings > AI developer tools in the Google Cloud Console.

Regional endpoints and network allowlists
Section titled “Regional endpoints and network allowlists”
Regional endpoints
Section titled “Regional endpoints”

Antigravity CLI, Antigravity 2.0, and IDE extensions support multi-region deployment endpoints to satisfy regional data residency requirements:

Region	Location ID	Supported capabilities
Global	global	Text generation, code inference, multimodal, image generation
US (Multi-region)	us	Text generation, code inference, multimodal
EU (Multi-region)	eu	Text generation, code inference, multimodal

Note

Image generation capabilities are currently available exclusively on global deployment endpoints.

For full endpoint specifications, consult the Deployment endpoints documentation.

Network allowlists and mTLS endpoints
Section titled “Network allowlists and mTLS endpoints”

If your organization restricts outbound developer traffic using corporate firewalls, proxies, or context-aware access rules, allowlist the following endpoints over TCP port 443 for Antigravity 2.0, Antigravity CLI (agy), and Antigravity for IDEs:

Service and protocol	Allowed hostnames (TCP port 443)
AI Developer Tools Orchestration (Standard HTTPS)	businessaicode.googleapis.com
AI Developer Tools Orchestration (Mutual TLS)	businessaicode.mtls.googleapis.com
Discovery Engine — Global, US, EU (Standard HTTPS)	discoveryengine.googleapis.com
us-discoveryengine.googleapis.com
eu-discoveryengine.googleapis.com
Discovery Engine — Global, US, EU (Mutual TLS)	discoveryengine.mtls.googleapis.com
us-discoveryengine.mtls.googleapis.com
eu-discoveryengine.mtls.googleapis.com
Security and governance
Section titled “Security and governance”

Request and response logging

Audit model interactions and maintain enterprise compliance records for your Gemini Enterprise instance. Learn more

VPC Service Controls (VPC-SC)

Enforce private networking security perimeters by adding the Gemini Enterprise API (aiplatform.googleapis.com) to your VPC-SC perimeter. Learn more

Troubleshooting and diagnostics
Section titled “Troubleshooting and diagnostics”
Common sign-in and license issues
Section titled “Common sign-in and license issues”

Review the following solutions for common sign-in and license issues:

No licenses appear during setup: Licenses are assigned by your organization’s Google Cloud administrator. If the License Selector is empty, contact your administrator to ensure your account has been granted access to a Gemini Enterprise Standard or Plus license.
Missing BYOID sign-in option: Ensure you are running the latest release of Antigravity 2.0, the Antigravity CLI, or your IDE extension, as enterprise authentication and BYOID support are included natively in all recent releases.
Important API provisioning advisory
Section titled “Important API provisioning advisory”

Caution

Enable required APIs before purchasing licenses: New Gemini Enterprise license purchases can fail or fail to provision if the Gemini Enterprise API (aiplatform.googleapis.com) is not enabled first. Enable the API in the Google Cloud Console and wait approximately five minutes for propagation before completing license purchases.

Sharing diagnostics with support
Section titled “Sharing diagnostics with support”

When contacting Google Cloud Support, include the diagnostic log file from your most recent session:

Antigravity CLI (Linux and macOS):
~/.gemini/antigravity-cli/cli.log
Antigravity 2.0 (macOS):
~/Library/Logs/Antigravity/language_server.log
What’s next
Section titled “What’s next”

Explore the following resources to learn more:

Explore supported model architectures in the Models guide.
Learn more about enterprise privacy and compliance in Security and governance.
Check the Antigravity CLI reference for headless automation commands.
Previous
Plans and AI credits
Next
Firebase Studio migration
About Google
Google Products
Privacy
Terms