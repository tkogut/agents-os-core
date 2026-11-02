# Workflows to Skills
Source URL: https://antigravity.google/docs/migration/workflows-to-skills

Workflows to skills migration2-0Antigravity AppGet StartedWorkflows to skills migration Antigravity App Get StartedAntigravity App
Get Started
Migrations
Workflows to Skills
Markdown
Migrate from workflows to skills
Section titled “Migrate from workflows to skills”

Learn how to migrate your legacy Antigravity workflows to modern, standard Agent skills.

Changes to workflows

We are accelerating bringing a more powerful, dynamic way to define and use workflows. Current workflows will stop working on October 19, 2026, and will be shortly followed with instructions on how to transition to the new workflows system. Existing workflows can also be migrated to Agent skills using the /migrate-workflows slash command to take advantage of progressive disclosure, directory-based asset bundling, and open ecosystem interoperability.

Why migrate to skills?
Section titled “Why migrate to skills?”

Workflows were originally introduced in the Antigravity IDE as single Markdown files designed for repeatable prompt sequences. While effective for simple instructions, monolithic files presented challenges as tasks grew in complexity.

In May 2026, Antigravity adopted the open industry standard for Agent Skills. Migrating to skills provides significant architectural and operational improvements:

Progressive context loading

Skills load only essential metadata (name and description) into the agent’s context upfront. Full instructions and reference materials are loaded on demand, preventing prompt bloat.

Multi-file directory bundling

Unlike single-file workflows, a skill is a directory bundle. You can co-locate executable helper scripts, documentation, sample schemas, and reference assets directly alongside SKILL.md.

Open ecosystem standard

Skills adhere to the cross-platform agent specification, enabling you to share and reuse skills across Antigravity IDE, Antigravity CLI, and other compliant agent tools.

Subagent integration

Skills can define specialized system prompts, specify tool requirements, and delegate subtasks to custom subagents directly from the skill bundle.

Comparison: Workflows and skills
Section titled “Comparison: Workflows and skills”
Specification
Proprietary Antigravity format
Open Agent Skills Standard (agentskills.io)
Structure
Single standalone .md file
Directory bundle (<skill-name>/SKILL.md + assets)
Workspace Path
.agents/workflows/<name>.md
.agents/skills/<name>/SKILL.md
Global Path
~/.gemini/config/workflows/<name>.md
~/.gemini/config/skills/<name>/SKILL.md
Context Loading
Entire file loaded into prompt
Progressive: Metadata indexed upfront; body loaded on demand
Bundled Assets
Not supported (everything must fit in one prompt)
Supported (scripts/, references/, examples/)
Slash Commands
Supported (/<workflow-name>)
Supported (/<skill-name>)
Autonomous Discovery
Supported
Supported (enhanced semantic matching using description)
File Size Limit
12,000 characters
Unrestricted bundle; modular multi-file architecture
Automatic migration
Section titled “Automatic migration”

Antigravity provides an automated migration command that discovers your existing workflows and converts them to skill directory bundles.

Using /migrate-workflows
Section titled “Using /migrate-workflows”

Complete the following steps to automatically migrate your workflows:

Open the Antigravity App.
Run the migration command:
/migrate-workflows
The agent performs the following actions:
Scans both global (~/.gemini/config/workflows/) and workspace-level (.agents/workflows/) directories.
Parses each workflow’s YAML frontmatter and body.
Scaffolds .agents/skills/<workflow-name>/SKILL.md with compliant metadata.
Archives original workflow files by appending .bak (for example, deploy.md becomes deploy.md.bak).
Immediately activates the new skills for slash commands and autonomous agent usage.
Manual migration guide
Section titled “Manual migration guide”

If you prefer to migrate your workflows manually or want to refactor monolithic prompts into modular skill packages, follow these steps:

Create the skill directory
Section titled “Create the skill directory”

In your workspace or global configuration directory, create a new folder named after your workflow under skills/:

