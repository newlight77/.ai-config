"""Resolve edited file paths to stack-specific lint commands (Composer hooks)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

STATE_FILE = Path(__file__).resolve().parent / ".code-lint-state.json"


@dataclass(frozen=True)
class LintTarget:
    stack: str
    key: str
    label: str
    package: str
    cmd: str
    extra: str = ""


def _mypy_module(folder_name: str) -> str:
    return folder_name.replace("-", "_")


def _monorepo_package(parts: list[str]) -> str | None:
    if len(parts) >= 2 and parts[0] == "apps":
        return f"apps/{parts[1]}"
    if len(parts) >= 4 and parts[0] == "packages" and parts[1] == "core" and parts[2] == "lib":
        return f"packages/core/lib/{parts[3]}"
    if len(parts) >= 4 and parts[0] == "packages" and parts[1] == "core" and parts[2] == "capabilities":
        return f"packages/core/enablers/{parts[3]}"
    if len(parts) >= 5 and parts[0] == "packages" and parts[1] == "domains":
        return f"packages/domains/{parts[2]}/{parts[3]}"
    return None


def _first_target(
    path: str, root: str, build: Callable[[str, str], "LintTarget | None"]
) -> "LintTarget | None":
    """Build a target for the first `root` segment of `path` that yields one.

    `prefix` is what precedes the stack root: empty at a repository root,
    `kapita/` from a workspace root, an absolute directory otherwise. Commands
    are built from it so they work whatever directory the session started in.
    """
    parts = path.replace("\\", "/").split("/")
    for index, part in enumerate(parts[:-1]):
        if part != root:
            continue
        prefix = "/".join(parts[:index]) + "/" if index else ""
        target = build(prefix, "/".join(parts[index + 1 :]))
        if target is not None:
            return target
    return None


def _backend_target(prefix: str, rel: str) -> LintTarget | None:
    if not rel.endswith(".py"):
        return None

    backend = f"{prefix}backend"
    parts = rel.split("/")

    if parts[0] == "scripts":
        return LintTarget(
            stack="backend",
            key=f"{prefix}backend-scripts",
            label="backend scripts",
            package=".",
            cmd=f"cd {backend} && poetry run ruff check {rel}",
            extra="Also run mypy when the script is type-checked in CI.",
        )

    package_path = _monorepo_package(parts)
    if package_path is not None:
        mypy = _mypy_module(package_path.rsplit("/", maxsplit=1)[-1])
        return LintTarget(
            stack="backend",
            key=f"{prefix}{package_path}",
            label=package_path.rsplit("/", maxsplit=1)[-1],
            package=package_path,
            cmd=f"make -C {backend} lint-package PACKAGE={package_path} MYPY_PACKAGE={mypy}",
            extra=(
                "Fix all ruff and mypy errors. Safe auto-fix: "
                f"`make -C {backend} lint-fix` then re-run package lint."
            ),
        )

    if len(parts) == 1 or parts[0] in {"make", "tools"}:
        return LintTarget(
            stack="backend",
            key=f"{prefix}backend-root",
            label="backend root",
            package=".",
            cmd=f"cd {backend} && poetry run ruff check .",
        )

    return None


def _web_target(prefix: str, rel: str) -> LintTarget | None:
    if Path(rel).suffix.lower() not in {".ts", ".tsx", ".css", ".mts"}:
        return None

    package_path = _monorepo_package(rel.split("/"))
    if package_path is None:
        return None

    web = f"{prefix}frontend-web"
    return LintTarget(
        stack="web",
        key=f"{prefix}{package_path}",
        label=package_path.rsplit("/", maxsplit=1)[-1],
        package=package_path,
        cmd=f"make -C {web} lint-package PACKAGE={package_path}",
        extra=(
            "For TypeScript errors, also run "
            f"`cd {web}/{package_path} && pnpm run type-check` "
            "when available. Tailwind `@apply` errors surface in app build "
            "(`pnpm run build` under the consuming app)."
        ),
    )


def _mobile_target(prefix: str, rel: str) -> LintTarget | None:
    if not rel.endswith(".dart"):
        return None

    package_path = _monorepo_package(rel.split("/"))
    if package_path is None:
        return None

    return LintTarget(
        stack="mobile",
        key=f"{prefix}{package_path}",
        label=package_path.rsplit("/", maxsplit=1)[-1],
        package=package_path,
        cmd=f"make -C {prefix}frontend-mobile lint-package PACKAGE={package_path}",
    )


def resolve_backend_lint_target(path: str) -> LintTarget | None:
    return _first_target(path, "backend", _backend_target)


def resolve_web_lint_target(path: str) -> LintTarget | None:
    return _first_target(path, "frontend-web", _web_target)


def resolve_mobile_lint_target(path: str) -> LintTarget | None:
    return _first_target(path, "frontend-mobile", _mobile_target)


def resolve_lint_target(path: str) -> LintTarget | None:
    for resolver in (
        resolve_backend_lint_target,
        resolve_web_lint_target,
        resolve_mobile_lint_target,
    ):
        target = resolver(path)
        if target is not None:
            return target
    return None


def write_path(tool_input: Any) -> str | None:
    if not isinstance(tool_input, dict):
        return None
    for key in ("path", "file_path", "target_file", "relative_workspace_path"):
        val = tool_input.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return None


def load_state() -> dict[str, dict[str, str]]:
    legacy = Path(__file__).resolve().parent / ".backend-lint-state.json"
    if legacy.is_file() and not STATE_FILE.is_file():
        try:
            legacy_data = json.loads(legacy.read_text(encoding="utf-8"))
            packages = legacy_data.get("packages", {})
            if isinstance(packages, dict):
                migrated = {
                    f"backend:{key}": {**value, "stack": "backend"}
                    for key, value in packages.items()
                    if isinstance(value, dict)
                }
                return {"targets": migrated}
        except (json.JSONDecodeError, OSError):
            pass

    if not STATE_FILE.is_file():
        return {"targets": {}}
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"targets": {}}
    targets = data.get("targets")
    if not isinstance(targets, dict):
        return {"targets": {}}
    return {"targets": targets}


def save_state(state: dict[str, dict[str, str]]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def clear_state() -> None:
    if STATE_FILE.is_file():
        STATE_FILE.unlink()
    legacy = Path(__file__).resolve().parent / ".backend-lint-state.json"
    if legacy.is_file():
        legacy.unlink()


def track_target(target: LintTarget) -> bool:
    """Record a lint target. Returns True when this target was newly tracked."""
    state = load_state()
    targets = state["targets"]
    state_key = f"{target.stack}:{target.key}"
    if state_key in targets:
        return False
    targets[state_key] = asdict(target)
    save_state(state)
    return True
