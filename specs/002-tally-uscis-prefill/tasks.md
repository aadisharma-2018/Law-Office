# Tasks: Tally Questionnaire Intake and USCIS Form Prefill

**Input**: Design documents from `/Users/aadisharma/Desktop/Law-Office/specs/002-tally-uscis-prefill/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [data-model.md](./data-model.md), [contracts/](./contracts/), [research.md](./research.md), [quickstart.md](./quickstart.md)

**Tests**: No dedicated TDD phase—the spec does not mandate test-first delivery. **Polish** includes a small **pytest** slice for critical boundaries (import + PDF).

**Organization**: Tasks are grouped by user story ([US1]–[US3]) per [spec.md](./spec.md). **MVP** = Setup + Foundational + **User Story 1** (import + structured profile).

**Root paths**: All implementation paths are relative to repository root `Law-Office/`. Primary package: `apps/uscis-fill-local/`.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Parallelizable (different files, no ordering dependency within the same phase)
- **[USn]**: Maps to User Story *n* in [spec.md](./spec.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Python project layout and tooling per [plan.md](./plan.md).

- [x] T001 Create `apps/uscis-fill-local/pyproject.toml` with `requires-python = ">=3.11"`, package `uscis-fill`, and runtime deps `sqlalchemy`, `pypdf` (or `pymupdf` as optional extra), plus dev `pytest`, `ruff`
- [x] T002 [P] Create `apps/uscis-fill-local/README.md` describing local install (`pip install -e .`), data directory, and that client PII stays on firm-controlled disk
- [x] T003 [P] Add `apps/uscis-fill-local/.gitignore` ignoring `data/`, `*.sqlite3`, `.env`, and `resources/*.pdf` when not redistributable
- [x] T004 Create package scaffold: `apps/uscis-fill-local/src/uscis_fill/__init__.py`, `apps/uscis-fill-local/tests/__init__.py`, and `apps/uscis-fill-local/tests/conftest.py` with a temporary SQLite path fixture

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Persistence, entities from [data-model.md](./data-model.md), and audit hook used by all stories. **No user story work starts until this phase completes.**

- [x] T005 Implement SQLAlchemy models for `Client`, `Matter`, `QuestionnaireDefinition`, `QuestionnaireInvitation`, `Submission`, `ReviewDecision`, `DraftUscisOutput`, and `AuditLog` in `apps/uscis-fill-local/src/uscis_fill/models.py`
- [x] T006 Implement SQLite engine, session factory, and `init_db()` calling `create_all` in `apps/uscis-fill-local/src/uscis_fill/db.py`
- [x] T007 Implement `log_action(actor_user_id, action, matter_id, metadata)` persisting to `AuditLog` in `apps/uscis-fill-local/src/uscis_fill/audit.py`
- [x] T008 Implement `apps/uscis-fill-local/src/uscis_fill/config.py` resolving a firm-configurable **data directory** (env var or default under user home) for SQLite file and exports
- [x] T009 Implement `apps/uscis-fill-local/src/uscis_fill/repositories/clients_matters.py` for minimal `Client`/`Matter` create and get-by-id used by imports
- [x] T010 Implement `apps/uscis-fill-local/src/uscis_fill/repositories/submissions.py` for `Submission` insert/update and dedupe by `tally_response_id` when present
- [x] T011 [P] Add anonymized sample Tally exports at `apps/uscis-fill-local/tests/fixtures/tally_export_sample.csv` (primary) and `tally_export_sample.json` (compatibility) for parser tests

**Checkpoint**: Database + audit + repositories ready; User Story phases can begin.

---

## Phase 3: User Story 1 — Client intake via import (Priority: P1) — MVP core

**Goal**: Staff **download** a Tally submission export (**CSV** preferred; **JSON** optional) and **import** into the app; answers become a **structured case profile** with **unambiguous** matter binding per **FR-002**, **FR-003**.

**Independent Test**: Import `tests/fixtures/tally_export_sample.csv` or `tally_export_sample.json` (or a real export) and verify `Submission` rows store `raw_payload` and `normalized_profile` tied to the correct `Matter`.

### Implementation

- [x] T012 [US1] Implement Tally import in `apps/uscis-fill-local/src/uscis_fill/tally_import.py`: **`parse_tally_file` / `parse_tally_csv`** (primary) and **`parse_tally_export`** for JSON, extracting fields, hidden matter/invitation identifiers, and response id when present
- [x] T013 [P] [US1] Add first-pass field mapping from Tally keys to canonical profile keys in `apps/uscis-fill-local/src/uscis_fill/mappings/tally_to_profile.yaml`
- [x] T014 [US1] Implement `normalize_to_profile(raw: dict) -> tuple[dict, list]` in `apps/uscis-fill-local/src/uscis_fill/normalize.py` applying the YAML map and recording mapping warnings
- [x] T015 [US1] Implement `import_submission_file(session, matter_id, path)` in `apps/uscis-fill-local/src/uscis_fill/services/submission_service.py` that rejects import if matter cannot be resolved unambiguously per **FR-003** (fail closed)
- [x] T016 [US1] Add CLI entrypoint `apps/uscis-fill-local/src/uscis_fill/__main__.py` or `cli.py` with command to run import against a file path and matter id
- [x] T017 [US1] Add minimal GUI or Streamlit page in `apps/uscis-fill-local/src/uscis_fill/ui/app.py` to choose export file, enter/confirm `matter_id`, and trigger import with visible errors

**Checkpoint**: US1 complete—structured intake without review UI.

---

## Phase 4: User Story 2 — Attorney review before drafts (Priority: P1)

**Goal**: Record **ReviewDecision** (approved / needs follow-up); block draft generation when not approved per default policy in [spec.md](./spec.md).

**Independent Test**: Mark a submission `approved` with notes; verify `require_approved` blocks until status is `approved`.

### Implementation

- [x] T018 [US2] Implement `ReviewDecision` lifecycle in `apps/uscis-fill-local/src/uscis_fill/services/review_service.py` (`pending` → `approved` | `needs_follow_up`) with `decided_at` and optional notes
- [x] T019 [US2] Call `audit.log_action` from `review_service.py` on each decision change per **FR-008**
- [x] T020 [US2] Extend `apps/uscis-fill-local/src/uscis_fill/ui/app.py` to list submissions for a matter and edit review status
- [x] T021 [US2] Add `assert_submission_approved_for_drafts(submission_id)` in `apps/uscis-fill-local/src/uscis_fill/services/review_service.py` raising a clear error if not approved (default block per US2 acceptance)

**Checkpoint**: US2 complete—review gating ready for US3.

---

## Phase 5: User Story 3 — Generate local USCIS draft PDFs (Priority: P2)

**Goal**: Load **downloaded** official USCIS PDF template, fill from **approved** structured profile, output draft file path and **unfilled_fields** per **FR-005**, **FR-006**.

**Independent Test**: Given approved fixture profile + template PDF path, generate a PDF and assert known AcroForm fields match expected values; missing keys appear in `unfilled_fields`.

### Implementation

- [x] T022 [P] [US3] Implement AcroForm field listing and fill helpers in `apps/uscis-fill-local/src/uscis_fill/pdf_utils.py` using `pypdf`
- [x] T023 [US3] Add profile→PDF field mapping for first target form in `apps/uscis-fill-local/src/uscis_fill/mappings/profile_to_i485.yaml` (or chosen first form code; adjust filename to match selection)
- [x] T024 [US3] Implement `generate_draft(submission_id, template_pdf_path, form_code)` in `apps/uscis-fill-local/src/uscis_fill/services/draft_service.py` writing output under data dir, persisting `DraftUscisOutput` with `unfilled_fields` JSON and calling `audit.log_action`
- [x] T025 [US3] Integrate draft generation into `apps/uscis-fill-local/src/uscis_fill/ui/app.py` with template file picker, **disabled** until submission approved, and display list of unfilled/ambiguous fields
- [x] T026 [US3] Prefix output filenames and UI labels with **DRAFT** (or equivalent) so outputs are clearly not final filings per **FR-005**

**Checkpoint**: End-to-end path: import → review → generate labeled draft PDF.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Tests, documentation, constitution alignment (confidentiality, audit review).

- [x] T027 [P] Add unit tests `apps/uscis-fill-local/tests/unit/test_tally_import.py` and `apps/uscis-fill-local/tests/unit/test_normalize.py` using fixtures
- [x] T028 [P] Add golden PDF field assertion test `apps/uscis-fill-local/tests/golden/test_pdf_fill.py` (skip if no redistributable template in CI; document in test docstring)
- [x] T029 Document optional future **Tally webhook** endpoint referencing `specs/002-tally-uscis-prefill/contracts/tally-webhook-inbound.md` in `apps/uscis-fill-local/README.md` (out of scope for MVP per **FR-010**)
- [x] T030 Run through `specs/002-tally-uscis-prefill/quickstart.md` manually and reconcile any gaps in `apps/uscis-fill-local/README.md`
- [x] T031 Security and data-handling pass: ensure logs and `AuditLog.metadata` avoid raw PII where possible per Law Office Constitution; document retention in README
- [x] T032 Add `Makefile` or `scripts/run_local.sh` at `apps/uscis-fill-local/` to launch UI/CLI consistently

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends on | Blocks |
|-------|------------|--------|
| Phase 1 Setup | — | Phase 2 |
| Phase 2 Foundational | Phase 1 | US1, US2, US3 |
| Phase 3 US1 | Phase 2 | — (MVP shippable here) |
| Phase 4 US2 | Phase 2 + US1 data model usage | US3 (logical: review before drafts) |
| Phase 5 US3 | Phase 2 + US1 + US2 | — |
| Phase 6 Polish | All desired stories | — |

### User Story Dependencies

- **US1**: Starts after Foundational. No dependency on US2/US3.
- **US2**: Needs persisted `Submission` from US1 (or empty DB with manual seed). Can be built against fixtures without full UI from US1 if services exist.
- **US3**: Depends on **approved** submission (**US2**) and **structured profile** (**US1**).

Recommended sequence: **Foundational → US1 → US2 → US3 → Polish**.

### Parallel Opportunities

- **Phase 1**: T002, T003 in parallel after T001.
- **Phase 2**: T011 in parallel with T005–T010 once fixture format is agreed (or after T012 defines parser expectations).
- **Phase 5**: T022 can start in parallel with mapping YAML authoring if interfaces are stable.
- **Phase 6**: T027, T028 in parallel.

### Parallel Example: User Story 1

```text
# After T012 exists:
T013 [P] [US1] mappings/tally_to_profile.yaml
T016 [US1] CLI  ||  T017 [US1] UI   # different files; coordinate on submission_service API
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1): import + structured profile + minimal UI/CLI.
3. **Stop and validate** with real Tally export files (firm data stays local).

### Incremental Delivery

1. Add US2 (review gating).
2. Add US3 (PDF fill + unfilled list).
3. Polish: pytest boundaries, README, constitution notes.

### Suggested MVP Scope

- **MVP**: Phases 1–3 (T001–T017). Delivers **FR-002**, **FR-003** (import path), and **FR-010** core loop without draft PDFs.

---

## Notes

- **Optional webhook** (contracts + FastAPI) is **not** in this task list per **FR-010**; add a future epic if needed.
- **Task count**: 32 tasks (T001–T032).
- **Per-story counts**: US1 = 6 tasks (T012–T017), US2 = 4 tasks (T018–T021), US3 = 5 tasks (T022–T026), Setup = 4, Foundational = 7, Polish = 6.
