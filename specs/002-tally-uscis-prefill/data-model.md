# Data Model: Tally Questionnaire Intake and USCIS Form Prefill

**Branch**: `002-tally-uscis-prefill`  
**Date**: 2025-03-24  
**Spec**: [spec.md](./spec.md)

## Overview

Logical model for a staff-facing portal that ties **Tally submissions** to **matters**, supports **review**, and drives **structured case profiles** for USCIS draft generation.

---

## Entities

### Client

Represents a person or entity the firm represents (simplified for intake).

| Field | Type | Notes |
|-------|------|--------|
| `id` | UUID | Primary key |
| `displayName` | string | Optional; for staff UI |
| `createdAt` | datetime | |
| `updatedAt` | datetime | |

---

### Matter

Legal matter / case bucket for questionnaires and drafts.

| Field | Type | Notes |
|-------|------|--------|
| `id` | UUID | Primary key |
| `clientId` | UUID | FK → Client |
| `reference` | string | Firm’s internal reference (optional) |
| `status` | enum | e.g. `open`, `closed` (firm-defined) |
| `createdAt` | datetime | |
| `updatedAt` | datetime | |

**Uniqueness:** `id` is the stable join key for invitations and submissions.

---

### QuestionnaireDefinition

Versioned definition of a Tally form the firm uses.

| Field | Type | Notes |
|-------|------|--------|
| `id` | UUID | Primary key |
| `tallyFormId` | string | Tally form identifier |
| `version` | int or semver | Increments when questions change |
| `title` | string | Staff-facing label |
| `mappingVersion` | string | Version of normalization mapping |
| `createdAt` | datetime | |

**Relationship:** One definition can have many **Invitations** and **Submissions**.

---

### QuestionnaireInvitation

A **unique emailed link** to a Tally form for one matter (FR-003, spec clarifications).

| Field | Type | Notes |
|-------|------|--------|
| `id` | UUID | Primary key |
| `matterId` | UUID | FK → Matter |
| `questionnaireDefinitionId` | UUID | FK → QuestionnaireDefinition |
| `token` | string | Opaque, unguessable; may appear in URL or map to hidden field values |
| `recipientEmail` | string | Where invitation was sent |
| `sentAt` | datetime | |
| `expiresAt` | datetime | Optional |
| `status` | enum | e.g. `sent`, `superseded`, `revoked` |

**Invariant:** Tally URL encodes `invitationId` and/or `matterId` via hidden fields so webhook can resolve **Matter** without client-entered codes.

---

### Submission

One Tally `FORM_RESPONSE` (or equivalent) stored for review and normalization.

| Field | Type | Notes |
|-------|------|--------|
| `id` | UUID | Primary key |
| `matterId` | UUID | FK → Matter (must match invitation) |
| `questionnaireDefinitionId` | UUID | FK |
| `invitationId` | UUID | FK → QuestionnaireInvitation (nullable if legacy) |
| `tallyResponseId` | string | External id from Tally (idempotency) |
| `receivedAt` | datetime | |
| `rawPayload` | JSON | Immutable copy for audit/dispute (may originate from a **CSV** or **JSON** file import; stored as structured JSON in the app) |
| `normalizedProfile` | JSON | Structured case profile after mapping (FR-002) |
| `mappingErrors` | JSON | Optional; field-level issues |

**Uniqueness:** `tallyResponseId` unique when present (dedupe webhooks).

---

### ReviewDecision

Attorney/staff review before draft generation (FR-004, US2).

| Field | Type | Notes |
|-------|------|--------|
| `id` | UUID | Primary key |
| `submissionId` | UUID | FK → Submission |
| `reviewerUserId` | string | From identity provider |
| `status` | enum | `pending`, `approved`, `needs_follow_up` |
| `notes` | text | Internal |
| `decidedAt` | datetime | |

**Rule:** Draft generation blocked unless latest review is `approved` (per spec default).

---

### DraftUscisOutput

Generated PDF artifact from approved profile (FR-005).

| Field | Type | Notes |
|-------|------|--------|
| `id` | UUID | Primary key |
| `matterId` | UUID | FK |
| `submissionId` | UUID | FK (which intake was used) |
| `formCode` | string | e.g. `I-485`, `I-130` |
| `formVersion` | string | USCIS edition |
| `storageKey` | string | Blob path or S3 key |
| `unfilledFields` | JSON | FR-006 |
| `generatedAt` | datetime | |
| `generatedByUserId` | string | |

---

### AuditLog

Material actions for accountability (FR-008).

| Field | Type | Notes |
|-------|------|--------|
| `id` | UUID | |
| `actorUserId` | string | |
| `action` | string | e.g. `submission.view`, `review.update`, `draft.generate` |
| `matterId` | UUID | nullable |
| `metadata` | JSON | Non-PII or minimized |
| `createdAt` | datetime | |

---

## State transitions

### ReviewDecision (per submission)

```
pending → approved
pending → needs_follow_up
needs_follow_up → approved (after corrections / new submission per firm policy)
```

### Submission vs. matter

- New submission may **supersede** prior for same matter per firm policy (spec edge cases); model may add `supersedesSubmissionId` in a later iteration.

---

## Validation rules (from spec)

- **FR-003:** Every `Submission.matterId` must be derivable from the invitation / hidden fields on ingest; ingest fails closed if matter cannot be resolved.
- **FR-006:** PDF generation never silently invents values; `unfilledFields` populated.
