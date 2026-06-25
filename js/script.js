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
    if (indicatorRedraw) { indicatorRedraw(); }
}

function applyFontSize(size) {
    document.documentElement.style.setProperty('--font-scale', FONT_SIZES[size] || '1');
    if (indicatorRedraw) { indicatorRedraw(); }
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
   7. Contact form (FormSubmit.co AJAX)
   ---------------------------------------------------------- */
var CONTACT_ENDPOINT = 'https://formsubmit.co/ajax/akshatsawner11@gmail.com';

function initContactForm() {
    var form = document.getElementById('contactForm');
    if (!form) { return; }

    var status = document.getElementById('contactStatus');
    var submitBtn = form.querySelector('button[type="submit"]');

    function setStatus(message, state) {
        if (!status) { return; }
        status.textContent = message;
        if (state) { status.setAttribute('data-state', state); }
        else { status.removeAttribute('data-state'); }
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        // Honeypot tripped — silently pretend success, drop the submission.
        if (form.elements._honey && form.elements._honey.value) { return; }

        setStatus('Sending…', null);
        if (submitBtn) { submitBtn.disabled = true; }

        fetch(CONTACT_ENDPOINT, {
            method: 'POST',
            headers: { 'Accept': 'application/json' },
            body: new FormData(form)
        })
            .then(function (res) {
                return res.json().catch(function () { return {}; }).then(function (data) {
                    if (!res.ok) { throw new Error((data && data.message) || ('HTTP ' + res.status)); }
                    var ok = data && (data.success === true || data.success === 'true');
                    if (!ok) { throw new Error((data && data.message) || 'Submission failed'); }
                    return data;
                });
            })
            .then(function () {
                form.reset();
                setStatus('Thanks! Your message has been sent — we’ll reply within two business days.', 'success');
            })
            .catch(function (err) {
                if (window.console && console.warn) { console.warn('Contact form submission failed:', err && err.message); }
                setStatus('Sorry, something went wrong. Please email us directly at akshatsawner11@gmail.com.', 'error');
            })
            .then(function () {
                if (submitBtn) { submitBtn.disabled = false; }
            });
    });
}

/* ----------------------------------------------------------
   5. Economic indicator charts (homepage)
   ---------------------------------------------------------- */
var indicatorRedraw = null;
var indicatorStateByCanvas = new WeakMap();
var indicatorYears = [];

function buildYearRange(start, end) {
    var years = [];
    for (var y = start; y <= end; y += 1) { years.push(y); }
    return years;
}

function interpolateSeries(anchors, years) {
    var anchorYears = Object.keys(anchors).map(Number).sort(function (a, b) { return a - b; });
    return years.map(function (year) {
        if (anchors[year] != null) { return anchors[year]; }

        var prevYear = null;
        var nextYear = null;

        for (var i = 0; i < anchorYears.length; i += 1) {
            var y = anchorYears[i];
            if (y < year) { prevYear = y; }
            if (y > year) { nextYear = y; break; }
        }

        if (prevYear == null && nextYear == null) { return 0; }
        if (prevYear == null) { return anchors[nextYear]; }
        if (nextYear == null) { return anchors[prevYear]; }

        var ratio = (year - prevYear) / (nextYear - prevYear);
        return anchors[prevYear] + (anchors[nextYear] - anchors[prevYear]) * ratio;
    });
}

var INDICATOR_START_YEAR = 2000;
var INDICATOR_END_YEAR = Math.max(2026, new Date().getUTCFullYear());
var INDICATOR_YEARS = buildYearRange(INDICATOR_START_YEAR, INDICATOR_END_YEAR);
indicatorYears = INDICATOR_YEARS.slice();

