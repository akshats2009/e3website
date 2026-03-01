// e3 Initiative site script
(function () {
  'use strict';

  function formatDate(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return iso;
    return d.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
  }

  function setStatus(el, message) {
    if (!el) return;
    el.textContent = message || '';
    el.style.display = message ? '' : 'none';
  }

  function renderArticles({ containerId, statusId, type, limit }) {
    const grid = document.getElementById(containerId);
    const status = document.getElementById(statusId);
    if (!grid) return;

    const data = (window.articlesData || []).filter((item) => {
      if (!type || type === 'all') return true;
      return item.type === type;
    });

    const items = typeof limit === 'number' ? data.slice(0, limit) : data;

    if (!items.length) {
      setStatus(status, type === 'article' ? 'No articles available yet.' : 'No publications available yet.');
      grid.innerHTML = '';
      return;
    }

    setStatus(status, '');

    grid.innerHTML = items
      .map((item) => {
        const date = formatDate(item.date);
        const img = item.image
          ? `<div class="card-media"><img src="${item.image}" alt="${item.imageAlt || item.title}" loading="lazy"></div>`
          : '';

        return `
          <article class="article-card clickable-card" data-href="${item.link}">
            ${img}
            <div class="article-content">
              <p class="article-date">${date}</p>
              <h3>${item.title}</h3>
              <p>${item.summary || ''}</p>
              <a class="read-more" href="${item.link}">Read more →</a>
            </div>
          </article>
        `;
      })
      .join('');

    grid.querySelectorAll('[data-href]').forEach((card) => {
      card.addEventListener('click', (e) => {
        const link = card.getAttribute('data-href');
        if (!link) return;
        // Don't hijack clicks on actual links
        if (e.target && e.target.closest && e.target.closest('a')) return;
        window.location.href = link;
      });
    });
  }

  function initToTop() {
    const btn = document.querySelector('.to-top');
    if (!btn) return;
    btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  function initScrollReveals() {
    const els = document.querySelectorAll('.fade-up');
    if (!els.length) return;

    const obs = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add('in-view');
        });
      },
      { threshold: 0.15 }
    );

    els.forEach((el) => obs.observe(el));
  }

  document.addEventListener('DOMContentLoaded', () => {
    initToTop();
    initScrollReveals();

    // Articles page
    renderArticles({ containerId: 'articlesGrid', statusId: 'articlesStatus', type: 'article' });

    // Home page
    renderArticles({ containerId: 'latestArticles', statusId: 'latestArticlesStatus', type: 'all', limit: 3 });

    // Research page (no grid right now). If you later add one, we can render research items.
    // For now, we only ensure the page doesn't show an "articles" empty-state.
    const researchStatus = document.getElementById('researchStatus');
    if (researchStatus) {
      // If you want a dynamic empty-state, you can set it here.
      // Leaving it blank because the page itself contains the description text.
      setStatus(researchStatus, '');
    }
  });
})();