# Great Vows — Project State Document
*Updated after schedule.html design session. Replace previous state doc in project instructions.*

---

## What We're Building

**Great Vows** is a web app for Zen chanting practice — a digital liturgy companion that plays real recordings of morning services while displaying synchronized scrolling text (teleprompter-style), ceremony cues (bows, bells, posture changes), and chant announcements. The experience is like a karaoke/teleprompter for Zen practice, designed to help home practitioners maintain the forms of monastic life.

**Core product thesis:** "The schedule is the teacher." The app holds the ceremonial container so practitioners don't have to reconstruct it alone at home after retreat.

**Target users:** Home practitioners, retreat returnees, people who can't attend in-person sangha.

**The user is called:** Shravaka (Sanskrit: "hearer/listener") — the one who heard the teaching and is trying to live by it.

**Starting tradition:** American Soto/Rinzai Zen, beginning with SFZC (San Francisco Zen Center) and ZCD (Zen Center of Denver).

---

## Product Vision

### The Train
The schedule is the spine of the experience. The train runs whether you're on it or not. You tune in, you don't start it.

**Key metaphors:**
- **Temple bell / horarium** — the SOURCE metaphor. The bell summons. You respond or you don't.
- **Radio broadcast** — "already running" quality. You tune in mid-broadcast.
- **Tide table** — emotional register. Natural law, not human imposition.
- **Japanese departures board** — visual language for the schedule display.
- **Swiss railway clock** — the Landeau energy made physical.

### The Horarium
A full daily schedule running on real clock time. Periods: han, zazen, kinhin, morning service, breakfast, work, noon meal, afternoon work, evening zazen, evening service, dinner, rest, lights out.

### The Form Factor
**The placed device** is the key insight. A phone placed in a small stand on the floor in front of your cushion facing the altar becomes a ritual object. The gesture of placement IS the beginning of the period.

**Three display modes:**
1. **Phone in hand** — portrait, now-playing bar → tap → full service view
2. **Phone/iPad in stand** — landscape, placed mode, departures board, glanceable
3. **Ambient/shelf** — always-on, current period visible across the room

---

## Tech Stack

- Pure HTML/CSS/JS single-page app (`index.html`)
- `schedule.html` — the horarium/train schedule page (substantially complete)
- JSON data files (`chantbook.json`, `sanghas/sfzc.json`, `sanghas/zcd.json`)
- Python tools for audio processing
- Local server: **`npx serve .`** (NOT `python3 -m http.server` — MP4 seeking requires HTTP range requests)
- Git for version control
- **Claude Code** for execution

**Project location:** `/Users/kevin/Desktop/great-vows/`

---

## File Structure

```
great-vows/
  chantbook.json
  schedule.html           ← substantially complete (see status below)
  sanghas/
    sfzc.json             ← SFZC chant book (~5500 lines, 17k+ tokens — read in sections)
    zcd.json
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
      temple_sounds-the_densho_bell.mp3
      temple_sounds-opening_chant.mp3
    sfzc/clips/
  tools/
    align.py
    align_service.py
    extract_clip.py
    merge_clip_alignment.py
    correct_timestamp.py
    apply_corrections.py
    beat_align.py
  index.html
  README.md
  .gitignore
```

**Note on sfzc.json size:** At ~17,500 tokens it exceeds Claude Code's 10,000 token file read limit. Always use `offset` and `limit` parameters. Suggested reads: lines 1–200 for chant structure, lines 4800+ for services array. This is a known architectural issue — future split into per-service files is planned.

---

## schedule.html — Current State

