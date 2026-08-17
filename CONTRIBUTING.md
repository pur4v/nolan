# Contributing to nolan

Thanks for wanting to help. nolan is a small, focused skill — the goal is to keep it
sharp, not sprawling. Contributions that make demos more *watchable* and more
*trustworthy to a first-time viewer* are especially welcome.

## Ground rules

1. **Never commit real secrets, private URLs, or customer data.** This is a public repo.
   All examples must be fictional (see `examples/quill/`). Videos are git-ignored — don't
   commit rendered `.webm`/`.mp4` files.
2. **Keep the four disciplines intact.** Every change should preserve: product-manager
   voice (not a smoke test), everyday relatable on-screen content, show-then-say (title
   cards + captions), and complete takes (wait for actions to finish). These are the point
   of the project.
3. **Progressive disclosure.** `SKILL.md` stays lean; depth goes in
   `skills/nolan/reference/`. Don't inline a long procedure into `SKILL.md` — add or
   extend a reference file and point to it.

## Project layout

```
.claude-plugin/    plugin.json + marketplace.json (plugin install)
commands/          slash commands: /nolan:storyboard, :record, :polish
agents/            storyboarder — drafts a shoot-ready storyboard
skills/nolan/      the skill itself — SKILL.md, reference/, scripts/, assets/
examples/          fictional worked storyboard
```

## Making a change

1. Fork and branch (`feat/…`, `fix/…`, `docs/…`).
2. Make the change. If you touch `skills/nolan/scripts/record.py`, run
   `python3 -m py_compile skills/nolan/scripts/record.py` — CI does too.
3. If you add or change a storyboard step, update `reference/storyboard.md` **and** the
   recorder, and add it to `assets/storyboard-template.json` if it's common.
4. If you change a stage's behavior, update the matching `reference/*.md` and, if
   user-facing, the `commands/*.md` and `README.md`.
5. Add a line to `CHANGELOG.md` under **Unreleased**.
6. Open a PR using the template. Describe what changed and how you verified it (ideally:
   shot a storyboard against a local app and watched it back).

## Style

- Markdown, wrapped ~100 cols, tables/checklists over walls of prose.
- Be concrete. If you claim nolan does something, show the reference file that makes it so.

## Code of conduct

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
