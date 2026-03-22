#!/usr/bin/env python3
"""
Merge clip-relative cueIn timestamps into a service timestampMap with absolute offsets.

Usage:
    python3 tools/merge_clip_alignment.py <sangha_json> <service_id> <chant_id> <clip_start>

Example:
    python3 tools/merge_clip_alignment.py sanghas/sfzc.json morning-service-monday names-buddhas-ancestors-monday 623
    python3 tools/merge_clip_alignment.py sanghas/sfzc.json morning-service-monday names-women-ancestors 798
"""

import argparse
import json
import shutil
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Merge clip-relative cueIn timestamps into a service timestampMap."
    )
    parser.add_argument("sangha_json", help="Path to sangha JSON file")
    parser.add_argument("service_id", help="Service ID")
    parser.add_argument("chant_id", help="Chant ID to merge")
    parser.add_argument("clip_start", type=float, help="Clip start time in seconds (absolute offset)")
    args = parser.parse_args()

    json_path = Path(args.sangha_json)
    if not json_path.exists():
        print(f"Error: {json_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(json_path) as f:
        data = json.load(f)

    # Find service
    service = next((s for s in data.get("services", []) if s["id"] == args.service_id), None)
    if service is None:
        print(f"Error: service '{args.service_id}' not found", file=sys.stderr)
        sys.exit(1)

    # Find chant
    chant = next((c for c in data.get("chants", []) if c["id"] == args.chant_id), None)
    if chant is None:
        print(f"Error: chant '{args.chant_id}' not found", file=sys.stderr)
        sys.exit(1)

    # Build absolute-offset lines from chant cueIn values
    abs_lines = []
    for i, line in enumerate(chant.get("lines", [])):
        if line.get("text") is None:
            continue
        if "cueIn" not in line:
            continue
        abs_cue = round(line["cueIn"] + args.clip_start, 2)
        abs_lines.append({"lineIndex": i, "cueIn": abs_cue})

    if not abs_lines:
        print(f"Error: no cueIn values found on chant '{args.chant_id}'", file=sys.stderr)
        sys.exit(1)

    start_time = abs_lines[0]["cueIn"]

    # Find or create timestampMap entry
    timestamp_map = service.setdefault("timestampMap", [])
    entry = next((e for e in timestamp_map if e["chantId"] == args.chant_id), None)
    if entry is not None:
        entry["startTime"] = start_time
        entry["lines"] = abs_lines
    else:
        timestamp_map.append({
            "chantId": args.chant_id,
            "startTime": start_time,
            "lines": abs_lines,
        })

    # Back up and write
    bak_path = json_path.with_suffix(json_path.suffix + ".bak")
    shutil.copy2(json_path, bak_path)
    print(f"Backed up original to {bak_path}")

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote updated JSON to {json_path}")

    print(f"\nSummary: {args.chant_id} | offset +{args.clip_start}s | {len(abs_lines)} lines updated | startTime={start_time}")


if __name__ == "__main__":
    main()
