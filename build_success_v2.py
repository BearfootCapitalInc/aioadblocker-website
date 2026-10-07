#!/usr/bin/env python3
"""Build success_v2.html from success_live.html (production snapshot).

Adds a "60-second tour" tutorial section between the hero and the footer:
3 numbered cards teaching (1) the popup counters, (2) per-site disable
instead of uninstalling — the money step, (3) everything is reversible.
Everything else is untouched.
"""
import sys

src = open('success_live.html').read()

# ── (J) Remove the "What happens now" card — the tour moves up in its place.
import re
src, n = re.subn(r'\s*<div class="what-now">.*?</ul>\s*</div>', '', src, count=1, flags=re.S)
if n != 1: sys.exit('what-now anchor not found')

CSS = """
      /* ── 60-second tour (tutorial) ───────────────────────── */
      .tour { padding: 6px 0 70px; position: relative; z-index: 2; }
      .tour-title { text-align: center; font-family: 'Courier New', monospace; font-size: 12px; letter-spacing: 3px; color: var(--green); text-transform: uppercase; margin-bottom: 26px; }
      .tour-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 1140px; margin: 0 auto; }
      /* wider page on big screens (J: stop hugging a narrow column) */
      @media (min-width: 1100px) { .container { max-width: 1140px; } .success-hero .container { max-width: 980px; } }
      .tour-card { position: relative; background: rgba(20,48,74,0.45); border: 1px solid var(--border); border-radius: 14px; padding: 24px 22px 22px; text-align: left; }
      .tour-card.tour-star { border-color: var(--green); background: rgba(61,220,132,0.07); box-shadow: 0 10px 34px rgba(61,220,132,0.12); }
      .tour-badge { position: absolute; top: -11px; left: 20px; background: var(--green); color: var(--bg); font-size: 11px; font-weight: 800; letter-spacing: 0.6px; text-transform: uppercase; padding: 3px 10px; border-radius: 999px; }
      .tour-num { width: 28px; height: 28px; border-radius: 50%; background: rgba(125,255,212,0.12); border: 1px solid var(--border); color: var(--cyan); font-weight: 800; font-size: 14px; display: flex; align-items: center; justify-content: center; margin-bottom: 14px; }
      .tour-card h3 { font-size: 16.5px; font-weight: 800; color: white; margin: 14px 0 8px; letter-spacing: -0.2px; }
      .tour-card p { font-size: 13.5px; color: var(--text-mute); line-height: 1.55; margin: 0; }
      .tour-card p strong { color: var(--text); }
      /* mini popup mock-ups — faithful to the real AIO popup:
         #020814 bg, #00FFB8 mint, monospace, square corners, SYS:: labels */
      .mock { background: #020814; border: 1px solid rgba(0,255,184,0.3); border-radius: 0; padding: 14px; box-shadow: 0 10px 26px rgba(0,0,0,0.5); font-family: ui-monospace, 'SF Mono', Menlo, Consolas, monospace; color: #E8F5FF; }
      .mock-head { display: flex; align-items: center; justify-content: space-between; font-size: 8px; letter-spacing: 2px; color: rgba(232,245,255,0.45); margin-bottom: 10px; }
      .mock-head .act { color: #00FFB8; }
      .mock-row { display: flex; align-items: center; gap: 9px; }
      .mock-shield { width: 18px; height: 21px; flex-shrink: 0; }
      .mock-name { font-size: 10px; font-weight: 700; letter-spacing: 2px; color: #E8F5FF; line-height: 1.5; }
      .mock-name .st { display: block; font-size: 8px; letter-spacing: 1.5px; color: #00FFB8; }
      .mock-hexwrap { text-align: center; margin: 6px 0 2px; }
      .mock-hexwrap svg { width: 86px; height: 86px; }
      .mock-cap { text-align: center; font-size: 8.5px; letter-spacing: 2px; color: #00FFB8; margin: 4px 0 10px; }
      .mock-stat { display: flex; align-items: center; justify-content: space-between; border: 1px dashed rgba(0,255,184,0.4); padding: 8px 10px; font-size: 8.5px; letter-spacing: 2px; color: #00FFB8; }
      .mock-stat b { font-size: 17px; letter-spacing: 0; color: #E8F5FF; font-weight: 700; }
      .mock-site { font-size: 10px; letter-spacing: 1px; color: rgba(232,245,255,0.75); margin: 10px 0 8px; }
      .mock-btn { display: block; text-align: center; background: rgba(0,255,184,0.08); border: 1px solid rgba(0,255,184,0.45); border-radius: 0; color: #00FFB8; font-size: 9px; font-weight: 600; letter-spacing: 2.4px; padding: 8px 10px; text-transform: uppercase; }
      .mock-allow { border: 1px dashed rgba(0,255,184,0.4); padding: 9px 10px 10px; margin-top: 12px; }
      .mock-allow-label { font-size: 8px; letter-spacing: 2px; color: #00FFB8; margin-bottom: 8px; }
      .mock-allow-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
      .mock-allow-row .site { font-size: 10px; letter-spacing: 1px; color: #E8F5FF; }
      .mock-allow-row .site::before { content: "\\2B22  "; color: #4DFFFF; font-size: 8px; }
      .mock-allow-btn { background: rgba(0,255,184,0.08); border: 1px solid rgba(0,255,184,0.45); color: #00FFB8; font-size: 9px; font-weight: 600; letter-spacing: 2.4px; padding: 5px 12px; }
      .mock-row.spread { justify-content: space-between; }
      .mock-ctrl { display: flex; align-items: center; gap: 10px; }
      .mock-gear { color: rgba(232,245,255,0.55); font-size: 15px; line-height: 1; }
      .mock-toggle { display: flex; align-items: center; justify-content: space-between; margin-top: 10px; }
      .mock-toggle:first-of-type { margin-top: 0; }
      .mock-toggle-label { font-size: 9px; letter-spacing: 2px; color: #00FFB8; }
      .mock-toggle-label.off { color: rgba(232,245,255,0.4); }
      .mock-pill { width: 40px; height: 20px; border-radius: 999px; background: #00FFB8; position: relative; flex-shrink: 0; }
      .mock-pill::after { content: ""; position: absolute; top: 2px; right: 2px; width: 16px; height: 16px; border-radius: 50%; background: #020814; }
      .mock-pill.off { background: rgba(232,245,255,0.18); }
      .mock-pill.off::after { right: auto; left: 2px; }
      @media (max-width: 880px) { .tour-grid { grid-template-columns: 1fr; max-width: 440px; } }
  """

