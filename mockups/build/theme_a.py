"""Variation A: Paper widgets. Warm paper, white tiles, thin Geist numerals, mono captions, one ultramarine accent.
Every page is built from the paper-widgets components: tiles with dot labels, calendar rows, tick dials, level bars,
the focus switch (here: reading mode, saved across pages)."""
from common import *

D = "site-a"

CSS = r"""
:root{
  --bg:#e7e5e0; --tile:#f8f7f4; --ink:#141416; --ink-rgb:20 20 22; --muted:#5b5850; --ai:#2b36ff; --accent:#2b36ff; --peach:#ffb48a;
  --line:rgba(20,20,22,.08); --wash:rgba(20,20,22,.05); --track:rgba(20,20,22,.07); --hair:rgba(20,20,22,.12);
  --marker:rgba(20,20,22,.14); --dotted:rgba(20,20,22,.16); --sun-glow:rgba(43,54,255,.14);
  --serif:"Fraunces","Iowan Old Style",Georgia,serif; --sans:"Instrument Sans",system-ui,sans-serif; --mono:"Geist Mono",ui-monospace,monospace; --label-font:500 13px/1.2 "Instrument Sans",system-ui,sans-serif;
  --s-1:.8125rem; --s0:1rem; --s1:1.25rem; --s2:1.75rem; --s3:clamp(2rem,1.6rem + 1.6vw,2.5rem); --s4:clamp(2.25rem,1.6rem + 2.8vw,3.5rem); --s5:clamp(2.75rem,1.8rem + 4vw,5rem);
  --disp:"opsz" 72,"SOFT" 50,"WONK" 0;
  --r:38px; --cell:292px; --gap:20px;
  --shadow:0 0 0 1px rgba(20,20,22,.05), inset 0 1px 0 #fff, 0 28px 46px -30px rgba(40,34,20,.35), 0 2px 4px rgba(40,34,20,.04);
  --focus-dark:radial-gradient(260px 220px at 75% 15%, rgba(43,54,255,.55), transparent 70%), #121215;
}
html.night{--ai:#9aa1ff;--bg:#0d0d10;--tile:#17171b;--ink:#f4f3f0;--ink-rgb:244 243 240;--muted:#a9a69e;--line:rgba(255,255,255,.07);--wash:rgba(255,255,255,.06);--track:rgba(255,255,255,.08);--hair:rgba(255,255,255,.14);--marker:rgba(255,255,255,.16);--dotted:rgba(255,255,255,.2);
  --shadow:0 0 0 1px rgba(255,255,255,.05), inset 0 1px 0 rgba(255,255,255,.06), 0 28px 46px -30px rgba(0,0,0,.8)}
h1,h2,h3{word-spacing:.04em;text-wrap:balance;font-optical-sizing:auto}p,li{text-wrap:pretty}
.serif-l,.hero h1,.ph h1,.shead h2,.thin,.big,.cnt,.digits,.state,.share .h,.ttl,.mission p,.atile h1,.prose h2,.pubcard h3,.count-num,.ind .val,.cal .day,.dd b{font-family:var(--serif);font-variation-settings:var(--disp);font-feature-settings:"kern","liga","lnum","tnum"}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:var(--s0);line-height:1.5;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;font-kerning:normal;font-feature-settings:"kern","liga","calt";font-variant-numeric:tabular-nums lining-nums;transition:background .5s,color .5s}
a{color:inherit;text-decoration:none}
button,input,select,textarea{font:inherit;color:inherit}
button{background:none;border:0;cursor:pointer}
img{display:block;max-width:100%}
.wrap{max-width:calc(var(--cell)*4 + var(--gap)*3 + 64px);margin:0 auto;padding:0 32px}
.skip{position:absolute;left:-999px;top:8px;background:var(--ink);color:var(--tile);padding:8px 14px;border-radius:99px;z-index:99}
.skip:focus{left:12px}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}

.serif-l{font-weight:300;letter-spacing:-.025em}
/* nav */
.nav{display:flex;align-items:center;justify-content:space-between;padding:26px 0 34px;gap:16px}
.brand{display:flex;align-items:center;gap:10px;font:500 17px/1 var(--serif);font-variation-settings:"opsz" 24;letter-spacing:-.02em}
.brand i{width:26px;height:26px;border-radius:9px;background:var(--accent);position:relative;overflow:hidden;flex:none}
.brand i::after{content:"";position:absolute;right:-9px;top:-9px;width:20px;height:20px;border-radius:50%;background:var(--peach)}
.pill-nav{display:flex;list-style:none;background:var(--tile);border-radius:99px;padding:5px;box-shadow:var(--shadow);transition:background .5s}
.pill-nav a{display:block;padding:9px 15px;border-radius:99px;font:500 16px/1.2 var(--sans);letter-spacing:.002em;color:var(--muted);white-space:nowrap;transition:color .2s}
.pill-nav a.on{background:var(--ink);color:var(--tile)}
.pill-nav a:hover:not(.on){color:var(--ink)}
.nav-r{display:flex;align-items:center;gap:10px}
.mini-sw{width:46px;height:28px;border-radius:99px;background:var(--hair);position:relative;transition:background .3s;flex:none}
.mini-sw b{position:absolute;left:3px;top:3px;width:22px;height:22px;border-radius:50%;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.2);transition:transform .3s cubic-bezier(.33,1,.68,1);display:grid;place-items:center;color:#141416}
html.night .mini-sw{background:var(--accent)}
html.night .mini-sw b{transform:translateX(18px)}
.menu-btn{display:none;width:44px;height:44px;border-radius:50%;background:var(--tile);box-shadow:var(--shadow);place-items:center}

/* tiles */
.tile{position:relative;display:block;background:var(--tile);border-radius:var(--r);box-shadow:var(--shadow);overflow:hidden;transition:background .5s,box-shadow .5s}
.rise{opacity:0;transform:translateY(22px) scale(.955)}
.rise.in{opacity:1;transform:none;transition:opacity .65s cubic-bezier(.33,1,.68,1),transform .65s cubic-bezier(.33,1,.68,1),background .5s,box-shadow .5s}
.pad{padding:24px 26px 26px}
.label{display:flex;align-items:center;gap:8px;font:600 13px/1.2 var(--sans);letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.label i{width:6px;height:6px;border-radius:50%;background:var(--accent);flex:none}
.tile > .label.abs{position:absolute;left:26px;top:22px}
.tr{position:absolute;right:26px;top:22px;font-size:13px;color:var(--muted)}
.mono{font-family:var(--mono)}
.muted{color:var(--muted)}
.thin{font-weight:300;letter-spacing:-.02em;line-height:1}
.chip{display:inline-flex;align-items:center;font:500 13px/1 var(--mono);letter-spacing:.04em;text-transform:uppercase;padding:5px 9px;border-radius:99px;background:var(--wash);color:var(--muted);white-space:nowrap}
.chip.a{background:var(--accent);color:#fff}
.chip.ink{background:var(--ink);color:var(--tile)}
.btn{display:inline-flex;align-items:center;gap:8px;height:46px;padding:0 20px;border-radius:99px;font:500 16px/1 var(--sans);letter-spacing:.005em;background:var(--ink);color:var(--tile);transition:transform .15s;white-space:nowrap}
.btn.ghost{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px var(--hair)}
.btn.sm{height:34px;padding:0 14px;font:500 13px/1 var(--mono);letter-spacing:.04em;text-transform:uppercase}
.btn:active{transform:scale(.96)}
.well{width:36px;height:36px;border-radius:11px;background:var(--wash);display:grid;place-items:center;flex:none}
.well.lg{width:64px;height:64px;border-radius:50%}

/* page header */
.ph{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:end;margin:6px 0 30px}
.ph h1{font-weight:300;font-size:var(--s5);line-height:.98;letter-spacing:-.02em;margin-top:14px}
.ph p{color:var(--muted);font-size:var(--s1);line-height:1.5;max-width:58ch;margin-top:16px}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:var(--gap)}
.c3{grid-column:span 3}.c4{grid-column:span 4}.c5{grid-column:span 5}.c6{grid-column:span 6}.c7{grid-column:span 7}.c8{grid-column:span 8}.c12{grid-column:span 12}
section{margin-top:72px}
.shead{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:20px;gap:16px}
.shead h2{font-weight:300;font-size:var(--s4);letter-spacing:-.018em;line-height:1.02}
.shead a{font:500 16px var(--sans);color:var(--muted)}.shead a:hover{color:var(--ink)}

/* calendar rows: the list primitive */
.rows{padding:8px 26px}
.crow{display:grid;grid-template-columns:74px 3px 1fr auto;gap:16px;align-items:center;padding:18px 0;border-top:1px solid var(--line)}
.crow:first-child{border-top:0}
.crow .t{font:500 13px/1.2 var(--mono);letter-spacing:.02em;color:var(--muted)}
.crow .m{height:36px;border-radius:2px;background:var(--marker);transition:background .2s}
.crow.next .m,.crow:hover .m{background:var(--accent)}
.crow .n{font-size:16.5px;font-weight:500;letter-spacing:-.011em;line-height:1.3}
.crow .d{font-size:13px;color:var(--muted);margin-top:3px;line-height:1.4}

/* level bars (batteries) */
.lvl{display:grid;grid-template-columns:36px 1fr auto;gap:4px 12px;align-items:center;padding:12px 0}
.lvl .well{grid-row:span 2}
.lvl .nm{font-size:16px}
.lvl .pc{font:13px var(--mono)}
.lvl .bar{grid-column:2/4;height:8px;border-radius:99px;background:var(--track);overflow:hidden;position:relative}
.lvl .bar b{position:absolute;inset:0 auto 0 0;border-radius:99px;background:var(--ink);width:0;transition:width 1s cubic-bezier(.33,1,.68,1)}
.lvl .bar b.ch{background:var(--accent)}
.shim{position:absolute;top:0;bottom:0;width:40px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.55),transparent);animation:shim 1.8s linear infinite}
@keyframes shim{from{left:-30%}to{left:100%}}

/* dial (focus timer) */
.dial line{stroke:var(--dotted);stroke-linecap:round;transition:stroke .25s}
.dial line.lit{stroke:var(--accent)}

/* forms */
.field{display:block;margin-bottom:14px}
.field span{display:flex;align-items:center;gap:8px;font:600 13px/1.2 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.field span i{width:6px;height:6px;border-radius:50%;background:var(--accent)}
.inp{width:100%;height:52px;border-radius:16px;border:0;background:var(--wash);padding:0 16px;font-size:16px;letter-spacing:-.005em;outline:none;transition:box-shadow .2s,background .2s}
textarea.inp{height:150px;padding:14px 16px;resize:vertical;line-height:1.5}
.inp:focus{box-shadow:inset 0 0 0 1.5px var(--accent);background:transparent}
.seg{display:flex;flex-wrap:wrap;gap:6px}
.seg button{height:34px;padding:0 13px;border-radius:99px;background:var(--wash);font:500 13px/1 var(--sans);color:var(--muted);transition:background .2s,color .2s}
.seg button.on{background:var(--ink);color:var(--tile)}

/* prose */
.prose{font-family:var(--serif);font-variation-settings:"opsz" 14,"SOFT" 0;font-feature-settings:"kern","liga","onum","pnum";font-variant-numeric:oldstyle-nums proportional-nums;font-size:clamp(1.0625rem,1rem + .3vw,1.2rem);line-height:1.68;max-width:64ch;hanging-punctuation:first;font-weight:380}
.prose p{margin:0 0 1.15em}
.prose h2{font-weight:340;font-size:var(--s3);letter-spacing:-.025em;line-height:1.08;margin:1.7em 0 .55em;font-variation-settings:var(--disp);scroll-margin-top:24px}
.prose h3{font:600 var(--s1)/1.3 var(--sans);letter-spacing:-.012em;margin:1.8em 0 .4em}
.prose li{margin:0 0 .6em 1.1em}
.prose a{text-decoration:underline;text-decoration-color:var(--accent);text-underline-offset:3px}

footer{margin-top:96px;padding:28px 0 44px;border-top:1px solid var(--hair);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center}
footer .links{display:flex;gap:18px;flex-wrap:wrap;font:500 13px var(--sans);color:var(--muted)}
footer .links a:hover{color:var(--ink)}

/* ——— home widgets ——— */
.home{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:48px;align-items:start;margin-top:16px}
.hero{display:flex;flex-direction:column;gap:24px;padding:8px 0}
.hero h1{font-weight:300;font-size:clamp(2.75rem,1.8rem + 4vw,4.5rem);line-height:.98;letter-spacing:-.022em}
.hero h1 span{font-style:italic;font-variation-settings:"opsz" 144,"SOFT" 100,"WONK" 1;color:var(--ai)}
.hero p{font-size:var(--s1);line-height:1.5;color:var(--muted);max-width:40ch}
.soon{padding:24px 24px 8px}
.soon-h{display:flex;justify-content:space-between;align-items:baseline;gap:16px;margin-bottom:8px}
.soon-h h2{font-weight:300;font-size:var(--s2);letter-spacing:-.018em;line-height:1.1}
.soon-h a{font-size:16px;color:var(--ai);text-decoration:underline;text-underline-offset:4px;display:inline-flex;align-items:center;min-height:44px}
.srow{display:grid;grid-template-columns:56px minmax(0,1fr) auto;gap:16px;align-items:center;padding:16px 8px;margin:0 -8px;border-radius:16px;transition:background .2s}
.srow:hover{background:var(--wash)}
.srow .dd{text-align:center}
.srow .dd b{display:block;font-weight:300;font-size:32px;line-height:1;letter-spacing:-.022em}
.srow .dd span{font:500 13px/1.3 var(--mono);letter-spacing:.06em;color:var(--muted);text-transform:uppercase}
.srow .n{font-size:16px;font-weight:500;line-height:1.3;letter-spacing:-.011em}
.srow .f{font-size:13px;color:var(--muted);margin-top:4px;line-height:1.35}
.srow .r{display:grid;gap:8px;justify-items:end}
.srow .amt{font:500 13px/1.2 var(--mono);white-space:nowrap}
.cta{display:flex;gap:8px;flex-wrap:wrap}
/* publication cards */
.pubcard{display:grid;grid-template-columns:200px 1fr;gap:26px;padding:24px;align-items:center}
.pubcard h3{font-weight:360;font-size:var(--s2);letter-spacing:-.02em;line-height:1.12;margin:12px 0 8px}
.pubcard p{color:var(--muted);font-size:16px;line-height:1.5}
.pubcard .meta{display:flex;align-items:center;gap:12px;margin-top:18px}
.pubcard .pbar{flex:1;max-width:220px;height:5px;border-radius:99px;background:var(--track);position:relative}
.pubcard .pbar b{position:absolute;inset:0 auto 0 0;border-radius:99px;background:var(--ink)}
.pubcard .playb{width:44px;height:44px;border-radius:50%;background:var(--ink);color:var(--tile);display:grid;place-items:center;transition:transform .2s}
.pubcard:hover .playb{transform:scale(1.08);background:var(--accent);color:#fff}

/* article page */
.read{display:grid;grid-template-columns:300px 1fr;gap:var(--gap);align-items:start}
.side{position:sticky;top:20px;display:grid;gap:var(--gap)}
.rprog{height:5px;border-radius:99px;background:var(--track);position:relative;margin:22px 0 8px}
.rprog b{position:absolute;inset:0 auto 0 0;border-radius:99px;background:var(--ink);width:0}
.rprog i{position:absolute;top:-5px;width:15px;height:15px;margin-left:-7px;border-radius:50%;background:#fff;box-shadow:0 0 0 1px var(--hair),0 2px 6px rgba(0,0,0,.15);left:0}
.toc .crow{grid-template-columns:3px 1fr;padding:10px 0;border-top:1px solid var(--line)}
.toc .crow .m{height:26px}
.toc .crow .n{font-size:16px;font-weight:450}
.atile{padding:30px 44px 50px}
.atile h1{font-weight:300;font-size:var(--s4);line-height:1.02;letter-spacing:-.018em;margin:18px 0 20px;max-width:18ch}
.banner{border-radius:24px;overflow:hidden;margin:26px 0 8px}
.banner img{width:100%;max-height:440px;object-fit:cover;filter:grayscale(1) contrast(1.05)}
.capt{font:13px/1.4 var(--sans);color:var(--muted);margin-bottom:30px}

/* grants */
.gfind{display:grid;grid-template-columns:320px 1fr;gap:var(--gap);align-items:start}
.gside{display:grid;gap:var(--gap);position:sticky;top:20px}
.search{position:relative}
.search .inp{padding-left:44px}
.search svg{position:absolute;left:16px;top:17px;color:var(--muted)}
.fl{margin-top:18px}.fl > .label{margin-bottom:10px}
.gres{padding:6px 26px}
.grow{display:grid;grid-template-columns:64px 1fr 140px 88px;gap:18px;align-items:center;padding:16px 0;border-top:1px solid var(--line);cursor:pointer}
.grow:first-child{border-top:0}
.grow .dd{text-align:center}
.grow .dd b{display:block;font-weight:300;font-size:32px;letter-spacing:-.022em;line-height:1;font-variant-numeric:lining-nums tabular-nums}
.grow .dd span{font:500 13px/1 var(--mono);letter-spacing:.1em;color:var(--muted);text-transform:uppercase}
.grow .n{font-size:16.5px;font-weight:500;letter-spacing:-.011em;line-height:1.3}
.grow .f{font-size:13px;color:var(--muted);margin-top:3px}
.grow .amt{white-space:nowrap;font:500 13px/1.2 var(--mono);text-align:right}
.grow .st{text-align:right}
.grow.closed{opacity:.55}
.gdetail{grid-column:1/-1;display:none;padding:4px 0 6px 80px;color:var(--muted);font-size:16px;line-height:1.6;max-width:62ch}
.grow.x .gdetail{display:block}
.gdetail .btn{margin-top:12px}
.count-num{font-weight:300;font-size:var(--s5);letter-spacing:-.022em;line-height:1;margin-top:20px}

/* indicators */
.ind{padding:22px 26px 22px;min-height:292px;position:relative}
.ind .val{font-weight:300;font-size:var(--s5);letter-spacing:-.022em;line-height:1;margin-top:26px}
.ind .val small{font:400 18px var(--sans);letter-spacing:0;color:var(--muted);margin-left:6px}
.ind .desc{font-size:13px;color:var(--muted);line-height:1.5;margin-top:10px;max-width:46ch}
.ind svg{display:block;width:100%;height:96px;margin-top:16px;overflow:visible}
.ind .yrs{display:flex;justify-content:space-between;font:13px/1 var(--mono);color:var(--muted);margin-top:6px}
.note{display:flex;gap:10px;align-items:center;padding:14px 18px;border-radius:18px;background:var(--wash);font-size:13px;color:var(--muted);margin-bottom:var(--gap)}

/* checklist (grant help) */
.check{display:grid;grid-template-columns:28px 1fr;gap:14px;padding:16px 0;border-top:1px solid var(--line);cursor:pointer;text-align:left;width:100%}
.check:first-child{border-top:0}
.check .bx{width:24px;height:24px;border-radius:8px;box-shadow:inset 0 0 0 1.5px var(--hair);display:grid;place-items:center;transition:background .2s,box-shadow .2s;color:#fff}
.check.done .bx{background:var(--accent);box-shadow:none}
.check b{font-weight:600;font-size:16px;letter-spacing:-.011em}
.check p{font-size:16px;color:var(--muted);line-height:1.5;margin-top:4px}
.check.done b{text-decoration:line-through;text-decoration-color:var(--accent)}

[hidden]{display:none!important}
summary{list-style:none}summary::-webkit-details-marker{display:none}summary.label::after{content:"+";margin-left:6px}
@media (max-width:1300px){
  .home{grid-template-columns:1fr;gap:32px}
  .wrap{max-width:calc(var(--cell)*2 + var(--gap) + 64px)}
  .mission{grid-template-columns:1fr}
  .pill-nav{display:none}.menu-btn{display:grid}
  .grid > *{grid-column:span 12}
  .read,.gfind{grid-template-columns:1fr}.side,.gside{position:static}
  .pill-nav.open{display:flex;flex-direction:column;position:absolute;right:32px;top:84px;border-radius:24px;z-index:20;padding:8px}
}
@media (max-width:700px){
  :root{--cell:calc(100vw - 48px);--r:30px}
  .wrap{padding:0 24px;max-width:none}
  .hero h1{font-size:clamp(2.5rem,13vw,3.25rem)}
  .soon{padding:20px 16px 8px}.srow{grid-template-columns:48px minmax(0,1fr) auto;gap:12px}
  .ph{grid-template-columns:1fr}.ph h1{font-size:clamp(2.6rem,12vw,3.4rem)}
  .pubcard{grid-template-columns:1fr}.pubcard .cover{max-width:160px}
  .atile{padding:24px 22px 36px}.atile h1{font-size:clamp(2.1rem,9vw,2.6rem)}
  .prose{font-size:1.0625rem}
  .grow{grid-template-columns:52px 1fr 78px}.grow .amt{display:none}.gdetail{padding-left:0}
  .crow{grid-template-columns:3px 1fr}.crow .t,.crow > .chip{display:none}
  .mission p{font-size:clamp(1.8rem,8vw,2.2rem)}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}.rise{opacity:1;transform:none}}
"""

