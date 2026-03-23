# Great Vows — Project State Document
*Generated for context handoff. Paste this into new conversations to resume work.*

---

## What We're Building

**Great Vows** is a web app for Zen chanting practice — a digital liturgy companion that plays real recordings of morning services while displaying synchronized scrolling text (teleprompter-style), ceremony cues (bows, bells, posture changes), and chant announcements. The experience is like a karaoke/teleprompter for Zen practice, designed to help home practitioners maintain the forms of monastic life.

**Core product thesis:** "The schedule is the teacher." The app holds the ceremonial container so practitioners don't have to reconstruct it alone at home after retreat.

**Target users:** Home practitioners, retreat returnees, people who can't attend in-person sangha.

**Starting tradition:** American Soto/Rinzai Zen, beginning with SFZC (San Francisco Zen Center) and ZCD (Zen Center of Denver).

---

## Tech Stack

- Pure HTML/CSS/JS single-page app (`index.html`)
- JSON data files (`chantbook.json`, `sanghas/sfzc.json`, `sanghas/zcd.json`)
- Python tools for audio processing
- Local server: **`npx serve .`** (NOT `python3 -m http.server` — MP4 seeking requires HTTP range requests)
- Git for version control
- Claude Code for execution

**Project location:** `/Users/kevin/Desktop/great-vows/`

---

## File Structure

```
great-vows/
  chantbook.json          ← manifest: lists sanghas, cross-links
  sanghas/
    sfzc.json             ← SFZC chant book (main working file, ~5500 lines)
    zcd.json              ← ZCD chant book (stub, no audio yet)
  audio/
    sfzc/
      Great_Vows.mp3
      MorningService_Monday.mp4
      MorningService_Tuesday.mp4
      MorningService_Wednesday.mp4
      MorningService_Thursday.mp4
      Full_Moon_Ceremony.mp4
      One_Day_Sitting.mp4
      temple_sounds-the_han.mp3
      temple_sounds-the_denshp_bell.mp3
      temple_sounds-opening_chant.mp3
    sfzc/clips/           ← extracted audio clips for alignment
  tools/
    align.py              ← align single chant to audio clip
    align_service.py      ← align full service recording
    extract_clip.py       ← extract audio clip from recording
    merge_clip_alignment.py ← merge clip timestamps into service timestampMap
    correct_timestamp.py  ← add manual timestamp correction
    apply_corrections.py  ← helper module: apply timestampCorrections
    beat_align.py         ← diagnostic: beat/onset detection (not used in prod)
    test_aeneas.py        ← diagnostic: aeneas test (abandoned)
  index.html              ← the app
  README.md
  .gitignore
```

---

## Data Model

### `chantbook.json` (manifest)
```json
{
  "version": "1.0",
  "sanghas": [
    { "id": "sfzc", "name": "San Francisco Zen Center", "file": "sanghas/sfzc.json", "color": "#2a3fcc" },
    { "id": "zcd",  "name": "Zen Center of Denver",     "file": "sanghas/zcd.json",  "color": "#8b4a2a" }
  ],
  "crossLinks": [ ... ]   ← chants appearing in multiple sanghas
}
```

### Sangha file structure (`sfzc.json`)
```json
{
  "id": "sfzc",
  "chants": [
    {
      "id": "great-vows",
      "title": "Four Bodhisattva Vows",
      "section": "Short Verses",
      "audio": "audio/sfzc/Great_Vows.mp3",  // null if no standalone audio
      "lines": [
        { "text": "Beings are numberless.", "cueIn": 24.0 },
        { "text": null },   // null = paragraph break
        ...
      ]
    }
  ],
  "services": [
    {
      "id": "morning-service-monday",
      "title": "Monday Morning Service",
      "audio": "audio/sfzc/MorningService_Monday.mp4",
      "duration": 1180,
      "recordingChants": ["heart-sutra", "hymn-perfection-wisdom", "shosaimyo-x3", ...],
      "items": [
        { "type": "ceremonial", "label": "Opening ceremony", "cues": [
          { "time": 0, "emoji": "〰️", "text": "Prepare to bow" },
          { "time": 39, "emoji": "⬇️", "text": "Bow" },
          ...
        ]},
        { "type": "doshi", "label": "Heart Sutra announcement" },
        { "type": "chant", "id": "heart-sutra", "noAnnouncement": true },
        { "type": "chant", "id": "hymn-perfection-wisdom" },
        ...
        { "type": "ceremonial", "label": "Closing bells and bows", "cues": [...] }
      ],
      "timestampMap": [
        {
          "chantId": "heart-sutra",
          "startTime": 251.95,
          "lines": [
            { "lineIndex": 0, "cueIn": 251.95 },
            ...
          ]
        }
      ],
      "timestampCorrections": {
        "heart-sutra": [
          { "lineIndex": 17, "cueIn": 302.5 },
          ...
        ]
      }
    }
  ]
}
```

---

## Key Concepts

