# Great Vows — Project State Document
*Updated after schedule canonization, three-mode system, bell taxonomy, iOS fixes, file hygiene, all three mode arrays formalized, Safari 18+ cross jitter fix, sticky now-row architecture, konsho evening bell loop, ambient audio engine, audio dot, git case-sensitivity fix, audio files committed to repo, ambient audio retry logic fix, audio dot alignment fix, Web Audio overnight bell scheduling, midnight reschedule, ambient audio stop bug fix, firewatch split, tick mark full-height fix, Web Audio wall-clock setTimeout fix, period transition polish, time-travel debug tool, mute covers Web Audio path, iOS keepalive, entry overlay z-index fix, ghost hover suppression, meta row tap-only on mobile, full mute system architecture, bell:/bellEnd:/service: field taxonomy, zazen bells, morning service day-keyed playback, elapsed seek, time-travel audio stop/restart, work-afternoon bellEnd migration (March 2026).*

---

## File Hygiene — Read First

### The canonical state doc
There is exactly **one** state doc: `great-vows-state-doc.md` in the project root.

- Naming convention: **kebab-case only** — `great-vows-state-doc.md`
- When updated, **overwrite in place** — no versioned copies, no `_v2`, no `GREAT_VOWS_STATE`, no `great_vows_state_doc`
- If CC sees any other files named similarly — **ignore them and flag to Kevin**

### General file hygiene rules
- No duplicate HTML files — `schedule copy.html` and similar are traps
- One canonical file per purpose. Experiment on a git branch, not a copy.
- Audio path is `audio/sfzc/` — lowercase always. GitHub Pages (Linux) is case-sensitive. macOS git silently ignores case (`core.ignorecase=true` default) — always use `git -c core.ignorecase=false add audio/sfzc/` when adding new audio files.
- Source recordings over 50MB: local only + .gitignore. Extracted clips under 5MB: in repo.

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

**CC session-start ritual:** Read `great-vows-state-doc.md` first, before doing anything. That is the source of truth for current project state, open issues, and conventions.

**State doc authorship split:** CC commits technical sections (file state, audio engine, pending fixes). Chat produces a short addendum at end of every Chat session. Kevin pastes addendum to CC; CC merges and commits. One doc, one commit, both knowledge threads.

**Project Instructions (Claude.ai):** Permanent identity and role only — no versioned content, no schedule, no fix queue. Nothing that can go stale. Kevin pastes state doc at Chat session start.

**Pending for CC section:** At the end of every Chat session addendum, Chat includes a "Pending for CC" list. CC executes those items and clears the list from the state doc after completing them.

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

### Dharma Talk — future period type
An aggregator model, not a host. Centers already produce audio; Great Vows gives existing teachings a ritual container rather than a podcast-browsing experience. Near-term: `dharmaTalk:` field in the horarium accepting a URL or local path. First concrete source: Kokyo's Santa Cruz Zen Center Google Drive archive.

Two architecturally distinct placements:
1. **Intensive/sesshin** — a named Dharma Talk period where the talk *is* the period. Fixed duration, fills the slot.
2. **Study Hall content option** — softer, ambient, supplementing the period rather than defining it. For practitioners without a text in hand.

**Opening sequence (confirm with Kokyo):** Great Vows owns a fixed ritual preamble before any external talk audio begins, restoring the processional context stripped by the podcast model: (1) bell rolldown / densho-style period-open; (2) processional silence — teacher enters, makes offerings, takes seat; (3) seating bells as attendant brings lectern and tea; (4) gassho moment → single click on small mokugyo/inkin — the room's attention hinge; (5) doan announces pre-talk chant — either full *Eihei Koso Hotsuganmon* or short "unsurpassed, penetrating and perfect dharma" verse (two variants, confirm with Kokyo); (6) chant; (7) talk begins into silence. No ambient bed during the talk — only the teacher's voice.

**CC implementation note:** Preamble is a fixed-duration audio sequence (parallel to `service:`). Talk URL seeks with elapsed-position offset accounting for preamble duration — same pattern as `bellEnd: { offsetMs }` but in the forward direction (`offsetMs: +preambleDuration`). Elapsed seek math: `elapsedInTalk = elapsedInPeriod - preambleDurationMs`.

### Dharma Talk content engine — Branching Streams feed network
Great Vows will aggregate dharma talk audio across the Branching Streams affiliate network — ~60 sanghas in the Suzuki Roshi lineage. Two content modes identified: (1) **General/Cross-cutting** — a curated rotation across teachers and centers, functioning like public radio programming for the lineage; (2) **Focused Teacher Mode** — a practitioner follows a single teacher chronologically through their full body of work, potentially across multiple institutions (e.g. Kokyo Henkel across SCZC, SFZC, and his own site). The zoom-level framing: Branching Streams network → single center → single teacher → full archive. Each level is a valid configuration. Focused Teacher Mode is the natural pairing with Intensive schedule mode.

**Infrastructure findings:** SFZC RSS feed (feeds.feedburner.com/SanFranciscoZenCenterPublicLectures) confirmed working — direct AAC URLs on content.jwplatform.com, streams cleanly from GitHub Pages `<audio>` tag, Creative Commons licensed. Google Drive direct links are not viable for `<audio>` streaming (interstitial wall). Squarespace podcast RSS pattern: `[page-url]?format=rss`.

**Files committed:** `sanghas/branching-streams-feeds.csv` (research output), `sanghas/branching-streams-feeds.json` (43 entries: 12 confirmed RSS, 4 unconfirmed, 11 talks-only, 16 none).

**Next steps for this workstream:** Verify 4 unconfirmed feeds (Ocean Gate, Seattle Soto, Twining Vines, Milwaukee). Wire a study hall period in the standard schedule to fetch the SFZC feed, filter by teacher, and play chronologically with elapsed-position seeking — proof of concept for the whole content engine.

---

## The Three Schedule Modes

**Design principle: the frame is constant, the content varies.**

All three modes open and close the same way:
- **Open:** Han → Zazen → Morning Service
- **Close:** Three Refuges → Firewatch/Quiet

The intensity differs in what happens between. Three Refuges is universal — not a Practice Period exclusive. Start and end the day together, regardless of tier.

**Standard is the current prototype baseline.** Mode switching is a future UI feature — for now Standard is hardcoded. Casual and Intensive arrays are ready to drop in when the mode switcher is built.

Sources cross-referenced: Typical Practice Period handbook, Green Dragon Temple Spring PP 2024, Green Gulch Farm Summer Daily Schedule, Zenshinji (Tassajara) Fall 2024 PP.

---

### Casual — "Home Practice"

The practitioner who sits in the morning, moves through their day, and comes home at the end. One zazen period (morning). Evening Service brings the sangha back together. Three Refuges closes the day. The day is yours in between.

**Arc: Wake up together → your day → come home together.**

