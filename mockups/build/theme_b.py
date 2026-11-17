"""Variation B: Graphite desk. Dark graphite slabs with gradient liners and grain, metal fader caps, stepped knobs,
LED meters (white fine, amber soon, red closed) and mono uppercase captions. Built from budget-mixer."""
import json
from common import *

D = "site-b"

CSS = r"""
:root{
  --page:#070708; --text:#f1f1f3; --text-rgb:241 241 243; --label:rgba(241,241,243,.42); --strong:rgba(241,241,243,.85); --body:rgba(241,241,243,.78);
  --panel-top:#1b1b1e; --panel-mid:#131315; --panel-bottom:#0f0f11;
  --divider:rgba(255,255,255,.06); --row-line:rgba(255,255,255,.07); --track:#08080a; --tick:rgba(255,255,255,.14); --tick-label:rgba(255,255,255,.28);
  --led-off:rgba(255,255,255,.05); --led-fine:214 236 226; --led-near:255 181 71; --led-over:255 75 62;
  --metal:linear-gradient(180deg,#f4f4f6 0%,#d3d3d7 48%,#a9a9ae 52%,#c9c9cd 100%);
  --metal-shadow:0 10px 18px rgba(0,0,0,.6),0 2px 4px rgba(0,0,0,.5),inset 0 1px 0 #fff,inset 0 -1px 0 rgba(0,0,0,.25);
  --liner:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.05) 40%,rgba(255,255,255,.02) 70%,rgba(255,255,255,.08));
  --well:#0b0b0d; --well-shadow:inset 0 1px 2px rgba(0,0,0,.9),inset 0 0 0 1px rgba(255,255,255,.04),0 1px 0 rgba(255,255,255,.06);
  --sans:"Geist",sans-serif; --mono:"Geist Mono",monospace; --r:32px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{background:var(--page)}
body{color:var(--text);font-family:var(--sans);-webkit-font-smoothing:antialiased;background:radial-gradient(1400px 900px at 50% 300px,#141416 0%,#0a0a0b 60%,var(--page) 100%) no-repeat}
.grain{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:60;opacity:.06;mix-blend-mode:overlay}
a{color:inherit;text-decoration:none}
button,input,textarea{font:inherit;color:inherit}
button{background:none;border:0;cursor:pointer}
img{display:block;max-width:100%}
.wrap{max-width:1200px;margin:0 auto;padding:0 32px}
.skip{position:absolute;left:-999px;top:8px;z-index:99;background:var(--metal);color:#111;padding:10px 14px;border-radius:10px}
.skip:focus{left:12px}
:focus-visible{outline:1.5px solid rgb(var(--led-near));outline-offset:3px}
.cap{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--label)}
.mono{font-family:var(--mono)}
.dim{color:var(--label)}

/* panel = the desk slab */
.panel{position:relative;border-radius:var(--r);isolation:isolate}
.panel::before{content:"";position:absolute;inset:0;border-radius:inherit;z-index:-1;background:linear-gradient(180deg,var(--panel-top) 0%,var(--panel-mid) 45%,var(--panel-bottom) 100%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.1),inset 0 0 60px rgba(255,255,255,.025),0 40px 70px -40px rgba(0,0,0,.9)}
.panel::after{content:"";position:absolute;inset:0;border-radius:inherit;padding:1px;background:var(--liner);pointer-events:none;
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude}
.pad{padding:30px 34px}
.sheen{position:absolute;left:0;right:0;top:0;height:200px;border-radius:var(--r) var(--r) 0 0;background:radial-gradient(ellipse 60% 100% at 50% 0%,rgba(255,255,255,.06),transparent 70%);pointer-events:none;z-index:-1}
a.panel{transition:transform .25s}
a.panel:hover{transform:translateY(-2px)}

/* nav */
.nav{display:flex;align-items:center;justify-content:space-between;height:84px;border-bottom:1px solid var(--divider);gap:18px}
.brand{display:flex;align-items:center;gap:12px;font-size:15px}
.brand i{width:30px;height:16px;border-radius:5px;background:var(--metal);box-shadow:var(--metal-shadow);position:relative;flex:none}
.brand i::before{content:"";position:absolute;left:6px;right:6px;top:7px;height:2px;border-radius:1px;background:#1a1a1c}
.nav ul{display:flex;gap:26px;list-style:none}
.nav ul a{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--label);display:flex;align-items:center;gap:8px;transition:color .2s}
.nav ul a::before{content:"";width:5px;height:5px;border-radius:1px;background:var(--led-off);transition:background .2s,box-shadow .2s}
.nav ul a:hover,.nav ul a.on{color:var(--text)}
.nav ul a.on::before{background:rgb(var(--led-fine));box-shadow:0 0 6px rgb(var(--led-fine)/.6)}
.menu-btn{display:none;height:40px;padding:0 14px;border-radius:10px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.14)}

/* buttons */
.mbtn{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;height:46px;padding:0 20px;display:inline-flex;align-items:center;gap:10px;border-radius:12px;
  background:var(--metal);color:#111;box-shadow:var(--metal-shadow);transition:transform .12s;white-space:nowrap}
.mbtn:active{transform:translateY(1px) scale(.98)}
.mbtn.ghost{background:transparent;color:var(--text);box-shadow:inset 0 0 0 1px rgba(255,255,255,.14)}
.mbtn.sm{height:34px;padding:0 14px;font-size:10px}
.led{display:inline-block;width:8px;height:8px;border-radius:2px;background:var(--led-off);flex:none}
.led.on{background:rgb(var(--led-fine)/.95);box-shadow:0 0 8px rgb(var(--led-fine)/.35)}
.led.near{background:rgb(var(--led-near));box-shadow:0 0 8px rgb(var(--led-near)/.6)}
.led.over{background:rgb(var(--led-over));box-shadow:0 0 8px rgb(var(--led-over)/.6)}
/* hardware toggle: a recessed key with an LED */
.key{height:38px;padding:0 13px;border-radius:10px;background:linear-gradient(180deg,#26262a,#1a1a1d);box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 4px 10px rgba(0,0,0,.5);
  display:inline-flex;align-items:center;gap:9px;font:10px var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--label);transition:color .2s,transform .1s}
.key::before{content:"";width:6px;height:6px;border-radius:1.5px;background:var(--led-off);transition:background .2s,box-shadow .2s}
.key.on{color:var(--text)}
.key.on::before{background:rgb(var(--led-fine));box-shadow:0 0 6px rgb(var(--led-fine)/.7)}
.key:active{transform:translateY(1px)}
.keys{display:flex;flex-wrap:wrap;gap:8px}
/* LED meter */
.meter{display:flex;gap:3px}
.meter i{width:9px;height:8px;border-radius:2px;background:var(--led-off)}
.meter i.on{background:rgb(var(--led-fine)/.9);box-shadow:0 0 6px rgb(var(--led-fine)/.25)}
.meter i.near{background:rgb(var(--led-near));box-shadow:0 0 6px rgb(var(--led-near)/.5)}
.meter.v{flex-direction:column-reverse;gap:4px}
.meter.v i{width:10px;height:7px}
/* knob */
.knob{position:relative;width:140px;height:140px;flex:none}
.knob svg{position:absolute;inset:0}
.knob .tr,.knob .pg{fill:none;stroke-width:2;stroke-linecap:round}
.knob .tr{stroke:rgba(255,255,255,.08)}.knob .pg{stroke:#f1f1f3}
.kbody{position:absolute;left:26px;top:26px;width:88px;height:88px;border-radius:50%;background:repeating-conic-gradient(from 0deg,#2b2b2f 0deg 3deg,#1c1c1f 3deg 6deg);
  box-shadow:0 14px 24px rgba(0,0,0,.7),0 3px 6px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.18);cursor:grab;touch-action:none;transition:transform .45s cubic-bezier(.65,0,.35,1)}
.kcap{position:absolute;left:34px;top:34px;width:72px;height:72px;border-radius:50%;background:radial-gradient(circle at 40% 28%,#3a3a3f 0%,#232326 55%,#18181a 100%);box-shadow:inset 0 1px 0 rgba(255,255,255,.16),inset 0 -6px 12px rgba(0,0,0,.5);pointer-events:none}
.kptr{position:absolute;left:69px;top:38px;width:2px;height:18px;border-radius:1px;background:#f4f4f6;box-shadow:0 0 8px rgba(255,255,255,.6);transform-origin:1px 32px;pointer-events:none;transition:transform .45s cubic-bezier(.65,0,.35,1)}
.det{position:absolute;font:10px var(--mono);letter-spacing:.1em;transform:translate(-50%,-50%);color:rgb(var(--text-rgb)/.32);transition:color .3s;padding:4px;white-space:nowrap}
.det.on{color:rgb(var(--text-rgb)/.92)}
.knob.sm{width:100px;height:100px}
.knob.sm .kbody{left:20px;top:20px;width:60px;height:60px}.knob.sm .kcap{left:25px;top:25px;width:50px;height:50px}
.knob.sm .kptr{left:49px;top:27px;height:12px;transform-origin:1px 23px}
/* fader */
.fader{position:relative;width:64px;flex:none}
.fader .trk{position:absolute;left:29px;top:0;bottom:0;width:6px;border-radius:3px;background:var(--track);box-shadow:inset 0 1px 2px rgba(0,0,0,.9),0 1px 0 rgba(255,255,255,.06)}
.fader .fill{position:absolute;left:0;right:0;bottom:0;border-radius:3px;background:linear-gradient(0deg,rgba(255,255,255,.05),rgba(255,255,255,.32))}
.fcap{position:absolute;left:0;width:64px;height:32px;margin-top:-16px;border-radius:9px;background:var(--metal);box-shadow:var(--metal-shadow);cursor:grab;touch-action:none}
.fcap::before{content:"";position:absolute;left:8px;right:8px;top:15px;height:2px;border-radius:1px;background:#1a1a1c;box-shadow:0 1px 0 rgba(255,255,255,.6)}
.fcap::after{content:"";position:absolute;inset:-5px;border-radius:13px;box-shadow:0 0 0 1px rgba(255,255,255,.5),0 0 24px rgba(255,255,255,.18);opacity:0;transition:opacity .12s}
.fcap:hover::after,.fcap.drag::after{opacity:1}
.fticks{position:absolute;right:calc(100% + 6px);top:0;bottom:0;width:30px}
.fticks span{position:absolute;right:0;font:9px var(--mono);color:var(--tick-label);transform:translateY(-50%)}
/* hairline rows */
.mrow{display:flex;justify-content:space-between;align-items:baseline;padding:12px 0;border-top:1px solid var(--row-line);gap:16px}
.mrow:last-child{border-bottom:1px solid var(--row-line)}
.mrow b{font:15px var(--mono);font-weight:400;color:var(--text);letter-spacing:0;text-transform:none}
.split{display:flex;gap:3px;height:10px}
.split i{display:block;border-radius:3px;transition:flex .4s cubic-bezier(.65,0,.35,1),opacity .3s}
/* recessed input */
.inp{width:100%;height:50px;border-radius:12px;border:0;background:var(--well);box-shadow:var(--well-shadow);padding:0 16px;font:14px var(--mono);color:var(--text);outline:none;transition:box-shadow .2s}
textarea.inp{height:160px;padding:14px 16px;resize:vertical;line-height:1.6}
.inp:focus{box-shadow:var(--well-shadow),0 0 0 1px rgba(255,255,255,.35)}
.inp::placeholder{color:rgba(241,241,243,.25)}
.field{display:block;margin-bottom:16px}
.field > span{display:flex;align-items:center;gap:8px;margin-bottom:8px}

/* layout */
.ph{display:grid;grid-template-columns:1.3fr 1fr;gap:48px;align-items:end;padding:64px 0 48px}
.ph h1{font-weight:300;font-size:68px;line-height:1;letter-spacing:-.035em;margin-top:20px}
.ph h1 span{color:var(--label)}
.ph p{color:var(--label);font-size:15px;line-height:1.6;max-width:46ch}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:20px}
.c3{grid-column:span 3}.c4{grid-column:span 4}.c5{grid-column:span 5}.c6{grid-column:span 6}.c7{grid-column:span 7}.c8{grid-column:span 8}.c12{grid-column:span 12}
section{margin-top:96px}
.shead{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:22px;gap:16px}
.shead h2{font-weight:300;font-size:46px;letter-spacing:-.03em;line-height:1;margin-top:12px}
.shead a{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--label)}.shead a:hover{color:var(--text)}
.vline{position:relative}
.vline + .vline::before{content:"";position:absolute;left:0;top:20px;bottom:20px;width:1px;background:linear-gradient(180deg,transparent,var(--divider) 20%,var(--divider) 80%,transparent)}

/* rows (index) */
.rows{padding:6px 34px}
.prow{display:grid;grid-template-columns:110px 1fr 140px 64px;gap:26px;align-items:center;padding:22px 0;border-top:1px solid var(--row-line)}
.prow:first-child{border-top:0}
.prow h3{font-weight:400;font-size:18px;letter-spacing:-.02em;line-height:1.3;transition:color .2s}
.prow p{color:var(--label);font-size:13px;margin-top:4px;line-height:1.5}
.prow:hover h3{color:#fff}
.prow .go{text-align:right}
.feat{display:grid;grid-template-columns:1fr 1fr;height:420px;overflow:hidden}
.feat img{width:100%;height:100%;object-fit:cover;border-radius:var(--r) 0 0 var(--r);filter:grayscale(1) contrast(1.1) brightness(.8)}
.feat .txt{padding:40px 44px;display:flex;flex-direction:column;justify-content:space-between}
.feat h3{font-weight:300;font-size:38px;line-height:1.06;letter-spacing:-.03em;margin-top:16px}
.feat p{color:var(--label);font-size:14px;line-height:1.6;max-width:46ch}

/* prose */
.prose{font-size:17.5px;line-height:1.78;color:var(--body);max-width:66ch}
.prose p{margin:0 0 1.2em}
.prose h2{font-weight:300;font-size:32px;letter-spacing:-.03em;line-height:1.1;color:var(--text);margin:1.7em 0 .6em;scroll-margin-top:24px}
.prose h3{font:11px var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--text);margin:2em 0 .6em}
.prose ul{margin:0 0 1.2em 1.1em}.prose li{margin:0 0 .5em}
.prose a{color:var(--text);text-decoration:underline;text-decoration-color:rgb(var(--led-near));text-underline-offset:3px}
.prose strong,.prose b{color:var(--text);font-weight:500}

footer{margin-top:120px;padding:30px 0 50px;border-top:1px solid var(--divider);display:flex;justify-content:space-between;flex-wrap:wrap;gap:18px}
footer nav{display:flex;gap:22px;flex-wrap:wrap}
footer a:hover{color:var(--text)}

/* home desk */
.desk{padding:40px 44px 30px}
.board{display:grid;grid-template-columns:repeat(6,1fr) 200px;margin-top:8px}
.board.mini3{grid-template-columns:repeat(3,1fr) 240px;margin-top:20px}
.board.mini3 .strip{height:480px}
summary{list-style:none}summary::-webkit-details-marker{display:none}
[hidden]{display:none!important}
.strip{position:relative;height:540px}
.strip .nm{position:absolute;left:20px;top:18px;display:flex;align-items:center;gap:8px}
.strip .nm i{width:6px;height:6px;border-radius:2px}
.strip .sub{position:absolute;left:20px;top:40px;font-size:10px}
.strip .fader{position:absolute;left:24px;top:84px;height:300px}
.strip .lm{position:absolute;left:100px;top:84px;height:300px;width:8px}
.strip .lm i{position:absolute;left:0;width:8px;height:24px;border-radius:2px;background:var(--led-off);transition:background .25s,box-shadow .25s}
.strip .lm i.on{background:rgb(var(--led-fine)/.95);box-shadow:0 0 8px rgb(var(--led-fine)/.25)}
.strip .lm i.near{background:rgb(var(--led-near));box-shadow:0 0 8px rgb(var(--led-near)/.6)}
.tag{position:absolute;left:104px;transform:translateX(-50%);padding:4px 7px;border-radius:6px;font:10px var(--mono);color:#fff;white-space:nowrap;background:rgba(255,181,71,.16);box-shadow:inset 0 0 0 1px rgba(255,181,71,.55);transition:top .3s,opacity .3s;opacity:0}
.strip .val{position:absolute;left:20px;top:404px;font:22px var(--mono);letter-spacing:-.02em}
.strip .share{position:absolute;left:20px;top:438px}
.strip .top{position:absolute;left:20px;top:464px;font:11px var(--mono);color:var(--label)}
.strip .top b{font-weight:400;color:var(--strong)}
.master{position:relative;padding:18px 0 0 22px}
.rrow{display:grid;grid-template-columns:14px 1fr 150px 120px 90px;gap:18px;align-items:center;padding:16px 0;border-top:1px solid var(--row-line)}
.rrow:first-child{border-top:0}
.rrow .n{font-size:15px;letter-spacing:-.01em;line-height:1.3}
.rrow .f{font:11px var(--mono);color:var(--label);margin-top:3px}
.rrow .a,.rrow .d{font:13px var(--mono);text-align:right}
.rrow .d{color:var(--label)}.rrow .d.near{color:rgb(var(--led-near))}.rrow .d.over{color:rgb(var(--led-over))}
.rrow .g{text-align:right}
.rrow.closed .n{color:var(--label)}
.rrow .x{grid-column:2/-1;display:none;color:var(--body);font-size:14px;line-height:1.6;padding-top:4px}
.rrow.xo .x{display:block}
.rrow .x .mbtn{margin-top:12px}
.empty{padding:22px 0;font:12px var(--mono);color:var(--label)}

/* scope (indicators) */
.scope{padding:24px 26px 22px}
.scope .screen{position:relative;height:150px;margin:18px 0 12px;border-radius:14px;background:#050506;box-shadow:var(--well-shadow);overflow:hidden;
  background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:100% 25%,10% 100%}
.scope svg{position:absolute;inset:10px 0;width:100%;height:calc(100% - 20px);overflow:visible}
.scope .readout{font:30px var(--mono);letter-spacing:-.02em}
.scope .readout small{font-size:12px;color:var(--label);margin-left:6px}
.scope p{color:var(--label);font-size:13px;line-height:1.55}
.notice{display:flex;gap:12px;align-items:center;padding:14px 20px;margin-bottom:20px;font:12px/1.5 var(--mono);color:var(--label)}

/* article */
.read{display:grid;grid-template-columns:1fr 280px;gap:20px;align-items:start}
.atile{padding:44px 56px 60px}
.atile h1{font-weight:300;font-size:50px;line-height:1.04;letter-spacing:-.035em;margin:18px 0 16px;max-width:20ch}
.banner{margin:28px -56px 10px;overflow:hidden}
.banner img{width:100%;max-height:460px;object-fit:cover;filter:grayscale(1) contrast(1.1) brightness(.85)}
.capt{font:11px var(--mono);color:var(--label);margin-bottom:34px}
.rside{position:sticky;top:20px;display:grid;gap:20px}
.secs a{display:flex;gap:12px;align-items:center;padding:11px 0;border-top:1px solid var(--row-line);font-size:14px;color:var(--label);transition:color .2s}
.secs a:first-child{border-top:0}
.secs a.on{color:var(--text)}
.secs a.on .led{background:rgb(var(--led-fine));box-shadow:0 0 8px rgb(var(--led-fine)/.5)}

/* switch (checklist) */
.tog{width:44px;height:24px;border-radius:99px;background:var(--well);box-shadow:var(--well-shadow);position:relative;flex:none;transition:background .2s}
.tog::after{content:"";position:absolute;left:3px;top:3px;width:18px;height:18px;border-radius:50%;background:var(--metal);box-shadow:0 2px 4px rgba(0,0,0,.6);transition:transform .25s cubic-bezier(.33,1,.68,1)}
.on > .tog,.tog.on{background:rgba(214,236,226,.25)}
.on > .tog::after,.tog.on::after{transform:translateX(20px)}
.chk{display:grid;grid-template-columns:40px 1fr 44px;gap:18px;align-items:start;padding:20px 0;border-top:1px solid var(--row-line);width:100%;text-align:left}
.chk:first-child{border-top:0}
.chk .no{font:11px var(--mono);color:var(--label);padding-top:3px}
.chk b{font-weight:400;font-size:17px;letter-spacing:-.01em}
.chk p{color:var(--label);font-size:14px;line-height:1.55;margin-top:6px}
.chk.on b{color:rgb(var(--led-fine))}

@media (max-width:1100px){
  .nav ul{display:none}.menu-btn{display:block}
  .nav ul.open{display:flex;flex-direction:column;position:absolute;top:84px;left:16px;right:16px;padding:20px;gap:16px;background:#141416;border-radius:20px;z-index:30;box-shadow:0 30px 60px rgba(0,0,0,.6)}
  .board,.board.mini3{grid-template-columns:repeat(3,1fr)}.master{grid-column:1/-1}
  .ph{grid-template-columns:1fr;gap:20px}
  .grid > *{grid-column:span 12}
  .read{grid-template-columns:1fr}.rside{position:static}
  .rrow{grid-template-columns:14px 1fr 110px 80px}.rrow .g{display:none}
}
@media (max-width:700px){
  .wrap{padding:0 16px}
  .ph h1{font-size:46px}
  .desk,.pad{padding:24px 20px}.rows{padding:6px 20px}
  .board,.board.mini3{grid-template-columns:repeat(2,1fr)}
  .feat{grid-template-columns:1fr;height:auto}.feat img{border-radius:var(--r) var(--r) 0 0;height:220px}
  .prow{grid-template-columns:1fr}.prow > .cap,.prow .go,.prow .meter{display:none}
  .rrow{grid-template-columns:14px 1fr 70px}.rrow .a{display:none}
  .atile{padding:28px 20px 40px}.atile h1{font-size:34px}.banner{margin:24px -20px 10px}
  .shead h2{font-size:36px}
  .gdesk{grid-template-columns:1fr!important}.gdesk > .vline{padding-left:0!important}.gdesk > .vline::before{display:none}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

JS = r"""
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
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500&family=Geist+Mono:wght@400&display=swap" rel="stylesheet">'
GRAIN = '<svg class="grain" aria-hidden="true"><filter id="gr"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#gr)"/></svg>'