### Item types in service.items
- `"ceremonial"` — bells, bows, silence. Has `cues[]` array with `{time, emoji, text}`.
- `"doshi"` — single voice reading/chanting. Has `label`. Auto-generates announcement cue in the teleprompter.
- `"chant"` — assembly chanting. Has `id` pointing to chant in `chants[]`. Add `"noAnnouncement": true` to suppress auto-generated title announcement.
- `"silence"` — zazen period. Has `durationMinutes`.

### timestampMap vs timestampCorrections
- `timestampMap` — machine-generated by alignment tools. Freely overwritten on re-alignment.
- `timestampCorrections` — human-authored manual corrections. NEVER overwritten by tools. Always applied on top of timestampMap.

### recordingChants
Array of chant IDs actually present in the service recording (may differ from items). Used by `align_service.py` to know what to align. Separate from `items` because recordings often skip or truncate chants.

### Announcement auto-generation
`loadService()` in `index.html` scans service items for `type: "doshi"` items, finds the next `type: "chant"` item, looks up its startTime in timestampMap, and creates a ceremony cue at `startTime - 10s`. Respects `noAnnouncement: true`. Uses `hasDoshiBetween` logic so only the closest doshi generates the announcement.

---

## Alignment Pipeline

### Tools and workflow for a new service day:

**Step 1 — Listen through the recording**
Note: which chants are present, start/end times (mm:ss), any repeats or variations.

**Step 2 — Update sfzc.json**
- Set `recordingChants` for the service
- Add day-specific chant variants if needed (e.g. `names-buddhas-ancestors-monday`)
- Add doshi announcement items in service `items`
- Remove existing `timestampMap` if re-aligning

**Step 3 — Extract clips** (one per chant)
```bash
python3 tools/extract_clip.py audio/sfzc/MorningService_X.mp4 [start_s] [end_s] audio/sfzc/clips/chant_day.mp3
```

**Step 4 — Align each clip**
```bash
# Dense Japanese chants: use --model large
python3 tools/align.py sanghas/sfzc.json --chant shosaimyo-x3 --audio audio/sfzc/clips/shosaimyo_x3_monday.mp3 --model large

# English chants: base model is fine
python3 tools/align.py sanghas/sfzc.json --chant heart-sutra --audio audio/sfzc/clips/heart_sutra_monday.mp3
```

**Step 5 — Merge each clip**
```bash
python3 tools/merge_clip_alignment.py sanghas/sfzc.json morning-service-monday chant-id [start_offset_seconds]
```

**Step 6 — Strip cueIn from chant objects** (prevents standalone cueIn contamination)
```bash
python3 -c "
import json
data = json.load(open('sanghas/sfzc.json'))
for chant in data['chants']:
    if chant['id'] in ['shosaimyo-x3', 'enmei-jukku-x7']:
        for line in chant['lines']:
            line.pop('cueIn', None)
with open('sanghas/sfzc.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')
"
```

**Step 7 — Sort timestampMap**
```bash
python3 -c "
import json
data = json.load(open('sanghas/sfzc.json'))
svc = next(s for s in data['services'] if s['id'] == 'morning-service-monday')
svc['timestampMap'].sort(key=lambda e: e['startTime'])
with open('sanghas/sfzc.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')
"
```

**Step 8 — Manual corrections for problem sections**
```bash
python3 tools/correct_timestamp.py sanghas/sfzc.json morning-service-monday heart-sutra 17 302.5
```

### Known alignment challenges
- **Dense Japanese lists** (shosaimyo, darani, maka-hannya): use `--model large`, still may need manual corrections for "no eyes no ears" equivalent sections
- **Repeated chants** (shosaimyo-x3, enmei-jukku-x7): pointer sometimes jumps to wrong repetition — smoother helps
- **Long recordings**: segment first, align per-clip, merge back
- **PDF column interleaving**: shosaimyo and enmei-jukku were on the same PDF page in two columns — text was extracted interleaved. Now fixed.

---

## Monday Morning Service — Status

**Chant sequence:**
1. Opening ceremony (9 bows, offerings, prepare for chanting)
2. Heart Sutra (English) — aligned ✓, manual corrections for lines 17-25
3. Hymn to Perfection of Wisdom — aligned ✓
4. Shōsaimyō Kichijō Darani ×3 — aligned ✓ (re-aligned after text fix)
5. Eko (doshi)
6. Names of Buddhas and Ancestors (Monday truncated version) — aligned ✓
7. Names of Women Ancestors — aligned ✓
8. Eko — Suzuki Roshi veneration (doshi)
9. After Dedication (Japanese: Ji ho san shi...) — aligned ✓, manual corrections
10. Closing ceremony (3 bows, bow to altar, bow to each other, process out)

**Announcements:** Heart Sutra, Hymn, Shōsaimyō, Names of Buddhas, Names of Women — all have doshi items and auto-generated cues.

**Known issues:**
- After-dedication-japanese closes at ~17:27 with `endTime: 1047` pending explicit implementation
- Closing ceremony cues: 17:32 first bow through 19:26 process out — in place

---

## Tuesday Morning Service — Status

