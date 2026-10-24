# React Design Skill

**When to use:** Designing or implementing React components and pages in `frontend-web` — structure, props/variants, composition, accessibility, stories. Complements `web.md` (tooling, lint) and `design-system.md` (tokens, styling, placement).

## Component design

- **Reuse first**: search `core-ui` before creating anything; extend via props/variants and composition, not copies.
- **Atomic hierarchy**: atoms → molecules → organisms → templates → pages. Generic UI goes in `core-ui`; domain behavior stays in the context's `presentation/` layer (placement rules in `design-system.md`).
- **Props API**: small, typed, intention-revealing. Prefer `variant` / `size` unions over boolean flags; pass behavior as callbacks; no API calls, routing or domain vocabulary in generic components.
- **Composition**: use `children` and slots over configuration objects; keep components presentational, put data fetching in hooks/containers.
- **State**: keep it local and minimal; derive instead of syncing; lift only when shared.
- **One `className` per element**, dedicated CSS file, design tokens only (see `design-system.md`).

## Accessibility

- Semantic elements first (`button`, `nav`, headings in order); ARIA only to fill gaps.
- Visible focus, keyboard operability, labels for icon-only controls, WCAG 2.1 AA contrast.

## Stories and tests

- Every new `core-ui` component: export from the barrel, import its CSS in `src/styles/index.css`, add a Storybook story (variants + states) and UI tests.
- Stories feed the living design system (the stories app).

## From Figma to React

1. Identify the Figma node and its mapped `core-ui` component (Code Connect).
2. Map variants → props, variables → tokens; flag gaps back to the design instead of hardcoding.
3. Build with existing components; add a new generic component only when none fits.

See `figma-design.md` for the design workflow and MCP usage.
