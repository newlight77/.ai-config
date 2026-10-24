"""Tests for the generic hooks: lint target resolution and the Claude adapter.

Run from the .ai-config directory: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1] / "hooks"
sys.path.insert(0, str(HOOKS))

from code_lint_targets import resolve_lint_target  # noqa: E402

PKG = "backend/packages/domains/platform-domain/documentation-context/src/a.py"


class ResolveLintTargetTest(unittest.TestCase):
    def test_repository_relative_backend_path(self) -> None:
        target = resolve_lint_target(PKG)
        self.assertIsNotNone(target)
        self.assertEqual(target.stack, "backend")
        self.assertEqual(
            target.cmd,
            "make -C backend lint-package "
            "PACKAGE=packages/domains/platform-domain/documentation-context "
            "MYPY_PACKAGE=documentation_context",
        )

    def test_workspace_relative_path_keeps_the_repository_prefix(self) -> None:
        target = resolve_lint_target(f"kapita/{PKG}")
        self.assertIsNotNone(target)
        self.assertTrue(target.cmd.startswith("make -C kapita/backend lint-package "))
        self.assertEqual(
            target.package, "packages/domains/platform-domain/documentation-context"
        )

    def test_absolute_path_keeps_the_absolute_prefix(self) -> None:
        target = resolve_lint_target(f"/w/repos/kapita/{PKG}")
        self.assertIsNotNone(target)
        self.assertTrue(
            target.cmd.startswith("make -C /w/repos/kapita/backend lint-package ")
        )

    def test_state_key_differs_per_repository(self) -> None:
        here = resolve_lint_target(f"kapita/{PKG}")
        there = resolve_lint_target(f"shipdeck/{PKG}")
        self.assertNotEqual(here.key, there.key)

    def test_backend_scripts(self) -> None:
        target = resolve_lint_target("kapita/backend/scripts/foo.py")
        self.assertEqual(
            target.cmd, "cd kapita/backend && poetry run ruff check scripts/foo.py"
        )

    def test_web_package(self) -> None:
        target = resolve_lint_target(
            "kapita/frontend-web/packages/core/lib/core-ui/src/Button.tsx"
        )
        self.assertEqual(target.stack, "web")
        self.assertEqual(
            target.cmd,
            "make -C kapita/frontend-web lint-package PACKAGE=packages/core/lib/core-ui",
        )

    def test_mobile_package(self) -> None:
        target = resolve_lint_target(
            "kapita/frontend-mobile/apps/app-mobile/lib/main.dart"
        )
        self.assertEqual(target.stack, "mobile")
        self.assertEqual(
            target.cmd,
            "make -C kapita/frontend-mobile lint-package PACKAGE=apps/app-mobile",
        )

    def test_unrelated_paths_are_ignored(self) -> None:
        for path in (
            "kapita/docs/architecture/a.md",
            "kapita/backend/README.md",
            "kapita/frontend-web/packages/core/lib/core-ui/README.md",
            "notes.py",
        ):
            self.assertIsNone(resolve_lint_target(path), path)


class ClaudeAdapterTest(unittest.TestCase):
    def test_child_runs_in_the_session_directory(self) -> None:
        with tempfile.TemporaryDirectory() as session:
            stub = Path(session) / "stub.py"
            stub.write_text(
                "import json, os\n"
                "print(json.dumps({'additional_context': os.getcwd()}))\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(HOOKS / "claude_output_adapter.py"), str(stub)],
                input=json.dumps({"hook_event_name": "SessionStart"}),
                capture_output=True,
                text=True,
                cwd=session,
                check=True,
            )
        out = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(out["hookEventName"], "SessionStart")
        self.assertEqual(Path(out["additionalContext"]).resolve(), Path(session).resolve())


if __name__ == "__main__":
    unittest.main()
