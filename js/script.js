/* =========================================================
   e3 Initiative – main script
   Handles: article rendering, scroll animations, back-to-top,
            article filtering, and date formatting.
   No external dependencies.
   ========================================================= */

/* ----------------------------------------------------------
   1. Utilities
   ---------------------------------------------------------- */

/** Escape HTML special characters to prevent XSS. */
function escHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

/** Format a YYYY-MM-DD date string as "Month D, YYYY". */
function formatDate(dateStr) {
    // Parse as UTC so timezone offsets don't shift the day
    const [year, month, day] = dateStr.split('-').map(Number);
    const d = new Date(Date.UTC(year, month - 1, day));
    return d.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        timeZone: 'UTC'
    });
}

/* ----------------------------------------------------------
   2. Article rendering
   ---------------------------------------------------------- */
function buildCard(article) {
    const card = document.createElement('article');
    card.className = 'article-card clickable-card fade-up';
    card.setAttribute('role', 'link');
    card.setAttribute('tabindex', '0');
    card.setAttribute('data-type', article.type || 'article');

    // Navigate on click or Enter key press
    card.addEventListener('click', () => { window.location.href = article.link; });
    card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') { window.location.href = article.link; }
    });

    card.innerHTML =
        '<div class="card-media">' +
            '<img src="' + escHtml(article.image) + '" alt="' + escHtml(article.imageAlt || '') + '" loading="lazy">' +
        '</div>' +
        '<div class="article-content">' +
            '<p class="article-date">' + escHtml(formatDate(article.date)) + '</p>' +
            '<h3>' + escHtml(article.title) + '</h3>' +
            '<p>' + escHtml(article.summary) + '</p>' +
            '<a href="' + escHtml(article.link) + '" class="read-more">Read more →</a>' +
        '</div>';

    return card;
}

function populateGrids() {
    const data = window.articlesData;
    if (!Array.isArray(data)) { return; }

    // Sort newest-first
    const sorted = data.slice().sort((a, b) => (b.date > a.date ? 1 : -1));

    document.querySelectorAll('.articles-grid').forEach(function (grid) {
        const typeFilter = (grid.getAttribute('data-type') || 'all').toLowerCase();
        const statusEl = document.getElementById(
            grid.id === 'latestArticles' ? 'latestArticlesStatus' :
            grid.id === 'articlesGrid'   ? 'articlesStatus'        :
            grid.id === 'researchGrid'   ? 'researchStatus'        : ''
        );

        const isResearchContext = typeFilter === 'research';

        // Filter articles by type (unless "all")
        let articles = typeFilter === 'all'
            ? sorted
            : sorted.filter(function (a) { return a.type === typeFilter; });

        // Homepage: limit to 3 most recent
        const isHomepage = grid.id === 'latestArticles';
        if (isHomepage) { articles = articles.slice(0, 3); }

        if (articles.length === 0) {
            if (statusEl) {
                statusEl.textContent = isResearchContext
                    ? 'No research papers are available yet'
                    : 'No articles available yet';
                statusEl.style.display = '';
            }
            return;
        }

        articles.forEach(function (article) { grid.appendChild(buildCard(article)); });

        // Hide the loading/status message on success
        if (statusEl) { statusEl.style.display = 'none'; }

        // Attach fade-up observer to newly created cards
        observeElements(grid.querySelectorAll('.article-card'));
    });
}

/* ----------------------------------------------------------
   3. Scroll animations via IntersectionObserver
   ---------------------------------------------------------- */
var scrollObserver = null;

function createObserver() {
    if (!('IntersectionObserver' in window)) { return null; }
    return new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
}

function observeElements(elements) {
    if (!scrollObserver) { return; }
    elements.forEach(function (el) { scrollObserver.observe(el); });
}

function initScrollAnimations() {
    scrollObserver = createObserver();
    const selector = '.pillar-card, .feature-card, .team-card, .liquid-glass, .section-header';
    document.querySelectorAll(selector).forEach(function (el) {
        el.classList.add('fade-up');
    });
    observeElements(document.querySelectorAll('.fade-up'));
}

/* ----------------------------------------------------------
   4. Back-to-top button
   ---------------------------------------------------------- */
