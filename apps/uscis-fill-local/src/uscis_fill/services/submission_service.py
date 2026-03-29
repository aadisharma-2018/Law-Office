from __future__ import annotations

from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from uscis_fill.audit import log_action
from uscis_fill.models import QuestionnaireDefinition, Submission
from uscis_fill.normalize import normalize_to_profile
from uscis_fill.repositories import clients_matters, submissions as submission_repo
from uscis_fill.tally_import import parse_tally_file, parsed_raw_payload


def _ensure_default_questionnaire(session: Session) -> QuestionnaireDefinition:
    row = session.scalar(select(QuestionnaireDefinition).limit(1))
    if row:
        return row
    q = QuestionnaireDefinition(tally_form_id="default", title="Default intake", version=1)
    session.add(q)
    session.flush()
    return q


def import_submission_file(
    session: Session,
    *,
    matter_id: str,
    path: Path,
    actor_user_id: str = "local",
) -> Submission:
    """
    Import a Tally export (CSV or JSON) into a Submission. FR-003: fail closed if matter binding conflicts.
    """
    matter = clients_matters.get_matter(session, matter_id)
    if matter is None:
        raise ValueError(f"Unknown matter_id: {matter_id}")

    parsed = parse_tally_file(path)
    mid = parsed.get("matter_id_from_export")
    if mid is not None and str(mid) != str(matter_id):
        raise ValueError(
            "Export matter id does not match selected matter (FR-003); refusing import."
        )

    tally_response_id = parsed.get("response_id")
    if tally_response_id:
        existing = submission_repo.get_by_tally_response_id(session, str(tally_response_id))
        if existing:
            raise ValueError(f"Duplicate submission for response id: {tally_response_id}")

    profile, warnings = normalize_to_profile(parsed)
    mapping_errors = [w for w in warnings if w.startswith("missing_source:")]

    qdef = _ensure_default_questionnaire(session)

    sub = submission_repo.create_submission(
        session,
        matter_id=matter_id,
        questionnaire_definition_id=qdef.id,
        invitation_id=None,
        tally_response_id=str(tally_response_id) if tally_response_id else None,
        raw_payload=parsed_raw_payload(parsed),
        normalized_profile=profile,
        mapping_errors=mapping_errors or None,
    )
    log_action(
        session,
        actor_user_id=actor_user_id,
        action="submission.import",
        matter_id=matter_id,
        metadata={"submission_id": sub.id, "response_id": tally_response_id},
    )
    return sub
