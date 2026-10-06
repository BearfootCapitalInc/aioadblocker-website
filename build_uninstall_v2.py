#!/usr/bin/env python3
"""Build uninstall_v2.html from uninstall_live.html (production snapshot).

Three surgical patches:
  1. CSS: site-picker styles appended before </style>
  2. HTML: site-picker block inserted at the top of #fb-extra
  3. JS: main IIFE replaced — full exit-beacon parsing, site chips,
     partial beacon, context forwarded to /uninstall/feedback/
Everything else (tracking iframe, localStorage.clear, chip shuffle) is untouched.
"""
import re, sys

src = open('uninstall_live.html').read()

# ───────────────────────── 1. CSS ─────────────────────────
CSS = """
      /* ── Site picker ("which site was it?") ───────────────── */
      .site-picker { display: none; margin: 0 0 18px; padding: 16px 18px; background: rgba(10,24,40,0.45); border: 1px solid var(--border-warn); border-radius: 12px; }
      .site-picker.show { display: block; animation: fade-up 0.3s ease; }
      .site-q { margin-bottom: 10px; }
      .site-q-title { display: block; font-size: 14px; font-weight: 700; color: var(--text); }
      .site-q-sub { display: block; font-size: 12px; font-weight: 500; color: var(--text-mute); margin-top: 2px; }
      .site-grid { display: flex; flex-wrap: wrap; gap: 8px; }
      .site-chip { padding: 8px 14px; background: rgba(26,52,80,0.55); border: 1px solid var(--border); border-radius: 999px; color: var(--text); font-size: 13px; font-weight: 600; font-family: inherit; cursor: pointer; transition: all 0.15s; }
      .site-chip:hover { border-color: rgba(255,122,89,0.55); color: #fff; }
      .site-chip.selected { background: rgba(255,122,89,0.18); border-color: var(--warn); color: #fff; box-shadow: 0 0 0 1px var(--warn); }
      #site-other-input { display: none; margin: 10px 0 0; }
      #site-other-input.show { display: block; }
  """

i = src.rindex('</style>')
src = src[:i] + CSS + '\n' + src[i:]

# ───────────────────────── 2. HTML ─────────────────────────
PICKER = """
\t\t\t\t<div class="site-picker" id="site-picker">
\t\t\t\t\t<div class="site-q">
\t\t\t\t\t\t<span class="site-q-title" id="site-q-title">Which site was it?</span>
\t\t\t\t\t\t<span class="site-q-sub">Tap all that apply — we only see site names, never what you did there.</span>
\t\t\t\t\t</div>
\t\t\t\t\t<div class="site-grid" id="site-grid"></div>
\t\t\t\t\t<input id="site-other-input" type="text" placeholder="example.com" autocomplete="off" spellcheck="false">
\t\t\t\t</div>
"""

m = re.search(r'(<div class="fb-extra" id="fb-extra">\s*\n)', src)
if not m: sys.exit('fb-extra anchor not found')
src = src[:m.end()] + PICKER + src[m.end():]

