/* ----------------------------------------------------------
   Grant database — relevance search, browse, and filter
   Loads data/grants.json and builds a small in-browser search index.
   Results are ranked by relevance (BM25 over name, funder, category,
   description, and notes). Partial words and small typos still match,
   matched words are highlighted, and the filters narrow the results.
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

    // Common words ignored by the search
    var STOPWORDS = [
        'a', 'an', 'and', 'are', 'at', 'be', 'by', 'do', 'for', 'from', 'have', 'i',
        'in', 'is', 'it', 'me', 'my', 'need', 'of', 'on', 'or', 'our', 'run', 'that',
        'the', 'this', 'to', 'want', 'we', 'with'
    ];

    // Searchable fields and how much a match in each one counts
    var FIELDS = [
        { weight: 3, value: function (g) { return g.name; } },
        { weight: 2, value: function (g) { return g.funder; } },
        { weight: 2, value: function (g) { return CATEGORY_LABELS[g.category] || g.category; } },
        { weight: 1, value: function (g) { return ELIGIBILITY_LABELS[g.eligibility]; } },
        { weight: 1, value: function (g) { return g.description; } },
        { weight: 1, value: function (g) { return g.notes; } }
    ];

    // BM25 ranking constants
    var K1 = 1.2;
    var B = 0.75;

    // Funding-amount buckets for the filter (label -> [min, max])
    var AMOUNT_BUCKETS = [
        { value: '', label: 'Any amount' },
        { value: '0-10000', label: 'Up to $10K', min: 0, max: 10000 },
        { value: '10000-50000', label: '$10K – $50K', min: 10000, max: 50000 },
        { value: '50000-100000', label: '$50K – $100K', min: 50000, max: 100000 },
        { value: '100000-', label: '$100K+', min: 100000, max: Infinity }
    ];

    var state = { grants: [], index: null, query: '', words: [], results: null };

    function esc(s) {
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    function escapeRe(s) {
        return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function formatDeadline(g) {
        if (g.deadline === 'rolling') return 'Rolling / ongoing';
        if (g.deadline === 'annual') return 'Recurs annually';
        // ISO date -> readable
        var d = new Date(g.deadline + 'T00:00:00Z');
        if (isNaN(d.getTime())) return g.deadline;
        return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' });
    }

    // Wrap each query word in <mark>, escaping everything else
    function highlight(text, words) {
        var s = String(text || '');
        if (!words.length) return esc(s);
        var re = new RegExp('(' + words.map(escapeRe).join('|') + ')', 'gi');
        return s.split(re).map(function (part, i) {
            return i % 2 ? '<mark>' + esc(part) + '</mark>' : esc(part);
        }).join('');
    }

    function buildCard(g, words) {
        var card = document.createElement('article');
        card.className = 'grant-card';

        var tags =
            '<span class="grant-tag status-' + esc(g.status) + '">' + esc(STATUS_LABELS[g.status] || g.status) + '</span>' +
            '<span class="grant-tag">' + esc(ELIGIBILITY_LABELS[g.eligibility] || g.eligibility) + '</span>' +
            '<span class="grant-tag">' + esc(CATEGORY_LABELS[g.category] || g.category) + '</span>';

        card.innerHTML =
            '<p class="grant-funder">' + esc(g.funder) + '</p>' +
            '<h3>' + highlight(g.name, words) + '</h3>' +
            '<div class="grant-tags">' + tags + '</div>' +
            '<p class="grant-desc">' + highlight(g.description, words) + '</p>' +
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
        var headerEl = document.getElementById('finderResultsHeader');
        var titleEl = document.getElementById('resultsTitle');

        var f = currentFilters();
        var base = state.query ? state.results : state.grants;
        var list = base.filter(function (g) { return passesFilters(g, f); });

        headerEl.style.display = state.query ? 'flex' : 'none';
        titleEl.textContent = 'Results for "' + state.query + '"';

        grid.innerHTML = '';

        if (list.length === 0) {
            countEl.textContent = '';
            emptyEl.textContent = state.query
                ? 'No grants match "' + state.query + '" with these filters. Try different words or widen the filters.'
                : 'No grants match these filters. Try widening them.';
            emptyEl.style.display = '';
            return;
        }
        emptyEl.style.display = 'none';
        countEl.textContent = list.length + (list.length === 1 ? ' grant' : ' grants') +
            (state.query ? ' found' : ' shown');

        list.forEach(function (g) { grid.appendChild(buildCard(g, state.words)); });
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
            document.getElementById(id).addEventListener('change', renderGrid);
        });
    }

    // ---------- Search ----------

    // Light suffix stripping so "bakeries", "funding", and "funded" share a root with
    // "bakery", "fund", and "fund". Applied the same way to queries and to the index.
    function stem(w) {
        if (w.length > 4 && /ies$/.test(w)) return w.slice(0, -3) + 'y';
        if (w.length > 4 && /(s|x|ch|sh)es$/.test(w)) return w.slice(0, -2);
        if (w.length > 5 && /ing$/.test(w)) return w.slice(0, -3);
        if (w.length > 4 && /ed$/.test(w)) return w.slice(0, -2);
        if (w.length > 3 && /s$/.test(w) && !/ss$/.test(w)) return w.slice(0, -1);
        return w;
    }

    // Lowercase words without stopwords, before stemming (used for highlighting)
    function rawWords(text) {
        var words = String(text || '').toLowerCase().split(/[^a-z0-9]+/).filter(function (t) {
            return t.length > 1 && STOPWORDS.indexOf(t) === -1;
        });
        return words.filter(function (w, i) { return words.indexOf(w) === i; });
    }

    function tokenize(text) {
        return rawWords(text).map(stem);
    }

    function levenshtein(a, b) {
        var prev = [];
        var j;
        for (j = 0; j <= b.length; j++) { prev[j] = j; }
        for (var i = 1; i <= a.length; i++) {
            var cur = [i];
            for (j = 1; j <= b.length; j++) {
                cur[j] = Math.min(
                    prev[j] + 1,
                    cur[j - 1] + 1,
                    prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)
                );
            }
            prev = cur;
        }
        return prev[b.length];
    }

    function buildIndex(grants) {
        var postings = {};
        var docLen = [];
        var total = 0;

        grants.forEach(function (g, i) {
            var len = 0;
            FIELDS.forEach(function (field) {
                tokenize(field.value(g)).forEach(function (t) {
                    postings[t] = postings[t] || {};
                    postings[t][i] = (postings[t][i] || 0) + field.weight;
                    len += field.weight;
                });
            });
            docLen[i] = len;
            total += len;
        });

        var df = {};
        Object.keys(postings).forEach(function (t) { df[t] = Object.keys(postings[t]).length; });

        return {
            postings: postings,
            df: df,
            terms: Object.keys(postings),
            docLen: docLen,
            avgLen: grants.length ? total / grants.length : 1,
            N: grants.length
        };
    }

    // Index terms that count for a query word: exact (full weight), prefix (for
    // search-as-you-type), and close spellings (for typos).
    function expandTerm(index, qt) {
        var out = [];
        index.terms.forEach(function (t) {
            if (t === qt) {
                out.push({ term: t, mult: 1 });
            } else if (qt.length >= 3 && t.indexOf(qt) === 0) {
                out.push({ term: t, mult: 0.6 });
            } else if (qt.length >= 5 && Math.abs(t.length - qt.length) <= 2 &&
                       levenshtein(t, qt) <= (qt.length >= 9 ? 2 : 1)) {
                out.push({ term: t, mult: 0.5 });
            }
        });
        return out;
    }

    function bm25(index, term, i) {
        var tf = index.postings[term][i];
        var df = index.df[term];
        var idf = Math.log(1 + (index.N - df + 0.5) / (df + 0.5));
        var norm = 1 - B + B * (index.docLen[i] / index.avgLen);
        return idf * (tf * (K1 + 1)) / (tf + K1 * norm);
    }

    function search(index, grants, query) {
        var qTokens = tokenize(query).filter(function (t, i, all) { return all.indexOf(t) === i; });
        var scores = {};

        qTokens.forEach(function (qt) {
            expandTerm(index, qt).forEach(function (m) {
                Object.keys(index.postings[m.term]).forEach(function (k) {
                    var i = Number(k);
                    scores[i] = (scores[i] || 0) + m.mult * bm25(index, m.term, i);
                });
            });
        });

        return Object.keys(scores)
            .map(function (k) { return { grant: grants[Number(k)], score: scores[k] }; })
            .sort(function (a, b) {
                return (b.score - a.score) || a.grant.name.localeCompare(b.grant.name);
            })
            .map(function (r) { return r.grant; });
    }

    function runSearch() {
        if (!state.index) { return; }
        var q = document.getElementById('finderInput').value.trim();
        state.query = q;
        state.words = rawWords(q);
        state.results = q ? search(state.index, state.grants, q) : null;
        renderGrid();
    }

    function init() {
        var grid = document.getElementById('grantsGrid');
        if (!grid) { return; }

        fetch('data/grants.json', { cache: 'no-cache' })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                state.grants = Array.isArray(data) ? data : [];
                state.index = buildIndex(state.grants);
                buildFilters();
                renderGrid();
                runSearch();
            })
            .catch(function () {
                document.getElementById('grantCount').textContent = '';
                document.getElementById('grantEmpty').style.display = '';
                document.getElementById('grantEmpty').textContent =
                    'Could not load the grant list. Please refresh the page.';
            });

        var input = document.getElementById('finderInput');
        var timer = null;
        input.addEventListener('input', function () {
            // Search as you type, after a short pause
            clearTimeout(timer);
            timer = setTimeout(runSearch, 150);
        });
        input.addEventListener('keydown', function (e) {
            // Enter searches; Shift+Enter adds a new line
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                clearTimeout(timer);
                runSearch();
            }
        });
        document.getElementById('finderBtn').addEventListener('click', runSearch);
        document.getElementById('clearSearch').addEventListener('click', function () {
            input.value = '';
            runSearch();
        });
        document.querySelectorAll('.example-chip').forEach(function (chip) {
            chip.addEventListener('click', function () {
                input.value = chip.getAttribute('data-query') || chip.textContent;
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
