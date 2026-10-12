# Rules
Source URL: https://antigravity.google/docs/rules

Features
Extend
Skills
Rules
Markdown
AVAILABLE ON:
Antigravity 2.0
Antigravity CLI
Antigravity IDE
Rules
Section titled “Rules”

Rules are persistent instructions, coding standards, and architectural constraints that shape how Antigravity behaves in your codebase. Unlike chat prompts that apply to a single conversation, Antigravity automatically discovers rules from your filesystem and injects them into the agent’s context.

Tip

Rule vs. Skill: Write a rule for constraints and invariants (for example, “Always use zod for validation” or “Never import internal/ across packages”). Write a skill for multi-step workflows (for example, “How to run database migrations”).

Where rules are stored
Section titled “Where rules are stored”

Antigravity discovers rules across multiple scopes, listed below in order of precedence (highest to lowest). Rules are cumulative rather than replacement-based: Antigravity combines all discovered rules across global, workspace, and directory scopes into the prompt. When instructions conflict, more specific directory rules take priority.

Directory-scoped rules
Section titled “Directory-scoped rules”

You can place an AGENTS.md or GEMINI.md file—or a .agents/rules/ directory—in any subdirectory of your project. Whenever Antigravity reads or edits a file, it walks up the directory tree from that file’s folder to the workspace root, loading rules at each level:

<dir>/AGENTS.md or <dir>/GEMINI.md
<dir>/.agents/AGENTS.md or <dir>/.agents/GEMINI.md
<dir>/.agents/rules/*.md (and legacy <dir>/.agent/rules/*.md)
Global rules
Section titled “Global rules”

Global rules apply across all projects on your workstation:

Standalone global files (no frontmatter needed, always active): ~/.gemini/AGENTS.md, ~/.gemini/GEMINI.md, ~/.gemini/config/AGENTS.md, or ~/.gemini/config/GEMINI.md
Modular global rules (YAML frontmatter required): ~/.gemini/config/rules/*.md

Caution

Flat directory scanning: Antigravity scans only immediate .md children inside .agents/rules/ (such as .agents/rules/typescript.md). Antigravity ignores files nested in subdirectories (such as .agents/rules/frontend/react.md) unless you explicitly register them in .agents/rules.json.

YAML frontmatter and activation modes
Section titled “YAML frontmatter and activation modes”

Frontmatter requirements depend on the file type:

AGENTS.md and GEMINI.md do not use frontmatter. Antigravity treats its entire content as plain Markdown and keeps it continuously active (always_on) for its directory scope.
Every .md file inside rules/ must start with YAML frontmatter declaring a valid trigger.

Caution

Missing frontmatter or invalid trigger: If a file in .agents/rules/*.md omits frontmatter or specifies an unrecognized trigger value (such as camelCase alwaysOn or modelDecision), Antigravity silently discards the rule.

Supported frontmatter keys
Section titled “Supported frontmatter keys”

Rules in .agents/rules/ support the following YAML frontmatter keys:

---
trigger: model_decision       # Required: always_on | model_decision | glob | manual
description: "..."            # Required for model_decision; recommended for all rules
globs: "*.ts, *.tsx"          # Required for glob (singular `glob:` is also accepted)
---
Field	Type	Required	Description
trigger	string	Yes	Controls how and when the rule activates: model_decision, always_on, glob, or manual.
description	string	Required for model_decision	Concise summary of when the rule applies. Antigravity injects this summary into the prompt index for model_decision rules, and uses it as fallback context if an always_on rule exceeds the token budget.
globs (or glob)	string	Required for glob	Comma-separated file glob patterns (for example, "*.py, *_test.py"). Wrap patterns starting with * in quotes so YAML does not treat * as an alias anchor.
Activation modes
Section titled “Activation modes”

Configure the trigger key to control how and when a rule is loaded into context:

model_decision (best for detailed domain guides): Antigravity injects only the rule’s path and description upfront (progressive disclosure). The agent reads the full rule on demand when your task matches the description.

---
trigger: model_decision
description: "Apply these guidelines whenever writing or reviewing database migrations or SQL schema changes."
---

# Database Migration Rules

1. Never drop or rename a column in a single deployment; use an expand-and-contract migration.
2. Always add `CONCURRENTLY` when creating indexes on existing tables in PostgreSQL.

always_on (always active in scope): Antigravity injects the full content into the system prompt on every turn. Prefer placing always_on rules directly in AGENTS.md when you do not need frontmatter.

glob (file-pattern scoped): Automatically activates when the agent interacts with files matching any comma-separated pattern in globs:

---
trigger: glob
globs: "*.proto, **/*.pb.go"
description: "Protobuf schema design and backward-compatibility rules."
---

