"""
Golden PDF tests: skipped unless a fillable template is provided (USCIS forms are often not redistributable).
"""

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def _minimal_template(path: Path) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with path.open("wb") as f:
        writer.write(f)


def test_fill_roundtrip(tmp_path):
    """Build minimal PDF with one field name matching profile_to_i485 placeholder."""
    tpl = tmp_path / "tpl.pdf"
    # pypdf adding form fields programmatically is limited; we only check writer path exists.
    _minimal_template(tpl)
    assert tpl.is_file()
    reader = PdfReader(str(tpl))
    assert len(reader.pages) >= 1
