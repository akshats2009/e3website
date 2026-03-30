/* =========================================================
   e3 Initiative – main script
   Handles: article rendering, scroll animations, back-to-top,
            article filtering, date formatting, and settings panel.
   No external dependencies.
   ========================================================= */

/* Apply saved preferences immediately to prevent flash */
(function () {
    var theme = localStorage.getItem('e3-theme');
    if (theme === 'light') document.body.classList.add('light-mode');
    var size = localStorage.getItem('e3-font-size');
    if (size) document.body.classList.add(size);
})();

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
    const card = document.createElement('a');
    card.className = 'article-card clickable-card fade-up';
    card.href = article.link;
    card.setAttribute('data-type', article.type || 'article');
    card.setAttribute('aria-label', 'Read: ' + (article.title || 'article'));

    card.innerHTML =
        '<div class="card-media">' +
            '<img src="' + escHtml(article.image) + '" alt="' + escHtml(article.imageAlt || '') + '" loading="lazy">' +
        '</div>' +
        '<div class="article-content">' +
            '<p class="article-date">' + escHtml(formatDate(article.date)) + '</p>' +
            '<h3>' + escHtml(article.title) + '</h3>' +
            '<p>' + escHtml(article.summary) + '</p>' +
            '<span class="read-more" aria-hidden="true">Read more →</span>' +
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
    const noMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    document.querySelectorAll('.to-top').forEach(function (btn) {
        btn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: noMotion ? 'auto' : 'smooth' });
        });
    });
}

/* ----------------------------------------------------------
   5b. Contact form (contact.html)
   Uses mailto so static hosting still works without a backend.
   ---------------------------------------------------------- */
function initContactForm() {
    const form = document.getElementById('contactForm');
    if (!form) { return; }

    const status = document.getElementById('contactStatus');
    const contactEmail = form.getAttribute('data-contact-email') || 'contact@e3initiative.org';

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const name = form.querySelector('#name') ? form.querySelector('#name').value.trim() : '';
        const email = form.querySelector('#email') ? form.querySelector('#email').value.trim() : '';
        const subject = form.querySelector('#subject') ? form.querySelector('#subject').value.trim() : '';
        const message = form.querySelector('#message') ? form.querySelector('#message').value.trim() : '';

        const emailSubject = subject || 'Website inquiry from e3 Initiative';
        const emailBody = [
            'Name: ' + name,
            'Email: ' + email,
            '',
            message
        ].join('\n');

        const mailto = 'mailto:' + encodeURIComponent(contactEmail) +
            '?subject=' + encodeURIComponent(emailSubject) +
            '&body=' + encodeURIComponent(emailBody);

        if (status) {
            status.textContent = 'Opening your email app...';
        }

        window.location.href = mailto;
        form.reset();
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
   6. Settings panel (hamburger menu)
   ---------------------------------------------------------- */
function initSettingsPanel() {
    var toggle = document.querySelector('.menu-toggle');
    var panel = document.querySelector('.settings-panel');
    var overlay = document.querySelector('.settings-overlay');
    if (!toggle || !panel) return;

    function openPanel() {
        toggle.classList.add('active');
        panel.classList.add('open');
        if (overlay) overlay.classList.add('open');
        toggle.setAttribute('aria-expanded', 'true');
    }

    function closePanel() {
        toggle.classList.remove('active');
        panel.classList.remove('open');
        if (overlay) overlay.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
    }

    toggle.addEventListener('click', function () {
        if (panel.classList.contains('open')) closePanel();
        else openPanel();
    });

    if (overlay) overlay.addEventListener('click', closePanel);

    // Dark/light mode toggle
    var themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        var savedTheme = localStorage.getItem('e3-theme');
        if (savedTheme === 'light') {
            document.body.classList.add('light-mode');
            themeToggle.classList.add('active');
        }

        themeToggle.addEventListener('click', function () {
            themeToggle.classList.toggle('active');
            document.body.classList.toggle('light-mode');
            localStorage.setItem('e3-theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');
        });
    }

    // Font size controls
    var sizes = ['font-small', 'font-normal', 'font-large', 'font-xlarge'];
    var savedSize = localStorage.getItem('e3-font-size') || 'font-normal';
    document.body.classList.add(savedSize);

    document.querySelectorAll('.font-size-btn').forEach(function (btn) {
        if (btn.getAttribute('data-size') === savedSize) btn.classList.add('active');

        btn.addEventListener('click', function () {
            var size = btn.getAttribute('data-size');
            sizes.forEach(function (s) { document.body.classList.remove(s); });
            document.body.classList.add(size);
            localStorage.setItem('e3-font-size', size);

            document.querySelectorAll('.font-size-btn').forEach(function (b) {
                b.classList.toggle('active', b === btn);
            });
        });
    });
}