```javascript
const SCHEDULE_CASUAL = [
  { id: 'quiet-morning',   time: [0,0],   end: [5,10],  name: 'Quiet',               type: 'quiet', hasService: false },
  { id: 'han',             time: [5,10],  end: [5,20],  name: 'Han',                  type: 'bell',  hasService: false, audio: 'audio/sfzc/temple_sounds-the_han.mp3' },
  { id: 'zazen-morning',   time: [5,20],  end: [6,20],  name: 'Zazen',                type: 'zazen', hasService: false, bell: 'audio/sfzc/3_Floor_Bells.mp3', bellEnd: { src: 'audio/sfzc/morning_zazen_end.mp3', offsetMs: -211000 } },
  { id: 'morning-service', time: [6,20],  end: [6,50],  name: 'Morning Service',      type: 'chant', hasService: true  },
  { id: 'breakfast',       time: [6,50],  end: [8,0],   name: 'Breakfast',            type: 'meal',  hasService: false, bell: 'audio/sfzc/eiheiji-breakfast-instruments.mp3' },
  { id: 'your-day',        time: [8,0],   end: [12,0],  name: 'Your Day',             type: 'rest',  hasService: false },
  { id: 'noon-meal',       time: [12,0],  end: [13,0],  name: 'Noon Meal',            type: 'meal',  hasService: false, bell: 'audio/sfzc/eiheiji-breakfast-instruments.mp3' },
  { id: 'your-day-pm',     time: [13,0],  end: [17,50], name: 'Your Day',             type: 'rest',  hasService: false },
  { id: 'evening-service', time: [17,50], end: [18,10], name: 'Evening Service',      type: 'chant', hasService: true,
    service: { default: 'audio/sfzc/evening-service-A.mp3' } },
  { id: 'dinner',          time: [18,10], end: [20,50], name: 'Dinner',               type: 'meal',  hasService: false, bell: 'audio/sfzc/eiheiji-breakfast-instruments.mp3' },
  { id: 'three-refuges',   time: [20,50], end: [21,0],  name: 'Three Refuges',        type: 'chant', hasService: false, bell: 'audio/sfzc/3-refuges.mp3' },
  { id: 'firewatch-bell',     time: [21,0],  end: [21,30], name: 'Firewatch',            type: 'quiet', hasService: false, audio: 'audio/sfzc/konsho-evening-bell.mp3' },
  { id: 'firewatch-clappers', time: [21,30], end: [22,0],  name: 'Firewatch',            type: 'quiet', hasService: false, audio: 'audio/sfzc/firewatch-clappers.mp3' },
  { id: 'quiet-night',     time: [22,0],  end: [24,0],  name: 'Quiet',                type: 'quiet', hasService: false },
];
```

---

### Standard — "Practice Period" ← CURRENT PROTOTYPE

Full monastic day. GGF/GDT consensus schedule. Three zazen periods, full work structure, study hall, soji, bath/personal time, Three Refuges.

```javascript
const SCHEDULE_STANDARD = [
  { id: 'quiet-morning',   time: [0,0],   end: [4,30],  name: 'Quiet',                 type: 'quiet', hasService: false },
  { id: 'wake-up-bell',    time: [4,30],  end: [4,45],  name: 'Wake-up Bell',           type: 'bell',  hasService: false, audio: 'audio/sfzc/koten-and-shinrei-wakeup.mp3' },
  { id: 'han',             time: [4,45],  end: [5,0],   name: 'Han',                    type: 'bell',  hasService: false, audio: 'audio/sfzc/temple_sounds-the_han.mp3' },
  { id: 'zazen-morning',   time: [5,0],   end: [6,30],  name: 'Zazen',                  type: 'zazen', hasService: false, bell: 'audio/sfzc/3_Floor_Bells.mp3', bellEnd: { src: 'audio/sfzc/morning_zazen_end.mp3', offsetMs: -211000 } },
  { id: 'morning-service', time: [6,30],  end: [7,0],   name: 'Morning Service',        type: 'chant', hasService: true,
    service: { mon: 'audio/sfzc/MorningService_Monday.mp4', tue: 'audio/sfzc/MorningService_Tuesday.mp4', wed: 'audio/sfzc/MorningService_Wednesday.mp4', thu: 'audio/sfzc/MorningService_Thursday.mp4',
               default: 'audio/sfzc/MorningService_Monday.mp4' } },
  { id: 'soji',            time: [7,0],   end: [7,20],  name: 'Soji',                   type: 'work',  hasService: false, bellEnd: { src: 'audio/sfzc/han-opening.mp3', offsetMs: -8000 } },
  { id: 'breakfast',       time: [7,20],  end: [8,10],  name: 'Breakfast',              type: 'meal',  hasService: false, bell: 'audio/sfzc/eiheiji-breakfast-instruments.mp3' },
  { id: 'study-hall',      time: [8,10],  end: [9,10],  name: 'Study Hall',             type: 'study', hasService: false, bell: 'audio/sfzc/study-bell.mp3', bellEnd: 'audio/sfzc/study-bell.mp3' },
  { id: 'work-morning',    time: [9,10],  end: [12,15], name: 'Work Period',            type: 'work',  hasService: false, bell: 'audio/sfzc/railroad-bell.mp3', bellEnd: { src: 'audio/sfzc/temple_sounds-the_densho_bell.mp3', offsetMs: -622000 } },
  { id: 'midday-service',  time: [12,15], end: [12,30], name: 'Mid-day Service',        type: 'chant', hasService: false,
    bell: 'audio/sfzc/midday-service-start.mp3',
    service: { default: 'audio/sfzc/midday-service.mp3' } },
  { id: 'lunch',           time: [12,30], end: [13,15], name: 'Lunch',                  type: 'meal',  hasService: false, bell: 'audio/sfzc/eiheiji-breakfast-instruments.mp3' },
  { id: 'work-afternoon',  time: [13,15], end: [15,0],  name: 'Afternoon Work',         type: 'work',  hasService: false, bell: 'audio/sfzc/railroad-bell.mp3', bellEnd: { src: 'audio/sfzc/railroad-bell.mp3', offsetMs: -300000 } },
  { id: 'personal',        time: [15,0],  end: [17,15], name: 'Personal Time',          type: 'rest',  hasService: false, bellEnd: { src: 'audio/sfzc/temple_sounds-the_han.mp3', offsetMs: -847000 } },
  { id: 'zazen-evening',   time: [17,15], end: [17,50], name: 'Zazen',                  type: 'zazen', hasService: false, bell: 'audio/sfzc/3_Floor_Bells.mp3', bellEnd: { src: 'audio/sfzc/end-of-zazen-before-service.mp3', offsetMs: -15816 } },
  { id: 'evening-service', time: [17,50], end: [18,0],  name: 'Evening Service',        type: 'chant', hasService: true,
    service: { default: 'audio/sfzc/evening-service-A.mp3' } },
  { id: 'dinner',          time: [18,0],  end: [19,30], name: 'Dinner',                 type: 'meal',  hasService: false, bell: 'audio/sfzc/eiheiji-breakfast-instruments.mp3', bellEnd: { src: 'audio/sfzc/temple_sounds-the_han.mp3', offsetMs: -847000 } },
  { id: 'zazen-night',     time: [19,30], end: [20,50], name: 'Zazen',                  type: 'zazen', hasService: false, bell: 'audio/sfzc/3_Floor_Bells.mp3' },
  { id: 'three-refuges',   time: [20,50], end: [21,0],  name: 'Three Refuges',          type: 'chant', hasService: false, bell: 'audio/sfzc/3-refuges.mp3' },
  { id: 'firewatch-bell',     time: [21,0],  end: [21,30], name: 'Firewatch',              type: 'quiet', hasService: false, audio: 'audio/sfzc/konsho-evening-bell.mp3' },
  { id: 'firewatch-clappers', time: [21,30], end: [22,0],  name: 'Firewatch',              type: 'quiet', hasService: false, audio: 'audio/sfzc/firewatch-clappers.mp3' },
  { id: 'quiet-night',     time: [22,0],  end: [24,0],  name: 'Quiet',                  type: 'quiet', hasService: false },
];
```

