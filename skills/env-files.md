# Environment Files — Naming Convention

**When to use:** Creating, locating, or documenting `.env` files for any backend service, BFF, or seed script across all namespaces and local development.

## Pattern

```
.env[.<kind>][.<component>].<namespace>
```

| Segment | Values | Notes |
|---------|--------|-------|
| `kind` | `bff`, `svc` | Omit for cross-cutting files (seeds, top-level app config) |
| `component` | e.g. `backoffice`, `product-tube`, `enabler-bff` | Matches the service/package name; omit only for namespace-wide files like seeds |
| `namespace` | `dev`, `staging`, `prod`, `enabler`, `build`, `run`, `infra`, `cicd`, `platform`, `local`, `template` | `local` = developer machine; `template` = checked-in defaults with no secrets |

## Examples

| File | What it configures |
|------|--------------------|
| `.env.bff.backoffice.dev` | Backoffice BFF pointed at the `dev` stage |
| `.env.bff.backoffice.staging` | Backoffice BFF pointed at `staging` |
| `.env.bff.backoffice.prod` | Backoffice BFF pointed at production |
| `.env.bff.backoffice.template` | Checked-in template (no real secrets) |
| `.env.bff.backoffice.local` | Developer override, not committed |
| `.env.svc.product-tube.build` | Product Tube service in the `build` namespace |
| `.env.svc.product-tube.template` | Template for any deployment of the product tube |
| `.env.seed.dev` | Seed script targeting the `dev` stage |
| `.env.seed.staging` | Seed script targeting `staging` |
| `.env.seed.prod` | Seed script targeting production |
| `.env.seed.local` | Seed script for local development database |
| `.env.seed.template` | Seed template with no real credentials |

## Rules

- **`template` files are committed**; all other files that contain real credentials are `.gitignore`d.
- **`local` overrides `template`**: load `.env.<kind>.<component>.template` first, then `.env.<kind>.<component>.local` to override.
- **No `kind` for seeds** — seeds operate across the whole stage, not a single service.
- **Component name matches the package/app directory name** (e.g. `app-enabler-bff` → component `enabler-bff`); keep it stable when renaming.
- **Namespace matches the cluster namespace** (`dev`, `staging`, `prod`, `enabler`, `build`, `run`, `infra`, `cicd`, `platform`). `prod` is the short form of the `production` namespace in file names.
- **One file per (kind, component, namespace) tuple** — never combine stages in one file or create `dev-staging` hybrids.
