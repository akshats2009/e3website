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
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function renderArticleCard(article) {
    const card = document.createElement('div');
    card.className = 'article-card fade-up clickable-card';
    
    // Safely create image element
    if (article.image) {
      const mediaDiv = document.createElement('div');
      mediaDiv.className = 'card-media';
      const img = document.createElement('img');
      img.src = article.image;
      img.alt = article.imageAlt || article.title;
      img.loading = 'lazy';
      mediaDiv.appendChild(img);
      card.appendChild(mediaDiv);
    }
    
    // Safely create content
    const contentDiv = document.createElement('div');
    contentDiv.className = 'article-content';
    
    const dateP = document.createElement('p');
    dateP.className = 'article-date';
    dateP.textContent = article.date;
    
    const titleH3 = document.createElement('h3');
    titleH3.textContent = article.title;
    
    const summaryP = document.createElement('p');
    summaryP.textContent = article.summary;
    
    const readMoreLink = document.createElement('a');
    readMoreLink.href = article.link;
    readMoreLink.className = 'read-more';
    readMoreLink.textContent = 'Read more →';
    
    contentDiv.appendChild(dateP);
    contentDiv.appendChild(titleH3);
    contentDiv.appendChild(summaryP);
    contentDiv.appendChild(readMoreLink);
    
    card.appendChild(contentDiv);
    
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
    const gridStatus = document.getElementById('articlesStatus');
    
    if (gridContainer) {
      const type = gridContainer.getAttribute('data-type') || 'all';
      const articles = window.articlesData || [];
      const filtered = type === 'all' ? articles : articles.filter(a => a.type === type);
      
      if (filtered.length > 0) {
        filtered.forEach(article => {
          gridContainer.appendChild(renderArticleCard(article));
        });
        // Clear any loading/status text now that we have content
        if (gridStatus) gridStatus.textContent = '';
      } else {
        gridContainer.innerHTML = '<p style="color: rgba(245,240,235,0.5);">No articles available yet.</p>';
        if (gridStatus) gridStatus.textContent = 'No articles available yet.';
      }
    }
    
    // Trigger fade-up animations
    setTimeout(observeFadeUps, 100);
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      loadArticles();
      observeFadeUps();
    });
  } else {
    loadArticles();
    observeFadeUps();
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