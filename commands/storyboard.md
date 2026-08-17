---
description: Storyboard a product-demo video — turn a feature into a scene-by-scene plan (title cards, PM-voice captions, exact steps, completion waits) as a nolan storyboard.json.
argument-hint: <what to demo, e.g. "our onboarding flow" or "the new export feature"> [+ the app URL]
---

Run **nolan** in **Storyboard** mode for: $ARGUMENTS

Goal: produce a `storyboard.json` a first-time viewer could follow. For each idea worth
showing, write one scene with: an opening title card, ordered steps (type / click /
select / wait), a `wait_text` on every async action, and captions that narrate each step
in **product-manager voice** (benefit, not mechanic).

Apply the four disciplines while drafting:
- PM voice, not a smoke test — captions say what the user gains.
- Everyday, relatable inputs on screen — no jargon, codenames, or sensitive data.
- Show, then say — title card per scene, caption each step before it happens.
- Complete takes — `wait_text` on real completion markers, generous closing holds.

Confirm the app URL and which selectors exist before finalizing. One idea per scene;
prefer several short scenes over one long clip.

Load `skills/nolan/reference/storyboard.md` and `skills/nolan/reference/pm-voice.md`
first; use `skills/nolan/assets/storyboard-template.json` as the shape. Offer to save the
storyboard next to the project being filmed.
