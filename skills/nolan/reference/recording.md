# Recording reference — the harness

`scripts/record.py` is a storyboard interpreter. It launches Chromium via Playwright,
opens the app, injects a caption/title-card overlay, then plays each scene's steps and
saves one `.webm` per scene. This file explains how it works and how to drive it well.

## Running it

```bash
# all scenes in the storyboard
python3 scripts/record.py path/to/storyboard.json

# just some scenes (by their "name")
python3 scripts/record.py path/to/storyboard.json first-draft history
```

Prerequisites:

```bash
pip install playwright
playwright install chromium
```

Videos land in the storyboard's `out_dir`, named by each scene's `file`.

## How a scene is shot

1. A fresh browser **context** is created per scene with `record_video_dir` set, so
   each scene is an independent `.webm` (re-shoot one without touching the others).
2. The page navigates to `url`, waits for network idle, then the **overlay** is
   injected (see below).
3. Steps run in order. Async steps (`wait_text`) block until the completion marker
   appears, so nothing is clipped.
4. The context is closed (which finalizes the video) and the file is renamed to the
   scene's `file`.

## The overlay (title cards + captions)

nolan injects a small JS overlay that exposes two globals on the page:

- `window.__card(title, sub)` — show a full-screen title card; `window.__card()` with
  no args fades it away.
- `window.__cap(text)` — show a subtitle banner at the top; `window.__cap('')` or a
  falsy value hides it.

Both are pure DOM (fixed-position elements at a very high `z-index`) so they sit above
the app and are captured in the video. Because they live in the page, they're baked
into the recording — no post-production needed. The `accent` colour themes the card's
mark.

Captions use `white-space: nowrap` by default, so keep a single caption to roughly one
readable line (~60–80 chars). Break a long thought into two sequential `cap` steps.

## Selecting elements robustly (avoid wasted takes)

A wrong selector ruins a whole scene. Prefer, in order:

1. **`role` + `name`** — `{"click": {"role": "button", "name": "History"}}`. Most
   robust; matches accessible name. Great for buttons, links, tabs.
2. **`placeholder`** for inputs — `{"type": {"placeholder": "Ask Quill…", …}}`.
3. **visible `text`** — `{"click": {"text": "New draft"}}`.
4. **`selector`** (CSS) — last resort; brittle against markup changes.

Before a full shoot, open the app and confirm these exist. A quick dry run of one
scene surfaces selector problems in seconds.

## Typing that reads as human

`type` uses `press_sequentially` with a per-character delay (default ~32ms) so the
text appears keystroke-by-keystroke on camera, then optionally submits. This is
deliberate — instant `fill()` looks robotic and undersells the "I'm using the product"
feel. Keep the typed text short and everyday.

## Waiting for completion (the anti-clip rule)

The single most common demo mistake is moving on before the app finished. Every async
action must be followed by `wait_text` keyed on a real UI completion marker — the text
that appears when a stream ends, a save confirms, or a page settles. `record.py` waits
up to `timeout` (default 150s) and, as a fallback, settles on the page text no longer
changing. Choose a marker that only appears when the action is truly done.

## Demoing failure / recovery (the `run` step)

To show resilience (a service dropping, a retry), a scene can `run` a shell command
mid-take — e.g. stop a backend you're running locally — then send another request and
`wait_text` for it to succeed anyway. Only ever target processes and services **you
own and are running for the demo**. Never run destructive commands against anything
shared. See the failover scene in `examples/quill/storyboard.json`.

## Tuning

- **Viewport / video size** come from `viewport` in the storyboard.
- **Pacing** is controlled entirely by `hold` values and `wait` steps — tune these
  when you watch it back (`reference/polish.md`).
- **Poster frame:** grab a still from any completed scene with `ffmpeg`:
  `ffmpeg -i 01-first-draft.webm -vf "select=eq(n\,0)" -frames:v 1 poster.png`.
- **GIF:** `ffmpeg -i scene.webm -vf "fps=12,scale=960:-1" scene.gif` for a lightweight
  loop (drop it in a README).
