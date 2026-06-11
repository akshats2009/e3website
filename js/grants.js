/* ----------------------------------------------------------
   Grant database — browse, filter, and AI-powered matching
   Loads data/grants.json, renders a filterable grid, and calls
   /api/grant-finder for natural-language search. The grid works fully
   without the AI endpoint; AI search is a progressive enhancement.
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

    // Funding-amount buckets for the filter (label -> [min, max])
    var AMOUNT_BUCKETS = [
        { value: '', label: 'Any amount' },
        { value: '0-10000', label: 'Up to $10K', min: 0, max: 10000 },
        { value: '10000-50000', label: '$10K – $50K', min: 10000, max: 50000 },
        { value: '50000-100000', label: '$50K – $100K', min: 50000, max: 100000 },
        { value: '100000-', label: '$100K+', min: 100000, max: Infinity }
    ];

    var state = { grants: [], aiMatches: null };

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

        var reason = g.reason
            ? '<div class="grant-reason"><strong>Why it fits</strong>' + esc(g.reason) + '</div>'
            : '';

        card.innerHTML =
            '<p class="grant-funder">' + esc(g.funder) + '</p>' +
            '<h3>' + esc(g.name) + '</h3>' +
            '<div class="grant-tags">' + tags + '</div>' +
            reason +
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
        if (state.aiMatches) {
            // AI mode: show only the matched grants, in ranked order (no client filtering)
            list = state.aiMatches;
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
            (state.aiMatches ? ' matched' : ' shown');

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
                // Changing a filter exits AI-results mode
                clearAiResults();
                renderGrid();
            });
        });
    }

    function setStatus(msg) {
        document.getElementById('finderStatus').textContent = msg || '';
    }

    function clearAiResults() {
        state.aiMatches = null;
        document.getElementById('finderResultsHeader').style.display = 'none';
        document.getElementById('grantFiltersHeading').style.display = '';
        document.getElementById('grantFilters').style.display = '';
    }

    function runAiSearch() {
        var input = document.getElementById('finderInput');
        var query = input.value.trim();
        if (!query) { input.focus(); return; }

        var btn = document.getElementById('finderBtn');
        btn.disabled = true;
        setStatus('Searching grants for the best fit…');

        fetch('/api/grant-finder', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        })
            .then(function (r) {
                return r.json().then(function (data) { return { ok: r.ok, data: data }; });
            })
            .then(function (res) {
                btn.disabled = false;
                if (!res.ok) {
                    // 503 (not configured) or other error -> fall back to filters
                    setStatus(res.data && res.data.error ? res.data.error : 'Search unavailable — use the filters below.');
                    return;
                }
                var matches = (res.data && res.data.matches) || [];
                if (matches.length === 0) {
                    setStatus('No strong matches found. Try rephrasing, or browse all grants with the filters below.');
                    return;
                }
                setStatus('');
                state.aiMatches = matches;
                // Hide manual filters while showing AI results to avoid confusion
                document.getElementById('grantFilters').style.display = 'none';
                document.getElementById('grantFiltersHeading').style.display = 'none';
                document.getElementById('finderResultsHeader').style.display = 'flex';
                renderGrid();
                document.getElementById('finderResultsHeader').scrollIntoView({ behavior: 'smooth', block: 'start' });
            })
            .catch(function () {
                btn.disabled = false;
                setStatus('Could not reach the AI search. Browse the grants with the filters below.');
            });
    }

    function init() {
        var grid = document.getElementById('grantsGrid');
        if (!grid) { return; }

        fetch('data/grants.json')
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

        document.getElementById('finderBtn').addEventListener('click', runAiSearch);
        document.getElementById('finderInput').addEventListener('keydown', function (e) {
            // Cmd/Ctrl + Enter submits
            if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') { runAiSearch(); }
        });
        document.getElementById('clearSearch').addEventListener('click', function () {
            document.getElementById('finderInput').value = '';
            setStatus('');
            clearAiResults();
            renderGrid();
        });
        document.querySelectorAll('.example-chip').forEach(function (chip) {
            chip.addEventListener('click', function () {
                document.getElementById('finderInput').value = chip.getAttribute('data-query') || chip.textContent;
                runAiSearch();
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
