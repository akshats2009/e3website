"""Variation C: Type specimen. Warm grained paper, Fraunces (opsz/wght/SOFT/WONK) for display, Newsreader (opsz/wght) for text, Geist Mono labels, orange type guides.
Weight carries meaning everywhere: page titles are live specimens with a weight lens, urgent deadlines are heavier,
finished checklist steps gain weight, reading an article gives its title weight. Built from weight-axis."""
import json
from common import *

D = "site-c"

CSS = r"""
:root{
  --page:#ebe7df; --paper-light:#f6f3ee; --ink:#141312; --guide:#ff5a2a; --guide-rgb:255 90 42;
  --label-ink:rgba(20,19,18,.42); --soft:rgba(20,19,18,.58); --track:rgba(20,19,18,.1); --tick:rgba(20,19,18,.22); --rule:rgba(20,19,18,.12); --wash:rgba(20,19,18,.04);
  --display:"Fraunces","Iowan Old Style",Georgia,serif; --text:"Newsreader","Iowan Old Style",Georgia,serif; --sans:var(--text); --mono:"Geist Mono",ui-monospace,monospace;
  --grain:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5  0 0 0 0 .45  0 0 0 0 .4  0 0 0 .35 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html{background:var(--page)}
body{font-family:var(--sans);color:var(--ink);-webkit-font-smoothing:antialiased;background:radial-gradient(1300px 900px at 50% 320px,var(--paper-light),var(--page)) no-repeat;font-variation-settings:'wght' 400}
body::after{content:"";position:fixed;inset:0;background-image:var(--grain);background-size:220px;opacity:.35;mix-blend-mode:multiply;pointer-events:none;z-index:50}
a{color:inherit;text-decoration:none}
button,input,textarea{font:inherit;color:inherit;font-variation-settings:inherit}
button{background:none;border:0;cursor:pointer}
img{display:block;max-width:100%}
.wrap{max-width:1180px;margin:0 auto;padding:0 40px}
.skip{position:absolute;left:-999px;top:8px;z-index:99;background:var(--ink);color:var(--paper-light);padding:8px 12px;border-radius:8px}
.skip:focus{left:12px}
:focus-visible{outline:1.5px dashed var(--guide);outline-offset:4px}
.lab{font-family:var(--mono);font-size:12.5px;color:var(--label-ink);font-variation-settings:normal}
.g{color:var(--guide)}
.w1{font-variation-settings:'wght' 100}.w2{font-variation-settings:'wght' 200}.w3{font-variation-settings:'wght' 300}.w5{font-variation-settings:'wght' 500}.w6{font-variation-settings:'wght' 600}.w7{font-variation-settings:'wght' 700}.w8{font-variation-settings:'wght' 800}.w9{font-variation-settings:'wght' 900}

.nav{display:flex;justify-content:space-between;align-items:center;height:78px;border-bottom:1px solid var(--rule);gap:20px}
.brand{font-size:17px;font-variation-settings:'wght' 650;letter-spacing:-.02em}
.brand span{font-variation-settings:'wght' 200}
.nav ul{display:flex;gap:26px;list-style:none}
.nav ul a{font-size:14px;color:var(--soft);font-variation-settings:'wght' 380;transition:font-variation-settings .3s,color .3s}
.nav ul a:hover,.nav ul a.on{color:var(--ink);font-variation-settings:'wght' 650}
.nav ul a.on{text-decoration:underline dashed var(--guide);text-underline-offset:8px;text-decoration-thickness:1px}
.menu-btn{display:none;font:13px var(--mono);padding:8px 12px;border-radius:8px;box-shadow:inset 0 0 0 1px var(--rule)}

/* specimen titles: letters are spans, the lens sets each one's weight */
[data-lens]{cursor:default}
[data-lens] .wd{display:inline-block;white-space:nowrap}
[data-lens] .lt{display:inline-block;transform-origin:50% 80%}
.ph{padding:56px 0 40px;border-bottom:1px dashed rgb(var(--guide-rgb)/.45);position:relative}
.ph .top{display:flex;justify-content:space-between;gap:20px;margin-bottom:26px}
.ph h1{font-size:96px;line-height:.95;letter-spacing:-.045em;font-weight:normal;font-variation-settings:'wght' 200;max-width:14ch}
.ph h1.long{font-size:60px;max-width:22ch}
.ph .lede{display:grid;grid-template-columns:1fr 1fr;gap:56px;margin-top:34px;align-items:end}
.ph .lede p{font-size:16px;line-height:1.6;color:var(--soft);max-width:48ch}
.ph .baseguide{position:absolute;left:0;right:0;border-top:1px dashed var(--guide);opacity:0;transition:opacity .3s;pointer-events:none}
.ph .baseguide span{position:absolute;right:0;top:-18px;font:11px var(--mono);color:var(--guide)}
.ph:hover .baseguide{opacity:.7}

.pill{height:46px;padding:0 20px;display:inline-flex;align-items:center;gap:10px;border-radius:10px;background:var(--ink);color:var(--paper-light);font:14px var(--mono);transition:transform .15s;white-space:nowrap}
.pill:active{transform:scale(.97)}
.pill.o{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px rgba(20,19,18,.2)}
.pill.sm{height:34px;padding:0 13px;font-size:12px}
.btns{display:flex;gap:10px;flex-wrap:wrap}

section{margin-top:110px}
.sh{display:flex;justify-content:space-between;align-items:baseline;padding-bottom:16px;border-bottom:1px solid var(--ink);gap:20px}
.sh h2{font-size:48px;letter-spacing:-.04em;line-height:1;font-weight:normal;font-variation-settings:'wght' 300}
.sh a{font:13px var(--mono);color:var(--soft)}.sh a:hover{color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:28px}
.c3{grid-column:span 3}.c4{grid-column:span 4}.c5{grid-column:span 5}.c6{grid-column:span 6}.c7{grid-column:span 7}.c8{grid-column:span 8}.c12{grid-column:span 12}
.rule{border-top:1px solid var(--rule)}
summary{list-style:none}summary::-webkit-details-marker{display:none}
[hidden]{display:none!important}

/* index rows: numeral + title that gains weight on hover */
.pub{display:grid;grid-template-columns:90px 1fr 220px;gap:32px;padding:34px 0;border-bottom:1px solid var(--rule);position:relative;align-items:start}
.pub .no{font-size:64px;line-height:.8;letter-spacing:-.05em;font-variation-settings:'wght' 100;color:var(--label-ink);transition:font-variation-settings .5s,color .3s}
.pub h3{font-size:32px;line-height:1.1;letter-spacing:-.035em;font-weight:normal;font-variation-settings:'wght' 300;transition:font-variation-settings .5s cubic-bezier(.2,1,.3,1)}
.pub p{font-size:14px;color:var(--soft);line-height:1.55;margin-top:10px;max-width:60ch}
.pub .meta{font:12px/1.9 var(--mono);color:var(--label-ink)}
.pub .meta b{font-weight:normal;color:var(--ink)}
.pub.jr{grid-template-columns:260px 1fr}
.pub img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:6px;filter:grayscale(1) sepia(.15);margin-bottom:12px}
.pub:hover h3{font-variation-settings:'wght' 620}
.pub:hover .no{font-variation-settings:'wght' 900;color:var(--ink)}
.pub::after{content:"";position:absolute;left:122px;right:252px;bottom:20px;border-top:1px dashed var(--guide);opacity:0;transition:opacity .3s}
.pub:hover::after{opacity:.8}

/* grants table: weight = urgency */
.gt{width:100%;border-collapse:collapse}
.gt th{font:12px var(--mono);color:var(--label-ink);text-align:left;font-weight:normal;padding:14px 0;border-bottom:1px solid var(--rule)}
.gt td{padding:18px 12px 18px 0;border-bottom:1px solid var(--rule);vertical-align:baseline}
.gt .n{font-size:18px;letter-spacing:-.02em;font-variation-settings:'wght' 420;line-height:1.3}
.gt .f{font-size:13px;color:var(--soft);margin-top:3px}
.gt .a{font:14px var(--mono);white-space:nowrap}
.gt .c{font:12px var(--mono);color:var(--label-ink)}
.gt .d{font-size:28px;letter-spacing:-.03em;text-align:right;white-space:nowrap;padding-right:0}
.gt .d small{display:block;font:11.5px var(--mono);color:var(--label-ink);letter-spacing:0;margin-top:3px}
.gt tr.hot .d{color:var(--guide)}
.gt tr.closed .n,.gt tr.closed .d{color:var(--label-ink)}
.gt tbody tr{transition:background .2s;cursor:pointer}
.gt tbody tr:hover{background:rgb(var(--guide-rgb)/.05)}
.gt tr.xr td{padding-top:0;color:var(--soft);font-size:14px;line-height:1.6;cursor:default}
.legend{display:flex;align-items:center;gap:14px;margin:22px 0 4px;flex-wrap:wrap}
.legend .ramp{display:flex;gap:10px;font-size:20px;color:var(--ink)}

/* slider (weight axis) */
.slider{position:relative;width:600px;max-width:100%;height:70px;margin:70px auto 0}
.slider .sl{position:absolute;left:0;top:-48px;font-size:14px;color:var(--soft)}
.slider .ro{position:absolute;right:0;top:-48px}
.trk{position:absolute;left:0;right:0;top:0;height:4px;border-radius:2px;background:var(--track);cursor:pointer}
.trk .fill{position:absolute;left:0;top:0;height:4px;border-radius:2px;background:var(--ink)}
.tk{position:absolute;top:20px;width:2px;height:8px;border-radius:1px;background:var(--tick);margin-left:-1px}
.tkl{position:absolute;top:36px;font:12px var(--mono);color:rgba(20,19,18,.36);transform:translateX(-50%)}
.knob{position:absolute;top:-14px;width:32px;height:32px;margin-left:-16px;border-radius:50%;background:#fff;cursor:grab;touch-action:none;box-shadow:0 0 0 1px rgba(20,19,18,.1),0 6px 14px -4px rgba(20,19,18,.35),inset 0 -2px 0 rgba(20,19,18,.06)}
.knob.drag{transform:scale(1.12);cursor:grabbing}
.tip{position:absolute;top:-62px;height:36px;padding:0 12px;border-radius:10px;background:var(--ink);color:var(--paper-light);display:flex;align-items:center;gap:8px;font:14px var(--mono);white-space:nowrap;transform:translateX(-50%);pointer-events:none}
.tip::after{content:"";position:absolute;left:50%;bottom:-4px;width:8px;height:8px;margin-left:-4px;background:var(--ink);transform:rotate(45deg);border-radius:2px}
.tip span:last-child{opacity:.55}
.mini.slider{width:100%;margin:56px 0 10px;height:52px}
.mini .tkl,.mini .sl{display:none}

/* home specimen */
.spec{position:relative;padding:44px 0 30px;user-select:none}
.tabs{display:flex;gap:6px}
.tabs button{font:13px var(--mono);color:var(--label-ink);padding:6px 10px;border-radius:8px;transition:background .2s,color .2s}
.tabs button.on{background:var(--ink);color:var(--paper-light)}
.band{position:relative;height:300px;margin-top:20px}
.guides{position:absolute;inset:0;pointer-events:none;overflow:visible}
.guides line{stroke:var(--guide)}.guides text{font:12px var(--mono);fill:var(--guide)}
.word{position:absolute;inset:0;display:flex;justify-content:center;align-items:center;white-space:nowrap;letter-spacing:-.04em;line-height:1}
.word span{display:inline-block;transform-origin:50% 80%}
.lede2{display:grid;grid-template-columns:1.1fr 1fr;gap:56px;align-items:end;padding:70px 0 0;border-top:1px dashed rgb(var(--guide-rgb)/.45);margin-top:50px}
.lede2 h1{font-size:62px;line-height:1;letter-spacing:-.045em;font-weight:normal;font-variation-settings:'wght' 250}
.lede2 p{font-size:16px;line-height:1.6;color:var(--soft);max-width:46ch;margin-bottom:26px}

/* three lenses */
.lenses{display:grid;grid-template-columns:repeat(3,1fr);border-bottom:1px solid var(--rule)}
.ln{position:relative;padding:28px 28px 34px 0}
.ln + .ln{padding-left:28px;border-left:1px solid var(--rule)}
.glyph{position:relative;height:210px;margin:6px 0 18px}
.glyph .e{position:absolute;left:0;bottom:22px;font-size:220px;line-height:.72;letter-spacing:-.04em}
.glyph .gl{position:absolute;left:-6px;right:0;border-top:1px dashed var(--guide);opacity:.6}
.glyph .gl span{position:absolute;right:0;top:-16px;font:11px var(--mono);color:var(--guide)}
.ln h3{font-size:30px;letter-spacing:-.03em;font-weight:normal}
.ln p{color:var(--soft);font-size:14px;line-height:1.55;margin-top:6px;max-width:32ch}

/* prose */
.read{display:grid;grid-template-columns:200px 1fr 200px;gap:40px;align-items:start;margin-top:40px}
.margin{position:sticky;top:24px;font:12px/1.8 var(--mono);color:var(--label-ink)}
.margin a{display:block;transition:color .2s,font-variation-settings .2s}
.margin a.on{color:var(--guide)}
.prose{font-size:18.5px;line-height:1.72;font-variation-settings:'wght' var(--bw,380);max-width:64ch}
.prose p{margin:0 0 1.2em}
.prose > p:first-of-type::first-letter{float:left;font-size:5.4em;line-height:.82;margin:.06em .1em 0 0;font-variation-settings:'wght' 800;letter-spacing:-.04em}
.prose h2{font-size:34px;line-height:1.08;letter-spacing:-.035em;font-weight:normal;font-variation-settings:'wght' 300;margin:1.7em 0 .6em;scroll-margin-top:24px;position:relative}
.prose h2::before{content:attr(data-n);position:absolute;right:calc(100% + 18px);top:.5em;font:12px var(--mono);color:var(--guide)}
.prose h3{font:13px var(--mono);color:var(--ink);margin:2em 0 .6em}
.prose ul{margin:0 0 1.2em 1.1em}.prose li{margin:0 0 .5em}
.prose a{text-decoration:underline dashed var(--guide);text-underline-offset:4px}
.prose strong,.prose b{font-weight:normal;font-variation-settings:'wght' 700}
.banner{margin:30px 0 8px}
.banner img{width:100%;max-height:480px;object-fit:cover;border-radius:6px;filter:grayscale(1) sepia(.15)}
.capt{font:12px var(--mono);color:var(--label-ink)}

/* form */
.field{display:block;margin-bottom:26px}
.field .fl{font:12.5px var(--mono);color:var(--label-ink);transition:color .2s}
.field:focus-within .fl{color:var(--guide)}
.inp{width:100%;border:0;border-bottom:1px solid var(--ink);background:transparent;padding:10px 0;font-size:28px;letter-spacing:-.02em;font-variation-settings:'wght' 250;outline:none;transition:font-variation-settings .3s,border-color .2s;border-radius:0}
.inp:focus{font-variation-settings:'wght' 500;border-bottom:1px dashed var(--guide)}
textarea.inp{font-size:20px;line-height:1.5;min-height:160px;resize:vertical}
.inp::placeholder{color:rgba(20,19,18,.25)}

/* tabs as filters */
.ftabs{display:flex;flex-wrap:wrap;gap:4px 20px}
.ftabs button{font:13px var(--mono);color:var(--label-ink);padding:6px 0;border-bottom:1px solid transparent;transition:color .2s,border-color .2s}
.ftabs button.on{color:var(--ink);border-bottom:1px dashed var(--guide)}
.fgroup{display:grid;grid-template-columns:150px 1fr;gap:20px;padding:14px 0;border-top:1px solid var(--rule);align-items:baseline}
.bigsearch{width:100%;border:0;background:transparent;font-size:64px;letter-spacing:-.045em;font-variation-settings:'wght' 200;outline:none;padding:6px 0 12px;border-bottom:1px dashed var(--guide)}
.bigsearch::placeholder{color:rgba(20,19,18,.2)}

/* checklist */
.tip-row{display:grid;grid-template-columns:70px 1fr 40px;gap:24px;padding:26px 0;border-bottom:1px solid var(--rule);text-align:left;width:100%;align-items:start}
.tip-row .no{font-size:44px;line-height:.85;letter-spacing:-.05em;font-variation-settings:'wght' 100;color:var(--label-ink);transition:font-variation-settings .5s,color .3s}
.tip-row b{display:block;font-weight:normal;font-size:24px;letter-spacing:-.03em;line-height:1.15;font-variation-settings:'wght' 250;transition:font-variation-settings .5s cubic-bezier(.2,1,.3,1)}
.tip-row p{color:var(--soft);font-size:14.5px;line-height:1.6;margin-top:8px}
.tip-row .bx{width:28px;height:28px;border-radius:50%;box-shadow:inset 0 0 0 1px var(--rule);display:grid;place-items:center;font:12px var(--mono);color:var(--paper-light);transition:background .2s}
.tip-row.on b{font-variation-settings:'wght' 720}
.tip-row.on .no{font-variation-settings:'wght' 900;color:var(--ink)}
.tip-row.on .bx{background:var(--guide);box-shadow:none}

.big-num{font-size:150px;line-height:.8;letter-spacing:-.06em}
.ind{padding:28px 0 30px;border-bottom:1px solid var(--rule);position:relative}
.ind .row1{display:flex;justify-content:space-between;align-items:baseline;gap:20px}
.ind .val{font-size:80px;line-height:.9;letter-spacing:-.05em;transition:font-variation-settings .4s}
.ind .val small{font:13px var(--mono);letter-spacing:0;color:var(--label-ink);margin-left:8px}
.ind svg{display:block;width:100%;height:110px;margin-top:20px;overflow:visible}
.ind svg text{font:11px var(--mono);fill:var(--guide)}
.ind p{font-size:14px;color:var(--soft);line-height:1.55;margin-top:12px;max-width:52ch}
.notice{font:12.5px/1.6 var(--mono);color:var(--guide);padding:14px 0;border-bottom:1px dashed var(--guide);margin-bottom:10px}

footer{margin-top:110px;border-top:1px solid var(--ink);padding:26px 0 50px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px}
footer nav{display:flex;gap:22px;flex-wrap:wrap}
footer a{font:13px var(--mono);color:var(--soft)}footer a:hover{color:var(--ink)}

@media (max-width:1000px){
  .nav ul{display:none}.menu-btn{display:block}
  .nav ul.open{display:flex;flex-direction:column;position:absolute;top:78px;left:20px;right:20px;padding:20px;gap:14px;background:var(--paper-light);border:1px solid var(--rule);border-radius:12px;z-index:30}
  .read{grid-template-columns:1fr}.margin{display:none}.read > aside:last-child{display:none}
  .grid > *{grid-column:span 12}
}
@media (max-width:760px){
  .wrap{padding:0 20px}
  .ph h1{font-size:58px}.ph h1.long{font-size:36px}.ph .lede,.lede2{grid-template-columns:1fr;gap:20px}.lede2 h1{font-size:44px}
  .band{height:200px}
  .pub{grid-template-columns:1fr;gap:10px}.pub .no{font-size:40px}.pub::after{display:none}.pub h3{font-size:24px}
  .gt .f,.gt .c,.gt th.c{display:none}.gt .d{font-size:20px}.gt .a{font-size:12px}
  .lenses{grid-template-columns:1fr}.ln + .ln{padding-left:0;border-left:0;border-top:1px solid var(--rule)}
  .fgroup{grid-template-columns:1fr;gap:6px}.bigsearch{font-size:38px}
  .slider{width:calc(100% - 64px)}.slider .ro{display:none}.pub.jr{grid-template-columns:1fr}
  .big-num{font-size:100px}.ind .val{font-size:56px}
  .tip-row{grid-template-columns:44px 1fr 32px;gap:14px}.tip-row .no{font-size:32px}
  .prose{font-size:17px}.prose h2::before{display:none}
  .sh h2{font-size:36px}
  .pub.jr{grid-template-columns:1fr!important}.grid{column-gap:0!important}.pub > *{min-width:0}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

JS = r"""
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
const urg = d => d == null ? 300 : Math.round(900 - 750 * Math.min(1, Math.max(0, d) / 60));
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,100..900,0..100,0..1;1,9..144,100..900,0..100,0..1&family=Newsreader:ital,opsz,wght@0,6..72,200..800;1,6..72,200..800&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">'


