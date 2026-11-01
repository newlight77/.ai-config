# Environment Files — Naming Convention

**When to use:** Creating, locating, or documenting `.env` files for any backend service, BFF, or seed script across all namespaces and local development.

## Pattern

```
.env[.<kind>][.<component>].<namespace>
```

| Segment | Values | Notes |
|---------|--------|-------|
| `kind` | `bff`, `svc` | Omit for cross-cutting files (seeds, top-level app config) |
| `component` | e.g. `backoffice`, `product-tube`, `enabler` | Matches the app/service name; omit only for namespace-wide files like seeds |
| `namespace` | `dev`, `staging`, `prod`, `enabler`, `build`, `run`, `infra`, `cicd`, `platform`, `local`, `template` | `local` = developer machine; `template` = checked-in defaults with no secrets |

## Single-instance tool namespaces

The six tool namespaces — `enabler`, `build`, `run`, `infra`, `cicd`, `platform` — each deploy **one instance only** (no dev/staging copy). Every namespace runs exactly two apps:

```
app-<namespace>-bff   (the BFF)
app-<namespace>-web   (the SPA)
```

Because the component name and the namespace name are identical (e.g. component `enabler` in namespace `enabler`), the env file segment pair `.<component>.<namespace>` reduces to two equal words:

```
.env.bff.enabler.enabler      ← full form
.env.bff.enabler.template     ← checked-in template (no secrets)
.env.bff.enabler.local        ← developer override, not committed
```

The same applies to all six: `.env.bff.build.build`, `.env.bff.run.run`, `.env.bff.cicd.cicd`, `.env.bff.platform.platform`, `.env.bff.infra.infra`.

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
| `.env.bff.backoffice.dev` | Backoffice BFF — `dev` stage |
| `.env.bff.backoffice.staging` | Backoffice BFF — `staging` stage |
| `.env.bff.backoffice.prod` | Backoffice BFF — production stage |
| `.env.bff.backoffice.template` | Backoffice BFF template (no real secrets) |
| `.env.bff.backoffice.local` | Backoffice BFF local override, not committed |
| `.env.bff.enabler.enabler` | Enabler BFF — single instance |
| `.env.bff.enabler.template` | Enabler BFF template |
| `.env.bff.build.build` | Build BFF — single instance |
| `.env.bff.platform.platform` | Platform BFF — single instance |
| `.env.svc.product-tube.build` | Product Tube service in the `build` namespace |
| `.env.svc.product-tube.template` | Product Tube template |
| `.env.seed.dev` | Seed script targeting `dev` |
| `.env.seed.staging` | Seed script targeting `staging` |
| `.env.seed.prod` | Seed script targeting production |
| `.env.seed.local` | Seed script for local development database |
| `.env.seed.template` | Seed template with no real credentials |

## Rules

- **`template` files are committed**; all other files that contain real credentials are `.gitignore`d.
- **`local` overrides `template`**: load `.env.<kind>.<component>.template` first, then `.env.<kind>.<component>.local` to override.
- **No `kind` for seeds** — seeds operate across the whole stage, not a single service.
- **Component name matches the app name** (e.g. `app-enabler-bff` → component `enabler`; `app-backoffice-bff` → component `backoffice`).
- **Namespace matches the cluster namespace** (`dev`, `staging`, `prod`, `enabler`, `build`, `run`, `infra`, `cicd`, `platform`). `prod` is the short form of `production` in file names.
- **One file per (kind, component, namespace) tuple** — never combine stages in one file.
- **For tool namespaces, only `template` and `local` qualifiers make sense** alongside the namespace value — there is no separate dev/staging file because there is no dev/staging instance.
