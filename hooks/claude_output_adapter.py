#!/usr/bin/env python3
"""Claude Code hook adapter.

The scripts in this directory were written for Cursor's hook contract —
they read the hook's stdin JSON and print `{"additional_context": "..."}`
(or, for the stop hook, `{"followup_message": "..."}`). Claude Code expects
a different output shape: `{"hookSpecificOutput": {"hookEventName": ...,
"additionalContext": "..."}}`.

Rather than duplicate every script's logic for each tool's contract, this
adapter runs the given script unchanged (same stdin, same working
directory) and re-wraps whatever Cursor-shaped JSON it prints into the
shape Claude Code understands. Usage (from `.claude/settings.json`):

    python3 .ai-config/hooks/claude_output_adapter.py .ai-config/hooks/<script>.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 2:
        print("usage: claude_output_adapter.py <script.py> [args...]", file=sys.stderr)
        sys.exit(1)

    target = sys.argv[1]
    target_args = sys.argv[2:]

    raw_stdin = sys.stdin.read()
    try:
        stdin_data = json.loads(raw_stdin) if raw_stdin.strip() else {}
    except json.JSONDecodeError:
        stdin_data = {}

    event_name = stdin_data.get("hook_event_name", "")

    result = subprocess.run(
        [sys.executable, target, *target_args],
        input=raw_stdin,
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parents[2],
    )

    try:
        child_output = json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        child_output = {}

    text = child_output.get("additional_context") or child_output.get("followup_message")
    if not text:
        json.dump({}, sys.stdout)
        return

    json.dump(
        {"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": text}},
        sys.stdout,
        ensure_ascii=False,
    )
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
