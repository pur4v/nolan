---
description: Polish a recorded demo — watch each scene against the four disciplines, fix pacing / captions / clipped actions in the storyboard, and re-shoot just the affected scenes.
argument-hint: <path to storyboard.json (and, if helpful, the rendered .webm files to review)>
---

Run **nolan** in **Polish** mode on: $ARGUMENTS

Goal: turn a first take into something you'd put in front of a customer. Watch each
scene back and run it through the review checklist:

- **Complete (§4):** did every async action fully finish on camera? Is there a
  `wait_text` on each? Does the payoff hold long enough (~4–5s)?
- **Show, then say (§3):** title card per scene, captions before each step, one readable
  line held long enough.
- **PM voice (§1):** captions describe a benefit, never a mechanic; zero demo-jargon.
- **Everyday content (§2):** every typed input is relatable; no codenames or sensitive data.
- **Craft:** human-paced typing, correct selectors, one idea per scene, `NN-slug.webm` naming.

For each problem: edit the storyboard, then re-shoot only that scene
(`python3 skills/nolan/scripts/record.py storyboard.json <scene>`). Iterate until every
box is checked.

Load `skills/nolan/reference/polish.md` first. Finish by listing the final clips (with a
one-line description each) and offer a poster frame or GIF per scene.