function initBackToTop() {
    document.querySelectorAll('.to-top').forEach(function (btn) {
        btn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
}

/* ----------------------------------------------------------
   5. Article filtering (articles.html)
   ---------------------------------------------------------- */
function initFilters() {
    document.querySelectorAll('[data-filter]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const filter = btn.getAttribute('data-filter').toLowerCase();

            // Toggle active state on filter buttons
            document.querySelectorAll('[data-filter]').forEach(function (b) {
                b.classList.toggle('active', b === btn);
            });

            // Show/hide cards in every grid on the page
            document.querySelectorAll('.article-card').forEach(function (card) {
                const type = (card.getAttribute('data-type') || '').toLowerCase();
                const show = filter === 'all' || type === filter;
                card.style.display = show ? '' : 'none';
            });
        });
    });
}

/* ----------------------------------------------------------
   6. Settings panel (theme + font size)
   ---------------------------------------------------------- */
var FONT_SIZES = { small: '0.9', normal: '1', large: '1.15' };

function initSettings() {
    // Apply saved preferences immediately
    var savedTheme = localStorage.getItem('theme') || 'dark';
    var savedFont  = localStorage.getItem('fontSize') || 'normal';
    applyTheme(savedTheme);
    applyFontSize(savedFont);

    // Inject settings button into navbar
    var navbar = document.querySelector('.navbar .container');
    if (!navbar) { return; }

    var btn = document.createElement('button');
    btn.className = 'settings-btn';
    btn.setAttribute('aria-label', 'Settings');
    btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>';
    navbar.appendChild(btn);

    // Build panel
    var panel = document.createElement('div');
    panel.className = 'settings-panel';
    panel.innerHTML =
        '<p class="settings-label">Appearance</p>' +
        '<div class="settings-row">' +
            '<span>Dark mode</span>' +
            '<label class="settings-pill">' +
                '<input type="checkbox" id="settings-theme-toggle">' +
                '<span class="settings-pill-track"><span class="settings-pill-thumb"></span></span>' +
            '</label>' +
        '</div>' +
        '<p class="settings-label">Text size</p>' +
        '<div class="settings-row settings-font-row">' +
            '<button class="font-btn" data-size="small">A<sup>-</sup></button>' +
            '<button class="font-btn" data-size="normal">A</button>' +
            '<button class="font-btn" data-size="large">A<sup>+</sup></button>' +
        '</div>';
    document.body.appendChild(panel);

    // Sync theme toggle state
    var themeCheckbox = panel.querySelector('#settings-theme-toggle');
    if (savedTheme === 'light') { themeCheckbox.checked = true; }

    // Sync font buttons
    syncFontButtons(panel, savedFont);

    // Toggle panel open/close
    btn.addEventListener('click', function (e) {
        e.stopPropagation();
        panel.classList.toggle('open');
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
        if (!panel.contains(e.target) && e.target !== btn) {
            panel.classList.remove('open');
        }
    });

    // Theme toggle
    themeCheckbox.addEventListener('change', function () {
        var newTheme = themeCheckbox.checked ? 'light' : 'dark';
        applyTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // Font size buttons
    panel.querySelectorAll('.font-btn').forEach(function (fontBtn) {
        fontBtn.addEventListener('click', function () {
            var size = fontBtn.getAttribute('data-size');
            applyFontSize(size);
            localStorage.setItem('fontSize', size);
            syncFontButtons(panel, size);
        });
    });
}

function syncFontButtons(panel, active) {
    panel.querySelectorAll('.font-btn').forEach(function (b) {
        b.classList.toggle('active', b.getAttribute('data-size') === active);
    });
}

function applyTheme(theme) {
    var html = document.documentElement;
    var cb = document.getElementById('settings-theme-toggle');
    if (theme === 'light') {
        html.classList.add('light-mode');
        if (cb) { cb.checked = true; }
    } else {
        html.classList.remove('light-mode');
        if (cb) { cb.checked = false; }
    }
}

function applyFontSize(size) {
    document.documentElement.style.setProperty('--font-scale', FONT_SIZES[size] || '1');
}

/* ----------------------------------------------------------
   7. Bootstrap on DOMContentLoaded
   ---------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', function () {
    initSettings();
    initScrollAnimations();
    populateGrids();
    initBackToTop();
    initFilters();
});