def shell(page, body, scripts=""):
    active = SECTION.get(page, "")
    nav = "".join(f'<li><a href="{h}"{" class=on aria-current=page" if h == active else ""}>{t}</a></li>' for h, t in NAV)
    foot = "".join(f'<a class="cap" href="{h}">{t}</a>' for h, t in FOOT)
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(TITLES[page])} · e3 Initiative</title>{FONTS}<link rel="stylesheet" href="theme.css"></head>
<body>{GRAIN}
<a class="skip" href="#main">Skip to main content</a>
<div class="wrap">
  <header class="nav"><a class="brand" href="index.html"><i></i>e3 Initiative</a><nav aria-label="Main"><ul id="nav">{nav}</ul></nav>
    <button class="menu-btn cap" aria-controls="nav" aria-expanded="false">Menu</button></header>
  <main id="main">
{body}
  </main>
  <footer><span class="cap">© 2026 e3 Initiative</span><nav aria-label="Footer">{foot}</nav></footer>
</div>
<script src="theme.js"></script>
{scripts}
</body></html>
"""


def panel(inner, cls="", tag="div", attrs=""):
    return f'<{tag} class="panel {cls}" {attrs}><div class="sheen"></div>{inner}</{tag}>'


def ph(kicker, title, lede="", right=""):
    return f'<div class="ph"><div><div class="cap">{kicker}</div><h1>{title}</h1></div><div>{f"<p>{lede}</p>" if lede else ""}{right}</div></div>'


def meter(n, lit, near=0, cls=""):
    return f'<span class="meter {cls}" data-n="{n}" data-lit="{lit}" data-near="{near}"></span>'


def led_for(g):
    s, d = status(g), days_left(g)
    if s == "closed":
        return "over", "closed"
    if d is not None:
        return "near", f"in {d}d"
    return "on", s


def grow(g):
    cls, txt = led_for(g)
    return (f'<a class="rrow{" closed" if status(g) == "closed" else ""}" href="{g["link"]}" target="_blank" rel="noopener"><span class="led {cls}"></span>'
            f'<div><div class="n">{esc(g["name"])}</div><div class="f">{esc(g["funder"])}</div></div><span class="g cap">{CAT_LABEL[g["category"]]}</span>'
            f'<span class="a">{esc(money(g.get("amountMax")))}</span><span class="d {cls}">{txt}</span></a>')


def prow(p):
    return (f'<a class="prow" href="{p["slug"]}.html"><span class="cap">{p["short"]}</span><div><h3>{esc(p["title"])}</h3><p>{esc(p["summary"])}</p></div>'
            f'{meter(12, min(12, -(-p["min"] // 1)))}<span class="cap go">{p["min"]} min</span></a>')


# ——— pages ———
def home():
    """Nav, hero, one three-channel mixer, footer."""
    three = [("minority_owned", "Minority", "#f1f1f3"), ("women_owned", "Women", "#c6c6cb"), ("veteran_owned", "Veteran", "#8a8a90")]
    G = [[g["category"], g["name"], g["funder"].split(" (")[0], g.get("amountMax") or 0, days_left(g)] for g in OPEN if g["category"] in [a for a, _, _ in three]]
    body = ph("Equity · Economics · Ethnicity", f"{TAGLINE}<span>.</span>", "Student-led research on who builds local economies, who gets credit and who gets left out.",
              '<div style="margin-top:26px"><a class="mbtn" href="articles.html">Read the research</a></div>') + panel(f"""
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
    <div><div class="cap">Grant mixer</div><div style="font-size:30px;letter-spacing:-.02em;margin-top:10px">Find funding in seconds</div></div>
    <div style="text-align:right"><div class="cap">Matching</div><div class="mono" style="font-size:30px;letter-spacing:-.02em;margin-top:10px" id="tot">0</div></div>
  </div>
  <div class="board mini3" id="board">
    <div class="master vline">
      <div class="cap">Deadline window</div>
      <div class="knob" id="win" data-label="Deadline window" style="margin:22px auto 0"></div>
      <div style="text-align:center;margin-top:8px"><div style="font-size:24px;letter-spacing:-.02em" id="wl">Any time</div></div>
      <a class="mbtn" href="grants.html" style="margin-top:26px;width:100%;justify-content:center">See the grants</a>
    </div>
  </div>""", "desk")
    js = f"""<script>
