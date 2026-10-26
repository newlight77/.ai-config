# Generic Skills Index

**When to use:** Pick the relevant skill file for your task. These skills are project-neutral engineering practice shared by every repository of the workspace. Product skills are indexed in `kapita/.ai-config/skills/kapita-skills.md`; tool and platform skills, including the build site and its enabler tubes, in `shipdeck/.ai-config/skills/shipdeck-skills.md`.

## Hierarchy

1. **Workspace `AGENTS.md`** – Entry point: read order for rules, workflow, skills, canonical docs
2. **Rules** (`.ai-config/rules/generic-rules.md`, then the repository's own rules) – Mandatory
3. **Workflow** (`.ai-config/workflow.md`) – Mode strategy, evidence, checkpoints, hooks
4. **Skills** (below, then the repository's index) – Context-dependent
5. **Canonical** (`.ai-config/canonical.md`) – Conflict resolution

**Triggers:** match the prompt's keywords against the *Triggers* column and read only the matching skill file(s); read nothing else unless the task widens.

## Skill Index

| Task type | Triggers (prompt keywords) | Skill file |
|-----------|---------|------------|
| Architecture, hexagons, vertical slices, atomic hexagonal layout | hexagon, port, adapter, bounded context, new context, vertical slice, layout | `architecture.md` |
| Method: triple loop (BSDD, ASDD, TDD), picking and delivering a spec | spec, SDD, BSDD, ASDD, triple loop, queue, story | `spec-driven.md` |
| Backend (Python, FastAPI, DB) | python, fastapi, sqlalchemy, poetry, ruff, mypy, migration, bff, endpoint | `backend.md` |
| Frontend web (React, TS, Tailwind) | react, tsx, tailwind, vite, vitest, eslint, pnpm | `web.md` |
| Frontend mobile (Flutter, Dart) | flutter, dart, widget, analyze | `mobile.md` |
| **Lint before finish** (backend ruff/mypy, web eslint/type-check/build, mobile analyze) | lint, type-check, ruff, mypy, eslint, analyze, before finishing | `backend.md`, `web.md`, `mobile.md` § Lint before finishing; enforced by `.ai-config/hooks/post-tool.py` + `stop-lint-reminder.py` |
| UI components, design tokens, styling, harmonising pages | design system, token, style, css, harmonise, page, banner, button | `design-system.md` |
| **Figma design** (wireframes, mockups, FigJam flows, Figma MCP, Code Connect, design-to-code) | figma, figjam, mockup, wireframe, code connect, design-to-code | `figma-design.md` |
| **React component design** (props/variants, composition, a11y, stories, Figma → React) | component props, variants, composition, a11y, storybook | `react-design.md` |
| Tests, coverage, Robot Framework | test, coverage, robot, e2e, vitest, pytest, use case test, feature test | `testing.md` |
| **New web context / app package** (Vitest ESM, test router) | vitest config, test router, new web package | `testing.md` § *Web frontend Vitest conventions* + `architecture.md` § *New web context scaffold* |
| Logging, tracing, analytics hygiene, E2E debug | log, trace, telemetry, correlation, analytics, debug id | `observability.md` |
| Refactoring, extraction, migrations | refactor, extract, rename, move, migrate, clean up | `refactoring.md` |
| Agent shell commands, file copies, non-interactive terminals | cp, shell, terminal, non-interactive, overwrite prompt | `shell.md` |
| Repo `scripts/`, Python-first tooling, make timing helpers | scripts/, make timing, python script, utility | `scripts.md` |
| Docs, API contracts, Robot E2E doc touchpoints | docs, readme, api contract, adr, document | `documentation.md` |
| **Evidence Template**, commit readiness, commit message shape | evidence, commit, commit message, ready to commit | `evidence.md` |
| Kubernetes / k3s as code (kubectl, Sealed Secrets, Helm, Argo CD, Ansible) | kubectl, k3s, helm, argo, sealed secret, ansible | `kubernetes-cluster.md` (concrete environment: `shipdeck-infra-skills.md`) |
| **Deep bug-finding** (explicit user request; scan recent commits for critical bugs) | find bugs, critical bugs, scan commits, audit | `bug-finding.md` |
