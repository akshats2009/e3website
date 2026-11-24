
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const NAMES = [[100, 'Thin'], [200, 'ExtraLight'], [300, 'Light'], [400, 'Regular'], [500, 'Medium'], [600, 'SemiBold'], [700, 'Bold'], [800, 'ExtraBold'], [900, 'Black']];
const nameOf = w => NAMES.reduce((a, b) => Math.abs(b[0] - w) < Math.abs(a[0] - w) ? b : a)[1];
$('.menu-btn')?.addEventListener('click', () => { const n = $('.nav ul'); n.classList.toggle('open'); $('.menu-btn').setAttribute('aria-expanded', n.classList.contains('open')); });

/* Springs: each letter eases to its target weight, each a touch softer than the last, so weight travels */
const springs = new Set(); let lastT = performance.now();
function tick(now) { const dt = Math.min(.033, (now - lastT) / 1000); lastT = now;
  springs.forEach(L => L.step(dt)); requestAnimationFrame(tick); }
requestAnimationFrame(tick);
function letters(el, base) {
  const text = el.textContent; el.setAttribute('aria-label', text); el.textContent = '';
  const ls = [];
  text.split(/(\s+)/).forEach(part => { if (/^\s+$/.test(part)) { el.appendChild(document.createTextNode(' ')); return; }
    const w = document.createElement('span'); w.className = 'wd'; w.setAttribute('aria-hidden', 'true');
    [...part].forEach(ch => { const s = document.createElement('span'); s.className = 'lt'; s.textContent = ch; w.appendChild(s); ls.push({ el: s, w: base, v: 0, y: 0, vy: 0, t: base, ty: 0, k: 190 - Math.min(ls.length, 10) * 12, c: 20 - Math.min(ls.length, 10) * .5 }); });
    el.appendChild(w); });
  const L = { ls, base, step(dt) { ls.forEach(l => { if (reduce) { l.w = l.t; l.y = l.ty; } else { l.v += ((l.t - l.w) * l.k - l.v * l.c) * dt; l.w += l.v * dt; l.vy += ((l.ty - l.y) * 260 - l.vy * 22) * dt; l.y += l.vy * dt; }
      const w = Math.max(100, Math.min(900, l.w)); l.el.style.fontVariationSettings = `'wght' ${w.toFixed(0)}, 'SOFT' ${((w - 100) / 8).toFixed(0)}, 'WONK' 1`; l.el.style.transform = `translateY(${l.y.toFixed(2)}px)`; }); } };
  springs.add(L); return L;
}
/* Lens: letters under the pointer go to 900 and lift; neighbours fall off on a bell curve */
function lens(el, base = +(el.dataset.lens || 200), lo = 160) {
  const L = letters(el, base), fs = () => parseFloat(getComputedStyle(el).fontSize), rd = el.closest('.ph')?.querySelector('.rd');
  const say = w => { if (!rd) return; const f = fs(); rd.textContent = `Fraunces ${Math.round(f)}px / ${Math.round(f * .75)}pt · opsz ${Math.min(144, Math.max(9, Math.round(f)))} · wght ${Math.round(w)} · SOFT ${Math.round((w - 100) / 8)}`; };
  say(base); addEventListener('resize', () => say(L.base));
  el.addEventListener('pointermove', e => { if (e.pointerType === 'touch') return; const f = fs();
    L.ls.forEach(l => { const r = l.el.getBoundingClientRect(), dx = (r.left + r.width / 2 - e.clientX) / (f * .55), dy = (r.top + r.height / 2 - e.clientY) / (f * .9), k = Math.exp(-(dx * dx + dy * dy) * 1.4);
      l.t = lo + (900 - lo) * k; l.ty = -f * .045 * k; }); say(Math.max(...L.ls.map(l => l.t))); });
  el.addEventListener('pointerleave', () => { L.ls.forEach(l => { l.t = L.base; l.ty = 0; }); say(L.base); });
  L.setBase = w => { L.base = w; L.ls.forEach(l => { l.t = w; }); };
  return L;
}
Promise.all([document.fonts.load('400 40px Fraunces'), document.fonts.load('400 20px Newsreader'), document.fonts.load('400 12px "Geist Mono"')]).then(() => $$('[data-lens]').forEach(el => { const L = lens(el); el._lens = L;
  if (!reduce) { L.ls.forEach(l => { l.w = 100; }); } }));

/* Weight slider: makeSlider(root, value, onChange) */
function makeSlider(root, w, onChange) {
  const trk = $('.trk', root), knob = $('.knob', root), fill = $('.fill', root), tip = $('.tip', root);
  NAMES.forEach(([v]) => { const t = document.createElement('div'); t.className = 'tk'; t.dataset.w = v; root.appendChild(t);
    if (v % 200 === 100) { const l = document.createElement('div'); l.className = 'tkl'; l.dataset.w = v; l.textContent = v; root.appendChild(l); } });
  const xOf = v => (v - 100) / 800 * trk.clientWidth;
  function set(v, quiet) { w = Math.max(100, Math.min(900, v)); const x = xOf(w);
    $$('.tk,.tkl', root).forEach(t => t.style.left = xOf(+t.dataset.w) + 'px'); knob.style.left = tip.style.left = x + 'px'; fill.style.width = x + 'px';
    $('[data-n]', tip).textContent = nameOf(w); $('[data-v]', tip).textContent = Math.round(w); knob.setAttribute('aria-valuenow', Math.round(w)); if (!quiet) onChange?.(w); }
  const fromX = cx => { const r = trk.getBoundingClientRect(); return 100 + 800 * Math.max(0, Math.min(1, (cx - r.left) / r.width)); };
  knob.addEventListener('pointerdown', e => { knob.setPointerCapture(e.pointerId); knob.classList.add('drag'); root.dataset.touched = 1; });
  knob.addEventListener('pointermove', e => { if (knob.classList.contains('drag')) set(fromX(e.clientX)); });
  knob.addEventListener('pointerup', () => knob.classList.remove('drag'));
  trk.addEventListener('pointerdown', e => { root.dataset.touched = 1; set(fromX(e.clientX)); });
  knob.addEventListener('keydown', e => { if (['ArrowRight', 'ArrowUp'].includes(e.key)) { e.preventDefault(); set(w + 100); } if (['ArrowLeft', 'ArrowDown'].includes(e.key)) { e.preventDefault(); set(w - 100); } root.dataset.touched = 1; });
  addEventListener('resize', () => set(w, true)); set(w, true); return { set, get: () => w };
}
function sliderHTML(label, ro = '') { return `<div class="sl">${label}</div>${ro ? `<div class="lab ro">${ro}</div>` : ''}<div class="trk"><div class="fill"></div></div><div class="knob" tabindex="0" role="slider" aria-label="${label}" aria-valuemin="100" aria-valuemax="900"></div><div class="tip"><span data-n>Thin</span><span data-v>100</span></div>`; }
$$('.slider[data-label]').forEach(s => s.innerHTML = sliderHTML(s.dataset.label, s.dataset.ro || ''));
/* urgency → weight: 0 days 900, 60+ days 150 */
const urg = d => d == null ? 400 : Math.round(800 - 400 * Math.min(1, Math.max(0, d) / 60));
