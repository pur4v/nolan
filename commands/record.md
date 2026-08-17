---
description: Record the demo — drive the live app with Playwright from a nolan storyboard, overlay title cards + narrated captions, wait for each action to complete, and save one .webm per scene.
argument-hint: <path to storyboard.json> [scene names to shoot — defaults to all]
---

Run **nolan** in **Record** mode using: $ARGUMENTS

Goal: capture the storyboard as video. Confirm the app is running and reachable at the
storyboard's `url`, verify Playwright is installed (`pip install playwright && playwright
install chromium`), then shoot.

```bash
python3 skills/nolan/scripts/record.py <storyboard.json> [scene ...]
```

Each scene becomes its own `.webm` in the storyboard's `out_dir`, with the caption /
title-card overlay baked in. Before a full shoot, dry-run one scene to catch bad
selectors (a wrong locator wastes a whole take) — prefer `role`+`name` or `placeholder`.

Never film sensitive data or secrets, and only use a `run` step against a process **you
own and started for the demo**.

Load `skills/nolan/reference/recording.md` first. After shooting, report where the files
landed (path, size, one line per scene) and offer to run the **polish** pass.
