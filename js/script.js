// Contact Form Handling
document.addEventListener('DOMContentLoaded', function() {
    // No JS needed for header animation; handled by CSS
    const contactForm = document.getElementById('contactForm');
    const contactStatus = document.getElementById('contactStatus');
    const newsletterForm = document.getElementById('newsletterForm');
    const newsletterStatus = document.getElementById('newsletterStatus');
    const articlesGrid = document.getElementById('articlesGrid');
    const latestArticles = document.getElementById('latestArticles');
    const articlesStatus = document.getElementById('articlesStatus');
    const latestArticlesStatus = document.getElementById('latestArticlesStatus');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;

            if (contactStatus) contactStatus.textContent = 'Sending your message…';

            fetch('/api/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, subject, message })
            })
                .then((response) => {
                    if (!response.ok) throw new Error('Request failed');
                    return response.json();
                })
                .then(() => {
                    if (contactStatus) contactStatus.textContent = 'Thanks! We will respond within two business days.';
                    contactForm.reset();
                })
                .catch(() => {
                    if (contactStatus) contactStatus.textContent = 'Unable to send right now. Please try again later.';
                });
        });
    }

    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = document.getElementById('newsletterEmail').value;
            if (newsletterStatus) newsletterStatus.textContent = 'Adding you to the list…';

            fetch('/api/newsletter', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            })
                .then((response) => {
                    if (!response.ok) throw new Error('Request failed');
                    return response.json();
                })
                .then(() => {
                    if (newsletterStatus) newsletterStatus.textContent = 'You’re subscribed. Welcome!';
                    newsletterForm.reset();
                })
                .catch(() => {
                    if (newsletterStatus) newsletterStatus.textContent = 'Unable to subscribe right now. Please try again later.';
                });
        });
    }

    const formatDate = (value) => {
        if (!value) return '';
        const parsed = new Date(value);
        if (Number.isNaN(parsed.getTime())) return value;
        return parsed.toLocaleDateString(undefined, {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    const shouldOpenNewTab = (url) => {
        if (!url) return false;
        return /^https?:\/\//i.test(url) || url.toLowerCase().endsWith('.pdf');
    };

    // Determine which page we're on so we can filter items by `type`.
    const pageType = (() => {
        const page = window.location.pathname.split('/').pop();
        if (page === 'research.html') return 'research';
        if (page === 'articles.html') return 'article';
        return 'all';
    })();

    const createArticleCard = (article) => {
        const card = document.createElement('div');
        card.className = 'article-card';

        const content = document.createElement('div');
        content.className = 'article-content';

        if (article.image) {
            const media = document.createElement('div');
            media.className = 'card-media';

            const img = document.createElement('img');
            img.src = article.image;
            img.alt = article.imageAlt || article.title || 'Research article';

            media.appendChild(img);
            card.appendChild(media);
        }

        const title = document.createElement('h3');
        title.textContent = article.title || 'Untitled Research';

        const date = document.createElement('p');
        date.className = 'article-date';
        date.textContent = formatDate(article.date);

        const summary = document.createElement('p');
        summary.textContent = article.summary || 'Summary coming soon.';

        const link = document.createElement('a');
        link.className = 'read-more';
        link.href = article.link || '#';
        link.textContent = article.linkText || 'Read More →';
        if (shouldOpenNewTab(link.href)) {
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
        }

        if (article.link && article.link !== '#') {
            card.classList.add('clickable-card');
            card.addEventListener('click', (event) => {
                if (event.target.closest('a')) return;
                if (shouldOpenNewTab(article.link)) {
                    window.open(article.link, '_blank', 'noopener,noreferrer');
                } else {
                    window.location.href = article.link;
                }
            });
        }

        content.appendChild(title);
        if (date.textContent) {
            content.appendChild(date);
        }
        content.appendChild(summary);
        content.appendChild(link);
        card.appendChild(content);

        return card;
    };

    const renderArticles = (container, list, limit) => {
        container.innerHTML = '';
        const items = limit ? list.slice(0, limit) : list;
        items.forEach((article, index) => {
            const card = createArticleCard(article);
            // Add stagger class for sequential animation
            card.classList.add(`stagger-${Math.min(index + 1, 6)}`);
            container.appendChild(card);
            
            // Observe the new card for reveal animation
            if (window.revealObserver) {
                window.revealObserver.observe(card);
            } else {
                // Fallback: add in-view immediately if observer not ready
                setTimeout(() => card.classList.add('in-view'), 100 + (index * 100));
            }
        });
    };

    if (articlesGrid || latestArticles) {
        const normalizeArticles = (items) => (items || []).map((article) => {
            const link = article.link || '';
            // Prefer explicit `type`. Otherwise infer from link path (research/), default to 'article'.
            const inferred = article.type || (/\bresearch\b/i.test(link) || /(^|\/)research\//i.test(link) ? 'research' : 'article');
            return {
                title: article.title,
                date: article.date,
                summary: article.summary || article.excerpt,
                link,
                linkText: article.linkText,
                image: article.image,
                imageAlt: article.imageAlt,
                type: inferred
            };
        });

        const loadArticles = (list) => {
            const articles = normalizeArticles(list);

            const renderForContainer = (container, statusEl, limit) => {
                if (!container) return;
                const ctype = (container.dataset && container.dataset.type) ? container.dataset.type : pageType;
                const filtered = ctype === 'all' ? articles : articles.filter((a) => a.type === ctype);
                const emptyMsg = ctype === 'research' ? 'No research publications yet.' : (ctype === 'article' ? 'No articles yet.' : 'No publications yet.');
                if (statusEl) statusEl.textContent = filtered.length ? '' : emptyMsg;
                renderArticles(container, filtered, limit);
            };

            renderForContainer(articlesGrid, articlesStatus);
            renderForContainer(latestArticles, latestArticlesStatus, 3);
        };

        fetch('/api/articles')
            .then((response) => {
                if (!response.ok) throw new Error('API not available');
                return response.json();
            })
            .then((data) => loadArticles(data))
            .catch(() => {
                if (Array.isArray(window.articlesData)) {
                    loadArticles(window.articlesData);
                } else {
                    fetch('data/articles.json')
                        .then((response) => response.json())
                        .then((data) => {
                            window.articlesData = Array.isArray(data) ? data : [];
                            loadArticles(window.articlesData);
                        })
                        .catch(() => {
                            if (articlesStatus) articlesStatus.textContent = 'Unable to load research articles.';
                            if (latestArticlesStatus) latestArticlesStatus.textContent = 'Unable to load research articles.';
                        });
                }
            });
    }

    // Load a representative hero image from the backend Unsplash proxy
    (function loadHeroFromUnsplash() {
        const hero = document.querySelector('.hero');
        if (!hero) return;

        fetch('/api/unsplash?q=community%20meeting')
            .then((r) => r.json())
            .then((data) => {
                if (data && data.urls && data.urls.full) {
                    // Use a reasonably sized URL (regular) for background
                    hero.style.backgroundImage = `url('${data.urls.regular}')`;
                    hero.setAttribute('data-photo-id', data.id || '');
                    // Optionally set attribution (not visible) for future use
                    if (data.photographer) hero.setAttribute('data-photo-credit', data.photographer);
                }
            })
            .catch(() => {
                // fail silently; keep existing background
            });
    })();

    document.querySelectorAll('.to-top').forEach((button) => {
        button.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });

    // ========================================
    // SCROLL ANIMATIONS SYSTEM
    // ========================================

    // 1. INTERSECTION OBSERVER FOR REVEAL ANIMATIONS
    const revealElements = document.querySelectorAll('.fade-up, .fade-left, .fade-right, .scale-in, .blur-reveal, .text-reveal, .section-divider, .pillar-card, .feature-card, .impact-card, .article-card');
    
    // Make observer global so dynamically added elements can use it
    window.revealObserver = new IntersectionObserver(
        (entries, obs) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                    // Unobserve after animation
                    obs.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );

    revealElements.forEach((el) => window.revealObserver.observe(el));

    // 2. STAGGERED CARD REVEALS
    const cardGroups = document.querySelectorAll('.pillar-grid, .articles-grid, .features-grid');
    cardGroups.forEach((group) => {
        const cards = group.querySelectorAll('.pillar-card, .feature-card, .article-card');
        cards.forEach((card, index) => {
            card.classList.add(`stagger-${Math.min(index + 1, 6)}`);
        });
    });

    // 3. READING PROGRESS BAR
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    document.body.prepend(progressBar);

    // 4. PARALLAX EFFECT FOR ORBS
    let ticking = false;
    
    function updateParallax() {
        const scrollY = window.scrollY;
        const windowHeight = window.innerHeight;
        const docHeight = document.documentElement.scrollHeight;
        
        // Update progress bar
        const scrollPercent = (scrollY / (docHeight - windowHeight)) * 100;
        progressBar.style.width = `${Math.min(scrollPercent, 100)}%`;
        
        // Parallax for body pseudo-elements (via CSS custom property)
        document.body.style.setProperty('--scroll-y', scrollY);
        
        // Parallax elements
        document.querySelectorAll('.parallax-slow').forEach((el) => {
            el.style.transform = `translateY(${scrollY * 0.3}px)`;
        });
        
        document.querySelectorAll('.parallax-fast').forEach((el) => {
            el.style.transform = `translateY(${scrollY * 0.6}px)`;
        });
        
        // 5. SCROLL-TRIGGERED TRANSFORMS
        document.querySelectorAll('.rotate-on-scroll').forEach((el) => {
            const rect = el.getBoundingClientRect();
            const elementCenter = rect.top + rect.height / 2;
            const windowCenter = windowHeight / 2;
            const rotation = (elementCenter - windowCenter) / windowHeight * 10;
            el.style.transform = `rotate(${rotation}deg)`;
        });
        
        document.querySelectorAll('.scale-on-scroll').forEach((el) => {
            const rect = el.getBoundingClientRect();
            const visible = Math.max(0, Math.min(1, 1 - (rect.top / windowHeight)));
            const scale = 0.8 + (visible * 0.2);
            el.style.transform = `scale(${scale})`;
        });
        
        ticking = false;
    }

    // 6. NUMBER COUNTER ANIMATION
    const counters = document.querySelectorAll('.counter');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'), 10);
                const duration = 2000;
                const step = target / (duration / 16);
                let current = 0;
                
                const updateCounter = () => {
                    current += step;
                    if (current < target) {
                        counter.textContent = Math.floor(current).toLocaleString();
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target.toLocaleString();
                    }
                };
                
                updateCounter();
                counterObserver.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach((counter) => counterObserver.observe(counter));

    // 7. HORIZONTAL SCROLL SECTION
    const horizontalWrappers = document.querySelectorAll('.horizontal-scroll-wrapper');
    horizontalWrappers.forEach((wrapper) => {
        const track = wrapper.querySelector('.horizontal-scroll-track');
        if (!track) return;
        
        const horizontalObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    wrapper.dataset.active = 'true';
                } else {
                    wrapper.dataset.active = 'false';
                }
            });
        }, { threshold: 0 });
        
        horizontalObserver.observe(wrapper);
    });

    // Scroll event listener
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
        
        // Horizontal scroll
        horizontalWrappers.forEach((wrapper) => {
            if (wrapper.dataset.active !== 'true') return;
            const track = wrapper.querySelector('.horizontal-scroll-track');
            if (!track) return;
            
            const rect = wrapper.getBoundingClientRect();
            const progress = Math.max(0, Math.min(1, -rect.top / (rect.height - window.innerHeight)));
            const maxScroll = track.scrollWidth - wrapper.clientWidth;
            track.style.transform = `translateX(-${progress * maxScroll}px)`;
        });
    }, { passive: true });

    // 8. SECTION BACKGROUND COLOR SHIFT
    const colorSections = document.querySelectorAll('.color-shift-section');
    const colorObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const color = entry.target.dataset.bgColor;
                if (color) {
                    document.body.style.setProperty('--section-bg', color);
                }
            }
        });
    }, { threshold: 0.5 });
    
    colorSections.forEach((section) => colorObserver.observe(section));

    // 9. TEXT REVEAL - Wrap each word in span
    document.querySelectorAll('.text-reveal').forEach((el) => {
        const text = el.textContent;
        el.innerHTML = `<span>${text}</span>`;
    });

    // Initial parallax update
    updateParallax();
});

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// All custom cursor JS removed. Only native pointer with SVG glow remains.
