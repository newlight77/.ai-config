#!/usr/bin/env python3
"""postToolUse (Write): nudge small-component refactor principles for frontend files."""
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


def _is_frontend_target(path: str) -> bool:
    norm = path.replace("\\", "/")
    in_web = "/frontend-web/" in norm and norm.endswith((".ts", ".tsx", ".css"))
    in_mobile = "/frontend-mobile/" in norm and norm.endswith(".dart")
    return in_web or in_mobile


def _is_page_or_banner_surface(path: str) -> bool:
    norm = path.replace("\\", "/")
    if "/presentation/pages/" in norm and norm.endswith((".tsx", ".css")):
        return True
    if norm.endswith("-page.css"):
        return True
    if "/presentation/components/" in norm and (
        "Panel" in norm or "Banner" in norm or "Page" in norm
    ):
        return True
    return False


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
    if not path or not _is_frontend_target(path):
        json.dump({}, sys.stdout)
        return

    msg = (
        "Frontend refactor habit (web + mobile): keep components/widgets small and composable. "
        "Prefer extracting reusable UI pieces, moving orchestration into hooks/use-cases, "
        "and keeping rendering logic focused with explicit typed props/contracts."
    )
    if _is_page_or_banner_surface(path):
        msg += (
            " Web pages/banners/buttons: harmonise with design-system.md § "
            "Harmonising new web pages, banners, and buttons "
            "(GlassCard, CardSection, kapita-form-button, token CSS, interactive-surface hover)."
        )
    json.dump({"additional_context": msg}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
