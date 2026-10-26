# Backend Skills

**When to use:** Python, FastAPI, database, migrations, ports/adapters, backend packages.

## Core Skills

- FastAPI + Pydantic idioms; async SQLAlchemy with psycopg
- Ports/adapters modeling; clear separation: use_cases, ports, services, entities, value_objects
- Split routes by responsibility (signin, signup, profile, password, refresh_token)
- Migration planning and backout steps; DB integration tests and fixtures
- Use existing Makefile targets and CI workflows

## Code Standards

- Use existing domain/use-case/adapter folder conventions; maintain context boundaries
- Explicit error types at boundaries; do not leak internal errors to API/UI
- Retry/timeout policies in adapters where required
- Consistent response envelopes for success/error; document contract changes in docs/api

## Lint before finishing (mandatory)

After **any** backend Python change (production `src/`, tests, or `backend/scripts/`), **before ending the agent turn or committing**:

1. **Run package lint** on every package you touched:
   ```bash
   make -C backend lint-package PACKAGE=<path-under-backend> MYPY_PACKAGE=<python_module>
   ```
   Examples:
   - `make -C backend lint-package PACKAGE=packages/domains/<domain>/<context> MYPY_PACKAGE=<context>`
   - `make -C backend lint-package PACKAGE=apps/<app> MYPY_PACKAGE=<app>`
2. **Scripts** under `backend/scripts/`: `cd backend && poetry run ruff check scripts/<file>.py` (or `poetry run ruff check .` when several root files changed).
3. **Fix all ruff and mypy errors** reported by that command — do not leave F401/F841/E402 or mypy `[arg-type]` / `[assignment]` for the next CI run.
4. **Auto-fix** only when safe: `make -C backend lint-fix`, then re-run the package lint command.
5. **Common patterns** (match existing code):
   - Imports after `sys.path` manipulation → `# noqa: E402` on those import lines.
   - Classic SQLAlchemy `Column()` models → `# type: ignore[arg-type]` / `[assignment]` when reading or assigning instance attributes in `_to_entity` (see the existing `_to_entity` mappers).
   - Optional internal deps in app `pyproject.toml` mypy overrides → add `your_context.*` to `[[tool.mypy.overrides]]` with `ignore_missing_imports = true` when needed.

Composer hooks track touched packages (`.ai-config/hooks/post-tool.py`) and the **stop** hook lists lint commands to run before declaring the task done.

## Logging (JSON)

Structured JSON with: timestamp, level, service, env, correlation_id, request_id, user_id, actor, operation, resource, status, duration_ms, error_code, error_message, trace_id, span_id, version.

- Never log PII or secrets; redact sensitive fields
- Log at ingress/egress boundaries; propagate correlation IDs across all calls
