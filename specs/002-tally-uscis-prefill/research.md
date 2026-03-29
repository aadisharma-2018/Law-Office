# Research: Tally Questionnaire Intake and USCIS Form Prefill

**Branch**: `002-tally-uscis-prefill`  
**Date**: 2025-03-24  
**Update (2026-03-24):** [spec.md](./spec.md) **FR-010** prioritizes **local-first** processing (download questionnaire export + download USCIS PDF + map/fill **on firm-controlled systems**). **Webhook-based** ingestion is **optional**, not required. Sections below remain valid but **§1–2** assume a **network app**—treat **file import + local PDF** as the **default path** unless the firm opts into webhooks.

**Update (same session):** Firm prefers a **simple Python-based** stack ([spec.md](./spec.md) Assumptions). Map earlier “Node/Next.js”-style decisions to **Python** equivalents in [plan.md](./plan.md) Technical Context; **§2** “Application shape” should be read as **Python desktop/CLI + optional FastAPI webhook**, not Next.js, unless planning explicitly revisits.

**Update (2026-03-28):** For **manual download → local import**, Tally’s **CSV (spreadsheet)** export is the **primary** format consumed by `uscis-fill-local`; **JSON** remains supported. Webhook payloads stay **JSON** per Tally’s API.

Consolidated decisions for Phase 0. Each item either resolves a `NEEDS CLARIFICATION` from Technical Context or records a deliberate technology choice.

---

## 1. Client questionnaire provider (Tally)

| Item | Decision |
|------|----------|
| **Decision** | Use **Tally** for client-facing forms per `spec.md`. Integrate via **Tally webhooks** (`FORM_RESPONSE` events) to the firm’s application and optional **Tally REST API** for automation (create webhooks, list forms) using an API key. |
| **Rationale** | Matches spec assumption; webhooks give near-real-time structured payloads; API supports programmatic webhook registration and operational tasks. |
| **Alternatives considered** | Typeform/Jotform (re-specify mappings); fully custom portal (higher build cost). |

**Matter binding (FR-003):** Tally supports **hidden fields** populated via **URL query parameters** (case-sensitive). The firm emails a **unique URL per invitation**, e.g. base form URL plus `matterId` / `invitationId` as hidden field params, so the webhook payload includes those values without the client typing a case code.

**Staff export path:** Results can be downloaded as **CSV** for spreadsheet workflows; the local Python app parses CSV headers into field keys aligned with `tally_to_profile.yaml`.

---

## 2. Application shape and runtime

| Item | Decision |
|------|----------|
| **Decision** | **Next.js** (App Router) on **Node.js 20 LTS** with **TypeScript**, deployed to a managed Node host (e.g. Vercel, Railway, or firm-managed VPS). **Staff-only** authenticated UI; clients never log into this app—they only use Tally links from email. |
| **Rationale** | One codebase for HTTP webhooks, staff UI, and PDF download flows; strong ecosystem for Prisma/auth; aligns with small-team maintainability. |
| **Alternatives considered** | Separate Python API + SPA (more moving parts); serverless-only functions without UI (insufficient for review workflows). |

---

## 3. Data storage

| Item | Decision |
|------|----------|
| **Decision** | **PostgreSQL** with **Prisma** ORM. Store matters, invitations, raw submission payloads (for audit), normalized **structured case profile** (JSON column or relational breakdown per evolution), review state, generated draft metadata (storage path or blob reference). |
| **Rationale** | ACID for matter/submission integrity; Prisma migrations fit spec-driven iteration. |
| **Alternatives considered** | SQLite for MVP only (weak concurrent multi-user staff access); document DB only (harder relational integrity for matters). |

---

## 4. Staff authentication and authorization

| Item | Decision |
|------|----------|
| **Decision** | **Auth** via a hosted identity provider or **NextAuth.js**-style solution with email/Google restricted to **firm domains** where possible; **role-based** access (e.g. admin vs. paralegal) enforced in middleware and server actions. |
| **Rationale** | Least privilege (FR-007); industry-standard session security; avoids custom password storage. |
| **Alternatives considered** | Shared single password (fails least privilege); Clerk/Auth0 (acceptable if firm prefers managed SSO—swap in plan implementation). |

---

## 5. Invitation delivery (email)

| Item | Decision |
|------|----------|
| **Decision** | **Primary path (per spec clarification):** staff send **unique Tally URLs** to clients using the firm’s **office email** (manual compose/send). **Optional later:** integrate a **transactional email provider** from the app if the firm wants templated, auditable sends from the same system as matters. |
| **Rationale** | FR-001 is satisfied by **firm-delivered email**, including manual office email; it does **not** require the product to be the SMTP sender. |
| **Alternatives considered** | App-only transactional email (rejected as mandatory—unnecessary if office email is preferred); marketing ESP without transactional APIs. |

---

## 6. USCIS PDF generation

| Item | Decision |
|------|----------|
| **Decision** | **pdf-lib** (or equivalent) against **official fillable USCIS PDFs**, driven by a **versioned mapping** from structured case profile keys → AcroForm field names per form/version. Missing/ambiguous fields reported in UI (FR-006). |
| **Rationale** | Keeps output on-government templates; mappers are testable (SC-001). |
| **Alternatives considered** | Manual Word merge (not spec-aligned); proprietary form engines (vendor lock-in). |

---

## 7. Audit and logging

| Item | Decision |
|------|----------|
| **Decision** | Append-only **audit log** table or structured log stream for: webhook receipt, submission stored, review state changes, draft generation, staff access to sensitive views (minimum viable: who/when/what action/matter id). |
| **Rationale** | Constitution III (Auditability) and FR-008. |
| **Alternatives considered** | Application logs only without DB audit (harder to query for investigations). |

---

## 8. Third-party / subprocessor summary

| Service | Role | Data |
|---------|------|------|
| **Tally** | Form hosting, submission capture | Client PII as entered in questionnaire |
| **Email provider** (optional) | App-sent invitations, if adopted | Recipient address, link metadata |
| **Hosting / DB** | App and PostgreSQL | All application data per retention policy |
| **Identity provider** (if used) | Staff login | Staff email, session metadata |

Document data flows and DPA review in security review before production.

---

## 9. Testing strategy (boundaries)

| Boundary | Approach |
|----------|----------|
| Tally webhook handler | Contract tests with **signed fixture payloads**; verify idempotency and matter association. |
| Normalization / mapping | Unit tests for mapping questionnaire → structured profile. |
| PDF fill | Golden tests per form: known profile → expected field values (SC-001). |
| Staff UI | Critical path E2E for review + generate draft (optional Playwright). |

---

## Open items (non-blocking for plan; implementation tickets)

- Exact USCIS form set for v1 (spec allows subset).
- Final choice between Auth.js vs. Clerk vs. Auth0 (functionally equivalent for gate).
- Production hosting region and data residency policy for the firm.
