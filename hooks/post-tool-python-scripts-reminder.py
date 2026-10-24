#!/usr/bin/env python3
"""postToolUse (Write): prefer Python for new repo scripts under scripts/."""
from __future__ import annotations

import json
import sys
from typing import Any


def _write_path(tool_input: Any) -> str | None:
    if not isinstance(tool_input, dict):
        return None
    for key in ("path", "file_path", "target_file", "relative_workspace_path"):
        val = tool_input.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        json.dump({}, sys.stdout)
        return

    if data.get("tool_name") != "Write":
        json.dump({}, sys.stdout)
        return

    path = _write_path(data.get("tool_input"))
    if not path:
        json.dump({}, sys.stdout)
        return

    norm = path.replace("\\", "/")
    if "/scripts/" not in norm or not norm.endswith(".sh"):
        json.dump({}, sys.stdout)
        return
    if norm.endswith("/install-git-hooks.sh") or norm.endswith("/merge-git.sh"):
        json.dump({}, sys.stdout)
        return

    msg = (
        "Kapita scripts: prefer Python (`python3 scripts/<name>.py`) for new repo utilities "
        "under `scripts/` (stdlib only when possible). Shell is acceptable for thin Makefile "
        "glue, git hooks that must be executable, or platform-specific one-liners — see "
        "`.ai-config/skills/scripts.md`."
    )
    json.dump({"additional_context": msg}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