**Notes:**
- Zazen and kinhin are one continuous period — kinhin is the middle, not a break. No split in UI.
- Work meeting is first 10-15 min of each work block — drum, incense, circle. Embedded, not a separate row.
- Soji is 20 min community cleaning swarm, ended by railroad bell.
- Meals are half meal, half personal time.
- Bath/Exercise/Personal = Tassajara's human gap between afternoon work and evening zazen.
- serviceId on morning-service and evening-service computed dynamically on every tick — no static hardcoding.

---

### Intensive — "Sesshin"

Zenshinji-style. Five or six zazen periods. Work compressed or absent. Rest replaces personal time. Every gap is sitting or service.

```javascript
const SCHEDULE_INTENSIVE = [
  { id: 'quiet-morning',    time: [0,0],   end: [4,25],  name: 'Quiet',            type: 'quiet', hasService: false },
  { id: 'wake-up-bell',     time: [4,25],  end: [4,50],  name: 'Wake-up Bell',     type: 'bell',  hasService: false, audio: 'audio/sfzc/koten-and-shinrei-wakeup.mp3' },
  { id: 'han',              time: [4,50],  end: [5,0],   name: 'Han',              type: 'bell',  hasService: false, audio: 'audio/sfzc/temple_sounds-the_han.mp3' },
  { id: 'zazen-1',          time: [5,0],   end: [6,30],  name: 'Zazen',            type: 'zazen', hasService: false, bell: 'audio/sfzc/3_Floor_Bells.mp3', bellEnd: { src: 'audio/sfzc/morning_zazen_end.mp3', offsetMs: -211000 } },
  { id: 'morning-service',  time: [6,30],  end: [7,0],   name: 'Morning Service',  type: 'chant', hasService: true  },
  { id: 'soji',             time: [7,0],   end: [7,20],  name: 'Soji',             type: 'work',  hasService: false, bellEnd: { src: 'audio/sfzc/han-opening.mp3', offsetMs: -8000 } },
  { id: 'breakfast',        time: [7,20],  end: [8,20],  name: 'Breakfast',        type: 'meal',  hasService: false, bell: 'audio/sfzc/eiheiji-breakfast-instruments.mp3' },
  { id: 'rest-1',           time: [8,20],  end: [9,20],  name: 'Rest',             type: 'rest',  hasService: false },
  { id: 'zazen-2',          time: [9,20],  end: [11,20], name: 'Zazen',            type: 'zazen', hasService: false, bell: 'audio/sfzc/3_Floor_Bells.mp3' },
  { id: 'noon-service',     time: [11,20], end: [11,30], name: 'Noon Service',     type: 'chant', hasService: false },
  { id: 'lunch',            time: [11,30], end: [13,30], name: 'Lunch',            type: 'meal',  hasService: false, bell: 'audio/sfzc/eiheiji-breakfast-instruments.mp3' },
  { id: 'rest-2',           time: [13,30], end: [14,40], name: 'Rest',             type: 'rest',  hasService: false },
  { id: 'zazen-3',          time: [14,40], end: [15,50], name: 'Zazen',            type: 'zazen', hasService: false, bell: 'audio/sfzc/3_Floor_Bells.mp3' },
  { id: 'tea',              time: [15,50], end: [16,20], name: 'Tea',              type: 'meal',  hasService: false },
  { id: 'rest-3',           time: [16,20], end: [16,30], name: 'Rest',             type: 'rest',  hasService: false },
  { id: 'zazen-4',          time: [16,30], end: [17,50], name: 'Zazen',            type: 'zazen', hasService: false, bell: 'audio/sfzc/3_Floor_Bells.mp3' },
  { id: 'evening-service',  time: [17,50], end: [18,0],  name: 'Evening Service',  type: 'chant', hasService: true,
    service: { default: 'audio/sfzc/evening-service-A.mp3' } },
  { id: 'dinner',           time: [18,0],  end: [19,30], name: 'Dinner',           type: 'meal',  hasService: false, bell: 'audio/sfzc/eiheiji-breakfast-instruments.mp3', bellEnd: { src: 'audio/sfzc/temple_sounds-the_han.mp3', offsetMs: -847000 } },
  { id: 'rest-4',           time: [19,30], end: [19,30], name: 'Rest',             type: 'rest',  hasService: false },
  { id: 'zazen-5',          time: [19,30], end: [20,55], name: 'Zazen',            type: 'zazen', hasService: false, bell: 'audio/sfzc/3_Floor_Bells.mp3' },
  { id: 'three-refuges',    time: [20,55], end: [21,0],  name: 'Three Refuges',    type: 'chant', hasService: false, bell: 'audio/sfzc/3-refuges.mp3' },
  { id: 'firewatch-bell',     time: [21,0],  end: [21,30], name: 'Firewatch',        type: 'quiet', hasService: false, audio: 'audio/sfzc/konsho-evening-bell.mp3' },
  { id: 'firewatch-clappers', time: [21,30], end: [22,0],  name: 'Firewatch',        type: 'quiet', hasService: false, audio: 'audio/sfzc/firewatch-clappers.mp3' },
  { id: 'quiet-night',      time: [22,0],  end: [24,0],  name: 'Quiet',            type: 'quiet', hasService: false },
];
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
- **Drum strikes** = the hour (1–12)
- **Bell strikes** = which 20-minute segment (0, 1, 2, or 3)
  - 0 bells = top of the hour (:00)
  - 1 bell = first segment (:01–:20)
  - 2 bells = second segment (:21–:40)
  - 3 bells = third segment (:41–:59)

4:30 wake-up = **4 drums + 2 bells**, repeated 3 times.
Future: generate correct koten pattern programmatically for any schedule time.

**Sound side quest status:**
- ✅ Han — in app (`temple_sounds-the_han.mp3`)
- ✅ Densho — in app
- ✅ Koten + shinrei wake-up — `audio/sfzc/koten-and-shinrei-wakeup.mp3` (polished, ready)
- ✅ Meal bell — `audio/sfzc/eiheiji-breakfast-instruments.mp3`; `bell:` on breakfast, lunch, dinner (Standard, Casual, Intensive)
- ✅ 3 Floor Bells — `audio/sfzc/3_Floor_Bells.mp3`; `bell:` on all zazen periods (start); Standard, Casual, Intensive. Also fires as third event in zazen midpoint sequence (after kinhin).
- ✅ Morning zazen end — `audio/sfzc/morning_zazen_end.mp3`; `bellEnd:` on `zazen-morning` (Standard, Casual) and `zazen-1` (Intensive)
- ✅ End of zazen before service — `audio/sfzc/end-of-zazen-before-service.mp3`; `bellEnd: { offsetMs: -15816 }` on `zazen-evening`; fires at 17:49:44 leading into evening service
- ✅ Railroad bell — `audio/sfzc/railroad-bell.mp3`; `bell:` on `work-morning` (9:10) and `work-afternoon` (13:15); `bellEnd: { offsetMs: -300000 }` on `work-afternoon` fires at 14:55; fully array-driven; Standard only
- ✅ Study bell — `audio/sfzc/study-bell.mp3`; `bell:` (8:10 open) and `bellEnd:` (9:10 close) on `study-hall`. Chant sequence wired: opening chant at 8:10 + 8271ms; closing bell at 9:05; closing chant at 9:05 + 8271ms. Hardcoded offsets in `scheduleUpcomingBells()`.
- ✅ Three Refuges — `audio/sfzc/3-refuges.mp3`; `bell:` on `three-refuges` period; Standard, Casual, Intensive
- ✅ Zazen midpoint sequence — densho at period midpoint, kinhin clapper at midpoint + 5min, floor bells at midpoint + 5min + 990ms + 30s. Fires for zazen periods > 42 min (`zazen-morning` 90 min, `zazen-night` 80 min; `zazen-evening` 35 min skipped). Scheduled via `scheduleUpcomingBells()`.
- ✅ Midday service — `bell: midday-service-start.mp3` + `service: { default: midday-service.mp3 }` on `midday-service`; Standard only
- ✅ Evening service — `service: { default: evening-service-A.mp3 }` on `evening-service`; Standard, Casual, Intensive. No day-keyed variants yet.
- 🔍 Work meeting drum — unique pattern, worth recording; watch haptic candidate
- 🎙 Hyoshigi clappers — needs dedicated edit/recording for `firewatch-clappers.mp3` (wired in schedule, file pending)

---

## Eiheiji Reference Recording

**The Way of Eiheiji** — Folkways FR 8980 / Smithsonian Folkways 2000
Recorded Eiheiji, Fukui Prefecture, Japan, 1957.
Direct audio: `https://terebess.hu/zen/szoto/The_Way_Of_Eiheiji.m4a`
Reference page: `https://terebess.hu/zen/szoto/Eiheiji.html`
Timestamp map: `eiheiji-timestamp-map.md` in project root
Source file: local only — `audio/The_Way_Of_Eiheiji.m4a` in .gitignore (80MB)

