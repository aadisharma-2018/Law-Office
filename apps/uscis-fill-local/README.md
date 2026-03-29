# uscis-fill (local)

Fill an official **USCIS fillable PDF** using answers from a **Tally** export (typically **CSV**; JSON is also supported). Everything runs on your machine.

## What you need

1. **Tally export** — Download your questionnaire results as **CSV** (wide format: one row per response, column headers in the first row). JSON exports still work if you use that path.
2. **USCIS PDF** — the fillable PDF from USCIS for the form you are preparing (e.g. I-485).

### CSV notes

- Column headers are turned into intake keys like `given_name`, `family_name` (spaces and punctuation normalized to snake_case). Align names with `src/uscis_fill/mappings/tally_to_profile.yaml`, or rename columns in the export / mapping file.
- If the file has **multiple data rows**, the **last** non-empty row is used (common when the export appends new responses).

## Setup

```bash
cd apps/uscis-fill-local
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Use the app (simplest)

```bash
make ui
```

Then:

1. Upload the **CSV** (or **JSON**) file.
2. Upload the **USCIS PDF** file.
3. Click **Fill PDF** and download the **DRAFT** PDF.

Field names in your PDF must match the mapping file. For I-485, edit:

`src/uscis_fill/mappings/profile_to_i485.yaml`

Point each intake field (`first_name`, `last_name`, …) at the exact **AcroForm** name from your PDF edition. If names do not match, fields stay empty and the app lists them after filling.

## Command line (optional)

```bash
uscis-fill --tally path/to/tally.csv --template path/to/uscis-form.pdf --out path/to/DRAFT-out.pdf
```

`--tally` accepts `.csv` or `.json`. The deprecated `--json` flag still works as an alias for a `.json` path.

## Tests

```bash
make test
```

## Privacy

Data stays on your computer. See the [Law Office Constitution](../../../.specify/memory/constitution.md) for professional obligations around client information.
