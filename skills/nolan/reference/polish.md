# Polish reference — watch it back before you ship

A first take is a draft. Polishing is watching each scene against the four disciplines
and fixing the storyboard until the clip is something you'd put in front of a customer.
Because recording is deterministic from the storyboard, polishing is: **note the
problem → edit the storyboard → re-shoot just that scene.**

## Review checklist (per scene)

Run every scene through this. Any "no" is a re-shoot.

**Complete takes (§4)**
- [ ] Did every async action fully finish on camera (nothing clipped mid-stream)?
- [ ] Is there a `wait_text` on each async step, keyed on a real completion marker?
- [ ] Does the payoff stay on screen long enough to read (~4–5s)?

**Show, then say (§3)**
- [ ] Does the scene open with a title card, then dismiss it before acting?
- [ ] Is each step captioned *before* it happens?
- [ ] Are captions one readable line, held long enough (~1s per 3 words)?
- [ ] Does the last caption state the payoff?

**PM voice (§1)**
- [ ] Does every caption describe a *benefit*, not a mechanic?
- [ ] Zero demo-jargon ("selector", "submit", "assertion", "endpoint")?

**Everyday content (§2)**
- [ ] Is every typed input something a stranger would recognize?
- [ ] No codenames, placeholder junk, sensitive data, or secrets on screen?

**Craft**
- [ ] Does the typing read as human (visible, not instant)?
- [ ] Right selectors — no mis-clicks, no "element not found" stalls?
- [ ] One idea per scene (split it if it's doing two things)?
- [ ] File named `NN-slug.webm` so scenes sort in order?

## Common problems → fixes

| Symptom | Fix in the storyboard |
|---|---|
| Answer/action cut off at the end | Add or correct `wait_text`; increase the final `hold`. |
| Feels rushed / can't read a caption | Raise `hold`; split a long caption into two `cap` steps. |
| Caption sounds like a test | Rewrite in PM voice (`pm-voice.md`) — lead with the benefit. |
| Typed prompt looks niche/confusing | Swap for an everyday example (`pm-voice.md` §2). |
| Typing looks robotic / instant | Ensure it's a `type` step (uses visible per-char typing), not a paste. |
| Title card lingers over the app | Add `{"card": null}` right after the opening card's hold. |
| Mis-click / stall | Switch the locator to `role`+`name` or `placeholder` (`recording.md`). |
| Video too long / heavy | Split into more scenes; trim setup captions; lower viewport if huge. |

## Re-shooting selectively

Every scene is its own `.webm`, so fix one without re-running the rest:

```bash
python3 scripts/record.py storyboard.json first-draft
```

Iterate scene-by-scene until every box above is checked. Then hand off with a one-line
description of each clip and where the files landed.

## Deliverables to offer

- The set of `NN-slug.webm` files (the scenes).
- Optionally a **poster frame** (still) and/or a **GIF** per scene — see the `ffmpeg`
  snippets in `recording.md`.
- A short caption list per scene (handy for accessibility / alt text / release notes).
