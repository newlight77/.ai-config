# Shell and Agent Terminal Skills

**When to use:** Running shell commands from an AI coding agent such as Cursor or Claude Code (Shell tool, spawned terminals, migration scripts, bulk file copies).

## Python-first for repo scripts

When adding utilities under `scripts/`, **prefer Python** (`python3 scripts/<name>.py`) over new Bash scripts. Shell is fine for thin Makefile glue, required executable hooks, or documented legacy helpers — see `.ai-config/skills/scripts.md`.

Composer reminds agents via `post-tool.py` when a new `scripts/*.sh` file is written.

## Non-interactive copy (macOS)

Many dev machines alias `cp` to `cp -i`. In that setup, `cp -f` **still** prompts `overwrite …? (y/n [n])` because the alias expands to `cp -i -f`.

**Always use the system binary for forced copies:**

```bash
/bin/cp -f source dest
/bin/cp -f source …/target_directory/
```

Do **not** rely on `cp -f`, `command cp -f`, or unaliasing unless the script explicitly documents it.

## Agent-spawned terminals

Terminals started by the agent often have **no interactive stdin**. Commands that prompt for `y/n`, passwords, pagers (`less`), or editors will appear hung and the user cannot type answers.

- Prefer **non-interactive** flags and binaries (`/bin/cp -f`, `-y`, `--yes`, `DEBIAN_FRONTEND=noninteractive`, etc.).
- If a command might prompt, rewrite it before running (e.g. `/bin/cp -f` instead of `cp`).
- Do not ask the user to answer prompts in an agent terminal; fix the command or run a non-interactive variant via the Shell tool.

## Cluster and production access

Cluster access is SSH-key only. Shell commands that use SSH, Docker, or gpg against the cluster **must** run outside the sandbox (`required_permissions: ["all"]` in Cursor). Full workflow:
`.ai-config/skills/kubernetes-cluster.md`.

## Bulk copy loops (example)

```bash
for f in $(find test/unit/… -name '*_test.dart'); do
  rel="${f#test/unit/}"
  dest="test/feature/$rel"
  mkdir -p "$(dirname "$dest")"
  /bin/cp -f "$f" "$dest"
done
```
