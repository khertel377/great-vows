# Great Vows — Project State Document
*Generated for context handoff. Paste this into new conversations to resume work.*

---

## What We're Building

**Great Vows** is a web app for Zen chanting practice — a digital liturgy companion that plays real recordings of morning services while displaying synchronized scrolling text (teleprompter-style), ceremony cues (bows, bells, posture changes), and chant announcements. The experience is like a karaoke/teleprompter for Zen practice, designed to help home practitioners maintain the forms of monastic life.

**Core product thesis:** "The schedule is the teacher." The app holds the ceremonial container so practitioners don't have to reconstruct it alone at home after retreat.

**Target users:** Home practitioners, retreat returnees, people who can't attend in-person sangha.

**The user is called:** Shravaka (Sanskrit: "hearer/listener") — the one who heard the teaching and is trying to live by it. Pre-sectarian, pan-Indian. Not Pilot (too much agency/steering energy — wrong for this product).

**Starting tradition:** American Soto/Rinzai Zen, beginning with SFZC (San Francisco Zen Center) and ZCD (Zen Center of Denver).

---

## Product Vision

### The Train
The schedule is the spine of the experience. Morning service, zazen periods, meals, work — these are cars on a train. The train runs whether you're on it or not. You tune in, you don't start it.

**Key metaphors synthesized:**
- **Temple bell / horarium** — the SOURCE metaphor. The bell summons. You respond or you don't.
- **Radio broadcast** — "already running" quality. You tune in mid-broadcast. The app opens on wherever the day is.
- **Tide table** — emotional register. Natural law, not human imposition. The schedule just *is*.
- **Japanese departures board** — visual language for the schedule display. Current train highlighted. Past trains gone without apology.
- **Swiss railway clock** — the Landeau energy made physical. Everything synchronized. The pause before commitment.

**The Spotify comparison:** We built the lyrics page (synchronized chanting view). Now we're building the album page (the schedule/horarium that contextualizes it).

### The Horarium
A full daily schedule — the monastic day — that runs on real clock time. Periods: han, zazen, kinhin, morning service, breakfast, work, noon meal, afternoon work, evening zazen, evening service, dinner, rest, lights out. Each period has a type, a voice line, a role speaker, and optionally a live service to enter.

### The Form Factor
**The placed device** is the key insight. A phone in your pocket is a distraction machine. The same phone, placed in a small stand on the floor in front of your cushion facing the altar — it becomes a ritual object. The gesture of placement IS the beginning of the period.

**Landscape orientation** — phone on its side in the stand. The schedule reads like a departures board. The chanting view reads like a music stand.

**The Stupa concept** — a small, beautiful stand (wood or unglazed ceramic, MagSafe base, weighted, floor-angle) that transforms whatever device is slotted into it. When your phone is in the stupa, it runs Great Vows. The physical act of docking is the ritual beginning. Carry it across the train car moments of your day. Optional, but the form factor is crucial.

**Three display modes:**
1. **Phone in hand** — portrait, Spotify pattern, now-playing bar → tap → full service view
2. **Phone/iPad in stand** — landscape, placed mode, departures board, glanceable at distance
3. **Ambient/shelf** — always-on, never touched, current period visible across the room

**Accelerometer trigger** — detect when device is placed/angled in a stand and auto-shift to placed mode. No tap required.

### Future Hardware Ecosystem (not blocking)
- **Watch as han** — haptic tap at period transitions. The inescapable summons on your wrist. High leverage, build later.
- **Speaker network** — han audio fills the room. HomePod / smart speaker via HomeKit/Shortcuts.
- **The distributed bell** — watch + speaker + screen all fire at once. The tide that fills the space.

---

## Tech Stack

- Pure HTML/CSS/JS single-page app (`index.html`)
- New: `schedule.html` — the horarium/train schedule page
- JSON data files (`chantbook.json`, `sanghas/sfzc.json`, `sanghas/zcd.json`)
- Python tools for audio processing
- Local server: **`npx serve .`** (NOT `python3 -m http.server` — MP4 seeking requires HTTP range requests)
- Git for version control
- **Claude Code** for execution (preferred over file download loop)

**Project location:** `/Users/kevin/Desktop/great-vows/`

---

## File Structure

