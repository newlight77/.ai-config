# Design System Skills

**When to use:** UI components, design tokens, styling, Tailwind, accessibility, core-ui.

**Project specifics** (brand values, token names, class prefix, component catalog, Figma file, exemplar pages) live in the project's design-system skill (Kapita: `kapita-design-system.md`).

## TSX Styling

- One `className` per HTML element; dedicated CSS file per component
- One CSS file per page; class names `<project>-*-page__*`; no shared CSS across pages
- Generic components: own classNames; featured components override via their CSS file—not multiple classNames in TSX
- Never hardcode colors, spacing, or typography; use design tokens
  - Web: Tailwind utilities backed by CSS variables (`bg-background`, `text-text-secondary`)
  - Mobile: `AppPalette.*` and theme values

## Component Hierarchy

Atoms → Molecules → Organisms → Templates → Pages. Feature-specific behavior stays in context presentation.

## Placement

- Platform design-system/core-ui packages are for generic, reusable, token-driven atomic components/widgets only.
- Domain/capability contexts own feature objects, featured views/widgets, routed pages/screens, and components/widgets with product/domain behavior.
- When extracting from a page/screen, first decide whether the result is generic UI (platform design-system/core-ui) or context-specific presentation (`presentation/components` / `presentation/featured`).
- Avoid adding API calls, use-case orchestration, routing decisions, providers, or domain vocabulary to generic UI packages; pass behavior through props/callbacks.

## Figma ↔ code token sync

- Code is the source of truth for tokens (CSS variables / Tailwind config in `core-ui`); Figma variables mirror them (same names, light/dark modes).
- Changing a token: update code first, then the Figma variable; record gaps in the whiteboard rather than hardcoding in either side.
- Design workflow and MCP usage: `figma-design.md`; component design: `react-design.md`.

## Interactive surface hover (web)

When adding or changing panels, cards, or list rows on web:

1. **Outermost panel/card:** primary-colour border + slight lift on hover.
2. **Nested panel/card:** no border highlight or lift on hover.
3. **List item in a panel/card:** subtle transparent background only (`color-mix(in srgb, var(--text-primary) 5%, transparent)`); no border or lift.

- Implement once in a shared utility stylesheet of `core-ui` (`styles/utilities/interactive-surface.css`); consumers opt in with the project's panel class, opt out on nested surfaces, and use a registered row class for list items
- Do not add page-local `:hover` border/lift on panel shells or list rows

Full spec: the project's `docs/architecture/2.design-system.md` § Interactive surface hover.

## Rules

- State the project's brand values and typefaces in its design-system skill; design to them
- WCAG 2.1 AA contrast, accessible focus states
- Use the shared card components; avoid bespoke glassmorphism or card implementations
- **Interactive surface hover (web):** three mandatory rules for panels/cards and list rows (above); implement via the shared utility stylesheet and the project's panel / opt-out / list-item classes
- Always check `core-ui` before creating new UI; reuse via props/variants and composition
- When a web `core-ui` component is added, export it from the appropriate barrel, add its CSS to `src/styles/index.css`, and add UI tests.
- When a mobile design-system/core-ui widget is added, export it through the package’s public barrel, use `AppPalette`/theme values, and add widget tests.

## Mobile shell molecules (generic)

Location: `frontend-mobile/packages/core/lib/core-ui/lib/components/molecules/`. Catalog: `docs/architecture/2.design-system.md` § Mobile shell molecules; app shell and routes: `docs/architecture/1.atomic-hexagonal-architecture.md` § Frontend mobile — app shell and placement.

| Widget | Purpose |
|--------|---------|
| `PageActionGroup` | Header / app-bar action group spacing |
| `IconToolbar`, `ToolbarIconButton`, `ToolbarDivider` | Pill toolbar; domain passes icons and `onPressed` |
| `DialogActionRow` | Dialog footer actions (primary, secondary, destructive) |
| `ConfirmDialog`, `ActionDialog` | Confirmation and outcome dialogs |
| `CardSection`, `PanelSection` | Card shell with title, optional trailing, child body |
| `FilterSection`, `FilterDialogShell` | Filter dialog layout; domain owns field widgets |

**Do not** put route names, account IDs, product copy, or repository calls inside these widgets — pass via constructor parameters and callbacks only.

## Harmonising new web pages, banners, and buttons

**When to apply:** Adding or changing a routed page, info/config banner, toolbar, or action buttons in `frontend-web`. Read this section before shipping UI so new surfaces match existing pages of the project (exemplars in its design-system skill).

### Before creating UI

1. **Find a sibling page** in the same app/context (same shell, similar density) and mirror its structure — do not invent a one-off layout.
2. **Reuse `core-ui` first** — page header, glass/card shells, card and panel sections, action group, text input, select, status badge, error message, table organisms — before raw HTML or bespoke CSS.
3. **Dedicated page CSS** — one file `presentation/styles/<page-name>.css`; class prefix `<project>-<page>-page__*`; style via Tailwind `@apply` and design tokens — **never** hardcoded hex colors or legacy `--color-*` variables in feature CSS.

### Page shell (standard layout)

```tsx
<div className="<project>-<page>-page">
  <PageHeader title="…" backLabel="…" onBack={…} />
  <p className="<project>-<page>-page__intro">…</p>
  {/* optional config / banners */}
  <PanelCard className="<project>-<page>-page__panel <project>-interactive-panel">
    <h2 className="<project>-<page>-page__section-title">Section title</h2>
    …
  </PanelCard>
</div>
```

- Page padding, intro text, inline `code` and section-title typography come from spacing/typography tokens (exact utilities in the project's design-system skill).

### Banners and config panels

| Pattern | Use |
|---------|-----|
| **Single outer panel** | One card shell + interactive-panel class per major page block (catalog, config, detail). |
| **Nested sections** | `CardSection` inside the card — title + optional `headerAction`; set `spaced={false}` when stacked. |
| **Multiple related config blocks** | One outer card; inner `CardSection`s with nested hover disabled (see interactive surface hover). |
| **Page-level grouping** | `PanelSection` when a titled group wraps several cards (title + description + content). |
| **Status / chips** | `StatusBadge` with semantic variants — not custom pill colors. |
| **Queue / list rows** | The registered list-item class on rows inside a panel — no local border/lift hover. |

### Buttons and toolbars

- **Primary actions** (submit, save, search, run): `Button` `variant="primary"` `size="md"` with the project's form-button class.
- **Secondary actions** (reset, cancel, outline triggers): `variant="outline"` `size="md"` with the project's form-button class.
- **Toolbar alignment**: wrap actions in `PageActionGroup` `variant="toolbar"` with an `ariaLabel`.
- **Do not** use `size="sm"` for form/page actions unless the surrounding page already standardises on small buttons.
- **Do not** use raw `<button>` for primary actions when `Button` exists (exception: icon-only toggles with explicit a11y labels).

### CSS checklist (before PR)

- [ ] No hardcoded colors in feature CSS; use `text-text-secondary`, `border-border`, `color-mix(in srgb, var(--primary-main) …)`, etc.
- [ ] Outermost panel has the interactive-panel class; nested `CardSection` / inner cards use the opt-out class or page CSS that resets hover/lift.
- [ ] One `className` per element in TSX; visual overrides in the page/component CSS file.
- [ ] New `core-ui` widgets exported, CSS imported in `styles/index.css`, UI tests added (if generic).
