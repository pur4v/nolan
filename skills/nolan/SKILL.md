---
name: nolan
description: >-
  Record polished product-demo videos by driving a live web app agentically and
  narrating it like a product manager. Use when someone wants a demo video, a
  screencast, a product walkthrough, a feature showcase, a launch/marketing clip,
  a GIF of a flow, or a recording of a user journey through an app. Turns a feature
  into a storyboard, drives the real UI with Playwright (visible typing, real
  clicks), overlays full-screen title cards and baked-in subtitle captions, waits
  for each action to fully complete, and saves a .webm per scene. Triggers:
  "record a demo / demo video / screencast", "make a product walkthrough / feature
  showcase", "screen record this flow", "capture a video of the app doing X",
  "storyboard a demo", "make a launch clip / marketing video", "record me a GIF of
  this", "show this feature on video".
---

# nolan

A director doesn't hit record and hope. They storyboard the shots, frame each one,
and shoot complete takes. **nolan** does that for software demos: it turns a feature
into a storyboard, drives your *real* app on screen, narrates every step like a
product manager showing the product to a user, and captures a clean video per scene.

The output is a demo, not a smoke test — the kind of clip you'd put on a landing
page or send to a customer, where a first-time viewer understands both *what* is
happening and *why it matters*.

## When to use this skill

Use it whenever the real job is *"produce a watchable video of this product doing
something, for a person who has never seen it."* That includes launch clips, feature
showcases, landing-page hero videos, onboarding walkthroughs, and release notes GIFs.

Do **not** reach for it to *test* a flow — that's an end-to-end test, and it should
be terse and headless. nolan optimizes for the opposite: legibility, pacing, and
narration for a human audience.

## The workflow — three stages

| Stage | You ask… | nolan produces | Reference |
|---|---|---|---|
| 🎬 **Storyboard** | "plan a demo of feature X" | A scene-by-scene storyboard (JSON): title cards, captions, the exact clicks/typing, and what to wait for | `reference/storyboard.md` |
| 🎥 **Record** | "record it" | One `.webm` per scene, driven live against the running app with overlaid title cards + subtitle captions | `reference/recording.md` |
| ✨ **Polish** | "make this watchable" | A reviewed, re-shot take: fixed pacing, complete actions, readable captions, corrected framing | `reference/polish.md` |

Stages chain: storyboard → record → watch it back → polish → re-record. The
storyboard is the source of truth; recording is deterministic from it.

## The four disciplines (non-negotiable, every video)

These are what separate a demo from a screen grab. They are not optional.

1. **Product-manager voice, not a smoke test.** Narrate the *value to the user* —
   what this lets them do and why it's good — never the mechanics of testing. Every
   caption reads like a PM walking a customer through the product. See
   `reference/pm-voice.md`.

2. **Everyday, relatable content on screen.** Only inputs a general audience already
   understands go into the UI — normal questions, real-world examples ("buy oat
   milk", "a thank-you note to a coworker"). **Never** niche jargon, internal
   codenames, or "alien" concepts the viewer has to decode. Approachability first.

3. **Show, then say.** Every scene opens with a full-screen **title card** (product +
   scene name) and carries **baked-in subtitle captions** (a top banner) that narrate
   each step as it happens, so no viewer is ever lost. See `reference/captions.md`.

4. **Complete takes on the real app.** Drive the *actual product* live — visible,
   human-paced typing and real clicks — and **wait for each action to fully finish**
   before moving on, then hold so it's readable. Never clip an answer or transition
   mid-stream. Length serves completeness.

## Standard procedure

1. **Scope the demo.** What product, which feature(s), what URL is it served at, and
   who's the audience? Confirm the app is running and reachable (nolan films a *live*
   app; it doesn't mock one).
2. **Storyboard.** Draft `storyboard.json` — one scene per idea, each with a title
   card, ordered steps (type / click / select / wait), and captions in PM voice.
   Use `assets/storyboard-template.json` as the shape. Keep prompts generic (§2).
3. **Dry-run the selectors.** Confirm the placeholders / roles / text the storyboard
   targets actually exist in the DOM before a full shoot (a wrong selector wastes a
   whole take). `reference/recording.md` covers robust selection.
4. **Record.** Run `scripts/record.py storyboard.json [scene ...]`. It injects the
   caption/title-card overlay, drives each scene, waits for completion, and saves one
   `.webm` per scene into the storyboard's `out_dir`.
5. **Watch it back and polish.** Check each discipline against
   `reference/polish.md` — is anything clipped, is any caption jargon, does the
   typing read as human, is every action complete? Fix the storyboard and re-shoot
   just the affected scenes.
6. **Deliver.** Report where the files landed, their sizes/durations, and a one-line
   description per scene. Offer a poster frame or GIF if useful.

## Setup nolan expects

- **Python + Playwright** (`pip install playwright && playwright install chromium`).
  `scripts/record.py` uses the sync API and `record_video_dir` to capture `.webm`.
- **A running app** at a URL the machine can reach (local dev server or a deployed
  environment you're allowed to film).
- Realistic, non-sensitive demo data loaded in the app — see discipline §2 and the
  data note in `SECURITY.md`. Never film real customer data or secrets.

See `reference/recording.md` for the harness details, the overlay technique, and the
storyboard step reference.

## Output principles

- One video per scene, named `NN-slug.webm`, so scenes can be re-shot independently.
- Lead your hand-off with the *watchable result* (what each clip shows), then the
  mechanics (paths, sizes, how to re-record).
- Prefer several short, complete scenes over one long clip — easier to re-shoot and
  to reuse.
- If a take had to be cut short or a caption is a placeholder, say so — an honest
  "scene 3 still needs a re-shoot" beats shipping a clipped demo.