MODE_HEAD = "<script>try{if(localStorage.getItem('e3-mode-c')==='dark')document.documentElement.classList.add('dark')}catch(e){}</script>"
MODE_JS = "<script>(function(){var r=document.documentElement;document.querySelectorAll('[data-mode]').forEach(function(b){b.setAttribute('aria-pressed',r.classList.contains('dark'));b.onclick=function(){var on=r.classList.toggle('dark');try{localStorage.setItem('e3-mode-c',on?'dark':'light')}catch(e){}document.querySelectorAll('[data-mode]').forEach(function(x){x.setAttribute('aria-pressed',on)})}})})();</script>"
MODE_CSS = '.nav-end{display:flex;align-items:center;gap:10px}.mode{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;flex:none;background:color-mix(in srgb,var(--ink) 8%,transparent);color:var(--ink);transition:background .2s}.mode:hover{background:color-mix(in srgb,var(--ink) 14%,transparent)}.mode svg{grid-area:1/1}\n.mode .sun{display:none}html.dark .mode .sun{display:block}html.dark .mode .moon{display:none}\nhtml.dark{--page:#10100f;--paper-light:#1b1a18;--ink:#f2efe8;--label-ink:rgba(242,239,232,.45);--soft:rgba(242,239,232,.62);--track:rgba(242,239,232,.12);--tick:rgba(242,239,232,.26);--rule:rgba(242,239,232,.12);--wash:rgba(242,239,232,.05)}\nhtml.dark body::after{mix-blend-mode:screen;opacity:.1}\nhtml.dark .tkl{color:rgba(242,239,232,.4)}\nhtml.dark .inp::placeholder,html.dark .bigsearch::placeholder{color:rgba(242,239,232,.25)}\nhtml.dark .pill.o{background:rgba(242,239,232,.09);color:var(--ink)}\nhtml.dark .inp{background:rgba(242,239,232,.06)}html.dark .inp:focus{background:rgba(242,239,232,.1)}\nhtml.dark .menu-btn{background:rgba(242,239,232,.08)}\nhtml.dark .knob{background:#f2efe8}\n'
MODE_BTN = '<button class="mode" data-mode aria-label="Toggle dark mode" aria-pressed="false"><svg class="sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg><svg class="moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/></svg></button>'


