# Testing Skills

**When to use:** Adding/updating tests, coverage, Robot Framework, CI test workflows.

**Entry point:** the workspace `AGENTS.md`. Strategy source of truth: the project's `docs/testing/Testing-Strategy.md` (see [`canonical.md`](../canonical.md)). **Coverage gates:** the project's `docs/testing/Coverage-Thresholds.md` (per-platform per-type minimums, lcov filters, `COVERAGE_ENFORCE`). Project-specific suites and scenario catalogs live in the project's own testing skill (Kapita: `kapita-testing.md`). Tool-side testing (functional-test catalog, stages): see the Shipdeck test tube skill.

## Strategy

- **Unit:** configuration, **driver** (inbound adapters), and **driven** (outbound adapters) only—**no** tests for `domain/` (entities, value objects, services, ports as types, or use case classes in isolation).
- **Use case:** **invoke use case classes** (`execute` / `run` / etc.) with **faked or mocked ports**—this is how domain rules and orchestration are asserted. **Do not** treat the use-case suite as a place to “move” former domain unit tests; there must be **no** unit tests for the domain layer.
- **Corner cases & domain coverage:** add **more use case tests** (additional scenarios, boundary conditions, failure paths) to raise coverage on domain behavior—**not** by adding unit tests against domain **services** or by moving files from `unit/` to `use_case/`.
- **Feature:** cross-hexagon flow within a context (e.g. `tests/feature/` with real DB or HTTP stack as defined per package)
- UI: component/page behavior (frontend only)
- **Sanity:** app-level smoke flows (e.g. `backend/apps/<app>/tests/sanity/`); run via `make test-sanity` / `make test-sanity-package PACKAGE=...` from `backend/`
- Robot Framework: end-to-end functional validation when user-facing behavior changes

## Unit test scope

**Unit** tests cover **configuration**, **driver** (inbound) adapters, and **driven** (outbound) adapters, plus **narrow exceptional cases** that belong at adapter boundaries (parsing, mapping, error translation, wiring)—still **not** the domain core.

**There are no unit tests against the domain:** do not unit-test `domain/` entities, value objects, domain **services**, ports as types only, or use case classes in isolation. Domain behavior and orchestration are asserted through **use case tests** (and broader tests where applicable).

## Use case test isolation

Use-case tests exercise the **real** use-case class and substitute **all ports** with fakes or mocks so there is no real network, database, or production adapter I/O.

- **Backend:** Fakes in `tests/use_case/conftest.py`; **pytest fixtures** inject them (per-test scope); optional `@pytest.mark.use_case` in some `pytest.ini` files.
- **Web:** `test/use-case/` with Vitest; fake repositories or mocked ports.
- **Mobile:** `test/use_case/` with Dart fakes or mocks; no real Dio / platform storage in that suite.

## Layout (must mirror `src`)

- Under `tests/unit/` (or `test/unit/`), **mirror** the same relative paths as production code: `driver/`, `driven/`, config, and shared non-domain libs as applicable.
- **Example (backend):** implementation `src/.../driven/spi/user/user_repository.py` → tests `tests/unit/driven/spi/user/test_user_repository.py` (not `tests/unit/domain/...`).
- **Backend coverage scope:** unit runs omit `domain/use_cases`, `domain/use-cases`, and `domain/ports`; use-case runs omit `driver/` and `driven/`; feature and sanity measure the full tree. Config: `backend/scripts/coverage/*.ini`, applied by `make test-*` via `--cov-config`. Web/mobile use the same omit rules via `scripts/testing/coverage_scope/coverage_scope.py` (Vitest exclude + lcov filters).
- Stack-specific roots (`tests/`, `test/`, `test/use-case` vs `test/use_case`) follow each package’s Makefile/CI; the **shape** under `unit/` still matches `src`.

## Practices

