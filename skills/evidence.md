# Evidence Template & Checkpoints

**When to use:** Completing change evidence, PR descriptions, validation before commit.

## Evidence Template (per change)

- Requirement: link or prompt reference, or the spec ID (`SPEC-<CODE>-<NNN>`) when the change implements a spec ([`spec-driven.md`](spec-driven.md)); the same evidence is copied to the spec's **Evidence** line before it moves to `functional-review`; if a review later happens on a separate pull request, that review also gets its own `Evidence (functional review)` / `Evidence (technical review)` line
- Scope: impacted domains/contexts
- Design: API/UI/data contracts summary
- Implementation: files changed and rationale
- Tests: unit (config, driver & driven adapters, narrow boundary cases only; **no** domain) / use case (real use-case class + **all ports** faked/mocked; corner cases for domain coverage; not relocated domain unit tests) / feature / UI / sanity / robot coverage added or updated
- Validation: build/test commands executed and results
- Risks: data migrations, performance, security considerations
- Rollback: how to undo/mitigate failures

## Commit message (required shape)

**Subject:** `type(domain/context)/area: imperative summary`: Conventional Commit **type**; **domain/context** in parentheses (e.g. `<domain>/<context>`); **area** after `/`, one of the values the project defines; then **`:`** and a concise summary. Kapita's areas: `backend`, `web`, `mobile`, `testing`, `docs`, `cursor`. For **docs-only** commits under `docs/`, the shorter `docs(domain/context): summary` without `/docs` is acceptable.

**Body:** blank line after the subject, then bullets or short paragraphs (what/why, pointers to tests or rollback). Examples: `.ai-config/hooks/session-context.md` § Commit messages.

**Optional Git check:** a commit-message validator wired through `core.hooksPath`, when the project provides one (Kapita: `scripts/git/validate_commit_message/`).

## Required Checkpoints

When executing changes, run the project's Makefile targets (do not invent commands). Default set:

- `make build`
- `make test-unit`
- `make test-use-case`
- `make test-feature`
- `make test-sanity`
- `cd testing && make test-e2e && cd -`
- `make format && make lint`
- `make test-regression`