def typo(html):
    """Typographic quotes, dashes and ellipses on text nodes only."""
    def fix(t):
        t = t.replace("...", "…").replace(" -- ", "\u2009—\u2009").replace("--", "—")
        t = re.sub(r'(^|[\s(\[—])"', "\\1\u201c", t); t = t.replace('"', "\u201d")
        t = re.sub(r"(^|[\s(\[—\u201c])'", "\\1\u2018", t); t = t.replace("'", "\u2019")
        return t
    return "".join(p if p.startswith("<") else fix(p) for p in re.split(r"(<[^>]+>)", html))


def shell(page, body, scripts=""):
    active = SECTION.get(page, "")
    nav = "".join(f'<li><a href="{h}"{" class=on aria-current=page" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    foot = "".join(f'<a href="{h}">{t}</a>' for h, t in FOOT)
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(TITLES[page])} · e3 Initiative</title>{MODE_HEAD}{FONTS}<link rel="stylesheet" href="theme.css"></head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<div class="wrap">
  <header class="nav"><a class="brand" href="index.html">e3 <span>Initiative</span></a><nav aria-label="Main"><ul id="nav">{nav}</ul></nav><div class="nav-end">{MODE_BTN}<button class="menu-btn" aria-controls="nav" aria-expanded="false">Menu</button></div></header>
  <main id="main">
{body}
  </main>
  <footer><span class="lab">© 2026 e3 Initiative · Fraunces · Newsreader · Geist Mono · scale ×1.25</span><nav aria-label="Footer">{foot}</nav></footer>
