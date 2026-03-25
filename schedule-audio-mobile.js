/* ============================================================
   GREAT VOWS — schedule.html audio engine + mobile CSS
   Drop this entire block in before the closing </body> tag.
   
   DEPENDENCIES (already in your project):
     audio/sfzc/temple_sounds-the_han.mp3
     audio/sfzc/temple_sounds-the_densho_bell.mp3
     audio/sfzc/MorningService_Monday.mp4
     audio/sfzc/MorningService_Tuesday.mp4
   
   SCHEDULE constant: must match your existing SCHEDULE array.
   This file uses the same SCHEDULE and getScheduleState() 
   you already have — do not redefine them here, just add 
   this block after your existing JS.
   ============================================================ */

/* ── Mobile CSS ──────────────────────────────────────────── */
const mobileStyles = document.createElement('style');
mobileStyles.textContent = `
  /* Portrait / narrow phone layout */
  @media (max-width: 600px) {
    body {
      flex-direction: column;
    }

    /* Hide sidebar in portrait — clock moves to top bar */
    .sidebar {
      display: none;
    }

    /* Full-width track */
    .track {
      width: 100%;
      padding: 0 16px;
    }

    /* Compact top bar with clock */
    .mobile-topbar {
      display: flex !important;
      align-items: baseline;
      gap: 12px;
      padding: 14px 16px 10px;
      border-bottom: 0.5px solid rgba(26,24,20,0.12);
      position: sticky;
      top: 0;
      background: #f4f0e8;
      z-index: 20;
    }

    .mobile-topbar .clock-display {
      font-family: 'Cormorant', serif;
      font-size: 28px;
      font-weight: 400;
      color: var(--ink);
      letter-spacing: -0.01em;
    }

    .mobile-topbar .mobile-next {
      font-family: 'IBM Plex Mono', monospace;
      font-size: 10px;
      color: rgba(26,24,20,0.5);
      letter-spacing: 0.05em;
    }

    /* Period rows tighter on mobile */
    .period-row {
      padding: 10px 0;
    }

    .period-row.now .period-name {
      font-size: 32px !important;
    }

    /* Mute button repositioned on mobile */
    #mute-btn {
      bottom: 16px;
      right: 16px;
    }
  }

  /* Landscape phone / placed mode */
  @media (max-width: 900px) and (orientation: landscape) {
    /* Already landscape-first — minimal changes */
    .sidebar {
      min-width: 160px;
    }

    .clock-display {
      font-size: 36px !important;
    }
  }

  /* ── Mute button (all sizes) ── */
  #mute-btn {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 0.5px solid rgba(26,24,20,0.2);
    background: rgba(244,240,232,0.92);
    backdrop-filter: blur(4px);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 30;
    transition: opacity 0.2s;
    padding: 0;
  }

  #mute-btn:hover {
    opacity: 0.7;
  }

  #mute-btn svg {
    width: 16px;
    height: 16px;
    stroke: var(--ink);
    fill: none;
    stroke-width: 1.5;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  /* Audio fade-in */
  @keyframes gv-fade { from { opacity: 0 } to { opacity: 1 } }
`;
document.head.appendChild(mobileStyles);


/* ── Mobile top bar (portrait only) ─────────────────────── */
const mobileTopbar = document.createElement('div');
mobileTopbar.className = 'mobile-topbar';
mobileTopbar.style.display = 'none'; // shown via CSS media query
mobileTopbar.innerHTML = `
  <span class="clock-display" id="mobile-clock">--:--:--</span>
  <span class="mobile-next" id="mobile-next"></span>
`;
document.body.prepend(mobileTopbar);


/* ── Mute button ─────────────────────────────────────────── */
const muteBtn = document.createElement('button');
muteBtn.id = 'mute-btn';
muteBtn.title = 'Toggle audio';
muteBtn.setAttribute('aria-label', 'Toggle audio');

const speakerOnSVG = `<svg viewBox="0 0 24 24"><path d="M11 5L6 9H2v6h4l5 4V5z"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>`;
const speakerOffSVG = `<svg viewBox="0 0 24 24"><path d="M11 5L6 9H2v6h4l5 4V5z"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></svg>`;

let isMuted = localStorage.getItem('gv-muted') === '1';
muteBtn.innerHTML = isMuted ? speakerOffSVG : speakerOnSVG;
document.body.appendChild(muteBtn);

muteBtn.addEventListener('click', () => {
  isMuted = !isMuted;
  localStorage.setItem('gv-muted', isMuted ? '1' : '0');
  muteBtn.innerHTML = isMuted ? speakerOffSVG : speakerOnSVG;
  AudioEngine.applyMute();
});


/* ══════════════════════════════════════════════════════════
   AUDIO ENGINE
   ══════════════════════════════════════════════════════════ */