var INDICATOR_SERIES = {
    cpi: {
        line: '#80b8ff',
        fill: 'rgba(128, 184, 255, 0.2)',
        format: function (v) { return 'Index ' + v.toFixed(1); },
        values: interpolateSeries({
            2000: 172.2, 2003: 184.0, 2006: 201.6, 2009: 214.5, 2012: 229.6,
            2015: 237.0, 2019: 255.7, 2020: 258.8, 2021: 271.0, 2022: 292.7,
            2023: 305.4, 2024: 313.5, 2025: 317.0, 2026: 320.0
        }, INDICATOR_YEARS)
    },
    core_cpi: {
        line: '#9ec5ff',
        fill: 'rgba(158, 197, 255, 0.19)',
        format: function (v) { return 'Index ' + v.toFixed(1); },
        values: interpolateSeries({
            2000: 174.0, 2003: 183.0, 2008: 218.0, 2012: 232.0, 2016: 249.0,
            2019: 259.0, 2021: 271.0, 2022: 291.0, 2023: 305.0, 2024: 313.0,
            2025: 318.0, 2026: 322.0
        }, INDICATOR_YEARS)
    },
    ppi: {
        line: '#63d4d8',
        fill: 'rgba(99, 212, 216, 0.19)',
        format: function (v) { return 'Index ' + v.toFixed(1); },
        values: interpolateSeries({
            2000: 136.0, 2003: 142.0, 2008: 191.0, 2009: 173.0, 2012: 198.0,
            2016: 190.0, 2019: 203.0, 2020: 199.0, 2021: 238.0, 2022: 281.0,
            2023: 269.0, 2024: 274.0, 2025: 278.0, 2026: 281.0
        }, INDICATOR_YEARS)
    },
    core_pce: {
        line: '#58cf9f',
        fill: 'rgba(88, 207, 159, 0.19)',
        format: function (v) { return 'Index ' + v.toFixed(1); },
        values: interpolateSeries({
            2000: 79.0, 2003: 85.0, 2008: 96.0, 2012: 104.0, 2016: 112.0,
            2019: 119.0, 2020: 121.0, 2021: 126.0, 2022: 136.0, 2023: 143.0,
            2024: 148.0, 2025: 152.0, 2026: 155.0
        }, INDICATOR_YEARS)
    },
    fed_funds: {
        line: '#f5b66b',
        fill: 'rgba(245, 182, 107, 0.2)',
        format: function (v) { return v.toFixed(2) + '%'; },
        values: interpolateSeries({
            2000: 6.2, 2003: 1.1, 2006: 5.0, 2009: 0.2, 2015: 0.1,
            2018: 2.4, 2020: 0.1, 2022: 3.8, 2023: 5.2, 2024: 5.1,
            2025: 4.8, 2026: 4.5
        }, INDICATOR_YEARS)
    },
    unemployment: {
        line: '#ff9383',
        fill: 'rgba(255, 147, 131, 0.2)',
        format: function (v) { return v.toFixed(1) + '%'; },
        values: interpolateSeries({
            2000: 4.0, 2003: 6.0, 2007: 4.6, 2010: 9.6, 2014: 6.2,
            2017: 4.4, 2019: 3.7, 2020: 8.1, 2022: 3.6, 2024: 3.9,
            2025: 4.1, 2026: 4.2
        }, INDICATOR_YEARS)
    },
    payrolls: {
        line: '#c2a7ff',
        fill: 'rgba(194, 167, 255, 0.2)',
        format: function (v) { return v.toFixed(1) + 'M'; },
        values: interpolateSeries({
            2000: 132.0, 2003: 130.0, 2007: 138.0, 2010: 130.0, 2014: 138.0,
            2018: 150.0, 2019: 152.0, 2020: 142.0, 2022: 153.0, 2024: 158.0,
            2025: 159.0, 2026: 160.0
        }, INDICATOR_YEARS)
    },
    ten_year: {
        line: '#8ed4ff',
        fill: 'rgba(142, 212, 255, 0.2)',
        format: function (v) { return v.toFixed(2) + '%'; },
        values: interpolateSeries({
            2000: 6.0, 2003: 4.0, 2007: 4.6, 2012: 1.8, 2016: 1.8,
            2018: 2.9, 2020: 0.9, 2022: 3.0, 2023: 4.0, 2024: 4.2,
            2025: 4.3, 2026: 4.1
        }, INDICATOR_YEARS)
    }
};

function buildIndicatorTickYears(years) {
    if (!years || !years.length) { return []; }

    var start = years[0];
    var end = years[years.length - 1];
    var ticks = [start];

    var decade = Math.ceil((start + 1) / 10) * 10;
    while (decade < end) {
        ticks.push(decade);
        decade += 10;
    }

    if (ticks[ticks.length - 1] !== end) {
        ticks.push(end);
    }

    return ticks;
}