</div>
<script src="theme.js"></script>
{MODE_JS}
{scripts}
</body></html>
"""


def ph(kicker, title, lede="", right="", readout="Fraunces · wght 200 · hover for a lens"):
    long = " long" if len(title) > 26 else ""
    return f"""<div class="ph"><div class="top"><span class="lab">{kicker}</span><span class="lab rd">{readout}</span></div>
  <h1 data-lens="200" class="{long.strip()}">{esc(title)}</h1>
  {f'<div class="lede"><p>{lede}</p><div>{right}</div></div>' if lede or right else ''}</div>"""


def urg(d):
    return 300 if d is None else round(900 - 750 * min(1, max(0, d) / 60))


def grant_tr(g):
    d, s = days_left(g), status(g)
    w = urg(d) if s != "closed" else 100
    when = deadline_label(g)
    sub = "closed" if s == "closed" else (f"in {d} days · wght {w}" if d is not None else s)
    return (f'<tr class="{"hot" if d is not None and 0 <= d <= 14 and s != "closed" else ""}{" closed" if s == "closed" else ""}" onclick="window.open(\'{g["link"]}\',\'_blank\')">'
            f'<td><div class="n">{esc(g["name"])}</div><div class="f">{esc(g["funder"])}</div></td><td class="a">{esc(money(g.get("amountMax")))}</td>'
            f'<td class="d" style="font-variation-settings:\'wght\' {w}">{when}<small>{sub}</small></td></tr>')


def pub_row(i, p, img=False):
    return (f'<a class="pub" href="{p["slug"]}.html"><div class="no">0{i+1}</div><div><h3>{esc(p["title"])}</h3><p>{esc(p["summary"])}</p></div>'
            f'<div>{f"<img src={chr(34)}{IMG}{p[chr(105)+chr(109)+chr(103)]}{chr(34)} alt={chr(34)}{chr(34)} loading=lazy>" if img else ""}<div class="meta"><b>{p["kind"]}</b><br>{p["short"]}<br>{p["author"]} · {p["min"]} min</div></div></a>')


LEGEND = '<div class="legend lab">The closer the deadline, the heavier it is set.<span class="ramp"><span class="w9">Aa</span><span class="w5">Aa</span><span class="w1">Aa</span></span><span>today → 60 days</span></div>'


def home():
    soon = sorted(OPEN, key=lambda g: days_left(g) if days_left(g) is not None else 999)[:4]
    body = f"""
<div class="spec">
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="tabs" role="tablist"><button class="on" data-w="Equity">Equity</button><button data-w="Economics">Economics</button><button data-w="Ethnicity">Ethnicity</button></div><div class="lab" id="axis">wght 100</div></div>
  <div class="band" id="band"><svg class="guides" id="guides" aria-hidden="true"></svg><div class="word" id="word"></div></div>
  <div class="slider" id="sl" data-label="Weight" data-ro="hover the word for a lens"></div>
  <div class="lede2">
    <h1>Some contributions get set in <span class="w1">thin</span>. We research to give them their <span class="w8">full weight.</span></h1>
    <div><p>Student-led research on who builds local economies, who gets credit and who gets left out.</p><div class="btns"><a class="pill" href="articles.html">Read the research</a></div></div>
  </div>
</div>
"""
    js = r"""<script>
const band = $('#band'), word = $('#word'), guides = $('#guides'); let L = null, weight = 100, lensX = null, G = {};
function setWord(w) { word.textContent = w; if (L) springs.delete(L); L = letters(word, weight); fit(); }
function fit() { const max = Math.min(232, band.clientHeight * .82); word.style.fontSize = max + 'px';
  L.ls.forEach(l => l.el.style.fontVariationSettings = "'wght' 900"); const sw = L.ls.reduce((s, l) => s + l.el.getBoundingClientRect().width, 0), room = band.clientWidth * .96;
  if (sw > room) word.style.fontSize = max * room / sw + 'px';
  const fs = parseFloat(word.style.fontSize), c = document.createElement('canvas').getContext('2d'); c.font = `400 ${fs}px Fraunces`; const m = c.measureText('H');
  const top = L.ls[0].el.getBoundingClientRect().top - band.getBoundingClientRect().top - L.ls[0].y, base = top + (fs - (m.fontBoundingBoxAscent + m.fontBoundingBoxDescent)) / 2 + m.fontBoundingBoxAscent;
  G = { base, cap: base - m.actualBoundingBoxAscent, x: base - c.measureText('x').actualBoundingBoxAscent }; }
let go = 0;
function frame() { const br = band.getBoundingClientRect(), fs = parseFloat(word.style.fontSize);
  L.ls.forEach(l => { if (lensX !== null) { const r = l.el.getBoundingClientRect(), d = (r.left + r.width / 2 - br.left - lensX) / (fs * .55), k = Math.exp(-d * d * 1.4); l.t = 160 + 740 * k; l.ty = -10 * k; } else { l.t = weight; l.ty = 0; } });
  { const w = Math.round(L.ls[0].w); $('#axis').textContent = (lensX !== null ? 'wght lens' : 'wght ' + w) + ' · opsz ' + Math.min(144, Math.round(parseFloat(word.style.fontSize))) + ' · SOFT ' + Math.round((w - 100) / 8) + ' · ' + Math.round(parseFloat(word.style.fontSize)) + 'px / ' + Math.round(parseFloat(word.style.fontSize) * .75) + 'pt'; }
  go += ((lensX !== null ? 1 : 0) - go) * .15; const W = band.clientWidth, x0 = W * .1, x1 = W * .86;
  const line = (y, t) => `<line x1="${x0}" x2="${x1}" y1="${y}" y2="${y}" stroke-dasharray="3 5" opacity="${.6 * go}"/><text x="${x1 + 6}" y="${y + 4}" opacity="${.8 * go}">${t}</text>`;
  guides.innerHTML = line(G.cap, 'Cap') + line(G.x, 'x') + line(G.base, 'Base') + (lensX !== null ? `<line x1="${lensX}" x2="${lensX}" y1="20" y2="${band.clientHeight - 10}" stroke-width="1.5" opacity="${.8 * go}"/>` : '');
  requestAnimationFrame(frame); }
band.addEventListener('pointermove', e => { if (e.pointerType !== 'touch') { lensX = e.clientX - band.getBoundingClientRect().left; $('#sl').dataset.touched = 1; } });
band.addEventListener('pointerleave', () => lensX = null);
const S = makeSlider($('#sl'), 100, w => weight = w);
$$('.tabs button').forEach(b => b.onclick = () => { $$('.tabs button').forEach(x => x.classList.toggle('on', x === b)); setWord(b.dataset.w); });
document.fonts.load('400 100px Fraunces').then(() => { setWord('Equity'); requestAnimationFrame(frame);
  if (reduce) { S.set(400); return; }
  const t0 = performance.now(), path = [[0, 100], [600, 100], [2200, 900], [3400, 900], [4600, 400]];
  (function step(now) { if ($('#sl').dataset.touched) return; const t = now - t0;
    for (let i = 1; i < path.length; i++) if (t <= path[i][0]) { const [a, wa] = path[i - 1], [b, wb] = path[i], k = (t - a) / (b - a), e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; $('.knob', $('#sl')).classList.toggle('drag', wa !== wb); S.set(wa + (wb - wa) * e); break; }
    if (t < 4600) requestAnimationFrame(step); else $('.knob', $('#sl')).classList.remove('drag'); })(t0); });
