# Deep Bug Finding

**When to use:** Only when the user explicitly asks — e.g. "find bugs", "run deep bug-finding", "use the bug-finding skill", or "scan recent commits for critical bugs". Do **not** auto-run during normal implementation.

**Goal:** Inspect recent changes and identify **critical correctness bugs** that escaped review. Surface only issues that would cause data loss, crashes, security holes, or significant user-facing breakage.

## Before you start

1. Read **`.ai-config/bug-finding-memories.md`** — tracks bugs already reported across runs (one-line description, location/root cause, PR or commit link, status, date). **Do not** re-investigate or re-fix a bug that already has an **open** PR listed there.
2. Determine scope from the user (default: commits on the current branch since `origin/main`, or the last ~10 commits if no base is given).
3. Read the project's rules file (`.ai-config/rules/generic-rules.md` plus the repository's own rules), `.ai-config/skills/architecture.md`, and `.ai-config/skills/testing.md` when fixes touch production code.

## Investigation strategy

- Focus on **behavioral changes** with meaningful blast radius (auth, payments, ledgers, deletion flows, routing guards, async/threading, path resolution, env wiring).
- Look for: data corruption, race conditions that lose writes, null dereferences in critical paths, auth/permission bypasses, infinite redirect/render loops, resource leaks, silent data truncation, brittle path/index assumptions (e.g. `Path.parents[n]` on a serverless host), and tests that call live external services in CI.
- **Trace the full code path** — caller chain and downstream effects. Do not pattern-match the diff alone.
- **Ignore:** style, minor edge cases without a concrete trigger, theoretical concerns, and low-severity UX degradation.

## Confidence bar

- You must describe a **concrete scenario** that triggers the bug.
- If you cannot construct a plausible trigger, **do not** implement a fix or open a PR.
- When uncertain, report findings in chat **without** changing code.

## Fix strategy (when a critical bug is confirmed)

- Implement a **minimal, high-confidence** fix aligned with the project's architecture and existing patterns.
- Add or update **tests** per `.ai-config/skills/testing.md` (use case tests with mocked ports; sanity tests must stay hermetic — no live network).
- Run targeted validation; record commands in the summary (see `.ai-config/skills/evidence.md`).
- **Avoid broad refactors** in the same change.
- **Do not commit or open a PR** unless the user asks — propose the fix and wait for approval.

## Avoiding duplicate work

For each finding that matches an entry in `.ai-config/bug-finding-memories.md`, check status:

| Status | Action |
|--------|--------|
| **open** | Do not open another PR. Note in the summary that a fix is still awaiting review; link the existing PR. |
| **merged** | Delete the entry — bug is fixed. |
| **rejected** | Keep entry; set status to `rejected`. Do not re-open unless the relevant code **materially changed** since. |
| **fixed elsewhere** | Delete the entry. |

Also delete **rejected** entries older than **30 days** — after that drift, the bug may warrant a fresh look.

Keep `.ai-config/bug-finding-memories.md` **small**: only open or rejected items with date recorded. Do not log run history or scan notes there.

## Safety rules

- Do not claim a bug is critical without a trigger scenario.
- Do not open a PR unless highly confident the bug is real **and** the fix is correct **and** the user requested a PR/commit.
- If no critical bug is found, post a short **"no critical bugs found"** summary with what was scanned. This is the expected outcome most of the time.

## Output format

### When a critical bug is found (and fixed or proposed)

```markdown
## Bug finding report

### Bug and impact
[What breaks, for whom, severity]

### Root cause
[File(s), mechanism]

### Fix and validation
[Change summary; tests added; commands run and results]

### Memory update
[Whether `.ai-config/bug-finding-memories.md` was updated]
```

### When no critical bug is found

```markdown
## Bug finding report

**Result:** No critical bugs found.

**Scope scanned:** [branch/commits/files reviewed]

**Notable non-critical observations:** [optional, brief — or omit]
```

## After opening a PR (user-requested only)

Before finishing, append to `.ai-config/bug-finding-memories.md`:

- Date (ISO)
- One line: location + root cause
- PR URL
- Status: `open`

Apply any pending cleanup from the table above in the same edit.
