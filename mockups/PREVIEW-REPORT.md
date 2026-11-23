# D homepage preview: baseline and result

Measured locally with Playwright (Chromium) and axe-core (WCAG 2.0/2.1/2.2 A and AA), no network throttling.

| | Live homepage (`/index.html`) | D preview (`/d-preview/index.html`) |
|---|---|---|
| Transfer, desktop | 510 KB | 368 KB |
| Transfer, mobile | 510 KB | 315 KB |
| Requests | 14 | 8 |
| Third-party hosts | fonts.googleapis.com, fonts.gstatic.com | none |
| axe violations | 1 (`label`) | 0, in light and dark mode, at 1440 and 390 px |
| Layout shift (CLS) | 0.016 | 0 |

Rulings applied (Cage Match council): solid nav, click-only city tabs (one photo loads per mode), next-closing-grant card below the hero
built from `/data/grants.json` and hidden if nothing is upcoming, two self-hosted font families, no wordmark, grain, parallax or glow,
credits page, `noindex` on the preview. The Grant Finder and every other page are untouched.

Not yet done: real-user test of the Grant Finder, Core Web Vitals on a throttled connection, a rollout plan for the other pages.
The live homepage also loads Google Analytics; the preview does not, so it records no traffic.