i = src.rindex('</style>')
src = src[:i] + CSS + '\n' + src[i:]

SHIELD = ('<svg class="mock-shield" viewBox="0 0 100 116"><path d="M 50,4 L 94,20 Q 94,76 50,112 Q 6,76 6,20 Z" fill="#1E3A6B"/>'
          '<path d="M 50,14 L 82,26 Q 82,68 50,98 Q 18,68 18,26 Z" fill="#2D5AA0"/>'
          '<path d="M 50,24 L 72,32 Q 72,60 50,82 Q 28,60 28,32 Z" fill="#4A8BDF"/></svg>')

HEX = ('<svg viewBox="0 0 100 100"><polygon points="50,7 88,28 88,72 50,93 12,72 12,28" fill="none" stroke="#00FFB8" stroke-width="1.6"/>'
       '<circle cx="50" cy="7" r="2.4" fill="#00FFB8"/><circle cx="88" cy="28" r="2.4" fill="#00FFB8"/><circle cx="88" cy="72" r="2.4" fill="#00FFB8"/>'
       '<circle cx="50" cy="93" r="2.4" fill="#00FFB8"/><circle cx="12" cy="72" r="2.4" fill="#00FFB8"/><circle cx="12" cy="28" r="2.4" fill="#00FFB8"/>'
       '<text x="50" y="63" text-anchor="middle" font-size="38" fill="#E8F5FF" font-family="monospace" font-weight="700">12</text></svg>')

TOUR = f"""
<section class="tour">
\t<div class="container">
\t\t<div class="tour-title">[ Your 60-second tour ]</div>
\t\t<div class="tour-grid">

\t\t\t<div class="tour-card">
\t\t\t\t<div class="tour-num">1</div>
\t\t\t\t<div class="mock">
\t\t\t\t\t<div class="mock-head"><span>NODE.7F3C</span><span class="act">[ SYS.ACTIVE ]</span></div>
\t\t\t\t\t<div class="mock-hexwrap">{HEX}</div>
\t\t\t\t\t<div class="mock-cap">::BLOCKED // THIS PAGE::</div>
\t\t\t\t\t<div class="mock-stat"><span>&#9679; ALL.TIME.BLOCKED</span><b>48.2K</b></div>
\t\t\t\t</div>
\t\t\t\t<h3>Your shield lives in the toolbar</h3>
\t\t\t\t<p>Click the AIO icon on any site to watch it work — ads and trackers blocked on that page, plus your all-time count climbing.</p>
\t\t\t</div>

\t\t\t<div class="tour-card tour-star">
\t\t\t\t<div class="tour-badge">Most useful tip</div>
\t\t\t\t<div class="tour-num">2</div>
\t\t\t\t<div class="mock">
\t\t\t\t\t<div class="mock-head"><span>NODE.7F3C</span><span class="act">[ SYS.ACTIVE ]</span></div>
\t\t\t\t\t<div class="mock-row">{SHIELD}<span class="mock-name">ALL-IN-ONE<span class="st">&#9679; SYS::PROTECTED</span></span></div>
\t\t\t\t\t<div class="mock-allow">
\t\t\t\t\t\t<div class="mock-allow-label">ALLOW ADS ON SITE</div>
\t\t\t\t\t\t<div class="mock-allow-row"><span class="site">example-site.com</span><span class="mock-allow-btn">ALLOW</span></div>
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t<h3>You decide where AIO runs</h3>
\t\t\t\t<p>A site acting up? Click the AIO icon and hit <strong>Allow</strong> next to the site's name. AIO steps aside on that one site — and keeps protecting you everywhere else.</p>
\t\t\t</div>

\t\t\t<div class="tour-card">
\t\t\t\t<div class="tour-num">3</div>
\t\t\t\t<div class="mock">
\t\t\t\t\t<div class="mock-head"><span>NODE.7F3C</span><span class="act">[ SYS.ACTIVE ]</span></div>
\t\t\t\t\t<div class="mock-row spread">
\t\t\t\t\t\t<div class="mock-row">{SHIELD}<span class="mock-name">ALL-IN-ONE<span class="st">&#9679; SYS::PROTECTED</span></span></div>
\t\t\t\t\t\t<div class="mock-ctrl"><span class="mock-gear">&#9881;</span><span class="mock-pill"></span></div>
\t\t\t\t\t</div>
\t\t\t\t</div>
\t\t\t\t<h3>You're always in control</h3>
\t\t\t\t<p>Changed your mind about a site? Hit its button again to re-protect it. And the switch at the top of the popup pauses everything at once. Your browsing, your rules.</p>
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