JS = r"""
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
"""

HEAD_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,250..600,0..100,0..1;1,9..144,250..600,0..100,0..1&family=Instrument+Sans:wght@400..700&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">'

ICONS = {
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    "hands": '<path d="M3 12l4-4 4 3 3-3 3 1 4 3M7 8v5l4 4 2-2M13 15l2 2 2-2M11 11l3 3"/>',
    "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" fill="currentColor" stroke="none"/>',
    "people": '<circle cx="9" cy="9" r="3.2"/><circle cx="16.5" cy="10" r="2.5"/><path d="M3.5 19c.6-3 3-5 5.5-5s4.9 2 5.5 5M15 15c2.4-.2 4.4 1.3 5 3.8"/>',
    "person": '<circle cx="12" cy="8" r="3.6"/><path d="M5 20c.8-3.6 3.6-6 7-6s6.2 2.4 7 6"/>',
    "shield": '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/>',
    "doc": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
    "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
    "menu": '<path d="M4 8h16M4 16h16"/>',
    "check": '<path d="m5 12 4.5 4.5L19 7" stroke-width="2.4"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "play": '<path d="M8 5v14l11-7z" fill="currentColor" stroke="none"/>',
}


def icon(n, s=18):
    return f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[n]}</svg>'


def label(t, cls=""):
    return f'<div class="label {cls}"><i></i>{t}</div>'


