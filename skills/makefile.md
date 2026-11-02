# Makefile — Normalized Target Conventions

**When to use:** Adding, renaming, or auditing Makefile targets in any repository. All repositories share this shape; repository-specific targets extend it — they never contradict it.

## Pattern

```
<verb>                   # aggregate: runs all sub-targets of that verb
<verb>-<component>       # per-component: scoped to one app, service or package
<verb>-<noun>-package    # per-package variant: accepts PACKAGE= argument
```

Use existing targets; never invent new verbs. When a component is added, add only the targets below that apply to it — do not add targets for operations the component does not support.

---

## Target groups

### `install` / `install-*`

Install dependencies for a component.

| Target | What it does |
|--------|-------------|
| `install` | Install all components (calls every `install-*`) |
| `install-<component>` | `poetry install` / `pnpm install` for one app or service |
| `install-package` | Install a single package; accepts `PACKAGE=` |

Convention: idempotent; safe to re-run. No side effects beyond the local virtualenv / `node_modules`.

---

### `build` / `build-*`

Compile, bundle or type-check artefacts.

| Target | What it does |
|--------|-------------|
| `build` | Build all components |
| `build-<component>` | Build one app or service (e.g. `pyinstaller`, `pnpm build`) |
| `build-package` | Build a single package; accepts `PACKAGE=` |

Convention: produces deterministic artefacts; does not start a server; does not touch the database.

---

### `run` / `run-*`

Start a component locally for development.

| Target | What it does |
|--------|-------------|
| `run` | Start the default / primary app |
| `run-<component>` | Start one app or service in the foreground (hot-reload where available) |

Convention: uses `.env.<kind>.<component>.local.env` when present, falls back to `.template.env`. Never used in CI.

---

### `test` / `test-*`

Run the test suite or a subset of it.

| Target | What it does |
|--------|-------------|
| `test` | Run all test layers for all components |
| `test-unit` | Unit tests only (all components) |
| `test-use-case` | Use-case tests only |
| `test-feature` | Feature tests only |
| `test-sanity` | Sanity / smoke tests only |
| `test-unit-package` | Unit tests for one package; accepts `PACKAGE=` |
| `test-use-case-package` | Use-case tests for one package; accepts `PACKAGE=` |
| `test-feature-package` | Feature tests for one package; accepts `PACKAGE=` |
| `test-sanity-package` | Sanity tests for one package; accepts `PACKAGE=` |
| `coverage` | Run tests and produce coverage report |
| `coverage-merge` | Merge coverage from multiple runs |
| `coverage-merge-package` | Merge coverage for one package; accepts `PACKAGE=` |

Convention: tests never write to production or staging; they never depend on the cluster being up. The `test` aggregate must be safe to run on CI without extra setup beyond `install`.

---

### `seed` / `seed-*`

Populate a namespace or service with initial or test data.

| Target | What it does |
|--------|-------------|
| `seed-<namespace>` | Seed the named namespace (`dev`, `staging`, `prod`, `enabler`, `build`, …) |
| `seed-<component>` | Seed data owned by one component (e.g. `seed-offers`, `seed-retro-planning`) |
| `seed-<component>-clear` | Remove seeded data for one component |

Convention: reads credentials from `seed.<seed-<namespace>|seed-<component>>.<namespace>.env`; must be idempotent or provide a matching `*-clear` target. Never seeds `prod` without explicit opt-in (`CONFIRM_PROD=true`).

---

### `format` / `format-*`

Auto-format source files.

| Target | What it does |
|--------|-------------|
| `format` | Format all packages |
| `format-package` | Format one package; accepts `PACKAGE=` |
| `format-check` | Check formatting without writing (CI gate) |
| `format-check-package` | Check one package; accepts `PACKAGE=` |

Convention: `format` modifies files; `format-check` exits non-zero if anything would change. CI always calls `format-check`.

---

### `lint` / `lint-*`

Static analysis and type checking.

| Target | What it does |
|--------|-------------|
| `lint` | Lint all packages |
| `lint-package` | Lint one package; accepts `PACKAGE=` and `MYPY_PACKAGE=` (backend) |
| `lint-fix` | Auto-fix safe lint violations |

Convention: `lint` must be zero-exit on a clean tree. `lint-fix` is local-only; CI calls `lint` without fix.

---

### `migrate` / `migrate-*`

Database schema migrations (backend only).

| Target | What it does |
|--------|-------------|
| `migrate` | Apply all pending migrations (`alembic upgrade head`) |
| `migration` | Generate a new migration file; accepts `MESSAGE=` |
| `migrate-current` | Show the current migration revision |
| `migrate-downgrade` | Roll back one revision; accepts `REVISION=` |
| `migrate-stamp` | Stamp the DB to a revision without running SQL; accepts `REVISION=` |
| `migrate-force` | Force-apply a specific revision; use with caution |

Convention: never run against `prod` without a backup checkpoint. Migration targets read the DB URL from the env file for the active namespace.

---

### `docker` / `docker-*`

Container lifecycle for local development and CI.

| Target | What it does |
|--------|-------------|
| `docker-build` | Build all images locally |
| `docker-up` | Start all services via `docker-compose.yml` |
| `docker-down` | Stop and remove containers |
| `docker-logs` | Tail logs from all running containers |
| `docker-e2e-up` | Start the e2e compose stack (`docker-compose.e2e.yml`) |
| `docker-e2e-down` | Stop the e2e compose stack |

Convention: `docker-up` uses the default `docker-compose.yml`; e2e variants use `docker-compose.e2e.yml`. CI uses `docker-compose.e2e.ci.yml` (no host-mount volumes, amd64 pinned).

---

### `clean` / `clear-*`

Remove generated artefacts or test state.

| Target | What it does |
|--------|-------------|
| `clean` | Remove build outputs, `__pycache__`, dist dirs |
| `clear-test-account` | Delete the current session's test account data |
| `clear-test-account-all` | Delete all test account data (use with care) |

Convention: `clean` must never touch source files or `.env` files.

---

## General rules

- **Verbs are fixed** — do not introduce new top-level verbs; extend existing groups with `<verb>-<component>`.
- **Aggregates call sub-targets** — `make test` expands to `make test-unit test-use-case test-feature test-sanity`; it does not duplicate logic.
- **`PACKAGE=` targets** operate on one package directory relative to the repo root; the path is passed verbatim to the underlying tool.
- **No implicit env loading in Makefile** — each target explicitly references the correct env file; `export` at the top of the Makefile is banned.
- **CI never calls `run-*`, `docker-up`, or `seed-*` against production** without an explicit guard variable.
- **Timing wrappers** — `test-*`, `format-*`, `lint-*` are wrapped by `scripts/make/make_timing/make-timing.mk` to print durations.
