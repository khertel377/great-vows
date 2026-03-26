# Great Vows — Project State Document
*Updated after schedule canonization, three-mode system, bell taxonomy, iOS fixes, and file hygiene rules.*

---

## File Hygiene — Read First

### The canonical state doc
There is exactly **one** state doc: `great-vows-state-doc.md` in the project root.

- Naming convention: **kebab-case only** — `great-vows-state-doc.md`
- When updated, **overwrite in place** — no versioned copies, no `_v2`, no `GREAT_VOWS_STATE`, no `great_vows_state_doc`
- If CC sees any other files named similarly (`GREAT_VOWS_STATE.md`, `great_vows_state_doc.md`, `state-doc-v2.md`, etc.) — **ignore them and flag to Kevin**

### Stale files to delete (one-time cleanup)
If these still exist in the project root, delete them:
```bash
rm -f GREAT_VOWS_STATE.md
rm -f great_vows_state_doc.md
rm -f "schedule copy.html"
```

### General file hygiene rules
- No duplicate HTML files — `schedule copy.html` and similar are traps. macOS is case-insensitive, GitHub Pages (Linux) is not.
- One canonical file per purpose. If you need to experiment, use a git branch, not a copy.
- Audio path is `audio/SFZC/` — capital letters, always. Linux is case-sensitive.

---

## Session Roles & Handoff Protocol

**This project uses two Claude interfaces with distinct roles. Always clarify which mode you're in at the start of each session.**

### Claude Chat — Mac Desktop App
The studio. Used for:
- Strategizing, envisioning, diagnosing, planning
- Architecture decisions and design discussions
- Drafting fixes with enough specificity that CC can execute
- Reviewing state docs, cross-checking schedules, liturgy questions
- Writing the state doc update at session end
- Does NOT write or edit actual project files directly

**Kevin always starts sessions here.**

### Claude Code — Terminal
The workshop. Used for:
- All file reading, editing, and execution
- Running the alignment pipeline (align.py, correct_timestamp.py, etc.)
- Git commits and pushes to GitHub Pages
- Verifying fixes in the browser via `npx serve`
- Receives a task list from Chat and executes against actual files

### Handoff Protocol
1. Chat produces a clearly scoped task list with code snippets where needed
2. CC opens the actual files first, reads them, then executes — does not re-derive architecture
3. The state doc is the source of truth; paste it at the start of every session in either interface
4. At session end, Chat drafts the updated state doc; CC overwrites `great-vows-state-doc.md` in place

**Rule of thumb:** If the work involves changing files → open CC Terminal. If the work is planning or diagnosis → start in Chat, then hand off.

---

## What We're Building

Great Vows is a web app for Zen chanting practice — a digital liturgy companion that plays real recordings of morning services while displaying synchronized scrolling text (teleprompter-style), ceremony cues (bows, bells, posture changes), and chant announcements. The experience is like a karaoke/teleprompter for Zen practice, designed to help home practitioners maintain the forms of monastic life.

**Core product thesis:** "The schedule is the teacher." The app holds the ceremonial container so practitioners don't have to reconstruct it alone at home after retreat.

**Target users:** Home practitioners, retreat returnees, people who can't attend in-person sangha.

**The user is called:** Shravaka (Sanskrit: "hearer/listener").

**Starting tradition:** American Soto/Rinzai Zen, beginning with SFZC and ZCD.

---

## Live URL & Deployment

- **Live:** https://khertel377.github.io/great-vows/schedule.html
- **Repo:** https://github.com/khertel377/great-vows
- **Deployment:** GitHub Pages, main branch, root. Pushes go live in ~60 seconds.
- **Git credentials:** osxkeychain configured. `git push` requires no token entry.

---

## Product Vision

### The Train
The schedule is the spine. The train runs whether you're on it or not. You tune in — you don't start it.

**Key metaphors:**
- Temple bell / horarium — the SOURCE metaphor
- Radio broadcast — "already running" quality
- Swiss railway clock — precision without negotiation
- Japanese departures board — visual language for schedule display

### The Horarium
Full daily schedule on real clock time. Two quiet periods bookend the night:
- `quiet-night`: 10:00 PM → midnight
- `quiet-morning`: midnight → 4:30 AM (wake-up bell)

