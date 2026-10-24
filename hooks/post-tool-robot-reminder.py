#!/usr/bin/env python3
"""postToolUse (Write): nudge business-domain vocabulary for backend Robot E2E files."""
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
    if "/testing/e2e/backend/" not in norm and not norm.endswith("/testing/e2e/backend"):
        json.dump({}, sys.stdout)
        return
    if not norm.endswith(".robot"):
        json.dump({}, sys.stdout)
        return

    msg = (
        "Kapita Robot E2E: In Test Cases, [Documentation], and keywords invoked from test cases, "
        "use business-domain language only (no URLs, HTTP codes, header names, JSON field names, or wire jargon). "
        "Keep technical HTTP/JSON details in libraries/ApiLibrary.py and resource keyword bodies."
    )
    json.dump({"additional_context": msg}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
