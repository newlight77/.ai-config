# Observability Skills

**When to use:** Logging, tracing, correlation across web, mobile and backend; debugging end-to-end flows; telemetry changes.

## End-to-end request flow (mental model)

```
Browser / mobile app
  → HTTP client → BFF (backend-for-frontend)
      → domain use cases → driven adapters (DB, external APIs)
  → Response

Parallel telemetry:
  → first-party analytics events (client → own BFF → analytics service, opt-in consent)
  → stdout JSON logs → log shipper → log store
```

**To debug a user journey:** align **time window**, **user identity** (pseudonymous id or `x-user-id`) and **path** across browser devtools, mobile logs, BFF logs and the log store.

## Correlation and identity

- Authenticate every call (`Authorization: Bearer …`); the BFF resolves the caller from it.
- Generate a **client request id** (UUID) per outbound API call and send it as **`x-request-id`** (or the agreed `x-correlation-id`) from every client (Axios, Dio, …).
- Log that id in BFF handlers and middleware; add it to event `properties` when adding new events.
- Until a single id is propagated across all layers, chain flows with **timestamp + user + path + duration** from the request log line and matching client logs.
- Derive a `distinct_id` for tracking from `x-user-id`, then `x-request-id`, then the client IP; never log the raw IP.

## Backend (BFF and services)

- **Structured logging** through the shared logging module (`setup_logging`, `get_logger`); bound loggers at ingress and egress.
- **Mandatory JSON fields** (envelope for new logs): `timestamp`, `level`, `service`, `env`, `correlation_id`, `request_id`, `user_id`, `actor`, `operation`, `resource`, `status`, `duration_ms`, `error_code`, `error_message`, `trace_id`, `span_id`, `version`. Populate what exists; never log PII or secrets.
- **Request middleware:** one PII-free JSON line per request (`method`, `path`, `status_code`, `duration_ms`, `platform`, `error_type` on failures).
- **Server telemetry:** OpenTelemetry configured once at application start; LLM spans log model, token counts and timing, never prompts. JSON lines when `LOG_FORMAT=json` or the environment is staging/preview/production; OTLP export is optional.
- **Feature flags:** routes that roll out by percentage resolve `distinct_id` from the same headers.

## Frontend web and mobile

- **HTTP client:** auth refresh interceptors, plus a request interceptor that adds the request id. Mobile may add a logging interceptor (method, URI, redacted headers) enabled with a `Logger` for dev diagnostics only.
- **Telemetry:** a first-party tracking client posting to the BFF, gated by feature flags and the user's consent; web and mobile use the same request id once standardized.
- **Debug options** stay off outside dev; never log secrets.

## Analytics principles

- Events carry **non-PII** context only: `platform`, `path` or `screen`, `method`, `status_code`, `duration_ms`, and `client_request_id` once propagated.
- Analytics is **first-party only**: no third-party analytics SDK or service.
- Consent is opt-in; unknown or denied consent sends nothing. Autocapture and session replay are masked by construction and behind kill-switch flags; never add a way to record unmasked content.
- Tube side (ingest, allow-list, retention, rollups, replay, tokens): `enabler-analytics-tube-skills.md` in the Shipdeck layer.

## Implementation checklist (new features)

1. Log at the **boundary** (route handler, adapter egress) with **operation** + **resource** + **duration_ms**.
2. Reuse Makefile targets; do not log bodies with tokens or PII.
3. Tracking changes: tests with **faked** tracking ports (see `testing.md`).
4. If you add an error reporter (e.g. Sentry), keep the same correlation id across spans and error reports.

Kapita wiring (middleware, tracking packages, flags, file paths): `kapita-observability.md` in the Kapita layer.
