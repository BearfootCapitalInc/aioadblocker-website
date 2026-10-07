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
      .fb-hint { font-size: 13px; color: var(--text-mute); margin: 0 0 10px 2px; }
  """

# ── 1b. Compact hero (J 2026-10-07): reasons must be reachable without
#    scrolling, and the headline had too many colours. Appended last so
#    it overrides the base rules AND the responsive media blocks.
CSS += """
      /* ── v2 compact hero: single accent, feedback above the fold ── */
      .hero { flex: 0 0 auto; padding: 30px 0 24px; }
      .shield-wrap { margin-bottom: 12px; }
      .shield { width: 64px; height: 75px; }
      .shield-x { width: 24px; height: 24px; font-size: 14px; top: -5px; right: -7px; }
      .hero-tag { margin-bottom: 14px; }
      .hero h1 { font-size: 32px; margin-bottom: 10px; letter-spacing: -0.6px; }
      .hero h1 .green, .hero h1 .warn { color: inherit; }
      .hero-sub { font-size: 15px; max-width: 640px; margin-bottom: 18px; }
      .cta-row { gap: 10px; margin-bottom: 0; }
      .btn-reinstall { padding: 14px 32px; font-size: 15px; }
      .loss-strip { display: none; }
      .feedback { padding: 36px 0 50px; }
      /* ── v2: dissociate the two jobs of the page — reinstall pitch on
         the dark page bg, feedback inside its own bordered panel ── */
      /* Reinstall = the hero card, visually dominant: raised, green-topped */
      .hero { padding: 26px 0 30px; }
      .hero-inner {
        background: #122c47;
        border: 1px solid rgba(125,255,212,0.25);
        border-top: 4px solid var(--green);
        border-radius: 16px;
        padding: 34px 44px 38px;
        box-shadow: 0 24px 70px rgba(0,0,0,0.55);
        max-width: 980px;
        margin: 0 auto;
      }
      /* ── /success/-style hero lockup, uninstall flavour ── */
      .shield-wrap { display: inline-block; position: relative; margin-bottom: 20px; animation: none; filter: drop-shadow(0 18px 50px rgba(255,122,89,0.30)); }
      .shield, .shield-wrap:hover .shield { width: 120px; height: 139px; display: block; filter: none; }
      .shield-x { top: auto; bottom: 4px; right: -12px; width: 50px; height: 50px; background: var(--warn); border: 4px solid #122c47; color: #0a1828; font-size: 28px; font-weight: 800; box-shadow: 0 10px 28px rgba(255,122,89,0.5); }
      .hero-tag { display: inline-block; padding: 6px 14px; background: rgba(255,122,89,0.12); border: 1px solid var(--warn); color: var(--warn); font-family: 'Courier New', monospace; font-size: 12px; letter-spacing: 3px; text-transform: uppercase; margin: 0 0 20px; border-radius: 0; }
      .hero h1 { font-size: 42px; margin-top: 0; }
      .hero h1 .green { color: inherit; }
      .hero h1 .warn { color: var(--warn); }
      .hero-sub { max-width: 560px; text-wrap: balance; margin-bottom: 18px; }
      /* A little breathing room around the reinstall CTA (not a lot) */
      .cta-row { margin-top: 22px; gap: 16px; margin-bottom: 6px; }
      /* Feedback = secondary: quieter, flatter panel below */
      .feedback { background: none; padding: 0 0 70px; }
      .feedback .container {
        background: rgba(13,33,56,0.5);
        border: 1px solid rgba(125,255,212,0.14);
        border-radius: 16px;
        padding: 32px 44px 38px;
      }
      /* Feedback pitch is the headline now (h2 removed from markup) */
      .fb-head p { font-size: 19px; font-weight: 700; color: white; max-width: 700px; line-height: 1.5; }
      .fb-head p.fb-sub { font-size: 14px; font-weight: 500; color: var(--text-mute); margin-top: 6px; }
      @media (max-width: 640px) {
        .hero-inner { padding: 24px 16px 28px; border-radius: 14px; }
        .feedback .container { padding: 24px 16px 28px; border-radius: 14px; }
      }

      /* ── v2: make the input fields clearly visible (were near-invisible
         — page-coloured bg + 15%-opacity border) ── */
      .fb-extra textarea, .fb-extra input {
        background: rgba(26,52,80,0.6);
        border: 1px solid rgba(125,255,212,0.38);
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.3);
      }
      .fb-extra textarea::placeholder, .fb-extra input::placeholder { color: rgba(154,196,208,0.85); }

      /* ── v2 wide screens: one shared 980px column, all edges aligned ── */
      @media (min-width: 1100px) {
        .container { max-width: 980px; }
        .hero h1 { max-width: 900px; }
        .hero-sub { max-width: 680px; }
        .chip-grid { max-width: 980px; grid-template-columns: repeat(4, 1fr); }
        .fb-extra { max-width: 980px; }
        .fb-submit { justify-content: space-between; }
      }
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
\t\t\t\t<p class="fb-hint">Please provide detailed feedback and hit Send — it really helps.</p>
"""

m = re.search(r'(<div class="fb-extra" id="fb-extra">\s*\n)', src)
if not m: sys.exit('fb-extra anchor not found')
src = src[:m.end()] + PICKER + src[m.end():]

# ── 2b. Copy (J 2026-10-07): "they can help us make it better — but we
#    need their feedback" has to be said explicitly.
src = src.replace(
    'No, I meant it — let me tell you why ↓',
    'No, I meant it — help us make AIO better ↓')
src = src.replace(
    "Pick the closest reason — it helps us fix what's broken. Click one, that's it.",
    "Your feedback is important to us — it's how AIO gets better.")

# ── 2c. (J 2026-10-07) Drop the "What pushed you to uninstall?" title;
#    the feedback pitch sentence becomes the headline itself.
src = re.sub(r'\s*<h2>What pushed you to uninstall\?</h2>', '', src)

# ── 2d0. (J 2026-10-07) Hero mimics the /success/ page lockup: big bright
#    shield + badge circle + bracketed eyebrow tag. Markup already matches
#    (shield-wrap + shield-x + hero-tag) — only the tag text changes here;
#    the rest is CSS overrides below.
src = src.replace('<div class="hero-tag">// PROTECTION OFFLINE</div>',
                  '<div class="hero-tag">[ PROTECTION OFFLINE ]</div>')

# ── 2d. (J 2026-10-07) Move the "No, I meant it" message out of the hero
#    card and into the feedback head, under the headline.
src = re.sub(r'\s*<button class="link-feedback"[^>]*>.*?</button>', '', src, flags=re.S)
src = src.replace(
    "Your feedback is important to us — it's how AIO gets better.</p>",
    "Your feedback is important to us — it's how AIO gets better.</p>\n"
    '\t\t\t\t<p class="fb-sub">No, I meant it — help us make AIO better.</p>')

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
