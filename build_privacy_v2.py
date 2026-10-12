#!/usr/bin/env python3
"""Build privacy_v2.html from privacy_live.html (production snapshot).

Six surgical edits for the CWS "Purple Nickel" rejection (2026-10-12):
disclose domain-level diagnostics (blocking stats per page domain,
install/uninstall tab-domain snapshots), framed exclusively as debugging +
future-proofing, with an at-a-glance box, bounded retention, and a
qualified "what we do NOT collect" list. Everything else untouched.
"""
import sys, datetime

src = open('privacy_live.html').read()
edits = 0

def rep(old, new):
    global src, edits
    if old not in src: sys.exit('ANCHOR MISSING: ' + old[:80])
    if src.count(old) != 1: sys.exit('ANCHOR NOT UNIQUE: ' + old[:80])
    src = src.replace(old, new)
    edits += 1

# ── 0. Last Updated date
rep('<p><strong>Last Updated:</strong> May 18, 2026</p>',
    '<p><strong>Last Updated:</strong> October 12, 2026</p>')

# ── ① At-a-glance box after the §2 summary list
rep("""	<p>The remainder of this Policy provides the legal detail underlying the summary above.</p>""",
    """	<p><strong>At a glance:</strong> We collect: an anonymous Installation ID, extension version, browser and OS type, language, and domain-level diagnostics (domain names only — never full URLs, page content, or anything you type). Why: debugging, site-compatibility fixes, and future-proofing our filters — nothing else. Storage: secured servers; diagnostic data kept for a maximum of twelve (12) months. Sharing and sales: none — never sold, never shared with advertisers or data brokers.</p>
	<p>The remainder of this Policy provides the legal detail underlying the summary above.</p>""")

# ── ② Replace the "Aggregate blocking statistics" bullet
rep("""<li><strong>Aggregate blocking statistics</strong> — the number of advertisements, trackers, or network requests blocked. These counts are aggregated and are not associated with the specific sites, URLs, or content involved.</li>""",
    """<li><strong>Blocking statistics</strong> — counts of blocked advertisements, trackers, and network requests, together with the domain name of the page on which the blocking occurred (strictly the domain name only, e.g. example.com — never URL paths, full addresses, or page content). Collected exclusively to debug our filters and future-proof them against changing ad-delivery techniques.</li>
		<li><strong>Domains present at installation and uninstallation</strong> — at those two moments we record the domain names of the tabs open in your browser and of recently adjusted site preferences (strictly domain names only — never URL paths or full addresses). Used exclusively to debug site-compatibility problems and to understand uninstall feedback.</li>""")

# ── ④ Qualify the first "do NOT collect" bullet
rep('<li>The specific URLs of pages you visit;</li>',
    '<li>The full URLs of pages you visit (we only ever process domain names, as described in Section 3.1);</li>')

# ── ⑤ New purpose bullet in §4
rep("""<li><strong>To Maintain and Improve the Extension</strong> — to debug errors, analyze aggregate usage trends, and improve performance, stability, and security.</li>""",
    """<li><strong>To Maintain and Improve the Extension</strong> — to debug errors, analyze aggregate usage trends, and improve performance, stability, and security.</li>
		<li><strong>To Debug and Future-Proof the Extension</strong> — domain-level diagnostics described in Section 3.1 are used exclusively to identify and fix websites where the Extension malfunctions or under-blocks, and to adapt our filters to evolving advertising infrastructure. They are never used for profiling, advertising, or any other purpose.</li>""")

# ── ⑥ Retention line in §7
rep("""<li><strong>Website server logs:</strong> IP addresses anonymized within ninety (90) days.</li>""",
    """<li><strong>Domain-level diagnostic data</strong> (blocking statistics and installation/uninstallation domain snapshots): retained for up to twelve (12) months from collection, after which it is deleted or irreversibly aggregated.</li>
		<li><strong>Website server logs:</strong> IP addresses anonymized within ninety (90) days.</li>""")

open('privacy_v2.html', 'w').write(src)
print(f'privacy_v2.html written: {len(src)} bytes, {edits} edits applied')
