# Example — "Quill" (fictional)

A complete, **entirely fictional** worked storyboard for nolan. *Quill* is a made-up
AI writing assistant — there's no real product, data, or secret here. It exists to show
what a good nolan storyboard looks like end to end.

## What the storyboard demonstrates

[`storyboard.json`](storyboard.json) contains four scenes, each becoming one `.webm`:

| Scene | File | Shows | nolan technique |
|---|---|---|---|
| `first-draft` | `01-first-draft.webm` | Type a plain request, watch it write | title card, PM-voice captions, visible typing, `wait_text` on completion |
| `tone` | `02-change-the-tone.webm` | Switch tone, regenerate | a `select` control, everyday input |
| `history` | `03-nothing-is-lost.webm` | Open History, drafts are saved | navigation via `role`+`name`, benefit-led captions |
| `offline` | `04-works-offline.webm` | Connection drops, it keeps working | a `run` step to simulate failure, then recovery |

Notice how every scene applies the four disciplines:

1. **PM voice** — captions say *"a ready-to-send note in seconds"*, never *"submitting
   the form"*.
2. **Everyday content** — "a thank-you note to a coworker", "invite the team to lunch",
   "an out-of-office reply". Nothing niche or jargony.
3. **Show, then say** — each scene opens with a title card, then captions set up every
   step before it happens.
4. **Complete takes** — every async step is followed by `wait_text: "Draft ready"` and a
   long closing `hold`, so nothing is clipped.

## How you'd shoot it

This example has no live app to point at (Quill isn't real), so it won't render videos
as-is — it's a reference for the *storyboard*, not a runnable demo. Against your own
running app you'd:

```bash
# 1. edit storyboard.json: set "url", "product", and the selectors to your app
# 2. shoot everything
python3 ../../skills/nolan/scripts/record.py storyboard.json

# or shoot a single scene while you iterate
python3 ../../skills/nolan/scripts/record.py storyboard.json first-draft
```

The `run` step in the `offline` scene here only echoes a message. In a real demo it
would stop a mock backend **you started for the shoot** — never a shared service.
