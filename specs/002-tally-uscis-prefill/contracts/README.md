# Contracts: Tally Questionnaire Intake and USCIS Form Prefill

This feature’s **external boundaries** are:

1. **Inbound**: HTTP **webhooks** from Tally to the firm’s application (`FORM_RESPONSE`).
2. **Outbound**: **Transactional email** to clients (invitation links).
3. **Internal**: **Staff-facing** HTTP API and UI (authenticated).

| Artifact | Description |
|----------|-------------|
| [tally-webhook-inbound.md](./tally-webhook-inbound.md) | Responsibilities and verification for the consumer of Tally webhooks. |
| [staff-api.yaml](./staff-api.yaml) | Representative OpenAPI for staff operations (review, draft generation). |

Implementation MUST keep webhook secrets and API keys out of source control (Constitution I).
