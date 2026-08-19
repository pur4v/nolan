#!/usr/bin/env python3
"""nolan — generate human-sounding narration and mux it onto recorded scenes.

Narration is spoken product explanation, timed to the on-screen steps. This module
is a small *pluggable* text-to-speech layer: pick a provider in the storyboard's
`voice` block, and each scene's lines are synthesized and mixed onto its `.webm`.

Providers (extensible — see PROVIDERS):
    Cloud (most human, need an API key + network):
        elevenlabs   ELEVENLABS_API_KEY   voice_id, model
        openai       OPENAI_API_KEY       voice, model
        deepgram     DEEPGRAM_API_KEY     model
    Free / open-source / offline:
        piper        (the `piper` binary + a .onnx voice model in voice_id)
        say          (macOS built-in `say`; robotic but zero-setup)
    Escape hatch (bring your own TTS):
        command      run any CLI: cfg["command"] with {text} and {out} placeholders

Where narration text comes from, per step (first that exists wins):
    step["vo"]  ->  a `cap` step's string  ->  (nothing)
A scene-level `"vo"` string, if present, is spoken once at the top instead.

Muxing requires ffmpeg (audio track is libopus, to stay inside .webm). If ffmpeg
or the chosen provider is unavailable, the scene is simply left silent and a
warning is printed — recording never fails because of audio.

Usage (standalone: add scene-level narration to already-recorded scenes):
    python3 narrate.py storyboard.json [scene-name ...]
record.py imports resolve_provider() / narrate_scene() for step-timed narration.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

# --- HTTP helper (stdlib only, no extra pip deps) ----------------------------


def _post(url, data, headers, timeout=120):
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


# --- providers: each writes audio for `text` to `out` (any ffmpeg-readable ----
# format) and returns True, or returns False if it could not produce audio. ---


def _p_elevenlabs(text, cfg, out):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        return False
    voice = cfg.get("voice_id", "21m00Tcm4TlvDq8ikWAM")  # "Rachel" default
    model = cfg.get("model", "eleven_multilingual_v2")
    body = json.dumps({"text": text, "model_id": model}).encode()
    audio = _post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}",
        body,
        {"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
    )
    out.write_bytes(audio)
    return True


def _p_openai(text, cfg, out):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return False
    body = json.dumps(
        {
            "model": cfg.get("model", "gpt-4o-mini-tts"),
            "voice": cfg.get("voice", cfg.get("voice_id", "alloy")),
            "input": text,
        }
    ).encode()
    audio = _post(
        "https://api.openai.com/v1/audio/speech",
        body,
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    out.write_bytes(audio)
    return True


def _p_deepgram(text, cfg, out):
    key = os.environ.get("DEEPGRAM_API_KEY")
    if not key:
        return False
    model = cfg.get("model", cfg.get("voice_id", "aura-asteria-en"))
    audio = _post(
        f"https://api.deepgram.com/v1/speak?model={model}",
        json.dumps({"text": text}).encode(),
        {"Authorization": f"Token {key}", "Content-Type": "application/json"},
    )
    out.write_bytes(audio)
    return True


def _p_piper(text, cfg, out):
    """Open-source neural TTS. voice_id is the path to a .onnx voice model."""
    if not shutil.which("piper"):
        return False
    model = cfg.get("voice_id") or cfg.get("model")
    if not model:
        print("     [narrate] piper needs voice_id = path to a .onnx voice model")
        return False
    subprocess.run(
        ["piper", "--model", model, "--output_file", str(out)],
        input=text.encode(),
        check=True,
    )
    return True


def _p_say(text, cfg, out):
    """macOS built-in TTS. Free and offline; not truly human, but zero-setup."""
    if not shutil.which("say"):
        return False
    cmd = ["say", "-o", str(out), "--data-format=LEF32@22050"]
    if cfg.get("rate"):
        cmd += ["-r", str(cfg["rate"])]
    if cfg.get("voice_id") or cfg.get("voice"):
        cmd += ["-v", str(cfg.get("voice_id") or cfg.get("voice"))]
    cmd.append(text)
    subprocess.run(cmd, check=True)
    return True


def _p_command(text, cfg, out):
    """Bring your own TTS: cfg['command'] is a shell template with {text}/{out}."""
    tmpl = cfg.get("command")
    if not tmpl:
        print("     [narrate] provider 'command' needs a 'command' template")
        return False
    import shlex

    cmd = tmpl.format(text=shlex.quote(text), out=shlex.quote(str(out)))
    subprocess.run(cmd, shell=True, check=True)
    return out.exists() and out.stat().st_size > 0


PROVIDERS = {
    "elevenlabs": _p_elevenlabs,
    "openai": _p_openai,
    "deepgram": _p_deepgram,
    "piper": _p_piper,
    "say": _p_say,
    "command": _p_command,
}

# Order tried when provider is "auto": best-sounding available wins.
_AUTO_ORDER = ["elevenlabs", "openai", "deepgram", "piper", "say"]


def _available(name, cfg):
    """Cheap check: can this provider plausibly run right now?"""
    if name == "elevenlabs":
        return bool(os.environ.get("ELEVENLABS_API_KEY"))
    if name == "openai":
        return bool(os.environ.get("OPENAI_API_KEY"))
    if name == "deepgram":
        return bool(os.environ.get("DEEPGRAM_API_KEY"))
    if name == "piper":
        return bool(shutil.which("piper") and (cfg.get("voice_id") or cfg.get("model")))
    if name == "say":
        return bool(shutil.which("say"))
    if name == "command":
        return bool(cfg.get("command"))
    return False


def resolve_provider(voice):
    """Return (name, fn) for the configured voice, or (None, None) to stay silent.

    Honors an explicit `provider`; "auto" (or unset) picks the best available free
    or keyed provider. "none"/"off" means: produce no audio.
    """
    if not voice:
        return None, None
    name = (voice.get("provider") or "auto").lower()
    if name in ("none", "off", "silent"):
        return None, None
    if name == "auto":
        for cand in _AUTO_ORDER:
            if _available(cand, voice):
                return cand, PROVIDERS[cand]
        print("     [narrate] no TTS provider available — leaving scenes silent")
        return None, None
    fn = PROVIDERS.get(name)
    if not fn:
        print(f"     [narrate] unknown voice provider '{name}' — leaving silent")
        return None, None
    if not _available(name, voice):
        print(f"     [narrate] provider '{name}' is not usable here — leaving silent")
        return None, None
    return name, fn


# --- muxing ------------------------------------------------------------------


def _mux(video, clips, tmp):
    """Overlay timed audio `clips` [(offset_sec, path)] onto `video` in place.

    Returns True on success. Requires ffmpeg; the audio track is written as
    libopus so the file stays a valid .webm.
    """
    if not shutil.which("ffmpeg"):
        print("     [narrate] ffmpeg not found — install it to add audio "
              "(macOS: brew install ffmpeg). Scene left silent.")
        return False
    if not clips:
        return False

    cmd = ["ffmpeg", "-y", "-i", str(video)]
    for _, path in clips:
        cmd += ["-i", str(path)]

    parts, labels = [], []
    for i, (off, _) in enumerate(clips):
        ms = max(0, int(off * 1000))
        parts.append(f"[{i + 1}:a]adelay={ms}:all=1[a{i}]")
        labels.append(f"[a{i}]")
    if len(clips) == 1:
        filt, out_label = parts[0], "[a0]"
    else:
        filt = ";".join(parts) + ";" + "".join(labels) + \
            f"amix=inputs={len(clips)}:normalize=0[aout]"
        out_label = "[aout]"

    dst = tmp / ("muxed-" + Path(video).name)
    cmd += [
        "-filter_complex", filt,
        "-map", "0:v", "-map", out_label,
        "-c:v", "copy", "-c:a", "libopus", str(dst),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("     [narrate] ffmpeg mux failed; scene left silent:\n"
              + proc.stderr.strip()[-800:])
        return False
    dst.replace(video)
    return True


# --- the public entry point --------------------------------------------------


def narrate_scene(video, lines, voice, provider=None):
    """Synthesize `lines` and mux them onto `video`.

    `lines` is a list of (offset_seconds, text). `provider` may be a pre-resolved
    (name, fn) tuple to avoid re-resolving per scene. Returns True if audio landed.
    """
    lines = [(off, t.strip()) for off, t in lines if t and t.strip()]
    if not lines:
        return False
    name, fn = provider if provider else resolve_provider(voice)
    if not fn:
        return False
    if not shutil.which("ffmpeg"):
        print("     [narrate] ffmpeg not found — install it to add audio "
              "(macOS: brew install ffmpeg). Scene left silent.")
        return False

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        clips = []
        for i, (off, text) in enumerate(lines):
            # .wav so macOS `say` picks a container; ffmpeg probes others by content.
            audio = tmp / f"vo-{i:02d}.wav"
            try:
                if fn(text, voice, audio) and audio.exists() and audio.stat().st_size:
                    clips.append((off, audio))
                else:
                    print(f"     [narrate] {name}: no audio for line {i}")
            except (urllib.error.URLError, subprocess.CalledProcessError, OSError) as e:
                print(f"     [narrate] {name} failed on line {i}: {e}")
        if not clips:
            return False
        ok = _mux(video, clips, tmp)
        if ok:
            print(f"     [narrate] {name}: added {len(clips)} line(s) of audio")
        return ok


# --- standalone CLI: scene-level narration for already-recorded scenes -------


def _scene_lines(scene):
    """Scene-level narration for the standalone (post-hoc, untimed) path.

    Uses scene `vo` if present; else concatenates step `vo`/`cap` text. Everything
    plays from the top (offset 0), since step timing isn't known post-recording.
    """
    vo = scene.get("vo")
    if isinstance(vo, str) and vo.strip():
        return [(0.0, vo)]
    texts = []
    for step in scene.get("steps", []):
        t = step.get("vo")
        if not t and isinstance(step.get("cap"), str):
            t = step["cap"]
        if t and t.strip():
            texts.append(t.strip())
    return [(0.0, " ".join(texts))] if texts else []


def main(argv):
    if not argv:
        sys.exit(__doc__)
    sb_path = Path(argv[0]).resolve()
    sb = json.loads(sb_path.read_text())
    voice = sb.get("voice")
    name, fn = resolve_provider(voice)
    if not fn:
        sys.exit("no usable voice provider (set storyboard 'voice' + an API key/tool)")
    out_dir = (sb_path.parent / sb.get("out_dir", ".")).resolve()

    wanted = set(argv[1:])
    for scene in sb["scenes"]:
        if wanted and scene["name"] not in wanted:
            continue
        video = out_dir / scene["file"]
        if not video.exists():
            print(f"[narrate] skip {scene['name']}: {video} not recorded yet")
            continue
        print(f"[narrate] {scene['name']} -> {video.name}")
        narrate_scene(video, _scene_lines(scene), voice, provider=(name, fn))
    print("done ->", out_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