function setIndicatorStatus(message, kind) {
    var statusEl = document.getElementById('indicator-data-status');
    if (!statusEl) { return; }

    statusEl.textContent = message;
    statusEl.dataset.kind = kind || 'default';
}

function mergeIndicatorData(seriesByKey, years) {
    if (!Array.isArray(years) || !years.length || !seriesByKey) { return false; }

    var numericYears = years.map(Number).filter(function (year) {
        return Number.isFinite(year);
    });
    if (!numericYears.length) { return false; }

    var hasAnySeries = false;
    Object.keys(INDICATOR_SERIES).forEach(function (key) {
        var nextValues = seriesByKey[key];
        if (!Array.isArray(nextValues) || nextValues.length !== numericYears.length) { return; }

        var isValid = nextValues.every(function (value) {
            return typeof value === 'number' && Number.isFinite(value);
        });
        if (!isValid) { return; }

        INDICATOR_SERIES[key].values = nextValues.slice();
        hasAnySeries = true;
    });

    if (!hasAnySeries) { return false; }

    indicatorYears = numericYears.slice();
    return true;
}

function loadLiveIndicatorData(renderAll) {
    if (!window.fetch) { return; }
    if (window.location.protocol !== 'http:' && window.location.protocol !== 'https:') {
        setIndicatorStatus('Live auto-updates run on the deployed site. Local file preview uses fallback data.', 'fallback');
        return;
    }

    fetch('/api/economic-indicators', { cache: 'no-store' })
        .then(function (response) {
            if (!response.ok) {
                throw new Error('Status ' + response.status);
            }
            return response.json();
        })
        .then(function (payload) {
            var applied = mergeIndicatorData(payload.series, payload.years);
            if (!applied) {
                throw new Error('Invalid payload');
            }

            renderAll();

            var asOf = payload && payload.asOfDate ? payload.asOfDate : null;
            if (asOf) {
                setIndicatorStatus('Auto-updating from FRED. Latest observation: ' + asOf + '.', 'live');
            } else {
                setIndicatorStatus('Auto-updating from FRED.', 'live');
            }
        })
        .catch(function () {
            setIndicatorStatus('Using embedded data (live source unavailable).', 'fallback');
        });
}