COVERS = ["cv-a", "cv-b", "cv-c"]


def cover(i, mk=None):
    return f'<div class="cover {COVERS[i % 3]}"><span class="mk">{mk or f"E3—0{i+1}"}</span></div>'


def shell(page, body, scripts=""):
    active = SECTION.get(page, "")
    nav = "".join(f'<li><a href="{h}"{" class=on aria-current=page" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    foot = "".join(f'<a href="{h}">{t}</a>' for h, t in FOOT)
    title = TITLES[page]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} · e3 Initiative</title>
<script>if(localStorage.getItem('e3-night')==='1')document.documentElement.classList.add('night')</script>
{HEAD_FONTS}
<link rel="stylesheet" href="theme.css">
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<div class="wrap">
  <header class="nav">
    <a class="brand" href="index.html"><i></i>e3 Initiative</a>
    <div class="nav-r">
      <ul class="pill-nav" id="nav">{nav}</ul>
      <button class="mini-sw" role="switch" aria-checked="false" aria-label="Dark mode" data-night><b>{icon('moon', 12)}</b></button>
      <button class="menu-btn" aria-label="Menu" aria-controls="nav" aria-expanded="false">{icon('menu')}</button>
    </div>
  </header>
  <main id="main">
{body}
  </main>
  <footer>
    <span class="mono" style="font-size:13px;color:var(--muted)">© 2026 e3 Initiative</span>
    <nav class="links" aria-label="Footer">{foot}</nav>
  </footer>
