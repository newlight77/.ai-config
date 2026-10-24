# Agent Workflow

Shared workflow for AI coding assistants (Cursor, Claude Code, and similar) in every repository of the workspace. **Start from** the workspace `AGENTS.md` (read order for AI tools). Generic rules, skills, and hooks live in `.ai-config/`; the product and the Shipdeck platform add their own `.ai-config/` layer; each tool's own plumbing sits in `.cursor/` and `.claude/` at the workspace root.

## Mode Strategy

| Mode | Use when |
|------|----------|
| **Ask** | Explore codebase, understand architecture, answer questions (read-only) |
| **Plan** | Non-trivial tasks (3+ steps), architectural decisions, unclear scope |
| **Agent** | Execute implementation after plan is approved |

**Flow:** Ask → Plan → Agent for complex tasks.

## Before Implementation

1. **Inspect first** — No speculation; explore repo before making claims
2. **Plan non-trivial work** — Use Plan mode for 3+ steps or multi-file changes
3. **Read relevant skills** — Consult `.ai-config/skills/generic-skills.md`, then the index of the repository you work in (`kapita/.ai-config/skills/kapita-skills.md` `shipdeck/.ai-config/skills/shipdeck-skills.md` or `shipdeck-enabler/.ai-config/skills/enabler-skills.md`); load the skill file for your task type

## During Implementation

- **Composer hooks** — Hooks registered in `.cursor/hooks.json` (Claude Code: `.claude/settings.json`) inject policy at **session start** (architecture, testing layers, Robot vocabulary, evidence checkpoints, **commit message convention**) and remind about **business-domain Robot** wording after **Write** to `testing/e2e/backend/**/*.robot`. After **Write/StrReplace** of backend, web, or mobile source files, hooks **track affected packages for lint**; the **stop** hook lists `make lint-package` commands to run before ending the turn. See `.ai-config/skills/backend.md`, `web.md`, and `mobile.md` § Lint before finishing.
- **Minimal diffs** — Focused changes; avoid unrelated refactors
- **Subagents** — Offload exploration or parallel analysis via subagents when helpful
- **Verify before done** — Run tests, check logs; prove it works
- **Figma MCP** — Design work (wireframes, mockups, FigJam flows, design-to-code) uses the `figma` MCP server declared in `.mcp.json` (Claude Code) and `.cursor/mcp.json` (Cursor). It uses OAuth: authorize once interactively (`/mcp` in Claude Code, MCP settings in Cursor); no tokens are stored in a repository. Follow `.ai-config/skills/figma-design.md`.
- **Agent shell** — Use non-interactive commands (`/bin/cp -f` for forced copies on macOS; see `.ai-config/skills/shell.md`)

## Before Commit

- **Evidence Template** — Complete per change (`.ai-config/skills/evidence.md`)
- **Commit messages** — Conventional Commits + domain scope: `type(domain/context)/area: summary`, then body after a blank line (`area` is defined by the project; Kapita: `backend` | `web` | `mobile` | `testing` | `docs` | `cursor`). Small atomic commits per repository and per step; no push unless asked. Spec and examples: `.ai-config/hooks/session-context.md` § Commit messages.
- **Checkpoints** — Run `make build`, `make test-*`, `make format`, `make lint`, `make test-regression`
- **Robot E2E** — When adding or changing `testing/e2e/backend/*.robot`, follow `.ai-config/skills/testing.md`: business vocabulary in test cases and scenario docs; technical terms only in libraries and resource keyword implementations.
- **Fail-safe** — If constraints cannot be met, stop and ask for guidance

## Definition of Done

A change is done only when all items are satisfied:

- Requirements clarified and accepted
- Architecture rules respected (atomic hexagonal, context boundaries)
- Automated tests added or updated
- CI gates pass (build, lint, tests)
- Robot Framework tests updated when user-facing behavior changes
- Documentation updated if behavior or contracts changed
- Observability/logging updated for new flows
- Release notes or migration steps added if needed

## AI prompting checklist

When authoring prompts for agents, include:

- Requirement and acceptance criteria
- Target context; avoid cross-context changes unless required
- Tests by type (unit / use case / feature / UI / sanity / Robot as applicable)
- Evidence template completion before commit
- Minimal diffs
- Validation steps, or an explicit note when validation is blocked

## Task Tracking

- Plan → `tasks/todo.md` with checkable items
- Lessons → `tasks/lessons.md` after corrections
