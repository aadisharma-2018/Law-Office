from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _mapping_path() -> Path:
    return Path(__file__).resolve().parent / "mappings" / "tally_to_profile.yaml"


def _load_mapping_yaml() -> dict[str, Any]:
    with _mapping_path().open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalize_to_profile(parsed: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """
    Apply tally_to_profile.yaml to map export fields → structured case profile.
    Returns (profile dict, warnings).
    """
    data = _load_mapping_yaml()
    mappings = data.get("mappings") or []
    warnings: list[str] = []
    profile: dict[str, Any] = {}
    fields = parsed.get("fields") or {}

    for m in mappings:
        src = m.get("source")
        tgt = m.get("target")
        if not src or not tgt:
            continue
        if src in fields:
            profile[tgt] = fields[src]
        else:
            warnings.append(f"missing_source:{src}")

    return profile, warnings