**Extracted clips** — `audio/eiheiji-clips/` (in repo, all under 2.5MB):
- `koten-time-drum-gong.m4a` — 1m20s, koten sequence then shinrei enters at 1:28
- `shinrei-hand-bell.m4a` — 15s, hand bell isolated
- `dai-kaijo-end-zazen.m4a` — 18s, end-of-zazen metal gong
- `breakfast-bells-dai-rai.m4a` — 1m45s, breakfast bells + thunder drum
- `kaishaku-clappers-meal.m4a` — 2m30s, wooden clappers (firewatch candidate)
- `konsho-evening-bell.m4a` — 2m, evening bell with rain on tile roof
- `fire-protection-mokugyo.m4a` — 2m30s, driving mokugyo (work meeting drum reference)

**Waveform navigation hack:** Silence gaps and amplitude envelope changes reveal edit points visually in Audition — much faster than blind listening. Future pipeline: pre-segmentation step using librosa silence detection before stable_whisper alignment.

---

## Tech Stack

- Pure HTML/CSS/JS — `index.html`, `schedule.html`
- JSON data: `chantbook.json`, `sanghas/sfzc.json`, `sanghas/zcd.json`
- Audio: MP3/MP4 served directly from repo (all files under 25MB)
- Local dev: `npx serve .` at localhost:3000
- Git: main branch, osxkeychain credential helper
- Claude Code in Terminal for all file execution

**Project location:** `/Users/kevin/Desktop/great-vows/`

---

## File Structure

```
great-vows/
  index.html                     ← chanting/service app
  schedule.html                  ← horarium
  great-vows-state-doc.md        ← THIS FILE — one canonical state doc
  eiheiji-timestamp-map.md       ← Eiheiji recording reference
  chantbook.json
  sanghas/
    sfzc.json
    zcd.json
  audio/sfzc/
    koten-and-shinrei-wakeup.mp3  ← polished wake-up bell audio, ready
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
  audio/sfzc/clips/
  audio/eiheiji-clips/
    koten-time-drum-gong.m4a
    shinrei-hand-bell.m4a
    dai-kaijo-end-zazen.m4a
    breakfast-bells-dai-rai.m4a
    kaishaku-clappers-meal.m4a
    konsho-evening-bell.m4a
    fire-protection-mokugyo.m4a
  tools/
    align.py
    align_service.py
    extract_clip.py
    merge_clip_alignment.py
    correct_timestamp.py
    apply_corrections.py
    beat_align.py
  README.md
  .gitignore                     ← includes audio/The_Way_Of_Eiheiji.m4a
```

---

## schedule.html — Current State

### What's working
- Live clock, proportional row heights, past/now/future states
- Continuous cross, no no-man's-land, pins to bottom of last row if gap
- Zoom lock ✅
- Wake lock ✅
- SCHEDULE array is `SCHEDULE_STANDARD` — 20 periods, all abutting (0:00–24:00) ✅
- Audio dots on wired periods ✅ — gold dot on wake-up-bell, han, morning-service, evening-service
- serviceId computed dynamically on every tick ✅
- sessionStorage audio unlock shared between schedule.html and index.html ✅
- try/catch with console logging on every `.play()` call ✅
- AudioContext health check on every tick — resumes if suspended ✅
- Thursday Enter button hidden (service audio not yet available) ✅
- Cross on rAF loop, geometry cached in `_connGeo` — no `getBoundingClientRect()` per frame ✅
- Row rects stored as document-space coords (+ scrollY); `_docToVp()` converts back each frame ✅
- Period transition polish ✅ — `--tick-progress` reset to 0 atomically on new now-row; `updateClock()` + `updateSidebar()` called at end of `buildTrack()` (no `--:--` flash); `rAF` scroll-to-now on transition
- `getNow()` shim ✅ — all bare `new Date()` "give me now" calls replaced; `_debugOffset` drives synthetic time for debug tool

