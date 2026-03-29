from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def _uuid() -> str:
    return str(uuid.uuid4())


class MatterStatus(str, enum.Enum):
    open = "open"
    closed = "closed"


class InvitationStatus(str, enum.Enum):
    sent = "sent"
    superseded = "superseded"
    revoked = "revoked"


class ReviewStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    needs_follow_up = "needs_follow_up"


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    display_name: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    matters: Mapped[list[Matter]] = relationship(back_populates="client")


class Matter(Base):
    __tablename__ = "matters"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    client_id: Mapped[str] = mapped_column(String(36), ForeignKey("clients.id"), nullable=False)
    reference: Mapped[str | None] = mapped_column(String(256), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default=MatterStatus.open.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    client: Mapped[Client] = relationship(back_populates="matters")


class QuestionnaireDefinition(Base):
    __tablename__ = "questionnaire_definitions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    tally_form_id: Mapped[str] = mapped_column(String(128), nullable=False)
    version: Mapped[int] = mapped_column(default=1)
    title: Mapped[str] = mapped_column(String(512), default="Intake")
    mapping_version: Mapped[str] = mapped_column(String(64), default="1")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class QuestionnaireInvitation(Base):
    __tablename__ = "questionnaire_invitations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    matter_id: Mapped[str] = mapped_column(String(36), ForeignKey("matters.id"), nullable=False)
    questionnaire_definition_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("questionnaire_definitions.id"), nullable=False
    )
    token: Mapped[str | None] = mapped_column(String(256), nullable=True)
    recipient_email: Mapped[str | None] = mapped_column(String(512), nullable=True)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default=InvitationStatus.sent.value)


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    matter_id: Mapped[str] = mapped_column(String(36), ForeignKey("matters.id"), nullable=False)
    questionnaire_definition_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("questionnaire_definitions.id"), nullable=True
    )
    invitation_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("questionnaire_invitations.id"), nullable=True
    )
    tally_response_id: Mapped[str | None] = mapped_column(String(256), nullable=True, unique=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    raw_payload: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    normalized_profile: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    mapping_errors: Mapped[list | None] = mapped_column(JSON, nullable=True)


class ReviewDecision(Base):
    __tablename__ = "review_decisions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    submission_id: Mapped[str] = mapped_column(String(36), ForeignKey("submissions.id"), nullable=False)
    reviewer_user_id: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DraftUscisOutput(Base):
    __tablename__ = "draft_uscis_outputs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    matter_id: Mapped[str] = mapped_column(String(36), ForeignKey("matters.id"), nullable=False)
    submission_id: Mapped[str] = mapped_column(String(36), ForeignKey("submissions.id"), nullable=False)
    form_code: Mapped[str] = mapped_column(String(32), nullable=False)
    form_version: Mapped[str] = mapped_column(String(64), default="unknown")
    storage_key: Mapped[str] = mapped_column(String(1024), nullable=False)
    unfilled_fields: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    generated_by_user_id: Mapped[str] = mapped_column(String(256), default="local")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    actor_user_id: Mapped[str] = mapped_column(String(256), nullable=False)
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    matter_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
