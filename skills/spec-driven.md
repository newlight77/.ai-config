# Spec-Driven Development (triple loop, reviews, consolidation)

**When to use:** Implementing, documenting or investigating a piece of intent that has (or should have) a spec in a domain's `specs/` folder; picking "the next thing to do" in a domain; writing a new spec; handling a spec in review; consolidating a finished spec into the docs.

**Conventions (the project supplies the paths):** a spec per file `SPEC-<CODE>-<NNN>-<slug>.md` in `<domain>/specs/`; a queue `specs/queue.yaml` per domain; a generated global queue (never edited by hand); spec, queue and review-checklist templates; a queue generator with a `--check` mode. Kapita: `docs/architecture/domains/` (`QUEUE.md`, `_templates/`), `make generate-spec-queue`, ADRs 0048 and 0049. **Tool side** (queue generation, status checks, tube view): Shipdeck spec tube skill.

## Lifecycle

`draft` → `ready` → `in-progress` → `functional-review` → `technical-review` → `done` (or `rejected`).

| Step of the workflow | Status | Who |
|---|---|---|
| 1 User story created with its materials and the spec | `draft` | owner team |
| 2 Spec (updated if needed) put in the queue | `draft` → `ready` | owner team |
| 3 Spec picked | `ready` → `in-progress` | **you** |
| 4 Triple loop | `in-progress` | **you** |
| 5 Functional review | `functional-review` | a person |
| 6 Technical review | `technical-review` | a person |
| 7 Consolidate into the documentation | `done` | owner team (you may draft it) |
| 8 Pick another spec, or re-iterate | next pick, or `done` → `draft` / `ready` | owner team |

**You run steps 3 and 4 and stop at `functional-review`.** Never write a review line and never set `done` yourself: reviews are signed by people.

## 1. Pick (step 3)

1. Open the global queue ("Next up"), or the domain's `queue.yaml` when the task names a domain. Take the **topmost** entry; `in-progress` comes before `ready`.
2. Only `ready` specs can be picked. A `draft` spec is not work to start: list its open questions to the owner team instead. A spec in review is waiting for a person, not for you. Never reorder a queue (the owner team sets the order).
3. Set the spec `in-progress` in **both** the spec front matter and `queue.yaml`, then regenerate the global queue.

## 2. Loop 1 — BSDD (behavior)

- Read the spec's user story (front matter `story`), business case, persona, flow, behaviors and examples, plus the linked events, rules, use cases, flows and the context's `behavior.md`.
- If a behavior is unclear, contradicts a rule, or an example is missing: **stop**, write the gap as a question on the spec (`- [ ] … — answered by <who>`), set the spec back to `draft`, and tell the person. Do not guess.
- `documentation` and `investigation` specs end after this loop: produce the doc change or the written finding, then go to step 5.

## 3. Loop 2 — ASDD (acceptance)

- Turn each Loop 2 scenario into a functional (Robot) scenario of the context or a feature test. Tag Robot scenarios `SPEC-<CODE>-<NNN>` next to their existing tags; follow `testing.md` for vocabulary.
- Run them and **see them fail for the right reason** before writing code. Functional tests never target a product's production environment.

## 4. Loop 3 — TDD (inner loop, three levels)

- **Feature** level first: the integrated slice, driver to driven, that turns the Loop 2 scenarios green. Then the **use-case** level (ports faked, the domain corner cases), then the **unit / UI** level (narrow adapter boundary tests, component behavior; `testing.md`). Red, green, refactor at each.
- Keep the change inside the spec's scope. Anything else found on the way becomes a new `draft` spec or a hot spot, not part of this change.
- Run the Loop 2 scenarios again at the end: all green, none skipped.

## 5. Hand over for review (step 4 → 5)

1. Fill in **Evidence** on the spec (pull request, test runs) and tick the Loop 1 to 3 boxes of the definition of done.
2. Set `status: functional-review` in the spec and in `queue.yaml`; regenerate the global queue; commit the queue and the manifest.
3. The pull request names the spec ID and carries the evidence ([`evidence.md`](evidence.md)). **Stop.** Tell the person the spec is waiting in "In review".

## 6. Reviews (steps 5 and 6) — people, not you

- Reviewers follow the project's review checklist template. The reviewer writes the **Functional review** line (`<reviewer · date · accepted | changes requested — feedback>`, plus an optional **Evidence (functional review)** line when that review ran on its own pull request), then the spec goes to `technical-review` and the **Technical review** line is written (likewise with its own optional **Evidence (technical review)** line).
- `changes requested`: the spec goes back to `in-progress`. Pick it up again from the feedback on the spec, redo the affected loops, and hand over again (section 5).

## 7. Consolidate (step 7)

Once both reviews are accepted, the documentation must carry the new behavior. In the **same** pull request or a follow-up that names the spec:

- Update **any doc** the change touches: the context's `behavior.md`, the domain model (events, rules, policies, use cases, flows, closed hot spots), product, testing or deployment docs.
- **Add or update an ADR** when the change makes or changes an architecture decision.
- **Add or update a documentation article** when the change tells a story the documentation should carry (with its catalog entry), then run the project's documentation consistency check.
- Write the **Consolidated** line on the spec: the `docs/…` paths updated, in `backticks`. The checker verifies that each exists. Then set `status: done` in the spec and in `queue.yaml`, regenerate the global queue, commit it. The owner team confirms.

## 8. Next (step 8)

- **Pick another spec:** back to section 1.
- **Re-iterate a spec:** set it `draft` (or `ready` when Loops 1 and 2 are complete again), raise `revision` by one, add a line to its **Revision log**, update `queue.yaml`. The ID never changes.

## Writing a spec

- Copy the template; take the next `NNN` for the domain code (IDs never change or get reused); add the entry to `queue.yaml`; start at `draft` with `revision: 1`.
- Put its user story in `story` (`US-<CODE>-<NNN>`, title, epic, feature) and in the domain's story map. Implementation specs need it to be `ready`.
- A spec is `ready` only with Loop 1 and Loop 2 complete, a user story, no open question, and the owner team's agreement.
- **Back-filling** existing behavior: write the spec `done`, point Loop 2 at the existing tests, tag those Robot scenarios. It is reviewed like any other spec (the reviewers confirm it matches what is built).
- Check with the queue generator's `--check` mode (also run by the pre-commit hook where the project has one).
