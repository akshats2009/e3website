// Quick hide for leftover loading text (temporary)
(function(){
  try {
    var s = document.createElement('style');
    s.id = 'quick-hide-loading';
    s.textContent = "[data-loading], .loading, .site-loading, .loading-indicator, .loading-text, #loading { display: none !important; visibility: hidden !important; }";
    document.head && document.head.appendChild(s);
  } catch(e) { /* ignore */ }
})();

// Article loading and rendering
(function() {
  function renderArticleCard(article) {
    const card = document.createElement('div');
    card.className = 'article-card fade-up clickable-card';
    
    const image = article.image ? `<div class="card-media"><img src="${article.image}" alt="${article.imageAlt || article.title}" loading="lazy"></div>` : '';
    
    card.innerHTML = `
      ${image}
      <div class="article-content">
        <p class="article-date">${article.date}</p>
        <h3>${article.title}</h3>
        <p>${article.summary}</p>
        <a href="${article.link}" class="read-more" style="color: #8b5cf6;">Read more →</a>
      </div>
    `;
    
    // Make card clickable
    card.addEventListener('click', function(e) {
      if (!e.target.closest('a')) {
        window.location.href = article.link;
      }
    });
    
    return card;
  }

  function loadArticles() {
    // Load articles for homepage (latestArticles)
    const latestContainer = document.getElementById('latestArticles');
    const latestStatus = document.getElementById('latestArticlesStatus');
    
    if (latestContainer) {
      const type = latestContainer.getAttribute('data-type') || 'all';
      const articles = window.articlesData || [];
      // For homepage, show all recent publications (both research and articles)
      const filtered = type === 'all' ? articles.slice(0, 3) : articles.filter(a => a.type === type).slice(0, 3);
      
      if (filtered.length > 0) {
        filtered.forEach(article => {
          latestContainer.appendChild(renderArticleCard(article));
        });
        if (latestStatus) latestStatus.textContent = '';
      } else {
        if (latestStatus) latestStatus.textContent = 'No articles available yet.';
      }
    }
    
    // Load articles for dedicated pages (articlesGrid)
    const gridContainer = document.getElementById('articlesGrid');
    
    if (gridContainer) {
      const type = gridContainer.getAttribute('data-type') || 'all';
      const articles = window.articlesData || [];
      const filtered = type === 'all' ? articles : articles.filter(a => a.type === type);
      
      if (filtered.length > 0) {
        filtered.forEach(article => {
          gridContainer.appendChild(renderArticleCard(article));
        });
      } else {
        gridContainer.innerHTML = '<p style="color: rgba(245,240,235,0.5);">No articles available yet.</p>';
      }
    }
    
    // Trigger fade-up animations
    setTimeout(observeFadeUps, 100);
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadArticles);
  } else {
    loadArticles();
  }
})();

// Fade-up animation observer
function observeFadeUps() {
  const elements = document.querySelectorAll('.fade-up');
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });
  
  elements.forEach(el => observer.observe(el));
}

// Initialize fade-ups on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', observeFadeUps);
} else {
  observeFadeUps();
}

// Back to top button functionality
document.addEventListener('click', function(e) {
  if (e.target.closest('.to-top')) {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
});

// Appended: copy-to-clipboard for citations and small UX feedback
(function(){
  function copyText(text){
    if(!navigator.clipboard) return fallbackCopy(text);
    return navigator.clipboard.writeText(text);
  }
  function fallbackCopy(text){
    var ta = document.createElement('textarea');
    ta.value = text; document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch(e){}
    ta.remove();
  }

  document.addEventListener('click', function(e){
    var btn = e.target.closest && e.target.closest('.copy-citation');
    if(!btn) return;
    var id = btn.getAttribute('data-citation-id');
    if(!id) return;
    var node = document.getElementById(id);
    if(!node) return;
    // Build a compact citation text
    var title = node.querySelector('.citation-title')?.textContent?.trim() || '';
    var author = node.querySelector('.citation-author')?.textContent?.trim() || '';
    var details = node.querySelector('.citation-details')?.textContent?.trim() || '';
    var link = node.querySelector('.citation-link')?.href || '';
    var citation = title + (author? (' — ' + author): '') + (details? (', ' + details): '') + (link? (' — ' + link): '');
    copyText(citation).then?.(function(){
      var prev = btn.textContent;
      btn.textContent = 'Copied!';
      btn.disabled = true;
      setTimeout(function(){ btn.textContent = prev; btn.disabled = false; }, 1600);
    }).catch(function(){
      var prev = btn.textContent;
      btn.textContent = 'Copied!';
      setTimeout(function(){ btn.textContent = prev; }, 1600);
    });
  });
})();