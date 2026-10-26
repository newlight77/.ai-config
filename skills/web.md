# Web (Frontend) Skills

**When to use:** React, TypeScript, Tailwind, frontend-web packages.

- TypeScript + React best practices
- Design system: `.ai-config/skills/design-system.md` (className, tokens, atomic hierarchy, **interactive surface hover** on panels/lists, **harmonising pages/banners/buttons**)
- Decoupled Tailwind (`@apply` in CSS); project-prefixed semantic class naming (see the project's design-system skill)
- Storybook for `core-ui`; component testing (Vitest, Playwright)
- Chart components (Recharts/FeaturedChart)
- Build/test via Makefile and CI; test layers: **unit** = config + driver/driven adapters only (no `domain/`); **use case** = real use case + mocked ports (see `testing.md`)
- **New web context / app package:** scaffold `vitest.config.mts`, `test/setup.ts`, and (when tests render routes) `test/support/test-router.tsx` before adding UI/feature/sanity tests — see `architecture.md` § *New web context scaffold* and `testing.md` § *Web frontend Vitest conventions*
- **Web Vitest + React Router in tests:** use `TestMemoryRouter` / `TestBrowserRouter` from `test/support/test-router.tsx` — never raw `MemoryRouter` / `BrowserRouter` in test files
- Frontend atomic hexagonal placement:
  - Put feature objects/views/pages in the owning domain or capability context (`presentation/pages`, `presentation/featured`, `presentation/components`).
  - Put generic reusable atomic UI in `frontend-web/packages/core/lib/core-ui` as atoms/molecules/organisms/templates.
  - Do not move domain-specific language, use-case orchestration, API calls, or context behavior into `core-ui`.
- Refactor habit (web): keep components small and composable.
  - Split large pages/components into focused presentational pieces + hooks before adding more behavior.
  - Keep data-fetching/state orchestration in container-level components.
  - Move chart/math/interaction helpers into dedicated hooks or utilities.
  - Extract a component to `core-ui` when it is generic, token-driven, and reusable across contexts; otherwise keep it in the context.
  - Prefer explicit props contracts over implicit shared mutable state.
- **New page / banner / buttons:** follow `design-system.md` § *Harmonising new web pages, banners, and buttons* — match sibling pages, reuse the project's page shell components and form-button classes (see its design-system skill), token-based page CSS; cite an existing page as the reference implementation.

## Lint before finishing (mandatory)

After **any** web change (`src/`, `test/`, or package CSS under `presentation/styles/`), **before ending the agent turn or committing**:

1. **Run package lint** on every package you touched:
   ```bash
   make -C frontend-web lint-package PACKAGE=<path-under-frontend-web>
   ```
   Examples:
   - `make -C frontend-web lint-package PACKAGE=packages/domains/<domain>/<context>`
   - `make -C frontend-web lint-package PACKAGE=apps/<app>`
2. **TypeScript:** when editing `.ts`/`.tsx`, also run `pnpm run type-check` in that package when the script exists (eslint alone does not catch `tsc` errors).
3. **Tailwind `@apply` in CSS:** invalid utility classes fail at **Vite build** — use Tailwind tokens from `tailwind.config.js` (e.g. `text-text-secondary`, `text-warning-main`), not compat-only classes like `text-<project>-warning` / `text-<project>-muted`. Verify with `pnpm run build` on the consuming app when CSS changed.
4. **Fix all eslint / type-check / build errors** before finishing — do not defer to CI.

Composer hooks track touched packages (`.ai-config/hooks/post-tool.py`); the **stop** hook lists commands for backend, web, and mobile edits this session.
