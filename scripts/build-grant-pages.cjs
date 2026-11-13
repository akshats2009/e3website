#!/usr/bin/env node
/*
 * Build the crawlable grant pages from data/grants.json.
 *
 *   node scripts/build-grant-pages.cjs
 *
 * Writes:
 *   - minority-owned-business-grants.html
 *   - women-owned-business-grants.html
 *   - veteran-owned-business-grants.html
 *   - the static grant list and category links inside grants.html
 *     (between the GRANTS / COUNT / LISTS marker comments)
 *
 * Re-run it whenever data/grants.json changes. The pages also mark grants
 * Closed in the browser once their deadline passes (same rule as js/grants.js).
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const read = (f) => fs.readFileSync(path.join(ROOT, f), 'utf8');
const write = (f, s) => fs.writeFileSync(path.join(ROOT, f), s);

const SITE = 'https://e3-initiative.org';
const NOW = new Date();
const BUILD_DATE = NOW.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });
const BUILD_ISO = NOW.toISOString().slice(0, 10);

const CATEGORY_LABELS = {
  general: 'General', technology: 'Technology', arts_culture: 'Arts & Culture',
  food_agriculture: 'Food & Agriculture', community_development: 'Community Development',
  women_owned: 'Women-Owned', minority_owned: 'Minority-Owned', veteran_owned: 'Veteran-Owned',
  research: 'Research & Innovation', environment: 'Environment', health: 'Health'
};
const ELIGIBILITY_LABELS = { small_business: 'Small business', nonprofit: 'Nonprofit', both: 'Small business or nonprofit' };
const STATUS_LABELS = { open: 'Open', rolling: 'Rolling', closed: 'Closed' };

const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

// Same rule as js/grants.js: a grant whose ISO deadline has passed is closed.
function effectiveStatus(g) {
  if (g.status !== 'closed' && /^\d{4}-\d{2}-\d{2}$/.test(g.deadline || '') &&
      new Date(g.deadline + 'T23:59:59Z').getTime() < NOW.getTime()) {
    return 'closed';
  }
  return g.status;
}

function formatDeadline(g) {
  if (g.deadline === 'rolling') return 'Rolling / ongoing';
  if (g.deadline === 'annual') return 'Recurs annually';
  const d = new Date(g.deadline + 'T00:00:00Z');
  if (isNaN(d.getTime())) return g.deadline;
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' });
}

// Mirrors buildCard() in js/grants.js so static and scripted cards look identical.
function card(g) {
  const status = effectiveStatus(g);
  return '<article class="grant-card" data-deadline="' + esc(g.deadline) + '">' +
    '<p class="grant-funder">' + esc(g.funder) + '</p>' +
    '<h3>' + esc(g.name) + '</h3>' +
    '<div class="grant-tags">' +
      '<span class="grant-tag status-' + esc(status) + '">' + esc(STATUS_LABELS[status] || status) + '</span>' +
      '<span class="grant-tag">' + esc(ELIGIBILITY_LABELS[g.eligibility] || g.eligibility) + '</span>' +
      '<span class="grant-tag">' + esc(CATEGORY_LABELS[g.category] || g.category) + '</span>' +
    '</div>' +
    '<p class="grant-desc">' + esc(g.description) + '</p>' +
    '<div class="grant-meta">' +
      '<div class="grant-meta-row"><span class="label">Award</span><span class="value">' + esc(g.amount) + '</span></div>' +
      '<div class="grant-meta-row"><span class="label">Deadline</span><span class="value">' + esc(formatDeadline(g)) + '</span></div>' +
    '</div>' +
    '<a class="btn grant-apply" href="' + esc(g.link) + '" target="_blank" rel="noopener noreferrer">View &amp; apply →</a>' +
    '</article>';
}

const grants = JSON.parse(read('data/grants.json'));

const PAGES = [
  {
    file: 'minority-owned-business-grants.html',
    category: 'minority_owned',
    title: 'Grants for Minority-Owned Businesses | e3 Initiative',
    h1: 'Grants for Minority-Owned Businesses',
    short: 'Minority-owned business grants',
    description: (n) => 'Browse ' + n + ' grants for minority-owned businesses, including Black, Native American, and LGBTQ+ founders. See amounts, deadlines, and who qualifies.',
    intro: (n, c) =>
      'This list gathers ' + n + ' grants for founders and organizations from communities that have historically had less access to capital, ' +
      'including Black, Native American, Hispanic/Latino, and LGBTQ+ business owners. The funders range from national foundations and ' +
      'corporations to a state commerce department. ' + counts(c) +
      ' Many of the closed programs run every year, so they are worth tracking.'
  },
  {
    file: 'women-owned-business-grants.html',
    category: 'women_owned',
    title: 'Grants for Women-Owned Businesses | e3 Initiative',
    h1: 'Grants for Women-Owned Businesses',
    short: 'Women-owned business grants',
    description: (n) => 'Browse ' + n + ' grants for women-owned businesses and women entrepreneurs, from monthly micro-grants to $100,000 awards. See amounts and deadlines.',
    intro: (n, c) =>
      'This list gathers ' + n + ' grants for women entrepreneurs and women-led organizations, from monthly micro-grants to awards of up to $100,000. ' +
      'Most are for small businesses; one supports nonprofit domestic violence shelters. ' + counts(c) +
      ' Many of the closed programs run every year, so they are worth tracking.'
  },
  {
    file: 'veteran-owned-business-grants.html',
    category: 'veteran_owned',
    title: 'Grants for Veteran-Owned Businesses | e3 Initiative',
    h1: 'Grants for Veteran-Owned Businesses',
    short: 'Veteran-owned business grants',
    description: (n) => 'Browse ' + n + ' grants for veteran- and military-spouse-owned businesses and veteran-serving nonprofits. See award amounts, deadlines, and who qualifies.',
    intro: (n, c) =>
      'This list gathers ' + n + ' grants for veteran and military-spouse entrepreneurs, plus nonprofits that serve veterans and their families. ' +
      'Awards range from $1,000 micro-grants to housing grants of up to $500,000 for nonprofits. ' + counts(c) +
      ' Many of the closed programs run every year, so they are worth tracking.'
  }
];

function counts(c) {
  const parts = [];
  if (c.open) parts.push(c.open + ' ' + (c.open === 1 ? 'is' : 'are') + ' open now');
  if (c.rolling) parts.push(c.rolling + ' accept' + (c.rolling === 1 ? 's' : '') + ' applications on a rolling basis');
  if (c.closed) parts.push(c.closed + ' ' + (c.closed === 1 ? 'is' : 'are') + ' closed for now');
  if (!parts.length) return '';
  const last = parts.pop();
  return (parts.length ? parts.join(', ') + ', and ' : '') + last + '.';
}

const ORDER = { open: 0, rolling: 1, closed: 2 };

const gridsrc = read('grants.html');
const headEnd = gridsrc.indexOf('<link rel="canonical"');
const bodyStart = gridsrc.indexOf('<body');
const navEnd = gridsrc.indexOf('</nav>') + '</nav>'.length;
const footerStart = gridsrc.indexOf('<footer class="main-footer">');
if (headEnd < 0 || bodyStart < 0 || navEnd < 6 || footerStart < 0) {
  throw new Error('grants.html no longer has the expected structure');
}

function buildCategoryPage(p) {
  const list = grants.filter((g) => g.category === p.category)
    .sort((a, b) => ORDER[effectiveStatus(a)] - ORDER[effectiveStatus(b)] || a.name.localeCompare(b.name));
  const c = { open: 0, rolling: 0, closed: 0 };
  list.forEach((g) => { c[effectiveStatus(g)] += 1; });
  const url = SITE + '/' + p.file;
  const desc = p.description(list.length);

  let head = gridsrc.slice(0, headEnd);
  head = head
    .replace(/<title>[^<]*<\/title>/, '<title>' + esc(p.title) + '</title>')
    .replace(/(<meta name="description" content=")[^"]*/, '$1' + esc(desc))
    .replace(/(<meta property="og:title" content=")[^"]*/, '$1' + esc(p.title))
    .replace(/(<meta property="og:description" content=")[^"]*/, '$1' + esc(desc))
    .replace(/(<meta property="og:url" content=")[^"]*/, '$1' + url)
    .replace(/(<meta name="twitter:title" content=")[^"]*/, '$1' + esc(p.title))
    .replace(/(<meta name="twitter:description" content=")[^"]*/, '$1' + esc(desc));

  let rest = gridsrc.slice(headEnd);
  rest = rest.replace(/<link rel="canonical" href="[^"]*">/, '<link rel="canonical" href="' + url + '">');
  // Replace the CollectionPage JSON-LD with this page's own structured data.
  const ld = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'CollectionPage', name: p.title, url, description: desc,
        isPartOf: { '@type': 'WebSite', name: 'e3 Initiative', url: SITE + '/' },
        publisher: { '@type': 'Organization', name: 'e3 Initiative', url: SITE + '/',
          logo: { '@type': 'ImageObject', url: SITE + '/logo.png', width: 512, height: 512 } },
        mainEntity: {
          '@type': 'ItemList', numberOfItems: list.length,
          itemListElement: list.map((g, i) => ({ '@type': 'ListItem', position: i + 1, name: g.name, url: g.link }))
        }
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Home', item: SITE + '/' },
          { '@type': 'ListItem', position: 2, name: 'Grant Finder', item: SITE + '/grants.html' },
          { '@type': 'ListItem', position: 3, name: p.short, item: url }
        ]
      }
    ]
  };
  rest = rest.replace(/<script type="application\/ld\+json">[\s\S]*?<\/script>/,
    '<script type="application/ld+json">\n    ' + JSON.stringify(ld, null, 2).replace(/\n/g, '\n    ') + '\n    </script>');

  const bodyOpen = gridsrc.slice(bodyStart, navEnd);
  const footer = gridsrc.slice(footerStart).replace(/\s*<script src="js\/grants\.js"><\/script>/, '');
  const others = PAGES.filter((o) => o.file !== p.file)
    .map((o) => '<li><a href="' + o.file + '">' + esc(o.short) + '</a></li>').join('\n                    ');

  const main = `

    <main id="main">

    <!-- Page Header -->
    <section class="page-header">
        <div class="container">
            <h1>${esc(p.h1)}</h1>
        </div>
    </section>

    <section class="content-section">
        <div class="container legal">
            <p>${esc(p.intro(list.length, c))}</p>
            <p><em>List last updated ${BUILD_DATE}. Search all ${grants.length} grants in the <a href="grants.html">Grant Finder</a>.</em></p>
        </div>
        <div class="container">
            <h2>${list.length} ${esc(p.short.toLowerCase())}</h2>
            <div class="grants-grid">
${list.map((g) => '                ' + card(g)).join('\n')}
            </div>
        </div>
        <div class="container legal">
            <h2>Before you apply</h2>
            <ul>
                <li><strong>Check the funder's page.</strong> Deadlines, award amounts, and rules change often. Treat this list as a starting point.</li>
                <li><strong>Read the eligibility details closely.</strong> Ownership share, years in business, revenue range, and location differ a lot between grants.</li>
                <li><strong>Plan for the next cycle.</strong> Many closed programs recur annually, so note their usual timing and prepare early.</li>
            </ul>
            <h2>More grant lists</h2>
            <ul>
                    ${others}
                    <li><a href="grants.html">Search and filter all ${grants.length} grants</a></li>
                    <li><a href="grant-help.html">Grant application tips and free help</a></li>
            </ul>
        </div>
    </section>

    </main>

    <script>
    /* Mark grants Closed once their deadline has passed (same rule as the Grant Finder). */
    (function () {
        var now = Date.now();
        document.querySelectorAll('.grant-card[data-deadline]').forEach(function (c) {
            var d = c.getAttribute('data-deadline');
            if (/^\\d{4}-\\d{2}-\\d{2}$/.test(d) && new Date(d + 'T23:59:59Z').getTime() < now) {
                var t = c.querySelector('.grant-tag[class*="status-"]');
                if (t) { t.className = 'grant-tag status-closed'; t.textContent = 'Closed'; }
            }
        });
    })();
    </script>

    `;

  write(p.file, head + rest.slice(0, rest.indexOf('<body')) + bodyOpen + main + footer);
  return { file: p.file, count: list.length, c, words: (p.intro(list.length, c) + list.map((g) => g.description).join(' ')).split(/\s+/).length };
}