addEventListener('resize', () => L && fit());
</script>"""
    return shell("index", body, js)


def pub_list(page, title, lede, items, extra=""):
    """Header, index rows, one line of related links."""
    return shell(page, ph("Publications", title, lede) + "".join(pub_row(i, p, False) for i, p in enumerate(items)))

def article(p):
    a = p["data"]
    secs, body, n = [], [], 0
    for i, (t, txt) in enumerate(a["blocks"]):
        if t == "h2":
            n += 1
            secs.append((f"s{i}", re.sub(r"<[^>]+>", "", txt), n))
            body.append(f'<h2 id="s{i}" data-n="§{n}">{typo(txt)}</h2>')
        elif t == "li":
            body.append(f"<ul><li>{typo(txt)}</li></ul>")
        else:
            body.append(f"<{t}>{typo(txt)}</{t}>")
    cite = {"article-railroad": "articles/chinese-labor-transcontinental-railroad-citations.html", "article-chinatown": "articles/chinatown-citations.html", "research-chinatown": "research/chinatown-solidarity-paper-citations.html"}[p["slug"]]
    body_html = f"""
<div class="ph" style="border-bottom:0;padding-bottom:10px"><div class="top"><span class="lab">{p['kind']} · {p['date']}</span><span class="lab" id="rw">Fraunces · wght 100</span></div>
  <h1 class="long" id="title" style="font-variation-settings:'wght' 100, 'WONK' 1;max-width:24ch">{typo(esc(p['title']))}</h1>
  <div class="lab" style="margin-top:22px">{esc(a['byline'] or 'By ' + p['author'])} · {p['min']} min · <a href="../../{cite}" style="text-decoration:underline dashed var(--guide);text-underline-offset:4px">citations</a></div></div>
<div class="banner"><img src="{IMG}{p['img'].replace('-640', '')}" alt="{esc(p['alt'])}"></div><div class="capt">{esc(a['caption'] or p['alt'])}</div>
<div class="read" style="grid-template-columns:1fr;max-width:none"><article class="prose" id="prose">{''.join(body)}</article></div>"""
    js = """<script>
const pr = $('#prose'), title = $('#title');
function upd() { const r = pr.getBoundingClientRect(), k = Math.max(0, Math.min(1, (innerHeight * .4 - r.top) / r.height)), w = Math.round(100 + k * 600);
  title.style.fontVariationSettings = `'wght' ${w}, 'SOFT' ${Math.round((w - 100) / 6)}, 'WONK' 1`; $('#rw').textContent = 'Fraunces · wght ' + w + ' · reading ' + Math.round(k * 100) + '%';
 }
addEventListener('scroll', upd, { passive: true }); upd();
</script>"""
    return shell(p["slug"], body_html, js)


def about():
    """Header, one statement, three people."""
    team = "".join(f'<div class="pub"><div class="no">0{i+1}</div><div><h3 data-lens="300" style="font-size:var(--s3)">{n}</h3><p style="font-size:15px">{b}</p></div><div class="meta"><b>{r}</b></div></div>' for i, (n, r, b) in enumerate(ABOUT["team"]))
    body = ph("About", "About e3 Initiative", ABOUT["what"]) + f"""
<p class="statement">{ABOUT['who']}</p>
<section style="margin-top:60px">{team}<p class="lab" style="margin-top:28px;line-height:1.7;max-width:80ch">We believe in community voices, cross-sector collaboration, and turning findings into stories of economic resilience.</p></section>"""
    return shell("about", body)

def journals():
    t, logo = JOURNAL
    body = ph("Publications", "Journals", "Browse our academic journals and long-form publications. Each journal entry includes comprehensive analysis and scholarly insights.") + f"""
<div class="pub jr" style="margin-top:30px"><img src="{IMG}{logo}" alt="{esc(t)}" width="260" height="260" style="aspect-ratio:1;filter:none;border-radius:8px">
<div><span class="lab">Journal</span><h3 data-lens="250" style="font-size:var(--s3);margin-top:12px">{t}</h3><p style="font-size:15px">Entries coming soon. New long-form work will appear here first.</p></div></div>"""
    return shell("journals", body)


def grants():
    """Header, the big search, two filter rows (more folded), count + table."""
    cats = "".join(f'<button data-v="{k}">{v}</button>' for k, v in CAT_LABEL.items())
    lists = " · ".join(f'<a href="{s}.html" style="text-decoration:underline dashed var(--guide);text-underline-offset:4px;color:var(--ink)">{CAT_LABEL[c]}</a>' for s, (c, _, _) in CATEGORY_PAGES.items())
    body = ph("Grants", "Grant Finder", f"Set by urgency: the closer a deadline, the heavier it is. Closed grants drop to Thin. Ready-made lists: {lists}.", '<a class="pill o" href="grant-help.html">Help & tips →</a>') + f"""
<div style="margin-top:40px"><label class="lab" for="q">Search</label><input class="bigsearch" id="q" type="search" placeholder="women-owned bakery…" autocomplete="off"></div>
<div style="margin-top:20px">
  <div class="fgroup"><span class="lab">Status</span><div class="ftabs" data-f="status"><button class="on" data-v="live">Open + rolling</button><button data-v="">Everything</button></div></div>
  <details class="fgroup" style="display:block"><summary class="lab" style="cursor:pointer">+ More filters</summary>
    <div class="fgroup" style="margin-top:12px"><span class="lab">Who qualifies</span><div class="ftabs" data-f="elig"><button class="on" data-v="">Anyone</button><button data-v="small_business">Small business</button><button data-v="nonprofit">Nonprofit</button></div></div>
    <div class="fgroup" style="margin-top:12px"><span class="lab">Award up to</span><div class="ftabs" data-f="amt"><button class="on" data-v="0">Any</button><button data-v="10000">$10k+</button><button data-v="50000">$50k+</button><button data-v="250000">$250k+</button></div></div>
    <div class="fgroup"><span class="lab">Category</span><div class="ftabs" data-f="cat" data-multi><button class="on" data-v="">All</button>{cats}</div></div></details>
</div>
<div style="display:flex;align-items:baseline;margin-top:40px;gap:14px"><span class="big-num" id="cnt" style="font-variation-settings:'wght' 200">0</span><span class="lab">of {len(GRANTS)} grants</span></div>
<table class="gt"><thead><tr><th>Grant</th><th>Max award</th><th style="text-align:right">Deadline</th></tr></thead><tbody id="gt" aria-live="polite"></tbody></table>"""
    js = """<script src="../shared/grants-data.js"></script><script>
const F = { q: '', elig: '', status: 'live', amt: 0, cat: new Set() };
$$('.ftabs[data-f]').forEach(t => t.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
  if (t.hasAttribute('data-multi')) { if (!b.dataset.v) { F.cat.clear(); $$('button', t).forEach(x => x.classList.toggle('on', !x.dataset.v)); } else { F.cat.has(b.dataset.v) ? F.cat.delete(b.dataset.v) : F.cat.add(b.dataset.v); b.classList.toggle('on'); $('button[data-v=""]', t).classList.toggle('on', !F.cat.size); } }
  else { $$('button', t).forEach(x => x.classList.toggle('on', x === b)); F[t.dataset.f] = t.dataset.f === 'amt' ? +b.dataset.v : b.dataset.v; } render(); }));
$('#q').addEventListener('input', e => { F.q = e.target.value.toLowerCase(); $('#q').style.fontVariationSettings = `'wght' ${200 + Math.min(500, e.target.value.length * 30)}`; render(); });
function render() {
  const rs = GRANTS.filter(g => (!F.q || (g.name + g.funder + g.desc + CAT_LABEL[g.cat]).toLowerCase().includes(F.q)) && (!F.elig || g.elig === F.elig || g.elig === 'both')
    && (F.status === '' || g.status !== 'closed') && (!F.amt || g.max >= F.amt) && (!F.cat.size || F.cat.has(g.cat)))
    .sort((a, b) => ({ open: 0, rolling: 1, closed: 2 }[a.status] - { open: 0, rolling: 1, closed: 2 }[b.status]) || (a.days ?? 999) - (b.days ?? 999));
  $('#cnt').textContent = rs.length; $('#cnt').style.fontVariationSettings = `'wght' ${Math.round(100 + rs.length / GRANTS.length * 800)}`;
  $('#gt').innerHTML = rs.length ? rs.map((g, i) => { const w = g.status === 'closed' ? 100 : urg(g.days), hot = g.days != null && g.days <= 14 && g.status !== 'closed';
    return `<tr class="${hot ? 'hot' : ''} ${g.status === 'closed' ? 'closed' : ''}" data-i="${i}" tabindex="0"><td><div class="n">${g.name}</div><div class="f">${g.funder}</div></td>
      <td class="a">${g.max ? '$' + g.max.toLocaleString() : 'Varies'}</td><td class="d" style="font-variation-settings:'wght' ${w}">${g.dl}<small>${g.status === 'closed' ? 'closed' : g.days != null ? 'in ' + g.days + ' days' : g.status}</small></td></tr>
      <tr class="xr" hidden><td colspan="3">${g.desc} <a class="pill sm o" href="${g.link}" target="_blank" rel="noopener" style="margin-left:8px">Funder's page →</a></td></tr>`; }).join('')
    : '<tr><td colspan="3" class="lab" style="padding:40px 0">No grants match these filters. Try widening them.</td></tr>'; }
