# PM voice & everyday content (disciplines §1 and §2)

The captions and the on-screen inputs are what make a recording a *demo* instead of a
screen grab. Two disciplines govern them.

## §1 — Product-manager voice, not a smoke test

Write every caption as a product manager walking a **first-time user** through the
product. The viewer should learn *what they can do* and *why it's good* — never how
you're testing it.

**Say what it lets the user do; never narrate the mechanics.**

| ❌ Smoke-test voice | ✅ PM voice |
|---|---|
| "Selecting the model dropdown." | "Pick whichever model fits — Quill remembers your default." |
| "Submitting the form." | "Hit send, and your draft starts writing itself." |
| "Waiting for the response to stream." | "Quill drafts it live, sentence by sentence." |
| "Clicking the History tab." | "Everything you write is saved here — nothing to lose." |
| "Assertion passed: text present." | "Done — a ready-to-send note in seconds." |

Guidelines:

- **Lead with the benefit.** "so you never lose a draft", "in seconds", "without
  leaving the page".
- **Present tense, active, second person.** "You describe it, Quill writes it."
- **One idea per caption.** If it needs a comma-spliced second clause, split it into
  two sequential captions.
- **Set up before you act.** Show the caption that explains the next step *before*
  performing it, so the viewer is never surprised.
- **Close each scene with the payoff.** The last caption states what the user just
  got.
- **No jargon about the demo itself** — no "assertion", "selector", "endpoint",
  "payload", "test". The viewer doesn't know or care that this is automated.

## §2 — Everyday, relatable content on screen

Whatever you type into the product is on camera. It must be something a general
audience instantly understands. Niche or internal examples make viewers feel the
product isn't for them.

**Use ordinary, real-world inputs:**

- ✅ "Write a thank-you note to a coworker"
- ✅ "Buy oat milk"
- ✅ "Three quick ideas for a healthy breakfast"
- ✅ "Explain compound interest in simple terms"

**Avoid "alien" content the viewer has to decode:**

- ❌ Internal codenames, ticket IDs, or project acronyms.
- ❌ Deeply domain-specific prompts ("optimize the CUDA kernel for the attention
  block") unless the audience *is* that domain — and even then, prefer the simplest
  example that still shows the feature.
- ❌ Lorem ipsum or obvious placeholder junk — it signals "this is fake".
- ❌ Anything sensitive: real names, real customer data, secrets, private URLs.

**Match content to audience.** A developer-tools demo can be a little more technical
than a consumer app, but the rule holds: pick the *simplest input that still shows the
feature*. When in doubt, choose the more relatable example.

## Quick self-check before shooting

- Could someone who has never seen this product follow every caption?
- Is every typed input something a stranger would recognize?
- Does each caption say a *benefit*, not a mechanic?
- Does the last caption of each scene state the payoff?

If any answer is "no", fix the storyboard before you record — it's cheaper than a
re-shoot.
