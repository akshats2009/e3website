// Quick hide for leftover loading text (temporary)
(function(){
  try {
    var s = document.createElement('style');
    s.id = 'quick-hide-loading';
    s.textContent = "[data-loading], .loading, .site-loading, .loading-indicator, .loading-text, #loading { display: none !important; visibility: hidden !important; }";
    document.head && document.head.appendChild(s);
  } catch(e) { /* ignore */ }
})();

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