const G = {json.dumps(G, ensure_ascii=False)}, CH = {json.dumps([{"id": a, "name": b, "shade": c} for a, b, c in three])};
const WIN = [[14, '14 days', '14D'], [30, '30 days', '30D'], [60, '60 days', '60D'], [Infinity, 'Any time', 'ANY']];
const money = v => v >= 1e6 ? '$' + (v / 1e6).toFixed(v % 1e6 ? 1 : 0) + 'M' : v >= 1000 ? '$' + Math.round(v / 1000) + 'k' : '$' + Math.round(v);
const valAt = p => p < .08 ? 0 : Math.pow(10, 3 + 3 * (p - .08) / .92), posOf = v => v <= 0 ? 0 : .08 + .92 * (Math.log10(v) - 3) / 3;
const mins = {{}}; let win = 3;
CH.forEach(c => {{ mins[c.id] = 0; const s = document.createElement('div'); s.className = 'strip vline';
  const tk = [[1, '1M'], [posOf(1e5), '100k'], [posOf(1e4), '10k'], [0, '0']].map(([p, l]) => `<span style="top:${{(1 - p) * 100}}%">${{l}}</span>`).join('');
  s.innerHTML = `<div class="nm cap"><i style="background:${{c.shade}}"></i>${{c.name}}-owned</div>
    <div class="fader"><div class="fticks">${{tk}}</div><div class="trk"><div class="fill"></div></div><div class="fcap" tabindex="0" role="slider" aria-label="Minimum award, ${{c.name}}-owned"></div></div>
    <div class="lm">${{Array.from({{ length: 10 }}, (_, k) => `<i style="top:${{300 - (k + 1) * 30 + 3}}px"></i>`).join('')}}</div><div class="tag"></div>
    <div class="val"></div><div class="share cap"></div>`;
  $('#board').insertBefore(s, $('.master')); c.el = s;
  makeFader($('.fader', s), 0, p => {{ mins[c.id] = valAt(p); render(); }}); }});
