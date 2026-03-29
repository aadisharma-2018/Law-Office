# Feature Specification: Tally Questionnaire Intake and USCIS Form Prefill

**Feature Branch**: `002-tally-uscis-prefill`  
**Created**: 2025-03-24  
**Status**: Draft (local fill tool implemented; invitation/review/DB workflows beyond minimal path not required for core FR-010)  
**Input**: User description: "I want to send the questionares to my clients via tally.so. Once they sent back the inforamtion i need to review and auto-fill the USCIS form based on the information on the questionare. what is the best way to go about implementing this?"

## Current implementation — local fill app (`apps/uscis-fill-local`)

Staff use a **minimal local-first** tool that takes **two file inputs** and produces a **draft** filled PDF. This matches **FR-010** (core read/map/fill runs locally) without requiring webhooks, hosted portals, or a database for the primary path.

### Streamlit UI

1. **Tally export** — upload the questionnaire export (**CSV** is the primary format; **JSON** is also accepted for compatibility and testing). The app parses and normalizes rows into a canonical profile (see `tally_import`, normalization, and Tally-to-profile mapping assets in the app).
2. **USCIS fillable PDF** — upload the **official fillable PDF** (AcroForm template) that should receive the mapped values.
3. **Form mapping** — the bundled UI offers **I-485**; field names are driven by `mappings/profile_to_i485.yaml` (staff can edit mappings to match their PDF’s AcroForm field names).
4. **Fill PDF** — when both files are present, the user clicks **Fill PDF**. The app fills the template from the normalized profile, then:
   - shows a **preview** of the normalized profile;
   - **warns** with any PDF fields that were not filled (missing intake value or field name mismatch);
   - offers **Download DRAFT PDF** for attorney review (**not** for filing as-is).

Copy in the UI states explicitly that output is a draft for professional review.

### Command-line equivalent

The same pipeline is available via `uscis-fill`：**`--tally`** (path to `.csv` or `.json`), **`--template`** (path to `.pdf`), **`--out`** (output path), optional **`--form`** (default `I-485`). No database is used on this path.

### Scope note

The **full** product vision in this specification still includes unique invitation links, structured matter binding, in-app review approval, and traceability (**FR-001–FR-009**). The **currently shipped** user-facing workflow for turning a downloaded Tally export and a downloaded USCIS template into a draft PDF is the **two-input + Fill PDF** flow above; other requirements remain targets for later increments unless explicitly deferred. Setup and verification: [quickstart.md](./quickstart.md); task-level deltas: [tasks.md](./tasks.md).

## Clarifications

### Session 2025-03-24

- Q: How will clients receive questionnaire invitation links? → A: By email from the firm.
- Q: How should a completed questionnaire bind to the correct client and matter? → A: **Unique invitation link per matter or per invitation** so the submission maps to the correct matter automatically (Option A).
- Q: Must the product send invitation emails, or may staff send unique Tally links using office email? → A: Staff may send invitations **manually** using the firm’s **office email**; the product is **not** required to send invitation emails.

### Session 2026-03-24

- Q: How simple and localized should the intake-to-USCIS workflow be? → A: **Local-first and minimal**: staff **download** the client’s questionnaire submission (from the provider), **download** the relevant official USCIS form, and use an application that **reads** the questionnaire data and **copies/maps** it **locally** into the USCIS form—without relying on a complex cloud-hosted system for the core read/map/fill workflow.
- Q: What implementation stack should the firm target? → A: A **very simple tech stack based on Python** (details in implementation planning, not binding on acceptance tests).

### Session 2026-03-28