```
great-vows/
  chantbook.json          ← manifest: lists sanghas, cross-links
  schedule.html           ← NEW: horarium / train schedule page
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
    align.py
    align_service.py
    extract_clip.py
    merge_clip_alignment.py
    correct_timestamp.py
    apply_corrections.py
    beat_align.py
    test_aeneas.py
  index.html              ← the chanting/service app
  README.md
  .gitignore
```

---

## Three Active Tracks

### Track 1 — Service content (existing pipeline)
Complete alignment for Wednesday, Thursday, Full Moon, One Day Sitting. Same workflow as Mon/Tue.

### Track 2 — The Train (new, in progress)
`schedule.html` — the always-on horarium. Real clock. Current period. What's now, what's next. The departures board view.

**Current state of schedule.html:**
- Live clock (IBM Plex Mono), paper/ink aesthetic (Cormorant serif + warm paper background)
- Full day timeline with past/now/future states
- Past: 45% opacity. Now: blue left border + glow + larger text + voice quote. Future: 78% opacity.
- Sidebar: sangha name, clock, current period name, voice line, minutes remaining, Enter service button
- Progress bar crawls across current period in real time
- `getBetweenState()` handles gaps between periods, pre-schedule, post-schedule correctly
- Placed mode: auto-detects landscape orientation, bumps up sizes for shelf viewing
- "Enter service →" button active only during live service periods; navigates to `index.html?service=ID`
- **Known remaining:** wire Enter button to actual index.html; pull schedule data from sfzc.json instead of hardcoded JS

### Track 3 — Ambient display mode (planned)
iPad landscape always-on display. Same data as schedule.html, stripped-down skin. Just now + next, giant clock, visible across the room. The screen outside the zendo.

---

## Temple Staff / Character System

The app has a voice system — brief utterances from named roles at appropriate moments. Not chatbots. The right person arriving at the right moment with exactly the words the function requires. Then gone.

| Role | Domain | Voice register | Example |
|------|---------|---------------|---------|
| **Ino** | Schedule, bells, transitions, the train | Clipped, Swiss, no negotiation | "5:30. Sit." |
| **Doshi** | Ceremony, service announcements, chant cues | Minimal, ceremonial, pure form | "Heart Sutra." |
| **Tanto** | Zazen periods, kinhin, practice | Gruff-warm, occasional dharma note | "Just sit." |
| **Tenzo** | Meals, food periods, kitchen | Pragmatic, dignified, no fuss | "Eat moderately. Clean your bowl." |
| **Shika** | Work period, soji, ordinary life | Grounded, slightly irreverent | "Whatever is in front of you." |

**Design principle:** The titles ARE the characters. No names, no personalities beyond register. The role is bigger than any person. You relate to the Ino-function, not a specific individual.

**Landeau** — the real Swiss ex-train-conductor Zen student at Green Gulch who inspired the Ino character. Serious, dry, wry, did not suffer delusive honeymoon ego games. His obvious underlying warmth only visible once you stopped needing him to perform it. Lives in the git history and the README.

---

## The Hungry Ghost Universe

A separate but related creative world — a contemplative game/monastic simulator concept ("Zen temple in cold hell," Spiritfarer-style) — that informs the app's character design vocabulary. Not the product, but upstream creative DNA.

**The animal-role system** (from sketchbook):
- 🐍 Snake → Ino (watchful, coiled, precise)
- 🐸 Frog → Doshi (ceremonial, between worlds)
- 🦉 Owl → Kokyo (chant leader, sees in dark)
- 🐉 Dragon → Doan (hall assistant, fire keeper)
- 🦊 Fox → Chiden (altar attendant)
- 🐢 Turtle → Fukudo (silence keeper, strikes the han)
- 🐯 Tiger → Tanto ("...GRUMBLE...")
- 🐷 Pig → Tenzo (head cook)
- 🐴 Horse → Shika (head of guests)
- 🐇 Rabbit → Abbot (holds the dharma)
- 🐐 Goat → Director/Tsusu ("Welcome, Shravaka.")

**The player character:** The Hungry Ghost — arrives at the temple with enormous craving and a needle-thin throat. This is us. This is why we practice.

**The greeting:** *"Gassho, Shravaka. My home was eaten by the wind."* — the onboarding moment. The post-retreat practitioner trying to keep practice alive alone.

**Shravaka** (not Pilot, not Shramana) — Sanskrit: "hearer/listener." The Buddha's immediate disciples, those who heard the dharma and transmitted it. In this context: you showed up to listen. That's enough. The app IS a listening experience.