### What's working
- Live clock (Cormorant serif, uniform weight, HH:MM:SS)
- Real-time schedule with proportional row heights (`28 + 6 * sqrt(durationMinutes)`)
- Past/now/future period states with correct opacity
- **The "now" cross:** vertical red bar + horizontal red rect forming a cross at the separator, centered on the current period headline's optical midpoint
- **The "now" system reads left to right:** `3:46:36` → cross → `Afternoon Work` — sidebar and track are one unified sentence
- Sidebar: clock baseline-aligned with now-row period name; "Next / Xh Xm" baseline-aligned with next period name
- `PM`/`AM` meta row below clock, matching track meta type style
- `Next` label in Cormorant italic + mono value, two lines
- Scroll sync: sidebar and track scroll together; cross snaps correctly on each scroll frame
- Period-proportional row heights — the page slowly moves toward the bottom over the course of the day. By evening you're near the bottom. This is intentional and elegant — position on page IS position in the day.
- Enter service button — active during live service periods, links to `index.html?service={serviceId}`
- Hover surfacing: past/future rows lift opacity on hover
- Grain texture on paper background

### The type system (locked — do not drift from these)

| Role | Font | Size | Weight | Opacity | Notes |
|------|------|------|--------|---------|-------|
| Headline | Cormorant | 48px (now) / 18px (other) | 400 | 1.0 | Period names + clock HH:MM:SS |
| Meta | IBM Plex Mono | 10px | 400 | 0.45 | Time, duration, AM/PM. Uppercase for AM/PM. `letter-spacing: 0.05em` |
| Label | Cormorant italic | 13px | 400 | 0.38 | "Next", section rubrics |
| Value | IBM Plex Mono | 11px | 400 | 0.5 | Live countdown data |
| Institutional | IBM Plex Mono | 8px | 400 | 0.3 | Sangha name. `letter-spacing: 0.15em`, uppercase |

**Two families only. Five roles only. No other combinations.**

### The color system (locked)

- `--ink: #1a1814` — all text, hairlines, structural elements
- `--seal: #B03A2E` — Zen stamp red. Used ONLY on: the vertical bar of the cross, the horizontal rect of the cross. Nothing else.
- Background: `#f4f0e8` warm paper with CSS grain overlay

### The cross — implementation notes (hard-won, do not break)

The cross consists of three elements in a single `position: fixed` overlay div (`#now-overlay`, `pointer-events: none`, `z-index: 10`):
- `#now-bar` — vertical, `3px wide`, full now-row height, `background: var(--seal)`
- `#now-mark` — horizontal, `18px wide × 3px tall`, `background: var(--seal)`, centered on period-name optical midpoint Y

Both elements use `getBoundingClientRect()` for positioning — viewport coordinates, scroll-aware automatically.

**Critical:** `transition: none` on both elements during normal operation and scroll. The CSS transition was the root cause of scroll sync bugs — every scroll-frame update triggered a 450ms animation, causing the cross to perpetually chase its target.

Transitions are applied **only temporarily during period boundary transitions:**
```js
function triggerTransition() {
  nowBar.style.transition  = 'top 0.45s ease-in-out, height 0.45s ease-in-out';
  nowMark.style.transition = 'top 0.45s ease-in-out';
  // ... do the swap ...
  setTimeout(() => {
    nowBar.style.transition  = 'none';
    nowMark.style.transition = 'none';
  }, 500);
}
```

### Sidebar alignment — implementation notes

```js
let clockNaturalTop = null;

function initSidebarAlignment() {
  const sidebarContent = document.querySelector('.sidebar-content');
  sidebarContent.style.transform = 'translateY(0)';
  clockNaturalTop = document.querySelector('.clock-display').getBoundingClientRect().top;
}

function alignSidebar() {
  const nowName = document.querySelector('.period-row.now .period-name');
  if (!nowName || clockNaturalTop === null) return;
  const delta = nowName.getBoundingClientRect().top - clockNaturalTop;
  document.querySelector('.sidebar-content').style.transform = `translateY(${delta}px)`;
}
```

- `initSidebarAlignment()` called once after initial render, and on resize
- `alignSidebar()` called on scroll and on minute change — NOT on every second tick (causes oscillation)
- `positionConnector()` called every second tick AND on scroll

### Schedule data (currently hardcoded in schedule.html JS)

