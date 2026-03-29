from __future__ import annotations

import streamlit as st

from uscis_fill.simple_fill import fill_tally_export_into_pdf

st.set_page_config(page_title="USCIS draft fill (local)", layout="centered")

FORM_CHOICES = ["I-485"]


def main() -> None:
    st.title("Fill USCIS PDF from Tally")
    st.markdown(
        "Upload your **Tally export (CSV or JSON)** and the **official USCIS fillable PDF**. "
        "The app maps intake answers into the form using built-in field names in "
        "`mappings/profile_to_i485.yaml` — **edit that file** if your PDF uses different AcroForm names."
    )
    st.caption("Output is a **draft** PDF for attorney review — not for filing as-is.")

    tally_up = st.file_uploader(
        "1. Tally export (CSV or JSON from your questionnaire)",
        type=["csv", "json"],
    )
    pdf_up = st.file_uploader("2. USCIS PDF (fillable template)", type=["pdf"])

    form_code = st.selectbox("Form mapping", FORM_CHOICES, help="Only I-485 mapping is bundled; extend YAML for other forms.")

    if st.button("Fill PDF", type="primary", disabled=not (tally_up and pdf_up)):
        try:
            out_bytes, unfilled, profile = fill_tally_export_into_pdf(
                tally_export=tally_up.getvalue(),
                tally_filename=tally_up.name,
                template_pdf=pdf_up.getvalue(),
                form_code=form_code,
            )
        except Exception as e:
            st.error(str(e))
            return

        st.success("Draft PDF generated.")
        with st.expander("Preview normalized profile (from Tally)"):
            st.json(profile)
        if unfilled:
            st.warning(
                "These PDF fields were not filled (missing value in intake, or field name not in your PDF): "
                + ", ".join(unfilled[:50])
                + ("…" if len(unfilled) > 50 else "")
            )
        st.download_button(
            label="Download DRAFT PDF",
            data=out_bytes,
            file_name="DRAFT_uscis_filled.pdf",
            mime="application/pdf",
        )


if __name__ == "__main__":
    main()
