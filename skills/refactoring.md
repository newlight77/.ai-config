# Refactoring Skills

**When to use:** Extraction, splitting modules, migrations, moving code between layers.

- Minimal diffs; avoid unrelated formatting changes
- Extract reusable atomic UI into the platform design-system/core-ui package; keep domain-specific UI, feature objects, featured views/widgets, and routed pages/screens in the owning context presentation layer
- When a page/screen/component/widget grows too large, split it into focused presentational pieces, hooks/providers, helpers, or use-case orchestration rather than extending the large file
- Promote a component/widget to platform design-system/core-ui only when it is generic, token-driven, reusable across contexts, and free of domain behavior/API calls/providers
- Split large modules (routes, repositories) by responsibility
- Add tests when refactoring behavior
- **New web context package:** include `vitest.config.mts` and `test/support/test-router.tsx` (when routed UI is tested) at scaffold time — see `testing.md` § *Web frontend Vitest conventions*
- Ensure no breaking cross-context imports; validate with sanity/regression tests
