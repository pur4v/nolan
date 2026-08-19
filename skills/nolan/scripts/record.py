#!/usr/bin/env python3
"""nolan — record product-demo videos from a storyboard by driving a live app.

Reads a storyboard JSON, drives the real UI with Playwright, overlays full-screen
title cards + baked-in subtitle captions (product-manager voice), waits for each
action to fully complete, and saves one .webm per scene.

Usage:
    python3 record.py storyboard.json [scene-name ...]     # no names = all scenes

Optional spoken narration: add a `voice` block to the storyboard and `vo` lines to
scenes/steps, and each scene gets human-sounding audio muxed in (see narrate.py).

Storyboard shape and the full step reference live in
../reference/storyboard.md. Prerequisites:
    pip install playwright && playwright install chromium
    # for narration audio only: ffmpeg (macOS: brew install ffmpeg)
"""
import json
import subprocess
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit(
        "Playwright is not installed. Run:\n"
        "    pip install playwright && playwright install chromium"
    )

import narrate  # sibling module: optional spoken narration (see narrate.py)

# ---- injected overlay: a top subtitle banner + a full-screen title card ------
# Exposes window.__cap(text) and window.__card(title, sub) on the page so the
# captions are baked into the recording (no post-production).
INJECT = r"""
(([accent]) => {
  if (window.__nolanInit) return; window.__nolanInit = true;
  const F = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif";
  const bar = document.createElement('div');
  bar.style.cssText =
    "position:fixed;top:24px;left:50%;transform:translateX(-50%);max-width:86%;"+
    "background:rgba(17,24,39,.94);color:#fff;font:600 18px/1.45 "+F+";"+
    "padding:11px 20px;border-radius:10px;z-index:2147483646;text-align:center;"+
    "white-space:nowrap;box-shadow:0 8px 26px rgba(0,0,0,.30);opacity:0;"+
    "transition:opacity .3s;pointer-events:none;";
  document.body.appendChild(bar);
  window.__cap = (t) => { if(!t){bar.style.opacity='0';return;} bar.textContent=t; bar.style.opacity='1'; };
  const card = document.createElement('div');
  card.style.cssText =
    "position:fixed;inset:0;z-index:2147483647;display:flex;flex-direction:column;"+
    "align-items:center;justify-content:center;background:#0d0f13;color:#fff;"+
    "opacity:0;transition:opacity .4s;pointer-events:none;font-family:"+F+";";
  card.innerHTML =
    "<div style='display:flex;align-items:center;gap:12px;margin-bottom:18px'>"+
    "<div style='width:14px;height:14px;border-radius:4px;background:"+accent+"'></div>"+
    "<div id='__np' style='font-size:30px;font-weight:800;letter-spacing:-.5px'></div></div>"+
    "<div id='__ct' style='font-size:40px;font-weight:800;letter-spacing:-1px;text-align:center;padding:0 40px'></div>"+
    "<div id='__cs' style='font-size:20px;color:#98a2b3;margin-top:14px;text-align:center;padding:0 60px'></div>";
  document.body.appendChild(card);
  window.__card = (t, s) => {
    if (t === undefined || t === null) { card.style.opacity='0'; return; }
    card.querySelector('#__ct').textContent = t;
    card.querySelector('#__cs').textContent = s || '';
    card.style.opacity = '1';
  };
  window.__nolanProduct = (p) => { card.querySelector('#__np').textContent = p || ''; };
})
"""


def _locator(pg, spec):
    """Resolve an element spec ({role,name} | {placeholder} | {text} | {selector})."""
    if "role" in spec:
        return pg.get_by_role(spec["role"], name=spec["name"])
    if "placeholder" in spec:
        return pg.get_by_placeholder(spec["placeholder"])
    if "text" in spec:
        return pg.get_by_text(spec["text"]).last
    if "selector" in spec:
        return pg.locator(spec["selector"]).last
    raise ValueError(f"cannot locate element from spec: {spec}")


def _hold(pg, step):
    ms = step.get("hold", 0)
    if ms:
        pg.wait_for_timeout(ms)


