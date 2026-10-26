"""Tests for the generic hooks: lint target resolution and the Claude adapter.

Run from the .ai-config directory: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import json
import os
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


class SessionContextTest(unittest.TestCase):
    def test_injects_the_generic_policy_text(self) -> None:
        result = subprocess.run(
            [sys.executable, str(HOOKS / "session-context.py")],
            input="{}",
            capture_output=True,
            text=True,
            check=True,
        )
        text = json.loads(result.stdout)["additional_context"]
        self.assertIn("Generic agent constraints", text)
        self.assertIn("type(domain/context)/area: imperative summary", text)

    def test_core_is_slim_and_full_adds_implementation_text(self) -> None:
        def run(*args: str) -> str:
            result = subprocess.run(
                [sys.executable, str(HOOKS / "session-context.py"), *args],
                input="{}", capture_output=True, text=True, check=True,
            )
            return json.loads(result.stdout)["additional_context"]

        core, full = run(), run("--full")
        self.assertNotIn("Hexagonal architecture", core)
        self.assertIn("Delegate", core)
        self.assertIn("Hexagonal architecture", full)


class PromptContextTest(unittest.TestCase):
    def _run(self, prompt: str, session_id: str) -> dict:
        result = subprocess.run(
            [sys.executable, str(HOOKS / "prompt-context.py")],
            input=json.dumps({"prompt": prompt, "session_id": session_id}),
            capture_output=True, text=True, check=True,
        )
        return json.loads(result.stdout)

    def test_ops_prompt_gets_nothing(self) -> None:
        self.assertEqual(self._run("is production up to date?", "t-ops"), {})

    def test_implementation_prompt_injects_once_per_session(self) -> None:
        sid = f"t-impl-{os.getpid()}"
        marker = Path(tempfile.gettempdir()) / f"ai-config-impl-{sid}"
        marker.unlink(missing_ok=True)
        try:
            first = self._run("implement the refund use case", sid)
            self.assertIn("Hexagonal architecture", first["additional_context"])
            self.assertEqual(self._run("add another test", sid), {})
        finally:
            marker.unlink(missing_ok=True)


class PostToolTest(unittest.TestCase):
    def test_messages_per_file_type(self) -> None:
        import importlib.util

        spec = importlib.util.spec_from_file_location("post_tool", HOOKS / "post-tool.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        def msgs(tool: str, path: str) -> list[str]:
            return mod.build_messages({"tool_name": tool, "tool_input": {"file_path": path}})

        self.assertTrue(any("Robot" in m for m in msgs("Write", "/r/kapita/testing/e2e/backend/a.robot")))
        self.assertTrue(any("Frontend" in m for m in msgs("Write", "/r/kapita/frontend-web/x/a.tsx")))
        self.assertTrue(any("Python" in m or "python" in m for m in msgs("Write", "/r/kapita/scripts/a.sh")))
        self.assertEqual(msgs("Edit", "/r/kapita/testing/e2e/backend/a.robot"), [])
        self.assertEqual(msgs("Write", "/r/kapita/docs/a.md"), [])


if __name__ == "__main__":
    unittest.main()