### The Form Factor
The placed device is the key insight. Phone on a stand in front of the cushion becomes a ritual object. Kevin carries the "stupa" (phone + stand) with him — opens it at the altar, sets it aside when using the phone for other things, returns to it.

**Three display modes:**
1. Portrait phone in hand
2. Landscape phone/iPad in stand — placed mode
3. Ambient/shelf — always-on, glanceable

---

## The Three Schedule Modes

The app supports three intensity tiers. **Standard is the current prototype baseline.** Mode switching is a future UI feature — for now Standard is hardcoded.

Sources cross-referenced: Typical Practice Period handbook, Green Dragon Temple Spring PP 2024, Green Gulch Farm Summer Daily Schedule, Zenshinji (Tassajara) Fall 2024 PP.

---

### Casual — "Home Practice"
The practitioner who sits in the morning and evening but lives a normal day in between. Zazen bookends, meal rhythms, no soji or study hall. Work period is simply "your day."

```
5:10  Han
5:20  Zazen (includes kinhin)
6:20  Morning Service
6:50  Breakfast
8:00  Your Day
12:00 Noon Meal
1:00  Your Day
5:15  Zazen (includes kinhin)
5:50  Evening Service
6:10  Dinner
9:00  Quiet / Lights out
```

---

### Standard — "Practice Period" ← CURRENT PROTOTYPE
Full monastic day. GGF/GDT consensus schedule. Includes study hall, soji, work periods with meeting ceremony, bath/personal time, full evening zazen block.

```
4:30  Wake-up bell (inkan circuit)
4:45  Han
5:00  Zazen (includes kinhin at 5:40)
6:30  Morning Service
7:00  Soji
7:20  Breakfast
8:10  Study Hall
9:10  Work Period (morning — begins with work meeting drum + incense)
12:15 Mid-day Service
12:30 Lunch
1:15  Work Period (afternoon — begins with work meeting drum + incense)
3:00  Bath / Exercise / Personal
5:15  Zazen (includes kinhin)
5:50  Evening Service
6:00  Dinner
7:30  Zazen (includes kinhin)
8:50  Three Refuges
9:00  Firewatch / Quiet
```

**Notes on Standard periods:**
- Zazen and kinhin are one continuous sitting period — kinhin is the middle, not a break. No need to split in UI.
- Work meeting is the first 10-15 min of each work block: drum pattern from zendo deck, incense offering, community circle. Embedded in work period, not a separate row.
- Soji is 20 min community cleaning swarm, ended by the railroad bell.
- Meals are half meal, half personal time. Meal bell calls you in, chant before eating, then your own pace.
- Bath/Exercise/Personal = Tassajara's "personal time" gap between afternoon work and evening zazen. Human and necessary.
- Three Refuges closes the evening zazen block before firewatch.

---

### Intensive — "Sesshin"
Zenshinji-style. Second full morning sitting block after study. Work compressed or absent. Rest periods replace personal time. Every gap is sitting or service.

```
4:25  Wake-up bell
4:50  Han
5:00  Zazen (includes kinhin)
6:30  Morning Service
7:00  Soji
7:20  Breakfast
8:20  Rest
9:20  Zazen (includes kinhin)
11:20 Noon Service
11:30 Lunch
1:30  Rest
2:40  Zazen (includes kinhin)
3:50  Tea
4:20  Rest
4:30  Zazen (includes kinhin)
5:50  Evening Service
6:00  Supper
6:50  Rest
7:30  Zazen (includes kinhin)
8:55  Three Refuges / End
9:00  Firewatch / Quiet
```

---

## The Bell & Percussion System

Seven instruments. Each has a distinct material, social register, and moment. From most sacred to most functional:

