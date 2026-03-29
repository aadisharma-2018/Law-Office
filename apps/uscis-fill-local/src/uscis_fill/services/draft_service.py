from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

import yaml

from uscis_fill.audit import log_action
from uscis_fill.config import drafts_dir
from uscis_fill.models import DraftUscisOutput
from uscis_fill.pdf_utils import fill_pdf
from uscis_fill.repositories import submissions as submission_repo
from uscis_fill.services import review_service


def _profile_mapping_path(form_code: str) -> Path:
    base = Path(__file__).resolve().parent.parent / "mappings"
    if form_code.upper() == "I-485":
        return base / "profile_to_i485.yaml"
    raise ValueError(f"No mapping for form {form_code}")


def _load_field_map(form_code: str) -> tuple[str, dict[str, str]]:
    path = _profile_mapping_path(form_code)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    fc = data.get("form_code", form_code)
    fm = data.get("field_map") or {}
    return fc, {str(k): str(v) for k, v in fm.items()}


def generate_draft(
    session,
    *,
    submission_id: str,
    template_pdf_path: Path,
    form_code: str,
    actor_user_id: str = "local",
) -> DraftUscisOutput:
    review_service.assert_submission_approved_for_drafts(session, submission_id)
    sub = submission_repo.get_submission(session, submission_id)
    if sub is None or not sub.normalized_profile:
        raise ValueError("Submission missing or has no normalized profile")

    _, field_map = _load_field_map(form_code)
    profile: dict[str, Any] = dict(sub.normalized_profile)
    pdf_field_values: dict[str, str | None] = {}
    for prof_key, pdf_name in field_map.items():
        val = profile.get(prof_key)
        if val is None or val == "":
            pdf_field_values[pdf_name] = None
        else:
            pdf_field_values[pdf_name] = str(val)

    matter_id = sub.matter_id
    out_name = f"DRAFT_{matter_id[:8]}_{form_code}_{uuid.uuid4().hex[:8]}.pdf"
    out_path = drafts_dir() / out_name

    missing = fill_pdf(template_pdf_path, out_path, pdf_field_values)
    combined_unfilled = sorted(set(missing))

    row = DraftUscisOutput(
        id=str(uuid.uuid4()),
        matter_id=matter_id,
        submission_id=submission_id,
        form_code=form_code,
        form_version="placeholder",
        storage_key=str(out_path),
        unfilled_fields=combined_unfilled,
        generated_by_user_id=actor_user_id,
    )
    session.add(row)
    session.flush()
    log_action(
        session,
        actor_user_id=actor_user_id,
        action="draft.generate",
        matter_id=matter_id,
        metadata={
            "submission_id": submission_id,
            "form_code": form_code,
            "unfilled_count": len(combined_unfilled),
        },
    )
    return row
