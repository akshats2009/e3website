# CLAUDE.md — e3 Initiative Website

This file provides guidance for AI assistants working in this repository.

---

## Project Overview

**e3 Initiative** (Equity, Economics, and Ethnicity) is a research organization. This repository is a **static HTML website** with no build process, no framework, and no package manager. All content is hand-authored HTML, CSS, and vanilla JavaScript.

**Founders:** Akshat Sawner and Minghao Gu
**Analytics ID:** G-JJDGPY8QCB
**Deployment:** Static site (GitHub Pages / Netlify / Vercel compatible)

---

## Repository Structure

```
e3website/
├── index.html              # Homepage
├── about.html              # About page (team info)
├── articles.html           # Articles listing page
├── research.html           # Research publications page
├── contact.html            # Contact form page
├── articles/               # Individual article HTML files
│   ├── chinatown-solidarity.html
│   └── chinatown-citations.html
├── research/               # Individual research HTML files
│   └── chinatown-solidarity.html
├── css/
│   ├── base.css            # Primary stylesheet (~875 lines)
│   ├── liquid-glass.css    # Glass morphism effects
│   └── override.css        # Editorial typography overrides
├── js/
│   └── script.js           # All client-side logic (~183 lines)
├── data/
│   ├── articles.js         # Article data (window.articlesData global)
│   └── articles.json       # Article metadata (JSON format)
├── image/                  # Site images (JPG, AVIF)
├── sitemap.xml             # Standard XML sitemap
├── news-sitemap.xml        # Google News sitemap
├── robots.txt              # SEO robots directive
└── DEPLOY_TRIGGER.txt      # Deployment marker file
```

---

## Tech Stack

| Layer      | Technology                                      |
|------------|-------------------------------------------------|
| Markup     | Plain HTML5 (semantic elements)                 |
| Styles     | Vanilla CSS3 (Grid, Flexbox, CSS Variables)     |
| Scripts    | Vanilla JavaScript (ES5-compatible, no modules) |
| Fonts      | Google Fonts: Inter + Instrument Serif          |
| Analytics  | Google Analytics (gtag.js)                      |
| Data       | JS global (`window.articlesData`) from data/articles.js |

**There is no build step, no bundler, no transpiler, and no package.json.**

---

## Development Workflow

### Making Changes

Since there is no build process, changes take effect immediately. Edit files directly:

1. Edit HTML, CSS, or JS files
2. Open in a browser to verify (or use a local static server: `python3 -m http.server 8080`)
3. Commit and push

### Adding a New Article or Research Entry

1. **Add the article data** in `data/articles.js` by appending to the `window.articlesData` array:
   ```javascript
   {
     title: "Article Title",
     date: "YYYY-MM-DD",            // ISO format, used for sorting
     summary: "Short description.", // One to two sentences
     image: "image/filename.jpg",   // Relative path from site root
     imageAlt: "Description of image for accessibility",
     link: "articles/filename.html", // Relative path to article page
     type: "article"               // "article" or "research"
   }
   ```

2. **Create the article HTML file** in `articles/` (or `research/` for research entries). Use an existing article as a template.

3. **Update sitemaps:** Add the new URL to `sitemap.xml` and `news-sitemap.xml` if it's a news article.

### Updating Sitemaps

- `sitemap.xml` — add a `<url>` entry with `<loc>`, `<lastmod>`, `<changefreq>`, and `<priority>`
- `news-sitemap.xml` — add a `<url>` entry with `<news:news>` metadata for Google News indexing

---

## JavaScript Architecture (`js/script.js`)

All JS runs on `DOMContentLoaded`. Key functions:

| Function             | Purpose                                                        |
|----------------------|----------------------------------------------------------------|
| `escHtml(str)`       | XSS-safe HTML entity encoding — **always use for user-supplied or data-driven content** |
| `formatDate(dateStr)`| Converts `YYYY-MM-DD` → human-readable (`February 2, 2026`)   |
| `buildCard(article)` | Generates article card HTML from a data object                 |
| `populateGrids()`    | Fills all `.articles-grid` elements from `window.articlesData` |
| `createObserver()`   | IntersectionObserver for fade-up scroll animations             |
| `initScrollAnimations()` | Adds `.fade-up` class to animatable elements              |
| `initBackToTop()`    | Scroll-to-top button behavior                                  |
| `initFilters()`      | Filter articles by `data-filter` attribute on buttons          |

**Data flow:** `data/articles.js` sets `window.articlesData` → `populateGrids()` renders cards into `.articles-grid` containers → sorted newest-first by date.

**Homepage** shows only the 3 most recent articles. **Listing pages** show all items of the matching `type`.

---

## CSS Architecture

### Files

- **`base.css`** — All core styles. Defines CSS custom properties, layout, components (navbar, hero, cards, forms, footer), animations, and media queries.
- **`liquid-glass.css`** — Glass morphism `.liquid-glass` class (backdrop-filter, blur, saturation). Used for the mission panel on the homepage.
- **`override.css`** — Editorial overrides: switches headings to `Instrument Serif`, enhances card hover interactions, adds scroll-reveal animation behavior.

### CSS Variables (defined in `base.css :root`)