function drawIndicatorChart(canvas, config, hoverIndex) {
    var ctx = canvas.getContext('2d');
    if (!ctx) { return null; }

    var rect = canvas.getBoundingClientRect();
    if (!rect.width || !rect.height) { return null; }

    var dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(rect.width * dpr);
    canvas.height = Math.round(rect.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, rect.width, rect.height);

    var w = rect.width;
    var h = rect.height;
    var pad = { left: 36, right: 10, top: 10, bottom: 24 };
    var plotW = w - pad.left - pad.right;
    var plotH = h - pad.top - pad.bottom;

    var years = config.years || indicatorYears;
    if (!years || years.length !== config.values.length) {
        years = INDICATOR_YEARS;
    }

    var values = config.values;
    if (!values || values.length < 2) { return null; }

    var min = Math.min.apply(null, values);
    var max = Math.max.apply(null, values);
    var span = max - min || 1;
    min -= span * 0.08;
    max += span * 0.08;

    function xAt(i) {
        return pad.left + (plotW * i) / (values.length - 1);
    }

    function yAt(v) {
        return pad.top + (max - v) * (plotH / (max - min));
    }

    function axisLabel(v) {
        var label = config.format ? config.format(v) : v.toFixed(1);
        return String(label).replace(/^Index\s*/, '');
    }

    var points = values.map(function (value, idx) {
        return {
            idx: idx,
            x: xAt(idx),
            y: yAt(value),
            year: years[idx],
            value: value
        };
    });

    var axisColor = document.documentElement.classList.contains('light-mode')
        ? 'rgba(0, 0, 0, 0.2)'
        : 'rgba(255, 255, 255, 0.2)';
    var labelColor = document.documentElement.classList.contains('light-mode')
        ? 'rgba(0, 0, 0, 0.65)'
        : 'rgba(255, 255, 255, 0.65)';
    var gridColor = document.documentElement.classList.contains('light-mode')
        ? 'rgba(0, 0, 0, 0.08)'
        : 'rgba(255, 255, 255, 0.09)';

    var yTicks = [max, (max + min) / 2, min];
    ctx.strokeStyle = gridColor;
    ctx.lineWidth = 1;
    yTicks.forEach(function (tick) {
        var y = yAt(tick);
        ctx.beginPath();
        ctx.moveTo(pad.left, y);
        ctx.lineTo(w - pad.right, y);
        ctx.stroke();
    });

    ctx.fillStyle = labelColor;
    ctx.font = '10px "Instrument Sans", sans-serif';
    ctx.textAlign = 'left';
    yTicks.forEach(function (tick) {
        var y = yAt(tick);
        ctx.fillText(axisLabel(tick), 2, y + 3);
    });

    ctx.beginPath();
    ctx.moveTo(pad.left, h - pad.bottom);
    ctx.lineTo(w - pad.right, h - pad.bottom);
    ctx.strokeStyle = axisColor;
    ctx.lineWidth = 1;
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (var i = 1; i < points.length; i += 1) {
        ctx.lineTo(points[i].x, points[i].y);
    }
    ctx.lineTo(points[points.length - 1].x, h - pad.bottom);
    ctx.lineTo(points[0].x, h - pad.bottom);
    ctx.closePath();
    ctx.fillStyle = config.fill;
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(points[0].x, points[0].y);
    for (var j = 1; j < points.length; j += 1) {
        ctx.lineTo(points[j].x, points[j].y);
    }
    ctx.strokeStyle = config.line;
    ctx.lineWidth = 2.2;
    ctx.stroke();

    if (hoverIndex != null && points[hoverIndex]) {
        var p = points[hoverIndex];
        var hoverGuide = document.documentElement.classList.contains('light-mode')
            ? 'rgba(0, 0, 0, 0.25)'
            : 'rgba(255, 255, 255, 0.28)';

        ctx.beginPath();
        ctx.moveTo(p.x, pad.top);
        ctx.lineTo(p.x, h - pad.bottom);
        ctx.strokeStyle = hoverGuide;
        ctx.lineWidth = 1;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(p.x, p.y, 3.2, 0, Math.PI * 2);
        ctx.fillStyle = config.line;
        ctx.fill();
    }

    var tickYears = buildIndicatorTickYears(years);
    ctx.fillStyle = labelColor;
    ctx.font = '11px "Instrument Sans", sans-serif';
    tickYears.forEach(function (year, idx) {
        var yearIndex = years.indexOf(year);
        if (yearIndex < 0) { return; }
        var x = xAt(yearIndex);
        ctx.textAlign = idx === 0 ? 'left' : (idx === tickYears.length - 1 ? 'right' : 'center');
        ctx.fillText(String(year), x, h - 7);
    });

    return { points: points };
}

