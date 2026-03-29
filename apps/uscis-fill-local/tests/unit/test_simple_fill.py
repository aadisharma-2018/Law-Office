from pathlib import Path

from pypdf import PdfWriter

from uscis_fill.simple_fill import fill_tally_export_into_pdf, fill_tally_json_into_pdf


def _blank_pdf(path: Path) -> None:
    w = PdfWriter()
    w.add_blank_page(width=612, height=792)
    with path.open("wb") as f:
        w.write(f)


def test_fill_tally_json_into_pdf_smoke(tmp_path):
    json_path = Path(__file__).resolve().parents[1] / "fixtures" / "tally_export_sample.json"
    tpl = tmp_path / "t.pdf"
    _blank_pdf(tpl)
    out, unfilled, profile = fill_tally_json_into_pdf(
        tally_json=json_path,
        template_pdf=tpl,
        form_code="I-485",
    )
    assert isinstance(out, bytes)
    assert len(out) > 0
    assert profile.get("last_name") == "Doe"
    # Blank PDF has no AcroForm fields — mapping targets will be unfilled
    assert len(unfilled) >= 1


def test_fill_tally_export_into_pdf_csv_smoke(tmp_path):
    csv_path = Path(__file__).resolve().parents[1] / "fixtures" / "tally_export_sample.csv"
    tpl = tmp_path / "t.pdf"
    _blank_pdf(tpl)
    out, unfilled, profile = fill_tally_export_into_pdf(
        tally_export=csv_path,
        template_pdf=tpl,
        form_code="I-485",
    )
    assert isinstance(out, bytes)
    assert len(out) > 0
    assert profile.get("last_name") == "Doe"
    assert len(unfilled) >= 1


def test_fill_tally_export_into_pdf_csv_bytes(tmp_path):
    csv_path = Path(__file__).resolve().parents[1] / "fixtures" / "tally_export_sample.csv"
    tpl = tmp_path / "t.pdf"
    _blank_pdf(tpl)
    out, unfilled, profile = fill_tally_export_into_pdf(
        tally_export=csv_path.read_bytes(),
        tally_filename="export.csv",
        template_pdf=tpl,
        form_code="I-485",
    )
    assert profile.get("last_name") == "Doe"
    assert len(out) > 0
