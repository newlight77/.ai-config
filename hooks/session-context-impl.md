# Generic implementation constraints (injected once, when the prompt looks like code work)

## Hexagonal architecture (new context / vertical slice)

- **Isolate the domain**; adapters implement **ports**; dependencies point **inward**; **no cross-context imports** of domain core.
- **New context:** replicate the hex layout (`domain/`, `driver/`, `driven/`, `presentation/`, `tests/`; see `.ai-config/skills/architecture.md`, `docs/architecture/`).
- **New web context / app package:** also scaffold `vitest.config.mts` (not `.ts`), `test/setup.ts`, `test/support/test-router.tsx` when tests render routed components; use `TestMemoryRouter` / `TestBrowserRouter`, not raw routers (`testing.md` § *Web frontend Vitest conventions*).
- **Ports first**, adapters second; wire dependencies only at **composition roots**.
- **Frontend:** feature objects/views/pages stay in the owning domain or capability context; generic reusable atomic UI belongs in `core-ui`. Split large pages/components into components, hooks or helpers before adding behavior.

## Testing strategy (mandatory shapes)

- **Unit tests:** only **configuration**, **driver** (inbound) and **driven** (outbound) adapters. Paths mirror `src` under `tests/unit/` (or `test/unit/`). **No** unit tests of entities, value objects, domain services, ports, or use case classes in isolation.
- **Use case tests:** the **real use case** with **all ports** faked; assert domain rules and orchestration. Corner cases and domain coverage go here, not into domain unit tests.
- **Feature tests:** cross-hexagon flow within a bounded context (`tests/feature/`); on the frontend they also cover component/page behavior.
- Add the appropriate tests per change (unit / use case / feature / UI / sanity / Robot E2E).

## Robot Framework E2E (`testing/e2e/backend/`)

- Test Cases, `[Documentation]` and keywords invoked from test cases: **business language only** (no URLs, HTTP codes, headers, JSON fields, wire jargon).
- Technical HTTP/JSON belongs in `libraries/ApiLibrary.py` and resource keyword bodies.
- One resource file per domain context; update the project's test scenarios document (`testing/README.md`).

## Lint before finishing (the post-tool hook tracks touched packages, the stop hook lists them)

- **Backend `.py`:** `make -C backend lint-package PACKAGE=… MYPY_PACKAGE=…` (or `poetry run ruff check` for `scripts/`); fix all ruff/mypy errors before ending the turn.
- **Web `.ts`/`.tsx`/`.css`:** `make -C frontend-web lint-package PACKAGE=…`; `pnpm run type-check` when TS changed; `pnpm run build` when Tailwind `@apply` CSS changed.
- **Mobile `.dart`:** `make -C frontend-mobile lint-package PACKAGE=…`; fix all `flutter analyze` issues.
- Checklists: `backend.md`, `web.md`, `mobile.md` § Lint before finishing.

## Observability

Propagate identity and debug context across clients and BFF (`.ai-config/skills/observability.md`); structured logs at boundaries; **no PII** in telemetry.