- Add appropriate tests per change (unit/use case/feature/UI/sanity)
- **`make test` / `test-*` / `format` / `format-*` / `lint` / `lint-*`:** print per-target and per-package durations via `scripts/make/make_time/make_time.py` (see `scripts/README.md` § Make target timing)
- **Web interactive surface hover:** assert panel/list CSS classes in UI/feature tests; do not add hover checks to Robot suites (see the project's design-system doc)
- Prefer **use case tests** for business corner cases; **do not** add domain coverage by unit-testing **services** in isolation
- Exclude storybook/story files from coverage
- Use fakes/mocks; avoid flaky external services
- For analytics/tracking changes: unit-test adapter/config wiring where needed; assert product behavior in **use case tests** with mocked clients

## Robot Framework E2E (testing/e2e/backend/)

**Targets:** point suites at `local`, `dev` or `staging` of the product, never at production hosts or the production stage. A target guard (`libraries/target_guard.py`) and the test tool refuse a production target; do not work around them.

**Index:** `testing/README.md` (Makefile entrypoints, link to `testing/e2e/backend/README.md`, vocabulary summary).

1. **Consult the scenario catalog first** (`docs/testing/Test-Scenarios.md`) – add scenarios there before writing suites (user journeys and expected outcomes in plain language; scenario groups carry letter prefixes defined in the catalog).
2. **Domain language in test suites (`*.robot` Test Cases and Settings)** – Use **only business / functional vocabulary**: actor intent, outcomes, and product terms. **Do not** put URLs, HTTP status codes, header names, JSON field names, OpenAPI, BFF, or wire-format acronyms in scenario titles, `[Documentation]`, or keyword names invoked from test cases.
3. **Domain-oriented keyword names in resource files** – Keywords exposed for test cases should read like capabilities or assertions in the product language (e.g. `User Requests Strategy Simulation For Symbol`, `Past Simulations Should Include The New Simulation`). Implementation may still call `ApiLibrary` and paths inside the keyword body; keep that detail out of the test-case layer.
4. **Technical vocabulary in libraries** – HTTP calls, status checks, JSON key access, and low-level assertions belong in `libraries/ApiLibrary.py` (and one library per separate service base URL, so keyword names do not clash in the same suite). Technical detail may also live in the *bodies* of resource keywords, not in test-case text.
5. **Resources per domain** – One resource file per context (`base.robot`, `authentication.robot`, …).
6. **Tests hit real services** – Validate end-to-end flows against running backends; tolerate optional dependencies where documented via `Pass Execution If` with **business** skip messages.
7. **Ephemeral test-data teardown** – Suites that create throwaway users register them during the test and clean them at **Test Teardown** through a shared teardown resource; registration happens immediately after signup so failed mid-test cases still clean up. The cleanup route is token-gated and disabled in production; seeded personas are never deleted. Make local skipping and strict CI failure switchable by environment variables.

## Robot Framework E2E UI (testing/e2e/web/)

**Index:** `testing/e2e/web/README.md` (Browser library, Makefile, `todo` / `ui-ready` tags, CI workflow).

A **postToolUse** hook applies the same **business-domain vocabulary** rules to `testing/e2e/web/**/*.robot` as for backend API suites.

1. **Mirror backend scenarios** — Each `functional-testing-*-api.robot` has a `functional-testing-*-ui.robot` counterpart; scaffold them with the project's scaffold script (preserve implemented cases without `todo` unless `--force`).
2. **Domain language in test suites** — Same rules as API E2E: no URLs, HTTP codes, JSON field names, or wire jargon in scenario titles, `[Documentation]`, or keywords invoked from test cases.
3. **Page resources** — `resources/pages/*.robot` hold selectors and navigation; name keywords in product language. Prefer stable `data-testid` on app flows as groups are implemented.
4. **Hybrid setup** — `resources/api-setup.robot` may seed users or read state via the API when faster than pure UI; keep API detail out of test-case text.
5. **Test-data teardown** — The UI teardown keyword clears ephemeral users through the shared teardown resource.
6. **CI** — `robot --exclude todo`; remove `todo` and add `ui-ready` when a case is implemented and expected to pass.

## Web frontend Vitest conventions

Applies to every **new or existing** `frontend-web` package/app with Vitest (contexts, capabilities, `core-ui`, app shells).

### New web context checklist (mandatory at scaffold time)

When creating a domain/capability package or a routed app, set this up **before** the first UI/feature/sanity test — not as a follow-up migration.

1. **`vitest.config.mts`** — copy/adapt from a sibling context. Do **not** add `vitest.config.ts`.
2. **`test/setup.ts`** — jest-dom matchers + RTL `afterEach(cleanup)` for jsdom suites (see existing contexts).
3. **`test/support/test-router.tsx`** — required when any test renders routed pages/components (see canonical shape below). Optional for packages with only unit/use-case (node) tests.
4. **`vitest.sanity.config.mts`** — when `test/sanity/` exists; point `package.json` / Makefile scripts at `.mts`.
5. **Test imports** — UI/feature/sanity tests import `TestMemoryRouter` / `TestBrowserRouter` from `test/support/test-router`; keep `Route`, `Routes`, hooks from `react-router-dom` as needed.
6. **Shared render helpers** — a router-wrapping render helper must wrap `TestMemoryRouter`, not `MemoryRouter`.
7. **Production parity** — app shells use the same v7 `future` flags on `BrowserRouter` (in the app's `app.tsx`); test flags live only in `test-router.tsx`.

**Reference packages:** pick two or three existing contexts of the project that already follow this checklist (Kapita: see `kapita-testing.md`).

### Vitest config (ESM)

- Use **`vitest.config.mts`** and **`vitest.sanity.config.mts`** — not `.ts`.
- Loading `.ts` configs triggers **“The CJS build of Vite's Node API is deprecated”** under Vitest.
- In coverage excludes, list `'**/vitest.config.{ts,js,mts}'`.
- Makefile / `package.json` sanity scripts must pass `--config vitest.sanity.config.mts` when overriding the default config.

### React Router in UI / feature / sanity tests

Production apps opt into React Router v7 future flags on `BrowserRouter` (in the app's `app.tsx`). Tests must match so Vitest does not emit future-flag warnings and behavior stays aligned.

**Per package/app that renders routed components in tests:**

1. Add **`test/support/test-router.tsx`** (canonical shape below — copy verbatim when creating a new context).
2. Import **`TestMemoryRouter`** / **`TestBrowserRouter`** from that helper — **never** raw `MemoryRouter` / `BrowserRouter` in test files.
3. Keep other router imports (`Route`, `Routes`, hooks) from `react-router-dom` as needed.
4. Shared render helpers (e.g. a `withRouter` helper) must wrap children with **`TestMemoryRouter`**, not `MemoryRouter`.

**Anti-patterns (do not introduce):**

- `vitest.config.ts` or `vitest.sanity.config.ts` in new packages
- Raw `<MemoryRouter>` / `<BrowserRouter>` in test files
- One-off `future={{ v7_startTransition: true, … }}` on routers in individual tests
- One-time migration scripts instead of scaffolding correctly up front

**Canonical `test/support/test-router.tsx`:**

```tsx
import React from 'react';
import {
  BrowserRouter,
  MemoryRouter,
  type BrowserRouterProps,
  type MemoryRouterProps,
} from 'react-router-dom';

export const REACT_ROUTER_FUTURE_FLAGS = {
  v7_startTransition: true,
  v7_relativeSplatPath: true,
} as const;

export function TestMemoryRouter(props: MemoryRouterProps) {
  return <MemoryRouter future={REACT_ROUTER_FUTURE_FLAGS} {...props} />;
}

export function TestBrowserRouter(props: BrowserRouterProps) {
  return <BrowserRouter future={REACT_ROUTER_FUTURE_FLAGS} {...props} />;
}
```

**Import path:** from `test/<layer>/…/<file>.test.tsx`, import relatively (e.g. `../../../../../support/test-router` — one `../` per directory under `test/`, excluding the file itself).

**Do not** add one-off `future={{ … }}` props on raw routers in individual tests; centralize in `test-router.tsx` so production and tests stay in sync.
