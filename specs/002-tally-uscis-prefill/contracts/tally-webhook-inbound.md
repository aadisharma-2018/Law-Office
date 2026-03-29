# Inbound contract: Tally → Firm application

**Direction:** Tally’s servers send HTTP `POST` requests to a **firm-configured HTTPS endpoint** when a form response is submitted (event `FORM_RESPONSE`).

## Security

- **TLS:** Endpoint MUST be HTTPS in production.
- **Signing:** If Tally webhook is created with a `signingSecret`, the consumer MUST verify the request signature per **current Tally documentation** (do not log the raw secret).
- **Idempotency:** Use Tally’s response identifier (e.g. response id in payload) to deduplicate retries.

## Functional contract (consumer responsibilities)

1. **Acknowledge quickly** with `2xx` after basic validation so Tally does not retry unnecessarily; defer heavy work to async jobs if needed.
2. **Resolve matter:** Extract **matter id** and/or **invitation id** from the payload (hidden fields or fields populated from URL parameters). If resolution fails, **do not** attach data to an arbitrary matter—record error for staff (spec FR-003).
3. **Persist** raw payload + normalized profile per `data-model.md`.
4. **Emit audit event** for `webhook.received` / `submission.created` (FR-008).

## Payload shape

Tally’s exact JSON schema may evolve. The implementation MUST:

- Parse per **Tally’s published webhook payload** for `FORM_RESPONSE` at the time of build.
- Store a **verbatim** `rawPayload` for audit.

**Reference:** [Tally Developer Docs — Webhooks](https://developers.tally.so/api-reference/endpoint/webhooks/post) and related payload documentation.

## Example (illustrative only — confirm against live docs)

```json
{
  "eventId": "string",
  "eventType": "FORM_RESPONSE",
  "createdAt": "2025-03-24T12:00:00.000Z",
  "data": {
    "responseId": "string",
    "formId": "string",
    "fields": []
  }
}
```

Field arrays include question blocks and **hidden fields** when configured in the form editor.