| Instrument | Character | Moment | Notes |
|---|---|---|---|
| **Inkan** | Japanese hand bell, traveling | 4:30 wake-up circuit | Student runs through all buildings, starts in kitchen ("wake up, oven spirits!"), ends ~4:40. Intimate — outside your door in the dark. |
| **Han** | Wood block post, struck pattern | 15 min before zazen (4:45) | Accelerating pattern draws you in. Echo-han: second student on far grounds echoes the primary han by ear to extend range through forest. Our phone network is literally echo-han. |
| **Densho** | Large hanging bell, ceremonial | Period transitions, service opening | Already in app. |
| **Meal bell** | Iron, Japanese, sacred, precise | Meals ready | Shape like the Rebel Alliance symbol, cast iron. Measured striking — a signal and a song. More ceremony than function. |
| **Railroad bell** | Western, rope-and-pulley, brass | Work meeting in 5 min (first ring); end of soji; end of work period (second ring) | Pure function. Clang clang clang. No ceremony. Heard across grounds. |
| **Work meeting drum** | Taiko on zendo deck | Start of work meeting only | Heartbeat pattern accelerating: *Bom bom. Bom bom. Bom bom bom bom bmmmbm. Bom bom!* Then incense offering begins. Candidate for watch haptic pattern. |
| **Firewatch clappers** | Hyoshigi (wooden clappers) | 9:00 lights-out circuit | Walking rhythm through grounds. Day ends not with a gong but with footsteps. |

### Koten — Time-Telling System
The koten (時点) announces the time via drum strikes and bell strikes:
- **Drum strikes** = the hour (1–12)
- **Bell strikes** = which 20-minute segment of the hour (0, 1, 2, or 3)
  - 0 bells = top of the hour (:00)
  - 1 bell = first segment (:01–:20)
  - 2 bells = second segment (:21–:40)
  - 3 bells = third segment (:41–:59)

So 4:30 wake-up = **4 drums + 2 bells**. Repeated 3 times.
Future: generate the correct koten pattern programmatically for any schedule time.

**Sound side quest status:**
- ✅ Han — in app
- ✅ Densho — in app
- ✅ Koten + shinrei (inkan) — extracted from Eiheiji recording, in `audio/eiheiji-clips/`
- 🔍 Meal bell — between ship's bell and rin bowl, may need field recording
- 🔍 Railroad bell — literal railroad bell, Freesound likely
- 🔍 Work meeting drum — unique pattern, worth recording; also candidate for watch haptic
- 🔍 Hyoshigi clappers — kaishaku-clappers-meal.m4a extracted from Eiheiji, confirm usability

---

## Eiheiji Reference Recording

**The Way of Eiheiji** — Folkways FR 8980 / Smithsonian Folkways 2000
Recorded Eiheiji, Fukui Prefecture, Japan, 1957.
Direct audio: `https://terebess.hu/zen/szoto/The_Way_Of_Eiheiji.m4a`
Reference page: `https://terebess.hu/zen/szoto/Eiheiji.html`
Timestamp map: `eiheiji-timestamp-map.md` in project root

**Extracted clips** — `audio/eiheiji-clips/`:
- `koten-time-drum-gong.m4a` — 1m20s, koten time-telling sequence (4 drums + 2 bells × 3) then shinrei hand bell enters at 1:28. This is the complete wake-up soundscape in one clip.
- `shinrei-hand-bell.m4a` — 15s, hand bell with time drum bleed
- `dai-kaijo-end-zazen.m4a` — 18s, end-of-zazen metal gong
- `breakfast-bells-dai-rai.m4a` — 1m45s, breakfast bells including thunder drum
- `kaishaku-clappers-meal.m4a` — 2m30s, wooden clappers in meal ceremony (firewatch candidate)
- `konsho-evening-bell.m4a` — 2m, evening bell with rain on tile roof
- `fire-protection-mokugyo.m4a` — 2m30s, driving mokugyo pattern (work meeting drum reference)

**Key insight:** `koten-time-drum-gong.m4a` already contains the complete wake-up sequence in correct order — koten announces the time (0:00–1:27), then hand bell circuit begins (1:28 onward). No stitching needed for prototype.

**Waveform navigation hack:** Silence gaps and amplitude envelope changes reveal all edit points visually in Adobe Audition — much faster than blind listening. Candidate technique for future alignment pipeline pre-segmentation step.