const knob = makeKnob($('#win'), WIN.map(w => w[2]), 3, i => {{ win = i; render(); }});
function render() {{ const W = WIN[win][0]; let M = 0;
  CH.forEach(c => {{ const hit = G.filter(g => g[0] === c.id && (!g[3] || g[3] >= mins[c.id]) && (g[4] === null || g[4] <= W)), dated = hit.filter(g => g[4] !== null).sort((a, b) => a[4] - b[4]);
    M += hit.length; const lit = hit.length * 2, amber = dated.length * 2, s = c.el;
    $$('.lm i', s).forEach((m, k) => m.className = k < lit ? (k >= lit - amber ? 'near' : 'on') : '');
    const tag = $('.tag', s); tag.style.opacity = dated.length ? 1 : 0; tag.textContent = dated.length ? dated[0][4] + 'd' : ''; tag.style.top = 84 + 300 - Math.max(lit, 1) * 30 - 30 + 'px';
    $('.val', s).textContent = mins[c.id] ? '≥' + money(mins[c.id]) : 'Any amount'; $('.share', s).textContent = hit.length + ' match'; }});
  $('#wl').textContent = WIN[win][1]; $('#tot').textContent = M; }}
render();
if (!reduce) setTimeout(() => knob.set(2), 900);
</script>"""
    return shell("index", body, js)

def pub_list(page, title, lede, items, extra=""):
    """Header and one index panel."""
    return shell(page, ph("Publications", title, lede) + panel('<div class="rows">' + "".join(prow(p) for p in items) + "</div>"))

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
    body.append(f'<p><a href="../../{cite}">Citations and sources →</a></p>')
    inner = f"""<div class="cap">{p["kind"]} · {p["date"]} · {p["min"]} min</div><h1>{esc(p["title"])}</h1><div class="cap" style="letter-spacing:.1em">{esc(a["byline"] or "By " + p["author"])}</div>
    <div class="banner"><img src="{IMG}{p["img"].replace("-640", "")}" alt="{esc(p["alt"])}"></div><div class="capt">{esc(a["caption"] or p["alt"])}</div>
    <div class="prose" id="prose">{"".join(body)}</div>"""
    body_html = f"""<style>.topbar{{position:fixed;left:0;right:0;top:0;height:3px;z-index:70}}.topbar b{{display:block;height:100%;width:0;background:rgb(var(--led-fine));box-shadow:0 0 8px rgb(var(--led-fine)/.6)}}</style>
