# All-In-One Adblocker — Privacy Policy

**Effective date:** May 17, 2026
**Extension version:** 1.1.46 and later
**Website:** https://aioadblocker.com
**Contact:** privacy@aioadblocker.com

---

## TL;DR

All-In-One Adblocker is a local tool. Ad blocking happens entirely inside your browser, on your device. We do not read your browsing history. We do not log the pages you visit. We do not track what you click. We do not sell, share, or monetize personal data, and we do not build profiles of users.

The one thing we do generate is a **random, anonymous user ID** when you install the extension. This ID is not tied to your name, email, IP address, or anything personal. It exists for technical and operational reasons described below, and it is not used to track or identify you.

AIO is free to use today, and will always be free to use. To keep it that way long-term, the extension may in the future include optional, non-intrusive monetization (for example, a sponsored slot in the popup, an opt-in promotion, or a partnership). If and when that happens, it will be clearly disclosed in the extension and in this policy. Such monetization will never compromise the core ad-blocking, and we will not begin collecting personal data to support it.

---

## 1. Who we are

All-In-One Adblocker ("AIO," "we," "us," "our") is a free, open-source-style Chrome extension that blocks advertisements, trackers, and known malicious domains. AIO is published on the Chrome Web Store and runs entirely inside your browser.

---

## 2. What we collect

### The one piece of data AIO does generate: a random anonymous user ID

When you install AIO, the extension generates a **random, anonymous identifier** — a string of characters with no personal meaning. This ID:

- Is generated on your device at install time
- Is not tied to your name, email address, phone number, IP address, or any other personal information you can be identified by
- Is used for technical and operational purposes only — for example, keeping your local settings consistent, distinguishing one installation from another for support purposes, and counting how many installations of AIO exist
- Is **never sold** to third parties
- Is **never shared** with advertisers, data brokers, or any commercial partner
- Is **never used to track your browsing**, build a profile of you, or target you with content

The user ID is the only identifier the extension generates. It is not paired with any other data about you on our side, because we don't collect any other data about you.

### Everything else AIO does NOT collect

To be unambiguous, AIO does **NOT** collect, store, transmit, sell, share, or process any of the following:

- ❌ Personally identifiable information beyond the anonymous user ID described above
- ❌ Names, email addresses, phone numbers, or addresses
- ❌ IP addresses (Chrome may include your IP when AIO downloads filter list updates from public hosts, but AIO itself does not store or transmit your IP)
- ❌ Device fingerprints
- ❌ Browsing history, URLs visited, or page contents
- ❌ Search queries
- ❌ Authentication credentials or passwords
- ❌ Financial or payment information
- ❌ Location data
- ❌ Health or biometric data
- ❌ Communications content
- ❌ Per-page click data, scroll data, or interaction analytics

We do not have user accounts. We do not have a login system. We do not maintain a central database of users that pairs the anonymous ID with anything personal.

---

## 3. What AIO does locally on your device

For the extension to block ads, it must read and modify the content of the web pages you visit. This processing happens **entirely on your device, inside your own browser, in real time**, and is never transmitted to us or to any third party.

Specifically, AIO locally:

- **Reads page URLs** to decide which filter rules apply to the current site (e.g. a YouTube rule on youtube.com)
- **Reads page DOM contents** to identify and hide ad elements with cosmetic filters
- **Reads outgoing network requests** through Chrome's declarativeNetRequest API to block requests to ad and tracker servers
- **Counts blocked items per-tab and lifetime totals**, which are stored in `chrome.storage.local` on your computer — these numbers never leave your device
- **Stores your per-site preferences** (whitelisted sites, pause states, custom rules) in `chrome.storage.local` on your computer

All of this is local processing. None of it is reported, transmitted, mirrored, or duplicated to any external service.

---

## 4. Filter list updates (the one network call AIO makes)

To keep ad blocking effective, AIO periodically downloads updated **filter lists** from public, third-party sources. These are the same filter lists used by uBlock Origin, AdGuard, EasyList, and other major adblockers.

When AIO downloads filter list updates:

- The request is a normal HTTPS GET to a public filter-list URL (e.g. raw.githubusercontent.com/...)
- The request includes the standard Chrome user agent and your IP address — both of which the public list maintainer's web server may log, the same as any other web traffic from your browser
- AIO does not add identifiers, account tokens, fingerprints, or telemetry to these requests
- AIO downloads the **same list everyone else downloads**; we do not request a personalized version

Filter list sources include (non-exhaustive):
- uBlock Origin filter lists (github.com/uBlockOrigin)
- uBlock Origin Lite rulesets
- EasyList and EasyPrivacy (easylist.to)
- AdGuard filters (github.com/AdguardTeam)
- Peter Lowe's ad/tracking server list (pgl.yoyo.org)
- URLhaus malware host list (urlhaus.abuse.ch)

Each list source has its own privacy policy. We do not control them, but we choose them because they have a long-standing reputation for not surveilling users.

---

## 5. Permissions AIO requests, and why

Chrome will warn you that AIO requests certain permissions on install. Here is why we need each one, and what we use it for:

| Permission | Why AIO needs it |
|---|---|
| `<all_urls>` host permission | To apply ad-blocking and cosmetic rules across any website you visit. AIO does not transmit any data about the sites you visit. |
| `declarativeNetRequest` | To block network requests to ad and tracker domains at the browser level. Chrome handles the matching — AIO does not "see" your traffic. |
| `declarativeNetRequestFeedback` | To count blocked requests for the per-page counter shown in the popup. Counts are stored locally. |
| `storage` and `unlimitedStorage` | To save your settings, whitelist, custom rules, and blocked-count totals on your device. Local-only. |
| `scripting` | To inject cosmetic and scriptlet rules into pages to hide ads that pure network-blocking can't catch. |
| `activeTab` | To know which page you're currently viewing so the popup shows accurate per-page stats. |
| `webNavigation` | To know when a page navigation starts so AIO can apply rules at the right moment. |
| `webRequest` | Used for debugging and rule analytics inside the extension only. No requests are forwarded externally. |
| `tabs` | To support pause-on-site and per-site whitelisting. |
| `alarms` | To schedule periodic filter list updates (typically every few hours). |

We use these permissions only for the purposes described above. We do not use them for analytics, tracking, advertising, monetization, profile-building, or any secondary purpose.

---

## 6. Data and behaviors we explicitly do NOT engage in

Just to be exhaustive — AIO does NOT:

- Sell or rent the user ID or any other data to anyone
- Share the user ID or any other data with advertisers, brokers, analytics companies, or any third party
- Tie the user ID to your name, email, IP address, browsing history, or any personal identifier
- Participate in an "acceptable ads" program (we don't allowlist paid advertisers in our blocking)
- Inject affiliate links into web pages you visit
- Modify the content of websites for commercial purposes beyond ad-blocking
- Run cryptocurrency miners, fingerprinters, or any other secondary code
- Use Google Analytics, Mixpanel, Amplitude, or any other third-party analytics SDK that aggregates user behavior
- Use Sentry, Datadog, or any other third-party crash/error reporting service that transmits identifying telemetry
- Sync your settings, browsing data, or blocked-counter data to any cloud service

---

## 7. Children's privacy

AIO does not knowingly collect any data from anyone, including children under the age of 13. Because AIO collects no data at all, this section is mainly a formality required by COPPA. If a child uses AIO, no data is generated, stored, or transmitted about them by the extension.

---

## 8. International users (GDPR, CCPA, and friends)

Because AIO does not collect, process, store, or transfer any personal data, the major privacy regimes have limited applicability:

- **GDPR (EU/EEA/UK):** AIO does not "process" personal data within the meaning of GDPR Article 4. There is no controller, no processor, and no lawful-basis question because no data leaves your device.
- **CCPA / CPRA (California):** We do not "sell" or "share" personal information because we do not collect any.
- **LGPD (Brazil), PIPEDA (Canada), APP (Australia), POPIA (South Africa):** Same — no collection means no obligations beyond transparency, which this policy provides.

If your local law nonetheless grants you rights to access, correct, port, or delete personal data, you can exercise them by contacting **privacy@aioadblocker.com**. Our response will almost always be: *"We have searched our records and found that we have no personal data about you."* We do not retain logs, accounts, or stored data on any AIO-controlled server that could identify a user.

---

## 9. Third parties

AIO is a standalone extension. We do not embed third-party SDKs, advertising networks, analytics providers, or social-media trackers.

The only external services AIO communicates with are the **public filter-list hosts** described in Section 4. These are third-party maintainers (e.g. GitHub-hosted repositories, EasyList domains). Their own privacy practices govern those interactions, and AIO does not transmit any identifying information to them beyond the standard properties of an HTTPS request from your browser.

---

## 10. Security

Because AIO has no servers and no central database, there is no central trove of user data that could be stolen, leaked, or subpoenaed. Your settings and counters live in `chrome.storage.local` on your device only, protected by your operating system's normal user-account security.

The AIO extension package itself is signed and distributed by the Chrome Web Store, which verifies its integrity before each install and update.

---

## 11. Open-source-style transparency

The blocking engines and filter lists that power AIO are derived from publicly auditable open-source projects (uBlock Origin, uBlock Origin Lite, AdGuard, EasyList, etc.). The AIO extension code that ties them together is available for inspection on request. We welcome independent privacy and security review.

If you would like to inspect a specific behavior of the extension, contact **privacy@aioadblocker.com** and we will provide the relevant code and configuration.

---

## 12. How AIO is funded — and potential future monetization

AIO is free to download and free to use. It is, and will continue to be, free — there is no premium tier, no paywall, and no subscription.

To sustain AIO long-term, the extension may in the future include **optional, non-intrusive monetization**. We are deliberately disclosing this possibility now, in advance, so that users installing AIO today are aware of how the project may eventually pay for itself.

Forms this monetization might take include, but are not limited to:

- A sponsored slot in the extension's popup or new-tab page
- An opt-in recommended product or service partnership
- Affiliate links to services we genuinely use or endorse, placed in the extension's settings or help pages
- Display advertising in extension-controlled surfaces (the popup, the options page, the new-tab page), potentially served through advertising partners
- Optional paid features or tiers, alongside the always-free core extension

If and when AIO begins any form of monetization, the following commitments hold:

1. **It will be clearly disclosed.** The extension itself will surface what is happening, and this policy will be updated to describe it specifically.
2. **The core ad-blocking will not be compromised.** AIO will continue to block ads on the websites you visit. We will not allow advertisers to pay for their ads to bypass our blocking, and we will not participate in an "acceptable ads" program.
3. **No personal data will start being collected to support monetization.** If a third-party ad partner is ever involved, this policy will describe exactly what that partner has access to, and you will have the ability to opt out of any tracking that the partner introduces.
4. **Monetization will be opt-in or opt-out where it materially changes the user experience.** Cosmetic sponsored placements may appear without opt-in, but anything that involves new data sharing will offer a clear control.

As of the effective date at the top of this policy, AIO contains no ads, no sponsored content, no affiliate links, and no commercial integrations of any kind. The above section exists so that, if any of that changes in the future, you have already been told it might.

## 13. Changes to this policy

If we ever change this policy in a way that affects users — for example, if a future feature requires any kind of network call we don't currently make, or if we begin any form of monetization — we will:

1. Publish the updated policy at https://aioadblocker.com/privacy with a new "Effective date"
2. Note the change in the extension's release notes on the Chrome Web Store
3. Where the change would materially alter what data is processed, ship the change behind an explicit opt-in toggle that defaults to off

We will not silently change our behavior. The promise on this page is the product.

---

## 14. Contact

Privacy questions, data requests, or audit inquiries:
**privacy@aioadblocker.com**

General support:
**support@aioadblocker.com**

Website:
**https://aioadblocker.com**

---

*This privacy policy is written in plain language so a normal person can read it without a lawyer. Where it conflicts with marketing claims elsewhere, this document controls.*