### Quiet mode
```js
{ id: 'quiet-night',   time: [22,0], end: [24,0], name: 'Quiet', type: 'quiet', hasService: false },
{ id: 'quiet-morning', time: [0,0],  end: [4,30], name: 'Quiet', type: 'quiet', hasService: false },
```
- `body.quiet-mode` class: full color inversion, `#1a1814` bg, 4s fade
- Midnight treadmill handles the 23:42→00:00 seam seamlessly

### Schedule array field schema

| Field | Type | Purpose |
|-------|------|---------|
| `id` | string | Unique period identifier |
| `time` | [h, m] | Start time |
| `end` | [h, m] | End time |
| `name` | string | Display name |
| `type` | string | `quiet`, `bell`, `zazen`, `chant`, `work`, `study`, `meal`, `rest` |
| `hasService` | bool | Whether Enter button should appear |
| `audio` | string | Ambient loop — plays for duration of period, shown as track dot |
| `bell` | string | One-shot bell — fires once at period start via Web Audio, shown as track dot |
| `bellEnd` | string \| `{ src, offsetMs }` | One-shot bell at period end — or before it when offsetMs is negative. String form: fires at `period.end`. Object form: fires at `period.end + offsetMs`. `-211000` = 3m31s before end (morning zazen end recording). Array-driven, shown as track dot. |
| `service` | `{ mon, tue, wed, thu, default }` | Day-keyed map of service audio files. Resolution: `service[dayKey] \|\| service.default`. `default` covers Fri/Sat/Sun until dedicated recordings exist — currently points to Monday. Missing both key and default → `console.warn` + silence. Played by `tickServiceAudio()`. Shown as track dot. |
| `dharmaTalk` | *(future)* | URL or local path to a dharma talk audio file. Played after a fixed ritual preamble sequence; elapsed seek offsets by preamble duration. Two placements: dedicated talk period (intensive/sesshin) or Study Hall content option. First source: Kokyo / Santa Cruz Zen Center archive. |

`audio:`, `bell:`, `bellEnd:`, and `service:` can coexist on a period. All render a dot; ambient dot pulses when ambient is playing.

### Audio engine
1. **Wake-up bell** — plays `koten-and-shinrei-wakeup.mp3` once when `wake-up-bell` period begins. Uses `wakeupPlaying` flag to prevent re-trigger on every tick.
2. **Han** — plays `temple_sounds-the_han.mp3` starting 15 min before any `type: 'zazen'` period. Seeks/loops.
3. **Ambient service** — MP4 at 0.33 volume, radio-model elapsed seek, 3s crossfade. (index.html path — not schedule.html)
4. **Period transition bell** — densho on boundary, skips first tick.
5. **Service audio** — `tickServiceAudio(currentPeriod)` runs each second from `tick()`. On period change, stops previous, reads `currentPeriod.service[getDayKey()]`, creates a fresh `Audio()` and plays from the beginning. No elapsed seek — schedule.html plays audio; index.html handles aligned chant player. Mon–Thu wired; Fri/Sat/Sun absent keys fall back to silence. `_serviceAudio` / `_servicePeriodId` globals in script #1; covered in `applyMute()` via `typeof` guard. `getDayKey()` uses `getNow()` — debug-aware.

**API corrections (locked — do not regress):**
- `getScheduleState(getNow())` — use `getNow()` not `new Date()` at all call sites
- `state.state === 'during'` not `state.type === 'current'`
- `state.next` not `state.nextPeriod`
- `#sidebar` / `#track` not `.sidebar` / `.track`
- `audio.muted` not `audio.volume` (iOS)

### Mobile portrait layout
- `#sidebar` 50vw, hairline at 50vw, track fills right half
- Now-row font 36px, meta always visible on now-row
- `env(safe-area-inset-bottom)` on vertical bar and both fixed buttons
- Scroll bounce guard: skip if `window.scrollY < 0`
- Mute button: `position: fixed; bottom-right` — `calc(24px + env(safe-area-inset-bottom, 0px))`
- Time-travel button: `position: fixed; bottom-left` — same safe-area formula, mirrored side

### Two script blocks
`schedule.html` has two `<script>` tags. Script #1 contains `tickAmbientAudio`, `scheduleAudioEvent`, and the core tick/audio engine. Script #2 contains the mute button, `isMuted`, and UI controls. `let`/`const` in script #2 are not visible in script #1. Even `var` doesn't help — script #2 hasn't executed yet when script #1's `tick()` fires on page load. **Rule: script #1 must never reference variables declared in script #2.** Script #1 always reads mute state directly from `localStorage.getItem('gv-muted') === '1'`.

**Mute system — complete architecture (all four paths):**
Script #1 owns `_ambientAudio` (ambient period loops) and `_devAudio` (dev tap-to-play). Script #2 `AudioEngine` owns `ambientAudio` (service audio), `hanAudio`, `denshoAudio`, `wakeupAudio`.

`applyMute()` in script #2 covers all six objects:
- `ambientAudio`, `hanAudio`, `denshoAudio`, `wakeupAudio` — direct references (same script)
- `_ambientAudio`, `_devAudio` — via `typeof` guard (cross-script, `let` not on `window`)