$('#gt').addEventListener('click', e => { const r = e.target.closest('tr[data-i]'); if (r && !e.target.closest('a')) r.nextElementSibling.hidden = !r.nextElementSibling.hidden; });
$('#gt').addEventListener('keydown', e => { if (e.key === 'Enter' && e.target.matches('tr[data-i]')) e.target.nextElementSibling.hidden = !e.target.nextElementSibling.hidden; });
render();
</script>"""
    return shell("grants", body, js)

def category(slug):
    """Header, three numerals, the table, one line of links."""
    cat, title, what = CATEGORY_PAGES[slug]
    intro, gs = category_intro(cat, what)
    gs = sorted(gs, key=lambda g: ({"open": 0, "rolling": 1, "closed": 2}[status(g)], days_left(g) if days_left(g) is not None else 999))
    c = {s: sum(1 for g in gs if status(g) == s) for s in ("open", "rolling", "closed")}
    nums = "".join(f'<div class="c4"><div class="big-num" style="font-variation-settings:{chr(39)}wght{chr(39)} {w};font-size:110px">{n}</div><div class="lab" style="margin-top:12px">{lab}</div></div>' for n, lab, w in [(c["open"], "open now", 800), (c["rolling"], "rolling", 450), (c["closed"], "closed for now", 100)])
    others = " · ".join(f'<a href="{s}.html" style="color:var(--ink)">{CAT_LABEL[v[0]]}</a>' for s, v in CATEGORY_PAGES.items() if s != slug)
    body = ph("Grant list", title, intro) + f"""
<table class="gt" style="margin-top:40px"><thead><tr><th>Grant</th><th>Award</th><th style="text-align:right">Deadline</th></tr></thead><tbody>{''.join(grant_tr(g) for g in gs)}</tbody></table>
<p class="lab" style="margin-top:24px">More lists: {others} · <a href="grants.html" style="color:var(--ink)">Search all {len(GRANTS)}</a></p>"""
    return shell(slug, body)

def grant_help():
    """Header, checklist (mistakes folded in), free-help index, one-line disclaimer."""
    tips = "".join(f'<button class="tip-row" data-i="{i}"><span class="no">0{i+1}</span><div><b>{a}</b><p>{b}</p></div><span class="bx">✓</span></button>' for i, (a, b) in enumerate(HELP["tips"]))
    orgs = "".join(f'<a class="pub" href="{u}" target="_blank" rel="noopener" style="padding:24px 0"><div class="no" style="font-size:44px">{chr(65+i)}</div><div><h3 style="font-size:24px">{n}</h3><p>{d}</p></div><div class="meta"><b>{l} →</b></div></a>' for i, (n, d, l, u) in enumerate(HELP["orgs"]))
    body = ph("Grants", "Grant Help & Tips", HELP["intro"], '<a class="pill" href="grants.html">Search grants →</a>') + f"""
<section style="margin-top:60px"><div class="sh"><h2>How to write a strong application</h2><span class="lab">Ready: <span id="rd" style="font-size:22px;color:var(--ink);font-family:var(--sans);font-variation-settings:'wght' 100">0 of 8</span></span></div>
<p class="lab" style="margin:14px 0 0">Tick a step when it's done: it gains weight.</p>{tips}
<details style="padding:20px 0;border-bottom:1px solid var(--rule)"><summary class="lab" style="cursor:pointer">+ Common mistakes to avoid</summary>{''.join(f'<p style="padding:10px 0;font-size:16px;line-height:1.5"><span class="g lab" style="margin-right:12px">✕</span>{m}</p>' for m in HELP['mistakes'])}</details></section>
<section><details><summary class="sh" style="cursor:pointer"><h2>Where to get free help</h2><span class="lab">+ show</span></summary>{orgs}<p class="lab" style="margin-top:20px;line-height:1.7;max-width:90ch">{HELP['disclaimer']}</p></details></section>"""
    js = """<script>
const done = new Set(JSON.parse(localStorage.getItem('e3-help') || '[]'));
function upd() { $$('.tip-row[data-i]').forEach(c => c.classList.toggle('on', done.has(+c.dataset.i))); $('#rd').textContent = done.size + ' of 8';
  $('#rd').style.fontVariationSettings = `'wght' ${100 + done.size * 100}`; localStorage.setItem('e3-help', JSON.stringify([...done])); }
$$('.tip-row[data-i]').forEach(c => c.addEventListener('click', () => { const i = +c.dataset.i; done.has(i) ? done.delete(i) : done.add(i); upd(); })); upd();
</script>"""
    return shell("grant-help", body, js)

def indicators():
    """Header, four key charts, the rest behind one button."""
    def row(k, grp, name, u, d, extra):
        return f"""<div class="ind c6{extra}" data-key="{k}" data-unit="{u}"><div class="row1"><span class="lab">{grp} · {name}</span><span class="lab" data-yr></span></div>
      <div class="val" style="margin-top:16px;font-variation-settings:'wght' 200"><span data-v>—</span><small>{u}</small></div>
      <svg viewBox="0 0 500 110" preserveAspectRatio="none" aria-hidden="true"></svg><p>{d}</p></div>"""
    key = [i for i in INDICATORS if i[0] in KEY_INDICATORS]
    more = [i for i in INDICATORS if i[0] not in KEY_INDICATORS]
    body = ph("Data", "Economic Indicators", "Everyday costs, job security and borrowing rates since 2000. Each value's weight shows where it sits in its own history: a record high is Black, a record low is Thin.") + f"""
<div class="notice" id="note" hidden>Preview: placeholder shapes. Live FRED data loads from /api/economic-indicators on the deployed site.</div>
<div class="grid" style="gap:0 48px">{''.join(row(*i, '') for i in key)}{''.join(row(*i, ' more') for i in more)}</div>
<div style="margin-top:28px"><button class="pill o" onclick="document.querySelectorAll('.ind.more').forEach(e=>e.hidden=false);this.remove()">Show all 8 indicators</button></div>"""
    js = """<script src="../shared/indicators.js"></script><script>
$$('.ind.more').forEach(e => e.hidden = true);
loadIndicators().then(D => { $('#note').hidden = D.live;
  $$('.ind').forEach(t => { const s = D.series[t.dataset.key]; if (!s) return; const n = s.length, lo = Math.min(...s), hi = Math.max(...s), x = i => i / (n - 1) * 500, y = v => 100 - (v - lo) / (hi - lo || 1) * 90, u = t.dataset.unit, svg = $('svg', t);
    const d = s.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1)).join(' ');
    svg.innerHTML = `<line x1="0" x2="500" y1="${y(hi)}" y2="${y(hi)}" stroke="var(--guide)" stroke-dasharray="3 5" opacity=".6" vector-effect="non-scaling-stroke"/><line x1="0" x2="500" y1="${y(lo)}" y2="${y(lo)}" stroke="var(--guide)" stroke-dasharray="3 5" opacity=".6" vector-effect="non-scaling-stroke"/>
      <path d="${d}" fill="none" stroke="var(--ink)" stroke-width="1.6" vector-effect="non-scaling-stroke" ${D.live ? '' : 'stroke-dasharray="2 4"'}/><line class="cur" y1="0" y2="110" stroke="var(--guide)" stroke-width="1.5" vector-effect="non-scaling-stroke"/>`;
    const show = i => { const k = (s[i] - lo) / (hi - lo || 1), w = Math.round(100 + k * 800); $('.val', t).style.fontVariationSettings = `'wght' ${w}`;
      $('[data-v]', t).textContent = D.live ? fmtIndicator(s[i], u).replace(/[%M]/g, '') : '—'; $('[data-yr]', t).textContent = D.years[i]; $('.cur', svg).setAttribute('x1', x(i)); $('.cur', svg).setAttribute('x2', x(i)); };
    show(n - 1); svg.onpointermove = e => { const r = svg.getBoundingClientRect(); show(Math.round((e.clientX - r.left) / r.width * (n - 1))); }; svg.onpointerleave = () => show(n - 1); }); });
