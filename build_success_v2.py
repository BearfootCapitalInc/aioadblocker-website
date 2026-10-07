#!/usr/bin/env python3
"""Build success_v2.html from success_live.html (production snapshot).

Adds a "60-second tour" tutorial section between the hero and the footer:
3 numbered cards teaching (1) the popup counters, (2) per-site disable
instead of uninstalling — the money step, (3) everything is reversible.
Everything else is untouched.
"""
import sys

src = open('success_live.html').read()

CSS = """
      /* ── 60-second tour (tutorial) ───────────────────────── */
      .tour { padding: 10px 0 70px; position: relative; z-index: 2; }
      .tour-title { text-align: center; font-family: 'Courier New', monospace; font-size: 12px; letter-spacing: 3px; color: var(--green); text-transform: uppercase; margin-bottom: 26px; }
      .tour-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; max-width: 980px; margin: 0 auto; }
      .tour-card { position: relative; background: rgba(20,48,74,0.45); border: 1px solid var(--border); border-radius: 14px; padding: 24px 22px 22px; text-align: left; }
      .tour-card.tour-star { border-color: var(--green); background: rgba(61,220,132,0.07); box-shadow: 0 10px 34px rgba(61,220,132,0.12); }
      .tour-badge { position: absolute; top: -11px; left: 20px; background: var(--green); color: var(--bg); font-size: 11px; font-weight: 800; letter-spacing: 0.6px; text-transform: uppercase; padding: 3px 10px; border-radius: 999px; }
      .tour-num { width: 28px; height: 28px; border-radius: 50%; background: rgba(125,255,212,0.12); border: 1px solid var(--border); color: var(--cyan); font-weight: 800; font-size: 14px; display: flex; align-items: center; justify-content: center; margin-bottom: 14px; }
      .tour-card h3 { font-size: 16.5px; font-weight: 800; color: white; margin: 14px 0 8px; letter-spacing: -0.2px; }
      .tour-card p { font-size: 13.5px; color: var(--text-mute); line-height: 1.55; margin: 0; }
      .tour-card p strong { color: var(--text); }
      /* mini popup mock-ups */
      .mock { background: #0d2138; border: 1px solid rgba(125,255,212,0.22); border-radius: 10px; padding: 12px 14px; box-shadow: 0 8px 22px rgba(0,0,0,0.35); }
      .mock-row { display: flex; align-items: center; gap: 9px; }
      .mock-shield { width: 18px; height: 21px; flex-shrink: 0; }
      .mock-kv { font-size: 12px; color: var(--text-mute); }
      .mock-kv b { color: var(--green); font-size: 15px; font-weight: 800; }
      .mock-count { margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(125,255,212,0.12); }
      .mock-btn { display: block; text-align: center; background: rgba(255,122,89,0.14); border: 1px solid rgba(255,122,89,0.45); color: #ffb3a0; font-size: 12.5px; font-weight: 700; border-radius: 8px; padding: 9px 10px; margin-top: 10px; }
      .mock-toggle { display: flex; align-items: center; justify-content: space-between; margin-top: 10px; }
      .mock-toggle-label { font-size: 12px; color: var(--text); font-weight: 600; }
      .mock-pill { width: 40px; height: 22px; border-radius: 999px; background: var(--green); position: relative; }
      .mock-pill::after { content: ""; position: absolute; top: 2px; right: 2px; width: 18px; height: 18px; border-radius: 50%; background: var(--bg); }
      @media (max-width: 880px) { .tour-grid { grid-template-columns: 1fr; max-width: 440px; } }
  """

i = src.rindex('</style>')
src = src[:i] + CSS + '\n' + src[i:]

SHIELD = ('<svg class="mock-shield" viewBox="0 0 100 116"><path d="M 50,4 L 94,20 Q 94,76 50,112 Q 6,76 6,20 Z" fill="#1E3A6B"/>'
          '<path d="M 50,14 L 82,26 Q 82,68 50,98 Q 18,68 18,26 Z" fill="#2D5AA0"/>'
          '<path d="M 50,24 L 72,32 Q 72,60 50,82 Q 28,60 28,32 Z" fill="#4A8BDF"/></svg>')

TOUR = f"""
<section class="tour">
\t<div class="container">
\t\t<div class="tour-title">[ Your 60-second tour ]</div>
\t\t<div class="tour-grid">

\t\t\t<div class="tour-card">
\t\t\t\t<div class="tour-num">1</div>
\t\t\t\t<div class="mock">
\t\t\t\t\t<div class="mock-row">{SHIELD}<span class="mock-kv">Blocked on this page&nbsp; <b>12</b></span></div>
\t\t\t\t\t<div class="mock-kv mock-count">Blocked in total&nbsp; <b>48,213</b></div>
\t\t\t\t</div>
\t\t\t\t<h3>Your shield lives in the toolbar</h3>
\t\t\t\t<p>Click the AIO icon on any site to see how many ads and trackers were just blocked — on that page, and in total.</p>
\t\t\t</div>

\t\t\t<div class="tour-card tour-star">
\t\t\t\t<div class="tour-badge">Most useful tip</div>
\t\t\t\t<div class="tour-num">2</div>
\t\t\t\t<div class="mock">
\t\t\t\t\t<div class="mock-row">{SHIELD}<span class="mock-kv">example-site.com</span></div>
\t\t\t\t\t<span class="mock-btn">Disable on this site</span>
\t\t\t\t</div>
\t\t\t\t<h3>Site acting weird? Pause, don't uninstall</h3>
\t\t\t\t<p>Very rarely, a site misbehaves with an adblocker on. Click the AIO icon → <strong>Disable on this site</strong>. AIO switches off for that one site only — everything else stays protected.</p>
\t\t\t</div>

\t\t\t<div class="tour-card">
\t\t\t\t<div class="tour-num">3</div>
\t\t\t\t<div class="mock">
\t\t\t\t\t<div class="mock-toggle"><span class="mock-toggle-label">Protection</span><span class="mock-pill"></span></div>
\t\t\t\t\t<div class="mock-toggle"><span class="mock-toggle-label" style="color:var(--text-mute)">On this site</span><span class="mock-pill" style="background:rgba(125,255,212,0.25)"></span></div>
\t\t\t\t</div>
\t\t\t\t<h3>Everything's reversible</h3>
\t\t\t\t<p>The same button turns protection back on. The big switch pauses AIO everywhere — so there's never a reason to uninstall just to switch it off.</p>
\t\t\t</div>

\t\t</div>
\t</div>
</section>
"""

anchor = '</section>\n\n<footer>'
if anchor not in src: sys.exit('footer anchor not found')
src = src.replace(anchor, '</section>\n' + TOUR + '\n<footer>', 1)

open('success_v2.html', 'w').write(src)
print(f'success_v2.html written: {len(src)} bytes')
