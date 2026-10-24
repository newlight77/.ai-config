# Generic agent constraints (from `.ai-config` rules, skills, workflow)

This block is injected at **session start** by the hooks registered at the workspace root (`.cursor/hooks.json`, `.claude/settings.json`) so agent runs align with policy. It **does not replace** reading the workspace `AGENTS.md`, the skill files, or the project's `docs/architecture/` / `docs/testing/Testing-Strategy.md` — see `.ai-config/canonical.md` if anything conflicts. The repository you work in adds its own session text (product: Kapita policy; tools and platform: Shipdeck rules).

**Read order (summary):** workspace `AGENTS.md` → `.ai-config/rules/generic-rules.md` → the rules of the repository you work in → `.ai-config/workflow.md` → `.ai-config/skills/generic-skills.md` and that repository's skills index (pick skills) → `.ai-config/canonical.md` for disputes.

## Workflow

- **Ask** → explore and answer (read-only). **Plan** → non-trivial work, unclear scope, architecture choices. **Agent** → implement after the plan is clear.
- **Inspect the repo** before claiming behavior; avoid speculation.
- **Minimal diffs**; no unrelated refactors.
- **Fail-safe:** if constraints cannot be met, stop and ask for guidance.

## Agent shell commands

- **Forced copy on macOS:** use `/bin/cp -f` (not `cp -f`) so `cp -i` aliases do not prompt `overwrite …? (y/n)` — agent terminals cannot accept interactive input. See `.ai-config/skills/shell.md`.

## Repo scripts (Python-first)

- **New utilities under `scripts/`:** prefer **Python** (`python3 scripts/<name>.py`); add `scripts/tests/test_<name>.py` for non-trivial logic; update `scripts/README.md`.
- **Make timing:** `test` / `test-*`, `format` / `format-*`, `lint` / `lint-*` targets print durations through the project's make timing helper (see `.ai-config/skills/scripts.md`).
- **Shell exceptions:** thin Makefile glue, required executable hooks, legacy helpers.

## Hexagonal architecture (new context / vertical slice)

- **Isolate the domain**; adapters implement **ports**; dependencies point **inward**.
- **No cross-context imports** of domain core.
- **New context:** replicate the hex layout (`domain/`, `driver/`, `driven/`, `presentation/`, `tests/` as in `.ai-config/skills/architecture.md` and `docs/architecture/`).
- **New web context / app package:** also scaffold `vitest.config.mts` (not `.ts`), `test/setup.ts`, and `test/support/test-router.tsx` when UI/feature/sanity tests render routed components — use `TestMemoryRouter` / `TestBrowserRouter`, not raw routers (see `.ai-config/skills/testing.md` § *Web frontend Vitest conventions*).
- **Ports first**, adapters second; wire dependencies only at **composition roots**.
- **Frontend atomic hexagonal placement:** feature objects/views/pages stay in the owning domain or capability context; generic reusable atomic UI belongs in `core-ui`. Split large pages/components into focused components, hooks, or helpers before adding more behavior.

## Testing strategy (mandatory shapes)

- **Unit tests** — only **configuration**, **driver** (inbound) adapters, and **driven** (outbound) adapters. Paths **mirror `src`** under `tests/unit/` (or package-local `test/unit/`). **No** unit tests whose subject is domain entities, value objects, domain services, ports as types only, or use case classes in isolation.
- **Use case tests** — invoke the **real use case** class with **all ports** faked or mocked; assert domain rules and orchestration. **Do not** “move” domain unit tests into the use-case suite. For **corner cases / domain coverage**, add **more use case tests**, not domain service unit tests.
- **Feature tests** — **cross-hexagon** flow within a bounded context (e.g. `tests/feature/` with real DB or HTTP stack **as defined per package**). On **frontend**, feature-level tests also cover **component** / page behavior where that package’s conventions apply.
- Add **appropriate** tests per change (unit / use case / feature / UI / sanity / Robot E2E as applicable).

## Robot Framework E2E (`testing/e2e/backend/`)