</script>"""
    return shell("economic-indicators", body, js)

def outreach():
    cols = "".join(f'<div class="c6" id="{k}"><span class="lab">0{i+1} · {s}</span><h2 data-lens="250" style="font-size:var(--d2);font-weight:normal;line-height:1;margin:16px 0 24px">{t}</h2><p style="line-height:1.6">{p1}</p><p style="color:var(--soft);font-size:15px;line-height:1.6;margin:16px 0 26px">{p2}</p><a class="pill" href="contact.html">{"Share your story" if k == "interview" else "Partner with us"} →</a></div>' for i, (k, (t, s, p1, p2)) in enumerate(OUTREACH.items()))
    return shell("outreach", ph("Outreach", "Outreach", "Interviews and partnerships: how community knowledge gets into our research.") + f'<div class="grid" style="margin-top:60px;gap:56px">{cols}</div>')


def contact():
    body = ph("Contact", "Let's connect", "Have questions about our research or want to collaborate? Send a message and we will respond within two business days.") + f"""
<div class="grid" style="margin-top:50px"><form class="c8" onsubmit="event.preventDefault();this.querySelector('[data-sent]').hidden=false">
  <div class="grid" style="gap:0 28px"><label class="field c6"><span class="fl">Name *</span><input class="inp" required autocomplete="name" placeholder="Your name"></label><label class="field c6"><span class="fl">Email *</span><input class="inp" type="email" required autocomplete="email" placeholder="you@example.com"></label></div>
  <label class="field"><span class="fl">Subject *</span><input class="inp" required placeholder="What it's about"></label>
  <label class="field"><span class="fl">Message *</span><textarea class="inp" required placeholder="Write as much as you like."></textarea></label>
  <div class="btns" style="align-items:center"><button class="pill" type="submit">Send message →</button><span class="lab g" data-sent hidden>Mockup: nothing was sent</span></div></form>
</div>"""
    return shell("contact", body)


def privacy():
    out, secs, ul, n = [], [], False, 0
    for i, (t, txt) in enumerate(PRIVACY):
        if t == "li":
            if not ul:
                out.append("<ul>"); ul = True
            out.append(f"<li>{typo(txt)}</li>"); continue
        if ul:
            out.append("</ul>"); ul = False
        if t == "h2":
            n += 1; secs.append((f"p{i}", txt, n)); out.append(f'<h2 id="p{i}" data-n="§{n}">{typo(txt)}</h2>')
        else:
            out.append(f"<{t}>{typo(txt)}</{t}>")
    body = ph("Legal · updated Nov 12, 2026", "Privacy Policy", "The e3 Initiative is a small research organization. This page explains what information this website collects, why, and the choices you have.") + f"""
<div class="read" style="grid-template-columns:1fr;max-width:none"><article class="prose" style="--bw:400">{''.join(out)}</article></div>"""
    return shell("privacy", body.replace('<p class="np">', '<p style="">'))


def notfound():
    body = f"""<div class="ph" style="border:0"><div class="top"><span class="lab">Page not found</span><span class="lab">hover the numerals</span></div>
  <h1 data-lens="100" style="font-size:clamp(110px,32vw,300px);letter-spacing:-.06em;line-height:.85">404</h1>
  <div class="lede"><p>Sorry, we couldn't find that page. It may have moved, or the link may be mistyped.</p><div class="btns"><a class="pill" href="index.html">Homepage</a><a class="pill o" href="articles.html">Articles</a><a class="pill o" href="research.html">Research</a><a class="pill o" href="contact.html">Contact</a></div></div></div>"""
    return shell("404", body)


def build():
    write(f"{D}/theme.css", CSS + NOB + MODE_CSS + TYPE)
    write(f"{D}/theme.js", JS)
    pages = {"index": home(), "about": about(), "journals": journals(), "grants": grants(), "grant-help": grant_help(),
             "economic-indicators": indicators(), "outreach": outreach(), "contact": contact(), "privacy": privacy(), "404": notfound(),
             "articles": pub_list("articles", "Publications", "Articles and research papers from our team and partners, from grassroots history to systemic policy analysis.", PUBS),
             "research": pub_list("research", "Research", "Research papers, reports, and briefs, each with clear summaries and next steps for community leaders and decision-makers.", RESEARCH,
                 '<section><div class="sh"><h2>Also in Publications</h2></div><a class="pub" href="journals.html"><div class="no">J</div><div><h3>Critical Debates in Humanities, Science and Global Justice</h3><p>Our journal. Entries coming soon.</p></div><div class="meta"><b>Journals →</b></div></a><a class="pub" href="economic-indicators.html"><div class="no">D</div><div><h3>Economic indicators since 2000</h3><p>Inflation, rates and the labor market, explained.</p></div><div class="meta"><b>Data →</b></div></a></section>')}
    for p in PUBS:
        pages[p["slug"]] = article(p)
    for s in CATEGORY_PAGES:
        pages[s] = category(s)
    for k, v in pages.items():
        write(f"{D}/{k}.html", v)
    return sorted(pages)

# NOBORDERS
NOB = r"""
/* no borders: type and space do the separating */
.nav,footer,.sh,.pub,.ph,.lede2,.lenses,.ind,.fgroup,.tip-row,.gt th,.gt td,.rule{border:0!important}
.ln + .ln{border:0!important}
.ph .baseguide,.pub::after{display:none}
.pill.o{box-shadow:none;background:rgba(20,19,18,.07)}
.inp{border:0!important;background:rgba(20,19,18,.05);padding:14px 16px;border-radius:10px;font-size:22px}
.inp:focus{background:rgba(20,19,18,.08)}
.bigsearch{border:0!important;background:transparent}
.menu-btn{box-shadow:none;background:rgba(20,19,18,.06)}
.nav ul a.on{text-decoration:none;font-variation-settings:'wght' 700}
.fgroup,.tip-row{padding-top:12px}
.knob{box-shadow:0 6px 14px -4px rgba(20,19,18,.3)}
.banner img,.pub img{border-radius:10px}
"""

