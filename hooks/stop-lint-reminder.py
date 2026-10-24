#!/usr/bin/env python3
"""stop: remind agent to run lint on every package edited this session."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HOOK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(HOOK_DIR))

from code_lint_targets import clear_state, load_state  # noqa: E402

_STACK_HEADING = {
    "backend": "Backend (ruff + mypy per package)",
    "web": "Web (eslint; add type-check / app build when TS or CSS @apply changed)",
    "mobile": "Mobile (flutter analyze per package)",
}

_STACK_SKILL = {
    "backend": ".ai-config/skills/backend.md § Lint before finishing",
    "web": ".ai-config/skills/web.md § Lint before finishing",
    "mobile": ".ai-config/skills/mobile.md § Lint before finishing",
}


def main() -> None:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass

    state = load_state()
    targets = state.get("targets", {})
    if not targets:
        json.dump({}, sys.stdout)
        return

    by_stack: dict[str, list[dict[str, str]]] = {}
    for item in targets.values():
        stack = item.get("stack", "backend")
        by_stack.setdefault(stack, []).append(item)

    lines = [
        "Before ending this task, run lint on every package you edited and fix all errors:"
    ]
    for stack in ("backend", "web", "mobile"):
        items = by_stack.get(stack)
        if not items:
            continue
        lines.append("")
        lines.append(f"**{_STACK_HEADING[stack]}**")
        for item in items:
            cmd = item.get("cmd")
            label = item.get("label", item.get("key", "package"))
            if cmd:
                lines.append(f"- **{label}**: `{cmd}`")
            extra = item.get("extra", "").strip()
            if extra:
                lines.append(f"  - {extra}")

    lines.extend(
        [
            "",
            "Policy: `.ai-config/rules/generic-rules.md` (lint before finish). "
            f"Backend: {_STACK_SKILL['backend']}. "
            f"Web: {_STACK_SKILL['web']}. "
            f"Mobile: {_STACK_SKILL['mobile']}.",
        ]
    )

    clear_state()
    json.dump({"followup_message": "\n".join(lines)}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
