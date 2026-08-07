# AGENTS-OS Task Router (v6.5-Swarm)

> This file is the ENTRY POINT for all agent operations.
> It routes tasks to domain-specific knowledge modules.
> DO NOT add domain knowledge here — keep this file lean.

## Role Dispatch

| Trigger | Route To | Role |
|---|---|---|
| New issue / bug report | `.agents/agents-pipeline.md` | Coordinator |
| Implementation task | `.agents/agents-pipeline.md` | Builder |
| Code review / QA | `.agents/agents-qa.md` | Auditor |
| UI/UX changes | `.agents/agents-ux.md` | Builder |
| Architecture decisions | `.agents/specs/` | Coordinator |
| Skill management | `global_skills/` | Coordinator |

## Domain Modules
- **Pipeline**: `.agents/agents-pipeline.md` — SDLC, branching, PR workflow
- **QA**: `.agents/agents-qa.md` — Testing, linting, review gates
- **UX**: `.agents/agents-ux.md` — Design system, visual proof, mockups

## Quick Commands
- `/om-setup-agent-pipeline` — Initialize SDLC for a new project
- `/om-auto-fix-issue` — Auto-triage and fix a bug
- `/om-auto-create-pr` — Create PR from current worktree
- `/om-auto-qa-pr` — Run QA gate on a PR

## Context Budget
- Max 3 domain modules loaded per session
- Router file stays under 100 lines
- Use `@skill-name` to invoke skills on-demand
