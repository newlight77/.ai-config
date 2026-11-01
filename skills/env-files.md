# Environment Files — Naming Convention

**When to use:** Creating, locating, or documenting env files for any backend service, BFF, web frontend, or seed script across all namespaces and local development.

## Pattern

```
<kind>.<component>.<namespace>.env
```

| Segment | Values | Notes |
|---------|--------|-------|
| `kind` | `bff`, `web`, `svc`, `seed` | Type of the app or script |
| `component` | e.g. `bff-backoffice`, `web-enabler`, `svc-product-tube`, `seed-kapita` | Full component name; prefix matches `kind` (`bff-*`, `web-*`, `svc-*`, `seed-*`) |
| `namespace` | `dev`, `staging`, `prod`, `enabler`, `build`, `run`, `infra`, `cicd`, `platform`, `local`, `template` | `local` = developer machine; `template` = checked-in defaults with no secrets |

Files **end** with `.env` — the kind is the first segment, not a file extension prefix.

## Single-instance tool namespaces

The six tool namespaces — `enabler`, `build`, `run`, `infra`, `cicd`, `platform` — each deploy **one instance only** (no dev/staging copy). The app names follow `app-<namespace>-bff` and `app-<namespace>-web`; `kind` = `namespace` in every case:

| Namespace | BFF env file | Web env file |
|-----------|-------------|-------------|
| `enabler` | `bff.bff-enabler.enabler.env` | `web.web-enabler.enabler.env` |
| `build` | `bff.bff-build.build.env` | `web.web-build.build.env` |
| `run` | `bff.bff-run.run.env` | `web.web-run.run.env` |
| `infra` | `bff.bff-infra.infra.env` | `web.web-infra.infra.env` |
| `cicd` | `bff.bff-cicd.cicd.env` | `web.web-cicd.cicd.env` |
| `platform` | `bff.bff-platform.platform.env` | `web.web-platform.platform.env` |

Each also has a `template` and optionally a `local` variant:
```
bff.bff-enabler.template.env
bff.bff-enabler.local.env
web.web-enabler.template.env
web.web-enabler.local.env
```

## Product / multi-stage apps (backoffice, main BFF, …)

Apps released through `dev → staging → prod` carry one file per stage:

```
bff.bff-backoffice.dev.env
bff.bff-backoffice.staging.env
bff.bff-backoffice.prod.env
bff.bff-backoffice.template.env
bff.bff-backoffice.local.env

web.web-backoffice.dev.env
web.web-backoffice.staging.env
web.web-backoffice.prod.env
web.web-backoffice.template.env
web.web-backoffice.local.env
```

## Services (`svc-*`)

A service deployed into one namespace:

```
svc.svc-product-tube.build.env
svc.svc-product-tube.template.env
```

## Seeds

Seeds are namespace-scoped, not app-scoped. The component name is `seed-<namespace>`:

**Kapita product namespaces:**
```
seed.seed-kapita.dev.env
seed.seed-kapita.staging.env
seed.seed-kapita.prod.env
seed.seed-kapita.local.env
seed.seed-kapita.template.env

seed.seed-enabler.enabler.env
seed.seed-enabler.template.env
```

**Shipdeck tool namespaces** (one pair per namespace):
```
seed.seed-build.build.env       seed.seed-build.template.env
seed.seed-run.run.env           seed.seed-run.template.env
seed.seed-platform.platform.env seed.seed-platform.template.env
seed.seed-cicd.cicd.env         seed.seed-cicd.template.env
seed.seed-infra.infra.env       seed.seed-infra.template.env
```

A seed may target any single namespace: `enabler`, `build`, `run`, `infra`, `cicd`, `platform`, `dev`, `staging`, `prod`.

## Rules

- **`template` files are committed**; all files containing real credentials are `.gitignore`d.
- **`local` overrides `template`**: load `<kind>.<component>.template.env` first, then `<kind>.<component>.local.env` to override.
- **Component prefix matches kind**: `bff-*` for BFF apps, `web-*` for SPAs, `svc-*` for services, `seed-*` for seed scripts.
- **For tool namespaces, only `template` and `local` qualifiers exist alongside the namespace value** — there is no `dev`/`staging` variant because there is no dev/staging instance.
- **One file per (kind, component, namespace) tuple** — never combine stages in one file.