# ───────────────────────── 3. JS ─────────────────────────
JS = r"""
    (() => {
        // Server-rendered reinstall URL — goes through our LP (version 11 +
        // reinstall/orgreinstall campaign) which redirects to the CWS listing.
        const CWS_URL = "https:\/\/aioadblocker.com\/rinsorg\/";
        const FEEDBACK_ENDPOINT = '/uninstall/feedback/';

        // ── Exit beacon (chrome.runtime.setUninstallURL, built in the
        //    extension's core/warden.js). Every param is optional — the
        //    page must work with a bare /uninstall/ hit too.
        //    a_tkn  backend UID            sx     store/extension id
        //    v      extension version      cfgv   remote-config version
        //    lists  enabled rulesets       blk    total blocked count
        //    age    install age (days)     lang   extension-side language
        //    cur    domain user was on     prev   domain before that
        //    wl     last whitelisted dom.  wlm    minutes since whitelisting
        //    tabs   open-tab domains, MRU first (may be truncated to fit
        //           Chrome's 1023-char uninstall-URL cap)
        //    tabn   true open-tab count even when tabs was truncated
        const qs   = new URLSearchParams(location.search);
        const aTkn = qs.get('a_tkn') || null;
        const sx   = qs.get('sx')    || null;

        const ctx = {};
        ['v','cfgv','lists','blk','age','lang','cur','prev','wl','wlm','tabn'].forEach(k => {
            const val = qs.get(k);
            if (val !== null && val !== '') ctx[k] = val;
        });
        const tabs = (qs.get('tabs') || '').split(',').map(s => s.trim()).filter(Boolean);
        if (tabs.length) ctx.tabs = tabs;

        // Suspect sites for the picker, strongest signal first: the domain
        // they just left (cur), the one before (prev), the last site they
        // whitelisted (wl), then the rest of their open tabs (already MRU).
        const SUSPECTS = [];
        [ctx.cur, ctx.prev, ctx.wl, ...tabs].forEach(h => {
            if (h && !SUSPECTS.includes(h)) SUSPECTS.push(h);
        });
        const MAX_SITE_CHIPS = 12;

        // Per-pageview id: the backend collapses partial → final on it.
        const sid = (crypto.randomUUID && crypto.randomUUID()) ||
                    (Date.now() + '-' + Math.random().toString(36).slice(2));

        document.querySelectorAll('#reinstall-top, #reinstall-sticky, #reinstall-thanks').forEach(a => {
            a.href = CWS_URL;
            a.target = '_blank';
            a.rel = 'noopener';
        });

        window.scrollToFeedback = () => {
            document.getElementById('feedback').scrollIntoView({ behavior: 'smooth', block: 'start' });
        };

        const sticky = document.getElementById('sticky-cta');
        let stickyShown = false;
        window.addEventListener('scroll', () => {
            const past = window.scrollY > window.innerHeight * 0.6;
            if (past !== stickyShown) {
                sticky.classList.toggle('show', past);
                stickyShown = past;
            }
        }, { passive: true });

        // ── Site picker ─────────────────────────────────────
        const SITE_QUESTIONS = {
            broken_site:  'Which site did AIO break?',
            too_many_ads: 'Where did ads still get through?',
            slow:         'Which site felt slow?',
            bug:          'Where did you hit the bug?',
        };
        const picker    = document.getElementById('site-picker');
        const siteGrid  = document.getElementById('site-grid');
        const siteTitle = document.getElementById('site-q-title');
        const otherIn   = document.getElementById('site-other-input');
        const chosenSites = new Set();

        SUSPECTS.slice(0, MAX_SITE_CHIPS).forEach(host => {
            const b = document.createElement('button');
            b.type = 'button';
            b.className = 'site-chip';
            b.textContent = host;
            b.addEventListener('click', () => {
                b.classList.toggle('selected');
                if (b.classList.contains('selected')) chosenSites.add(host);
                else chosenSites.delete(host);
                queuePartial();
            });
            siteGrid.appendChild(b);
        });

        const otherChip = document.createElement('button');
        otherChip.type = 'button';
        otherChip.className = 'site-chip';
        otherChip.textContent = SUSPECTS.length ? 'another site…' : 'type the site…';
        otherChip.addEventListener('click', () => {
            otherChip.classList.toggle('selected');
            otherIn.classList.toggle('show', otherChip.classList.contains('selected'));
            if (otherChip.classList.contains('selected')) otherIn.focus();
        });
        siteGrid.appendChild(otherChip);
        otherIn.addEventListener('input', () => queuePartial());

        function showPicker(reason) {
            const q = SITE_QUESTIONS[reason];
            if (!q) { picker.classList.remove('show'); return; }
            siteTitle.textContent = q;
            picker.classList.add('show');
        }

        function collectSites() {
            const sites = Array.from(chosenSites);
            const typed = (otherIn.value || '').trim().toLowerCase();
            if (typed && otherChip.classList.contains('selected')) sites.push(typed);
            return sites;
        }

        // ── Reason chips ────────────────────────────────────
        let chosenReason = null;
        const chips = document.querySelectorAll('.chip');
        const extra = document.getElementById('fb-extra');

        chips.forEach(chip => {
            chip.addEventListener('click', () => {
                chips.forEach(c => c.classList.remove('selected'));
                chip.classList.add('selected');
                chosenReason = chip.dataset.reason;
                extra.classList.add('show');
                showPicker(chosenReason);
                if (chosenReason === 'other') {
                    setTimeout(() => document.getElementById('fb-text').focus(), 200);
                }
                // Partial beacon: most visitors bounce without pressing
                // Send — one chip tap must already deliver reason + context.
                queuePartial(true);
            });
        });

        function payload(partial, text, email) {
            return {
                reason: chosenReason,
                sites: collectSites(),
                text:  text  || '',
                email: email || '',
                partial,
                sid,
                ctx,
                a_tkn: aTkn,
                sx,
                ua: navigator.userAgent,
                lang: navigator.language,
                ts: Date.now(),
            };
        }

        // Debounced partial sender. Backend keeps the latest record per
        // sid; a final (partial:false) always wins over partials.
        let partialTimer = null;
        let finalSent = false;
        function queuePartial(now) {
            if (!chosenReason || finalSent) return;
            clearTimeout(partialTimer);
            partialTimer = setTimeout(() => send(payload(true)), now ? 0 : 1200);
        }

        window.submitFeedback = (skipText) => {
            if (!chosenReason) return;
            clearTimeout(partialTimer);
            finalSent = true;
            const text  = skipText ? '' : (document.getElementById('fb-text').value  || '').trim();
            const email = skipText ? '' : (document.getElementById('fb-email').value || '').trim();
            send(payload(false, text, email));
            showThanks();
        };

        function send(body) {
            const blob = new Blob([JSON.stringify(body)], { type: 'application/json' });
            let ok = false;
            try {
                if (navigator.sendBeacon) {
                    ok = navigator.sendBeacon(FEEDBACK_ENDPOINT, blob);
                }
            } catch (_) {}
            if (!ok) {
                fetch(FEEDBACK_ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(body),
                    keepalive: true,
                    credentials: 'omit',
                }).catch(() => { /* swallow — page is already showing thanks */ });
            }
        }

        function showThanks() {
            document.getElementById('fb-form-wrap').style.display = 'none';
            document.getElementById('thank-you').classList.add('show');
            document.getElementById('thank-you').scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    })();
"""

# Replace the main IIFE script (the one containing CWS_URL)
pat = re.compile(r'(<script>)\s*\(\(\) => \{.*?CWS_URL.*?\}\)\(\);\s*(</script>)', re.S)
src, n = pat.subn(lambda m: m.group(1) + JS + m.group(2), src, count=1)
if n != 1: sys.exit('main script anchor not found')

open('uninstall_v2.html', 'w').write(src)
print(f'uninstall_v2.html written: {len(src)} bytes')
