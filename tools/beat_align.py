#!/usr/bin/env python3
"""
Prototype: use librosa onset/beat detection to align chant lines to a rhythmic pulse.

Usage:
    python3 tools/beat_align.py <audio_file> <num_lines> <start_time> <end_time>

Example:
    python3 tools/beat_align.py audio/sfzc/clips/maka_hannya_tuesday.mp3 38 283 330

Arguments:
    audio_file  — path to audio clip
    num_lines   — number of chant lines to align
    start_time  — section start in seconds (relative to clip start)
    end_time    — section end in seconds (relative to clip start)

This is a diagnostic tool — prints results only, does not write to JSON.
"""

import argparse
import sys
import numpy as np
import librosa


def main():
    parser = argparse.ArgumentParser(description="Onset/beat detection for chant alignment.")
    parser.add_argument("audio_file", help="Path to audio clip")
    parser.add_argument("num_lines", type=int, help="Number of chant lines")
    parser.add_argument("start_time", type=float, help="Section start time (seconds)")
    parser.add_argument("end_time", type=float, help="Section end time (seconds)")
    args = parser.parse_args()

    print(f"Loading {args.audio_file} …")
    y, sr = librosa.load(args.audio_file, sr=None, mono=True)

    # Extract sub-section
    start_sample = int(args.start_time * sr)
    end_sample = int(args.end_time * sr)
    section = y[start_sample:end_sample]
    duration = args.end_time - args.start_time
    print(f"Section: {args.start_time}s – {args.end_time}s ({duration:.1f}s), {args.num_lines} lines\n")

    # Onset detection
    onset_frames = librosa.onset.onset_detect(y=section, sr=sr, units='time')
    onset_times = onset_frames  # already in seconds (relative to section start)
    print(f"Detected {len(onset_times)} onsets:")
    for i, t in enumerate(onset_times):
        abs_t = round(t + args.start_time, 3)
        print(f"  onset {i:3d}: section={t:.3f}s  abs={abs_t:.3f}s")

    # Beat tracking
    tempo, beat_frames = librosa.beat.beat_track(y=section, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    print(f"\nBeat tempo: {float(tempo):.1f} BPM, {len(beat_times)} beats detected:")
    for i, t in enumerate(beat_times):
        abs_t = round(t + args.start_time, 3)
        print(f"  beat  {i:3d}: section={t:.3f}s  abs={abs_t:.3f}s")

    # Group onsets into N groups — one per line
    # Divide section evenly into N windows, find nearest onset to each division point
    print(f"\nNearest-onset assignment ({args.num_lines} lines):")
    if len(onset_times) == 0:
        print("  No onsets detected — cannot assign.")
        return

    division_points = np.linspace(0, duration, args.num_lines + 1)[:-1]  # N start points
    assigned = []
    for i, dp in enumerate(division_points):
        nearest_idx = int(np.argmin(np.abs(onset_times - dp)))
        t_section = onset_times[nearest_idx]
        t_abs = round(float(t_section) + args.start_time, 2)
        assigned.append(t_abs)

    print(f"  {'line':<6} {'abs_time':>10}")
    print(f"  {'-'*6} {'-'*10}")
    for i, t in enumerate(assigned):
        print(f"  {i:<6} {t:>10.2f}")


if __name__ == "__main__":
    main()
