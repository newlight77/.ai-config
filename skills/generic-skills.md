# Generic Skills Index

**When to use:** Pick the relevant skill file for your task. These skills are project-neutral engineering practice shared by every repository of the workspace. Product skills are indexed in `kapita/.ai-config/skills/kapita-skills.md`; tool and platform skills in `shipdeck/.ai-config/skills/shipdeck-skills.md`.

## Hierarchy

1. **Workspace `AGENTS.md`** – Entry point: read order for rules, workflow, skills, canonical docs
2. **Rules** (`.ai-config/rules/generic-rules.md`, then the repository's own rules) – Mandatory
3. **Workflow** (`.ai-config/workflow.md`) – Mode strategy, evidence, checkpoints, hooks
4. **Skills** (below, then the repository's index) – Context-dependent
5. **Canonical** (`.ai-config/canonical.md`) – Conflict resolution

## Skill Index

| Task type | Skill file |
|-----------|------------|
| Architecture, hexagons, vertical slices, atomic hexagonal layout | `architecture.md` |
| Method: triple loop (BSDD, ASDD, TDD), picking and delivering a spec | `spec-driven.md` |
| Backend (Python, FastAPI, DB) | `backend.md` |
| Frontend web (React, TS, Tailwind) | `web.md` |
| Frontend mobile (Flutter, Dart) | `mobile.md` |
| **Lint before finish** (backend ruff/mypy, web eslint/type-check/build, mobile analyze) | `backend.md`, `web.md`, `mobile.md` § Lint before finishing; enforced by `.ai-config/hooks/post-tool-lint-track.py` + `stop-lint-reminder.py` |
| UI components, design tokens, styling, harmonising pages | `design-system.md` |
| **Figma design** (wireframes, mockups, FigJam flows, Figma MCP, Code Connect, design-to-code) | `figma-design.md` |
| **React component design** (props/variants, composition, a11y, stories, Figma → React) | `react-design.md` |
| Tests, coverage, Robot Framework | `testing.md` |
| **New web context / app package** (Vitest ESM, test router) | `testing.md` § *Web frontend Vitest conventions* + `architecture.md` § *New web context scaffold* |
| Logging, tracing, analytics hygiene, E2E debug | `observability.md` |
| Refactoring, extraction, migrations | `refactoring.md` |
| Agent shell commands, file copies, non-interactive terminals | `shell.md` |
| Repo `scripts/`, Python-first tooling, make timing helpers | `scripts.md` |
| Docs, API contracts, Robot E2E doc touchpoints | `documentation.md` |
| **Evidence Template**, commit readiness, commit message shape | `evidence.md` |
| Kubernetes / k3s as code (kubectl, Sealed Secrets, Helm, Argo CD, Ansible) | `kubernetes-cluster.md` (concrete environment: `shipdeck-infra-skills.md`) |
| **Deep bug-finding** (explicit user request; scan recent commits for critical bugs) | `bug-finding.md` (+ `.ai-config/bug-finding-memories.md`) |