- Q: What file format does staff use when they download questionnaire results from Tally for the local import path? → A: Tally’s **spreadsheet (CSV)** export is the **primary** format supported for the simplified local tool; **JSON** exports remain **supported** for compatibility and testing. Column headers map to intake keys after normalization (see app `tally_import` and `tally_to_profile.yaml`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Client completes firm questionnaire (Priority: P1)

The firm delivers to the client **a unique questionnaire invitation link by email** (unique to the matter or to that specific invitation)—for example **composed and sent by staff from the firm’s office email**—using the firm’s chosen online questionnaire provider. The client opens the link from email, completes the questionnaire, and submits answers. The firm obtains those answers for case preparation in a structured way: **either** via provider mechanisms that preserve matter association **or** by **downloading/exporting** the submission and **importing** it into the firm’s tool, with **unambiguous** matter association per **FR-003**. The firm **does not** require a heavyweight cloud stack for the **core** step of reading questionnaire data and filling USCIS forms **locally** (see **FR-010**).

**Why this priority**: Without reliable capture of client answers, review and preparation of government forms cannot proceed.

**Independent Test**: Send a test questionnaire invitation by email, complete a test submission from the linked questionnaire, and confirm the firm can access all required answers for the intended client or matter **in the structured workflow** (including, if applicable, by **downloading** the submission and **importing** it into the firm’s application).

**Acceptance Scenarios**:

1. **Given** a client has been invited by email to complete a questionnaire, **When** they submit all required answers, **Then** the submission is recorded and available to authorized firm users without loss of required fields.
2. **Given** a questionnaire definition has required fields, **When** the client attempts to submit without completing them, **Then** the client is guided to complete missing items before submission succeeds (per the provider’s capabilities).
3. **Given** the firm has sent a questionnaire link to the client’s email address on file, **When** the client opens the email and uses the link, **Then** they can access and complete the questionnaire without requiring a separate firm-specific account unless otherwise specified in planning.
4. **Given** an invitation was issued for a specific matter, **When** the client submits the questionnaire, **Then** the submission is recorded against that same matter (and client) without staff manually selecting the matter from a list at submit time.
5. **Given** staff use a **downloaded/exported** submission file, **When** they import it into the firm’s tool, **Then** the submission is associated only with the **intended** matter using **unambiguous** binding per **FR-003** (embedded identifiers and/or explicit confirmation).

---

### User Story 2 - Attorney reviews submission before use (Priority: P1)

An authorized firm user opens a submitted questionnaire, verifies completeness and plausibility, and records whether the information may be used for preparing official drafts (or notes what is missing or needs follow-up).

**Why this priority**: Using unreviewed client input for government forms creates professional and filing risk.

**Independent Test**: Open a test submission, complete the review steps, and confirm that unapproved data is not treated as final for draft generation intended for filing preparation.

**Acceptance Scenarios**:

1. **Given** a new submission exists, **When** an authorized user completes review, **Then** they can record that it is approved for draft preparation or that corrections or additional information are required.
2. **Given** a submission is not approved, **When** the firm attempts to generate official-form drafts for filing preparation, **Then** the system blocks or clearly warns according to firm policy (default: block until approved).

---

### User Story 3 - Generate USCIS drafts from approved information (Priority: P2)

After approval, an authorized user generates draft USCIS forms populated from the structured information derived from the questionnaire, for attorney review before any filing. Generation and field mapping run **on firm-controlled systems** (**local-first** per **FR-010**), using **downloaded** official USCIS form files as the fill targets.

**Implemented slice (today)**: Staff provide a **downloaded Tally export** and a **downloaded USCIS fillable PDF**, then run the local app and click **Fill PDF** (or use the CLI). That path assumes the firm has already satisfied review outside the tool if required by policy; the app still labels output as a **draft** and surfaces unfilled fields (**FR-006**). A future increment can enforce **FR-004** (in-app approval gating) before generation.

**Why this priority**: This delivers the time savings after the firm trusts the underlying data.

**Independent Test**: From an approved structured record with known test values, request generation of at least one supported USCIS draft and confirm populated fields match the approved values (allowing normal formatting differences). For the shipped app, use a known-good CSV/JSON export and template and assert field values and unfilled warnings after **Fill PDF**.

**Acceptance Scenarios**:

1. **Given** an approved structured record for a matter, **When** the user requests draft generation for a supported USCIS form in scope, **Then** the system produces a draft with mappable fields filled from that record.
2. **Given** a value is missing or ambiguous in the structured record, **When** draft generation runs, **Then** the user sees which fields were not populated or need manual input.

---

### Edge Cases

- The questionnaire is revised after a client started: the firm can tell which definition version applies and how answers map to the structured case profile.
- Incomplete or inconsistent answers: review captures gaps; the system does not silently invent facts to fill fields.
- Multiple matters for one client: submissions and drafts associate to the correct matter to avoid cross-case data bleed.
- Correction after an initial submission: the firm can follow a defined policy (for example: new submission supersedes prior, or parallel revisions with clear audit) without losing accountability.
- Email to the client fails or is wrong: the firm can correct the address or resend the invitation per firm policy, without losing traceability of which matter the invitation was for.
- The invitation link is shared or forwarded: the submission still associates with the matter the invitation was issued for; the firm relies on review before approval to catch misuse or wrong respondent where relevant.
- **Download/import path**: exported or downloaded submission files are malformed, incomplete, or for the wrong matter—the system MUST NOT silently attach them to the wrong matter; staff can correct or re-import per firm policy.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The firm MUST be able to deliver to each client a **unique** questionnaire invitation link using the firm’s designated online questionnaire provider, **by email**. That email MAY be sent **manually** by authorized staff using the firm’s **office email client**; a **system-sent** invitation email is **not** required to satisfy this requirement.
- **FR-002**: The system MUST represent submitted answers in a **structured** form suitable for reuse across multiple USCIS forms, not only as a static document snapshot. Intake MAY combine **provider export/download** (e.g. from Tally) **and/or** other capture methods described in planning, provided the structured representation is achieved.
- **FR-003**: Submissions MUST be associable to the correct client and matter so information is not mixed between cases. **Where** the questionnaire uses **unique links per matter or per invitation**, completed responses MUST tie to that matter **automatically** (without the client typing a case code). **Where** the firm uses **downloaded/exported** submission files, matter association MUST be **unambiguous** (for example **embedded identifiers** in the export **or** explicit **staff confirmation** at import).
- **FR-004**: Authorized firm users MUST be able to review submissions and record whether the information is approved for use in preparing official drafts.
- **FR-005**: For USCIS forms in scope, the system MUST produce draft outputs populated from approved structured data, clearly presented as drafts requiring professional review before filing. Staff MUST be able to use **official USCIS form files** (e.g. **downloaded** fillable PDFs) as the **targets** for filling.
- **FR-006**: The system MUST surface fields that cannot be populated or are ambiguous rather than filling incorrect values without notice.
- **FR-007**: Access to client and matter information MUST follow least privilege; only authorized roles may view submissions and generated drafts.
- **FR-008**: Material actions (for example: access to sensitive submissions, approval decisions, generation of drafts) MUST be traceable for accountability consistent with the Law Office Constitution.
- **FR-009**: Third-party services used to collect or process client or matter data MUST be identified in planning with respect to confidentiality, retention, and subprocessors.
- **FR-010**: The **core** workflow for reading questionnaire data and writing it into USCIS forms MUST run **locally** on **firm-controlled** systems (simple, localized tooling). **Network-hosted** automation (for example **webhook ingestion**) MAY exist as an **optional** convenience but MUST NOT be required to achieve the primary outcome described in this specification.

### Key Entities

- **Client / matter**: The legal context that owns a questionnaire response and resulting drafts.
- **Questionnaire invitation**: A **unique** questionnaire URL scoped to a specific matter (or invitation instance), **delivered to the client by email** (including manual send from office email), so that the provider’s submission can be linked to that matter without separate client-entered identifiers.
- **Questionnaire definition**: The questions and semantics the firm uses for a given intake, including versioning when questions change.
- **Submission**: A completed response instance tied to a client or matter, with time of receipt and reference to the questionnaire definition version.
- **Review decision**: Record of review outcome and whether data is approved for draft preparation.
- **Structured case profile**: Normalized answers used for mapping to multiple USCIS forms.
- **Draft USCIS output**: A generated draft government form prepared from the structured case profile for attorney review.
- **Downloaded form template**: An official USCIS fillable PDF (or successor format) obtained by the firm and supplied to the filling process.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In structured test cases with complete, approved inputs, each in-scope USCIS form type can produce a draft where at least 95% of fields defined as mappable for that form are populated correctly compared to the approved source values.
- **SC-002**: Authorized users can locate a given client’s latest submission and its review status within two minutes in usability testing with representative test data.
- **SC-003**: During a pilot period, median staff time from submission receipt to readiness for attorney review of generated drafts decreases by at least 40% compared to fully manual retyping for the same supported forms (measured on pilot matters).
- **SC-004**: In structured testing, there are zero instances of a submission or draft being associated with the wrong client or matter.

## Assumptions

- The firm uses Tally (tally.so) as the client-facing questionnaire provider unless the scope is explicitly changed later.
- Initial delivery may support a subset of USCIS forms; additional forms are added incrementally with explicit scope.
- “Auto-fill” means generating drafts for attorney review; filing decisions remain with the attorney.
- Resubmission and versioning rules follow firm policy; the product supports at least one clear policy without ambiguous loss of audit history.
- Clients have connectivity and devices sufficient to complete a web questionnaire under typical consumer conditions.
- Clients can receive email at addresses the firm maintains for communications.
- Each emailed invitation uses a **unique** link per matter or per invitation so matter association does not depend on the client typing a case code.
- Staff may **manually** send those links from **office email**; automated invitation email from the product is optional.
- The firm prefers a **simple, local-first** tool: **download** questionnaire submissions as needed, **download** USCIS form templates, and **map/fill locally**—see **FR-010**.
- **Automated** server-side ingestion (e.g. webhooks) is **optional** and not required for the core workflow (**FR-010**).
- The firm prefers a **simple Python-based** implementation for the local tool; concrete libraries and packaging are defined in planning.
