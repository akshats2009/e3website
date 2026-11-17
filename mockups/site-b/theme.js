
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
$('.menu-btn')?.addEventListener('click', () => { const n = $('.nav ul'); n.classList.toggle('open'); $('.menu-btn').setAttribute('aria-expanded', n.classList.contains('open')); });
/* Stepped knob: 270° sweep, one detent per label. makeKnob(el, labels, start, onChange) */
function makeKnob(el, labels, idx, onChange) {
  const small = el.classList.contains('sm'), S = small ? 100 : 140, C = S / 2, R = small ? 44 : 62, DR = small ? 58 : 84;
  const START = -135, SWEEP = labels.length > 1 ? 270 / (labels.length - 1) : 0;
  const pol = (a, r) => { const t = (a - 90) * Math.PI / 180; return [C + r * Math.cos(t), C + r * Math.sin(t)]; };
  const arc = (a0, a1) => { const p0 = pol(a0, R), p1 = pol(a1, R); return `M${p0[0]} ${p0[1]} A${R} ${R} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${p1[0]} ${p1[1]}`; };
  el.innerHTML = `<svg width="${S}" height="${S}" viewBox="0 0 ${S} ${S}"><path class="tr" d="${arc(START, -START)}"/><path class="pg"/></svg><div class="kbody" tabindex="0" role="slider" aria-label="${el.dataset.label || 'Knob'}"></div><div class="kcap"></div><div class="kptr"></div>`;
  const dets = labels.map((l, i) => { const [x, y] = pol(START + i * SWEEP, DR), d = document.createElement('div'); d.className = 'det'; d.style.left = x + 'px'; d.style.top = y + 'px'; d.textContent = l; d.style.cursor = 'pointer'; d.onclick = () => set(i); el.appendChild(d); return d; });
  const body = $('.kbody', el);
  function set(i, quiet) { idx = Math.max(0, Math.min(labels.length - 1, i)); const a = START + idx * SWEEP;
    body.style.transform = $('.kptr', el).style.transform = `rotate(${a}deg)`; $('.pg', el).setAttribute('d', idx ? arc(START, a) : 'M0 0');
    dets.forEach((d, j) => d.classList.toggle('on', j === idx)); body.setAttribute('aria-valuetext', labels[idx]); if (!quiet) onChange?.(idx); }
  let drag = false;
  body.addEventListener('pointerdown', e => { body.setPointerCapture(e.pointerId); drag = true; });
  body.addEventListener('pointermove', e => { if (!drag) return; const r = el.getBoundingClientRect(); let a = Math.atan2(e.clientX - (r.left + C), -(e.clientY - (r.top + C))) * 180 / Math.PI;
    a = Math.max(START, Math.min(-START, a)); const i = Math.round((a - START) / (SWEEP || 1)); if (i !== idx) set(i); });
  body.addEventListener('pointerup', () => drag = false);
  body.addEventListener('keydown', e => { if (['ArrowRight', 'ArrowUp'].includes(e.key)) { e.preventDefault(); set(idx + 1); } if (['ArrowLeft', 'ArrowDown'].includes(e.key)) { e.preventDefault(); set(idx - 1); } });
  set(idx, true); return { set, get: () => idx };
}
/* Fader: value 0..1, onChange(p) */
function makeFader(el, p, onChange) {
  const cap = $('.fcap', el), fill = $('.fill', el);
  function set(v, quiet) { p = Math.max(0, Math.min(1, v)); cap.style.top = (1 - p) * 100 + '%'; fill.style.height = p * 100 + '%'; if (!quiet) onChange?.(p); }
  const from = y => { const r = $('.trk', el).getBoundingClientRect(); return 1 - (y - r.top) / r.height; };
  cap.addEventListener('pointerdown', e => { cap.setPointerCapture(e.pointerId); cap.classList.add('drag'); set(from(e.clientY)); });
  cap.addEventListener('pointermove', e => { if (cap.classList.contains('drag')) set(from(e.clientY)); });
  cap.addEventListener('pointerup', () => cap.classList.remove('drag'));
  cap.addEventListener('keydown', e => { if (e.key === 'ArrowUp') { e.preventDefault(); set(p + .05); } if (e.key === 'ArrowDown') { e.preventDefault(); set(p - .05); } });
  set(p, true); return { set, get: () => p };
}
/* key groups: data-group, data-multi */
$$('.keys[data-group]').forEach(g => g.addEventListener('click', e => { const k = e.target.closest('.key'); if (!k) return;
  if (g.hasAttribute('data-multi')) k.classList.toggle('on'); else $$('.key', g).forEach(x => x.classList.toggle('on', x === k));
  g.dispatchEvent(new CustomEvent('change')); }));
/* LED meters fill in */
$$('.meter[data-n]').forEach((m, j) => { const n = +m.dataset.n, lit = +m.dataset.lit, near = +(m.dataset.near || 0);
  m.innerHTML = Array.from({ length: n }, () => '<i></i>').join('');
  [...m.children].forEach((c, i) => setTimeout(() => { if (i < lit) c.className = i >= lit - near ? 'near' : 'on'; }, reduce ? 0 : 300 + j * 60 + i * 35)); });
$$('.knob[data-labels]').forEach(k => makeKnob(k, k.dataset.labels.split('|'), +(k.dataset.idx || 0)));