const AudioEngine = (() => {

  /* ── Config ── */
  const BASE = 'audio/sfzc/';

  const AUDIO_FILES = {
    han:     BASE + 'temple_sounds-the_han.mp3',
    densho:  BASE + 'temple_sounds-the_densho_bell.mp3',
    opening: BASE + 'temple_sounds-opening_chant.mp3',
  };

  /* Maps serviceId → audio file path */
  const SERVICE_AUDIO = {
    'morning-service-monday':  BASE + 'MorningService_Monday.mp4',
    'morning-service-tuesday': BASE + 'MorningService_Tuesday.mp4',
    // extend as you add Wednesday/Thursday
  };

  const HAN_LEAD_MINUTES = 15;   // how early the han starts playing
  const AMBIENT_VOLUME   = 0.33; // "through the door" level
  const FADE_DURATION_MS = 3000; // ambient cross-fade in

  /* ── State ── */
  let hanAudio        = null;
  let ambientAudio    = null;
  let denshoAudio     = null;
  let hanDuration     = null;   // loaded once after first play
  let hanTriggeredFor = null;   // which period id the han was triggered for
  let activeServiceId = null;   // currently playing ambient service
  let lastPeriodId    = null;   // for detecting period transitions

  /* ── Helpers ── */

  function nowSeconds() {
    const d = new Date();
    return d.getHours() * 3600 + d.getMinutes() * 60 + d.getSeconds();
  }

  function periodStartSeconds(period) {
    return period.time[0] * 3600 + period.time[1] * 60;
  }

  function periodEndSeconds(period) {
    return period.end[0] * 3600 + period.end[1] * 60;
  }

  function getAudio(src) {
    const a = new Audio(src);
    a.preload = 'metadata';
    return a;
  }

  function fadeIn(audioEl, targetVolume, durationMs) {
    if (!audioEl) return;
    audioEl.volume = 0;
    const steps = 30;
    const stepMs = durationMs / steps;
    const stepVol = targetVolume / steps;
    let step = 0;
    const id = setInterval(() => {
      step++;
      audioEl.volume = Math.min(targetVolume, stepVol * step);
      if (step >= steps) clearInterval(id);
    }, stepMs);
  }

  function stopAndClear(audioEl) {
    if (!audioEl) return null;
    audioEl.pause();
    audioEl.src = '';
    return null;
  }

  /* ── Public: apply mute/unmute to all active audio ── */
  function applyMute() {
    const vol = isMuted ? 0 : AMBIENT_VOLUME;
    if (ambientAudio)    ambientAudio.volume    = vol;
    if (hanAudio)        hanAudio.volume         = isMuted ? 0 : 1;
    if (denshoAudio)     denshoAudio.volume      = isMuted ? 0 : 1;
  }

  /* ── Han logic ── */
  /*
    The han plays during the 15-minute window BEFORE each zazen period.
    If the audio is shorter than 15 min, it loops.
    If longer (a full 15-min han sequence), it plays once.

    We detect the han window like this:
      hanWindowStart = zazenPeriodStart - HAN_LEAD_MINUTES * 60
      hanWindowEnd   = zazenPeriodStart

    If now is inside a han window and the han isn't already 
    playing for this period, we start it.
  */
  function getHanTarget() {
    const now = nowSeconds();
    for (const period of SCHEDULE) {
      if (period.type !== 'zazen') continue;
      const start = periodStartSeconds(period);
      const windowStart = start - HAN_LEAD_MINUTES * 60;
      if (now >= windowStart && now < start) {
        return { period, elapsed: now - windowStart };
      }
    }
    return null;
  }

  function tickHan() {
    const target = getHanTarget();

    if (!target) {
      // Outside all han windows — stop if playing
      if (hanAudio) {
        hanAudio = stopAndClear(hanAudio);
        hanTriggeredFor = null;
      }
      return;
    }

    const { period, elapsed } = target;

    // Already playing for this period? Nothing to do.
    if (hanTriggeredFor === period.id && hanAudio && !hanAudio.paused) return;

    // Start the han
    hanTriggeredFor = period.id;
    hanAudio = getAudio(AUDIO_FILES.han);
    hanAudio.volume = isMuted ? 0 : 1;

    hanAudio.addEventListener('loadedmetadata', () => {
      hanDuration = hanAudio.duration;
      const windowDuration = HAN_LEAD_MINUTES * 60;

      if (hanDuration >= windowDuration - 5) {
        // Long recording: seek to elapsed position (radio model)
        hanAudio.currentTime = Math.min(elapsed, hanDuration - 1);
        hanAudio.loop = false;
      } else {
        // Short clip: loop and seek to position within current loop
        hanAudio.loop = true;
        hanAudio.currentTime = elapsed % hanDuration;
      }

      hanAudio.play().catch(() => {
        // Autoplay blocked — will retry on next user interaction
        document.addEventListener('click', () => {
          if (hanAudio) hanAudio.play().catch(() => {});
        }, { once: true });
      });
    }, { once: true });

    hanAudio.load();
  }

  /* ── Ambient service audio ── */
  /*
    During any service period (hasService: true), play the 
    corresponding recording at AMBIENT_VOLUME. 
    
    Radio model: seek to elapsed time so it's already "in progress"
    when you open the page. Cross-fade in over FADE_DURATION_MS.

    Pauses when tab is hidden, resumes when visible.
  */
  function tickAmbient(currentState) {
    if (!currentState || currentState.type !== 'current') {
      // Not in any period — stop ambient
      if (ambientAudio) {
        ambientAudio = stopAndClear(ambientAudio);
        activeServiceId = null;
      }
      return;
    }

    const period = currentState.period;

    if (!period.hasService || !SERVICE_AUDIO[period.serviceId]) {
      // Period exists but has no audio
      if (ambientAudio) {
        ambientAudio = stopAndClear(ambientAudio);
        activeServiceId = null;
      }
      return;
    }

    // Already playing the right service
    if (activeServiceId === period.serviceId && ambientAudio && !ambientAudio.paused) return;

    // Stop previous ambient if switching
    if (ambientAudio) stopAndClear(ambientAudio);

    activeServiceId = period.serviceId;
    ambientAudio = getAudio(SERVICE_AUDIO[period.serviceId]);
    ambientAudio.volume = 0; // starts at 0, fades in

    const elapsedSeconds = nowSeconds() - periodStartSeconds(period);

    ambientAudio.addEventListener('loadedmetadata', () => {
      const seekTo = Math.min(Math.max(elapsedSeconds, 0), ambientAudio.duration - 1);
      ambientAudio.currentTime = seekTo;
      ambientAudio.play().then(() => {
        if (!isMuted) fadeIn(ambientAudio, AMBIENT_VOLUME, FADE_DURATION_MS);
      }).catch(() => {
        // Autoplay blocked — play on next click
        document.addEventListener('click', () => {
          if (ambientAudio) {
            ambientAudio.play().then(() => {
              if (!isMuted) fadeIn(ambientAudio, AMBIENT_VOLUME, FADE_DURATION_MS);
            }).catch(() => {});
          }
        }, { once: true });
      });
    }, { once: true });

    ambientAudio.load();
  }

  /* Pause ambient when tab hidden, resume when visible */
  document.addEventListener('visibilitychange', () => {
    if (!ambientAudio) return;
    if (document.hidden) {
      ambientAudio.pause();
    } else {
      // Re-sync position on resume (in case significant time passed)
      if (activeServiceId) {
        const period = SCHEDULE.find(p => p.serviceId === activeServiceId);
        if (period) {
          const elapsed = nowSeconds() - periodStartSeconds(period);
          if (elapsed >= 0 && elapsed < ambientAudio.duration) {
            ambientAudio.currentTime = elapsed;
          }
        }
      }
      ambientAudio.play().catch(() => {});
    }
  });

  /* ── Period transition bell ── */
  /*
    Plays a single densho bell strike when we cross into a new period.
    Skips the very first tick (page load) so we don't bell on arrival.
  */
  let firstTick = true;

  function tickBell(currentPeriodId) {
    if (firstTick) {
      firstTick = false;
      lastPeriodId = currentPeriodId;
      return;
    }

    if (currentPeriodId && currentPeriodId !== lastPeriodId) {
      lastPeriodId = currentPeriodId;
      playDensho();
    }
  }

  function playDensho() {
    if (isMuted) return;
    // Don't stack bells
    if (denshoAudio && !denshoAudio.ended) return;
    denshoAudio = getAudio(AUDIO_FILES.densho);
    denshoAudio.volume = 1;
    denshoAudio.play().catch(() => {});
  }

  /* ── Enter Service timestamp handoff ── */
  /*
    Updates the "Enter Service" link to include the current 
    elapsed seconds as a ?t= parameter.
    
    Your schedule.html already renders:
      <a href="index.html?service={serviceId}" ...>Enter service →</a>
    
    We upgrade that href every tick so it always has ?t=elapsed.

    In index.html, on load, read:
      const params = new URLSearchParams(window.location.search);
      const seekTo = parseFloat(params.get('t') || '0');
      // then: audioEl.currentTime = seekTo;
  */
  function updateEnterServiceLink() {
    const btn = document.querySelector('[data-enter-service]') 
             || document.querySelector('a[href*="service="]');
    if (!btn) return;

    const href = btn.getAttribute('href') || '';
    const match = href.match(/service=([^&]+)/);
    if (!match) return;

    const serviceId = match[1];
    const period = SCHEDULE.find(p => p.serviceId === serviceId);
    if (!period) return;

    const elapsed = Math.max(0, nowSeconds() - periodStartSeconds(period));
    const base = href.split('?')[0];
    btn.href = `${base}?service=${serviceId}&t=${Math.floor(elapsed)}`;
  }

  /* ── Mobile clock sync ── */
  function updateMobileClock() {
    const mobileClock = document.getElementById('mobile-clock');
    if (!mobileClock) return;

    const now = new Date();
    const h = String(now.getHours()).padStart(2, '0');
    const m = String(now.getMinutes()).padStart(2, '0');
    const s = String(now.getSeconds()).padStart(2, '0');
    mobileClock.textContent = `${h}:${m}:${s}`;

    // Mobile next period text
    const mobileNext = document.getElementById('mobile-next');
    if (mobileNext) {
      const state = getScheduleState(); // your existing function
      if (state && state.nextPeriod) {
        const nextStart = state.nextPeriod.time[0] * 60 + state.nextPeriod.time[1];
        const nowMin = now.getHours() * 60 + now.getMinutes();
        const diffMin = nextStart - nowMin;
        if (diffMin > 0) {
          const h = Math.floor(diffMin / 60);
          const m = diffMin % 60;
          const label = h > 0 ? `${h}h ${m}m` : `${m}m`;
          mobileNext.textContent = `${label} · ${state.nextPeriod.name}`;
        }
      }
    }
  }

  /* ── Main tick (called from your existing 1s interval) ── */
  function tick() {
    // Get schedule state using your existing function
    const state = typeof getScheduleState === 'function' ? getScheduleState() : null;
    const currentPeriodId = state && state.type === 'current' ? state.period.id : null;

    tickHan();
    tickAmbient(state);
    tickBell(currentPeriodId);
    updateEnterServiceLink();
    updateMobileClock();
  }

  /* ── Init ── */
  function init() {
    // Hook into your existing tick. Your schedule.html already has
    // a setInterval that runs every second. We just piggyback on it.
    //
    // If you prefer, replace this with:
    //   setInterval(tick, 1000);
    // and call AudioEngine.tick() from your existing interval instead.
    //
    const originalTick = window._scheduleTick; 
    if (typeof originalTick === 'function') {
      // If you exposed your tick function as window._scheduleTick
      window._scheduleTick = () => { originalTick(); tick(); };
    } else {
      // Otherwise run our own interval
      setInterval(tick, 1000);
    }

    // First tick immediately
    tick();
  }

  return { init, tick, applyMute };

})();

