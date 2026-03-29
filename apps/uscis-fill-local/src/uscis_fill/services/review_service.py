from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from uscis_fill.audit import log_action
from uscis_fill.models import ReviewDecision, ReviewStatus
from uscis_fill.repositories import submissions as submission_repo


def latest_decision(session: Session, submission_id: str) -> ReviewDecision | None:
    q = (
        select(ReviewDecision)
        .where(ReviewDecision.submission_id == submission_id)
        .order_by(ReviewDecision.decided_at.desc())
        .limit(1)
    )
    return session.scalar(q)


def set_review_decision(
    session: Session,
    *,
    submission_id: str,
    reviewer_user_id: str,
    status: str,
    notes: str | None = None,
) -> ReviewDecision:
    if status not in (
        ReviewStatus.approved.value,
        ReviewStatus.needs_follow_up.value,
        ReviewStatus.pending.value,
    ):
        raise ValueError(f"Invalid review status: {status}")
    sub = submission_repo.get_submission(session, submission_id)
    if sub is None:
        raise ValueError("Unknown submission")

    row = ReviewDecision(
        id=str(uuid.uuid4()),
        submission_id=submission_id,
        reviewer_user_id=reviewer_user_id,
        status=status,
        notes=notes,
        decided_at=datetime.now(timezone.utc),
    )
    session.add(row)
    session.flush()
    log_action(
        session,
        actor_user_id=reviewer_user_id,
        action="review.update",
        matter_id=sub.matter_id,
        metadata={"submission_id": submission_id, "status": status},
    )
    return row


def assert_submission_approved_for_drafts(session: Session, submission_id: str) -> None:
    d = latest_decision(session, submission_id)
    if d is None or d.status != ReviewStatus.approved.value:
        raise PermissionError(
            "Submission is not approved for draft generation (default policy: block until approved)."
        )


def is_approved(session: Session, submission_id: str) -> bool:
    d = latest_decision(session, submission_id)
    return d is not None and d.status == ReviewStatus.approved.value