```css
--text: #ffffff          /* Primary text color */
--muted: #d1d5db         /* Secondary/muted text */
--duration: 0.3s         /* Default transition duration */
```

### Key Design Tokens

- Background: `#000000` (pure black)
- Card background: dark semi-transparent
- Border radius: `20px`–`30px`
- Mobile breakpoint: `max-width: 768px`
- Fluid typography: `clamp()` for responsive font sizes

### Animation Classes

- `.fade-up` — Applied by JS; elements animate in when scrolled into view
- `.header-animate`, `.delay-1`, `.delay-2`, `.delay-3` — Staggered hero text animations

---

## HTML Conventions

### Page Structure

Every page follows this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Canonical URL, viewport, charset -->
  <!-- Open Graph / Twitter Card meta tags -->
  <!-- Google Analytics (gtag.js) -->
  <!-- Schema.org JSON-LD structured data -->
  <!-- CSS: base.css, override.css, (liquid-glass.css if needed) -->
  <!-- Google Fonts preconnect + stylesheet -->
</head>
<body>
  <nav>...</nav>
  <main>
    <section class="hero">...</section>
    <!-- page content -->
  </main>
  <footer>...</footer>
  <!-- data/articles.js before script.js -->
  <script src="../data/articles.js"></script>
  <script src="../js/script.js"></script>
</body>
</html>
```

> **Note:** For root-level pages, script paths are `data/articles.js` and `js/script.js`. For pages in subdirectories (`articles/`, `research/`), prefix with `../`.

### SEO Requirements

Every page must include:
- `<link rel="canonical" href="...">` — absolute URL
- Open Graph tags: `og:title`, `og:description`, `og:type`, `og:url`, `og:image`
- Twitter Card tags: `twitter:card`, `twitter:title`, `twitter:description`
- Schema.org JSON-LD appropriate to the page type

### Accessibility Requirements

- All images must have descriptive `alt` attributes
- Images below the fold: add `loading="lazy"`
- Interactive non-button elements (e.g., card divs): add `tabindex="0"` and `role="button"`
- Form inputs must have associated `<label>` elements
- Use `aria-label` on icon-only links and navigation landmarks
- Dynamic content regions: use `aria-live="polite"`

---

## Design System

### Color Scheme

The site uses a **dark theme** (black background, white text). Do not introduce light-mode colors unless explicitly requested.

### Typography

- Body: `Inter` (sans-serif)
- Headings: `Instrument Serif` (serif) — applied via `override.css`

### Component Classes

| Class             | Usage                                            |
|-------------------|--------------------------------------------------|
| `.card`           | Article/research cards with hover effects        |
| `.btn`            | Primary call-to-action buttons                   |
| `.hero`           | Full-width hero sections with background images  |
| `.articles-grid`  | Responsive card grid (`auto-fit`, `minmax(300px, 1fr)`) |
| `.liquid-glass`   | Glass morphism panel (backdrop-filter)           |
| `.fade-up`        | Scroll-animated element                          |
| `.section-header` | Section title + subtitle wrapper                 |
| `.container`      | Max-width content wrapper with horizontal padding|

---

## Content Guidelines

### Article Files

- Stored in `articles/` (editorial) or `research/` (research papers)
- Follow the structure of `articles/chinatown-solidarity.html`
- Include: hero with banner image, article body, citation section if applicable
- Link citations: create a companion `-citations.html` file if needed

### Images

- Store in `image/` directory
- Prefer AVIF for large background images (better compression)
- Use JPG for photography
- Keep filenames lowercase with hyphens (e.g., `chinatown-banner.jpg`)
- Optimize before committing — large uncompressed images slow page load

---

## Deployment

The site is a static site with no server-side processing.

- **DEPLOY_TRIGGER.txt** — Update this file's timestamp to trigger a deployment pipeline (if configured).
- No build command required.
- Any static hosting service works: GitHub Pages, Netlify, Vercel, Cloudflare Pages.

---

## What NOT to Do

- **Do not introduce a build system** (webpack, Vite, etc.) unless explicitly requested
- **Do not add npm/package.json** unless explicitly requested
- **Do not add a JavaScript framework** (React, Vue, etc.) without explicit instruction
- **Do not inline large base64 images** in CSS or HTML
- **Do not skip `escHtml()`** when rendering any dynamic string into HTML — XSS prevention is critical
- **Do not hardcode absolute URLs** in `<a href>` or `<img src>` — use relative paths
- **Do not modify `sitemap.xml`** without also updating `news-sitemap.xml` for news articles
- **Do not commit unoptimized images** larger than ~500KB without discussion

---

## Common Tasks Quick Reference

| Task | What to do |
|------|------------|
| Add a new article | Add entry to `data/articles.js`, create HTML in `articles/`, update sitemaps |
| Add a new research entry | Add entry to `data/articles.js` with `type: "research"`, create HTML in `research/`, update sitemaps |
| Update team members | Edit `about.html` team cards section |
| Change site colors | Edit CSS variables in `css/base.css` `:root` |
| Add a new page | Copy an existing page as template, add to nav in all pages, add to `sitemap.xml` |
| Fix a rendering bug | Check `js/script.js` `buildCard()` and `populateGrids()` |
| Update contact form behavior | Edit `js/script.js` form submission handler |
