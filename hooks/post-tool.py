#!/usr/bin/env python3
"""postToolUse (Write|StrReplace|Edit): one process for the file-type nudges and the lint tracking.

- Write only: Robot E2E vocabulary, frontend small-component habit, Python-first `scripts/`.
- Write|StrReplace|Edit: track backend/web/mobile packages that need lint.
"""
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

_SCRIPT_EXEMPT = ("/install-git-hooks.sh", "/merge-git.sh")


def _robot(norm: str) -> str | None:
    if "/testing/e2e/backend/" in norm and norm.endswith(".robot"):
        return (
            "Robot E2E: in Test Cases, [Documentation] and keywords invoked from test cases use "
            "business-domain language only (no URLs, HTTP codes, header names, JSON fields, wire jargon). "
            "Keep technical HTTP/JSON in libraries/ApiLibrary.py and resource keyword bodies."
        )
    return None


def _is_page_or_banner_surface(norm: str) -> bool:
    if "/presentation/pages/" in norm and norm.endswith((".tsx", ".css")):
        return True
    if norm.endswith("-page.css"):
        return True
    return "/presentation/components/" in norm and any(k in norm for k in ("Panel", "Banner", "Page"))


def _frontend(norm: str) -> str | None:
    in_web = "/frontend-web/" in norm and norm.endswith((".ts", ".tsx", ".css"))
    in_mobile = "/frontend-mobile/" in norm and norm.endswith(".dart")
    if not (in_web or in_mobile):
        return None
    msg = (
        "Frontend refactor habit (web + mobile): keep components/widgets small and composable; extract "
        "reusable UI, move orchestration into hooks/use-cases, use explicit typed props/contracts."
    )
    if _is_page_or_banner_surface(norm):
        msg += (
            " Web pages/banners/buttons: harmonise with design-system.md § Harmonising new web pages, "
            "banners, and buttons (GlassCard, CardSection, kapita-form-button, token CSS, interactive-surface hover)."
        )
    return msg


def _scripts(norm: str) -> str | None:
    if "/scripts/" in norm and norm.endswith(".sh") and not norm.endswith(_SCRIPT_EXEMPT):
        return (
            "Scripts: prefer Python (`python3 scripts/<name>.py`, stdlib when possible) for new utilities "
            "under `scripts/`; shell only for thin Makefile glue, executable git hooks, platform one-liners "
            "(`.ai-config/skills/scripts.md`)."
        )
    return None


def _lint(path: str) -> str | None:
    target = resolve_lint_target(path)
    if target is None or not track_target(target):
        return None
    skill = _STACK_SKILL.get(target.stack, ".ai-config/skills/generic-skills.md")
    return (
        f"{target.stack.capitalize()} lint: you edited code under `{target.package}`. "
        f"Before finishing this task, run `{target.cmd}` and fix all reported errors "
        f"(see {skill}). The stop hook lists every package touched this session."
    )


def build_messages(data: object) -> list[str]:
    if not isinstance(data, dict):
        return []
    tool = data.get("tool_name")
    if tool not in {"Write", "StrReplace", "Edit"}:
        return []
    path = write_path(data.get("tool_input"))
    if not path:
        return []
    norm = path.replace("\\", "/")
    found = [_robot(norm), _frontend(norm), _scripts(norm)] if tool == "Write" else []
    found.append(_lint(path))
    return [m for m in found if m]


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        data = None
    messages = build_messages(data)
    if not messages:
        json.dump({}, sys.stdout)
        return
    json.dump({"additional_context": "\n".join(messages)}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
