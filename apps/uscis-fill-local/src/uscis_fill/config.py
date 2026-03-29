from __future__ import annotations

import os
import sys
from pathlib import Path


def get_data_dir() -> Path:
    """Resolve firm-configurable data directory (SQLite, drafts, exports)."""
    env = os.environ.get("USCIS_FILL_DATA_DIR")
    if env:
        return Path(env).expanduser().resolve()
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA", str(Path.home()))
        return Path(base) / "uscis-fill"
    return Path.home() / ".local" / "share" / "uscis-fill"


def ensure_data_dir() -> Path:
    d = get_data_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / "drafts").mkdir(exist_ok=True)
    return d


def database_url() -> str:
    override = os.environ.get("USCIS_FILL_DATABASE_URL")
    if override:
        return override
    return f"sqlite:///{ensure_data_dir() / 'app.sqlite3'}"


def drafts_dir() -> Path:
    return ensure_data_dir() / "drafts"