# Protobuf Conventions

* Never reuse a deleted field number; always mark both the field number and name as `reserved`.

manual (explicit @ mention only): Antigravity never loads these rules automatically. The agent injects the rule only when you explicitly @-mention it in chat (ideal for release checklists or audit rubrics).

Advanced features and limits
Section titled “Advanced features and limits”
File includes
Section titled “File includes”

Inside any rule file (AGENTS.md, GEMINI.md, or .agents/rules/*.md), Antigravity supports two distinct @ syntaxes for referencing files:

@[label](path): Inlines the target file’s contents directly into the rule before prompt evaluation and size-limit checks.
Path resolution: Antigravity resolves relative paths from the directory containing the rule file. Paths starting with ~/ expand to your user home directory.
Frontmatter stripping: If an included file contains YAML frontmatter, Antigravity strips the frontmatter and splices in only the Markdown body.
@filename: Does not inline file contents. Instead, it resolves the path (relative to the rule file, or as a workspace-relative/absolute path) and rewrites it to a canonical absolute workspace path (@/workspace/path) so the agent has an unambiguous file reference.
Follow our shared API design standards:
@[API Design Standards](../docs/api-standards.md)

When updating database models, check @src/db/schema.ts first.
Sharing rules across projects
Section titled “Sharing rules across projects”

To share rules stored outside .agents/rules/ or to include nested subdirectories of rules while preserving their YAML frontmatter and triggers, create .agents/rules.json:

{
  "inherits": [
    { "path": "../shared-config/.agents/rules.json" }
  ],
  "entries": [
    { "path": "../shared-rules", "exclude": ["deprecated_rules.md", "legacy/"] },
    { "path": "rules", "include_only": ["frontend/react.md"] }
  ]
}
Size limits and token budgets
Section titled “Size limits and token budgets”

To prevent rules from exhausting the context window, Antigravity enforces two limits:

24 KB (24,000 bytes) per-file limit: Antigravity truncates any single rule file that exceeds 24,000 bytes (after expanding @[label](path) includes).
20,000-token aggregate rules budget: All active global and always_on rules share a 20,000-token budget separate from the customization budget (plugins such as skills and MCP). If the total exceeds 20,000 tokens, Antigravity automatically demotes the largest rule files from inline text to lightweight pointers (- <path>: <description>), allowing the agent to read them on demand.
Configuration by surface
Section titled “Configuration by surface”

Select your surface below to configure global or workspace-specific rules:

Antigravity 2.0
Antigravity CLI
Antigravity IDE & Extensions
Antigravity 2.0
Managing rules in Antigravity 2.0
Section titled “Managing rules in Antigravity 2.0”

Follow these steps to create or manage rules in Antigravity 2.0:

Open the Customizations panel from the application menu or project settings.
Select the Rules tab.
Click + Global to create global rules, or + Workspace to create rules scoped to the active project.
Antigravity 2.0 file locations
Section titled “Antigravity 2.0 file locations”

Antigravity 2.0 loads rules from the following locations:

Workspace rules: AGENTS.md, GEMINI.md, or .agents/rules/*.md in your workspace root or any project subdirectory.
Global rules: ~/.gemini/AGENTS.md, ~/.gemini/GEMINI.md, or modular rules in ~/.gemini/config/rules/*.md.
Previous
Agent skills
Next
IDE workflows
About Google
Google Products
Privacy
Terms