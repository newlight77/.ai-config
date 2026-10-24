# Canonical Source (Generic Layer)

For conflicts or ambiguity, apply this order:

1. **Generic rules** (`.ai-config/rules/generic-rules.md`) – Mandatory
2. **Layer rules** – `kapita/.ai-config/rules/kapita-rules.md` for product work, `shipdeck/.ai-config/rules/shipdeck-rules.md` for tool and platform work, which includes the build-site add-on `rules/enabler-rules.md` (a layer rule wins over a generic rule on its own ground)
3. **Skills** (`.ai-config/skills/*.md`, then the layer's `*-skills.md` index) – Context-dependent
4. **Architecture** (the project's `docs/architecture/1.atomic-hexagonal-architecture.md`) – Source of truth for structure
5. **Testing** (the project's `docs/testing/Testing-Strategy.md`) – Source of truth for test strategy

Each layer keeps its own `canonical.md` for the documents it owns: `kapita/.ai-config/canonical.md` (product docs) and `shipdeck/.ai-config/canonical.md` (ADRs, platform and build-site docs).

**Hooks:** the hooks registered at the workspace root inject session context from `.ai-config/hooks/session-context.md` and the layer's own session text. That text is derived from the items above; if anything conflicts, use **this order**, not the hook text alone.

**Entry point:** the workspace `AGENTS.md` describes the same read order for humans and tools.

## Constraints

- Use existing Makefile targets; do not invent new commands
- Consult authoritative docs when producing designs; link versions in Evidence Template