This universe is available as a future Layer 3 of the product (animal avatars, full character art, Goat-Director welcoming you). Current product is Layer 1-2 (role titles, voice register, no full character art).

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
  "crossLinks": [ ... ]
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
      "audio": "audio/sfzc/Great_Vows.mp3",
      "lines": [
        { "text": "Beings are numberless.", "cueIn": 24.0 },
        { "text": null },
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
      "recordingChants": ["heart-sutra", "hymn-perfection-wisdom", ...],
      "items": [ ... ],
      "timestampMap": [ ... ],
      "timestampCorrections": { ... }
    }
  ]
}
```

### Schedule data (currently hardcoded in schedule.html, future: schedule.json or sfzc.json)
```js
{
  id: 'morning-service-monday',
  time: [6, 40],   // 24h [hour, minute]
  end:  [7, 0],
  name: 'Monday Morning Service',
  type: 'chant',   // bell | zazen | chant | meal | work | rest
  voice: '"Heart Sutra."',
  voiceRole: 'Doshi',
  hasService: true,
  serviceId: 'morning-service-monday',
}
```

---

## Key Concepts

### Item types in service.items
- `"ceremonial"` — bells, bows, silence. Has `cues[]` with `{time, emoji, text}`.
- `"doshi"` — single voice reading. Has `label`. Auto-generates announcement cue.
- `"chant"` — assembly chanting. Has `id` pointing to chant. Add `"noAnnouncement": true` to suppress.
- `"silence"` — zazen period. Has `durationMinutes`.

### timestampMap vs timestampCorrections
- `timestampMap` — machine-generated. Freely overwritten on re-alignment.
- `timestampCorrections` — human-authored. NEVER overwritten by tools. Always applied on top.

### Announcement auto-generation
`loadService()` scans for `type: "doshi"` items, finds next `type: "chant"`, creates ceremony cue at `startTime - 10s`. Respects `noAnnouncement: true`. Uses `hasDoshiBetween` logic.

---

## Alignment Pipeline

**Step 1** — Listen through recording, note which chants, start/end times, repeats.

**Step 2** — Update sfzc.json: `recordingChants`, day-specific variants, doshi items, remove old `timestampMap`.

**Step 3** — Extract clips:
```bash
python3 tools/extract_clip.py audio/sfzc/MorningService_X.mp4 [start_s] [end_s] audio/sfzc/clips/chant_day.mp3
```

**Step 4** — Align:
```bash
python3 tools/align.py sanghas/sfzc.json --chant shosaimyo-x3 --audio audio/sfzc/clips/shosaimyo_x3_monday.mp3 --model large
python3 tools/align.py sanghas/sfzc.json --chant heart-sutra --audio audio/sfzc/clips/heart_sutra_monday.mp3
```

**Step 5** — Merge:
```bash
python3 tools/merge_clip_alignment.py sanghas/sfzc.json morning-service-monday chant-id [start_offset_seconds]
```

**Step 6** — Strip cueIn from chant objects (prevents standalone contamination):
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

**Step 7** — Sort timestampMap. **Step 8** — Manual corrections for problem sections.

---

## Service Status

### Monday Morning Service ✓
1. Opening ceremony (9 bows) ✓
2. Heart Sutra (English) ✓ — manual corrections lines 17-25
3. Hymn to Perfection of Wisdom ✓
4. Shōsaimyō ×3 ✓
5. Eko (doshi)
6. Names of Buddhas and Ancestors (Monday truncated) ✓
7. Names of Women Ancestors ✓
8. Eko — Suzuki Roshi (doshi)
9. After Dedication Japanese ✓ — manual corrections
10. Closing ceremony ✓

### Tuesday Morning Service ✓
1. Opening ceremony ✓
2. Maka Hannya Haramitta Shin Gyō ✓ — manual corrections lines 19-25
3. Hymn ✓
4. Shōsaimyō ×3 ✓
5. Warning bells, eko (doshi)
6. After Dedication English ✓
7. Loving Kindness Meditation ✓
8. Enmei Jukku ×7 ✓
9. Warning bells, eko (doshi)
10. After Dedication Japanese ✓
11. Closing ceremony ✓

### Wednesday — Not started (17:20 duration)
### Thursday — Not started (19:30 duration)

---

## Chant Variants

| ID | Description |
|---|---|
| `shosaimyo-x3` | Shōsaimyō ×3 (47 lines) |
| `enmei-jukku-x7` | Enmei Jukku ×7 |
| `names-buddhas-ancestors-monday` | Truncated Monday version |
| `after-dedication-japanese` | Japanese half only |
| `after-dedication-english` | English half only |
| `after-dedication-english-tuesday-1` | Tuesday occurrence at 11:00 |

---

## UI Architecture

### The Teleprompter (index.html)
Single unified scrolling track. Chant lines and ceremony cues as `<span class="chant-line">`. No separate overlay.

**Display states:** active (dist 0) → next (+1, 0.4) → near-next (+2, 0.15) → past (-1, 0.2) → near-past (-2, 0.1) → hidden.

**Spotlight mode:** When playing: `next` → 0.15, everything else → 0.

**Windowed rendering:** Only renders items within current + 180s window. Rebuilds when < 90s future content remains.

**Seek bar:** Custom div-based (not `<input type="range">`). Handles mousedown/mousemove/mouseup on `#seekWrap`.