```js
const SCHEDULE = [
  { id: 'han',             time: [5,10],  end: [5,20],  name: 'Han',                   type: 'bell',  hasService: false },
  { id: 'zazen-morning',  time: [5,20],  end: [6,35],  name: 'Zazen',                 type: 'zazen', hasService: false },
  { id: 'morning-service-monday', time: [6,40], end: [7,5], name: 'Monday Morning Service', type: 'chant', hasService: true, serviceId: 'morning-service-monday' },
  { id: 'breakfast',      time: [7,10],  end: [7,45],  name: 'Breakfast',              type: 'meal',  hasService: false },
  { id: 'work-morning',   time: [8,0],   end: [12,0],  name: 'Work Period',            type: 'work',  hasService: false },
  { id: 'noon-meal',      time: [12,0],  end: [12,40], name: 'Noon Meal',             type: 'meal',  hasService: false },
  { id: 'work-afternoon', time: [13,0],  end: [17,0],  name: 'Afternoon Work',        type: 'work',  hasService: false },
  { id: 'zazen-evening',  time: [17,15], end: [18,15], name: 'Evening Zazen',         type: 'zazen', hasService: false },
  { id: 'evening-service',time: [18,15], end: [18,45], name: 'Evening Service',       type: 'chant', hasService: true, serviceId: 'evening-service' },
  { id: 'dinner',         time: [18,45], end: [19,30], name: 'Dinner',                type: 'meal',  hasService: false },
  { id: 'rest',           time: [19,30], end: [21,30], name: 'Rest',                  type: 'rest',  hasService: false },
  { id: 'lights-out',     time: [21,30], end: [22,0],  name: 'Lights Out',            type: 'bell',  hasService: false },
];
```

### Off-schedule states (in progress / partially implemented)

**Before first period (before 5:10 AM):**
- All rows future opacity
- No cross — small red dot above first row instead (train approaching)
- Sidebar: clock + `Next / Xh Xm until Han`

**Between periods (gap between scheduled events):**
- Previous period past, next period slightly brighter future (`opacity: 0.82`)
- Cross floats in the gap — bar spans only the gap height, mark at gap midpoint
- Sidebar: clock + `Next / Xm` countdown