</div>
<script src="theme.js"></script>
{scripts}
</body>
</html>
"""


def ph(kicker, title, lede="", right=""):
    return f'<div class="ph"><div>{label(kicker)}<h1>{title}</h1>{f"<p>{lede}</p>" if lede else ""}</div><div>{right}</div></div>'


def crow(t, n, d="", href="#", chip="", next_=False):
    tag = "a" if href else "div"
    return f'<{tag} class="crow{" next" if next_ else ""}"{f" href={chr(34)}{href}{chr(34)}" if href else ""}><span class="t">{t}</span><span class="m"></span><div><div class="n">{n}</div>{f"<div class=d>{d}</div>" if d else ""}</div>{chip}</{tag}>'


def lvl(ic, name, pct, charging=False):
    return f'<div class="lvl"><div class="well">{icon(ic)}</div><div class="nm">{name}</div><div class="pc">0%</div><div class="bar"><b class="{"ch" if charging else ""}" data-w="{pct:.0f}">{"<span class=shim></span>" if charging else ""}</b></div></div>'


def status_chip(s, d=None):
    if s == "open":
        return f'<span class="chip a">{"in " + str(d) + "d" if d is not None else "Open"}</span>'
    return f'<span class="chip">{"Rolling" if s == "rolling" else "Closed"}</span>'


# ——— Pages ———
def home():
    """Nav, hero with one primary action, and the next four dated deadlines."""
    rows = ""
    for g in DATED_SOON[:4]:
        mon, day = deadline_label(g).split(" ")
        d = days_left(g)
        chip = f'<span class="chip a">{"Today" if d == 0 else f"in {d} days" if d != 1 else "in 1 day"}</span>'
        rows += (f'<a class="srow" href="grants.html"><div class="dd"><b>{int(day)}</b><span>{mon}</span></div>'
                 f'<div><div class="n">{esc(g["name"])}</div><div class="f">{esc(g["funder"])}</div></div>'
                 f'<div class="r"><span class="amt">{"up to " + money(g.get("amountMax")) if g.get("amountMax") else "Varies"}</span>{chip}</div></a>')
    body = f"""
<div class="home">
  <div class="hero">
    {label('Equity · Economics · Ethnicity')}
    <h1>{TAGLINE}<span>.</span></h1>
    <p>Student-led research on who builds local economies, who gets credit and who gets left out.</p>
    <div class="cta"><a class="btn pri" href="grants.html">Open Grant Finder</a><a class="btn ghost" href="articles.html">Read the research</a></div>
  </div>
  <section class="tile soon rise" aria-labelledby="soon-h" style="margin-top:0">
    <div class="soon-h"><h2 id="soon-h">Closing soon</h2><a href="grants.html">All grants</a></div>
    {rows}
  </section>
