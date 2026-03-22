#!/usr/bin/env python3
"""
Quick test: align maka-hannya against its Tuesday clip using aeneas.
Prints begin/end/text for each fragment for comparison with stable-whisper.

Usage:
    python3 tools/test_aeneas.py
"""

import json
import tempfile
import os
from pathlib import Path

from aeneas.executetask import ExecuteTask
from aeneas.task import Task

ROOT = Path(__file__).parent.parent
SANGHA_JSON = ROOT / "sanghas/sfzc.json"
AUDIO = ROOT / "audio/sfzc/clips/maka_hannya_tuesday.mp3"

data = json.loads(SANGHA_JSON.read_text())
chant = next(c for c in data["chants"] if c["id"] == "maka-hannya")
text_lines = [l["text"] for l in chant["lines"] if l.get("text")]

with tempfile.TemporaryDirectory() as tmpdir:
    text_path = os.path.join(tmpdir, "maka_hannya.txt")
    output_path = os.path.join(tmpdir, "sync_map.json")

    with open(text_path, "w") as f:
        f.write("\n".join(text_lines) + "\n")

    config_string = "task_language=eng|is_text_type=plain|os_task_file_format=json"
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = str(AUDIO.resolve())
    task.text_file_path_absolute = text_path
    task.sync_map_file_path_absolute = output_path

    ExecuteTask(task).execute()
    task.output_sync_map_file()

    result = json.loads(Path(output_path).read_text())

fragments = result["fragments"]
print(f"{'#':<4} {'begin':>7} {'end':>7}  text")
print("-" * 60)
for i, frag in enumerate(fragments):
    begin = float(frag["begin"])
    end = float(frag["end"])
    text = frag["lines"][0] if frag.get("lines") else ""
    print(f"{i:<4} {begin:>7.2f} {end:>7.2f}  {text}")
