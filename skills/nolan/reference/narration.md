# Narration reference (spoken audio)

Captions carry the demo with the sound off. **Narration** adds a spoken product
explanation on top — a voice walking the viewer through what's happening, in the same
product-manager voice as the captions (`reference/pm-voice.md`). It's optional: a
storyboard with no `voice` block records exactly as before — silent.

`scripts/narrate.py` is a small **pluggable** text-to-speech layer. `record.py` uses
it to synthesize each line and mux it onto the scene's `.webm`, timed to when each
step fires.

## Turning it on

Add a top-level `voice` block to the storyboard, then give scenes or steps `vo` text.

```json
{
  "product": "Quill",
  "url": "http://localhost:3000/",
  "voice": { "provider": "auto" },
  "scenes": [
    {
      "name": "first-draft",
      "file": "01-first-draft.webm",
      "title": "Write your first draft",
      "subtitle": "Describe it in a sentence — Quill writes the rest",
      "steps": [
        { "card": ["Write your first draft", "…"], "hold": 4000,
          "vo": "Meet Quill — your everyday writing assistant." },
        { "card": null },
        { "cap": "Just tell it what you need, in plain words.", "hold": 3500 },
        { "type": { "placeholder": "Ask Quill…", "text": "Write a thank-you note to a coworker", "submit": true } },
        { "wait_text": "Draft ready" },
        { "cap": "Done — a ready-to-send note in seconds.", "hold": 5000,
          "vo": "And that's it — a polished, ready-to-send note in seconds." }
      ]
    }
  ]
}
```

## Where the spoken text comes from

Per step, the first of these that exists is spoken, timed to when the step runs:

1. `step["vo"]` — an explicit narration line (write full, natural sentences here).
2. a `cap` step's string — so existing captions are narrated automatically if you
   add no `vo` at all.

Alternatively, a **scene-level** `vo` overrides per-step lines for that scene:

- `"vo": "one paragraph…"` — spoken once from the top (offset 0). A single flowing
  voiceover.
- `"vo": [ {"at": 1.5, "text": "…"}, {"at": 18, "text": "…"} ]` — **timed lines**
  placed at explicit offsets in seconds (`[1.5, "…"]` shorthand also works). This is
  the way to narrate footage that's **already recorded** — where the recorder can't
  know step timing — by hand-placing each line along the clip.

Write `vo` as speech, not screen text: full sentences, natural phrasing, and short
enough to finish inside the step's `hold`/wait so lines don't overrun the next scene.

## Choosing a provider — the `voice` block

```json
"voice": {
  "provider": "auto",
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "model": "eleven_multilingual_v2",
  "rate": 180,
  "command": "mytts --text {text} --out {out}"
}
```

| `provider` | Sounds | Needs |
|---|---|---|
| `elevenlabs` | most human | `ELEVENLABS_API_KEY`; `voice_id`, `model` |
| `openai` | very natural | `OPENAI_API_KEY`; `voice` (e.g. `alloy`), `model` |
| `deepgram` | natural | `DEEPGRAM_API_KEY`; `model` (e.g. `aura-asteria-en`) |
| `piper` | good, offline, open-source | the `piper` binary + `voice_id` = path to a `.onnx` voice |
| `say` | robotic, but free & offline | macOS built-in; optional `voice_id` (e.g. `Samantha`), `rate` |
| `command` | whatever you plug in | `command` template with `{text}` / `{out}` placeholders |
| `auto` | best available | picks the first usable of the list above |
| `none` | — | no audio (same as omitting `voice`) |

- **Human-sounding** means a cloud provider (ElevenLabs / OpenAI / Deepgram) or a
  good Piper voice. `say` is the zero-setup fallback but sounds synthetic.
- **`command`** is the escape hatch for any other TTS (Coqui, Azure, Google Cloud,
  Amazon Polly, PlayHT, a local script…): give a shell template and nolan fills in
  `{text}` (already shell-quoted) and `{out}` (the file to write). Example:
  `"command": "edge-tts --text {text} --write-media {out}"`.
- **`auto`** tries `elevenlabs → openai → deepgram → piper → say` and uses the first
  one whose key/binary is present. Great default for a shared storyboard.

Fields other than `provider` are provider-specific and all optional — sensible
defaults are used when omitted.

## Requirements

- **ffmpeg** — required to mux audio into the `.webm` (`brew install ffmpeg`, or your
  platform's package manager). The audio track is encoded as libopus so the file
  stays a valid `.webm`.
- An **API key** (cloud providers) or the **tool** (`piper`, `say`, or your
  `command`). API keys are read from the environment, never stored in the storyboard.

If ffmpeg or the chosen provider is missing, the scene is recorded **silent** and a
warning is printed — narration never fails a good take.

## Standalone (add audio to already-recorded scenes)

`record.py` narrates as it shoots (with step-level timing). To (re)generate audio for
scenes already on disk — a scene-level voiceover from the top — run:

```bash
python3 scripts/narrate.py storyboard.json [scene ...]
```

This re-muxes onto the existing `.webm` files without re-recording. (Step timing isn't
known post-hoc, so this path plays scene-level narration from the top.)

## Cost & privacy

- Cloud TTS bills per character — keep `vo` tight, and prefer re-shooting single
  scenes over re-synthesizing everything.
- `vo` text is sent to the provider you choose. Keep it to the same non-sensitive,
  everyday content discipline as the rest of the demo (`SECURITY.md`).
