#!/usr/bin/env python3
"""
Add or update a manual timestamp correction for a chant line.

Usage:
    python3 tools/correct_timestamp.py <sangha_json> <service_id> <chant_id> <line_index> <cue_in>

Example:
    python3 tools/correct_timestamp.py sanghas/sfzc.json morning-service-monday heart-sutra 32 345.0
"""

import argparse
import json
import shutil
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Add or update a manual timestamp correction."
    )
    parser.add_argument("sangha_json", help="Path to sangha JSON file")
    parser.add_argument("service_id", help="Service ID")
    parser.add_argument("chant_id", help="Chant ID")
    parser.add_argument("line_index", type=int, help="Line index to correct")
    parser.add_argument("cue_in", type=float, help="Corrected cueIn time in seconds")
    args = parser.parse_args()

    json_path = Path(args.sangha_json)
    if not json_path.exists():
        print(f"Error: {json_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(json_path) as f:
        data = json.load(f)

    service = next((s for s in data.get("services", []) if s["id"] == args.service_id), None)
    if service is None:
        print(f"Error: service '{args.service_id}' not found", file=sys.stderr)
        sys.exit(1)

    corrections = service.setdefault("timestampCorrections", {})
    chant_corrections = corrections.setdefault(args.chant_id, [])

    existing = next((c for c in chant_corrections if c["lineIndex"] == args.line_index), None)
    if existing is not None:
        existing["cueIn"] = args.cue_in
    else:
        chant_corrections.append({"lineIndex": args.line_index, "cueIn": args.cue_in})

    chant_corrections.sort(key=lambda c: c["lineIndex"])

    bak_path = json_path.with_suffix(json_path.suffix + ".bak")
    shutil.copy2(json_path, bak_path)

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Correction saved: {args.chant_id} lineIndex={args.line_index} cueIn={args.cue_in}")


if __name__ == "__main__":
    main()