/* ----------------------------------------------------------
   7. Bootstrap on DOMContentLoaded
   ---------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', function () {
    initScrollAnimations();
    populateGrids();
    initBackToTop();
    initContactForm();
    initFilters();
    initSettingsPanel();
});

/* ----------------------------------------------------------
   7. Aesthetic enhancements — parallax, micro-interactions
   No content or layout changes; all purely visual.
   ---------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', function () {
    var noMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Scroll progress bar
    var progressBar = null;
    if (!noMotion) {
        progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        document.body.prepend(progressBar);
    }

    // Scroll handler: progress bar + navbar compact + pillar parallax
    var ticking = false;
    function onScroll() {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () {
            var scrollY = window.scrollY;
            var docH = document.documentElement.scrollHeight - window.innerHeight;

            // Progress bar
            if (progressBar && docH > 0) {
                progressBar.style.width = Math.min((scrollY / docH) * 100, 100) + '%';
            }

            // Navbar compact
            var navbar = document.querySelector('.navbar');
            if (navbar) navbar.classList.toggle('scrolled', scrollY > 60);

            if (!noMotion) {
                // Pillar cards — each drifts at a slightly different scroll speed
                // Uses CSS `translate` (independent of transform) so fade-in animations are unaffected
                document.querySelectorAll('.pillar-card').forEach(function (card, i) {
                    var rect = card.getBoundingClientRect();
                    var dist = (rect.top + rect.height / 2) - window.innerHeight * 0.5;
                    var speeds = [0.04, 0.07, 0.055];
                    card.style.translate = '0 ' + (dist * speeds[i % speeds.length] * 0.25) + 'px';
                });

                // Ambient orb layer drifts at 12% scroll speed via CSS custom property
                document.body.style.setProperty('--scroll-y', scrollY);
            }

            ticking = false;
        });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    if (!noMotion) {
        // 3D card tilt on mousemove
        document.querySelectorAll('.pillar-card, .feature-card').forEach(function (card) {
            card.addEventListener('mousemove', function (e) {
                var rect = card.getBoundingClientRect();
                var x = (e.clientX - rect.left) / rect.width - 0.5;
                var y = (e.clientY - rect.top) / rect.height - 0.5;
                card.style.transform = 'perspective(800px) rotateX(' + (-y * 6) + 'deg) rotateY(' + (x * 6) + 'deg) translateY(-4px)';
            });
            card.addEventListener('mouseleave', function () {
                card.style.transition = 'transform 0.5s ease';
                card.style.transform = '';
                setTimeout(function () { card.style.transition = ''; }, 500);
            });
        });

        // Magnetic CTA buttons — follow cursor slightly on hover
        document.querySelectorAll('.btn').forEach(function (btn) {
            btn.addEventListener('mousemove', function (e) {
                var rect = btn.getBoundingClientRect();
                var x = (e.clientX - rect.left - rect.width / 2) * 0.25;
                var y = (e.clientY - rect.top - rect.height / 2) * 0.25;
                btn.style.transform = 'translate(' + x + 'px, ' + y + 'px)';
            });
            btn.addEventListener('mouseleave', function () {
                btn.style.transform = '';
            });
        });
    }

    // Page fade-out on internal navigation (disabled for reduced motion)
    if (!noMotion) {
        document.querySelectorAll('a[href]').forEach(function (link) {
            var href = link.getAttribute('href');
            if (!href || href[0] === '#' || /^(https?:|mailto:|tel:)/.test(href)) return;
            link.addEventListener('click', function (e) {
                if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
                e.preventDefault();
                document.body.style.transition = 'opacity 0.25s ease';
                document.body.style.opacity = '0';
                setTimeout(function () { window.location.href = href; }, 260);
            });
        });
    }
});