<div class="topbar"><b id="rb"></b></div>
<div style="margin-top:40px;max-width:860px;margin-left:auto;margin-right:auto">{panel(inner, "atile", "article")}</div>"""
    js = """<script>
const pr = $('#prose');
function upd() { const r = pr.getBoundingClientRect(), k = Math.max(0, Math.min(1, (innerHeight * .4 - r.top) / r.height)); $('#rb').style.width = k * 100 + '%'; }
addEventListener('scroll', upd, { passive: true }); upd();
</script>"""
    return shell(p["slug"], body_html, js)

def about():
    """Header, one statement, three people."""
    team = panel('<div class="rows">' + "".join(f'<div class="mrow" style="display:block;border:0;border-top:1px solid var(--row-line);padding:22px 0"><div style="display:flex;gap:18px;align-items:baseline;flex-wrap:wrap"><span class="cap">0{i+1}</span><b style="font:20px var(--sans);letter-spacing:-.01em">{n}</b><span class="cap" style="margin-left:auto">{r}</span></div><p class="dim" style="font-size:14px;line-height:1.6;margin:8px 0 0 40px;max-width:70ch">{b}</p></div>' for i, (n, r, b) in enumerate(ABOUT["team"])) + "</div>", "", attrs='style="margin-top:20px"')
    body = ph("About", "About e3 Initiative", ABOUT["what"]) + panel(f'<p style="font-weight:300;font-size:26px;line-height:1.35;letter-spacing:-.02em;max-width:48ch">{ABOUT["who"]}</p>', "pad") + team + '<p class="cap" style="margin-top:22px;line-height:1.8;max-width:80ch">We believe in community voices, cross-sector collaboration, and turning findings into stories of economic resilience.</p>'
    return shell("about", body)

def journals():
    t, logo = JOURNAL
    body = ph("Publications", "Journals", "Browse our academic journals and long-form publications.") + panel(f"""
  <div style="display:flex;gap:34px;align-items:center;flex-wrap:wrap"><div style="border-radius:20px;background:var(--well);box-shadow:var(--well-shadow);padding:22px"><img src="{IMG}{logo}" alt="{esc(t)}" width="150" height="150" style="border-radius:12px"></div>
  <div><div class="cap">Journal</div><div style="font-weight:300;font-size:34px;letter-spacing:-.03em;line-height:1.1;margin-top:12px;max-width:20ch">{t}</div><div class="cap" style="margin-top:14px">Entries coming soon</div></div></div>""", "pad")
    return shell("journals", body)

def grants():
    """Header, one desk (search, status, knob; the rest folded), results."""
    cats = "".join(f'<button class="key" data-v="{k}">{v}</button>' for k, v in CAT_LABEL.items())
    lists = " · ".join(f'<a href="{s}.html" style="color:var(--text)">{CAT_LABEL[c]}</a>' for s, (c, _, _) in CATEGORY_PAGES.items())
    body = ph("Grants", "Grant Finder", f"Funding for small businesses and nonprofits. Ready-made lists: {lists}.", '<a class="mbtn ghost" href="grant-help.html" style="margin-top:20px">Help & tips →</a>') + panel(f"""
  <div style="display:grid;grid-template-columns:1fr 190px;gap:34px" class="gdesk">
    <div>
      <label class="field"><span class="cap">Search</span><input class="inp" id="q" type="search" placeholder="WOMEN-OWNED BAKERY…" aria-label="Search grants"></label>
      <div class="keys" data-group="status"><button class="key on" data-v="live">Open + rolling</button><button class="key" data-v="">Include closed</button></div>
      <details style="margin-top:18px"><summary class="cap" style="cursor:pointer">+ More filters</summary>
        <div class="cap" style="margin:14px 0 10px">Who qualifies</div><div class="keys" data-group="elig"><button class="key on" data-v="">Anyone</button><button class="key" data-v="small_business">Business</button><button class="key" data-v="nonprofit">Nonprofit</button></div>
        <div class="cap" style="margin:14px 0 10px">Category</div><div class="keys" data-group="cat" data-multi>{cats}</div></details>
    </div>
    <div class="vline" style="padding-left:24px"><div class="cap">Deadline window</div><div class="knob" id="win" data-label="Deadline window" style="margin:14px auto 0"></div>
      <div class="mrow cap" style="margin-top:14px">Matching<b id="mM">—</b></div></div>
  </div>""", "desk") + panel('<div class="rows" id="gres" aria-live="polite"></div>', "", attrs='style="margin-top:20px"')
    js = """<script src="../shared/grants-data.js"></script><script>
