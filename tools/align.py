#!/usr/bin/env python3
"""
Align chant audio to text lines using stable-whisper forced alignment.

Usage:
    python3 tools/align.py sanghas/sfzc.json
    python3 tools/align.py sanghas/sfzc.json --dry-run
    python3 tools/align.py sanghas/sfzc.json --chant names-buddhas-ancestors --audio audio/sfzc/clips/names_buddhas_monday.mp3
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
    """Return the first whitespace-delimited token from a line."""
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


def process_chant(chant: dict, model, dry_run: bool, audio_override=None, no_write_cuein: bool = False) -> int:
    """
    Align one chant.  Returns the number of lines that received a cueIn.
    If audio_override is given, use it for alignment but do not persist it.
    If no_write_cuein is True, run alignment and print results but do not
    write cueIn values back to the chant object.
    """
    audio_path = audio_override or chant.get("audio")
    lines = chant.get("lines", [])

    # Collect non-null text lines for the transcript
    text_lines = [l["text"] for l in lines if l.get("text")]
    if not text_lines:
        return 0

    transcript = " ".join(text_lines)

    print(f"  Aligning '{chant['id']}' — {audio_path}")
    if dry_run:
        print(f"    [dry-run] would align transcript: {transcript[:80]}{'…' if len(transcript) > 80 else ''}")
        return 0

    result = model.align(audio_path, transcript, language="en")
    words = flatten_words(result.segments)

    matched = 0
    pointer = 0  # advance forward after each match so repeated lines get distinct timestamps
    for line in lines:
        text = line.get("text")
        if not text:
            continue
        key = first_word(text)
        # Scan forward from pointer for the next occurrence of this line's first word
        for i in range(pointer, len(words)):
            if words[i][0] == key:
                cue = round(words[i][1], 2)
                if no_write_cuein:
                    print(f"    [no-write] {text[:40]!r} → {cue}")
                else:
                    line["cueIn"] = cue
                pointer = i + 1
                matched += 1
                break
        # else: leave cueIn unchanged if it exists, or skip

    return matched


def main():
    parser = argparse.ArgumentParser(description="Align chant audio with stable-whisper.")
    parser.add_argument("sangha_json", help="Path to sangha JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen without writing")
    parser.add_argument("--chant", metavar="ID", help="Only process the chant with this id")
    parser.add_argument("--audio", metavar="PATH", help="Override audio path for the selected chant (not written to JSON)")
    parser.add_argument("--no-write-cuein", action="store_true", help="Run alignment but do not write cueIn values back to the chant object")
    args = parser.parse_args()

    if args.audio and not args.chant:
        print("Error: --audio requires --chant", file=sys.stderr)
        sys.exit(1)

    json_path = Path(args.sangha_json)
    if not json_path.exists():
        print(f"Error: {json_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(json_path) as f:
        data = json.load(f)

    if args.chant:
        chants_with_audio = [c for c in data.get("chants", []) if c["id"] == args.chant]
        if not chants_with_audio:
            print(f"Error: chant '{args.chant}' not found in {json_path}", file=sys.stderr)
            sys.exit(1)
        if not args.audio and not chants_with_audio[0].get("audio"):
            print(f"Error: chant '{args.chant}' has no audio field and --audio was not provided", file=sys.stderr)
            sys.exit(1)
    else:
        chants_with_audio = [c for c in data.get("chants", []) if c.get("audio") is not None]

    if not chants_with_audio:
        print("No chants with audio found.")
        sys.exit(0)

    print(f"Found {len(chants_with_audio)} chant(s) with audio.")

    if not args.dry_run:
        import stable_whisper
        print("Loading stable-whisper model (base, cpu)…")
        model = stable_whisper.load_model("base", device="cpu")
    else:
        model = None

    total_chants = 0
    total_lines = 0

    for chant in chants_with_audio:
        audio_override = args.audio if (args.chant and chant["id"] == args.chant) else None
        lines_matched = process_chant(chant, model, dry_run=args.dry_run, audio_override=audio_override, no_write_cuein=args.no_write_cuein)
        total_chants += 1
        total_lines += lines_matched

    if args.dry_run:
        print(f"\n[dry-run] Would process {total_chants} chant(s).")
        print(f"[dry-run] Would back up {json_path} → {json_path}.bak")
        print(f"[dry-run] Would write updated JSON to {json_path}")
    elif args.no_write_cuein:
        print(f"\n[no-write-cuein] Alignment complete — cueIn values not written to JSON.")
    else:
        bak_path = json_path.with_suffix(json_path.suffix + ".bak")
        shutil.copy2(json_path, bak_path)
        print(f"\nBacked up original to {bak_path}")

        with open(json_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Wrote updated JSON to {json_path}")

    print(f"\nSummary: {total_chants} chant(s) processed, {total_lines} line(s) got timestamps.")


if __name__ == "__main__":
    main()
