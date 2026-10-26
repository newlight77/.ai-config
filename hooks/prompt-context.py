#!/usr/bin/env python3
"""userPromptSubmit: inject the implementation constraints once per session, only for code-work prompts.

Extra markdown files (layer-specific implementation text) are passed as arguments, relative to the
session's project directory.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

_IMPLEMENTATION = re.compile(
    r"\b(implement\w*|add(?:ing)?|creat\w+|fix\w*|bug|refactor\w*|rewrit\w+|writ(?:e|ing)|edit\w*|"
    r"chang\w+|updat\w+|remov\w+|renam\w+|extract\w*|migrat\w+|scaffold\w*|"
    r"tests?|robot|e2e|lint\w*|format|endpoint|component|page|hook|hexagon\w*|use[- ]case|"
    r"adapter|port|feature|code|backend|frontend|mobile|web|commit)\b",
    re.IGNORECASE,
)


def _already_injected(session_id: str) -> bool:
    marker = Path(tempfile.gettempdir()) / f"ai-config-impl-{re.sub(r'[^A-Za-z0-9_-]', '', session_id)}"
    if marker.exists():
        return True
    try:
        marker.touch()
    except OSError:
        pass
    return False


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        data = {}
    prompt = data.get("prompt") if isinstance(data, dict) else None
    session_id = data.get("session_id") if isinstance(data, dict) else None

    if not isinstance(prompt, str) or not _IMPLEMENTATION.search(prompt):
        json.dump({}, sys.stdout)
        return
    if isinstance(session_id, str) and session_id and _already_injected(session_id):
        json.dump({}, sys.stdout)
        return

    hook_dir = Path(__file__).resolve().parent
    parts = [hook_dir / "session-context-impl.md", *(Path(a) for a in sys.argv[1:])]
    text = "\n".join(p.read_text(encoding="utf-8") for p in parts if p.is_file())
    if not text.strip():
        json.dump({}, sys.stdout)
        return
    json.dump({"additional_context": text}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
