# Environment Files — Naming Convention

**When to use:** Creating, locating, or documenting `.env` files for any backend service, BFF, or seed script across all namespaces and local development.

## Pattern

```
.env[.<kind>][.<component>].<namespace>
```

| Segment | Values | Notes |
|---------|--------|-------|
| `kind` | `bff`, `web`, `svc` | Omit for cross-cutting files (seeds, top-level app config) |
| `component` | e.g. `app-backoffice`, `app-enabler`, `svc-product-tube` | Full app/service name prefixed with `app-` or `svc-`; omit only for namespace-wide files like seeds |
| `namespace` | `dev`, `staging`, `prod`, `enabler`, `build`, `run`, `infra`, `cicd`, `platform`, `local`, `template` | `local` = developer machine; `template` = checked-in defaults with no secrets |

## Single-instance tool namespaces

The six tool namespaces — `enabler`, `build`, `run`, `infra`, `cicd`, `platform` — each deploy **one instance only** (no dev/staging copy). Every namespace runs exactly two apps:

```
app-<namespace>-bff   (the BFF)
app-<namespace>-web   (the SPA)
```

The component is named `app-<namespace>` and the namespace is the same word, so the segment pair `.<component>.<namespace>` always contains the namespace name twice. Each app has two env files — one for the BFF and one for the web frontend:

```
.env.bff.app-enabler.enabler      ← BFF, deployed instance
.env.web.app-enabler.enabler      ← SPA, deployed instance
.env.bff.app-enabler.template     ← BFF template (no secrets), committed
.env.web.app-enabler.template     ← SPA template (no secrets), committed
.env.bff.app-enabler.local        ← BFF local override, not committed
.env.web.app-enabler.local        ← SPA local override, not committed
```

The same pattern applies to all six namespaces:

| Namespace | BFF env file | Web env file |
|-----------|-------------|-------------|
| `enabler` | `.env.bff.app-enabler.enabler` | `.env.web.app-enabler.enabler` |
| `build` | `.env.bff.app-build.build` | `.env.web.app-build.build` |
| `run` | `.env.bff.app-run.run` | `.env.web.app-run.run` |
| `infra` | `.env.bff.app-infra.infra` | `.env.web.app-infra.infra` |
| `cicd` | `.env.bff.app-cicd.cicd` | `.env.web.app-cicd.cicd` |
| `platform` | `.env.bff.app-platform.platform` | `.env.web.app-platform.platform` |

## Product / multi-stage apps

Apps that follow the product release cycle (`dev` → `staging` → `prod`) carry different env files per stage because the component name and namespace name differ:

```
.env.bff.backoffice.dev
.env.bff.backoffice.staging
.env.bff.backoffice.prod
.env.bff.backoffice.template
.env.bff.backoffice.local
```

## Examples

| File | What it configures |
|------|--------------------|
| `.env.bff.app-backoffice.dev` | Backoffice BFF — `dev` stage |
| `.env.bff.app-backoffice.staging` | Backoffice BFF — `staging` stage |
| `.env.bff.app-backoffice.prod` | Backoffice BFF — production stage |
| `.env.bff.app-backoffice.template` | Backoffice BFF template (no real secrets) |
| `.env.bff.app-backoffice.local` | Backoffice BFF local override, not committed |
| `.env.bff.app-enabler.enabler` | Enabler BFF — single instance |
| `.env.web.app-enabler.enabler` | Enabler SPA — single instance |
| `.env.bff.app-enabler.template` | Enabler BFF template |
| `.env.bff.app-build.build` | Build BFF — single instance |
| `.env.bff.app-platform.platform` | Platform BFF — single instance |
| `.env.svc.svc-product-tube.build` | Product Tube service in the `build` namespace |
| `.env.svc.svc-product-tube.template` | Product Tube template |
| `.env.seed.dev` | Seed script targeting `dev` |
| `.env.seed.staging` | Seed script targeting `staging` |
| `.env.seed.prod` | Seed script targeting production |
| `.env.seed.local` | Seed script for local development database |
| `.env.seed.template` | Seed template with no real credentials |

## Rules

- **`template` files are committed**; all other files that contain real credentials are `.gitignore`d.
- **`local` overrides `template`**: load `.env.<kind>.<component>.template` first, then `.env.<kind>.<component>.local` to override.
- **No `kind` for seeds** — seeds operate across the whole stage, not a single service.
- **Component name is the full app or service name** (e.g. `app-enabler-bff` → component `app-enabler`; `app-backoffice-bff` → component `app-backoffice`; `svc-product-tube` → component `svc-product-tube`). Use the `app-` or `svc-` prefix; drop only the `-bff` / `-web` suffix since `kind` already captures that.
- **Namespace matches the cluster namespace** (`dev`, `staging`, `prod`, `enabler`, `build`, `run`, `infra`, `cicd`, `platform`). `prod` is the short form of `production` in file names.
- **One file per (kind, component, namespace) tuple** — never combine stages in one file.
- **For tool namespaces, only `template` and `local` qualifiers make sense** alongside the namespace value — there is no separate dev/staging file because there is no dev/staging instance.
