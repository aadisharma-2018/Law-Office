from pathlib import Path

from uscis_fill.normalize import normalize_to_profile
from uscis_fill.tally_import import parse_tally_file


def test_normalize_maps_fields_from_json():
    path = Path(__file__).resolve().parents[1] / "fixtures" / "tally_export_sample.json"
    parsed = parse_tally_file(path)
    profile, warnings = normalize_to_profile(parsed)
    assert profile.get("last_name") == "Doe"
    assert profile.get("first_name") == "Jane"
    assert "dob" in profile


def test_normalize_maps_fields_from_csv():
    path = Path(__file__).resolve().parents[1] / "fixtures" / "tally_export_sample.csv"
    parsed = parse_tally_file(path)
    profile, warnings = normalize_to_profile(parsed)
    assert profile.get("last_name") == "Doe"
    assert profile.get("first_name") == "Jane"
    assert "dob" in profile


def test_normalize_family_name_last_name_header():
    """Tally-style label 'Family Name (Last Name)' → key family_name_last_name → last_name."""
    from uscis_fill.tally_import import parse_tally_csv_text

    text = 'Family Name (Last Name),First Name\nSmith,Pat\n'
    parsed = parse_tally_csv_text(text)
    profile, _ = normalize_to_profile(parsed)
    assert profile.get("last_name") == "Smith"
    assert profile.get("first_name") == "Pat"


def test_normalize_csv_first_name_last_name_columns():
    """Plain 'First Name' / 'Last name' columns (see documents/tally.csv style)."""
    from uscis_fill.tally_import import parse_tally_csv_text

    text = 'First Name,Last name\nJohn,Doe\n'
    parsed = parse_tally_csv_text(text)
    profile, _ = normalize_to_profile(parsed)
    assert profile.get("first_name") == "John"
    assert profile.get("last_name") == "Doe"
