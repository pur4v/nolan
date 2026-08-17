<div align="center">

# nolan 🎬

**Record product-demo videos by driving your live app — narrated like a product manager.**

[![CI](https://github.com/pur4v/nolan/actions/workflows/ci.yml/badge.svg)](https://github.com/pur4v/nolan/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Agent%20Skill-8A63D2)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-000000)](https://docs.claude.com/en/docs/claude-code)

</div>

A director doesn't hit record and hope — they storyboard the shots, frame each one, and
shoot complete takes. **nolan** does that for software demos: point Claude at your running
app and it turns a feature into a storyboard, drives the *real* UI on screen, narrates
every step like a product manager showing a customer around, and captures a clean video
per scene.

The output is a demo, not a smoke test — the kind of clip you'd put on a landing page or
send to a user, where a first-time viewer understands both *what* is happening and *why it
matters*.

---

## What it does — three stages

| Stage | Ask it… | You get |
|---|---|---|
| 🎬 **Storyboard** | "plan a demo of feature X" | A scene-by-scene `storyboard.json`: title cards, PM-voice captions, exact clicks/typing, and what to wait for |
| 🎥 **Record** | "record it" | One `.webm` per scene, driven live against the running app, with title cards + subtitle captions baked in |
| ✨ **Polish** | "make this watchable" | A reviewed, re-shot take: fixed pacing, complete actions, readable captions, right framing |

Stages chain: storyboard → record → watch it back → polish → re-record. The storyboard is
the source of truth; recording is deterministic from it, so re-shooting one scene is free.

## What makes it a demo, not a screen grab — four disciplines

Baked into every video:

1. **Product-manager voice, not a smoke test** — captions say the *value to the user*
   ("a ready-to-send note in seconds"), never the mechanics ("submitting the form").
2. **Everyday, relatable content on screen** — only inputs a stranger recognizes go into
   the UI; no jargon, codenames, or "alien" concepts.
3. **Show, then say** — every scene opens with a full-screen title card and carries
   baked-in subtitle captions that narrate each step, so no viewer is ever lost.
4. **Complete takes on the real app** — drive the actual product, type visibly, and wait
   for each action to fully finish before moving on. Never clip mid-stream.

## How nolan works

```
you: "/nolan:storyboard our onboarding flow  (app at http://localhost:3000)"
                │
                ▼
        ┌────────────────┐   inspects the live UI: placeholders, buttons, completion markers
        │  nolan skill   │
        └───────┬────────┘
                │  drafts storyboard.json — scenes, title cards, steps, PM-voice captions
                ▼
     ┌──────────────────────┐
     │  scripts/record.py   │  drives the real app with Playwright, one scene at a time
     └──────────┬───────────┘
                │  injects title-card + caption overlay · visible typing · waits for completion
     ┌──────────┼───────────┬───────────┐
     ▼          ▼           ▼           ▼
 01-*.webm  02-*.webm   03-*.webm   04-*.webm   (one video per scene)
                │
                ▼  watch it back → polish → re-shoot only what needs it
        watchable demo videos, captions and all
```

## Install

nolan ships **two ways** from this one repo — pick whichever fits your setup.

### A) As a Claude Code plugin (recommended)

Installs the skill *plus* the `/nolan:*` slash commands and the storyboarder agent.

Run these **one at a time** — enter the first, press Enter and let it finish, then run the
second (copying both at once feeds the second line into the marketplace prompt):

```
/plugin marketplace add pur4v/nolan
```

```
/plugin install nolan
```

Then use the commands directly:

```
/nolan:storyboard   plan a demo of <feature>  (+ the app URL)
/nolan:record       storyboard.json [scene ...]
/nolan:polish       storyboard.json  — watch it back and fix
```

### B) As a standalone Agent Skill

Just the skill (no slash commands) — drop it where your Claude tooling looks for skills:

```bash
# Personal skill for Claude Code
git clone https://github.com/pur4v/nolan /tmp/nolan
cp -r /tmp/nolan/skills/nolan ~/.claude/skills/nolan
```

Or copy `skills/nolan` into a project's `.claude/skills/`. Once present, Claude invokes it
automatically when a request matches the triggers in `SKILL.md`, or you can ask for it by
name.

### Recorder prerequisites

The recorder drives a browser, so it needs Playwright:

```bash
pip install playwright && playwright install chromium
```

…and a **running app** at a URL you're allowed to film (a local dev server or a
demo/staging environment — never real customer data or secrets).

## Quick start

```bash
# 1. storyboard your app (or hand-write one — see skills/nolan/assets/storyboard-template.json)
# 2. shoot every scene
python3 skills/nolan/scripts/record.py storyboard.json

# or shoot a single scene while you iterate
python3 skills/nolan/scripts/record.py storyboard.json first-draft
```

Each scene becomes a `NN-slug.webm` in the storyboard's `out_dir`, title cards and
captions already baked in.

## Repo layout

```
nolan/
├── .claude-plugin/
│   ├── plugin.json          # plugin manifest
│   └── marketplace.json     # so `/plugin marketplace add pur4v/nolan` works
├── commands/                # slash commands → /nolan:storyboard :record :polish
├── agents/
│   └── storyboarder.md      # drafts a shoot-ready storyboard from a feature + URL
├── skills/nolan/            # the skill itself (canonical, installable on its own)
│   ├── SKILL.md             # when-to-use, 3 stages, 4 disciplines, procedure
│   ├── reference/           # progressive-disclosure docs, loaded on demand
│   │   ├── storyboard.md  recording.md  pm-voice.md  captions.md  polish.md
│   ├── scripts/record.py    # storyboard-driven Playwright recorder
│   └── assets/storyboard-template.json
└── examples/quill/          # a fully fictional worked storyboard (4 scenes)
```

## Example

See [`examples/quill/`](examples/quill/) for a complete, **entirely fictional** storyboard
(an AI writing assistant) showing all four disciplines across four scenes — streaming
output, a tone control, saved history, and an offline/recovery take.

## Contributing

Issues and PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) and the
[Code of Conduct](CODE_OF_CONDUCT.md). Security & safe-filming notes:
[SECURITY.md](SECURITY.md).

## License

MIT — see [LICENSE](LICENSE).