### The Schedule (schedule.html) — NEW
**Aesthetic:** Japanese utilitarian-sacred. IBM Plex Mono for time/data. Cormorant serif for period names. Warm paper background (#f4f0e8). Grain overlay for warmth.

**Layout:** 200px sidebar (clock + now summary + enter button) | flex-1 schedule track.

**Period states:** past (45% opacity) | now (blue left border + glow + larger text + voice quote + progress bar) | future (78% opacity).

**Sidebar:** Shows "Now" or "Next" depending on whether inside a period or between. Voice line from the appropriate role. Minutes remaining / countdown. Enter button active only during live service periods.

**Placed mode:** Auto-detects landscape orientation via `window.innerWidth > window.innerHeight * 1.4`. Bumps clock to 52px, period name to 26px, dims future/past further.

**Clock:** Ticks every second. Re-renders schedule on minute change. Progress bar updates every second.

---

## Known Bugs / Next Steps

### Immediate (Claude Code)
- [ ] Wire schedule.html "Enter service →" to `index.html?service=ID`
- [ ] Verify now-detection fix works at actual daytime hours (10:42 AM work period bug)
- [ ] Visual tuning: placed mode sizing, past/now contrast
- [ ] Wednesday morning service — listen through and align
- [ ] Thursday morning service — listen through and align
- [ ] `endTime` explicit field support in loadService()
- [ ] Maka-hannya dense section (Tuesday ~5:00) still slightly rough

### Schedule / Architecture
- [ ] Pull horarium data from `sfzc.json` or new `schedule.json` instead of hardcoded JS
- [ ] `schedule.json` data format design
- [ ] Portrait/mobile layout for schedule.html
- [ ] Full Moon Ceremony alignment
- [ ] One Day Sitting alignment
- [ ] ZCD chant book — needs audio recordings

### Product / Design
- [ ] Ambient/iPad mode — stripped-down landscape skin, just now + next, giant clock
- [ ] Watch as han — haptic tap at period transitions (later, high leverage)
- [ ] "Surrender the phone" placement gesture — landing animation when device placed in stand
- [ ] Onboarding: "Gassho, Shravaka. The schedule is already running."
- [ ] Schedule / practice clock home screen linking schedule.html → index.html
- [ ] Time zone handling for social layer
- [ ] GitHub / deployment

---

## Git Workflow

```bash
git add .
git commit -m "description"
git checkout .          # rollback
npx serve /Users/kevin/Desktop/great-vows
# localhost:3000
```

Current branch: `main`.

---

## Product Vision Notes

- **"The schedule is the teacher"** — the app holds the form
- **The train doesn't negotiate** — no snooze, no rescheduling. The bell rang. Next one at noon.
- **Shravaka is the user** — the hearer, the listener, the one who showed up. Not the pilot.
- **"Gassho, Shravaka. My home was eaten by the wind."** — the onboarding line. The whole app in one sentence.
- **The placed device is already a ritual object** — the photo of the phone on the floor in front of the altar/cushion IS the product shot. Honor that instinct in every design decision.
- **Layer 1:** Just the schedule + chanting. Works now.
- **Layer 2:** Temple staff voices. Ino announces periods. Doshi announces chants.
- **Layer 3:** Full Hungry Ghost universe. Animal characters. Goat welcomes you. Tiger grumbles.
- **The stupa** — a wooden MagSafe stand, weighted, floor-angled, travel-sized. Your passport for the train. Someday.
- **Landeau lives in the README.**
