# /learn
Source URL: https://antigravity.google/docs/commands/learn

Learn command (/learn)2-0Antigravity AppFeaturesLearn command (/learn) Antigravity App FeaturesAntigravity AppAntigravity CLIAntigravity IDE
Features
Slash commands
/learn
Markdown
AVAILABLE ON:
Antigravity App
Antigravity CLI
Antigravity IDE
Learn command (/learn)
Section titled “Learn command (/learn)”

Capture what the agent learned in this session, such as a correction you made, a constraint it kept missing, or a multi-step setup that finally worked, and persist it as a rule or skill so future sessions benefit automatically.

Overview
Section titled “Overview”

Agents don’t remember conversations. If you spend twenty minutes teaching the agent that your repository’s tests must run with a particular flag, that knowledge disappears when the conversation ends, unless it’s written down as a customization.

The /learn command asks the agent to reflect on recent interactions and propose durable changes:

Finds the lesson: the agent analyzes your recent messages for explicit corrections (“no,” “instead,” “that failed”), compares failed attempts with the eventual fix, and isolates the pivotal change and its root cause.
Classifies it: the agent decides whether the lesson is a rule (a guardrail, constraint, or formatting invariant) or a skill (a reusable multi-step procedure, flag combination, or cheat sheet).
Prefers updates over new files: if an existing rule or skill was used but failed, was outdated, or missed an edge case, the agent updates it rather than creating a duplicate.
Proposes before writing: the agent never edits configuration files immediately. It drafts a proposal artifact for your review first.

If the session didn’t reveal anything reusable, the agent says so and exits without proposing changes.

Run /learn
Section titled “Run /learn”

You can run /learn with or without a focus.

Reflect on the recent session
Section titled “Reflect on the recent session”

After correcting the agent or working through a tricky setup, type the bare command:

/learn

The agent reviews the recent conversation, identifies what to retain, and proposes rules or skills.

Teach a specific lesson
Section titled “Teach a specific lesson”

To point the agent at exactly what to capture, add an instruction:

/learn always run vitest with --pool=forks in this repo
/learn save the database transaction retry pattern we just used as a project rule

The agent still classifies and scopes the lesson, but skips the discovery step.

Review and approve the proposal
Section titled “Review and approve the proposal”

/learn follows a mandatory proposal workflow:

Schema check: the agent inspects your existing rules and skills, or the built-in customizations guide, so new files match the exact frontmatter and directory conventions your project already uses.
Proposal artifact: the agent creates a learning_proposal.md artifact that states its classification (rule or skill), the rationale, and the precise text additions or diffs it intends to make.
Your review: the artifact requests feedback. Add inline comments to adjust the scope, wording, or location.
Apply: only after you explicitly approve does the agent create or update the files.
Where /learn saves knowledge
Section titled “Where /learn saves knowledge”

/learn writes to the same locations that Antigravity discovers customizations from. The agent chooses the scope, workspace or global, based on whether the lesson is specific to this project or applies everywhere, and confirms the location in the proposal.

Rule
AGENTS.md or GEMINI.md in the workspace folder or .agents/, or .agents/rules/<name>.md
~/.gemini/AGENTS.md, ~/.gemini/GEMINI.md, ~/.gemini/config/AGENTS.md, ~/.gemini/config/GEMINI.md, or ~/.gemini/config/rules/<name>.md
Skill
.agents/skills/<name>/SKILL.md
~/.gemini/config/skills/<name>/SKILL.md

Note

Files inside a rules/ directory require YAML frontmatter with a valid trigger. AGENTS.md and GEMINI.md files don’t use frontmatter and are always active. For the full discovery rules and precedence, refer to the Rules guide.

Rule or skill?
Section titled “Rule or skill?”

The agent uses the same guidance you’d use when writing customizations by hand:

Rule: “Always use zod for validation,” “Never import internal/ across packages,” “Commit messages must follow Conventional Commits.” Rules are short constraints the agent should keep in mind continuously or when a trigger matches.
Skill: “How to run database migrations,” “How to regenerate protobuf bindings and fix the three places they break.” Skills are procedures the agent loads on demand and can run as /<skill-name> slash commands.
Next steps
Section titled “Next steps”

Explore related documentation:

Rules: Learn how rules are discovered, scoped, and activated.
Agent skills: Learn the SKILL.md format and how skills become slash commands.
Plugins: Package rules and skills to share across projects and teams.
Slash commands overview: Browse every available slash command.
Previous
/grill-me
Next
/permissions
About Google
Google Products
Privacy
Terms