// ---- grants.html: static list, count, and category links -------------------
function replaceBetween(src, start, end, inner) {
  const a = src.indexOf(start), b = src.indexOf(end);
  if (a < 0 || b < 0 || b < a) throw new Error('Missing marker ' + start + ' / ' + end + ' in grants.html');
  return src.slice(0, a + start.length) + inner + src.slice(b);
}

function updateGrantsPage() {
  let s = read('grants.html');
  s = replaceBetween(s, '<!--GRANTS:START-->', '<!--GRANTS:END-->',
    '\n' + grants.map((g) => '                ' + card(g)).join('\n') + '\n            ');
  s = replaceBetween(s, '<!--COUNT:START-->', '<!--COUNT:END-->', grants.length + ' grants');
  const counts = {};
  grants.forEach((g) => { counts[g.category] = (counts[g.category] || 0) + 1; });
  s = replaceBetween(s, '<!--LISTS:START-->', '<!--LISTS:END-->',
    '\n                <p class="grant-lists">Browse by group: ' +
    PAGES.map((p) => '<a href="' + p.file + '">' + esc(p.short) + ' (' + counts[p.category] + ')</a>').join(' &middot; ') +
    '</p>\n                ');
  write('grants.html', s);
}

const results = PAGES.map(buildCategoryPage);
updateGrantsPage();
results.forEach((r) => console.log(r.file, r.count + ' grants', JSON.stringify(r.c), '~' + r.words + ' words'));
console.log('grants.html updated with ' + grants.length + ' static cards (build date ' + BUILD_ISO + ')');