**After lights out (after 10 PM):**
- All rows past at very low opacity (`0.18`)
- Cross gone — single closing hairline (`0.5px`) at bottom of last row
- Background slightly warmer (`#f0ebe0`)
- Sidebar: clock + `Tomorrow / in Xh Xm` (counting toward tomorrow's Han)

### Period transition animation (in progress)

When `getScheduleState()` returns a different period ID than previous tick:
1. Outgoing period name shrinks from 48px → 18px, fades (`0.6s ease`)
2. Incoming period name grows from 18px → 48px, appears (`0.6s ease`)
3. Cross slides to new position with temporary `transition: top 0.45s ease-in-out`
4. Transition removed after 500ms so scroll snapping resumes

### Known remaining work on schedule.html

- [ ] Off-schedule states — fully tested (in progress with CC)
- [ ] Period transition animation — fully tested (in progress with CC)
- [ ] Placed mode / landscape detection (specced, not yet implemented)
- [ ] Portrait/mobile layout
- [ ] Pull schedule data from `sfzc.json` or new `schedule.json` instead of hardcoded JS
- [ ] Wire Enter Service button fully to `index.html?service=ID`
- [ ] Scroll: auto-scroll to now-row on page load

### Key design principles established this session (do not regress)

- **The page moves down over the course of the day** — proportional row heights cause this naturally. Protect it in all layout changes.
- **The cross has no CSS transition during normal operation** — only temporarily during period transitions.
- **Nothing at the far right of any row** — scan path is left-anchored. No right-aligned content.
- **Five type roles, two families, no exceptions.**
- **`--seal` red appears exactly twice** — vertical bar, horizontal mark. Nowhere else.
- **`alignSidebar()` does not run on every second tick** — only on scroll and minute change.

---

## index.html — The Chanting/Service App

### Status
Monday and Tuesday morning services substantially complete. Wednesday and Thursday not started.

### UI Architecture
Single unified scrolling track. Chant lines and ceremony cues as `<span class="chant-line">`. No separate overlay.

**Display states:** active (dist 0) → next (+1, 0.4) → near-next (+2, 0.15) → past (-1, 0.2) → near-past (-2, 0.1) → hidden.

**Spotlight mode:** When playing: `next` → 0.15, everything else → 0.

### Service Status

**Monday Morning Service ✓**
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

**Tuesday Morning Service ✓**
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

**Wednesday — Not started (17:20 duration)**
**Thursday — Not started (19:30 duration)**

---

## Alignment Pipeline

**Step 1** — Listen through recording, note chants, start/end times, repeats.
**Step 2** — Update sfzc.json: `recordingChants`, day-specific variants, doshi items, remove old `timestampMap`.
**Step 3** — Extract clips:
```bash
python3 tools/extract_clip.py audio/sfzc/MorningService_X.mp4 [start_s] [end_s] audio/sfzc/clips/chant_day.mp3
```
**Step 4** — Align (use `--model large` for Japanese):
```bash
python3 tools/align.py sanghas/sfzc.json --chant heart-sutra --audio audio/sfzc/clips/heart_sutra_monday.mp3
```
**Step 5** — Merge:
```bash
python3 tools/merge_clip_alignment.py sanghas/sfzc.json morning-service-monday chant-id [start_offset_seconds]
```
**Step 6** — Strip cueIn from chant objects (prevents standalone contamination)
**Step 7** — Sort timestampMap
**Step 8** — Manual corrections for problem sections

---

## Temple Staff / Character System

| Role | Domain | Voice register | Example |
|------|---------|---------------|---------|
| **Ino** | Schedule, bells, transitions | Clipped, Swiss, no negotiation | "5:30. Sit." |
| **Doshi** | Ceremony, service announcements | Minimal, ceremonial, pure form | "Heart Sutra." |
| **Tanto** | Zazen periods, kinhin, practice | Gruff-warm, occasional dharma note | "Just sit." |
| **Tenzo** | Meals, food periods | Pragmatic, dignified, no fuss | "Eat moderately. Clean your bowl." |
| **Shika** | Work period, soji, ordinary life | Grounded, slightly irreverent | "Whatever is in front of you." |

---

## Data Model Notes

### timestampMap vs timestampCorrections
- `timestampMap` — machine-generated. Freely overwritten on re-alignment.
- `timestampCorrections` — human-authored. NEVER overwritten by tools.

### Future architecture split (planned, not blocking)
```
sanghas/
  sfzc.json              ← chants[] only
  sfzc-schedule.json     ← horarium data
  sfzc-services/
    monday.json
    tuesday.json
    wednesday.json
    thursday.json
```

---

## Product Vision Notes

- **"The schedule is the teacher"** — the app holds the form
- **The train doesn't negotiate** — no snooze, no rescheduling
- **Shravaka is the user** — the hearer, the listener, the one who showed up
- **"Gassho, Shravaka. My home was eaten by the wind."** — the onboarding line
- **The placed device is already a ritual object**
- **The page moves down over the course of the day** — by evening you're near the bottom. Position on page IS position in the day.
- **"Enter Service" appearing live during a service period** — this is the product thesis made real. You come back and it's already happening. You're not launching an app. You're joining something.

### Origin story (session note)
The rakusu sewing teacher at Congress Park — turned her high-rise apartment into a little temple, started chanting the Metta Sutta every morning when the war started. She told Kevin about it, and a few days later he came and started working on Great Vows. She's an inspiration for the Shravaka archetype. Podcast introduction pending.

---

## On the Horizon

- Complete Wednesday and Thursday morning services
- Full Moon Ceremony and One Day Sitting alignment
- Watch as han — haptic bell on wrist (high leverage, deferred)
- Dedicated physical stupa/stand object (longer-term)
- Landscape placed mode development
- Ambient/iPad mode — stripped-down skin, just now + next, giant clock
- ZCD chant book — needs audio recordings
- GitHub / deployment

---

## Git Workflow

```bash
git add .
git commit -m "description"
git checkout .          # rollback
npx serve /Users/kevin/Desktop/great-vows
# localhost:3000
```

Current branch: `main`
