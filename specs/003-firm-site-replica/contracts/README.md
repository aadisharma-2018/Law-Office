# Contracts: Firm public website (`003-firm-site-replica`)

## Scope

The **v1** public marketing site is primarily **HTTP GET** HTML pages and **static** assets served from a **CDN** (see [plan.md](../plan.md)).

## Boundaries

| Surface | Direction | Description |
|---------|-----------|-------------|
| **Public pages** | Server → Browser | **HTML** + **RSC** payload for Next.js; **no** authenticated API for visitors in v1. |
| **Contact / lead form** | Browser → Server | **POST** to **Route Handler** or **Server Action** (exact path TBD in implementation). Request body: **JSON** or `form-urlencoded` with `name`, `email`, `message` (fields subject to **FR-007**). |
| **Third-party embeds** | External → Page | **iframe** or script tags for **booking** / **payments**; **not** defined as OpenAPI here—follow vendor docs. |

## Future (optional)

- `openapi.yaml` for a **lead-ingestion** API if the firm adds **headless** CRM sync.
- **Webhooks** from CMS preview deployments—deferred.

## Compliance

- **HTTPS** only in production.
- **No** client PII in **URL** query strings for forms.
- Subprocessors listed in the firm’s **privacy policy** (**plan** subprocessors table).
