# Security & data handling

nolan is a Claude skill/plugin that records demo videos by driving a live web app with
Playwright. It runs a browser against a URL you give it and captures video. This document
covers how it treats your app and data, and how to report a problem.

## What nolan does with your data

- **It drives whatever URL you point it at.** nolan opens the app in your storyboard's
  `url`, performs the clicks/typing you scripted, and records the screen to a `.webm`.
  Point it only at apps you're allowed to film.
- **Local by default.** The recorder runs on your machine with your Playwright install.
  There is no nolan server, telemetry, or phone-home. Whatever appears on screen is
  captured into the video file you keep.
- **No bundled credentials.** Nothing in this repo contains real secrets or private URLs.
  The worked example under `examples/` is entirely fictional and not runnable as-is.
- **Rendered videos are git-ignored** so a recording you make inside this repo isn't
  committed by accident.

## Filming safely

Because a recording captures *everything on screen*, treat the shoot like publishing:

- **Never film sensitive data.** Use a demo/staging environment with fake data. Don't
  record real customer records, personal data, private dashboards, or anything you
  wouldn't put on a landing page.
- **No secrets on camera.** Watch for tokens in URLs, API keys in dev tools, autofilled
  passwords, or secrets in the app's own UI. Redact or use throwaway values.
- **The `run` step executes shell commands.** A storyboard can run a shell command
  mid-scene (e.g. to demo a service dropping). Only ever target a process **you own and
  started for the demo**. Never run a `run` step from a storyboard you didn't write and
  read. Review any third-party storyboard before shooting it.
- **Check the final video before sharing.** Watch it back — the recording is the artifact
  that leaves your machine.

## Reporting a vulnerability

If you find a security issue in nolan itself (for example, a code path that could run
unintended commands or capture data it shouldn't), please **do not open a public issue**.
Instead, open a [private security advisory](https://github.com/pur4v/nolan/security/advisories/new)
on the repository, or contact the maintainer directly. You'll get an acknowledgement as
soon as possible.

Please include: what you observed, steps to reproduce, and the impact you're concerned
about.
