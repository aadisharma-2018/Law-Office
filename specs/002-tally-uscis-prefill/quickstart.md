# Quickstart: Tally Questionnaire Intake and USCIS Form Prefill

**Branch**: `002-tally-uscis-prefill`  
**Date**: 2025-03-24 (updated 2026-03-29: shipped `uscis-fill-local` workflow)

This document is the **onboarding checklist** for [apps/uscis-fill-local](../../apps/uscis-fill-local/README.md). A **hosted** portal + **webhooks** remain **optional** ([spec.md](./spec.md) **FR-010**); they are **not** required to run the tool below.

## Prerequisites

- **Python 3.11+**
- **Tally** account (export questionnaires as **CSV** or **JSON**)
- Official **USCIS fillable PDF** for the form you are mapping (e.g. I-485)

**Not required for the shipped path:** Node.js, PostgreSQL, ngrok, or Tally API keys.

## Install and run the UI

```bash
cd apps/uscis-fill-local
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
make ui
```

In the browser:

1. Upload the **Tally export** (`.csv` or `.json`).
2. Upload the **USCIS fillable PDF**.
3. Choose **Form mapping** (bundled: **I-485**).
4. Click **Fill PDF**, then **Download DRAFT PDF**.

Adjust mappings if needed:

- Tally columns → profile: `src/uscis_fill/mappings/tally_to_profile.yaml`
- Profile → AcroForm names: `src/uscis_fill/mappings/profile_to_i485.yaml`

## Command line (same pipeline, no database)

```bash
uscis-fill --tally path/to/export.csv --template path/to/AOS-form-fillable.pdf --out path/to/DRAFT-out.pdf
```

`--tally` accepts `.csv` or `.json`. Optional: `--form I-485`.

## Tests

```bash
make test
```

## Optional: hosted / webhook path (future)

If the firm adds a **network** tier later, the following become relevant ([contracts/](./contracts/)):

| Variable (illustrative) | Purpose |
|---------------------------|---------|
| `DATABASE_URL` | PostgreSQL (hosted portal only) |
| `TALLY_API_KEY` | Tally API (webhook registration) |
| `TALLY_WEBHOOK_SECRET` | Webhook signature verification |
| `AUTH_SECRET` | Staff session secret |
| `PUBLIC_APP_URL` | Webhook callback base URL |

For local webhook development you would expose **HTTPS** (e.g. ngrok) per [contracts/tally-webhook-inbound.md](./contracts/tally-webhook-inbound.md). This is **out of scope** for the current Python-only fill app.

## Optional: SQLite / matter import (library)

The package includes SQLAlchemy models and `submission_service.import_submission_file` for **matter-bound** imports (**FR-003**). There is **no** Streamlit screen for matter selection yet; use programmatically or extend the UI per [tasks.md](./tasks.md) (T020, T025).

## Verification checklist (shipped app)

- [ ] Streamlit: both files upload, **Fill PDF** enabled only when both present
- [ ] Draft download opens; AcroForm fields match mapping for a known fixture
- [ ] Unfilled PDF fields are listed when intake or names are missing
- [ ] `uscis-fill` CLI writes the same draft bytes as the UI for the same inputs
- [ ] (Optional future) Webhook signature verification; matter association from hidden fields

## References

- [spec.md](./spec.md) — requirements and **Current implementation** section
- [plan.md](./plan.md) — technical context
- [data-model.md](./data-model.md) — entities (full product; partial use today)
