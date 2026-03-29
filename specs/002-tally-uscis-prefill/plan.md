# Implementation Plan: Tally Questionnaire Intake and USCIS Form Prefill

**Branch**: `002-tally-uscis-prefill` | **Date**: 2025-03-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-tally-uscis-prefill/spec.md`

## Summary

Per [spec.md](./spec.md) (**FR-010**, Session 2026-03-24), the **primary** delivery is **simple and local-first**: staff **download** questionnaire submissions (e.g. from Tally as **CSV** spreadsheet export; **JSON** also supported), **download** official **USCIS fillable PDFs**, and run a **firm-controlled local application** that **reads** the questionnaire data and **maps/fills** USCIS forms **on device**—no **required** cloud-hosted processing for that core loop.

Staff may still **email unique Tally links** from **office email** (earlier clarifications). **Tally webhooks** and a **hosted** staff portal are **optional** accelerators, **not** prerequisites: **FR-010** explicitly allows **network-hosted** automation only as **optional** convenience.

**Implemented (2026-03-29):** [apps/uscis-fill-local](../../apps/uscis-fill-local/) delivers **Streamlit** + **`uscis-fill` CLI**: upload **Tally export (CSV/JSON)** + **USCIS fillable PDF** → **Fill PDF** → **DRAFT** download. **`simple_fill`** / **`pypdf`** implement the core loop. **Review** and **draft_service** (SQLite) exist in the package but are **not** wired into that UI yet ([tasks.md](./tasks.md)).

**Implication for implementation:** **Python** localhost tool with **file-based import** + **PDF fill** is **shipped**; **in-app review** and **hosted webhook + sync** are **later** increments if desired. Subprocessors for the shipped slice: **Tally** (forms + exports) only. See [research.md](./research.md).

## Technical Context

**Language/Version**: **Python 3.11+** (per [spec.md](./spec.md) clarification: simple Python stack)  
**Primary Dependencies**: **`pypdf`** or **PyMuPDF** for AcroForm/fillable PDF; **`sqlite3`** or **SQLAlchemy** + SQLite for local state; minimal UI via **Tkinter**, **CustomTkinter**, **PyQt/PySide**, or **Streamlit** for local browser—pick smallest that meets review UX; **`httpx`** / **`requests`** only if webhooks added later  
**Storage**: **SQLite** or **flat files** under a firm-chosen data directory  
**Testing**: **pytest**; import fixtures for Tally exports (**CSV** + **JSON**); golden PDF comparisons; optional webhook tests **only if** webhooks ship  
**Target Platform**: **Windows/macOS desktop** or **localhost** browser (firm-controlled machine); optional Linux VPS **only for** optional webhook service  
**Project Type**: **local application** (desktop or localhost) with **optional** network components  
**Performance Goals**: Import + fill under interactive thresholds on a typical laptop; optional webhook 2xx under provider retry limits if implemented  
**Constraints**: Client/matter data stays on **firm-controlled** storage by default; secrets out of source control  
**Scale/Scope**: Single small firm; low concurrent users; **simplicity over multi-tenant cloud**  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence in this plan |
|-----------|--------|------------------------|
| **I. Confidentiality & data minimization** | Pass | Raw Tally payloads and profiles stored only for stated intake/draft workflows; hidden-field strategy avoids extra client identifiers; secrets via env ([quickstart](./quickstart.md)). |
| **II. Spec-driven delivery** | Pass | Plan and artifacts trace to [spec.md](./spec.md) FR/US/SC; scope changes require spec updates. |
| **III. Auditability** | Pass | Local audit trail (file or SQLite) for review/draft actions; [data-model.md](./data-model.md) pattern adaptable; [research.md](./research.md) §7. |
| **IV. Testing discipline** | Pass | [research.md](./research.md) §9 + **import/PDF** boundaries per **FR-010**; webhook tests **if** webhooks exist. |
| **V. Simplicity** | Pass | **Local-first** stack per **FR-010**; hosted pieces **optional** and tracked in [Complexity Tracking](#complexity-tracking). |

**Post–Phase 1 re-check:** Re-validate after spec change **FR-010**: **local-first** core; **contracts/** webhooks are **optional**—**Pass** with note to refresh `data-model.md` on next implementation pass.

## Project Structure

### Documentation (this feature)

```text
specs/002-tally-uscis-prefill/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/           # Phase 1
│   ├── README.md
│   ├── tally-webhook-inbound.md
│   └── staff-api.yaml
├── spec.md
└── tasks.md             # Phase 2: /speckit.tasks (not created by this command)
```

### Source Code (repository root)

Greenfield layout **(Python, local-first)** when implementation starts:

```text
apps/uscis-fill-local/
├── pyproject.toml            # or requirements.txt
├── src/
│   └── uscis_fill/         # import, normalize, review, pdf_fill, audit
├── resources/               # USCIS template PDFs (gitignored if not redistributable)
└── tests/
    ├── fixtures/            # Sample Tally exports
    ├── golden/              # PDF output checks
    └── unit/

```

**Optional** (Phase 2): `src/uscis_fill/webhook_server.py` or small **FastAPI** app—only if hosted **Tally webhook** is adopted (not required by **FR-010**).

**Structure Decision**: **Single Python package** under `apps/uscis-fill-local/` for **download → import → review → fill**. Add a **hosted** component only if the firm wants automatic webhook ingestion later.

## Complexity Tracking

> No unjustified constitution violations. For **local-first MVP**, core external dependency is **Tally** (client forms + staff **downloads**); **host/DB** are optional until cloud webhook or sync is added ([spec.md](./spec.md) **FR-010**).

_No rows — no violations requiring justification._

---

## Phase 0: Outline & Research

**Output:** [research.md](./research.md)

Resolved: **local-first** **Python** stack, Tally via **export/download + import** (webhooks optional), invitation path (manual office email), PDF approach (AcroForm via **pypdf**/PyMuPDF), audit strategy, **pytest** boundaries. **Refresh** when UI toolkit (Tkinter vs Streamlit vs Qt) is chosen.

## Phase 1: Design & Contracts

**Outputs:**

- [data-model.md](./data-model.md) — entities, validation, review states  
- [contracts/](./contracts/) — Tally inbound consumer contract; representative staff OpenAPI  
- [quickstart.md](./quickstart.md) — env vars, Tally setup, local webhook testing  

**Agent context:** Updated via `.specify/scripts/bash/update-agent-context.sh cursor-agent`.

## Phase 2

Implementation tasks are **not** produced by `/speckit.plan`. Run **`/speckit.tasks`** when ready.

---

## Subprocessors & data flows (FR-009)

| System | Flow |
|--------|------|
| **Tally** | Client enters PII in forms; staff obtain responses via **provider export/download** (primary per **FR-010**). Optional: Tally **webhooks** to a hosted endpoint. |
| **Firm app (local)** | Import/export files, structured profile, review, draft PDFs, audit (SQLite or local files per implementation). |
| **Firm app + PostgreSQL** (optional) | If a **hosted** tier is added: sync/store matter-linked submissions, profiles, reviews, drafts metadata, audit. |
| **Firm office email** (e.g. Microsoft 365 / Google Workspace) | Staff **manually** send clients unique Tally URLs; governed by firm’s existing email terms and mailbox security—not the app’s SMTP. |
| **Email provider** (optional) | Only if the product sends invitation email ([research.md](./research.md) §5). |
| **Identity provider** (optional) | Staff authentication only. |

Review DPAs/terms for **Tally** before production client data; review optional email provider only if app-sent mail is enabled.
