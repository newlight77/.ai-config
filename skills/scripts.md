# Repository Scripts Skills

**When to use:** Adding or changing utilities under `scripts/`, Makefile helpers, git hooks, or repo-wide Python tooling.

## Python-first

- **Layout:** one folder per tool, **`scripts/<domain>/<tool>/<tool>.py`**, with a `README.md` beside it (purpose, pre-requisites, usage, impacts). Group tools by domain (for example `architecture`, `backend`, `ci`, `deploy`, `docs`, `git`, `make`, `testing`); add a domain only when none fits. A tool that imports another adds that tool's folder to `sys.path` explicitly.
- **Default:** implement new repo utilities as **`python3 scripts/<domain>/<tool>/<tool>.py`** (stdlib when possible; match the patterns of the existing tools).
- **Shell exceptions:** thin Makefile glue, hooks that must be executable shell, platform-specific one-liners, or documented legacy helpers — do not rewrite those without a concrete need.
- **Tests:** add `scripts/tests/test_<name>.py` (unittest) for non-trivial script logic. Doc generators may keep tests in `scripts/docs/tests/`.
- **Docs:** add or update the tool's `README.md` and its row in `scripts/README.md` when adding a script or changing CLI subcommands.

## Make target timing

Wrap aggregate `test`, `test-*`, `format`, `format-*`, `lint` and `lint-*` Makefile targets in a shared timing include (`scripts/make/make_timing/make-timing.mk`) that calls a small `make_time.py` helper (`run`, `finish`, `now`), so each target prints its duration:

```text
✓ unit tests <package> finished in 8s
✓ test-unit finished in 2m 15s
```

- **Aggregate targets** run an inner recipe through the timing wrapper.
- **Per-package steps** print their duration with `make_time.py finish` at the end of the run, format and lint defines.
- Project-specific wrapper names and the deploy scripts live in the project's scripts skill (Kapita: `kapita-scripts.md`).

## Generated files: build material vs committed input

Two kinds of machine-written file live in a repository, and they are handled in opposite ways. The test is **whether the build produces the file or consumes it.**

- **Build material — never committed.** Produced during a build (copied or generated from the repository's originals) and baked into the image, with no life in the repo afterwards. Gitignore it and edit the original, never the copy. If such a file is tracked, untrack it with `git rm --cached` (which keeps it on disk) and extend `.gitignore` — after confirming that the file really is generated (re-run the generator and watch it change) and that every consumer regenerates it, since untracking is only safe when nothing deploys straight from repository contents.
- **Committed input — stays tracked.** Written by a manual `make` target and then *consumed* by a build, so it must exist in git. These rot silently: guard freshness in CI with a `--check` mode that regenerates in memory, compares to the committed file without writing it, ignores volatile stamps (such as `generatedAt`), and fails when they differ. Regenerate and commit when it fails.

The documentation bundle, architecture map and releases timeline are the reference cases; their generators and the documentation-tube side are in `shipdeck-documentation-tube-skills.md` (Shipdeck) and `kapita-scripts.md` (Kapita files and targets).

## Agent reminders

- The **postToolUse** hook nudges toward Python when a new `scripts/*.sh` file is created (`.ai-config/hooks/post-tool.py`).
- Non-interactive terminal rules remain in `.ai-config/skills/shell.md` (`/bin/cp -f`, no interactive prompts).
