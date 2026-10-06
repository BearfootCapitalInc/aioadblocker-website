# Uninstall page v2 — handoff notes

**What:** `/uninstall/` upgrade — the page now consumes the full exit-beacon
the extension (≥ v1.1.85) already puts in the uninstall URL, asks *which site*
was affected, and forwards everything to the existing feedback endpoint.
**No backend changes are required to go live** — the JSON POST target is the
same `/uninstall/feedback/`; the body just carries more fields.

## Files

- `uninstall_v2.html` — ready-to-ship page (built from the live production
  page fetched 2026-10-06, not from the old repo copy)
- `uninstall_v2.diff` — unified diff vs. that live snapshot (`uninstall_live.html`)
- `build_uninstall_v2.py` — reproducible patcher (live snapshot → v2)

Note: the live page server-renders the reinstall URL (`/rinsorg/`). The diff
keeps that markup byte-identical — if it's a template variable on your side,
nothing to re-wire. Tracking iframe + `localStorage.clear()` untouched.

## What changed (3 spots)

1. **CSS** — `.site-picker` / `.site-chip` block appended at the end of `<style>`.
2. **HTML** — site-picker `<div>` inserted at the top of `#fb-extra`
   (hidden until a site-related reason is chosen).
3. **JS** — the main IIFE replaced:
   - Parses all uninstall-URL params set by the extension:
     `tabs` (open-tab domains, MRU-first, may be truncated), `tabn` (true tab
     count), `cur`/`prev` (last active domains), `wl`/`wlm` (last whitelisted
     domain + minutes since), `v`, `cfgv`, `lists`, `blk`, `age`, `lang`.
   - For reasons `broken_site | too_many_ads | slow | bug`, shows
     **"Which site?" chips** built from cur → prev → wl → tabs (deduped,
     max 12, multi-select) + an "another site…" free-text option.
     Other reasons / no beacon params degrade gracefully.
   - **Partial beacons restored**: first reason tap fires immediately;
     site-chip/text changes re-fire debounced (1.2 s). A final Send/Skip
     stops partials.
   - All beacons now include: `sites[]`, `ctx{...all params above}`,
     `sid` (per-pageview UUID), `partial` (bool) — plus the existing
     `reason/text/email/a_tkn/sx/ua/lang/ts`.

## Backend recommendation (optional, not blocking)

Dedupe on `sid`: keep the latest record per sid, `partial:false` always wins
over `partial:true`. If you only ever keep the last row per sid you get exactly
one clean record per visitor, with site + full context even for bouncers.

## QA done (VPS preview)

- JS syntax (node --check), full flow in headless Chrome:
  reason chip → picker renders with correct ordering → multi-select →
  partial + final payloads captured and verified field-by-field.
- Preview: http://46.250.241.134/aioadblocker/uninstall-v2/
  (append the sample params below to see the picker populated)

```
?a_tkn=TEST-UID-123&sx=kkfjlmnopabc&v=1.1.85&cfgv=7&lists=17&blk=48213&age=14&lang=en-US&cur=realestate.com.au&prev=youtube.com&wl=news.com.au&wlm=22&tabn=9&tabs=realestate.com.au,youtube.com,news.com.au,reddit.com,mail.google.com,twitch.tv,ebay.com.au
```

## Privacy note

Tab domains are collected by the shipped extension only at domain level and
leave the user's machine only via the uninstall URL (nothing streams during
normal use). Suggest adding one line to the privacy policy under diagnostics:
domain-level context may accompany uninstall feedback.
