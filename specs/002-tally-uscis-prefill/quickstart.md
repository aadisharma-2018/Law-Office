# Quickstart: Tally Questionnaire Intake and USCIS Form Prefill

**Branch**: `002-tally-uscis-prefill`  
**Date**: 2025-03-24 (updated 2026-03-28: CSV local import)

This document is for developers once the repo contains the application scaffold (see [plan.md](./plan.md)). Until then, treat this as a **target** local-dev checklist.

## Prerequisites

- Node.js 20 LTS
- PostgreSQL 15+ (local or Docker)
- Tally account with API access for webhook registration
- (Optional) Transactional email provider if the app will send invitations; **not** required if staff send links via **office email** only ([spec.md](./spec.md) FR-001 clarification)

## Environment variables (representative)

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string |
| `TALLY_API_KEY` | Tally API bearer token (create webhooks, optional) |
| `TALLY_WEBHOOK_SECRET` | Signing secret for webhook verification (if configured) |
| `EMAIL_API_KEY` | Transactional email provider (omit if invitations are manual office email only) |
| `AUTH_SECRET` | Session/JWT secret for staff auth |
| `PUBLIC_APP_URL` | Base URL for webhook URL registration and any app-generated links |

**Never commit secrets.** Use `.env.local` (gitignored) or a secret manager.

## Tally form setup

1. Create hidden fields for **`matterId`** and/or **`invitationId`** (or a single signed token) per [Tally hidden fields](https://tally.so/help/hidden-fields).
2. Build invitation URLs: base form URL + query parameters that populate hidden fields.
3. Register webhook: `FORM_RESPONSE` → `https://<your-domain>/api/webhooks/tally` (exact path per implementation).

## Local file import (CSV / JSON)

For the **local-first** path ([spec.md](./spec.md) **FR-010**, clarification Session 2026-03-28), staff typically **download results as CSV** from Tally (spreadsheet export) and pass that file to `apps/uscis-fill-local` (UI or CLI). **JSON** exports are still accepted. Multi-row CSV files: the implementation uses the **last** non-empty data row unless the firm configures otherwise—confirm against real exports during rollout.

## Local webhook testing

- Use **ngrok** (or similar) to expose localhost HTTPS for Tally to call.
- Replay captured payloads in **contract tests** to avoid manual submits every time.

## Database

```bash
# After scaffold exists (illustrative)
npx prisma migrate dev
```

## Verification checklist

- [ ] Webhook signature verification passes with test payload
- [ ] Submission deduplication by Tally response id
- [ ] Matter association matches hidden fields from invitation URL
- [ ] Review blocks draft generation until `approved`
- [ ] Audit log entries for review and draft generation

## References

- [spec.md](./spec.md) — requirements
- [data-model.md](./data-model.md) — entities
- [contracts/](./contracts/) — inbound/outbound boundaries