def _do_step(pg, step, product):
    """Execute one storyboard step (an object with exactly one action key)."""
    if "card" in step:
        val = step["card"]
        if val is None:
            pg.evaluate("window.__card(null)")
        else:
            title, sub = (val + [""])[:2] if isinstance(val, list) else (val, "")
            pg.evaluate("(p)=>window.__nolanProduct(p)", product)
            pg.evaluate("([t,s])=>window.__card(t,s)", [title, sub or ""])
        _hold(pg, step)
        return

    if "cap" in step:
        pg.evaluate("(t)=>window.__cap(t)", step["cap"] or "")
        _hold(pg, step)
        return

    if "type" in step:
        spec = step["type"]
        el = _locator(pg, spec)
        el.click()
        el.press_sequentially(spec["text"], delay=spec.get("delay", 32))  # visible typing
        pg.wait_for_timeout(spec.get("pause", 700))
        if spec.get("submit"):
            el.press("Enter")
        _hold(pg, step)
        return

    if "click" in step:
        _locator(pg, step["click"]).click()
        _hold(pg, step)
        return

    if "select" in step:
        spec = step["select"]
        sel = pg.locator(spec["selector"]) if "selector" in spec else pg.locator("select").first
        sel.select_option(label=spec["label"])
        _hold(pg, step)
        return

    if "key" in step:
        pg.keyboard.press(step["key"])
        _hold(pg, step)
        return

    if "wait" in step:
        pg.wait_for_timeout(step["wait"])
        return

    if "wait_text" in step:
        _wait_text(pg, step["wait_text"], step.get("timeout", 150000))
        _hold(pg, step)
        return

    if "run" in step:
        print(f"     run: {step['run']}")
        subprocess.run(step["run"], shell=True)
        _hold(pg, step)
        return

    raise ValueError(f"unknown step: {step}")


def _wait_text(pg, text, timeout_ms):
    """Block until `text` appears (the completion marker), so nothing is clipped."""
    try:
        pg.get_by_text(text).last.wait_for(timeout=timeout_ms)
    except Exception:
        # Fallback: settle on the page text no longer changing.
        last, stable, t0 = "", 0, time.time()
        while (time.time() - t0) * 1000 < timeout_ms:
            pg.wait_for_timeout(1200)
            body = pg.inner_text("body")
            stable = stable + 1 if len(body) == len(last) else 0
            if stable >= 4:
                break
            last = body


def _step_line(step):
    """Per-step narration text: explicit `vo` → a `cap` string → nothing."""
    text = step.get("vo")
    if not text and isinstance(step.get("cap"), str):
        text = step["cap"]
    return str(text) if text and str(text).strip() else None


def _shoot(browser, sb, scene, out_dir, voice=None, provider=None):
    view = sb.get("viewport", {"width": 1280, "height": 800})
    accent = sb.get("accent", "#4b8bff")
    product = sb.get("product", "")
    print(f"[scene] {scene['name']} -> {scene['file']}")

    ctx = browser.new_context(viewport=view, record_video_dir=str(out_dir), record_video_size=view)
    pg = ctx.new_page()
    t0 = time.monotonic()  # ≈ when the video starts recording; narration offsets from here
    pg.goto(sb["url"], wait_until="networkidle")
    pg.wait_for_timeout(1200)
    pg.evaluate(f"({INJECT})([{json.dumps(accent)}])")

    # A scene-level `vo` (string or timed list) sets narration explicitly; else
    # collect per-step lines timed to when each step actually fires.
    scene_vo = narrate.scene_vo_lines(scene)
    lines = []
    for step in scene["steps"]:
        if scene_vo is None:
            text = _step_line(step)
            if text is not None:
                lines.append((time.monotonic() - t0, text))
        _do_step(pg, step, product)
    if scene_vo is not None:
        lines = scene_vo

    video_path = pg.video.path()
    ctx.close()  # finalizes the .webm
    dst = out_dir / scene["file"]
    if dst.exists():
        dst.unlink()
    Path(video_path).rename(dst)
    print(f"  saved {dst}")

    # Optional spoken narration, timed to the steps and muxed onto the .webm.
    if provider and provider[1] and lines:
        try:
            narrate.narrate_scene(dst, lines, voice, provider=provider)
        except Exception as e:  # narration is best-effort: never fail a good take
            print(f"     [narrate] skipped ({e})")


def main(argv):
    if not argv:
        sys.exit(__doc__)
    sb_path = Path(argv[0]).resolve()
    sb = json.loads(sb_path.read_text())
    out_dir = (sb_path.parent / sb.get("out_dir", ".")).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    wanted = argv[1:]
    scenes = sb["scenes"]
    if wanted:
        by_name = {s["name"]: s for s in scenes}
        missing = [n for n in wanted if n not in by_name]
        if missing:
            sys.exit(f"no such scene(s): {', '.join(missing)}")
        scenes = [by_name[n] for n in wanted]

    voice = sb.get("voice")
    provider = narrate.resolve_provider(voice)  # (name, fn) or (None, None); warns once
    if provider[1]:
        print(f"[voice] narration provider: {provider[0]}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for scene in scenes:
            _shoot(browser, sb, scene, out_dir, voice=voice, provider=provider)
        browser.close()
    print("done ->", out_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
