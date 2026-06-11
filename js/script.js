/* =========================================================
   e3 Initiative – main script
   Handles: article rendering, back-to-top, article filtering,
            and date formatting.
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
    card.className = 'article-card clickable-card';
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
    });
}

/* ----------------------------------------------------------
   3. Back-to-top button
   ---------------------------------------------------------- */
function initBackToTop() {
    document.querySelectorAll('.to-top').forEach(function (btn) {
        btn.addEventListener('click', function () {
            window.scrollTo(0, 0);
        });
    });

    var scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', function (e) {
            e.preventDefault();
            window.scrollBy({ top: window.innerHeight * 0.85, behavior: 'smooth' });
        });
    }
}

/* ----------------------------------------------------------
   4. Article filtering (articles.html)
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
   5. Parallax effects
   ---------------------------------------------------------- */
function initParallax() {
    var banners = document.querySelectorAll('.page-header-image img');
    var orbs    = document.querySelectorAll('.orb');
    var hero    = document.querySelector('.hero');

    if (!banners.length && !orbs.length) { return; }

    // Give banner images extra height so they have room to travel
    banners.forEach(function (img) {
        img.style.height = 'calc(100% + 160px)';
        img.style.marginTop = '-80px';
        img.style.willChange = 'transform';
    });

    orbs.forEach(function (orb) {
        orb.style.willChange = 'transform';
    });

    var ticking = false;

    function update() {
        var scrollY = window.pageYOffset;

        // Banner parallax — image moves up at 40% of scroll speed
        banners.forEach(function (img) {
            var rect = img.closest('.page-header-image').getBoundingClientRect();
            if (rect.bottom > 0 && rect.top < window.innerHeight) {
                img.style.transform = 'translateY(' + (scrollY * 0.35) + 'px)';
            }
        });

        // Orb parallax — each orb drifts at a slightly different speed
        orbs.forEach(function (orb, i) {
            var speed = 0.04 + i * 0.03;
            orb.style.transform = 'translateY(' + (scrollY * speed) + 'px)';
        });

        // Hero content subtle upward drift
        if (hero) {
            var heroContainer = hero.querySelector('.container');
            if (heroContainer && scrollY < window.innerHeight) {
                heroContainer.style.transform = 'translateY(' + (scrollY * 0.15) + 'px)';
            }
        }

        ticking = false;
    }

    window.addEventListener('scroll', function () {
        if (!ticking) {
            requestAnimationFrame(update);
            ticking = true;
        }
    }, { passive: true });

    update();
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

    // Use existing settings button in nav, fallback to creating one.
    var navbar = document.querySelector('.navbar .container');
    if (!navbar) { return; }

    var btn = navbar.querySelector('.settings-btn');
    if (!btn) {
        btn = document.createElement('button');
        btn.className = 'settings-btn';
        btn.setAttribute('aria-label', 'Settings');
        btn.textContent = '⚙️';
        navbar.appendChild(btn);
    }

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
   Mobile navigation (hamburger menu)
   ---------------------------------------------------------- */
function initMobileNav() {
    var navbar = document.querySelector('.navbar .container');
    var navLinks = document.querySelector('.nav-links');
    if (!navbar || !navLinks) { return; }

    var hamburger = document.createElement('button');
    hamburger.className = 'hamburger';
    hamburger.setAttribute('aria-label', 'Toggle navigation');
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.innerHTML = '<span></span><span></span><span></span>';

    // Insert before settings button if it exists, else append
    var settingsBtn = navbar.querySelector('.settings-btn');
    if (settingsBtn) {
        navbar.insertBefore(hamburger, settingsBtn);
    } else {
        navbar.appendChild(hamburger);
    }

    function closeMenu() {
        navLinks.classList.remove('mobile-open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
    }

    hamburger.addEventListener('click', function (e) {
        e.stopPropagation();
        var isOpen = navLinks.classList.toggle('mobile-open');
        hamburger.classList.toggle('open', isOpen);
        hamburger.setAttribute('aria-expanded', String(isOpen));
    });

    // Close when a nav link is clicked
    navLinks.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', closeMenu);
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
        if (!navbar.contains(e.target)) { closeMenu(); }
    });

    // Close on resize to desktop
    window.addEventListener('resize', function () {
        if (window.innerWidth > 768) { closeMenu(); }
    });
}

/* ----------------------------------------------------------
   7. Bootstrap on DOMContentLoaded
   ---------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', function () {
    initMobileNav();
    initSettings();
    initParallax();
    populateGrids();
    initBackToTop();
    initFilters();
});