const F = { q: '', elig: '', status: 'live', cat: new Set(), win: 3 }, WIN = [[14, '14D'], [30, '30D'], [90, '90D'], [Infinity, 'ANY']];
makeKnob($('#win'), WIN.map(w => w[1]), 3, i => { F.win = i; render(); });
$$('.keys[data-group]').forEach(g => g.addEventListener('change', () => { const on = $$('.key.on', g).map(k => k.dataset.v);
  if (g.dataset.group === 'cat') F.cat = new Set(on); else F[g.dataset.group] = on[0] ?? ''; render(); }));
$('#q').addEventListener('input', e => { F.q = e.target.value.toLowerCase(); render(); });
function render() { const W = WIN[F.win][0];
  const rs = GRANTS.filter(g => (!F.q || (g.name + g.funder + g.desc + CAT_LABEL[g.cat]).toLowerCase().includes(F.q)) && (!F.elig || g.elig === F.elig || g.elig === 'both')
    && (F.status === '' || g.status !== 'closed') && (!F.cat.size || F.cat.has(g.cat)) && (W === Infinity || (g.days != null && g.days <= W && g.days >= 0)))
    .sort((a, b) => ({ open: 0, rolling: 1, closed: 2 }[a.status] - { open: 0, rolling: 1, closed: 2 }[b.status]) || (a.days ?? 999) - (b.days ?? 999));
  $('#mM').textContent = rs.length;
  $('#gres').innerHTML = rs.length ? rs.map(g => { const c = g.status === 'closed' ? 'over' : g.days != null ? 'near' : 'on';
    return `<div class="rrow ${g.status === 'closed' ? 'closed' : ''}" tabindex="0" style="cursor:pointer;grid-template-columns:14px 1fr 130px 90px"><span class="led ${c}"></span><div><div class="n">${g.name}</div><div class="f">${g.funder}</div></div>
      <span class="a">${g.max ? '$' + g.max.toLocaleString() : 'varies'}</span><span class="d ${c}">${g.status === 'closed' ? 'closed' : g.days != null ? 'in ' + g.days + 'd' : g.dl.toLowerCase()}</span>
      <div class="x">${g.desc}<br><a class="mbtn sm" href="${g.link}" target="_blank" rel="noopener">Funder's page →</a></div></div>`; }).join('')
    : '<div class="empty">Nothing matches. Widen the window or clear the search.</div>'; }
