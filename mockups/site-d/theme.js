
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const SVG = 'http://www.w3.org/2000/svg';
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const out = t => 1 - Math.pow(1 - t, 3), inOut = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
function countUp(el, to, dur = 1200, fmt = v => Math.round(v)) {
  if (!el) return; if (reduce) { el.textContent = fmt(to); return; }
  const t0 = performance.now(); (function s(n) { const k = Math.min(1, (n - t0) / dur); el.textContent = fmt(to * out(k)); if (k < 1) requestAnimationFrame(s); })(t0);
}
/* Reading mode: saved, applied before paint by the inline head script */
function setNight(on) { document.documentElement.classList.toggle('night', on); localStorage.setItem('e3-night', on ? '1' : '0');
  $$('[data-night-state]').forEach(e => e.textContent = on ? 'On' : 'Off'); $$('[data-night-cap]').forEach(e => e.textContent = on ? 'Ink on dark, for evenings' : 'Paper, for daytime');
  $$('[role=switch][data-night]').forEach(e => e.setAttribute('aria-checked', on)); }
$$('[data-night]').forEach(b => b.addEventListener('click', () => setNight(!document.documentElement.classList.contains('night'))));
setNight(document.documentElement.classList.contains('night'));
$('.menu-btn')?.addEventListener('click', () => { const n = $('.pill-nav'); n.classList.toggle('open'); $('.menu-btn').setAttribute('aria-expanded', n.classList.contains('open')); });
/* tiles rise in, in turn */
$$('.rise').forEach((t, i) => setTimeout(() => t.classList.add('in'), 80 + Math.min(i, 10) * 70));
/* dials: 60 ticks, lit up to data-lit */
function buildDial(svg, lit, delay = 600) {
  const ticks = [];
  for (let i = 0; i < 60; i++) { const a = i / 60 * Math.PI * 2 - Math.PI / 2, r2 = i % 5 ? 96 : 99, l = document.createElementNS(SVG, 'line');
    l.setAttribute('x1', 100 + Math.cos(a) * 86); l.setAttribute('y1', 100 + Math.sin(a) * 86); l.setAttribute('x2', 100 + Math.cos(a) * r2); l.setAttribute('y2', 100 + Math.sin(a) * r2);
    l.setAttribute('stroke-width', i % 5 ? 1.4 : 2); l.style.opacity = reduce ? 1 : 0; svg.appendChild(l); ticks.push(l); }
  const set = n => ticks.forEach((l, i) => l.classList.toggle('lit', i < n));
  if (reduce) set(lit); else ticks.forEach((l, i) => setTimeout(() => { l.style.transition = 'opacity .3s, stroke .25s'; l.style.opacity = 1; l.classList.toggle('lit', i < lit); }, delay + i * 12));
  return set;
}
$$('svg.dial[data-lit]').forEach(s => buildDial(s, +s.dataset.lit));
/* level bars fill */
$$('.lvl').forEach((l, i) => setTimeout(() => { const b = $('.bar b', l); b.style.width = b.dataset.w + '%'; countUp($('.pc', l), +b.dataset.w, 1000, v => Math.round(v) + '%'); }, 500 + i * 120));
$$('[data-count]').forEach(e => setTimeout(() => countUp(e, +e.dataset.count, 1200), 400));

(function () {
  const ws = document.querySelectorAll('#sky .w');
  if (!ws.length) return;
  ws.forEach(w => { if (Math.random() < .55) w.classList.add('on'); });
  const rm = matchMedia('(prefers-reduced-motion:reduce)').matches;
  if (!rm) {
    setInterval(() => { for (let i = 0; i < 4; i++) { const w = ws[Math.floor(Math.random() * ws.length)]; w.classList.toggle('on'); } }, 500);
    const t = document.getElementById('train'); let x = -60, last = performance.now();
    (function loop(now) { const dt = (now - last) / 1000; last = now; const W = t.parentNode.offsetWidth; x += dt * 90; if (x > W + 60) x = -60; t.style.left = x + 'px'; requestAnimationFrame(loop); })(last);
  }
})();
