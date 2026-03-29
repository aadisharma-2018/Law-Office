from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from uscis_fill.models import Client, Matter


def create_client(session: Session, *, display_name: str | None = None) -> Client:
    c = Client(display_name=display_name)
    session.add(c)
    session.flush()
    return c


def get_client(session: Session, client_id: str) -> Client | None:
    return session.get(Client, client_id)


def create_matter(
    session: Session,
    *,
    client_id: str,
    reference: str | None = None,
) -> Matter:
    m = Matter(client_id=client_id, reference=reference)
    session.add(m)
    session.flush()
    return m


def get_matter(session: Session, matter_id: str) -> Matter | None:
    return session.get(Matter, matter_id)


def list_matters_for_client(session: Session, client_id: str) -> list[Matter]:
    return list(session.scalars(select(Matter).where(Matter.client_id == client_id)))
