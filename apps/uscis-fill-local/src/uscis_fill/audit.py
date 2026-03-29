from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.orm import Session

from uscis_fill.models import AuditLog


def log_action(
    session: Session,
    *,
    actor_user_id: str,
    action: str,
    matter_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> AuditLog:
    """Append-only audit row (FR-008). Keep metadata minimal—avoid raw PII (T031)."""
    safe_meta = metadata or {}
    row = AuditLog(
        id=str(uuid.uuid4()),
        actor_user_id=actor_user_id,
        action=action,
        matter_id=matter_id,
        metadata_=safe_meta,
    )
    session.add(row)
    return row
