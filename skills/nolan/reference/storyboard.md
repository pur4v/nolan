# Storyboard reference

The storyboard is the source of truth for a demo. `scripts/record.py` reads it and
shoots deterministically — so the thinking happens here, once, and re-shoots are free.

A storyboard is a JSON file. Top-level shape:

```json
{
  "product": "Quill",
  "url": "http://localhost:3000/",
  "viewport": { "width": 1280, "height": 800 },
  "out_dir": ".",
  "accent": "#4b8bff",
  "voice": { "provider": "auto" },
  "scenes": [ /* … */ ]
}
```

| Field | Meaning |
|---|---|
| `product` | Shown on every title card. Keep it the real product name. |
| `url` | The **live** app to film. nolan drives this; it does not mock it. |
| `viewport` | Recording size in px. `1280×800` is a good 16:10 default. |
| `out_dir` | Where `.webm` files are written (relative to the storyboard file). |
| `accent` | Hex colour for the title-card mark. Match the product's brand. |
| `voice` | *Optional.* Enables spoken narration and picks the TTS provider. Omit it (or set `"provider": "none"`) to keep the video silent. See `reference/narration.md`. |
| `scenes` | Ordered list of scenes; each becomes one `.webm`. |

## A scene

```json
{
  "name": "first-draft",
  "file": "01-first-draft.webm",
  "title": "Write your first draft",
  "subtitle": "Describe it in a sentence — Quill writes the rest",
  "steps": [ /* ordered actions */ ]
}
```

`name` is how you shoot one scene (`record.py storyboard.json first-draft`). `file`
is the output name — prefix with `NN-` so scenes sort in order. `title`/`subtitle`
are the opening full-screen card.

## Steps

Each step is an object with **one** action key (plus optional `hold`, in ms, to pause
after it, and optional `vo`, a spoken narration line — see below). Steps run top to
bottom.

| Step | Example | Does |
|---|---|---|
| `card` | `{"card": ["Write your first draft", "…"], "hold": 4000}` | Show a full-screen title card `[title, subtitle]`, hold, then it stays until dismissed. |
| `card` (dismiss) | `{"card": null}` | Fade the title card away to reveal the app. |
| `cap` | `{"cap": "This is Quill — your writing assistant.", "hold": 3500}` | Show a subtitle caption (top banner) and hold so it's readable. |
| `cap` (clear) | `{"cap": null}` | Hide the caption banner. |
| `type` | `{"type": {"placeholder": "Ask Quill…", "text": "Write a thank-you note to a coworker"}}` | Click a field and type **visibly** (human-paced). Locate by `placeholder`, `selector`, or `role`+`name`. Optional `delay` ms/char, `submit: true` to press Enter after. |
| `click` | `{"click": {"role": "button", "name": "History"}}` | Click an element by `role`+`name`, `text`, or `selector`. |
| `select` | `{"select": {"label": "Friendly"}}` | Pick an option (by visible `label`) from a `<select>`; optionally scope with `selector`. |
| `key` | `{"key": "Enter"}` | Press a key on the focused element. |
| `wait` | `{"wait": 2000}` | Pause N ms (for animations / reveals). |
| `wait_text` | `{"wait_text": "Draft ready", "timeout": 120000}` | **Wait for an action to finish** — block until this text appears (e.g. a completion marker). This is how you avoid clipping. |
| `run` | `{"run": "kill $(lsof -ti:8081)"}` | Run a shell command mid-scene (e.g. to demo failure/recovery). Use sparingly and only against processes you own. |

## Writing a good scene (the disciplines, applied)

- **Open with a card** naming the scene, then dismiss it (`{"card": null}`) before
  the action so the app is unobscured.
- **Caption before you act, not after.** Show the caption that explains the *next*
  step, hold ~3–4s so it can be read, then perform the step. The viewer should always
  know what they're about to see.
- **Type something everyday.** The text in a `type` step is on screen — make it
  generic and relatable (see `pm-voice.md`). No internal jargon.
- **Always `wait_text` on anything async.** Streaming answers, saves, navigations —
  wait for the real completion marker so the take is complete, then `cap` a closing
  line and `hold` ~4–5s so the result is readable.
- **One idea per scene.** If you're tempted to demo two features, make two scenes.
- **Optional: narrate it out loud.** Add a `voice` block to the storyboard and a `vo`
  line to any step (or a scene-level `"vo"` paragraph) to get human-sounding spoken
  narration muxed onto the `.webm`, timed to the steps. If a step has no `vo`, its
  `cap` text is spoken instead. Full details — providers, keys, ffmpeg — in
  `reference/narration.md`.

## Minimal example

```json
{
  "product": "Quill",
  "url": "http://localhost:3000/",
  "out_dir": ".",
  "scenes": [
    {
      "name": "first-draft",
      "file": "01-first-draft.webm",
      "title": "Write your first draft",
      "subtitle": "Describe it in a sentence — Quill writes the rest",
      "steps": [
        { "card": ["Write your first draft", "Describe it in a sentence — Quill writes the rest"], "hold": 4000 },
        { "card": null },
        { "cap": "This is Quill — tell it what you need in plain words.", "hold": 3500 },
        { "type": { "placeholder": "Ask Quill…", "text": "Write a thank-you note to a coworker", "submit": true } },
        { "cap": "Quill drafts it live, sentence by sentence.", "hold": 2500 },
        { "wait_text": "Draft ready" },
        { "cap": "Done — a ready-to-send note in seconds.", "hold": 5000 }
      ]
    }
  ]
}
```

See `assets/storyboard-template.json` for a fuller multi-scene template and
`examples/quill/` for a complete worked storyboard.
