#!/usr/bin/env python3
"""sessionStart: inject the generic policy text into composer additional_context."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    # Consume hook input (session_id, composer_mode, …)
    try:
        raw = sys.stdin.read()
        if raw.strip():
            json.loads(raw)
    except json.JSONDecodeError:
        pass

    hook_dir = Path(__file__).resolve().parent
    md_path = hook_dir / "session-context.md"
    text = (
        md_path.read_text(encoding="utf-8")
        if md_path.is_file()
        else "[Generic hook] session-context.md missing; restore from the .ai-config repository.\n"
    )
    json.dump({"additional_context": text}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
