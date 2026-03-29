# Research: Tally Questionnaire Intake and USCIS Form Prefill

**Branch**: `002-tally-uscis-prefill`  
**Date**: 2025-03-24  

**Update (2026-03-24):** [spec.md](./spec.md) **FR-010** prioritizes **local-first** processing (download questionnaire export + download USCIS PDF + map/fill **on firm-controlled systems**). **Webhook-based** ingestion is **optional**, not required. Treat **file import + local PDF** as the **default path** unless the firm opts into webhooks.

**Update (2026-03-24):** Firm prefers a **simple Python-based** stack ([spec.md](./spec.md) Assumptions). Earlier **Next.js / Node** “application shape” in **§2** is **superseded** for the **implemented** product by **Python + Streamlit + CLI** (see **§2** below and [plan.md](./plan.md)).

**Update (2026-03-28):** For **manual download → local import**, Tally’s **CSV (spreadsheet)** export is the **primary** format consumed by `uscis-fill-local`; **JSON** remains supported. Webhook payloads stay **JSON** per Tally’s API.

**Update (2026-03-29):** **Shipped app** (`apps/uscis-fill-local`): staff upload **Tally export** + **USCIS fillable PDF**, click **Fill PDF**, receive a **DRAFT** download; **`pypdf`** drives AcroForm fill (**§6**). **SQLAlchemy/SQLite** and review/draft **services** exist for future matter-bound workflows but are **not** on the Streamlit hot path.

Consolidated decisions for Phase 0. Each item either resolves a `NEEDS CLARIFICATION` from Technical Context or records a deliberate technology choice.

---

## 1. Client questionnaire provider (Tally)

| Item | Decision |
|------|----------|
| **Decision** | Use **Tally** for client-facing forms per `spec.md`. Integrate via **staff export (CSV/JSON)** for the **required** local loop. **Optionally**, **Tally webhooks** (`FORM_RESPONSE`) and **Tally REST API** for hosted automation—not required by **FR-010**. |
| **Rationale** | Matches spec assumption; CSV export matches firm spreadsheet workflows; webhooks are an optional accelerator for a future hosted tier. |
| **Alternatives considered** | Typeform/Jotform (re-specify mappings); fully custom portal (higher build cost). |

**Matter binding (FR-003):** Tally supports **hidden fields** populated via **URL query parameters** (case-sensitive). The firm can email a **unique URL per invitation**, e.g. base form URL plus `matterId` / `invitationId` as hidden field params, so exports/webhooks can include those values. The **current Streamlit UI** does not collect `matter_id`; parsers still surface `matter_id_from_export` when present for future DB import.

**Staff export path:** Results download as **CSV**; the local Python app parses headers into field keys aligned with `tally_to_profile.yaml`.

---

## 2. Application shape and runtime

| Item | Decision |
|------|----------|
| **Decision (implemented)** | **Python 3.11+** package `uscis-fill-local`: **Streamlit** UI on **localhost** for uploads + **Fill PDF**; **`uscis-fill`** CLI for the same pipeline; **`pypdf`** for PDF. **No** Next.js requirement for the shipped product. |
| **Rationale** | Matches **FR-010** and spec clarification (simple Python stack); single process, minimal ops; firm-controlled machine. |
| **Alternatives considered** | **Next.js** (App Router) + hosted Node (**legacy research**): still a valid option if the firm later wants a **hosted** webhook + staff portal—see [contracts/staff-api.yaml](./contracts/staff-api.yaml) as a **future** shape. |

---

## 3. Data storage

| Item | Decision |
|------|----------|
| **Decision (implemented baseline)** | **SQLite** + **SQLAlchemy** in-repo for **optional** persistence (matters, submissions, review, draft metadata) used by **services**; the **primary** fill workflow runs **without** opening a DB. |
| **Decision (optional future)** | **PostgreSQL** + **Prisma** if a **hosted** multi-user staff portal replaces or augments the local tool—**not** in the shipped Python app. |
| **Rationale** | ACID when the firm adopts matter binding and review in-app; local SQLite matches single-workstation use. |
| **Alternatives considered** | PostgreSQL-only from day one (more ops than needed for file-in/file-out MVP). |

---

## 4. Staff authentication and authorization

| Item | Decision |
|------|----------|
| **Decision (implemented)** | **No** auth on **localhost Streamlit** v1; physical access + firm policy guard the workstation (**FR-007** partially delegated to environment). |
| **Decision (future hosted)** | **Auth** via hosted IdP or session middleware; **role-based** access in middleware and server actions. |
| **Rationale** | Smallest viable local tool; hosted tier would restore least privilege per **FR-007**. |
| **Alternatives considered** | Shared single password (weak); Clerk/Auth0 for a future portal. |

---

## 5. Invitation delivery (email)

| Item | Decision |
|------|----------|
| **Decision** | **Primary path (per spec clarification):** staff send **unique Tally URLs** to clients using the firm’s **office email** (manual compose/send). **Optional later:** transactional email from a hosted app. |
| **Rationale** | FR-001 is satisfied by **firm-delivered email**, including manual office email; it does **not** require the product to be the SMTP sender. |
| **Alternatives considered** | App-only transactional email (optional enhancement). |

---

## 6. USCIS PDF generation

| Item | Decision |
|------|----------|
| **Decision (implemented)** | **`pypdf`** against **official fillable USCIS PDFs**, driven by **`profile_to_i485.yaml`** (and Tally → profile YAML). Missing/ambiguous fields reported in UI (**FR-006**). |
| **Rationale** | Python-native; keeps output on-government templates; mappers are testable (SC-001). |
| **Alternatives considered** | **pdf-lib** in Node (fits a future TypeScript portal); PyMuPDF (optional heavier dependency). |

---

## 7. Audit and logging

| Item | Decision |
|------|----------|
| **Decision** | **SQLite `AuditLog`** when code paths use **`log_action`** (e.g. review updates). Stateless Streamlit fill does **not** emit DB audit rows today—rely on firm policy and OS-level access control for workstation use; expand when review UI lands. |
| **Rationale** | Constitution III (Auditability) and FR-008 for in-app actions. |
| **Alternatives considered** | Application stdout only (weaker for investigations). |

---

## 8. Third-party / subprocessor summary

| Service | Role | Data |
|---------|------|------|
| **Tally** | Form hosting, submission capture | Client PII as entered in questionnaire |
| **Email provider** (optional) | App-sent invitations, if adopted | Recipient address, link metadata |
| **Hosting / DB** (optional future) | Hosted portal + PostgreSQL | Application data per retention policy |
| **Identity provider** (optional future) | Staff login | Staff email, session metadata |

Document data flows and DPA review in security review before production.

---

## 9. Testing strategy (boundaries)

| Boundary | Approach |
|----------|----------|
| Tally webhook handler | Contract tests with **signed fixture payloads** **if** a webhook server is implemented; **not** required for shipped local fill. |
| Normalization / mapping | Unit tests: questionnaire export → structured profile (`test_tally_import.py`, `test_normalize.py`). |
| PDF fill | Golden tests per form: known profile → expected field values (`test_pdf_fill.py`, `test_simple_fill.py`). |
| Streamlit UI | Manual checklist: two uploads, **Fill PDF**, draft download, unfilled warnings ([quickstart.md](./quickstart.md)). |

---

## Open items (non-blocking for plan; implementation tickets)

- Exact USCIS form set for v1 (spec allows subset); **I-485** bundled.
- Streamlit **review** + **matter** screens (tasks T020, T025) if the firm wants **FR-003** / **FR-004** enforced in-app.
- Production hosting region and data residency policy **if** a hosted tier is added.
