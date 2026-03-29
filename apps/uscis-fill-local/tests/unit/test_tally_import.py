from pathlib import Path

import pytest

from uscis_fill.tally_import import parse_tally_csv, parse_tally_export, parse_tally_file


def test_parse_tally_export_sample_json():
    path = Path(__file__).resolve().parents[1] / "fixtures" / "tally_export_sample.json"
    p = parse_tally_export(path)
    assert p["response_id"] == "tally_resp_sample_001"
    assert p["fields"]["family_name"] == "Doe"
    assert "raw_document" in p


def test_parse_tally_csv_sample():
    path = Path(__file__).resolve().parents[1] / "fixtures" / "tally_export_sample.csv"
    p = parse_tally_csv(path)
    assert p["response_id"] == "tally_resp_sample_001"
    assert p["fields"]["family_name"] == "Doe"
    assert p["fields"]["given_name"] == "Jane"
    assert p["raw_document"]["format"] == "csv"


def test_parse_tally_file_dispatches_by_suffix():
    base = Path(__file__).resolve().parents[1] / "fixtures"
    j = parse_tally_file(base / "tally_export_sample.json")
    c = parse_tally_file(base / "tally_export_sample.csv")
    assert j["fields"]["family_name"] == c["fields"]["family_name"]


def test_parse_tally_csv_last_row_wins():
    from uscis_fill.tally_import import parse_tally_csv_text

    text = "a,b\n1,first\n2,second\n"
    p = parse_tally_csv_text(text)
    assert p["fields"]["a"] == "2"
    assert p["fields"]["b"] == "second"


def test_parse_tally_csv_empty_raises():
    from uscis_fill.tally_import import parse_tally_csv_text

    with pytest.raises(ValueError, match="no data rows"):
        parse_tally_csv_text("h1,h2\n")