**Audio restoration tools in Audition:**
- Click/Pop Eliminator — for crackles on bell sustains. Scan first, then tune Sensitivity and Discrimination.
- Heal Selection (Shift+U) — surgical single-moment repair. Select just the crackle, hit Shift+U.
- Noise Reduction (process) — for tape hiss. Capture noise print from silent section first.
- DeNoise — ML-based, no noise print needed. Good for consistent 1957 noise floor.

---

## Tech Stack

- Pure HTML/CSS/JS — `index.html`, `schedule.html`
- JSON data: `chantbook.json`, `sanghas/sfzc.json`, `sanghas/zcd.json`
- Audio: MP3/MP4 served directly from repo (all files under 25MB, total ~130MB)
- Local dev: `npx serve .` at localhost:3000 (Python server retired — required for HTTP range requests / MP4 seeking)
- Git: main branch, osxkeychain credential helper
- Claude Code in Terminal for execution

**Project location:** `/Users/kevin/Desktop/great-vows/`

---

## File Structure

```
great-vows/
  index.html                ← chanting/service app
  schedule.html             ← horarium (substantially complete)
  great-vows-state-doc.md   ← THIS FILE — one canonical state doc, kebab-case, overwrite in place
  eiheiji-timestamp-map.md  ← Eiheiji recording reference
  chantbook.json
  sanghas/
    sfzc.json
    zcd.json
  audio/SFZC/               ← NOTE: capital SFZC — Linux/GitHub Pages case-sensitive
    Great_Vows.mp3
    MorningService_Monday.mp4
    MorningService_Tuesday.mp4
    MorningService_Wednesday.mp4
    MorningService_Thursday.mp4
    Full_Moon_Ceremony.mp4
    One_Day_Sitting.mp4
    temple_sounds-the_han.mp3
    temple_sounds-the_densho_bell.mp3
    temple_sounds-opening_chant.mp3
  audio/SFZC/clips/
  audio/eiheiji-clips/      ← extracted from Eiheiji recording
    koten-time-drum-gong.m4a
    shinrei-hand-bell.m4a
    dai-kaijo-end-zazen.m4a
    breakfast-bells-dai-rai.m4a
    kaishaku-clappers-meal.m4a
    konsho-evening-bell.m4a
    fire-protection-mokugyo.m4a
  audio/The_Way_Of_Eiheiji.m4a  ← full source recording
  tools/
    align.py
    align_service.py
    extract_clip.py
    merge_clip_alignment.py
    correct_timestamp.py
    apply_corrections.py
    beat_align.py
  README.md
  .gitignore
```

---

## schedule.html — Current State

### What's working
- Live clock (Cormorant serif, HH:MM:SS, 12h format)
- Real-time schedule, proportional row heights (`28 + 6 * sqrt(durationMinutes)`)
- Past/now/future period states with correct opacity
- Continuous cross drifting proportionally through each row in real time
- All schedule gaps closed — continuous chain, no no-man's-land
- Cross pins to bottom of last period's row if gap ever encountered
- Zoom lock — `user-scalable=no` on viewport meta ✅
- Wake lock — WakeLock IIFE with visibility restore ✅
- SCHEDULE array updated to Standard Practice Period baseline ✅

