#!/usr/bin/env python3
"""postToolUse (Write|StrReplace|Edit): track packages that need lint (backend, web, mobile)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HOOK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(HOOK_DIR))

from code_lint_targets import resolve_lint_target, track_target, write_path  # noqa: E402

_STACK_SKILL = {
    "backend": ".ai-config/skills/backend.md § Lint before finishing",
    "web": ".ai-config/skills/web.md § Lint before finishing",
    "mobile": ".ai-config/skills/mobile.md § Lint before finishing",
}


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        json.dump({}, sys.stdout)
        return

    if data.get("tool_name") not in {"Write", "StrReplace", "Edit"}:
        json.dump({}, sys.stdout)
        return

    path = write_path(data.get("tool_input"))
    if not path:
        json.dump({}, sys.stdout)
        return

    target = resolve_lint_target(path)
    if target is None:
        json.dump({}, sys.stdout)
        return

    if not track_target(target):
        json.dump({}, sys.stdout)
        return

    skill = _STACK_SKILL.get(target.stack, ".ai-config/skills/kapita-skills.md")
    msg = (
        f"Kapita {target.stack} lint: you edited code under `{target.package}`. "
        f"Before finishing this task, run `{target.cmd}` and fix all reported errors "
        f"(see {skill}). The stop hook lists every package touched this session."
    )
    json.dump({"additional_context": msg}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
