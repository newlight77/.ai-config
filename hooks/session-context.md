# Generic agent constraints (from `.ai-config` rules, skills, workflow)

Injected at **session start** by the hooks registered at the workspace root (`.cursor/hooks.json`, `.claude/settings.json`). This is the slim core: the implementation constraints (hexagonal layout, test shapes, Robot, lint, observability) are in `session-context-impl.md` and arrive with the first prompt that looks like code work. It **does not replace** the workspace `AGENTS.md`, the skill files or `docs/architecture/`; see `.ai-config/canonical.md` on conflict. Each repository adds its own session text (product: Kapita policy; tools and platform: Shipdeck rules).

**Read order:** workspace `AGENTS.md` → `.ai-config/rules/generic-rules.md` → rules of the repository you work in → `.ai-config/workflow.md` → skill indexes (`.ai-config/skills/generic-skills.md` + the repository's; match the **Triggers** column to the prompt, read only the matching skill file) → `.ai-config/canonical.md` for disputes.

## Workflow

- **Ask** → explore and answer (read-only). **Plan** → non-trivial work, unclear scope, architecture choices. **Agent** → implement after the plan is clear.
- **Inspect the repo** before claiming behavior; **minimal diffs**; no unrelated refactors.
- **Fail-safe:** if constraints cannot be met, stop and ask.

## Delegate to keep the main context small

- **Inline:** edits, short questions, sequential dependent steps, anything you will need the raw output of again.
- **`Explore` agent:** locating files, symbols or usages ("where is X defined", "who calls Y"); give a breadth (quick / medium / thorough).
- **Fork / general-purpose agent:** open-ended research, surveys across many files, log or test-output triage, independent sub-questions (launch them in parallel). Ask for a short, structured report.
- **`Plan` agent:** design of non-trivial changes before you edit.
- Never delegate understanding: brief agents with paths, symptoms and what you already ruled out.

## Shell and scripts

- **macOS copy:** use `/bin/cp -f` (not `cp -f`); agent terminals cannot answer `cp -i` prompts (`.ai-config/skills/shell.md`).
- **New utilities under `scripts/`:** Python (`python3 scripts/<name>.py`), with `scripts/tests/test_<name>.py` and `scripts/README.md` updated; shell only for thin Makefile glue, executable hooks, legacy helpers (`.ai-config/skills/scripts.md`).
- Use existing Makefile targets; never invent new ones.

## Before commit

Evidence Template (`.ai-config/skills/evidence.md`), then the checkpoints from the repository you changed: `make build`, `make test-*`, `make format`, `make lint`, `make test-regression`. Lint reminders for touched packages come from the post-tool and stop hooks.

## Commit messages (Conventional Commits + domain scope)

Subject (≤ ~72 chars): `type(domain/context)/area: imperative summary`

- **`type`:** `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`, `build`, …
- **`(domain/context)`:** bounded domain or slice, slash-separated when nested (e.g. `orders/checkout`).
- **`/area`:** where the change lands; the set is defined by the repository's session text (Kapita: `backend`, `web`, `mobile`, `testing`, `docs`, `cursor`).
- Short imperative summary, no trailing period. After a blank line, a body: what, why, risk/rollback.
- One small atomic commit per repository and per step. Never push, amend published commits or skip hooks unless asked.
- `docs`-only commits may use `docs(domain/context): …`.

Example: `feat(orders/checkout)/backend: add the refund use case`

## Canonical conflict order

1. `.ai-config/rules/generic-rules.md`, then the repository's own rules
2. `.ai-config/skills/*.md` and the repository's skills
3. `docs/architecture/1.atomic-hexagonal-architecture.md`
4. `docs/testing/Testing-Strategy.md`
