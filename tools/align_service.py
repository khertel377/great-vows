#!/usr/bin/env python3
"""
Align a full service recording to chant text using stable-whisper forced alignment.

Usage:
    python3 tools/align_service.py sanghas/sfzc.json morning-service-monday
    python3 tools/align_service.py sanghas/sfzc.json morning-service-monday --dry-run
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


def normalize(word: str) -> str:
    """Strip punctuation and lowercase for matching."""
    return re.sub(r"[^a-z0-9']", "", word.lower())


def first_word(text: str) -> str:
    """Return the normalized first whitespace-delimited token from a line."""
    tokens = text.split()
    return normalize(tokens[0]) if tokens else ""


def flatten_words(segments) -> list[tuple[str, float]]:
    """Return a flat list of (normalized_word, start_time) in order."""
    words = []
    for seg in segments:
        for w in seg.words:
            key = normalize(w.word)
            if key:
                words.append((key, w.start))
    return words


def build_transcript(chants: list[dict]) -> tuple[str, list[dict]]:
    """
    Concatenate all non-null text lines from the ordered chant list into a
    single transcript string.

    Returns:
        transcript: the full joined string
        index: list of {chant_id, chant_obj, line_index, first_word} for each
               non-null line, in order — used to drive the timestamp matching pass.
    """
    parts = []
    index = []
    for chant in chants:
        for i, line in enumerate(chant.get("lines", [])):
            text = line.get("text")
            if text:
                parts.append(text)
                index.append({
                    "chant_id": chant["id"],
                    "chant_obj": chant,
                    "line_obj": line,
                    "line_index": i,
                    "first_word": first_word(text),
                })
    return " ".join(parts), index


def main():
    parser = argparse.ArgumentParser(
        description="Align a service recording to chant text with stable-whisper."
    )
    parser.add_argument("sangha_json", help="Path to sangha JSON file")
    parser.add_argument("service_id", help="Service ID to align")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without running the model or writing files",
    )
    args = parser.parse_args()

    json_path = Path(args.sangha_json)
    if not json_path.exists():
        print(f"Error: {json_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(json_path) as f:
        data = json.load(f)

    # Find the service
    service = next(
        (s for s in data.get("services", []) if s["id"] == args.service_id),
        None,
    )
    if service is None:
        print(f"Error: service '{args.service_id}' not found in {json_path}", file=sys.stderr)
        available = [s["id"] for s in data.get("services", [])]
        if available:
            print(f"Available services: {', '.join(available)}", file=sys.stderr)
        sys.exit(1)

    if not service.get("audio"):
        print(f"Error: service '{args.service_id}' has no audio field", file=sys.stderr)
        sys.exit(1)

    # Build chant lookup and ordered chant list
    chant_lookup = {c["id"]: c for c in data.get("chants", [])}
    if service.get("recordingChants"):
        chant_ids = service["recordingChants"]
    else:
        chant_ids = [item["id"] for item in service.get("items", []) if item.get("type") == "chant"]

    ordered_chants = []
    for cid in chant_ids:
        if cid not in chant_lookup:
            print(f"Warning: chant '{cid}' referenced in service but not found in data.chants", file=sys.stderr)
            continue
        ordered_chants.append(chant_lookup[cid])

    if not ordered_chants:
        print("No chants found in service items.", file=sys.stderr)
        sys.exit(1)

    transcript, line_index = build_transcript(ordered_chants)

    if not line_index:
        print("No non-null text lines found across service chants.", file=sys.stderr)
        sys.exit(1)

    print(f"Service: {service['id']}")
    print(f"Audio:   {service['audio']}")
    print(f"Chants:  {len(ordered_chants)}  ({', '.join(c['id'] for c in ordered_chants)})")
    print(f"Lines:   {len(line_index)}")

    if args.dry_run:
        print("\n[dry-run] Transcript excerpts per chant:")
        for chant in ordered_chants:
            lines = [l["text"] for l in chant.get("lines", []) if l.get("text")]
            excerpt = " ".join(lines)[:60]
            ellipsis = "…" if len(" ".join(lines)) > 60 else ""
            print(f"  {chant['id']}: {excerpt}{ellipsis}")
        print("\n[dry-run] Would skip model loading, alignment, and file writing.")
        sys.exit(0)

    import stable_whisper
    print("\nLoading stable-whisper model (base, cpu)…")
    model = stable_whisper.load_model("base", device="cpu")

    print("Aligning…")
    result = model.align(service["audio"], transcript, language="en")
    words = flatten_words(result.segments)

    # Match each line's first word forward through the word list
    pointer = 0
    # Track per-chant data for timestampMap assembly
    chant_data: dict[str, dict] = {}  # chant_id -> {startTime, lines: [{lineIndex, cueIn}]}

    for entry in line_index:
        key = entry["first_word"]
        if not key:
            continue
        for i in range(pointer, len(words)):
            if words[i][0] == key:
                t = round(words[i][1], 2)
                cid = entry["chant_id"]
                if cid not in chant_data:
                    chant_data[cid] = {"startTime": t, "lines": []}
                chant_data[cid]["lines"].append({"lineIndex": entry["line_index"], "cueIn": t})
                pointer = i + 1
                break

    # Build timestampMap in chant order
    timestamp_map = []
    for chant in ordered_chants:
        cid = chant["id"]
        if cid in chant_data:
            entry = chant_data[cid]
            timestamp_map.append({
                "chantId": cid,
                "startTime": entry["startTime"],
                "lines": entry["lines"],
            })

    service["timestampMap"] = timestamp_map

    # Back up and write
    bak_path = json_path.with_suffix(json_path.suffix + ".bak")
    shutil.copy2(json_path, bak_path)
    print(f"\nBacked up original to {bak_path}")

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote updated JSON to {json_path}")

    total_lines = sum(len(e["lines"]) for e in timestamp_map)
    print(f"\nSummary: {args.service_id} — {len(timestamp_map)} chant(s) processed, {total_lines} line(s) timestamped.")


if __name__ == "__main__":
    main()
