from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

import yaml

from uscis_fill.normalize import normalize_to_profile
from uscis_fill.pdf_utils import fill_pdf
from uscis_fill.tally_import import parse_tally_bytes, parse_tally_file


def _mapping_path(form_code: str) -> Path:
    base = Path(__file__).resolve().parent / "mappings"
    code = form_code.upper().replace("-", "")
    if code == "I485":
        return base / "profile_to_i485.yaml"
    raise ValueError(
        f"No built-in mapping for form {form_code!r}. Use I-485 (or edit mappings/profile_to_i485.yaml)."
    )


def load_profile_to_pdf_field_map(form_code: str) -> dict[str, str]:
    """Map canonical profile keys → PDF AcroForm field names."""
    path = _mapping_path(form_code)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    fm = data.get("field_map") or {}
    return {str(k): str(v) for k, v in fm.items()}


def fill_tally_export_into_pdf(
    *,
    tally_export: bytes | Path,
    template_pdf: bytes | Path,
    form_code: str = "I-485",
    tally_filename: str | None = None,
) -> tuple[bytes, list[str], dict[str, Any]]:
    """
    Parse a Tally export (``.csv`` or ``.json``), normalize to profile, fill the USCIS PDF template.

    For ``bytes`` input, set ``tally_filename`` to the original name (e.g. ``responses.csv``) so the
    format is detected from the extension. Defaults to ``export.csv``.

    Returns ``(filled_pdf_bytes, unfilled_pdf_field_names, normalized_profile)``.
    """
    cleanup: list[Path] = []

    def _path(data: bytes | Path, suffix: str) -> Path:
        if isinstance(data, Path):
            return data
        t = Path(tempfile.mkstemp(suffix=suffix)[1])
        t.write_bytes(data)
        cleanup.append(t)
        return t

    if isinstance(tally_export, Path):
        parsed = parse_tally_file(tally_export)
    else:
        name = tally_filename or "export.csv"
        parsed = parse_tally_bytes(tally_export, name)

    ppath = _path(template_pdf, ".pdf")
    fd, out_name = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    out_path = Path(out_name)
    cleanup.append(out_path)

    try:
        profile, _warnings = normalize_to_profile(parsed)
        field_map = load_profile_to_pdf_field_map(form_code)
        pdf_field_values: dict[str, str | None] = {}
        for prof_key, pdf_name in field_map.items():
            val = profile.get(prof_key)
            pdf_field_values[pdf_name] = None if val in (None, "") else str(val)

        unfilled = fill_pdf(ppath, out_path, pdf_field_values)
        pdf_bytes = out_path.read_bytes()
        return pdf_bytes, sorted(set(unfilled)), profile
    finally:
        for p in cleanup:
            p.unlink(missing_ok=True)


def fill_tally_json_into_pdf(
    *,
    tally_json: bytes | Path,
    template_pdf: bytes | Path,
    form_code: str = "I-485",
) -> tuple[bytes, list[str], dict[str, Any]]:
    """Backward-compatible alias: treats bytes as JSON (``export.json``)."""
    if isinstance(tally_json, Path):
        return fill_tally_export_into_pdf(
            tally_export=tally_json,
            template_pdf=template_pdf,
            form_code=form_code,
        )
    return fill_tally_export_into_pdf(
        tally_export=tally_json,
        template_pdf=template_pdf,
        form_code=form_code,
        tally_filename="export.json",
    )
