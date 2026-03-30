## Launch checklist (FR-006 / FR-007)

This checklist captures the pre-launch guidance required by **FR-006** and the minimum data-handling controls required by **FR-007** **before enabling** any form submissions or embedding scheduling/payment providers.

### Hosting, domain, HTTPS, and backups (FR-006)

- **Hosting**: confirm the production host (e.g., Vercel) account ownership, team access, and billing are under firm control.
- **Domain**: confirm registrar ownership, DNS access, and a cutover plan (TTL reduction, rollback).
- **HTTPS**: ensure HTTPS is enforced; verify certificates renew automatically.
- **Backups**:
  - **Source of truth**: Git repo is the system of record for site content/config.
  - **Operational backups**: confirm how hosting configuration, DNS settings, and any third-party provider configs are recoverable.

### Privacy/disclosures (FR-006)

- **Privacy Notice** is published and linked in site navigation or footer.
- **Analytics** (if enabled): vendor listed, high-level data collected described, and configuration avoids unnecessary PII.
- **Third parties** (booking/payment/email/CRM): disclosed with links to their terms/privacy where appropriate.

### Forms and scheduling data-handling (FR-007)

Before enabling contact submissions or scheduling embeds:

- **Notice**: Privacy Notice describes:
  - what fields are collected
  - why they are collected
  - where they are sent (email/CRM/scheduling provider)
  - retention/deletion approach
  - how users can request deletion
  - “no attorney-client relationship” / confidentiality expectations for web submissions (as firm policy dictates)
- **Least data**: collect only what is necessary (no extra fields “just in case”).
- **Server-side validation**: enforce field limits and reject unexpected fields.
- **Consent (if required by firm policy)**:
  - checkbox is present and required
  - store only consent metadata (timestamp + policy version) with the submission
- **Abuse controls**: rate limiting is enabled; consider CAPTCHA if spam is observed.
- **Logging**: application logs must not contain full message bodies or sensitive PII.

### Smoke checks

- `npm -w apps/firm-site run build`
- `npm -w apps/firm-site run test:e2e`
