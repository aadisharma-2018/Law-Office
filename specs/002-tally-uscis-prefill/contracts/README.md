# Contracts: Tally Questionnaire Intake and USCIS Form Prefill

## Boundaries today vs future

The **implemented** [apps/uscis-fill-local](../../apps/uscis-fill-local/) product boundary is **local files**:

1. **Inbound (primary):** **Tally export** files (**CSV** primary; **JSON** supported) and an official **USCIS fillable PDF**, supplied by staff after download—no HTTP server required (**[spec.md](../spec.md) FR-010**).

**Future / optional** HTTP boundaries (not shipped in the Streamlit app):

2. **Inbound:** HTTP **webhooks** from Tally (`FORM_RESPONSE`) → firm-hosted endpoint ([tally-webhook-inbound.md](./tally-webhook-inbound.md)).
3. **Internal:** **Staff** REST API for listings, review, and DB-backed draft generation ([staff-api.yaml](./staff-api.yaml))—representative of a **hosted** portal (e.g. Node or FastAPI), not the current Python UI.

| Artifact | Description |
|----------|-------------|
| [tally-webhook-inbound.md](./tally-webhook-inbound.md) | Responsibilities for a **future** consumer of Tally webhooks. |
| [staff-api.yaml](./staff-api.yaml) | Representative OpenAPI for **future** staff operations (review, submission-scoped drafts). |

Implementation MUST keep webhook secrets and API keys out of source control (Constitution I).
