from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from uscis_fill.config import database_url
from uscis_fill.models import Base

_engine = None
_session_factory = None
_last_db_url: str | None = None


def get_engine(echo: bool = False):
    global _engine, _session_factory, _last_db_url
    url = database_url()
    if _engine is None or _last_db_url != url:
        if _engine is not None:
            _engine.dispose()
        _last_db_url = url
        _engine = create_engine(url, echo=echo, future=True)
        _session_factory = None
    return _engine


def init_db(echo: bool = False) -> None:
    engine = get_engine(echo=echo)
    Base.metadata.create_all(engine)


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(bind=get_engine(), expire_on_commit=False, future=True)
    session = _session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Session:
    """Return a new session; caller must close."""
    if _session_factory is None:
        init_db()
    factory = sessionmaker(bind=get_engine(), expire_on_commit=False, future=True)
    return factory()


def reset_engine() -> None:
    """Test helper: dispose cached engine (e.g. after env change)."""
    global _engine, _session_factory, _last_db_url
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _session_factory = None
    _last_db_url = None
