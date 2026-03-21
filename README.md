# Great Vows
## SFZC Daily Sutras — Local Chant Player

### Setup
1. Put this folder anywhere on your machine
2. Drop audio recordings into the `audio/` folder
3. Match the filename to the `"audio"` field in `chants.json`
4. Run a local server from this folder:
   ```
   npx serve .
   ```
5. Open http://localhost:3000 in your browser

> **Note:** Do not use `python3 -m http.server` — it does not support HTTP range requests, which are required for seeking in MP4 files.

### Adding Audio
In `chants.json`, find the chant you have a recording for and set:
```json
"audio": "audio/your-recording.mp3"
```
Then add `cueIn` timestamps (seconds) to each line:
```json
{ "text": "Beings are numberless.", "cueIn": 22 }
```

### Adding a New Chant
Add an entry to the `chants` array in `chants.json` following the existing pattern.

### Folder Structure
```
great-vows/
  index.html      — the app
  chants.json     — all chant text + timing data
  audio/          — drop .mp3 files here
  README.md
```
