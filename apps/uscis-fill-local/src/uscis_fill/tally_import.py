from __future__ import annotations

import csv
import json
import re
from io import StringIO
from pathlib import Path
from typing import Any


def _header_to_field_key(header: str) -> str:
    """Turn a CSV column header into a snake_case key (e.g. 'Given name' -> 'given_name')."""
    h = header.strip()
    if not h:
        return ""
    h = h.lower()
    h = re.sub(r"[^\w\s]", "", h)
    h = re.sub(r"\s+", "_", h.strip())
    return h


def parse_tally_csv_text(text: str) -> dict[str, Any]:
    """
    Parse Tally **CSV** text (wide format: one row per response, headers in row 1).

    Uses the **last** non-empty data row when multiple rows are present.
    """
    reader = csv.DictReader(StringIO(text))
    fieldnames = list(reader.fieldnames or [])
    rows = [row for row in reader if any((v or "").strip() for v in row.values())]
    if not rows:
        raise ValueError("CSV has no data rows.")

    row = rows[-1]

    flat_fields: dict[str, Any] = {}
    hidden: dict[str, Any] = {}
    response_id: str | None = None

    id_headers_lower = {
        "submissionid",
        "submission_id",
        "responseid",
        "response_id",
        "id",
    }

    for raw_header, value in row.items():
        if raw_header is None:
            continue
        key = _header_to_field_key(raw_header)
        if not key:
            continue
        v = (value or "").strip()
        lk = raw_header.strip().lower().replace(" ", "").replace("_", "")

        if lk in id_headers_lower or key in ("submission_id", "response_id", "id"):
            if v and response_id is None:
                response_id = v
            continue

        if key in ("matterid", "matter_id", "invitationid", "invitation_id"):
            hidden[key] = v
            continue

        flat_fields[key] = v if v else None

    matter_from_export = hidden.get("matter_id") or hidden.get("matterid")
    invitation_from_export = hidden.get("invitation_id") or hidden.get("invitationid")

    raw_document = {"format": "csv", "row_count": len(rows), "headers": fieldnames}

    return {
        "response_id": response_id,
        "form_id": None,
        "fields": flat_fields,
        "hidden": hidden,
        "matter_id_from_export": matter_from_export,
        "invitation_id_from_export": invitation_from_export,
        "raw_document": raw_document,
    }


def parse_tally_csv(path: Path) -> dict[str, Any]:
    """Parse a Tally CSV file (UTF-8 with optional BOM)."""
    return parse_tally_csv_text(path.read_text(encoding="utf-8-sig"))


def _parse_tally_export_dict(raw: dict[str, Any]) -> dict[str, Any]:
    response_id = raw.get("responseId") or raw.get("response_id")
    hidden = raw.get("hidden") or {}
    if not isinstance(hidden, dict):
        hidden = {}

    fields_raw = raw.get("fields")
    flat_fields: dict[str, Any] = {}
    if isinstance(fields_raw, dict):
        flat_fields = dict(fields_raw)
    elif isinstance(fields_raw, list):
        for item in fields_raw:
            if isinstance(item, dict):
                k = item.get("key") or item.get("id") or item.get("label")
                v = item.get("value")
                if k is not None:
                    flat_fields[str(k)] = v

    matter_from_export = (
        hidden.get("matterId")
        or hidden.get("matter_id")
        or raw.get("matterId")
        or raw.get("matter_id")
    )
    invitation_from_export = hidden.get("invitationId") or hidden.get("invitation_id")

    return {
        "response_id": response_id,
        "form_id": raw.get("formId") or raw.get("form_id"),
        "fields": flat_fields,
        "hidden": hidden,
        "matter_id_from_export": matter_from_export,
        "invitation_id_from_export": invitation_from_export,
        "raw_document": raw,
    }


def parse_tally_export(path: Path) -> dict[str, Any]:
    """Parse a Tally **JSON** export file."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    return _parse_tally_export_dict(raw)


def parse_tally_file(path: Path) -> dict[str, Any]:
    """Parse a Tally export file by extension: ``.csv`` or ``.json``."""
    suf = path.suffix.lower()
    if suf == ".csv":
        return parse_tally_csv(path)
    if suf == ".json":
        return parse_tally_export(path)
    raise ValueError(f"Unsupported Tally export type {suf!r}; use .csv or .json.")


def parse_tally_bytes(data: bytes, filename: str) -> dict[str, Any]:
    """Parse an upload: ``filename`` must end with ``.csv`` or ``.json``."""
    suf = Path(filename).suffix.lower()
    text = data.decode("utf-8-sig")
    if suf == ".csv":
        return parse_tally_csv_text(text)
    if suf == ".json":
        raw = json.loads(text)
        if not isinstance(raw, dict):
            raise ValueError("Tally JSON export must be an object at the top level.")
        return _parse_tally_export_dict(raw)
    raise ValueError(f"Unsupported Tally export type {suf!r}; use .csv or .json.")


def parsed_raw_payload(parsed: dict) -> dict | list:
    """Original export document for immutable audit storage."""
    return parsed.get("raw_document") or parsed
