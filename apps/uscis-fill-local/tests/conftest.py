from __future__ import annotations

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture
def temp_data_dir() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def temp_sqlite_url(temp_data_dir: Path) -> str:
    return f"sqlite:///{temp_data_dir / 'test.db'}"


@pytest.fixture
def isolated_db(temp_data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Point DB at a temp SQLite file and reset engine."""
    from uscis_fill.db import init_db, reset_engine

    db_path = temp_data_dir / "test.sqlite3"
    url = f"sqlite:///{db_path}"
    monkeypatch.setenv("USCIS_FILL_DATABASE_URL", url)
    monkeypatch.setenv("USCIS_FILL_DATA_DIR", str(temp_data_dir))
    reset_engine()
    init_db()
    yield
    reset_engine()
