# Mobile (Frontend) Skills

**When to use:** Flutter, Dart, `frontend-mobile/`.

**Canonical (structure):** the project's `docs/architecture/1.atomic-hexagonal-architecture.md` § *Frontend mobile — app shell and placement*. **Molecules:** `docs/architecture/2.design-system.md` § *Mobile shell molecules*.

- Widget hierarchy: atoms → molecules → organisms → templates
- Tokens via `AppPalette` / theme (`.ai-config/skills/design-system.md`)
- Riverpod, GoRouter, Dio/Retrofit; export screens via `regions.dart` and `package:<context>/<context>.dart`
- Coverage: `docs/testing/Coverage-Thresholds.md` (widget tests for `core-ui` and extracted presentation)

## Splitting oversized screens

Same rules as the architecture doc § Frontend mobile — app shell and placement; Flutter-specific habits below.

1. **Shells** — Reuse or add layout widgets in `core-ui` (molecule catalog above); `molecules.dart` + widget tests; context owns copy and fields.
2. **Screen** — `presentation/screens/` in the owning package; export via `regions.dart` and context barrel.
3. **Featured** — `presentation/featured/` and `widgets/`; `CustomPainter` in `feature/`.
4. **App stub** — `apps/app-mobile/lib/screens/<route>.dart` re-exports only.
5. **Ports** — Extend ports/providers and test fakes; no `driven/http` in presentation.

**Tests:** widget tests for new `core-ui` widgets; widget/feature tests in the owning context; app tests import presentation helpers from context barrels (not from `app-mobile`). Web uses the same placement model in the architecture doc § Design system and atomic design.

## Flutter refactor habits

- Prefer `StatelessWidget` / `ConsumerWidget`; push state to `ConsumerStatefulWidget` or notifiers only when needed.
- Extract repeated subtrees as top-level widgets with `const` constructors; generic → `core-ui`, domain → context `presentation/`.
- Keep `CustomPainter` and overlays in `feature/`; parents handle layout and `RepaintBoundary`.
- Split huge `State` classes with mixins or `part` files only when navigation improves; prefer small collaborators under `presentation/`.
- Required constructor args and `@immutable` widgets over deep `Map` payloads.

## Lint before finishing (mandatory)

After **any** Dart change (`lib/`, `test/`, or app shell under `apps/`), **before ending the agent turn or committing**:

1. **Run package lint** on every package you touched:
   ```bash
   make -C frontend-mobile lint-package PACKAGE=<path-under-frontend-mobile>
   ```
   Examples:
   - `make -C frontend-mobile lint-package PACKAGE=packages/domains/<domain>/<context>`
   - `make -C frontend-mobile lint-package PACKAGE=apps/app-mobile`
2. **Fix all `flutter analyze` issues** reported for that package (unused imports, type errors, deprecated APIs).
3. **Format** when needed: `make -C frontend-mobile format-package PACKAGE=…` (or workspace `make format` before commit).

Composer hooks track touched packages (`.ai-config/hooks/post-tool-lint-track.py`); the **stop** hook lists commands for backend, web, and mobile edits this session.
