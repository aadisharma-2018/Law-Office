# uscis-fill — run from this directory: apps/uscis-fill-local

.PHONY: venv install test ui cli lint

# Editable installs do not always put src/ on sys.path; Streamlit must resolve `uscis_fill`.
export PYTHONPATH := $(abspath src)

# Create virtualenv (delete .venv first if you want a clean env: rm -rf .venv)
venv:
	python3 -m venv .venv

install: venv
	. .venv/bin/activate && pip install -e ".[dev]"

test:
	.venv/bin/python -m pytest -q

# Two-file UI: Tally CSV/JSON + USCIS PDF → download filled draft
ui:
	.venv/bin/python -m streamlit run src/uscis_fill/ui/app.py

cli:
	.venv/bin/python -m uscis_fill.cli --help

lint:
	.venv/bin/ruff check src tests
