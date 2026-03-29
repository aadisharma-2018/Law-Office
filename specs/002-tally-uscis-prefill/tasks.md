# Tasks: Tally Questionnaire Intake and USCIS Form Prefill

**Input**: Design documents from `specs/002-tally-uscis-prefill/` (repo root: `Law-Office/`)  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [data-model.md](./data-model.md), [contracts/](./contracts/), [research.md](./research.md), [quickstart.md](./quickstart.md)

**Tests**: No dedicated TDD phase—the spec does not mandate test-first delivery. **Polish** includes a small **pytest** slice for critical boundaries (import + PDF).

**Organization**: Tasks are grouped by user story ([US1]–[US3]) per [spec.md](./spec.md).

**Shipped UX (2026-03-29):** The **primary** staff workflow is **local, stateless**: upload **Tally export (CSV or JSON)** + **USCIS fillable PDF** in Streamlit (or `uscis-fill` CLI), then **Fill PDF** → draft download. That path uses `tally_import` → `normalize` → `simple_fill` / `pdf_utils` and does **not** require SQLite. **SQLAlchemy models**, **submission/review/draft services**, and **repositories** exist for a future matter-bound, review-gated UI but are **not** wired into the Streamlit page or the fill CLI today.

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

**Purpose**: Persistence, entities from [data-model.md](./data-model.md), and audit hook for **future** matter/review flows and programmatic use. The **shippped** fill path does not depend on this phase at runtime.

- [x] T005 Implement SQLAlchemy models for `Client`, `Matter`, `QuestionnaireDefinition`, `QuestionnaireInvitation`, `Submission`, `ReviewDecision`, `DraftUscisOutput`, and `AuditLog` in `apps/uscis-fill-local/src/uscis_fill/models.py`
- [x] T006 Implement SQLite engine, session factory, and `init_db()` calling `create_all` in `apps/uscis-fill-local/src/uscis_fill/db.py`
- [x] T007 Implement `log_action(actor_user_id, action, matter_id, metadata)` persisting to `AuditLog` in `apps/uscis-fill-local/src/uscis_fill/audit.py`
- [x] T008 Implement `apps/uscis-fill-local/src/uscis_fill/config.py` resolving a firm-configurable **data directory** (env var or default under user home) for SQLite file and exports
- [x] T009 Implement `apps/uscis-fill-local/src/uscis_fill/repositories/clients_matters.py` for minimal `Client`/`Matter` create and get-by-id used by imports
- [x] T010 Implement `apps/uscis-fill-local/src/uscis_fill/repositories/submissions.py` for `Submission` insert/update and dedupe by `tally_response_id` when present
- [x] T011 [P] Add anonymized sample Tally exports at `apps/uscis-fill-local/tests/fixtures/tally_export_sample.csv` (primary) and `tally_export_sample.json` (compatibility) for parser tests

**Checkpoint**: Database + audit + repositories available for import/review/draft **services**; primary UI remains file-in/file-out.

---

## Phase 3: User Story 1 — Client intake (parse + profile) (Priority: P1)

**Goal**: **Parse** a downloaded Tally export (**CSV** primary; **JSON** supported), produce a **structured case profile** (**FR-002**), and (when using DB import APIs) bind to a **Matter** with **unambiguous** matter id (**FR-003**).

**Shipped test**: Upload sample CSV/JSON + template in Streamlit and confirm normalized profile preview + filled PDF. Optionally: call `import_submission_file` in tests with a `matter_id` when exercising the DB path.

### Implementation

- [x] T012 [US1] Implement Tally import in `apps/uscis-fill-local/src/uscis_fill/tally_import.py`: **`parse_tally_file` / CSV path** (primary) and **JSON** parsing, extracting fields, hidden matter/invitation identifiers, and response id when present
- [x] T013 [P] [US1] Add first-pass field mapping from Tally keys to canonical profile keys in `apps/uscis-fill-local/src/uscis_fill/mappings/tally_to_profile.yaml`
- [x] T014 [US1] Implement `normalize_to_profile(raw: dict) -> tuple[dict, list]` in `apps/uscis-fill-local/src/uscis_fill/normalize.py` applying the YAML map and recording mapping warnings
- [x] T015 [US1] Implement `import_submission_file(session, matter_id, path)` in `apps/uscis-fill-local/src/uscis_fill/services/submission_service.py` that rejects import if matter cannot be resolved unambiguously per **FR-003** (fail closed) — **library/API path; not exposed in Streamlit v1**
- [x] T016 [US1] CLI entrypoint `apps/uscis-fill-local/src/uscis_fill/cli.py` (via `__main__`): **`uscis-fill --tally … --template … --out …`** for **stateless PDF fill** (no DB on the hot path)
- [x] T017 [US1] Streamlit UI `apps/uscis-fill-local/src/uscis_fill/ui/app.py`: **upload Tally export + USCIS PDF**, optional form mapping (**I-485**), **Fill PDF**, profile preview, unfilled-field warnings, **Download DRAFT PDF** — **no matter id field in v1**

**Checkpoint**: US1 parsing + normalization drive the **shipped** fill experience.

---

## Phase 4: User Story 2 — Attorney review before drafts (Priority: P1)

**Goal**: Record **ReviewDecision** (approved / needs follow-up); block draft generation when not approved when using **draft_service** (**spec** default policy).

**Service-layer test**: `review_service` transitions + `assert_submission_approved_for_drafts` behave as expected.

### Implementation