### Current SCHEDULE array (Standard mode, as implemented)
```javascript
const SCHEDULE = [
  { id: 'quiet-morning',   time: [0,0],   end: [4,30],  name: 'Quiet',                 type: 'quiet', hasService: false },
  { id: 'wake-up-bell',    time: [4,30],  end: [4,45],  name: 'Wake-up Bell',           type: 'bell',  hasService: false },
  { id: 'han',             time: [4,45],  end: [5,0],   name: 'Han',                    type: 'bell',  hasService: false },
  { id: 'zazen-morning',   time: [5,0],   end: [6,30],  name: 'Zazen',                  type: 'zazen', hasService: false },
  { id: 'morning-service', time: [6,30],  end: [7,0],   name: 'Morning Service',        type: 'chant', hasService: true  },
  { id: 'soji',            time: [7,0],   end: [7,20],  name: 'Soji',                   type: 'work',  hasService: false },
  { id: 'breakfast',       time: [7,20],  end: [8,10],  name: 'Breakfast',              type: 'meal',  hasService: false },
  { id: 'study-hall',      time: [8,10],  end: [9,10],  name: 'Study Hall',             type: 'study', hasService: false },
  { id: 'work-morning',    time: [9,10],  end: [12,15], name: 'Work Period',            type: 'work',  hasService: false },
  { id: 'midday-service',  time: [12,15], end: [12,30], name: 'Mid-day Service',        type: 'chant', hasService: false },
  { id: 'lunch',           time: [12,30], end: [13,15], name: 'Lunch',                  type: 'meal',  hasService: false },
  { id: 'work-afternoon',  time: [13,15], end: [15,0],  name: 'Afternoon Work',         type: 'work',  hasService: false },
  { id: 'personal',        time: [15,0],  end: [17,15], name: 'Bath / Rest / Personal', type: 'rest',  hasService: false },
  { id: 'zazen-evening',   time: [17,15], end: [17,50], name: 'Zazen',                  type: 'zazen', hasService: false },
  { id: 'evening-service', time: [17,50], end: [18,0],  name: 'Evening Service',        type: 'chant', hasService: true  },
  { id: 'dinner',          time: [18,0],  end: [19,30], name: 'Dinner',                 type: 'meal',  hasService: false },
  { id: 'zazen-night',     time: [19,30], end: [20,50], name: 'Zazen',                  type: 'zazen', hasService: false },
  { id: 'three-refuges',   time: [20,50], end: [21,0],  name: 'Three Refuges',          type: 'chant', hasService: false },
  { id: 'firewatch',       time: [21,0],  end: [22,0],  name: 'Firewatch',              type: 'quiet', hasService: false },
  { id: 'quiet-night',     time: [22,0],  end: [24,0],  name: 'Quiet',                  type: 'quiet', hasService: false },
];
```

**serviceId routing:** `morning-service` and `evening-service` compute `serviceId` dynamically on every tick based on current day of week — no static hardcoding.

### Quiet mode
```js
{ id: 'quiet-night',   time: [22,0], end: [24,0], name: 'Quiet', type: 'quiet', hasService: false },
{ id: 'quiet-morning', time: [0,0],  end: [4,30], name: 'Quiet', type: 'quiet', hasService: false },
```
- `body.quiet-mode` class: full color inversion, `#1a1814` bg, 4s fade
- Midnight treadmill handles the 23:42→00:00 seam seamlessly

### Audio engine
Self-contained `AudioEngine` IIFE on `window._scheduleTick`.
1. **Han** — plays 15 min before any `type: 'zazen'` period, seeks/loops
2. **Ambient service** — MP4 at 0.33 volume, radio-model elapsed seek, 3s crossfade
3. **Period transition bell** — densho on boundary, skips first tick

**API corrections (locked — do not regress):**
- `getScheduleState(new Date())` — requires Date argument
- `state.state === 'during'` not `state.type === 'current'`
- `state.next` not `state.nextPeriod`
- `#sidebar` / `#track` not `.sidebar` / `.track`
- `audio.muted` not `audio.volume` (iOS)

### Mobile portrait layout
- `#sidebar` 50vw, hairline at 50vw, track fills right half
- Now-row font 36px, meta always visible on now-row
- `env(safe-area-inset-bottom)` on vertical bar
- Scroll bounce guard: skip if `window.scrollY < 0`

---

## index.html — Current State

### What's working ✅
- Zoom lock on viewport meta
- WakeLock IIFE with visibility restore
- iOS overlay: dark `#05060f` background matching index.html dark theme (not paper color)
- Overlay subtitle shows service name
- `sessionStorage['gv-audio-unlocked']` shared with schedule.html (same origin)
  - If user tapped schedule.html overlay first → index.html skips overlay, goes directly to loadService
  - If navigating to index.html directly (bookmark) → overlay shows correctly
- `_pendingSeekTime` consumed inside gesture context in `tryAutoLoad → onReady` just before `audioEl.play()`
  - Seek happens in same user gesture context — iOS compliant
- `?service=X&t=Y` parsed after all sangha data loads, finds service across all sanghas, routes correctly

### Known issue to verify tomorrow morning
zazen-morning end time: state doc says 6:30, CC may have set to 6:40 during gap-closing pass. Confirm against live schedule before 6:30 AM.

---

## The Type System (locked)