New audio creation sets muted state at birth:
- `_ambientAudio` — reads `localStorage.getItem('gv-muted') === '1'` at line 995 (script #1)
- `_devAudio` — reads `localStorage.getItem('gv-muted') === '1'` at creation (script #1)
- `AudioEngine` objects — read `isMuted` at creation (same script)
- Web Audio scheduled bells — reads `localStorage.getItem('gv-muted') === '1'` at fire time (line 1112, script #1)

`firewatch-clappers.mp3` — placeholder, file still pending. Ambient mute works; nothing to mute until file exists.

### Meta row reveal
- **Desktop:** `mouseenter`/`mouseleave` on `.period-row` — sets `data-hover="active"` and `data-hover="neighbor"` on adjacent rows; CSS drives opacity
- **Mobile:** tap-to-toggle, single open — `_showMeta(row)` / `_clearMeta(row)` toggle `meta-visible` class; `_showMeta` closes any previously open row before opening the new one; no auto-dismiss
- `isTouchDevice` detection: `window.matchMedia('(hover: none)').matches` — pointer capability, not UA sniffing
- IntersectionObserver scroll-trigger removed — was auto-revealing meta when row crossed center band; replaced by tap-only
- `_metaObserver` and `_metaDismissTimer` are declared but inert — remove in next cleanup pass

---

## index.html — Current State

### What's working ✅
- Zoom lock on viewport meta
- WakeLock IIFE with visibility restore
- iOS overlay: dark `#05060f` background, subtitle shows service name
- `sessionStorage['gv-audio-unlocked']` shared with schedule.html
- `_pendingSeekTime` consumed inside gesture context — iOS compliant seek
- `?service=X&t=Y` parsed after sangha data loads, routes correctly

---

## The Type System (locked)

| Role | Font | Size | Weight | Opacity |
|------|------|------|--------|---------|
| Headline | Cormorant | 54px now / 20px other | 400 | 1.0 |
| Meta | IBM Plex Mono | 12px | 400 | 0.45 |
| Label | Cormorant italic | 15px | 400 | 0.38 |
| Value | IBM Plex Mono | 12px | 400 | 0.5 |
| Institutional | IBM Plex Mono | 10px | 400 | 0.3 |

Two families only. Five roles only. No exceptions.

## The Color System (locked)

- `--ink: #1a1814` — all text, hairlines, structural elements
- `--seal: #B03A2E` — used ONLY on the cross (vertical bar + horizontal mark)
- Background: `#f4f0e8` warm paper + CSS grain overlay
- Quiet mode: `#1a1814` background, paper-toned text inversions
- index.html dark theme: `#05060f` background
- Audio dot: `#B8860B` dark goldenrod, opacity 0.6

---

## Cross Implementation — Architecture Decision (March 2026)

### What changed
Replaced the fixed overlay + JS positioning system with a CSS sticky now-row.
Deleted ~280 lines: `positionConnector()`, the rAF loop, `alignSidebar()`,
`initSidebarAlignment()`, `_refreshConnGeo()`, `_connGeo`, `clockNaturalTop`,
`clockNaturalBottom`, and all coordinate cache vars.

### Old architecture (removed)
- `#sidebar`: position sticky, contained clock
- `#now-overlay`: position fixed, full viewport
- `#now-bar` / `#now-mark`: position absolute children of overlay
- JS ran at 60fps reading `getBoundingClientRect()` to sync three separate layout contexts
- Root cause of all scroll jitter bugs: read-after-write layout thrash, iOS `scrollY` unreliable during momentum scroll, dynamic viewport geometry invalidating stored coords

### New architecture (current)
- Every `.period-row` is `display: flex` with `.period-left` and `.period-right`
- `.period-row.now` gets `display: grid` (2-column, 4 named rows), `position: sticky; top: 0; background: var(--paper)`
- Clock and info live as direct grid children of the now-row, injected by `buildTrack()`
- Cross is pure CSS: `::before` on `.period-row.now` for the full-height red bar at the column boundary; `::after` on `.period-row.now` for the tick mark (travels full now-row height)
- Zero JS positioning. Browser compositor handles sticky natively.

### Grid layout (now-row only)
```css
.period-row.now {
  display: grid;
  grid-template-columns: 280px 1fr;
  grid-template-areas:
    "clock  name "
    "ampm   meta "
    "next   .    "
    "enter  .    ";
}
```
Six grid children: `.clock-display`, `.clock-meta`, `.sidebar-next`, `.enter-btn`, `.period-name`, `.period-row-meta`.

### Mobile column width — keep in sync
Four values must always match at every breakpoint: `.period-left { width }`,
`.period-row.now { grid-template-columns }`, `.period-row.now::before { left }`, and `.period-row.now::after { left }`.
All four live in the same `mobileStyles` block. If column width changes, update
all four together.

### Key constraints
- `.period-row.now` must have an opaque background (`var(--paper)`) — past rows scroll behind it
- Quiet mode inversion must also invert the now-row background
- The vertical red bar is bounded by now-row height — no full-viewport bar. Accepted tradeoff.
- Tick mark travels top-to-bottom over the period's duration via `--tick-progress` CSS custom property. JS writes a 0–1 float to `.period-row.now` once per second; CSS reads it as `top: calc(var(--tick-progress, 0.1) * 100%)` with `transform: translate(-50%, -50%)` on `.period-row.now::after`. Anchored to `.period-row.now` (not `.period-name`) so it travels the full now-row height. Default 0.1 keeps the mark visible before JS fires on first load.
- "Next" baseline alignment with next period title was removed — grid approach inflated now-row height. `sidebar-next` sits below meta row at fixed `margin-top: 8px` instead.

### Branch
Prototyped on `sticky-now-row` branch. Mobile scroll smoothness is the primary motivation — has not yet been fully validated on new iPhone Safari (pending).

### Do not regress
- No JS positioning of any kind for the cross or clock
- No rAF loops for layout
- No `getBoundingClientRect()` in scroll handlers
- No fixed overlay for the now indicator

---

## Alignment Pipeline

- `stable_whisper` with `--model large` for dense Japanese chants
- `timestampCorrections` kept separate — human corrections persist across re-runs
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
*(Cleared)*

**4:30 wake-up bell overnight test:** Wall-clock setTimeout architecture is in place. First real overnight test was this session. If 4:30 fires cleanly the issue is closed. If not, next suspect is iOS killing the tab under memory pressure — which requires Service Worker + Web Push.

### Ambient audio engine — working
`tickAmbientAudio(currentPeriod)` runs each second from `tick()`.
Compares `currentPeriod.id` to `_ambientPeriodId` — only acts on transitions.
Stops old loop, starts new `Audio()` with `loop = true`.
Any period with an `audio:` field automatically gets ambient playback + track dot.

Current ambient periods:
- `firewatch-bell` (all three mode arrays) → `audio/sfzc/konsho-evening-bell.mp3`
- `firewatch-clappers` (all three mode arrays) → `audio/sfzc/firewatch-clappers.mp3` ← placeholder, file pending

**Retry logic:** `.play()` is blocked by autoplay policy until a user gesture.
When blocked, `_pendingAmbientPlay = true`. Two retry paths:
1. Every `tick()` silently retries if flag is set
2. Any tap retries with console logging
First success clears the flag and lights the dot.
`{ once: true }` pattern was a bug — listener was consumed by entry screen tap
before play block occurred. Persistent listener with flag check is the correct pattern.

**`#ambient-dot`** positioned absolute, anchored to `ampmEl` (position: relative).
Pulses gold (#B8860B, opacity 0.6) while ambient is playing.
Auto-appears on any `audio:`-bearing period — no hardcoding required.

**Night mode flash at Firewatch transition** — known cosmetic quirk. now-row
background flips synchronously; body background transitions asynchronously.
Would need transition-delay on now-row to fix. Not worth the complexity.

### Dev tap-to-play tool — working
Click any `.period-row[data-bell]`, `[data-bell-end]`, or `[data-service]` row to play/pause (or cycle).
Whole row is the tap target; `.audio-dot` is visual only.
`_devAudio` is always a fresh `Audio()` object — no reuse, no play/pause race.
`data-service` resolves day src at `buildTrack()` time — stores resolved string, not the map object.
`data-bell-end` also stores a resolved src string (`p.bellEnd.src` for objects, `p.bellEnd` for plain strings) — same pattern. `bellEnd`-only periods (no `bell:` or `audio:`) get full dot, cursor, and tap support.
Console unlock step removed — tap itself sets `sessionStorage`.
`data-audio` removed from selector — ambient loops (`audio:` field) are not dev-tool tap targets.

**Cycle behavior (bell + bellEnd rows):** `wireAudioDevTool()` uses a `cycleState` Map keyed by `data-period-id` (values: 0 = off, 1 = bell playing, 2 = bellEnd playing). Rows with both `data-bell` and `data-bell-end` cycle bell → bellEnd → off on successive taps. Single-src rows (bell-only, bellEnd-only, service) toggle on/off as before. `onended` resets `cycleState` to 0 — a naturally-finished audio doesn't leave the row stuck mid-cycle. `.playing` class and `_devPlayingRow` dot pulse preserved throughout.

### Web Audio scheduling — working
`unlockAudioContext()` creates `_webAudioCtx` on first user gesture. `scheduleAudioEvent(url, firesAt)` computes `msUntil = firesAt.getTime() - (Date.now() + _debugOffset)` and calls `setTimeout(msUntil)`. At fire time, the callback calls `resumeAudioContext()` (new helper — resumes `_webAudioCtx` if suspended), then fetches, decodes, and plays the buffer immediately via `src.start(0)`. No future AudioContext offset is computed at scheduling time. Immune to AudioContext clock drift over long sessions and overnight context suspension on foreground tabs. `visibilitychange` calls `resumeAudioContext()` via the same helper.

**Midnight reschedule:** `scheduleMidnightReschedule()` sets a `setTimeout` to midnight; when it fires it calls `scheduleUpcomingBells()` for the new day and resets itself. Called once from the overlay tap alongside `scheduleUpcomingBells()`.

**Ambient loops excluded:** `firewatch-bell` and `firewatch-clappers` (`type: 'quiet'`) stay on the `Audio()` retry path — not scheduled here.

**Remaining failure mode:** If iOS kills the tab entirely overnight, scheduled bells are lost — no web app can recover from this. setTimeout drift on a foreground, screen-on tab is negligible (well under 1 second). Next solution class if needed: Service Worker + Web Push.

### Time-travel debug tool — working
`#time-travel-btn` — clock icon, `position: fixed`, bottom-left, mirroring mute button bottom-right. Both use `calc(Npx + env(safe-area-inset-bottom, 0px))`.

Tap opens `#tt-panel` — floating panel with hour/minute/second inputs, AM/PM toggle (`#tt-ampm`), and Go button (`#tt-go`). No `<input type="time">` — unreliable cross-platform. Panel pre-fills with current `getNow()` time including seconds. On Go: calls `unlockAudioContext()` (creates `_webAudioCtx` on desktop where no entry overlay exists), computes `_debugOffset = target - Date.now()`, rebuilds track, reschedules bells.

On cancel (tap button while active): stops `_serviceAudio` and `_bellEndAudio` immediately, nulls `_servicePeriodId` so next tick re-evaluates against real time, clears `_debugOffset`, rebuilds track and reschedules.

`#time-travel-dot` (reuses `.audio-dot` class) pulses gold on the button while debug mode is active.

`getNow()` shim: returns `new Date(Date.now() + _debugOffset)` when offset is set, plain `new Date()` otherwise. All bare `new Date()` call sites use `getNow()`. Bell scheduling uses `Date.now() + _debugOffset` for `msUntil` math. Tick progress uses `(Date.now() + _debugOffset) / 1000` for the now-seconds value.

### Near term
- Mode switcher UI: drop in `SCHEDULE_CASUAL` or `SCHEDULE_INTENSIVE` from this doc
- Weekly schedule layer: day-off on 4th & 9th days
- Sesshin calendar layer: 1, 2, 3, 5, 7-day (Rohatsu)
- Sound side quest: work meeting drum, hyoshigi confirmation
- Work meeting drum as watch haptic pattern
- ~~Study hall chant sequencing~~ ✅ wired: opening chant at 8:10 + bell duration; closing bell at 9:05; closing chant at 9:05 + bell duration. Hardcoded in `scheduleUpcomingBells()`.
- zazen-night end bell — no `bellEnd:` on `zazen-night` yet; night zazen ends without a send-off audio
- Time-travel ghost bell cancellation — `scheduleAudioEvent` stores no timeout handles; stale bells from cancelled time-travel sessions can fire. Fix: accumulate IDs in `_scheduledTimeouts = []`, call `_scheduledTimeouts.forEach(clearTimeout)` at the top of `scheduleUpcomingBells()`. Mute is the current manual escape hatch. Not urgent — narrow exposure in practice — but a clean one-pass fix.
- Kinhin duration (5 min) is a schedule-config candidate — currently hardcoded as `KINHIN_DURATION_MS` in `scheduleUpcomingBells()`; could become a period field or top-level constant
- `bellSequence:` field concept — for chained events (opening chant after study bell, closing chant after closing bell); currently hardcoded in `scheduleUpcomingBells()`
- Confirm `tickBellEndAudio()` on real-time passive passage (page load mid-window) — expected to work via `scheduleUpcomingBells()` on entry overlay tap
- Time-travel scrub mode — scroll gesture on TT panel scrubs time without committing; scrim drops over schedule; Go confirms jump
- Inkin single strike — highest-leverage unacquired sound; covers zazen starting bells, lecture bells, study hall
- Service audio modular architecture — `sanghas/sfzc.json` declares rotating chant slot setlist; schedule page assembles playlist at render time; Wed/Thu files present, unaligned for index.html
- Morning zazen end audio clarification — re-listen with bonsho/densho/han distinction to confirm the GGF recording identity
- Dharma Talk period type — confirm preamble sequence and chant variant with Kokyo; `dharmaTalk:` field in schedule array; preamble-offset elapsed seek

### Later
- Full Moon Ceremony and One Day Sitting alignment
- Watch as han — haptic bell on wrist
- Landscape placed mode
- Ambient/iPad mode — giant clock, just now + next
- ZCD chant book
- Pull schedule from JSON
- Generative koten: programmatic drum+bell pattern for any schedule time

### Untracked audio files — pending triage
- `audio/sfzc/Great_Vows.mp3` — never tracked, not in git history; local only; triage before committing
- `audio/sfzc/temple_sounds-opening_chant.mp3` — "An unsurpassed..." chant; slot reserved at 8:10 study bell offset
- `audio/sfzc/temple_sounds-the_densho_bell.mp3` — renamed from `_denshp_` typo; untracked, stage when ready

### Tracked audio files — new batch (March 2026)
- `audio/sfzc/3-refuges.mp3` — Three Refuges chant; `bell:` on `three-refuges` (Standard, Casual, Intensive)
- `audio/sfzc/opening_chant.mp3` — "An unsurpassed..." English verse; fires at study hall start + 8271ms
- `audio/sfzc/closing_chant.mp3` — "Shu jo, mu hen..." Japanese verse; fires at 9:05 + 8271ms
- `audio/sfzc/eiheiji-breakfast-instruments.mp3` — meal bell (123s); `bell:` on breakfast, lunch, dinner
- `audio/sfzc/end-of-zazen-before-service.mp3` — 15.8s send-off; `bellEnd: { offsetMs: -15816 }` on `zazen-evening`
- `audio/sfzc/midday-service-start.mp3` — 117s; `bell:` on `midday-service`
- `audio/sfzc/midday-service.mp3` — 666s full service; `service: { default: ... }` on `midday-service`
- `audio/sfzc/densho-end-zazen-kinhin.mp3` — 8.4s densho rolldown; fires at zazen midpoint
- `audio/sfzc/kinhin-clapper.mp3` — 1s clapper; fires at midpoint + 5min
- `audio/sfzc/evening-service-A.mp3` — evening service; `service: { default: ... }` on `evening-service` (Standard, Casual, Intensive). No day-keyed variants yet.

---

## Key Principles (do not regress)

1. The page moves down over the course of the day — proportional row heights, protect always
2. The cross has no CSS transition during normal operation
3. Nothing at the far right of any row
4. Five type roles, two families, no exceptions
5. `--seal` red appears exactly twice — the vertical bar (`::before` on `.period-row.now`) and the tick mark (`::after` on `.period-row.now`). Nowhere else.
6. No JS positioning for the cross or clock. No rAF loops for layout. No `getBoundingClientRect()` in scroll handlers. Cross is pure CSS sticky.
7. Audio path is `audio/sfzc/` — lowercase always. GitHub Pages (Linux) is case-sensitive.
8. `audio.muted` not `audio.volume` for iOS compatibility
9. `getScheduleState(new Date())` — requires Date argument
10. `state.state === 'during'` not `state.type === 'current'`
11. The cross never disappears — pins to bottom of last period's row if no current period
12. Zazen and kinhin are one period in the UI — do not split
13. Work meeting is embedded in work period — not a separate row
14. One canonical state doc — `great-vows-state-doc.md`, kebab-case, overwrite in place, never duplicate
15. The frame is constant, the content varies — all modes open and close the same way
16. Three Refuges is universal — every mode, every night, not a Practice Period exclusive
17. Any period with `audio:`, `bell:`, or `bellEnd:` auto-gets a track dot — no hardcoding in `buildTrack()`. `audio:` drives ambient looping; `bell:` fires at period start; `bellEnd:` fires at period end. `bellEnd:` accepts a string (fires at `period.end`) or `{ src, offsetMs }` (fires at `period.end + offsetMs`). Use `offsetMs: -N` for recordings that must begin before the period ends — `morning_zazen_end.mp3` uses `-211000` (3m31s before 6:30 = fires at 6:26:29).
18. `core.ignorecase=true` is macOS git default — always use `git -c core.ignorecase=false add audio/sfzc/` when adding audio files. GitHub Pages is case-sensitive and will 404 silently otherwise.
19. Ambient audio retry: use a persistent click listener with a `_pendingAmbientPlay` flag — never `{ once: true }`. The entry screen tap will consume a one-time listener before the play block occurs.
20. `tickAmbientAudio` tracks `_ambientPeriodId` by `currentPeriod?.id` (not by whether the period has audio). This ensures stop logic fires on every period transition, not just audio→no-audio changes. `_pendingAmbientPlay` is cleared on every transition.
21. Consecutive periods with the same `name` render as one visual label — `buildTrack` detects `isContinuation` (prev period same name) and skips the name text node. Proportional height and audio dot still render. Used by the firewatch-bell / firewatch-clappers split.
22. Use `getNow()` everywhere "give me the current time" is needed — never bare `new Date()`. Use `new Date(someValue)` only for parsing/constructing from a known value. `_debugOffset` is the single source of truth for synthetic time; `msUntil` and tick progress both derive from `Date.now() + _debugOffset`.
23. z-index stack: grain texture overlay = 999 (CSS, line ~61). Entry overlay = 1000 (inline JS). Nothing should sit between these. New fixed elements (mute button, time-travel panel, etc.) belong below 999 or above 1000 intentionally — no values in the 999–1000 gap.
24. `todayAt()` must use `getNow()` as its date basis — never bare `new Date()` inside `todayAt()`. All elapsed math (`elapsedSecs = getNow() - todayAt(...)`) must share the same time basis. Wall-clock `new Date()` breaks elapsed math when `_debugOffset` is active.
25. `loadedmetadata` before seek, `.load()` after constructing `Audio()`. Set `currentTime` inside the `loadedmetadata` event handler — never before. `audio.duration` is NaN until metadata is loaded. `.load()` triggers the metadata fetch on browsers that defer it. This is the required pattern for all seekable audio (`_serviceAudio`, `_bellEndAudio`).
26. Any new audio-triggering UI on desktop must call `unlockAudioContext()` as a first step. Desktop has no entry overlay — `_webAudioCtx` is null until a gesture. `unlockAudioContext()` is idempotent (guards on `if (_webAudioCtx) return`).
27. `bell:` / `bellEnd:` / `service:` is the complete field taxonomy for schedule audio. Before adding a hardcoded entry to `scheduleUpcomingBells()`, ask whether the audio belongs to one of these three types. The only acceptable hardcode is audio that fires at a sub-period offset not expressible as period start or end (currently: none).
28. `bellEnd`-only periods are fully supported throughout the stack — scheduling, dev tool dot, pointer cursor, and tap-to-play. No `bell:` field required. `data-bell-end` stores the resolved src string (same pattern as `data-bell` and `data-service`). `personal` is the canonical example: han fires at −847s, no bell at period open.
29. Any period with both `bell:` and `bellEnd:` automatically gets cycle behavior in the dev tool (bell → bellEnd → off). No per-period handling required — the `cycleState` Map and `hasBoth` check in `wireAudioDevTool()` handle it generically.
30. Kinhin bisects the zazen period. Densho fires at the exact midpoint (`periodStart + floor(duration / 2)`); kinhin clapper at midpoint + 5min; floor bells at midpoint + 5min + 990ms + 30s settle. Fires only for zazen periods > 42 min. Midpoint math means the sequence self-adjusts to any zazen duration — no hardcoded clock times.