- [x] T018 [US2] Implement `ReviewDecision` lifecycle in `apps/uscis-fill-local/src/uscis_fill/services/review_service.py` (`pending` → `approved` | `needs_follow_up`) with `decided_at` and optional notes
- [x] T019 [US2] Call `audit.log_action` from `review_service.py` on each decision change per **FR-008**
- [ ] T020 [US2] Streamlit (or other) UI to list submissions for a matter and edit review status — **deferred**; staff review is **out-of-band** for the stateless fill path ([spec.md](./spec.md) “Implemented slice” under US3)
- [x] T021 [US2] Add `assert_submission_approved_for_drafts(submission_id)` in `apps/uscis-fill-local/src/uscis_fill/services/review_service.py` raising a clear error if not approved (used by `draft_service`, not by Streamlit v1)

**Checkpoint**: Review **services** ready; **UI** for review not in shipped Streamlit app.

---

## Phase 5: User Story 3 — Generate local USCIS draft PDFs (Priority: P2)

**Goal**: Fill **downloaded** official USCIS PDF from structured profile; surface **unfilled** AcroForm fields (**FR-005**, **FR-006**).

**Shipped test**: Golden/unit PDF tests + manual Streamlit **Fill PDF** with fixture export.

### Implementation

- [x] T022 [P] [US3] Implement AcroForm field listing and fill helpers in `apps/uscis-fill-local/src/uscis_fill/pdf_utils.py` using `pypdf`
- [x] T023 [US3] Add profile→PDF field mapping for first target form in `apps/uscis-fill-local/src/uscis_fill/mappings/profile_to_i485.yaml`
- [x] T024 [US3] Implement `generate_draft(submission_id, template_pdf_path, form_code)` in `apps/uscis-fill-local/src/uscis_fill/services/draft_service.py` writing output under data dir, persisting `DraftUscisOutput` with `unfilled_fields` JSON and calling `audit.log_action` — **DB-backed path**; parallel to stateless `simple_fill`
- [ ] T025 [US3] Wire **draft_service** into Streamlit with approval gate — **deferred**; Streamlit uses `fill_tally_export_into_pdf` in `simple_fill.py` directly (no `submission_id`)
- [x] T026 [US3] Prefix output filenames and UI labels with **DRAFT** (or equivalent) so outputs are clearly not final filings per **FR-005**

**Checkpoint**: **Stateless** path: Tally file + template → draft PDF in UI/CLI. **Stateful** draft artifact path remains available via services.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Tests, documentation, constitution alignment (confidentiality, audit review).

- [x] T027 [P] Add unit tests `apps/uscis-fill-local/tests/unit/test_tally_import.py` and `apps/uscis-fill-local/tests/unit/test_normalize.py` using fixtures
- [x] T028 [P] Add golden PDF field assertion test `apps/uscis-fill-local/tests/golden/test_pdf_fill.py` (skip if no redistributable template in CI; document in test docstring)
- [x] T029 Document optional future **Tally webhook** endpoint referencing `specs/002-tally-uscis-prefill/contracts/tally-webhook-inbound.md` in `apps/uscis-fill-local/README.md` (out of scope for MVP per **FR-010**)
- [x] T030 Run through `specs/002-tally-uscis-prefill/quickstart.md` manually and reconcile any gaps in `apps/uscis-fill-local/README.md`
- [x] T031 Security and data-handling pass: ensure logs and `AuditLog.metadata` avoid raw PII where possible per Law Office Constitution; document retention in README
- [x] T032 Add `Makefile` or `scripts/run_local.sh` at `apps/uscis-fill-local/` to launch UI/CLI consistently (`make ui`, `make test`)

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends on | Blocks |
|-------|------------|--------|
| Phase 1 Setup | — | Phase 2 |
| Phase 2 Foundational | Phase 1 | Optional DB stories |
| Phase 3 US1 | Phase 1 (T012–T014 need only package + fixtures conceptually) | — **Shippable: stateless fill** |
| Phase 4 US2 | Phase 2 for persisted review | **draft_service** approval gate |
| Phase 5 US3 | US1 parsing/mapping; **DB draft path** needs US2 | **Streamlit fill** needs only US1 + T022–T023 + `simple_fill` |

### User Story Dependencies

- **US1**: Parsing + Streamlit/CLI fill path does **not** require US2/US3 database flows.
- **US2**: Uses persisted `Submission` when staff use `import_submission_file` / future UI.
- **US3 (UI)**: **Shipped** Streamlit flow uses **in-memory** profile from export file, not an approved `Submission` row.

Recommended sequence for **full** vision: **Foundational → US1 → US2 → US3 (DB) → Polish**. **Delivered first**: US1 stateless fill + PDF utilities + tests.

### Parallel Opportunities

- **Phase 1**: T002, T003 in parallel after T001.
- **Phase 2**: T011 in parallel with T005–T010 once fixture format is agreed.
- **Phase 5**: T022 can start in parallel with mapping YAML authoring.
- **Phase 6**: T027, T028 in parallel.

---

## Implementation Strategy

### Shipped slice (stateless fill)

1. Complete Phase 1; T012–T014 + T022–T023 + Streamlit + fill CLI (**T016–T017**).
2. Validate with real Tally exports and official PDFs (firm data stays local).

### Incremental delivery

1. Optional: T020 + T025 — wire SQLite **matter**, **review**, and **draft_service** into the UI for **FR-003** / **FR-004** gating.
2. Polish: pytest boundaries, README, constitution notes.

### MVP scope (current product)

- **MVP**: Two-input **Fill PDF** path (**FR-010** core), I-485 mapping YAML, draft labeling, unfilled-field reporting.

---

## Notes

- **Optional webhook** (contracts + FastAPI) is **not** in the shipped app per **FR-010**; add a future epic if needed.
- **Open tasks**: T020, T025 (review UI + DB-backed draft generation in Streamlit).
- **Task count**: 32 tasks (T001–T032); 2 deferred with `[ ]`.