**Chant sequence:**
1. Opening ceremony (offering in progress, 9 bows, restore, prepare for chanting)
2. Maka Hannya Haramitta Shin Gyō (Japanese Heart Sutra) — aligned ✓, manual corrections lines 19-25
3. Hymn to Perfection of Wisdom — aligned ✓
4. Shōsaimyō Kichijō Darani ×3 — aligned ✓
5. Warning bells, eko (doshi) — Luminous Mirror Wisdom
6. Hold standing bow / Rise (ceremony cues)
7. After Dedication English (All buddhas...) — aligned ✓
8. Loving Kindness Meditation — aligned ✓
9. Enmei Jukku Kannon Gyō ×7 — aligned ✓
10. Warning bells, eko (doshi)
11. Shashu bow (ceremony cue)
12. After Dedication Japanese (Ji ho san shi...) — aligned ✓, manual corrections
13. Closing ceremony (restore, bow to altar, bow to each other, process out)

**Known issues:**
- Maka-hannya dense section still slightly rough around 5:00 mark despite manual corrections

---

## Wednesday and Thursday — Status

**Not started.** Will follow same workflow as Tuesday. Need to listen through each recording and note:
- Which chants are present
- Start/end times
- Any variations from Monday/Tuesday

Wednesday is 17:20, Thursday is 19:30 duration.

---

## Chant Variants Created for Service Use

| ID | Description |
|---|---|
| `shosaimyo-x3` | Shōsaimyō repeated 3× (15 lines × 3 + 2 nulls = 47 lines) |
| `enmei-jukku-x7` | Enmei Jukku repeated 7× |
| `names-buddhas-ancestors-monday` | Truncated ancestors list (Monday only chants through Kēizān Jōkīn) |
| `after-dedication-japanese` | Japanese half only (Ji ho san shi...ho ro mi) |
| `after-dedication-english` | English half only (All buddhas...Maha Prajna Paramita) |
| `after-dedication-english-tuesday-1` | Tuesday occurrence at 11:00 |

---

## UI Architecture

### The Teleprompter System
Single unified scrolling track. Both chant lines and ceremony cues render as `<span class="chant-line">` elements in `#chantTrack`. No separate overlay system.

### Display states (distance from active line)
- `active` (dist 0): opacity 1, full white
- `next` (dist +1): opacity 0.4
- `near-next` (dist +2): opacity 0.15
- `past` (dist -1): opacity 0.2
- `near-past` (dist -2): opacity 0.1
- `hidden` (dist > ±2): opacity 0, invisible

### Spotlight mode
When playing (not scrubbing): `next` → 0.15, everything else → 0. Only active line visible.

### Windowed rendering
Track only renders items within a time window (current + 180s). `rebuildTrackIfNeeded()` called from tick() when < 90s of future content remains.

### Ceremony cues
- IDs: `line-C-0`, `line-C-1`, etc.
- Interleaved with chant lines by time in `getAllTimedItems()`
- Chant lines win tiebreaks over ceremony cues at same timestamp
- Auto-generated title announcements from `doshi` items in service definition

### Seek bar
Custom div-based seek bar (not `<input type="range">`) — range inputs had cross-browser drag issues. Handles mousedown/mousemove/mouseup on `#seekWrap`. Updates ceremony line and stage visibility in real time during drag.

### Sangha switcher
Top of index screen. Switches between SFZC and ZCD. Updates accent color from sangha's `color` field. ZCD has no audio yet so shows listening mode.

---

## Known Bugs / Next Steps

### Immediate
- [ ] Wednesday morning service — listen through and align
- [ ] Thursday morning service — listen through and align
- [ ] `endTime` explicit field support in loadService() (Monday closing ceremony timing)
- [ ] Maka-hannya dense section (Tuesday ~5:00) — still slightly rough

### Product / Architecture
- [ ] Full Moon Ceremony — has audio, needs alignment
- [ ] One Day Sitting — has audio, needs alignment  
- [ ] ZCD chant book — needs audio recordings
- [ ] Schedule / practice clock home screen (the "train schedule" concept)
- [ ] Time zone handling for "chanting now" social layer
- [ ] Sitting period container (zazen with held silence)
- [ ] GitHub / deployment to real server

### Design
- [ ] "Coming home from retreat" onboarding path
- [ ] Inter-sangha chant cross-linking UI ("also chanted at ZCD")
- [ ] Mobile optimization

---

## Git Workflow

```bash
# Before significant changes:
git add .
git commit -m "description of working state"

# Roll back if something breaks:
git checkout .

# Server:
npx serve /Users/kevin/Desktop/great-vows
# then open localhost:3000
```

Current branch: `main`. All commits on main, no branches.

---

## Product Vision Notes

- **"The schedule is the teacher"** — the app holds the form, not the practitioner's willpower
- **Schedule doesn't negotiate** — no snooze, no rescheduling. The train left. Next one at noon.
- **Two user modes:** sangha-anchored (sits at SFZC, wants their exact chant book) and unaffiliated (home practitioner, post-retreat, needs the container)
- **Default inter-sangha track** — non-sectarian services for people without a specific sangha
- **Permeable membranes** — sangha labels are metadata, not hard walls. ZCD uses SFZC's Jewel Mirror Samadhi translation.
- **Practice place over lineage** — organize by where people sit, not Soto vs. Rinzai taxonomy