Workspace Skill
Global Skill
mkdir -p .agents/skills/deploy-staging
Create and populate SKILL.md
Section titled “Create and populate SKILL.md”

Move your existing workflow Markdown file to SKILL.md inside the new folder:

mv .agents/workflows/deploy-staging.md .agents/skills/deploy-staging/SKILL.md
Standardize the YAML frontmatter
Section titled “Standardize the YAML frontmatter”

Ensure your SKILL.md begins with the standard name and description frontmatter fields. The description should clearly explain what the skill does and when the agent should use it:

---
name: deploy-staging
description: Deploys the current project build to the staging preview environment on App Engine. Use when testing staging releases or verifying PR previews.
---

# Deploy Staging

Follow these instructions to deploy the current build to staging...
(Optional) Extract scripts and resources
Section titled “(Optional) Extract scripts and resources”

If your workflow contains embedded scripts, code snippets, or lengthy reference documentation, extract them into dedicated subdirectories to keep SKILL.md lean:

.agents/skills/deploy-staging/
├── SKILL.md
├── scripts/
│   └── deploy.sh
└── references/
    └── staging-endpoints.json

In SKILL.md, instruct the agent to run or inspect those files when needed rather than duplicating them in the prompt.

Verify the migrated skill
Section titled “Verify the migrated skill”

Invoke the skill directly in the Antigravity App:

/deploy-staging

The agent loads the skill metadata and executes the steps.

Before and after migration example
Section titled “Before and after migration example”
Before: Legacy monolithic workflow
Section titled “Before: Legacy monolithic workflow”
---
name: build-and-test
description: Run test suites and verify build
---

Run the following checks sequentially:
1. First run `npm run check` to verify TypeScript and template integrity.
2. Next execute `npm run test` for unit tests.
3. If tests pass, run `npm run build` and report the generated bundle size.
After: Modular agent skill package
Section titled “After: Modular agent skill package”
.agents/skills/build-and-test/
├── SKILL.md
└── scripts/
    └── verify-bundle.js
---
name: build-and-test
description: Runs full validation suite including TypeScript checks, unit tests, and production build verification. Use before submitting changes.
---

# Build and Test Suite

Execute the project verification pipeline:

1. **Type & Template Diagnostics**:
   ```bash
   npm run check
   ```

2. **Unit Tests**:
   ```bash
   npm run test
   ```

3. **Production Build & Bundle Size Analysis**:
   ```bash
   npm run build
   node scripts/verify-bundle.js
   ```
Frequently asked questions
Section titled “Frequently asked questions”
Will my workflows stop working immediately?
Section titled “Will my workflows stop working immediately?”

No. Current workflows remain operational in Antigravity until October 19, 2026. We are accelerating bringing a more powerful, dynamic way to define and use workflows, and will follow up shortly with instructions on how to transition to the new workflows system. After October 19, 2026, legacy workflow directories are no longer indexed or executable using slash commands.

Can I still invoke my migrated skills using slash commands?
Section titled “Can I still invoke my migrated skills using slash commands?”

Yes. You can invoke any skill located in .agents/skills/<name>/ or ~/.gemini/config/skills/<name>/ by typing /<name> in chat, just like legacy workflows.

What happens if I have both a workflow and a skill with the same name?
Section titled “What happens if I have both a workflow and a skill with the same name?”

Skills take precedence over legacy workflows. If both .agents/skills/deploy/ and .agents/workflows/deploy.md exist, Antigravity executes the skill.

Where should I put global skills?
Section titled “Where should I put global skills?”

Place global skills in ~/.gemini/config/skills/<skill-name>/SKILL.md to make them accessible across all your workspaces.

Related documentation
Section titled “Related documentation”

Explore the following resources to learn more:

Agent skills overview: Full guide on creating, configuring, and organizing skills.
Customizing agent rules: Learn how to define persistent workspace and global rules.
Antigravity CLI plugins and skills: Manage skills in the Antigravity CLI.
Previous
Firebase Studio
Next
Plans
About Google
Google Products
Privacy
Terms