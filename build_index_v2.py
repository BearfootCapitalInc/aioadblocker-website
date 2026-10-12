#!/usr/bin/env python3
"""Build index_v2.html from index_live.html (production snapshot).

Three claim corrections (2026-10-12): the landing page promised "no tracking /
zero data collected / we don't log the pages you visit", which contradicts the
extension's disclosed domain-level diagnostics and the amended privacy policy.
Reworded to keep the marketing punch while staying truthful: no selling, no
profiling, domain-level diagnostics only.
"""
import sys

src = open('index_live.html').read()
edits = 0

def rep(old, new):
    global src, edits
    if src.count(old) != 1: sys.exit(f'ANCHOR BAD (count={src.count(old)}): {old[:70]}')
    src = src.replace(old, new)
    edits += 1

# ── ① Hero claim
rep('Free forever. No pop-ups. No tracking. No data collected about you. Install in ten seconds and get your internet back.',
    'Free forever. No pop-ups. No selling your data. No profiling. Install in ten seconds and get your internet back.')

# ── ② Comparison table row
rep('<td>Zero data collected about you</td>',
    '<td>Never sells or shares your data</td>')

# ── ③ Competitor paragraph — the mocking setup stays, but our counter-claims
#     become exactly what the privacy policy says we do.
rep("<p><strong>AIO doesn't do any of that.</strong> We don't read what you browse. We don't log the pages you visit. We don't track what you click. We don't ask for your email. We don't build a profile of who you are. The extension lives on your computer and stays there.</p>",
    "<p><strong>AIO doesn't do any of that.</strong> We never see full addresses, page content, searches, or what you click. We don't ask for your email. We don't build a profile of who you are. The only thing that ever leaves your computer is anonymous, domain-level diagnostics that help us fix broken sites — never sold, never shared with anyone.</p>")

open('index_v2.html', 'w').write(src)
print(f'index_v2.html written: {len(src)} bytes, {edits} edits applied')
