# Figma Design Skill

**When to use:** Wireframes, mockups, FigJam user-flow boards, system/product design artifacts, design-to-code, Code Connect, design-token sync.

## Tooling

- Figma MCP server `figma` — declared in `.mcp.json` (Claude Code) and `.cursor/mcp.json` (Cursor). OAuth only; authorize interactively (`/mcp` in Claude Code). Never commit tokens.
- Figma file: named in the project's design-system skill (Kapita: `kapita-design-system.md`).
- If the MCP server is not authorized, say so and continue with the repo-side artifacts (whiteboard docs); do not fake Figma output.

## Workflow (Product Design phase)

1. **Flow** — Start from the user flow (the project's user-flow skill and `docs/product/` flow documents, `docs/architecture/domains/*/flows/*.md`). Draw it in FigJam (Mermaid via `generate_diagram`).
2. **Wireframe** — Low-fidelity frames per page, one Figma page per flow group.
3. **Mockup** — High-fidelity frames built from design-system components and variables only.
4. **Handoff** — Map components with Code Connect; implement via `design-to-code` using `core-ui`.
5. **Record** — Link the frames from the project's whiteboard docs (Kapita: `docs/documentation-tube/whiteboard/`) and update the prompt status.

## Conventions

- **Pages** in Figma = flow groups (e.g. `Onboarding`, `Checkout`); **frames** = routes, named `<route-or-screen> / <breakpoint>` (`Dashboard / desktop`, `Dashboard / mobile`).
- **Variables** mirror code tokens (colors, spacing, radius, typography); light and dark modes. Never hardcode hex values in mockups.
- **Components** mirror `core-ui` names (`PageHeader`, `GlassCard`, `CardSection`, `PanelSection`, `Button`, `StatusBadge`); variants map to props.
- Honour the brand values and interaction rules in `design-system.md` (hover rules, WCAG 2.1 AA).

## MCP usage rules

- Load the matching Figma skill/tool guidance before writing to Figma (`figma-use`, `figma-generate-design`, `figma-generate-diagram`, `figma-design-to-code`).
- Read before write: inspect the file's existing pages, components and variables; reuse, do not duplicate.
- Build incrementally, one screen or section at a time, and verify each.
- Implementing from Figma: fetch design context for the exact node, then translate to `core-ui` components and tokens, not pixel-copied CSS (see `react-design.md`).

## Related skills

`design-system.md` (tokens, hierarchy), `react-design.md` (component design), the project's user-flow skill, `web.md`.
