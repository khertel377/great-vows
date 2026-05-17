#!/usr/bin/env python3
"""
Align a full service recording to chant text using stable-whisper forced alignment.

Usage:
    python3 tools/align_service.py sanghas/sfzc.json morning-service-monday
    python3 tools/align_service.py sanghas/sfzc.json morning-service-monday --dry-run
    python3 tools/align_service.py sanghas/sfzc.json evening-service --model small
    python3 tools/align_service.py sanghas/sfzc.json evening-service --model medium --language ja
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from apply_corrections import apply_corrections


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


# ---------------------------------------------------------------------------
# Per-chant post-processing
# ---------------------------------------------------------------------------

# Chant IDs that are phonetically repetitive dharanis or Japanese-script chants
# and benefit from tighter alignment constraints.
DHARANI_CHANT_IDS = {
    "dai-hi-shin-darani",
    "shosaimyo",
    "enmei-jukku",
    "maka-hannya",
    "before-lecture",
    "after-dedication",
}


def smooth_service_chant(chant_id: str, lines: list[dict], chant_duration: float) -> int:
    """
    Post-process cueIn timestamps for a single chant within a service recording.

    `lines` is the list of {lineIndex, cueIn} dicts from the timestampMap entry —
    all entries here have a cueIn (nulls were never added).

    `chant_duration` is the wall-clock span of this chant segment (last cueIn
    minus first cueIn); used to set the outlier ceiling.

    Returns the number of cueIn values that were changed.
    """
    if len(lines) < 2:
        return 0

    original = [l["cueIn"] for l in lines]

    # --- Parameters ---
    # Tighter floor for phonetically repetitive dharanis; looser for normal chants.
    if chant_id in DHARANI_CHANT_IDS:
        min_gap = 2.0          # no two lines closer than 2s
        outlier_ratio = 1.8    # gap > 1.8× median is an outlier
    else:
        min_gap = 1.2
        outlier_ratio = 3.5

    # --- Pass 1: Enforce minimum gap (cascade forward) ---
    for i in range(1, len(lines)):
        gap = lines[i]["cueIn"] - lines[i - 1]["cueIn"]
        if gap < min_gap:
            lines[i]["cueIn"] = round(lines[i - 1]["cueIn"] + min_gap, 2)

    # --- Pass 2: Outlier ceiling — redistribute gaps that are suspiciously large ---
    # A large gap after a rushed pair means the aligner stole time and dumped it
    # as dead space. We detect it by comparing each gap to the median gap, then
    # redistribute the surplus evenly to the neighbours.
    gaps = [lines[i]["cueIn"] - lines[i - 1]["cueIn"] for i in range(1, len(lines))]
    if gaps:
        sorted_gaps = sorted(gaps)
        median_gap = sorted_gaps[len(sorted_gaps) // 2]
        ceiling = outlier_ratio * median_gap

        for i in range(1, len(lines)):
            gap = lines[i]["cueIn"] - lines[i - 1]["cueIn"]
            if gap > ceiling and i + 1 < len(lines):
                # Steal half the surplus from this gap and give it to the next.
                surplus = gap - ceiling
                half = round(surplus / 2, 2)
                lines[i]["cueIn"] = round(lines[i]["cueIn"] - half, 2)
                # Cascade: bump subsequent lines forward only if they'd collide.
                # (They shouldn't, but guard anyway.)
                for j in range(i + 1, len(lines)):
                    if lines[j]["cueIn"] < lines[j - 1]["cueIn"] + min_gap:
                        lines[j]["cueIn"] = round(lines[j - 1]["cueIn"] + min_gap, 2)
                    else:
                        break

    changed = sum(1 for i, l in enumerate(lines) if l["cueIn"] != original[i])
    return changed


def smooth_timestamp_map(timestamp_map: list[dict], chant_id_set: set[str] | None = None) -> None:
    """
    Run smooth_service_chant on every chant in the timestamp_map.
    If chant_id_set is given, only smooth those chants.
    Prints a summary line for each chant where changes were made.
    """
    for entry in timestamp_map:
        cid = entry["chantId"]
        if chant_id_set and cid not in chant_id_set:
            continue
        lines = entry.get("lines", [])
        if not lines:
            continue
        span = lines[-1]["cueIn"] - lines[0]["cueIn"] if len(lines) > 1 else 0
        changed = smooth_service_chant(cid, lines, span)
        if changed:
            print(f"  [smooth] {cid}: adjusted {changed} line(s)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

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
    parser.add_argument(
        "--language", metavar="LANG", default="en",
        help="Language code for alignment (default: en)",
    )
    parser.add_argument(
        "--model", metavar="NAME", default="base",
        help="stable-whisper model name: base | small | medium | large (default: base). "
             "Use 'small' or 'medium' for phonetically dense dharanis or Japanese chants.",
    )
    parser.add_argument(
        "--no-smooth", action="store_true",
        help="Skip the post-alignment smoothing pass",
    )
    parser.add_argument(
        "--smooth-only", action="store_true",
        help="Re-run smoothing on the existing timestampMap without re-aligning. "
             "Useful for tuning parameters without re-running the model.",
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

    # --smooth-only: re-smooth existing timestampMap without re-aligning
    if args.smooth_only:
        existing_map = service.get("timestampMap")
        if not existing_map:
            print(f"Error: service '{args.service_id}' has no timestampMap to smooth.", file=sys.stderr)
            sys.exit(1)
        print(f"Re-smoothing existing timestampMap for '{args.service_id}'…")
        smooth_timestamp_map(existing_map)
        apply_corrections(service, existing_map)
        service["timestampMap"] = existing_map
        bak_path = json_path.with_suffix(json_path.suffix + ".bak")
        shutil.copy2(json_path, bak_path)
        print(f"Backed up original to {bak_path}")
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Wrote updated JSON to {json_path}")
        return

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
    print(f"Model:   {args.model}")
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
    print(f"\nLoading stable-whisper model ({args.model}, cpu)…")
    model = stable_whisper.load_model(args.model, device="cpu")

    print("Aligning…")
    result = model.align(service["audio"], transcript, language=args.language)
    words = flatten_words(result.segments)

    # Match each line's first word forward through the word list
    pointer = 0
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

    # Smoothing pass
    if not args.no_smooth:
        print("\nSmoothing timestamps…")
        smooth_timestamp_map(timestamp_map)

    apply_corrections(service, timestamp_map)
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