</div>
"""
    return shell("index", body)

def pub_list(page, kicker, title, lede, items, extra=""):
    """Header and one list."""
    rows = "".join(crow(p['short'][:6], esc(p['title']), f"{p['kind']} · {p['min']} min · {p['author']}", p['slug'] + '.html') for p in items)
    return shell(page, ph(kicker, title, lede) + f'<div class="tile rows rise">{rows}</div>')

def article(p):
    """Title, banner, text. A thin bar at the top shows reading progress."""
    a = p["data"]
    body = []
    for i, (t, txt) in enumerate(a["blocks"]):
        if t == "h2":
            body.append(f'<h2 id="s{i}">{txt}</h2>')
        elif t == "li":
            body.append(f"<ul><li>{txt}</li></ul>")
        else:
            body.append(f"<{t}>{txt}</{t}>")
    cite = {"article-railroad": "articles/chinese-labor-transcontinental-railroad-citations.html", "article-chinatown": "articles/chinatown-citations.html", "research-chinatown": "research/chinatown-solidarity-paper-citations.html"}[p["slug"]]
    body.append(f'<p class="muted" style="font-size:16px;margin-top:2em"><a href="../../{cite}">Citations and sources →</a></p>')
    body_html = f"""
<style>.topbar{{position:fixed;left:0;right:0;top:0;height:3px;background:transparent;z-index:40}}.topbar b{{display:block;height:100%;width:0;background:var(--accent)}}</style>
<div class="topbar"><b id="rb"></b></div>
<article class="tile atile rise" style="max-width:820px;margin:0 auto">
  {label(f"{p['kind']} · {p['date']} · {p['min']} min")}
  <h1>{esc(p['title'])}</h1>
  <div class="mono muted" style="font-size:13px">{esc(a['byline'] or 'By ' + p['author'])}</div>
  <div class="banner"><img src="{IMG}{p["img"].replace("-640", "")}" alt="{esc(p["alt"])}"></div><div class="capt">{esc(a["caption"] or p["alt"])}</div>
  <div class="prose" id="prose">{''.join(body)}</div>
</article>"""
    js = """<script>
const pr = $('#prose');
function upd() { const r = pr.getBoundingClientRect(), k = Math.max(0, Math.min(1, (innerHeight * .4 - r.top) / r.height)); $('#rb').style.width = k * 100 + '%'; }
addEventListener('scroll', upd, { passive: true }); upd();
</script>"""
    return shell(p["slug"], body_html, js)

def about():
    """Header, one statement, three people."""
    team = "".join(crow(f"0{i+1}", n, f"{r}. {b}", "") for i, (n, r, b) in enumerate(ABOUT["team"]))
    body = ph("About", "About e3 Initiative") + f"""
<div class="tile pad rise"><p class="serif-l" style="font-size:var(--s3);line-height:1.15;max-width:30ch">{ABOUT['who']}</p><p class="muted" style="font-size:16px;line-height:1.6;margin-top:18px;max-width:64ch">{ABOUT['what']}</p></div>
<section style="margin-top:20px"><div class="tile rows rise">{team}</div>
<p class="muted" style="font-size:16px;margin-top:20px;max-width:70ch">We believe in community voices, cross-sector collaboration, and turning findings into stories of economic resilience.</p></section>"""
    return shell("about", body)

def journals():
    t, logo = JOURNAL
    body = ph("Publications", "Journals", "Browse our academic journals and long-form publications.") + f"""
<div class="tile pad rise" style="display:flex;gap:30px;align-items:center;flex-wrap:wrap"><img src="{IMG}{logo}" alt="{esc(t)}" width="160" height="160" style="border-radius:20px">
<div>{label('Journal')}<div class="serif-l" style="font-size:var(--s3);line-height:1.08;margin-top:14px;max-width:18ch">{t}</div><p class="muted" style="margin-top:10px;font-size:16px">Entries coming soon.</p></div></div>"""
    return shell("journals", body)

def grants():
    """Header, one search row, results. Other filters are folded away."""
    cats = "".join(f'<button data-v="{k}">{v}</button>' for k, v in CAT_LABEL.items())
    lists = " · ".join(f'<a href="{s}.html" style="color:var(--ink)">{CAT_LABEL[c]}</a>' for s, (c, _, _) in CATEGORY_PAGES.items())
    body = ph("Grants", "Grant Finder", f"Funding for small businesses and nonprofits. Ready-made lists: {lists}.", '<a class="btn ghost" href="grant-help.html">Help & tips →</a>') + f"""
<form class="tile pad rise gform" style="margin-bottom:24px" onsubmit="return false" role="search" aria-label="Grant filters">
  <div class="gtop">
    <div class="gctl"><label class="label" for="q"><i></i>Search</label><div class="search">{icon('search')}<input class="inp" id="q" type="search" placeholder="Women-owned bakery" autocomplete="off"></div></div>
    <fieldset class="gctl"><legend class="label"><i></i>Status</legend><div class="seg" data-f="status"><button type="button" class="on" aria-pressed="true" data-v="live">Open + rolling</button><button type="button" aria-pressed="false" data-v="">All</button></div></fieldset>
    <fieldset class="gctl"><legend class="label"><i></i>Sort by</legend><div class="seg" data-f="sort"><button type="button" class="on" aria-pressed="true" data-v="soon">Soonest deadline</button><button type="button" aria-pressed="false" data-v="amt">Largest award</button></div></fieldset>
  </div>
  <details><summary class="label"><i></i>More filters</summary>
    <fieldset class="gctl fl"><legend class="label">Who qualifies</legend><div class="seg" data-f="elig"><button type="button" class="on" aria-pressed="true" data-v="">Anyone</button><button type="button" aria-pressed="false" data-v="small_business">Business</button><button type="button" aria-pressed="false" data-v="nonprofit">Nonprofit</button></div></fieldset>
    <fieldset class="gctl fl"><legend class="label">Award up to at least</legend><div class="seg" data-f="amt"><button type="button" class="on" aria-pressed="true" data-v="0">Any</button><button type="button" aria-pressed="false" data-v="10000">$10k</button><button type="button" aria-pressed="false" data-v="50000">$50k</button><button type="button" aria-pressed="false" data-v="250000">$250k</button></div></fieldset>
    <fieldset class="gctl fl"><legend class="label">Category</legend><div class="seg" data-f="cat" data-multi><button type="button" class="on" aria-pressed="true" data-v="">All</button>{cats.replace('<button ', '<button type="button" aria-pressed="false" ')}</div></fieldset></details>
</form>
<div class="gcount"><h2 id="gcount" aria-live="polite">33 grants</h2><p id="gsort">Soonest deadline first</p></div>
<div class="tile gres rise" id="gres"><div class="gload" role="status">Loading grants</div></div>"""
    js = """<script src="../shared/grants-data.js"></script><script>
const F = { q: '', elig: '', status: 'live', amt: 0, cat: new Set(), sort: 'soon' };
const press = (b, on) => { b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); };
$$('.seg[data-f]').forEach(seg => seg.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; const f = seg.dataset.f;
  if (seg.hasAttribute('data-multi')) { if (!b.dataset.v) { F.cat.clear(); $$('button', seg).forEach(x => press(x, !x.dataset.v)); }
    else { F.cat.has(b.dataset.v) ? F.cat.delete(b.dataset.v) : F.cat.add(b.dataset.v); press(b, F.cat.has(b.dataset.v)); press($('button[data-v=""]', seg), !F.cat.size); } }
  else { $$('button', seg).forEach(x => press(x, x === b)); F[f] = f === 'amt' ? +b.dataset.v : b.dataset.v; } render(); }));
