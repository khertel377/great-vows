#!/usr/bin/env python3
"""
Extract an audio clip from a source file using ffmpeg.

Usage:
    python3 tools/extract_clip.py <source> <start> <end> <output.mp3>

Example:
    python3 tools/extract_clip.py audio/sfzc/MorningService_Monday.mp4 527 795 audio/sfzc/clips/names_buddhas_monday.mp3
"""

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Extract an audio clip via ffmpeg.")
    parser.add_argument("source", help="Source audio/video file")
    parser.add_argument("start", type=float, help="Start time in seconds")
    parser.add_argument("end", type=float, help="End time in seconds")
    parser.add_argument("output", help="Output file path (mp3)")
    args = parser.parse_args()

    source = Path(args.source)
    if not source.exists():
        print(f"Error: source file not found: {source}", file=sys.stderr)
        sys.exit(1)

    duration = args.end - args.start
    if duration <= 0:
        print(f"Error: end ({args.end}) must be greater than start ({args.start})", file=sys.stderr)
        sys.exit(1)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(args.start),
        "-to", str(args.end),
        "-i", str(source),
        "-vn",                  # audio only
        "-acodec", "libmp3lame",
        "-q:a", "2",            # VBR ~190kbps
        str(output),
    ]

    print(f"Extracting {args.start}s – {args.end}s ({duration:.1f}s) from {source} …")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("ffmpeg error:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

    print(f"Output: {output}  ({duration:.1f}s)")


if __name__ == "__main__":
    main()
