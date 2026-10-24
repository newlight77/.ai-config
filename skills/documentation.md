# Documentation Skills

**When to use:** API contracts, migration docs, PR descriptions. When you change **repo-wide AI instructions**, keep the workspace `AGENTS.md`, the `.ai-config/` layers and the authoritative `docs/` aligned (see [`canonical.md`](../canonical.md)).

- Update design and API contracts when behavior changes
- Use the Evidence Template per change (`.ai-config/skills/evidence.md`)
- **Commits:** subject `type(domain/context)/area: imperative summary` (Conventional Commits; `area` values are project-defined); blank line then body. See `evidence.md` § Commit message and `.ai-config/hooks/session-context.md`
- Keep docs minimal but traceable and linked to PRs
- Document migration steps and rollback plans for DB changes
- Document breaking changes, deprecations and user-facing changelog entries when shipping behavior or contract changes
- Maintain component docs (Storybook/Widgetbook)
- When design-system behavior changes (hover rules, tokens, placement), update the design-system doc, `design-system.md` and the stylesheet that implements it together
- When mobile screens or widgets move between the app shell and domain contexts, or shell widgets are promoted to `core-ui`, update the architecture doc (§ Frontend mobile — app shell and placement), the design-system doc (§ Mobile shell molecules) and `mobile.md`
- Keep README and `.ai-config` rules/skills/workflow (and hooks, if policy changes) aligned when processes or architecture change
- When adding repo utilities under `scripts/`, update `scripts/README.md` and `scripts.md` (Python-first policy)

## Where domain documentation goes

Docs are sliced **sub-product → domain → context**, each slice with one owner team. Keep the index, owners and templates in one place (`docs/architecture/domains/README.md`, `_templates/`), copy the matching template rather than inventing a layout, and update a context's `behavior.md` (and the domain model when a rule, event or policy changed) in the same change as the behavior. Cross-cutting docs (product, testing, deployment, design) stay in their own folders; a domain extracts its part and links back. Layout and front matter of Kapita's slices: `kapita-documentation.md`. The documentation tube that serves them: `shipdeck-documentation-tube-skills.md` in the Shipdeck layer.

## Authoritative docs — frontmatter (where applicable)

For `docs/architecture/`, `docs/testing/` and other long-lived reference docs, include YAML frontmatter when the repo or CI expects it:

- `title`, `owner` (team or role), `update_cadence` (e.g. `daily` | `weekly` | `monthly` | `quarterly`)
- `source_of_truth`: `true` only for documents that define contracts (see `canonical.md`)
- `checkpoints`: optional list of relevant review gates

Non-authoritative docs reference the authoritative architecture and testing sources (`docs/architecture/1.atomic-hexagonal-architecture.md`, `docs/testing/Testing-Strategy.md`). State in the Evidence Template which doc versions were consulted.

## Robot Framework E2E and functional scenarios

- **Scenario source of truth:** add or update user-centric flows in `docs/testing/Test-Scenarios.md` before (or alongside) Robot suites under `testing/e2e/backend/`.
- **README hierarchy:** `testing/README.md` (index + conventions) → `testing/e2e/backend/README.md` (commands, tags, vocabulary tables). The root `README.md` links to these under **Functional E2E Testing**.
- **Vocabulary:** functional Robot test cases use **business-domain language** only in titles and documentation; technical HTTP/JSON details belong in `libraries/ApiLibrary.py` and resource keyword bodies. See the Robot Framework E2E section in `testing.md`.