# TYPE: the typographic system (loaded last, so it wins over the structural CSS above)
TYPE = r"""
/* ── Scale: base fluid 17→20px, ×1.25 (major third); display steps get a vw term ── */
:root{
  --b:clamp(1.0625rem,1rem + .3vw,1.25rem);
  --s-1:calc(var(--b)*.82); --s1:calc(var(--b)*1.25); --s2:calc(var(--b)*1.5625); --s3:calc(var(--b)*1.953); --s4:calc(var(--b)*2.441);
  --d2:clamp(2.6rem,1.4rem + 4.2vw,4.5rem);   /* ≈72px */
  --d1:clamp(2.1rem,1.2rem + 2.6vw,3.25rem);  /* ≈52px */
  --d0:clamp(3.25rem,.9rem + 8.2vw,6.25rem);  /* ≈100px hero */
  --measure:60ch;
}
html{font-optical-sizing:auto;text-rendering:optimizeLegibility;font-kerning:normal;-webkit-text-size-adjust:100%}
body{font-family:var(--text);font-size:var(--b);line-height:1.5;font-variation-settings:normal;font-weight:400;font-feature-settings:"kern","liga","calt"}
h1,h2,h3{text-wrap:balance}
p,li{text-wrap:pretty}

/* display voice: Fraunces */
.brand,.ph h1,.sh h2,.pub .no,.pub h3,.lede2 h1,.glyph .e,.ln h3,.prose h2,.prose>p:first-of-type::first-letter,.bigsearch,.tip-row .no,.tip-row b,.big-num,.ind .val,.gt .d,.word,.legend .ramp,.tabs button.dsp,.statement,.inp,.slider .sl{font-family:var(--display)}
.brand{font-size:var(--s1);letter-spacing:-.01em;font-variation-settings:'wght' 600,'SOFT' 100,'WONK' 1}
.brand span{font-variation-settings:'wght' 200,'SOFT' 0,'WONK' 1;font-style:italic}
.ph h1{font-size:var(--d0);line-height:.98;letter-spacing:-.025em;max-width:13ch;font-variation-settings:'wght' 200,'WONK' 1}
.ph h1.long{font-size:var(--d1);max-width:20ch;line-height:1.02}
.ph .lede p{font-size:var(--s1);line-height:1.5;max-width:44ch;color:var(--soft)}
.sh h2{font-size:var(--d1);letter-spacing:-.02em;line-height:1.02;font-variation-settings:'wght' 300,'WONK' 1}
.pub .no{font-size:var(--d2);letter-spacing:-.03em;line-height:.8;font-variation-settings:'wght' 100;font-variant-numeric:lining-nums}
.pub h3{font-size:var(--s2);letter-spacing:-.015em;line-height:1.12;font-variation-settings:'wght' 300}
.pub:hover h3{font-variation-settings:'wght' 620,'SOFT' 60}
.pub:hover .no{font-variation-settings:'wght' 900,'SOFT' 100}
.pub p{font-size:var(--b);line-height:1.5;max-width:56ch;margin-top:10px}
.pub .meta{font-size:12px;letter-spacing:.02em}
.lede2 h1{font-size:var(--d1);letter-spacing:-.02em;line-height:1.04;font-variation-settings:'wght' 250,'WONK' 1}
.lede2 h1 .w8{font-style:italic;font-variation-settings:'wght' 800,'SOFT' 100,'WONK' 1}
.lede2 h1 .w1{font-variation-settings:'wght' 100,'WONK' 1}
.lede2 p{font-size:var(--s1);line-height:1.5}
.ln h3{font-size:var(--s3);letter-spacing:-.015em;font-variation-settings:'wght' 400}
.ln p{font-size:var(--b)}
.glyph .e{letter-spacing:-.02em}
.statement{font-size:var(--s3);line-height:1.22;letter-spacing:-.012em;font-variation-settings:'wght' 300,'WONK' 1;max-width:34ch;margin-top:50px;text-wrap:balance}
.word{letter-spacing:-.025em}

/* labels: mono, small, tracked; tabular so figures align in specimens */
.lab,.pub .meta,.gt th,.gt .a,.gt .c,.gt .d small,.margin,.field .fl,.ftabs button,.tabs button,.pill,.sh a,footer a,.menu-btn,.notice,.capt,.prose h3,.tip,.tkl{font-family:var(--mono);font-variant-numeric:tabular-nums slashed-zero}
.lab{font-size:12px;letter-spacing:.015em;line-height:1.5}
.lab.rd{font-variant-numeric:tabular-nums;white-space:nowrap;text-align:right}
.gt th{letter-spacing:.06em;text-transform:uppercase;font-size:11px}
.field .fl{text-transform:uppercase;letter-spacing:.06em;font-size:11px}

/* nav */
.nav ul a{font-size:var(--b);font-variation-settings:'wght' 400;letter-spacing:0}
.nav ul a:hover,.nav ul a.on{font-variation-settings:'wght' 700}
.nav ul a.on{font-variation-settings:'wght' 700}

/* tables: Newsreader text, Fraunces figures, tabular + lining */
.gt{font-variant-numeric:tabular-nums lining-nums}
.gt .n{font-size:var(--s1);letter-spacing:-.005em;font-variation-settings:'wght' 500;line-height:1.25;text-wrap:balance}
.gt .f{font-size:var(--s-1);font-style:italic;color:var(--soft);margin-top:4px}
.gt .a{font-size:14px;letter-spacing:0}
.gt .d{font-size:var(--s3);letter-spacing:-.01em;font-variant-numeric:tabular-nums lining-nums;line-height:1.05}
.gt .d small{font-size:11.5px;letter-spacing:.01em}
.gt tr.xr td{font-size:var(--b);line-height:1.55;max-width:60ch}
.big-num{letter-spacing:-.04em;font-variant-numeric:lining-nums}
.ind .val{letter-spacing:-.035em;font-variant-numeric:lining-nums tabular-nums}
.ind p{font-size:var(--b);line-height:1.5}
.legend .ramp{font-size:var(--s2)}

/* forms */
.inp{font-size:var(--s2);letter-spacing:-.005em;font-variation-settings:'wght' 300;line-height:1.25}
.inp:focus{font-variation-settings:'wght' 500,'SOFT' 100}
textarea.inp{font-family:var(--text);font-size:var(--s1);line-height:1.55;font-variation-settings:'wght' 400;letter-spacing:0}
textarea.inp:focus{font-variation-settings:'wght' 460}
.bigsearch{font-size:var(--d2);letter-spacing:-.025em;font-variation-settings:'wght' 200,'WONK' 1}
.inp::placeholder{font-style:italic}
.pill{font-size:13px;letter-spacing:.01em}

/* checklist */
.tip-row .no{font-size:var(--d2);letter-spacing:-.03em;font-variation-settings:'wght' 100}
.tip-row b{font-size:var(--s2);letter-spacing:-.01em;line-height:1.15;font-variation-settings:'wght' 250}
.tip-row.on b{font-variation-settings:'wght' 720,'SOFT' 60}
.tip-row p{font-size:var(--b);line-height:1.5}

/* long-form: ~60ch measure, hanging punctuation, drop cap, small-caps lead-in */
.read{display:block}
.prose{font-family:var(--text);font-size:calc(var(--b)*1.075);line-height:1.58;max-width:var(--measure);margin:0 auto;font-variation-settings:'wght' var(--bw,400);font-feature-settings:"kern","liga","onum","pnum";hanging-punctuation:first allow-end last;hyphens:manual}
.prose p{margin:0 0 1em;text-wrap:pretty}
.prose p + p{margin-top:0}
.prose>p:first-of-type{font-size:calc(var(--b)*1.2);line-height:1.5}
.prose>p:first-of-type::first-line{font-variant-caps:all-small-caps;letter-spacing:.06em}
.prose>p:first-of-type::first-letter{float:left;font-size:5.6em;line-height:.78;margin:.07em .09em 0 0;font-variation-settings:'wght' 800,'SOFT' 100,'WONK' 1;letter-spacing:0;font-variant-caps:normal;color:var(--ink)}
.prose h2{font-size:var(--s3);line-height:1.1;letter-spacing:-.015em;font-variation-settings:'wght' 300,'WONK' 1;margin:2em 0 .55em;max-width:24ch}
.prose h2::before{font-size:11.5px;letter-spacing:.02em}
.prose h3{font-size:12px;letter-spacing:.06em;text-transform:uppercase;margin:2.2em 0 .6em}
.prose ul{margin:0 0 1em 1.2em}.prose li{margin:0 0 .45em}
.prose strong,.prose b{font-variation-settings:'wght' 700}
.prose em,.prose i{font-style:italic}
.prose a{text-decoration-thickness:1px;text-underline-offset:.22em}
.banner + .capt{margin-top:10px}
.capt{font-size:11.5px;letter-spacing:.01em;max-width:var(--measure)}
.margin{font-size:12px}
footer .lab{font-size:11.5px}
footer a{font-size:12px}

html.dark .prose{--bw:430!important}
html.dark .gt .n{font-variation-settings:'wght' 540}
html.dark .ph .lede p,html.dark .pub p{font-variation-settings:'wght' 430}

@media (max-width:760px){
  .ph .top{flex-direction:column;gap:6px;margin-bottom:20px}
  .lab.rd{text-align:left;white-space:normal}
  .ph h1{max-width:none}
  .pub .no{font-size:var(--s4)}
  .gt .d{font-size:var(--s1)}
  .prose{font-size:calc(var(--b)*1.05)}
  .statement{margin-top:34px}
}
"""
