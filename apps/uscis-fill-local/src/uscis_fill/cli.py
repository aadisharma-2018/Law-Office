from __future__ import annotations

import argparse
from pathlib import Path

from uscis_fill.simple_fill import fill_tally_export_into_pdf


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="uscis-fill",
        description="Fill a USCIS PDF from a Tally export (.csv or .json; local, no database).",
    )
    parser.add_argument(
        "--tally",
        type=Path,
        help="Path to Tally export (.csv or .json)",
    )
    parser.add_argument(
        "--json",
        type=Path,
        dest="json_legacy",
        help="Deprecated: same as --tally (for .json paths)",
    )
    parser.add_argument("--template", type=Path, required=True, help="Path to USCIS fillable .pdf")
    parser.add_argument("--out", type=Path, required=True, help="Output path for filled PDF")
    parser.add_argument(
        "--form",
        type=str,
        default="I-485",
        help="Form mapping to use (default: I-485)",
    )
    args = parser.parse_args()

    tally_path = args.tally or args.json_legacy
    if tally_path is None:
        raise SystemExit("Provide --tally path/to/export.csv (or .json). Use --json only as a deprecated alias.")

    if not tally_path.is_file():
        raise SystemExit(f"Not found: {tally_path}")
    if not args.template.is_file():
        raise SystemExit(f"Not found: {args.template}")

    out_bytes, unfilled, _profile = fill_tally_export_into_pdf(
        tally_export=tally_path,
        template_pdf=args.template,
        form_code=args.form.strip(),
    )
    args.out.write_bytes(out_bytes)
    print(f"Wrote: {args.out.resolve()}")
    if unfilled:
        print(f"Unfilled PDF fields ({len(unfilled)}):", ", ".join(unfilled[:20]))
        if len(unfilled) > 20:
            print("...")


if __name__ == "__main__":
    main()