$('#gres').addEventListener('click', e => { const r = e.target.closest('.rrow'); if (r && !e.target.closest('a')) r.classList.toggle('xo'); });
$('#gres').addEventListener('keydown', e => { if (e.key === 'Enter' && e.target.classList.contains('rrow')) e.target.classList.toggle('xo'); });
render();
</script>"""
    return shell("grants", body, js)

def category(slug):
    """Header and one list."""
    cat, title, what = CATEGORY_PAGES[slug]
    intro, gs = category_intro(cat, what)
    gs = sorted(gs, key=lambda g: ({"open": 0, "rolling": 1, "closed": 2}[status(g)], days_left(g) if days_left(g) is not None else 999))
    others = " · ".join(f'<a href="{s}.html" style="color:var(--text)">{CAT_LABEL[v[0]]}</a>' for s, v in CATEGORY_PAGES.items() if s != slug)
    body = ph("Grant list", title, intro) + panel('<div class="rows">' + "".join(grow(g) for g in gs) + "</div>") + f'<p class="cap" style="margin-top:22px">More lists · {others} · <a href="grants.html" style="color:var(--text)">Search all {len(GRANTS)}</a></p>'
    return shell(slug, body)

def grant_help():
    """Header, one checklist. Mistakes and the directory are folded away."""
    tips = "".join(f'<button class="chk" data-i="{i}"><span class="no">0{i+1}</span><div><b>{a}</b><p>{b}</p></div><span class="tog"></span></button>' for i, (a, b) in enumerate(HELP["tips"]))
    mistakes = '<details style="padding:18px 0 0;border-top:1px solid var(--row-line)"><summary class="cap" style="cursor:pointer">+ Common mistakes to avoid</summary>' + "".join(f'<div class="mrow" style="justify-content:flex-start;gap:14px;align-items:flex-start;border:0;padding:8px 0"><span class="led over" style="margin-top:6px"></span><span style="font-size:14px;line-height:1.5;color:var(--body)">{m}</span></div>' for m in HELP["mistakes"]) + "</details>"
    orgs = "".join(f'<a class="rrow" href="{u}" target="_blank" rel="noopener" style="grid-template-columns:14px 1fr 170px"><span class="led on"></span><div><div class="n">{n}</div><div class="f" style="font-family:var(--sans);font-size:13px;line-height:1.5">{d}</div></div><span class="cap" style="text-align:right">{l} →</span></a>' for n, d, l, u in HELP["orgs"])
    directory = f'<details style="padding:18px 0 0;border-top:1px solid var(--row-line);margin-top:14px"><summary class="cap" style="cursor:pointer">+ Where to get free help</summary><div style="margin-top:8px">{orgs}</div><p class="dim mono" style="font-size:11px;line-height:1.7;margin-top:14px;max-width:90ch">{HELP["disclaimer"]}</p></details>'
    body = ph("Grants", "Grant Help & Tips", HELP["intro"], '<a class="mbtn" href="grants.html" style="margin-top:20px">Search grants →</a>') + panel('<div class="cap" style="margin-bottom:6px">How to write a strong application · <span id="hc">0/8</span> done</div>' + tips + mistakes + directory, "pad")
    js = """<script>
const done = new Set(JSON.parse(localStorage.getItem('e3-help') || '[]'));
function upd() { $$('.chk').forEach(c => c.classList.toggle('on', done.has(+c.dataset.i))); $('#hc').textContent = done.size + '/8'; localStorage.setItem('e3-help', JSON.stringify([...done])); }
$$('.chk').forEach(c => c.addEventListener('click', () => { const i = +c.dataset.i; done.has(i) ? done.delete(i) : done.add(i); upd(); })); upd();
</script>"""
    return shell("grant-help", body, js)

def indicators():
    """Header with range knob, four key scopes, the other four behind one button."""
    def scope(k, grp, name, u, d, extra):
        return panel(f"""<div style="display:flex;justify-content:space-between;align-items:center"><span class="cap">{grp} · {name}</span><span class="led" data-led></span></div>
      <div class="screen"><svg viewBox="0 0 500 130" preserveAspectRatio="none" aria-hidden="true"></svg></div>
      <div style="display:flex;justify-content:space-between;align-items:baseline;gap:12px"><div class="readout"><span data-v>— —</span><small>{u}</small></div><span class="cap" data-yr></span></div>
      <p style="margin-top:10px">{d}</p>""", f"scope c6{extra}", attrs=f'data-key="{k}" data-unit="{u}"')
    key = [i for i in INDICATORS if i[0] in KEY_INDICATORS]
    more = [i for i in INDICATORS if i[0] not in KEY_INDICATORS]
    body = ph("Data", "Economic Indicators", "Everyday costs, job security and borrowing rates. Turn the knob to change the range; hover a screen to read any year.",
              '<div style="display:flex;align-items:center;gap:24px;margin-top:18px"><div class="knob" id="rng" data-label="Time range"></div><div class="mono" style="font-size:22px" id="rngl">2000 →</div></div>') + f"""
{panel('<span class="led near"></span><span>Preview: placeholder traces. Live FRED data loads from /api/economic-indicators on the deployed site.</span>', "notice", attrs='id="note" hidden')}
<div class="grid">{''.join(scope(*i, '') for i in key)}{''.join(scope(*i, ' more') for i in more)}</div>
<div style="text-align:center;margin-top:24px"><button class="mbtn ghost" onclick="document.querySelectorAll('.scope.more').forEach(e=>e.hidden=false);this.remove()">Show all 8 indicators</button></div>"""
    js = """<script src="../shared/indicators.js"></script><script>
$$('.scope.more').forEach(e => e.hidden = true);
let D, from = 0; const STARTS = [2000, 2008, 2016, 2020];
makeKnob($('#rng'), STARTS.map(String), 0, i => { from = i; draw(); });
function draw() { if (!D) return; const y0 = STARTS[from]; $('#rngl').textContent = y0 + ' →';
  $$('.scope').forEach(t => { const all = D.series[t.dataset.key]; if (!all) return; const i0 = Math.max(0, D.years.indexOf(y0)), s = all.slice(i0), yrs = D.years.slice(i0), n = s.length;
    const lo = Math.min(...s), hi = Math.max(...s), x = i => i / (n - 1) * 500, y = v => 120 - (v - lo) / (hi - lo || 1) * 110, svg = $('svg', t);
    const d = s.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1)).join(' ');
    svg.innerHTML = `<path d="${d}" fill="none" stroke="rgba(214,236,226,.25)" stroke-width="6" vector-effect="non-scaling-stroke" style="filter:blur(3px)"/>
      <path d="${d}" fill="none" stroke="rgb(214,236,226)" stroke-width="1.6" vector-effect="non-scaling-stroke" ${D.live ? '' : 'stroke-dasharray="4 4"'}/>
      <line class="cur" x1="${x(n - 1)}" x2="${x(n - 1)}" y1="0" y2="130" stroke="rgba(255,181,71,.6)" vector-effect="non-scaling-stroke"/>`;
    const u = t.dataset.unit, show = i => { $('[data-v]', t).textContent = D.live ? fmtIndicator(s[i], u).replace(/[%M]/g, '') : '— —'; $('[data-yr]', t).textContent = yrs[i]; $('.cur', svg).setAttribute('x1', x(i)); $('.cur', svg).setAttribute('x2', x(i)); };
    show(n - 1); $('[data-led]', t).className = 'led ' + (D.live ? 'on' : 'near');
    svg.onpointermove = e => { const r = svg.getBoundingClientRect(); show(Math.round((e.clientX - r.left) / r.width * (n - 1))); }; svg.onpointerleave = () => show(n - 1); }); }