| Role | Font | Size | Weight | Opacity |
|------|------|------|--------|---------|
| Headline | Cormorant | 48px now / 18px other | 400 | 1.0 |
| Meta | IBM Plex Mono | 10px | 400 | 0.45 |
| Label | Cormorant italic | 13px | 400 | 0.38 |
| Value | IBM Plex Mono | 11px | 400 | 0.5 |
| Institutional | IBM Plex Mono | 8px | 400 | 0.3 |

Two families only. Five roles only. No exceptions.

## The Color System (locked)

- `--ink: #1a1814` — all text, hairlines, structural elements
- `--seal: #B03A2E` — used ONLY on the cross (vertical bar + horizontal mark)
- Background: `#f4f0e8` warm paper + CSS grain overlay
- Quiet mode: `#1a1814` background, paper-toned text inversions
- index.html dark theme: `#05060f` background

---

## Cross Implementation

```js
const elapsed = nowSecs() - periodStartSeconds(period);
const duration = periodEndSeconds(period) - periodStartSeconds(period);
const progress = elapsed / duration;
const markY = rowRect.top + (progress * rowRect.height);
```
`transition: none` always except temporarily during period boundary crossings (450ms, then removed).

---

## Alignment Pipeline

- `stable_whisper` with `--model large` for dense Japanese chants
- `timestampCorrections` kept separate from machine-generated alignment — human corrections persist across re-runs
- Unified single-track teleprompter — stable architecture

**Key chant variants:** `shosaimyo-x3`, `enmei-jukku-x7`, `names-buddhas-ancestors-monday`, `after-dedication-japanese`, `after-dedication-english`

---

## Temple Staff / Voice System

| Role | Domain | Voice |
|------|--------|-------|
| Ino | Schedule, bells | Clipped, Swiss, no negotiation |
| Doshi | Ceremony | Minimal, ceremonial |
| Tanto | Zazen, kinhin | Gruff-warm |
| Tenzo | Meals | Pragmatic, dignified |
| Shika | Work, soji | Grounded, slightly irreverent |

---

## On the Horizon

### Immediate (next CC session)
- Delete stale state docs: `GREAT_VOWS_STATE.md`, `great_vows_state_doc.md`, `schedule copy.html`
- Verify zazen-morning end time (6:30 vs 6:40) against live schedule
- Copy `eiheiji-timestamp-map.md` into project root
- Add `audio/eiheiji-clips/` files to repo and push

### Near term
- Hook up koten/shinrei wake-up clip to 4:30 wake-up-bell period in audio engine
- Sound side quest: meal bell, railroad bell, work meeting drum, hyoshigi confirmation
- Work meeting drum as watch haptic pattern
- Mode switcher UI: Casual / Standard / Intensive
- Weekly schedule layer: day-off on 4th & 9th days
- Sesshin calendar layer: 1, 2, 3, 5, 7-day (Rohatsu)

### Later
- Complete Wednesday and Thursday morning services
- Full Moon Ceremony and One Day Sitting alignment
- Watch as han — haptic bell on wrist
- Landscape placed mode
- Ambient/iPad mode — giant clock, just now + next
- ZCD chant book
- Pull schedule from JSON
- Generative koten: programmatically generate correct drum+bell pattern for any schedule time

---

## Key Principles (do not regress)

1. The page moves down over the course of the day — proportional row heights, protect always
2. The cross has no CSS transition during normal operation
3. Nothing at the far right of any row
4. Five type roles, two families, no exceptions
5. `--seal` red appears exactly twice — bar and mark. Nowhere else.
6. `alignSidebar()` not on every second tick — scroll and minute change only
7. Audio path is `audio/SFZC/` — capital letters, Linux case-sensitive
8. `audio.muted` not `audio.volume` for iOS compatibility
9. `getScheduleState(new Date())` — requires Date argument
10. `state.state === 'during'` not `state.type === 'current'`
11. The cross never disappears — pins to bottom of last period's row if no current period
12. Zazen and kinhin are one period in the UI — do not split
13. Work meeting is embedded in work period — not a separate row
14. One canonical state doc — `great-vows-state-doc.md`, kebab-case, overwrite in place, never duplicate