$('#q').addEventListener('input', e => { F.q = e.target.value.toLowerCase(); render(); });
function reset() { Object.assign(F, { q: '', elig: '', status: 'live', amt: 0, sort: 'soon' }); F.cat.clear(); $('#q').value = '';
  $$('.seg[data-f]').forEach(seg => $$('button', seg).forEach((x, i) => press(x, i === 0))); render(); }
const RANK = { open: 0, rolling: 1, closed: 2 };
function render() {
  const rs = GRANTS.filter(g => (!F.q || (g.name + g.funder + g.desc + CAT_LABEL[g.cat]).toLowerCase().includes(F.q))
    && (!F.elig || g.elig === F.elig || g.elig === 'both') && (F.status === '' || g.status !== 'closed')
    && (!F.amt || g.max >= F.amt) && (!F.cat.size || F.cat.has(g.cat)))
    .sort((a, b) => (a.status === 'closed') - (b.status === 'closed') || (F.sort === 'amt' ? b.max - a.max : (a.days ?? 9999) - (b.days ?? 9999) || RANK[a.status] - RANK[b.status]));
  $('#gcount').textContent = rs.length + (rs.length === 1 ? ' grant' : ' grants');
  $('#gsort').textContent = F.sort === 'amt' ? 'Largest award first' : 'Soonest deadline first';
  $('#gres').innerHTML = rs.length ? rs.map(g => { const dt = g.days != null ? g.dl.split(' ') : null;
    return `<div class="grow ${g.status}" tabindex="0" role="button" aria-expanded="false"><div class="dd">${dt ? `<b>${+dt[1]}</b><span>${dt[0]}</span>` : `<b style="font-size:24px">∞</b><span>${g.dl}</span>`}</div>
      <div><div class="n">${g.name}</div><div class="f">${g.funder}</div></div><div class="amt">${g.max ? 'up to $' + g.max.toLocaleString() : 'Varies'}</div>
      <div class="st">${g.status === 'open' ? `<span class="chip a">${g.days != null ? 'in ' + g.days + ' days' : 'Open'}</span>` : `<span class="chip">${g.status === 'rolling' ? 'Rolling' : 'Closed'}</span>`}</div>
      <div class="gdetail">${g.desc}<br><a class="btn sm" href="${g.link}" target="_blank" rel="noopener">Funder's page (opens in new tab) →</a></div></div>`; }).join('')
    : '<div class="gempty"><b>No grants match these filters</b><span class="muted">Try a shorter search or clear the filters.</span><button type="button" class="btn" id="clr">Clear filters</button></div>';
  $('#clr')?.addEventListener('click', reset);
}
const tog = r => r.setAttribute('aria-expanded', r.classList.toggle('x'));
$('#gres').addEventListener('click', e => { const r = e.target.closest('.grow'); if (r && !e.target.closest('a')) tog(r); });
$('#gres').addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && e.target.classList.contains('grow')) { e.preventDefault(); tog(e.target); } });
render();
</script>"""
    return shell("grants", body, js)

def category(slug):
    """Header and one list."""
    cat, title, what = CATEGORY_PAGES[slug]
    intro, gs = category_intro(cat, what)
    gs = sorted(gs, key=lambda g: ({"open": 0, "rolling": 1, "closed": 2}[status(g)], days_left(g) if days_left(g) is not None else 999))
    rows = "".join(crow(deadline_label(g), esc(g["name"]), esc(g["funder"]) + " · " + esc(g["amount"]), g["link"], status_chip(status(g), days_left(g)), status(g) == "open") for g in gs)
    others = " · ".join(f'<a href="{s}.html" style="color:var(--ink)">{CAT_LABEL[v[0]]}</a>' for s, v in CATEGORY_PAGES.items() if s != slug)
    body = ph("Grant list", title, intro) + f'<div class="tile rows rise">{rows}</div><p class="muted" style="margin-top:22px;font-size:16px">More lists: {others} · <a href="grants.html" style="color:var(--ink)">Search all {len(GRANTS)}</a></p>'
    return shell(slug, body)

def grant_help():
    """Header, one checklist. The directory is folded away."""
    tips = "".join(f'<button class="check" data-i="{i}"><span class="bx">{icon("check", 14)}</span><div><b>{a}</b><p>{b}</p></div></button>' for i, (a, b) in enumerate(HELP["tips"]))
    orgs = "".join(crow("→", n, d, u, f'<span class="chip">{l}</span>') for n, d, l, u in HELP["orgs"])
    body = ph("Grants", "Grant Help & Tips", HELP["intro"], '<a class="btn" href="grants.html">Search grants →</a>') + f"""
<div class="tile rows rise" style="padding-top:18px">{label('How to write a strong application · <span id="hcount">0/8</span>')}<div style="margin-top:6px">{tips}</div>
  <details style="padding:16px 0;border-top:1px solid var(--line)"><summary class="label" style="cursor:pointer">Common mistakes to avoid</summary><ul style="margin:12px 0 0 18px;color:var(--muted);font-size:16px;line-height:1.7">{''.join(f'<li>{m}</li>' for m in HELP['mistakes'])}</ul></details>
  <details style="padding:16px 0;border-top:1px solid var(--line)"><summary class="label" style="cursor:pointer">Where to get free help</summary><div style="margin-top:8px">{orgs}</div><p class="muted" style="font-size:13px;line-height:1.6;margin-top:14px;max-width:80ch">{HELP['disclaimer']}</p></details></div>"""
    js = """<script>
const done = new Set(JSON.parse(localStorage.getItem('e3-help') || '[]'));
function upd() { $$('.check[data-i]').forEach(c => c.classList.toggle('done', done.has(+c.dataset.i))); $('#hcount').textContent = done.size + '/8'; localStorage.setItem('e3-help', JSON.stringify([...done])); }
$$('.check[data-i]').forEach(c => c.addEventListener('click', () => { const i = +c.dataset.i; done.has(i) ? done.delete(i) : done.add(i); upd(); })); upd();
</script>"""
    return shell("grant-help", body, js)

def indicators():
    """Header, four key charts, the other four behind one button."""
    def tile(k, grp, name, u, d, extra):
        return f"""<div class="tile ind rise c6{extra}" data-key="{k}" data-unit="{u}">
      {label(f'{grp}: {name}')}<div class="tr mono" data-hl></div>
      <div class="val"><span data-v>—</span><small>{u if u != 'index' else 'index'}</small></div>
      <svg viewBox="0 0 500 96" preserveAspectRatio="none" aria-hidden="true"></svg>
      <div class="yrs"><span>2000</span><span data-end>today</span></div>
      <p class="desc">{d}</p></div>"""
    key = [i for i in INDICATORS if i[0] in KEY_INDICATORS]
    more = [i for i in INDICATORS if i[0] not in KEY_INDICATORS]
    body = ph("Data", "Economic Indicators", "Everyday costs, job security and borrowing rates since 2000. Hover a chart to read any year.") + f"""