function initIndicatorCharts() {
    var cards = document.querySelectorAll('[data-indicator-key]');
    if (!cards.length) { return; }

    function setTooltipTheme(tooltip) {
        if (document.documentElement.classList.contains('light-mode')) {
            tooltip.style.background = 'rgba(255, 255, 255, 0.95)';
            tooltip.style.color = '#111111';
            tooltip.style.borderColor = 'rgba(0, 0, 0, 0.2)';
        } else {
            tooltip.style.background = 'rgba(0, 0, 0, 0.9)';
            tooltip.style.color = '#f3f4f6';
            tooltip.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        }
    }

    function renderAll() {
        cards.forEach(function (card) {
            var key = card.getAttribute('data-indicator-key');
            var canvas = card.querySelector('.indicator-chart');
            var config = INDICATOR_SERIES[key];
            if (!canvas || !config) { return; }

            var state = drawIndicatorChart(canvas, config, null);
            if (state) { indicatorStateByCanvas.set(canvas, state); }
        });
    }

    cards.forEach(function (card) {
        var key = card.getAttribute('data-indicator-key');
        var canvas = card.querySelector('.indicator-chart');
        var config = INDICATOR_SERIES[key];
        if (!canvas || !config || canvas.dataset.interactiveBound === 'true') { return; }

        card.style.position = 'relative';

        if (!card.querySelector('.indicator-legend')) {
            var legend = document.createElement('div');
            legend.className = 'indicator-legend';
            var swatch = document.createElement('span');
            swatch.className = 'indicator-legend-swatch';
            swatch.style.background = config.line;
            var text = document.createElement('span');
            var cardTitle = card.querySelector('h3');
            text.textContent = cardTitle ? cardTitle.textContent : 'Trend';
            legend.appendChild(swatch);
            legend.appendChild(text);
            canvas.parentNode.insertAdjacentElement('afterend', legend);
        }

        var tooltip = document.createElement('div');
        tooltip.style.position = 'absolute';
        tooltip.style.left = '0';
        tooltip.style.top = '0';
        tooltip.style.transform = 'translate(-9999px, -9999px)';
        tooltip.style.pointerEvents = 'none';
        tooltip.style.padding = '0.32rem 0.55rem';
        tooltip.style.fontSize = '0.72rem';
        tooltip.style.borderRadius = '0.45rem';
        tooltip.style.border = '1px solid';
        tooltip.style.opacity = '0';
        tooltip.style.transition = 'opacity 0.12s ease';
        tooltip.style.zIndex = '3';
        setTooltipTheme(tooltip);
        card.appendChild(tooltip);

        function moveToClient(clientX, clientY) {
            var rect = canvas.getBoundingClientRect();
            var localX = clientX - rect.left;
            var state = indicatorStateByCanvas.get(canvas);
            if (!state || !state.points || !state.points.length) { return; }

            var nearest = state.points[0];
            var bestDx = Math.abs(localX - nearest.x);

            for (var i = 1; i < state.points.length; i += 1) {
                var dx = Math.abs(localX - state.points[i].x);
                if (dx < bestDx) {
                    bestDx = dx;
                    nearest = state.points[i];
                }
            }

            var redrawState = drawIndicatorChart(canvas, config, nearest.idx);
            if (redrawState) { indicatorStateByCanvas.set(canvas, redrawState); }

            var formatter = config.format || function (v) { return v.toFixed(1); };
            tooltip.textContent = nearest.year + ' • ' + formatter(nearest.value);
            setTooltipTheme(tooltip);
            tooltip.style.opacity = '1';

            var tipWidth = tooltip.offsetWidth || 120;
            var left = Math.min(Math.max(nearest.x + 10, 8), rect.width - tipWidth - 8);
            var top = Math.max(nearest.y - 28, 8);
            tooltip.style.transform = 'translate(' + left + 'px, ' + top + 'px)';
        }

        function resetHover() {
            var redrawState = drawIndicatorChart(canvas, config, null);
            if (redrawState) { indicatorStateByCanvas.set(canvas, redrawState); }
            tooltip.style.opacity = '0';
            tooltip.style.transform = 'translate(-9999px, -9999px)';
        }

        canvas.addEventListener('mousemove', function (evt) {
            moveToClient(evt.clientX, evt.clientY);
        });
        canvas.addEventListener('mouseleave', resetHover);
        canvas.addEventListener('touchstart', function (evt) {
            if (evt.touches && evt.touches[0]) {
                moveToClient(evt.touches[0].clientX, evt.touches[0].clientY);
            }
        }, { passive: true });
        canvas.addEventListener('touchmove', function (evt) {
            if (evt.touches && evt.touches[0]) {
                moveToClient(evt.touches[0].clientX, evt.touches[0].clientY);
            }
        }, { passive: true });
        canvas.addEventListener('touchend', resetHover, { passive: true });

        canvas.dataset.interactiveBound = 'true';
    });

    renderAll();
    loadLiveIndicatorData(renderAll);
    indicatorRedraw = function () {
        cards.forEach(function (card) {
            var tooltip = card.querySelector('div[style*="pointer-events: none"]');
            if (tooltip) { setTooltipTheme(tooltip); }
        });
        renderAll();
    };

    var resizeTimer = null;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(renderAll, 80);
    });
}


/* ----------------------------------------------------------
   8. Bootstrap on DOMContentLoaded
   ---------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', function () {
    initMobileNav();
    initSettings();
    initParallax();
    initIndicatorCharts();
    populateGrids();
    initBackToTop();
    initFilters();
    initContactForm();
});
