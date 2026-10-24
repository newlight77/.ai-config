# Architecture Skills

**When to use:** Hexagonal layout, vertical slices, ports/adapters, cross-context boundaries.

**Entry point:** the workspace `AGENTS.md`. Structural source of truth: the project's `docs/architecture/1.atomic-hexagonal-architecture.md` (see [`canonical.md`](../canonical.md)).

## Principles

- **Hexagonal**: domain core isolated; adapters implement ports; dependencies inward
- **Wire formats** (CSV, bulk upload layouts, export filenames, MIME/streaming): decode and map in **driving** adapters (e.g. BFF); domain use cases accept **domain types** only—see `docs/architecture/1.atomic-hexagonal-architecture.md` (“Wire formats and driver-side serialization”)
- **Atomic Design (UI)**: atoms → molecules → organisms → templates → featured objects/views/pages
- **Vertical Slice**: each context self-contained with ports, adapters, tests
- **Modularization**: keep small modules with focused responsibilities, enforce hexagon boundaries and avoid cross-context imports
- **Observability:** Log and trace at hexagon boundaries; see `.ai-config/skills/observability.md`

## Rules

- No cross-context imports of domain core
- A service owns its database (Kapita ADR 0033, valid for every project). Cross-domain and cross-capability callers use that service's API. An in-process driven adapter is only for contexts of the same domain composed in the owning process.
- Extract reusable atomic UI into the platform design-system/core-ui package; keep feature-specific behavior in context presentation.
- Place **feature objects/views/pages/widgets** inside the owning domain/capability context; do not promote domain-specific UI into platform design-system/core-ui packages.
- Split large pages/components into smaller presentational components, hooks, helpers, or use-case orchestration before adding more behavior.
- Enforce dependency inversion: use ports in domain, adapters in infrastructure.

## Practices

- **Testing:** **Unit** tests target configuration, **driver** and **driven** adapters, and **exceptional cases** only when they stay at adapter/config boundaries; paths **mirror `src`** under `tests/unit/` (or `test/unit/` on clients). **No** tests whose subject is domain entities, VOs, domain services, or use cases in isolation—use **use case tests** for that. Use case tests **invoke use case classes** with mocked/faked ports (see `.ai-config/skills/testing.md`). **Do not** relocate domain-only tests into the use-case folder as a stand-in. Add **use case tests** for corner cases to improve domain coverage—**not** unit tests against domain services.
- Ports-first: design ports/contracts before adapters
- Compose dependency wiring in composition roots only
- Monorepo: packages per capability, lib, or domain context

## Layout

- **SPI/Models**: Split by responsibility (e.g. `spi/user/user_repository.py`, `user_model.py`)
- **Domain**: `use_cases`, `ports` under `domain/`; `services`, `entities`, `value_objects` under `domain/core/`
- **API Routes**: Split by responsibility (signin, signup, profile, password, refresh_token)

## Structure (Backend)

```
backend/domains/<domain>/<context>/hexagons/<context>/
  domain/     # use_cases, ports, core (entities, value_objects, services)
  driver/     # inbound adapters (API/controllers)
  driven/     # outbound adapters (DB/queue/3rd-party)
  presentation/
  tests/
```

## Structure (Frontend Web)

```
frontend-web/.../domains/<domain>/<context>/hexagons/<context>/
  domain/     # use cases + ports (TS)
  driver/     # UI drivers (React modules/providers)
  driven/     # adapters (API clients, storage)
  presentation/
    pages/       # routed pages for this context
    featured/    # context-specific feature objects/views
    components/  # context-specific components only
  test/          # unit/, use-case/, feature/, ui/, sanity/; support/
  vitest.config.mts
```

### New web context scaffold

When adding a **new** `frontend-web` domain/capability package (or a routed app under `apps/`), include test boilerplate up front — do **not** use `vitest.config.ts` or raw `MemoryRouter` / `BrowserRouter` in tests.

| Artifact | Required | Notes |
|----------|----------|-------|
| `vitest.config.mts` | Yes | Copy from a sibling context. **Never** `vitest.config.ts` — Vitest loads it as CJS and emits a deprecation warning. |
| `vitest.sanity.config.mts` | When `test/sanity/` exists | Wire `package.json` / Makefile to `--config vitest.sanity.config.mts`. |
| `test/setup.ts` | Yes | jest-dom matchers + RTL cleanup for jsdom suites. |
| `test/support/test-router.tsx` | When UI/feature/sanity tests render routed components | Provides `TestMemoryRouter` / `TestBrowserRouter` with React Router v7 future flags (matches the app shell's router). |
| Production router | App shell only | `BrowserRouter` + same `future` flags live in the web app shell; contexts use test helpers only. |

Full canonical shapes, import-path rules, and anti-patterns: `.ai-config/skills/testing.md` § *Web frontend Vitest conventions*.

Generic reusable UI goes in `frontend-web/packages/core/lib/core-ui/src/components/` following atomic design:

```
atoms/       # smallest reusable primitives (Button, Avatar)
molecules/   # composed reusable controls (DropdownMenu)
organisms/   # larger reusable sections
templates/   # layout-level reusable structures
```

## Structure (Frontend Mobile)

```
frontend-mobile/.../domains/<domain>/<context>/hexagons/<context>/
  domain/     # use cases + ports (Dart)
  driver/     # UI drivers (providers/modules)
  driven/     # adapters (API clients, storage)
  presentation/
    pages/       # routed screens/pages for this context
    featured/    # context-specific feature objects/views/widgets
    components/  # context-specific widgets only
  tests/
```

Generic reusable mobile UI goes in the mobile design-system/core-ui package following atomic design:

```
frontend-mobile/packages/core/lib/core-ui/lib/components/
  atoms/       # smallest reusable widgets
  molecules/   # composed reusable controls (incl. shell molecules: IconToolbar, CardSection, …)
  organisms/   # larger reusable sections
  templates/   # layout-level reusable structures
```

**Mobile app shell:** `frontend-mobile/apps/app-mobile` wires routes and providers; domain screens live in context packages. See `docs/architecture/1.atomic-hexagonal-architecture.md` § Frontend mobile — app shell and placement. Flutter habits: `.ai-config/skills/mobile.md`.

## External PSPs (payments example)

For **third-party checkout** (e.g. Stripe Hosted Checkout), keep card data and provider SDK calls in **driven** adapters only:

- **Port** in domain (e.g. `CheckoutSessionProvider`): create session, parse/verify webhooks.
- **Adapter** under `driven/spi/<provider>/`: REST/SDK calls, webhook signature verification.
- **BFF**: authenticated routes for session creation; **webhook route** uses raw body + provider signature header (no user JWT).
- **Cross-stack:** same BFF contract for web and mobile HTTP clients; document the provider flow in the owning context's README.
