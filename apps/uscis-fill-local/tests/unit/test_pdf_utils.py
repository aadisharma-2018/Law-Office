from uscis_fill.pdf_utils import resolve_pdf_field_key


def test_resolve_exact():
    s = {"form1[0].#subform[0].Pt1Line1a_FamilyName[0]"}
    assert resolve_pdf_field_key("form1[0].#subform[0].Pt1Line1a_FamilyName[0]", s) == next(
        iter(s)
    )


def test_resolve_short_key_when_yaml_has_full_path():
    """Reader often exposes only the terminal name; YAML may use the full Acrobat path."""
    existing = {"Pt1Line1a_FamilyName[0]", "Pt1Line1a_GivenName[0]"}
    assert (
        resolve_pdf_field_key(
            "form1[0].#subform[0].Pt1Line1a_FamilyName[0]",
            existing,
        )
        == "Pt1Line1a_FamilyName[0]"
    )


def test_resolve_matches_last_segment():
    existing = {"foo.bar.Pt1Line3_DateOfBirth[0]"}
    assert (
        resolve_pdf_field_key(
            "form1[0].#subform[0].Pt1Line3_DateOfBirth[0]",
            existing,
        )
        == "foo.bar.Pt1Line3_DateOfBirth[0]"
    )
