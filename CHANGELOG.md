# Changelog

All notable changes to nolan are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Spoken narration (optional).** A new pluggable text-to-speech layer
  (`skills/nolan/scripts/narrate.py`) generates human-sounding voiceover and muxes it
  onto each scene's `.webm`, timed to the steps. Enable it with a top-level `voice`
  block and per-step (or per-scene) `vo` lines; steps with no `vo` speak their `cap`
  text. Providers: **ElevenLabs**, **OpenAI**, **Deepgram** (cloud, API key —
  most human), **Piper** (offline, open-source), macOS **say** (free), a **command**
  escape hatch for any other TTS, plus **auto** (best available) and **none** (silent).
  Muxing requires ffmpeg; if ffmpeg or the provider is unavailable the scene records
  silent with a warning. New reference: `reference/narration.md`.

## [0.1.0] — 2026-08-17

First public release.

### Added
- **The nolan skill** (`skills/nolan/`) with three stages — **Storyboard**, **Record**,
  **Polish** — and four disciplines: product-manager voice (not a smoke test), everyday
  relatable on-screen content, show-then-say (title cards + baked-in captions), and
  complete takes on the real app (wait for every action to finish).
- **Storyboard-driven recorder** `skills/nolan/scripts/record.py` — a JSON storyboard
  interpreter that drives a live app with Playwright, injects a title-card + subtitle
  overlay, waits on completion markers, and saves one `.webm` per scene.
- **Progressive-disclosure reference docs** (`skills/nolan/reference/`): `storyboard.md`,
  `recording.md`, `pm-voice.md`, `captions.md`, `polish.md`.
- **Storyboard template** (`skills/nolan/assets/storyboard-template.json`).
- **Plugin packaging**: `.claude-plugin/plugin.json` and `marketplace.json` so nolan can
  be installed via `/plugin marketplace add pur4v/nolan`.
- **Slash commands**: `/nolan:storyboard`, `/nolan:record`, `/nolan:polish`.
- **Sub-agent**: `storyboarder` (drafts a shoot-ready storyboard from a feature + URL).
- **Fictional worked example** under `examples/quill/`.
- Project docs: `README`, `SECURITY`, `CONTRIBUTING`, `CODE_OF_CONDUCT`, and CI.

[Unreleased]: https://github.com/pur4v/nolan/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/pur4v/nolan/releases/tag/v0.1.0
