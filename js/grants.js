/* ----------------------------------------------------------
   Grant database — keyword search, browse, and filter
   Loads data/grants.json, renders a filterable grid, and runs a
   simple keyword search over the same data in the browser.
   ---------------------------------------------------------- */
(function () {
    'use strict';

    var CATEGORY_LABELS = {
        general: 'General',
        technology: 'Technology',
        arts_culture: 'Arts & Culture',
        food_agriculture: 'Food & Agriculture',
        community_development: 'Community Development',
        women_owned: 'Women-Owned',
        minority_owned: 'Minority-Owned',
        veteran_owned: 'Veteran-Owned',
        research: 'Research & Innovation',
        environment: 'Environment',
        health: 'Health'
    };

    var ELIGIBILITY_LABELS = {
        small_business: 'Small business',
        nonprofit: 'Nonprofit',
        both: 'Small business or nonprofit'
    };

    var STATUS_LABELS = { open: 'Open', rolling: 'Rolling', closed: 'Closed' };

    // Common words ignored by the keyword search
    var STOPWORDS = [
        'a', 'an', 'and', 'are', 'at', 'be', 'by', 'do', 'for', 'from', 'have', 'i',
        'in', 'is', 'it', 'me', 'my', 'need', 'of', 'on', 'or', 'our', 'run', 'that',
        'the', 'this', 'to', 'want', 'we', 'with'
    ];

    // Funding-amount buckets for the filter (label -> [min, max])
    var AMOUNT_BUCKETS = [
        { value: '', label: 'Any amount' },
        { value: '0-10000', label: 'Up to $10K', min: 0, max: 10000 },
        { value: '10000-50000', label: '$10K – $50K', min: 10000, max: 50000 },
        { value: '50000-100000', label: '$50K – $100K', min: 50000, max: 100000 },
        { value: '100000-', label: '$100K+', min: 100000, max: Infinity }
    ];

    var state = { grants: [], searchResults: null };

    function esc(s) {
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    function formatDeadline(g) {
        if (g.deadline === 'rolling') return 'Rolling / ongoing';
        if (g.deadline === 'annual') return 'Recurs annually';
        // ISO date -> readable
        var d = new Date(g.deadline + 'T00:00:00Z');
        if (isNaN(d.getTime())) return g.deadline;
        return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' });
    }

    function buildCard(g) {
        var card = document.createElement('article');
        card.className = 'grant-card';

        var tags =
            '<span class="grant-tag status-' + esc(g.status) + '">' + esc(STATUS_LABELS[g.status] || g.status) + '</span>' +
            '<span class="grant-tag">' + esc(ELIGIBILITY_LABELS[g.eligibility] || g.eligibility) + '</span>' +
            '<span class="grant-tag">' + esc(CATEGORY_LABELS[g.category] || g.category) + '</span>';

        var matched = g.matched
            ? '<div class="grant-reason"><strong>Matched on</strong>' + esc(g.matched) + '</div>'
            : '';

        card.innerHTML =
            '<p class="grant-funder">' + esc(g.funder) + '</p>' +
            '<h3>' + esc(g.name) + '</h3>' +
            '<div class="grant-tags">' + tags + '</div>' +
            matched +
            '<p class="grant-desc">' + esc(g.description) + '</p>' +
            '<div class="grant-meta">' +
                '<div class="grant-meta-row"><span class="label">Award</span><span class="value">' + esc(g.amount) + '</span></div>' +
                '<div class="grant-meta-row"><span class="label">Deadline</span><span class="value">' + esc(formatDeadline(g)) + '</span></div>' +
            '</div>' +
            '<a class="btn grant-apply" href="' + esc(g.link) + '" target="_blank" rel="noopener noreferrer">View &amp; apply →</a>';

        return card;
    }

    function passesFilters(g, f) {
        if (f.eligibility) {
            // "both" grants match either eligibility filter
            if (!(g.eligibility === f.eligibility || g.eligibility === 'both')) return false;
        }
        if (f.category && g.category !== f.category) return false;
        if (f.status && g.status !== f.status) return false;
        if (f.amount) {
            var bucket = AMOUNT_BUCKETS.filter(function (b) { return b.value === f.amount; })[0];
            if (bucket) {
                var amt = typeof g.amountMax === 'number' ? g.amountMax : 0;
                if (amt < bucket.min || amt > bucket.max) return false;
            }
        }
        return true;
    }

    function currentFilters() {
        return {
            eligibility: document.getElementById('filter-eligibility').value,
            category: document.getElementById('filter-category').value,
            amount: document.getElementById('filter-amount').value,
            status: document.getElementById('filter-status').value
        };
    }

    function renderGrid() {
        var grid = document.getElementById('grantsGrid');
        var countEl = document.getElementById('grantCount');
        var emptyEl = document.getElementById('grantEmpty');
        grid.innerHTML = '';

        var list;
        if (state.searchResults) {
            // Search mode: show only the matched grants, best match first
            list = state.searchResults;
        } else {
            var f = currentFilters();
            list = state.grants.filter(function (g) { return passesFilters(g, f); });
        }

        if (list.length === 0) {
            countEl.textContent = '';
            emptyEl.style.display = '';
            return;
        }
        emptyEl.style.display = 'none';
        countEl.textContent = list.length + (list.length === 1 ? ' grant' : ' grants') +
            (state.searchResults ? ' matched' : ' shown');

        list.forEach(function (g) { grid.appendChild(buildCard(g)); });
    }

    function populateSelect(id, options) {
        var sel = document.getElementById(id);
        options.forEach(function (o) {
            var opt = document.createElement('option');
            opt.value = o.value;
            opt.textContent = o.label;
            sel.appendChild(opt);
        });
    }

    function buildFilters() {
        // Only include categories that actually appear in the data
        var cats = {};
        state.grants.forEach(function (g) { cats[g.category] = true; });
        var catOpts = [{ value: '', label: 'All categories' }].concat(
            Object.keys(cats).map(function (c) {
                return { value: c, label: CATEGORY_LABELS[c] || c };
            })
        );

        populateSelect('filter-eligibility', [
            { value: '', label: 'Anyone' },
            { value: 'small_business', label: 'Small business' },
            { value: 'nonprofit', label: 'Nonprofit' }
        ]);
        populateSelect('filter-category', catOpts);
        populateSelect('filter-amount', AMOUNT_BUCKETS);
        populateSelect('filter-status', [
            { value: '', label: 'Any status' },
            { value: 'open', label: 'Open' },
            { value: 'rolling', label: 'Rolling' },
            { value: 'closed', label: 'Closed' }
        ]);

        ['filter-eligibility', 'filter-category', 'filter-amount', 'filter-status'].forEach(function (id) {
            document.getElementById(id).addEventListener('change', function () {
                // Changing a filter exits search-results mode
                clearSearchResults();
                renderGrid();
            });
        });
    }

    function setStatus(msg) {
        document.getElementById('finderStatus').textContent = msg || '';
    }

    function clearSearchResults() {
        state.searchResults = null;
        document.getElementById('finderResultsHeader').style.display = 'none';
        document.getElementById('grantFiltersHeading').style.display = '';
        document.getElementById('grantFilters').style.display = '';
    }

    // Split the search text into lowercase keywords, dropping short words and stopwords
    function tokenize(text) {
        return String(text || '').toLowerCase().split(/[^a-z0-9$]+/).filter(function (t) {
            return t.length > 1 && STOPWORDS.indexOf(t) === -1;
        });
    }

    // Score one grant against the keywords. Each keyword earns the weight of the
    // most important field it appears in: name > funder/category > everything else.
    function scoreGrant(g, tokens) {
        var fields = [
            [g.name, 3],
            [g.funder, 2],
            [CATEGORY_LABELS[g.category] || g.category, 2],
            [ELIGIBILITY_LABELS[g.eligibility], 1],
            [g.description, 1],
            [g.notes, 1]
        ].map(function (f) { return [String(f[0] || '').toLowerCase(), f[1]]; });

        var score = 0;
        var hits = [];
        tokens.forEach(function (t) {
            var best = 0;
            fields.forEach(function (f) {
                if (f[0].indexOf(t) !== -1 && f[1] > best) { best = f[1]; }
            });
            if (best > 0) {
                score += best;
                hits.push(t);
            }
        });
        return { score: score, hits: hits };
    }

    function runSearch() {
        var input = document.getElementById('finderInput');
        var query = input.value.trim();
        if (!query) { input.focus(); return; }

        var tokens = tokenize(query);
        if (tokens.length === 0) {
            setStatus('Try a few keywords, like "women-owned", "arts", or "Chicago".');
            return;
        }

        var results = [];
        state.grants.forEach(function (g) {
            var s = scoreGrant(g, tokens);
            if (s.hits.length > 0) {
                results.push(Object.assign({}, g, {
                    matched: s.hits.join(', '),
                    _score: s.score,
                    _hits: s.hits.length
                }));
            }
        });

        // Most keywords matched first, then strongest field matches
        results.sort(function (a, b) {
            return (b._hits - a._hits) || (b._score - a._score);
        });

        if (results.length === 0) {
            document.getElementById('grantsGrid').innerHTML = '';
            document.getElementById('grantCount').textContent = '';
            setStatus('No grants matched those keywords. Try different words, or browse all grants with the filters below.');
            return;
        }

        setStatus('');
        state.searchResults = results;
        // Hide manual filters while showing search results to avoid confusion
        document.getElementById('grantFilters').style.display = 'none';
        document.getElementById('grantFiltersHeading').style.display = 'none';
        document.getElementById('finderResultsHeader').style.display = 'flex';
        renderGrid();
        document.getElementById('finderResultsHeader').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function init() {
        var grid = document.getElementById('grantsGrid');
        if (!grid) { return; }

        fetch('data/grants.json', { cache: 'no-cache' })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                state.grants = Array.isArray(data) ? data : [];
                buildFilters();
                renderGrid();
            })
            .catch(function () {
                document.getElementById('grantCount').textContent = '';
                document.getElementById('grantEmpty').style.display = '';
                document.getElementById('grantEmpty').textContent =
                    'Could not load the grant list. Please refresh the page.';
            });

        document.getElementById('finderBtn').addEventListener('click', runSearch);
        document.getElementById('finderInput').addEventListener('keydown', function (e) {
            // Cmd/Ctrl + Enter submits
            if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') { runSearch(); }
        });
        document.getElementById('clearSearch').addEventListener('click', function () {
            document.getElementById('finderInput').value = '';
            setStatus('');
            clearSearchResults();
            renderGrid();
        });
        document.querySelectorAll('.example-chip').forEach(function (chip) {
            chip.addEventListener('click', function () {
                document.getElementById('finderInput').value = chip.getAttribute('data-query') || chip.textContent;
                runSearch();
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
