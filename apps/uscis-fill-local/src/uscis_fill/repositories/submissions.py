from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from uscis_fill.models import Submission


def get_by_tally_response_id(session: Session, tally_response_id: str) -> Submission | None:
    return session.scalar(
        select(Submission).where(Submission.tally_response_id == tally_response_id)
    )


def create_submission(
    session: Session,
    *,
    matter_id: str,
    questionnaire_definition_id: str | None,
    invitation_id: str | None,
    tally_response_id: str | None,
    raw_payload: dict | list | None,
    normalized_profile: dict | None,
    mapping_errors: list | None,
) -> Submission:
    sub = Submission(
        matter_id=matter_id,
        questionnaire_definition_id=questionnaire_definition_id,
        invitation_id=invitation_id,
        tally_response_id=tally_response_id,
        raw_payload=raw_payload,
        normalized_profile=normalized_profile,
        mapping_errors=mapping_errors,
    )
    session.add(sub)
    session.flush()
    return sub


def list_for_matter(session: Session, matter_id: str) -> list[Submission]:
    return list(session.scalars(select(Submission).where(Submission.matter_id == matter_id)))


def get_submission(session: Session, submission_id: str) -> Submission | None:
    return session.get(Submission, submission_id)
