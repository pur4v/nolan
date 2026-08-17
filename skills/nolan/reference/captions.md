# Captions & title cards (discipline §3 — show, then say)

Every nolan video carries two kinds of on-screen text, both baked into the recording
so no editing step is needed: **title cards** and **subtitle captions**. Together they
mean a viewer with the sound off still understands the whole demo.

## Title cards

A full-screen card that opens a scene (and can also close a demo). It names the
product and the scene so the viewer has context before the app appears.

```json
{ "card": ["Write your first draft", "Describe it in a sentence — Quill writes the rest"], "hold": 4000 },
{ "card": null }
```

- `["title", "subtitle"]` shows the card; `hold` keeps it up (3.5–4.5s reads well).
- `{"card": null}` fades it away to reveal the app — always dismiss before acting.
- The product name and an accent mark are drawn automatically from the storyboard's
  `product` and `accent`.

Use a title card:
- at the **start of every scene** (what am I about to see?),
- optionally at the **end** of the last scene as a sign-off (name + tagline / URL).

## Subtitle captions

A single-line banner at the top that narrates the current step. This is where the PM
voice (`pm-voice.md`) lives.

```json
{ "cap": "Quill drafts it live, sentence by sentence.", "hold": 2500 },
{ "cap": null }
```

Rules that keep captions readable:

- **One line.** The banner is `nowrap` by default — keep to ~60–80 chars. Split a
  longer thought into two sequential `cap` steps.
- **Show before you act.** Caption the step, `hold` ~3–4s so it can be read, *then*
  perform the action. During a long async wait you can swap in a shorter "in progress"
  caption.
- **Hold on the payoff.** The closing caption of a scene should stay up ~4–5s after
  the action completes so the result is legible.
- **Reading speed:** budget ~1 second per ~3 words as a floor. A 12-word caption wants
  ~4s of `hold`.

## Pacing cheat-sheet

| Moment | Typical `hold` |
|---|---|
| Opening title card | 3500–4500 ms |
| Setup caption (before an action) | 3000–4000 ms |
| "In progress" caption during a wait | 2000–2500 ms |
| Closing / payoff caption | 4000–5500 ms |
| Brief reveal / animation (`wait`) | 1000–2500 ms |

These are starting points — always watch it back and adjust (`polish.md`). Too fast is
the more common failure: when unsure, hold longer.

## Why baked-in, not post-production

Captions are injected into the page and captured in the `.webm`, so the recording is
final on the first pass — no editor, no burn-in step, and re-shooting a scene keeps its
captions automatically. The trade-off is that captions are plain page elements: keep
them short and high-contrast (the defaults are white text on a dark rounded banner).
