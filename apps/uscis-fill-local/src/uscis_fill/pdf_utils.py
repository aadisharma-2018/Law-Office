from __future__ import annotations

from pathlib import Path
from typing import Any

from pypdf import PdfReader, PdfWriter


def _field_last_segment(name: str) -> str:
    """Last dot-separated segment (e.g. ``...Pt1Line1a_FamilyName[0]`` → ``Pt1Line1a_FamilyName[0]``)."""
    return name.rpartition(".")[2] if name else name


def resolve_pdf_field_key(wanted: str, existing_names: set[str]) -> str | None:
    """
    Map a field name from our YAML (often a long Acrobat-style path) to a key that
    :meth:`pypdf.PdfReader.get_fields` actually returns. Those keys can differ: some
    PDFs use only the terminal ``/T`` name, or ``/TM``, while docs show full paths.
    """
    if wanted in existing_names:
        return wanted
    leaf = _field_last_segment(wanted)
    if not leaf:
        return None
    if leaf in existing_names:
        return leaf

    same_leaf = [k for k in existing_names if _field_last_segment(k) == leaf]
    if len(same_leaf) == 1:
        return same_leaf[0]
    if len(same_leaf) > 1:
        if wanted in same_leaf:
            return wanted
        return min(same_leaf, key=len)

    # Suffix match (e.g. wanted ends with key or vice versa)
    for k in existing_names:
        if k.endswith(leaf) or leaf.endswith(k):
            return k
    return None


def _reader_for_form(path: Path) -> PdfReader:
    """Decrypt with empty password when needed (typical for fillable USCIS PDFs using AES)."""
    reader = PdfReader(str(path))
    if reader.is_encrypted:
        reader.decrypt("")
    return reader


def _collect_field_identifiers(reader: PdfReader) -> set[str]:
    """
    All name strings that :meth:`~pypdf.PdfWriter.update_page_form_field_values` may match:
    keys from :meth:`~pypdf.PdfReader.get_fields` plus each page widget's qualified name and
    short ``/T``. Encrypted PDFs often return no fields from ``get_fields`` until decrypted.
    """
    names: set[str] = set()
    fields = reader.get_fields()
    if fields:
        names.update(fields.keys())

    for page in reader.pages:
        annots = page.get("/Annots")
        if not annots:
            continue
        for ref in annots:
            try:
                annot = ref.get_object()
            except Exception:
                continue
            if annot.get("/Subtype") != "/Widget":
                continue
            if annot.get("/FT") is not None and annot.get("/T") is not None:
                parent_annotation = annot
            else:
                parent = annot.get("/Parent")
                if parent is None:
                    continue
                parent_annotation = parent.get_object()
            try:
                q = reader._get_qualified_field_name(parent_annotation)
                if q:
                    names.add(q)
            except Exception:
                pass
            t = parent_annotation.get("/T")
            if t is not None:
                names.add(str(t))

    return names


def list_acroform_fields(template_path: Path) -> dict[str, Any]:
    reader = _reader_for_form(template_path)
    fields = reader.get_fields()
    return dict(fields) if fields else {}


def fill_pdf(
    template_path: Path,
    out_path: Path,
    field_values: dict[str, str | None],
) -> list[str]:
    """
    Fill AcroForm fields. Keys are PDF field names. Returns PDF field names that were not
    filled (missing value, or field absent from template).
    """
    reader = _reader_for_form(template_path)
    writer = PdfWriter()
    # Full document clone copies /Catalog /AcroForm; append_pages_from_reader alone omits
    # AcroForm and causes "No /AcroForm dictionary in PDF of PdfWriter Object" on fill.
    writer.clone_document_from_reader(reader)
    existing_names = _collect_field_identifiers(reader)
    unfilled: list[str] = []
    to_apply: dict[str, str] = {}
    for k, v in field_values.items():
        if v is None or v == "":
            unfilled.append(k)
            continue
        resolved = resolve_pdf_field_key(k, existing_names)
        if resolved is None:
            unfilled.append(k)
            continue
        to_apply[resolved] = str(v)

    # pypdf requires an /AcroForm; skip updates if there is nothing to write or no form fields.
    if to_apply:
        for page in writer.pages:
            writer.update_page_form_field_values(page, to_apply)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as f:
        writer.write(f)
    return unfilled