/* ── Boot ─────────────────────────────────────────────────── */
/*
  Call AudioEngine.init() after your existing schedule JS is set up.
  If your schedule already has a DOMContentLoaded handler, add this 
  inside it. Otherwise this inline call works fine — it runs after 
  the script tag is parsed.
*/
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', AudioEngine.init);
} else {
  AudioEngine.init();
}


/* ══════════════════════════════════════════════════════════
   index.html — timestamp seek on load
   
   ADD THIS BLOCK to your existing index.html JS,
   inside your audio initialization section:
   ══════════════════════════════════════════════════════════ */

/*
const params = new URLSearchParams(window.location.search);
const seekOnLoad = parseFloat(params.get('t') || '0');

// After your audio element is set up and can receive a seek:
if (seekOnLoad > 0) {
  audioEl.addEventListener('loadedmetadata', () => {
    audioEl.currentTime = seekOnLoad;
    // Optional: also start playing immediately
    // audioEl.play();
  }, { once: true });
}
*/


/* ══════════════════════════════════════════════════════════
   GitHub Pages — deployment in 3 steps

   1. In your project root, make sure you have:
        index.html
        schedule.html
        chantbook.json
        sanghas/
        audio/
      
      (All already present per your file structure)

   2. Push to GitHub if you haven't:
        git remote add origin https://github.com/YOURNAME/great-vows.git
        git push -u origin main

   3. In GitHub → Settings → Pages:
        Source: Deploy from branch
        Branch: main / (root)
        Save

      Your site will be live at:
        https://YOURNAME.github.io/great-vows/
      
      Share schedule.html as:
        https://YOURNAME.github.io/great-vows/schedule.html

   NOTE ON AUDIO: GitHub Pages has a 100MB file limit per file 
   and 1GB total. Your MP4 service recordings may be large. 
   Options:
   a) Host audio on a CDN (Cloudflare R2 is free, great for this)
   b) Use Git LFS for audio files (GitHub supports this)
   c) For sharing the schedule page without audio, audio 
      just fails silently — the page still works.

   For a shareable link RIGHT NOW without deploying:
     npx localtunnel --port 3000
   This gives you a public URL for your local server 
   (ephemeral, good for demos).
   ══════════════════════════════════════════════════════════ */