<div class="note" id="note" hidden>{icon('spark')}<span>Preview: placeholder shapes. Live FRED data loads from <span class="mono">/api/economic-indicators</span> on the deployed site.</span></div>
<div class="grid">{''.join(tile(*i, '') for i in key)}{''.join(tile(*i, ' more') for i in more)}</div>
<div style="text-align:center;margin-top:24px"><button class="btn ghost" id="moreb" onclick="document.querySelectorAll('.ind.more').forEach(e=>e.hidden=false);this.remove()">Show all 8 indicators</button></div>"""
    js = """<script src="../shared/indicators.js"></script><script>
$$('.ind.more').forEach(e => e.hidden = true);
loadIndicators().then(D => {
  $('#note').hidden = D.live;
  $$('.ind').forEach(t => { const s = D.series[t.dataset.key]; if (!s) return; const svg = $('svg', t), n = s.length, lo = Math.min(...s), hi = Math.max(...s);
    const x = i => i / (n - 1) * 500, y = v => 86 - (v - lo) / (hi - lo || 1) * 76;
    const d = s.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1)).join(' ');
    svg.innerHTML = `<line x1="0" x2="500" y1="90" y2="90" stroke="var(--hair)"/><path d="${d}" fill="none" stroke="var(--dotted)" stroke-width="1.2" stroke-dasharray="2 4" vector-effect="non-scaling-stroke"/>
      <path class="ln" d="${d}" fill="none" stroke="var(--ink)" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" vector-effect="non-scaling-stroke" style="transition:stroke-dashoffset 1.4s cubic-bezier(.65,0,.35,1)"/>
      <circle class="dot" cx="${x(n - 1)}" cy="${y(s[n - 1])}" r="5" fill="var(--accent)"/>`;
    setTimeout(() => $('.ln', svg).setAttribute('stroke-dashoffset', 0), 300);
    $('[data-end]', t).textContent = D.years[n - 1];
    const u = t.dataset.unit, f = v => D.live ? fmtIndicator(v, u) : '—';
    $('[data-v]', t).textContent = D.live ? fmtIndicator(s[n - 1], u).replace('%', '').replace('M', '') : '—';
    $('[data-hl]', t).textContent = D.live ? `H ${f(hi)} · L ${f(lo)}` : '';
    svg.addEventListener('pointermove', e => { const r = svg.getBoundingClientRect(), i = Math.round((e.clientX - r.left) / r.width * (n - 1));
      $('.dot', svg).setAttribute('cx', x(i)); $('.dot', svg).setAttribute('cy', y(s[i])); $('[data-end]', t).textContent = D.years[i] + (D.live ? ' · ' + fmtIndicator(s[i], u) : ''); });
  });
});
</script>"""
    return shell("economic-indicators", body, js)

def outreach():
    cards = "".join(f"""<div class="tile pad rise c6" id="{k}" style="min-height:360px;display:flex;flex-direction:column;justify-content:space-between">
          <div>{label(t)}<p class="serif-l" style="font-size:var(--s2);line-height:1.22;margin-top:22px">{p1}</p><p class="muted" style="margin-top:16px;font-size:16px;line-height:1.55">{p2}</p></div>
          <a class="btn" href="contact.html" style="align-self:flex-start;margin-top:24px">{'Share your story' if k == 'interview' else 'Partner with us'} →</a></div>"""
        for k, (t, s, p1, p2) in OUTREACH.items())
    return shell("outreach", ph("Outreach", "Outreach", "Interviews and partnerships: how community knowledge gets into our research.") + f'<div class="grid">{cards}</div>')

def contact():
    """Header and the form."""
    body = ph("Contact", "Let's connect", "Have questions about our research or want to collaborate? Send a message and we will respond within two business days. We use your details only to reply.") + """
<form class="tile pad rise" onsubmit="event.preventDefault();this.querySelector('[data-sent]').hidden=false" style="padding:30px;max-width:760px">
  <div class="grid" style="gap:0 16px"><label class="field c6"><span><i></i>Name *</span><input class="inp" required autocomplete="name"></label>
  <label class="field c6"><span><i></i>Email *</span><input class="inp" type="email" required autocomplete="email"></label></div>
  <label class="field"><span><i></i>Subject *</span><input class="inp" required></label>
  <label class="field"><span><i></i>Message *</span><textarea class="inp" required></textarea></label>
  <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap"><button class="btn" type="submit">Send message →</button><span class="chip a" data-sent hidden>Mockup: nothing was sent</span></div>
</form>"""
    return shell("contact", body)

def privacy():
    """Header and the policy."""
    out, ul = [], False
    for i, (t, txt) in enumerate(PRIVACY):
        if t == "li":
            if not ul:
                out.append("<ul>"); ul = True
            out.append(f"<li>{txt}</li>"); continue
        if ul:
            out.append("</ul>"); ul = False
        out.append(f"<{t}>{txt}</{t}>")
    if ul:
        out.append("</ul>")
    body = ph("Legal", "Privacy Policy", "The e3 Initiative is a small research organization. This page explains what information this website collects, why, and the choices you have.", '<span class="chip">Updated Nov 12, 2026</span>') + f'<article class="tile atile rise" style="max-width:820px"><div class="prose">{"".join(out)}</div></article>'
    return shell("privacy", body)

def notfound():
    body = f"""<div class="tile rise" style="padding:26px 34px 36px;max-width:760px;margin-top:20px">{label('Page not found')}
    <div class="thin" style="font-family:var(--serif);font-variation-settings:var(--disp);font-size:clamp(8rem,28vw,13rem);font-weight:250;letter-spacing:-.04em;margin:30px 0 10px;color:var(--accent)">404</div>
    <p class="muted" style="max-width:40ch;margin-bottom:24px">Sorry, we couldn't find that page. It may have moved, or the link may be mistyped.</p>
    <div class="cta"><a class="btn" href="index.html">Go home</a><a class="btn ghost" href="articles.html">Publications</a></div></div>"""
    return shell("404", body)

def build():
    write(f"{D}/theme.css", CSS + NOB)
    write(f"{D}/theme.js", JS)
    pages = {
        "index": home(), "about": about(), "journals": journals(), "grants": grants(), "grant-help": grant_help(),
        "economic-indicators": indicators(), "outreach": outreach(), "contact": contact(), "privacy": privacy(), "404": notfound(),
        "articles": pub_list("articles", "Publications", "Publications", "Articles and research papers from our team and partners, from grassroots history to systemic policy analysis.", PUBS),
        "research": pub_list("research", "Publications", "Research", "Research papers, reports, and briefs. Each publication includes clear summaries and next steps for community leaders and decision-makers.", RESEARCH,
            '<section><div class="shead"><h2>Also in Publications</h2></div><div class="grid"><a class="tile pad rise c6" href="journals.html">' + label("Journals") + '<p class="serif-l" style="font-size:var(--s2);line-height:1.15;margin-top:12px">Critical Debates in Humanities, Science and Global Justice →</p></a><a class="tile pad rise c6" href="economic-indicators.html">' + label("Data") + '<p class="serif-l" style="font-size:var(--s2);line-height:1.15;margin-top:12px">Economic indicators since 2000 →</p></a></div></section>'),
    }
    for p in PUBS:
        pages[p["slug"]] = article(p)
    for s in CATEGORY_PAGES:
        pages[s] = category(s)
    for k, v in pages.items():
        write(f"{D}/{k}.html", v)
    return sorted(pages)

# NOBORDERS
NOB = r"""
/* no borders: surfaces separate by tone and space only */
:root{--r:22px}
.tile{box-shadow:none!important;border-radius:22px}
.pill-nav{box-shadow:none}
.crow,.grow,.check,.toc .crow{border-top:0!important}
.cal .div,.gdetail{border:0}
.cal .div{display:none}
details{border-top:0!important}
.btn.ghost{box-shadow:none;background:var(--wash)}
footer{border-top:0}
.tile.rows .crow + .crow,.gres .grow + .grow{box-shadow:none}
.menu-btn{box-shadow:none}
.knob,.mini-sw b{box-shadow:0 2px 6px rgba(0,0,0,.18)}
.inp:focus{box-shadow:none;background:rgb(var(--ink-rgb)/.08)}
.cover.photo,.banner{border-radius:16px}