loadIndicators().then(d => { D = d; $('#note').hidden = d.live; draw(); });
</script>"""
    return shell("economic-indicators", body, js)

def outreach():
    cards = "".join(panel(f"""<div class="cap">{t}</div>
      <p style="font-weight:300;font-size:26px;line-height:1.3;letter-spacing:-.02em;margin:22px 0 16px">{p1}</p><p class="dim" style="font-size:14px;line-height:1.6">{p2}</p>
      <a class="mbtn" href="contact.html" style="margin-top:26px">{'Share your story' if k == 'interview' else 'Partner with us'} →</a>""", "pad c6", attrs=f'id="{k}"') for k, (t, s, p1, p2) in OUTREACH.items())
    return shell("outreach", ph("Outreach", "Outreach", "Interviews and partnerships: how community knowledge gets into our research.") + f'<div class="grid">{cards}</div>')

def contact():
    """Header and the form."""
    form = """<form onsubmit="event.preventDefault();this.querySelector('[data-sent]').hidden=false" id="cf">
      <div class="grid" style="gap:0 18px"><label class="field c6"><span><span class="led" data-for="n"></span><span class="cap">Name *</span></span><input class="inp" id="n" required autocomplete="name"></label>
      <label class="field c6"><span><span class="led" data-for="e"></span><span class="cap">Email *</span></span><input class="inp" id="e" type="email" required autocomplete="email"></label></div>
      <label class="field"><span><span class="led" data-for="s"></span><span class="cap">Subject *</span></span><input class="inp" id="s" required></label>
      <label class="field"><span><span class="led" data-for="m"></span><span class="cap">Message *</span></span><textarea class="inp" id="m" required></textarea></label>
      <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap"><button class="mbtn" type="submit">Send message</button><span class="cap" data-sent hidden style="color:rgb(var(--led-near))">Mockup: nothing was sent</span></div></form>"""
    body = ph("Contact", "Let's connect", "Have questions about our research or want to collaborate? Send a message and we will respond within two business days. We use your details only to reply.") + f'<div style="max-width:780px">{panel(form, "pad")}</div>'
    js = """<script>
function chk() { ['n', 'e', 's', 'm'].forEach(id => { const v = $('#' + id).checkValidity() && $('#' + id).value; $(`[data-for=${id}]`).className = 'led' + (v ? ' on' : ''); }); }
$('#cf').addEventListener('input', chk);
</script>"""
    return shell("contact", body, js)

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
    body = ph("Legal", "Privacy Policy", "The e3 Initiative is a small research organization. This page explains what information this website collects, why, and the choices you have.", '<div class="cap" style="margin-top:14px">Last updated · Nov 12 2026</div>') + f'<div style="max-width:860px">{panel("<div class=prose>" + "".join(out) + "</div>", "atile", "article")}</div>'
    return shell("privacy", body)

def notfound():
    body = f"""<div style="margin-top:60px">{panel(f'''<div style="display:flex;justify-content:space-between"><span class="cap">Page not found</span><span class="led over"></span></div>
  <div style="display:flex;gap:40px;align-items:center;margin:40px 0;flex-wrap:wrap"><div class="mono" style="font-size:150px;letter-spacing:-.04em;line-height:1">404</div>
  <div style="display:flex;gap:6px">{"".join(f'<span class="meter v" data-n="14" data-lit="0"></span>' for _ in range(6))}</div><div class="cap" style="color:rgb(var(--led-over))">No signal</div></div>
  <p class="dim" style="max-width:46ch;margin-bottom:26px">Sorry, we couldn't find that page. It may have moved, or the link may be mistyped.</p>
  <div style="display:flex;gap:10px;flex-wrap:wrap"><a class="mbtn" href="index.html">Homepage</a><a class="mbtn ghost" href="articles.html">Articles</a><a class="mbtn ghost" href="research.html">Research</a><a class="mbtn ghost" href="contact.html">Contact</a></div>''', "desk")}</div>"""
    return shell("404", body)


def build():
    write(f"{D}/theme.css", CSS + NOB)
    write(f"{D}/theme.js", JS)
    pages = {"index": home(), "about": about(), "journals": journals(), "grants": grants(), "grant-help": grant_help(),
             "economic-indicators": indicators(), "outreach": outreach(), "contact": contact(), "privacy": privacy(), "404": notfound(),
             "articles": pub_list("articles", "Publications", "Articles and research papers from our team and partners, from grassroots history to systemic policy analysis.", PUBS),
             "research": pub_list("research", "Research", "Research papers, reports, and briefs, each with clear summaries and next steps for community leaders and decision-makers.", RESEARCH,
                 '<section class="grid">' + panel('<div class="cap">Journals</div><p style="font-weight:300;font-size:24px;letter-spacing:-.02em;margin-top:12px">Critical Debates in Humanities, Science and Global Justice →</p>', "pad c6", "a", 'href="journals.html"') + panel('<div class="cap">Data</div><p style="font-weight:300;font-size:24px;letter-spacing:-.02em;margin-top:12px">Economic indicators since 2000 →</p>', "pad c6", "a", 'href="economic-indicators.html"') + '</section>')}
    for p in PUBS:
        pages[p["slug"]] = article(p)
    for s in CATEGORY_PAGES:
        pages[s] = category(s)
    for k, v in pages.items():
        write(f"{D}/{k}.html", v)
    return sorted(pages)

# NOBORDERS
NOB = r"""
/* no borders */
:root{--r:22px}
.panel::after{display:none}
.panel::before{box-shadow:0 30px 60px -40px rgba(0,0,0,.85)}
.nav{border-bottom:0}
footer{border-top:0}
.rrow,.prow,.chk,.secs a,details{border-top:0!important}
.mrow{border:0!important}
.strip + .strip::before,.master::before,.vline + .vline::before,.lens + .lens::before{display:none}
.mbtn.ghost{box-shadow:none;background:rgba(255,255,255,.07)}
.key{box-shadow:0 4px 10px rgba(0,0,0,.5)}
.inp{box-shadow:none;background:#0b0b0d}
.inp:focus{box-shadow:none;background:#111114}
.tog{box-shadow:none}
.brand i,.fcap,.mbtn{box-shadow:0 6px 14px rgba(0,0,0,.5)}
.mbtn.ghost{box-shadow:none}
"""