- In **Test Cases**, **`[Documentation]`**, and **keywords invoked from test cases**: use **business / product language** only (actors, outcomes, product terms). **Do not** use URLs, HTTP status codes, header names, JSON field names, OpenAPI/BFF/wire-format jargon in those places.
- **Technical** HTTP, paths, JSON keys, and low-level checks belong in **`libraries/ApiLibrary.py`** and in the **bodies** of resource keywords — not in the test-case layer.
- Prefer **one resource file per domain context** (e.g. `<context>.robot`). Update the project's test scenarios document when adding scenarios (see `testing/README.md`).

## Evidence and quality (before commit)

- Use the **Evidence Template** (`.ai-config/skills/evidence.md`): requirement, scope, design, implementation, **tests**, validation commands, risks, rollback.
- **Backend lint (before finishing edits):** after changing backend `.py` (src, tests, or `scripts/`), run `make -C backend lint-package PACKAGE=… MYPY_PACKAGE=…` (or root `poetry run ruff check` for scripts) and fix all ruff/mypy errors **before ending the agent turn**.
- **Web lint (before finishing edits):** after changing frontend-web `.ts`/`.tsx`/`.css` or tests, run `make -C frontend-web lint-package PACKAGE=…`, fix eslint; run `pnpm run type-check` when TS changed; verify app `pnpm run build` when Tailwind `@apply` CSS changed.
- **Mobile lint (before finishing edits):** after changing frontend-mobile `.dart`, run `make -C frontend-mobile lint-package PACKAGE=…` and fix all `flutter analyze` issues.
- Hooks (**postToolUse** / **stop**) track touched packages across all three stacks, in any repository of the workspace, and list commands. Full checklists: `.ai-config/skills/backend.md`, `web.md`, `mobile.md` § Lint before finishing.
- **Checkpoints** (use existing Makefile targets from repo / package): `make build`, `make test-unit`, `make test-use-case`, `make test-feature`, `make test-sanity`, functional E2E from `testing/` where relevant, `make format`, `make lint`, `make test-regression`.

## Commit messages (Conventional Commits + domain scope)

Use **[Conventional Commits](https://www.conventionalcommits.org/)** types (`feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`, `build`, …). **Subject line (≤ ~72 chars):**

`type(domain/context)/area: imperative summary`

- **`type`:** conventional verb (what changed).
- **`(domain/context)`:** bounded domain or slice, slash-separated when nested (e.g. `orders/checkout`). Mirrors product/architecture language.
- **`/area`:** where the change lands. The set of areas is **defined by the project** (Kapita: `backend`, `web`, `mobile`, `testing`, `docs`, `cursor`; the repository's own session text lists its set).
- **`:`** then a **short imperative summary** (no trailing period).

**Body:** After a blank line, add a **description** (bullets or short paragraphs): what changed, why, risk/rollback pointers — aligned with the Evidence Template when possible.

**Granularity:** one small, atomic commit per repository and per step. Never push, amend published commits, or skip hooks unless asked.

**Uniform `docs` commits:** Prefer `docs(domain/context)/docs: …` for consistency. The shorter `docs(domain/context): …` form is acceptable when the commit is **only** documentation under `docs/` and the type already signals doc-only scope.

**Examples:**

- `docs(orders/checkout): update checkout docs and testing scenarios`
- `test(orders/checkout)/testing: add refund scenarios and robot helpers`
- `feat(orders/checkout)/mobile: add the refund screen + tests and API client forwarding`
- `feat(orders/checkout)/web: add the refund form + tests`
- `feat(orders/checkout)/backend: add the refund use case`

## Observability

- Propagate identity and debug context across clients and BFF (`.ai-config/skills/observability.md`); structured logs at boundaries; **no PII** in telemetry.

## Canonical conflict order

1. `.ai-config/rules/generic-rules.md`, then the repository's own rules
2. `.ai-config/skills/*.md` and the repository's skills
3. `docs/architecture/1.atomic-hexagonal-architecture.md`
4. `docs/testing/Testing-Strategy.md`

Do **not** invent new Makefile command names; use existing targets.