/* ——— accessibility and clarity pass ——— */
body{font-size:16px}
:focus-visible{outline:3px solid var(--ai);outline-offset:3px;border-radius:6px}
.btn:focus-visible,.seg button:focus-visible,.pill-nav a:focus-visible,.mini-sw:focus-visible,.menu-btn:focus-visible{border-radius:99px}
.inp:focus-visible{outline:3px solid var(--ai);outline-offset:2px}
.grow:focus-visible{outline-offset:-3px;border-radius:16px}
.pill-nav a{min-height:44px;display:flex;align-items:center;font-size:16px;padding:0 16px}
.pill-nav a.on{color:var(--tile)}
.brand{min-height:44px;font-size:20px}
.mini-sw{width:56px;height:44px;background:none!important}
.mini-sw::before{content:"";position:absolute;left:5px;top:8px;width:46px;height:28px;border-radius:99px;background:var(--hair);transition:background .3s}
html.night .mini-sw::before{background:var(--accent)}
.mini-sw b{left:8px;top:11px}
.menu-btn{width:48px;height:48px}
.btn{height:48px;font-size:16px;padding:0 24px;transition:transform .15s,background .2s,box-shadow .2s}
.btn.pri{background:var(--accent);color:#fff}
.btn.pri:hover{background:#1f29d9}
.btn:hover{box-shadow:0 0 0 3px rgb(var(--ink-rgb)/.12)}
.btn.ghost:hover{background:rgb(var(--ink-rgb)/.1)}
.btn.sm{height:44px;font:500 16px/1 var(--sans);letter-spacing:0;text-transform:none}
.btn[disabled]{opacity:.5;cursor:not-allowed}
.chip{font:500 13px/1 var(--mono);padding:7px 11px;letter-spacing:.02em}
.chip.a{background:#2b36ff;color:#fff}
html.night .chip.a{background:#3d47ff}
.label{font-size:13px;letter-spacing:.08em}
.ph p,.hero p{color:var(--muted)}
.crow .t{font-size:13px}
.crow .n{font-size:16px}.crow .d{font-size:16px}
.grow .n{font-size:16px}.grow .f{font-size:16px}.grow .amt{font-size:16px}
.grow .dd span{font-size:13px}
.grow{padding:16px 8px;margin:0 -8px;border-radius:16px;transition:background .2s}
.grow:hover{background:var(--wash)}
.grow.closed{opacity:1}.grow.closed .n,.grow.closed .dd b{color:var(--muted)}
.grow .st .chip{min-width:72px;justify-content:center}
.gdetail{font-size:16px;padding-left:80px}
.seg{gap:8px}
.seg button{min-height:44px;height:44px;padding:0 18px;font-size:16px;color:var(--ink);background:var(--wash);transition:background .2s,color .2s}
.seg button:hover:not(.on){background:rgb(var(--ink-rgb)/.12)}
.seg button.on{background:var(--ink);color:var(--tile)}
.field span{font-size:13px}
.inp{height:52px}
summary.label{min-height:44px;display:flex;align-items:center;cursor:pointer}
.check b,.check p{font-size:16px}
footer .links{font-size:16px;gap:4px 8px}
footer .links a{display:inline-flex;align-items:center;min-height:44px;padding:0 8px}
.shead a{font-size:16px}
.capt,.ind .desc,.note,.pubcard p,.prose + p{font-size:16px}
.toc .crow .n{font-size:16px}
.ind .yrs,.tr{font-size:13px}
.ind .val small{font-size:20px}
.prose a{text-decoration-thickness:2px}
a.skip:focus{outline-color:var(--tile)}
/* grant finder */
.grow{grid-template-columns:64px minmax(0,1fr) 150px 112px}
.grow .st{white-space:nowrap}
.gform{display:grid;gap:24px}
.gtop{display:grid;grid-template-columns:minmax(240px,1fr) auto auto;gap:24px;align-items:end}
.gctl{display:grid;gap:8px;min-width:0}
.gctl > .label{margin:0}
fieldset.gctl{border:0;min-width:0}
fieldset.gctl legend{padding:0;margin-bottom:8px}
.gcount{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap;margin:8px 4px 16px}
.gcount h2{font-family:var(--serif);font-variation-settings:var(--disp);font-weight:300;font-size:var(--s3);letter-spacing:-.02em;line-height:1.1}
.gcount p{font-size:16px;color:var(--muted)}
.gempty{padding:48px 0;text-align:center;display:grid;gap:16px;justify-items:center}
.gempty b{font:500 20px var(--sans)}
.gload{padding:48px 0;text-align:center;color:var(--muted)}
.gres{padding:8px 24px}
.fl{margin-top:24px}
@media (max-width:900px){.gtop{grid-template-columns:1fr}}
@media (max-width:700px){
  .grow{grid-template-columns:48px minmax(0,1fr) auto;gap:12px}
  .grow .st .chip{min-width:0}
  .grow .amt{display:none}
  .gres{padding:8px 16px}
  .crow{grid-template-columns:3px 1fr}
  .gcount h2{font-size:2rem}
}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{transition:none!important;animation:none!important;scroll-behavior:auto!important}.rise{opacity:1;transform:none}}
"""
