"""Variation A: Paper widgets. Warm paper, white tiles, thin Geist numerals, mono captions, one ultramarine accent.
Every page is built from the paper-widgets components: tiles with dot labels, calendar rows, tick dials, level bars,
the now-playing player and the focus switch (here: reading mode, saved across pages)."""
from common import *

D = "site-d"

CSS = r"""
:root{
  --bg:#dde0e3; --tile:#f3f4f5; --ink:#101318; --ink-rgb:16 19 24; --muted:#79808a; --accent:#00a06a; --peach:#ffc42e;
  --line:rgba(16,19,24,.08); --wash:rgba(16,19,24,.05); --track:rgba(16,19,24,.07); --hair:rgba(16,19,24,.13);
  --marker:rgba(16,19,24,.14); --dotted:rgba(16,19,24,.16); --sun-glow:rgba(0,160,106,.16);
  --sans:"Geist",system-ui,sans-serif; --mono:"Geist Mono",monospace; --label-font:400 14px "Inter",system-ui,sans-serif;
  --r:38px; --cell:292px; --gap:20px;
  --shadow:0 0 0 1px rgba(16,19,24,.04), inset 0 1px 0 #fff, 0 28px 46px -30px rgba(20,28,40,.38), 0 2px 4px rgba(20,28,40,.05);
  --focus-dark:radial-gradient(260px 220px at 75% 15%, rgba(0,160,106,.5), transparent 70%), #0e1218;
  --sky:linear-gradient(180deg,#cfd6dd 0%,#eceff1 70%,#f6efe3 100%); --far:#c2c9d1; --near:#a5aeb8; --front:#10151c; --win:#ffc42e; --winoff:rgba(255,255,255,.45);
}
html.night{--bg:#07090d;--tile:#10141b;--ink:#f1f3f5;--ink-rgb:241 243 245;--muted:#838b96;--line:rgba(255,255,255,.07);--wash:rgba(255,255,255,.06);--track:rgba(255,255,255,.08);--hair:rgba(255,255,255,.14);--marker:rgba(255,255,255,.16);--dotted:rgba(255,255,255,.2);
  --shadow:0 0 0 1px rgba(255,255,255,.04), inset 0 1px 0 rgba(255,255,255,.05), 0 28px 46px -30px rgba(0,0,0,.85);
  --sky:linear-gradient(180deg,#0b1020 0%,#121a2e 62%,#2a2438 100%); --far:#141b2c; --near:#0d121e; --front:#06080c; --win:#ffcf6b; --winoff:rgba(255,255,255,.05)}
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
.pill-nav a{display:block;padding:9px 15px;border-radius:99px;font:500 14px/1.2 var(--sans);letter-spacing:.002em;color:var(--muted);white-space:nowrap;transition:color .2s}
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
.label{display:flex;align-items:center;gap:8px;font:600 11.5px/1.2 var(--sans);letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.label i{width:6px;height:6px;border-radius:50%;background:var(--accent);flex:none}
.tile > .label.abs{position:absolute;left:26px;top:22px}
.tr{position:absolute;right:26px;top:22px;font-size:13px;color:var(--muted)}
.mono{font-family:var(--mono)}
.muted{color:var(--muted)}
.thin{font-weight:300;letter-spacing:-.02em;line-height:1}
.chip{display:inline-flex;align-items:center;font:500 11px/1 var(--mono);letter-spacing:.04em;text-transform:uppercase;padding:5px 9px;border-radius:99px;background:var(--wash);color:var(--muted);white-space:nowrap}
.chip.a{background:var(--accent);color:#fff}
.chip.ink{background:var(--ink);color:var(--tile)}
.btn{display:inline-flex;align-items:center;gap:8px;height:46px;padding:0 20px;border-radius:99px;font:500 14.5px/1 var(--sans);letter-spacing:.005em;background:var(--ink);color:var(--tile);transition:transform .15s;white-space:nowrap}
.btn.ghost{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px var(--hair)}
.btn.sm{height:34px;padding:0 14px;font:500 11px/1 var(--mono);letter-spacing:.04em;text-transform:uppercase}
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
.shead a{font:500 14px var(--sans);color:var(--muted)}.shead a:hover{color:var(--ink)}

/* calendar rows: the list primitive */
.rows{padding:8px 26px}
.crow{display:grid;grid-template-columns:74px 3px 1fr auto;gap:16px;align-items:center;padding:18px 0;border-top:1px solid var(--line)}
.crow:first-child{border-top:0}
.crow .t{font:500 12px/1.2 var(--mono);letter-spacing:.02em;color:var(--muted)}
.crow .m{height:36px;border-radius:2px;background:var(--marker);transition:background .2s}
.crow.next .m,.crow:hover .m{background:var(--accent)}
.crow .n{font-size:16.5px;font-weight:500;letter-spacing:-.011em;line-height:1.3}
.crow .d{font-size:13.5px;color:var(--muted);margin-top:3px;line-height:1.4}

/* covers (now-playing art), used for every publication */
.cover{position:relative;border-radius:24px;overflow:hidden;aspect-ratio:1;flex:none}
.cv-a{background:var(--accent)}.cv-a::before{content:"";position:absolute;right:-22%;top:-16%;width:76%;height:76%;border-radius:50%;background:var(--peach)}
.cv-a::after{content:"";position:absolute;left:9%;bottom:12%;width:48%;height:2px;background:#fff;opacity:.85}
.cv-b{background:#e6e0d2}.cv-b::before{content:"";position:absolute;left:10%;top:12%;width:60%;height:60%;border-radius:50%;background:#141416}
.cv-b::after{content:"";position:absolute;right:12%;bottom:12%;width:15%;height:15%;border-radius:6px;background:var(--accent)}
.cv-c{background:#141416}.cv-c::before{content:"";position:absolute;left:38%;top:16%;width:60%;height:60%;border-radius:50%;border:2px solid var(--peach)}
.cv-c::after{content:"";position:absolute;left:25%;top:44%;width:26%;height:26%;border-radius:50%;background:var(--accent)}
.cover .mk{position:absolute;left:9%;bottom:17%;font:10px var(--mono);letter-spacing:1px;color:#fff;z-index:1}
.cv-b .mk{color:#141416;bottom:9%}
.cover.photo img{width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.05)}

/* level bars (batteries) */
.lvl{display:grid;grid-template-columns:36px 1fr auto;gap:4px 12px;align-items:center;padding:12px 0}
.lvl .well{grid-row:span 2}
.lvl .nm{font-size:14.5px}
.lvl .pc{font:12.5px var(--mono)}
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
.field span{display:flex;align-items:center;gap:8px;font:600 11.5px/1.2 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
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
footer .links{display:flex;gap:18px;flex-wrap:wrap;font:500 13.5px var(--sans);color:var(--muted)}
footer .links a:hover{color:var(--ink)}

/* ——— home widgets ——— */
.home{display:grid;grid-template-columns:repeat(4,var(--cell));grid-auto-rows:var(--cell);gap:var(--gap)}
.home .rows .crow{padding:13px 0}.home .rows .crow .m{height:28px}
.home .tile{height:100%}
.w2{grid-column:span 2}
.hero{grid-column:span 2;display:flex;flex-direction:column;justify-content:space-between;padding:4px 8px 4px 0}
.hero h1{font-weight:300;font-size:clamp(3rem,2rem + 4vw,4.1rem);line-height:.96;letter-spacing:-.022em}
.hero h1 span{font-style:italic;font-variation-settings:"opsz" 144,"SOFT" 100,"WONK" 1}
.hero h1 span{color:var(--accent)}
.hero p{font-size:15px;line-height:1.5;color:var(--muted);max-width:46ch;margin-bottom:16px}
.cta{display:flex;gap:8px;flex-wrap:wrap}
.player .pcov{position:absolute;left:24px;top:24px;width:248px;height:248px;border-radius:24px;overflow:hidden}
.player .art{position:absolute;inset:0;transition:transform .5s cubic-bezier(.65,0,.35,1),opacity .5s;border-radius:0}
.player .label.abs{left:300px}
.eq{position:absolute;left:426px;top:24px;width:30px;height:14px}
.eq b{position:absolute;bottom:0;width:3px;border-radius:2px;background:var(--accent);height:3px}
.ttl{position:absolute;left:300px;top:64px;right:26px;font-size:25px;font-weight:350;letter-spacing:-.02em;line-height:1.1;transition:opacity .15s}
.by{position:absolute;left:301px;top:132px;font-size:14px;color:var(--muted);transition:opacity .15s}
.prog{position:absolute;left:300px;top:186px;width:288px;height:5px;border-radius:99px;background:var(--track);overflow:hidden}
.prog .f{position:absolute;inset:0 auto 0 0;border-radius:99px;background:var(--ink);width:0}
.knob{position:absolute;top:181px;width:15px;height:15px;margin-left:-7px;border-radius:50%;background:#fff;box-shadow:0 0 0 1px var(--hair),0 2px 6px rgba(0,0,0,.15);left:300px}
.times{position:absolute;top:202px;font:11px/1 var(--mono);color:var(--muted)}
.ctl{position:absolute;top:232px;width:40px;height:40px;display:grid;place-items:center;border-radius:50%;transition:transform .15s,background .15s}
.ctl:active{transform:scale(.88);background:rgb(var(--ink-rgb)/.07)}
.play{position:absolute;left:420px;top:226px;width:52px;height:52px;display:grid;place-items:center;border-radius:50%;background:var(--ink);color:var(--tile)}
.cal .day{position:absolute;left:20px;top:64px;font-size:150px;font-weight:250;letter-spacing:-.04em;line-height:1}
.cal .month{position:absolute;left:28px;top:222px;font:500 17px var(--sans);letter-spacing:-.01em}
.cal .sum{position:absolute;left:28px;top:246px;font-size:13px;color:var(--muted)}
.cal .div{position:absolute;left:262px;top:28px;bottom:28px;width:1px;background:var(--line)}
.list{position:absolute;left:290px;top:34px;width:296px;height:232px;overflow:hidden}
.row{position:absolute;left:0;right:0;height:56px;display:flex;align-items:center;gap:14px;transition:top .6s cubic-bezier(.65,0,.35,1),opacity .6s}
.row .t{font:500 12px/1.2 var(--mono);color:var(--muted);width:46px;flex:none}
.row .m{width:3px;height:30px;border-radius:2px;background:var(--marker);flex:none;transition:background .3s}
.row.next .m{background:var(--accent)}
.row .n,.row .d{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:126px}
.row .n{font-size:15px;font-weight:500;letter-spacing:-.01em}
.row .d{font-size:12px;color:var(--muted);margin-top:2px}
.list .chip{position:absolute;right:0;top:16px;transition:opacity .2s}
.dialw{position:absolute;left:46px;top:56px}
.digits{position:absolute;left:46px;top:124px;width:200px;text-align:center;font-size:44px;font-weight:300;letter-spacing:-.022em}
.digits small{font-size:18px;letter-spacing:0;color:var(--muted)}
.dcap{position:absolute;left:46px;top:178px;width:200px;text-align:center;font-size:13px;color:var(--muted)}
.focus .dark{position:absolute;inset:0;background:var(--focus-dark);opacity:0;transition:opacity .45s}
html.night .focus .dark{opacity:1}
html.night .focus{color:#f4f3f0}
.moon{position:absolute;left:24px;top:70px;transition:transform .45s,background .45s}
html.night .focus .moon{background:rgba(255,255,255,.1);transform:rotate(-40deg)}
.state{position:absolute;left:26px;top:160px;font-size:32px;font-weight:300;letter-spacing:-.018em}
.cap2{position:absolute;left:27px;top:200px;font-size:13px;color:var(--muted)}
.sw{position:absolute;left:26px;top:238px;width:60px;height:34px;border-radius:99px;background:var(--hair);transition:background .3s,transform .15s}
html.night .focus .sw{background:var(--accent)}
.sw b{position:absolute;left:3px;top:3px;width:28px;height:28px;border-radius:50%;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.2);transition:transform .3s cubic-bezier(.33,1,.68,1)}
html.night .focus .sw b{transform:translateX(26px)}
.big{position:absolute;left:22px;top:58px;font-size:92px;font-weight:250;letter-spacing:-.03em;line-height:1}
.sky{position:absolute;left:27px;top:160px;font-size:15px}
.arcbox{position:absolute;left:24px;top:182px;overflow:visible}
.arcbox .dotted{fill:none;stroke:var(--dotted)}.arcbox .hz{stroke:var(--hair)}
.arcbox .lit{fill:none;stroke:var(--accent);stroke-linecap:round}.arcbox .pub{fill:var(--tile);stroke:var(--ink);stroke-width:1.5}
.tiny{position:absolute;top:268px;font:10.5px/1 var(--mono);color:var(--muted)}
.cnt{position:absolute;left:24px;top:58px;font-size:56px;font-weight:300;letter-spacing:-.022em;line-height:1}
.goal{position:absolute;left:27px;top:118px;font-size:13px;color:var(--muted)}
.col{position:absolute;top:0}
.col .e,.col .b{position:absolute;left:0;top:166px;width:22px;height:90px;border-radius:7px}
.col .e{background:var(--wash)}
.col .b{background:var(--ink);opacity:.85;transform-origin:bottom;transform:scaleY(0);transition:transform .6s cubic-bezier(.34,1.56,.64,1)}
.col .b.hl{background:var(--accent);opacity:1}
.col .l{position:absolute;left:-6px;top:264px;width:34px;text-align:center;font:10.5px/1 var(--mono);color:var(--muted)}
.devs{position:absolute;left:24px;right:26px;top:60px}
.share .h{position:absolute;left:26px;top:160px;font-size:30px;font-weight:300;letter-spacing:-.018em;line-height:1.05}
.share .s{position:absolute;left:27px;top:200px;font-size:13px;color:var(--muted);right:24px}
.share .go{position:absolute;left:26px;top:238px}
.share .well{position:absolute;left:24px;top:70px}
.mission{display:grid;grid-template-columns:var(--cell) 1fr;gap:var(--gap)}
.mission p{font-weight:300;font-size:var(--s4);line-height:1.1;letter-spacing:-.018em;max-width:24ch}
.mission p span{color:var(--muted)}

/* publication cards */
.pubcard{display:grid;grid-template-columns:200px 1fr;gap:26px;padding:24px;align-items:center}
.pubcard h3{font-weight:360;font-size:var(--s2);letter-spacing:-.02em;line-height:1.12;margin:12px 0 8px}
.pubcard p{color:var(--muted);font-size:14.5px;line-height:1.5}
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
.toc .crow .n{font-size:14px;font-weight:450}
.atile{padding:30px 44px 50px}
.atile h1{font-weight:300;font-size:var(--s4);line-height:1.02;letter-spacing:-.018em;margin:18px 0 20px;max-width:18ch}
.banner{border-radius:24px;overflow:hidden;margin:26px 0 8px}
.banner img{width:100%;max-height:440px;object-fit:cover;filter:grayscale(1) contrast(1.05)}
.capt{font:12.5px/1.4 var(--sans);color:var(--muted);margin-bottom:30px}

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
.grow .dd span{font:500 10.5px/1 var(--mono);letter-spacing:.1em;color:var(--muted);text-transform:uppercase}
.grow .n{font-size:16.5px;font-weight:500;letter-spacing:-.011em;line-height:1.3}
.grow .f{font-size:13.5px;color:var(--muted);margin-top:3px}
.grow .amt{white-space:nowrap;font:500 13px/1.2 var(--mono);text-align:right}
.grow .st{text-align:right}
.grow.closed{opacity:.55}
.gdetail{grid-column:1/-1;display:none;padding:4px 0 6px 80px;color:var(--muted);font-size:14.5px;line-height:1.6;max-width:62ch}
.grow.x .gdetail{display:block}
.gdetail .btn{margin-top:12px}
.count-num{font-weight:300;font-size:var(--s5);letter-spacing:-.022em;line-height:1;margin-top:20px}

/* indicators */
.ind{padding:22px 26px 22px;min-height:292px;position:relative}
.ind .val{font-weight:300;font-size:var(--s5);letter-spacing:-.022em;line-height:1;margin-top:26px}
.ind .val small{font:400 18px var(--sans);letter-spacing:0;color:var(--muted);margin-left:6px}
.ind .desc{font-size:13.5px;color:var(--muted);line-height:1.5;margin-top:10px;max-width:46ch}
.ind svg{display:block;width:100%;height:96px;margin-top:16px;overflow:visible}
.ind .yrs{display:flex;justify-content:space-between;font:10.5px/1 var(--mono);color:var(--muted);margin-top:6px}
.note{display:flex;gap:10px;align-items:center;padding:14px 18px;border-radius:18px;background:var(--wash);font-size:13px;color:var(--muted);margin-bottom:var(--gap)}

/* checklist (grant help) */
.check{display:grid;grid-template-columns:28px 1fr;gap:14px;padding:16px 0;border-top:1px solid var(--line);cursor:pointer;text-align:left;width:100%}
.check:first-child{border-top:0}
.check .bx{width:24px;height:24px;border-radius:8px;box-shadow:inset 0 0 0 1.5px var(--hair);display:grid;place-items:center;transition:background .2s,box-shadow .2s;color:#fff}
.check.done .bx{background:var(--accent);box-shadow:none}
.check b{font-weight:600;font-size:16px;letter-spacing:-.011em}
.check p{font-size:14.5px;color:var(--muted);line-height:1.5;margin-top:4px}
.check.done b{text-decoration:line-through;text-decoration-color:var(--accent)}

[hidden]{display:none!important}
summary{list-style:none}summary::-webkit-details-marker{display:none}summary.label::after{content:"+";margin-left:6px}
@media (max-width:1300px){
  .home{grid-template-columns:repeat(2,var(--cell));justify-content:center}
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
  .home{grid-template-columns:var(--cell);grid-auto-rows:292px}
  .w2,.hero{grid-column:auto}.hero{grid-row:span 2}.hero h1{font-size:50px}
  .player,.cal{grid-row:span 2}
  .player .pcov{width:calc(100% - 48px);height:230px}
  .player .label.abs{left:26px;top:272px}.eq{left:auto;right:26px;top:272px}
  .ttl{left:26px;top:304px;font-size:22px}.by{left:27px;top:366px}
  .prog{left:26px;top:420px;width:calc(100% - 52px)}.knob{top:415px}.times{top:436px}
  #el{left:26px!important}#len{left:auto!important;right:26px}
  .ctl,.play{top:476px}.play{top:470px;left:calc(50% - 26px)}#prev{left:calc(50% - 90px)!important}#next{left:calc(50% + 50px)!important}
  .cal .div{display:none}.list{left:26px;top:300px;width:calc(100% - 52px)}.row .n,.row .d{max-width:60vw}
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

HEAD_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..500&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">'

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


PHOTOS = ["web/street.jpg", "web/lanterns.jpg", "web/shop.jpg", "web/skyline.jpg", "web/rail.jpg"]


def cover(i, mk=None):
    return f'<div class="cover photo"><img src="../shared/img/{PHOTOS[i % 5]}" alt="" loading="lazy"></div>'


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
    <span class="mono" style="font-size:11px;color:var(--muted)">© 2026 e3 Initiative · Photos: Wikimedia Commons, Flickr (CC)</span>
    <nav class="links" aria-label="Footer">{foot}</nav>
  </footer>
  <div class="mega" aria-hidden="true">e3 Initiative</div>
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
import random as _r

def skyline(h=300, mini=False, seed=7):
    """Two layers of buildings as inline SVG. Windows are <i> style rects toggled by JS."""
    rnd = _r.Random(seed)
    W = 1200
    out = [f'<svg class="sky-svg" viewBox="0 0 {W} {h}" preserveAspectRatio="xMidYMax slice" aria-hidden="true">']
    for layer, (fill, lo, hi, step) in enumerate([("var(--far)", .30, .62, 70), ("var(--near)", .22, .5, 62), ("var(--front)", .10, .30, 80)]):
        x = -20 + rnd.randint(0, 30)
        while x < W:
            w = rnd.randint(46, 104); bh = int(h * rnd.uniform(lo, hi)); y = h - bh
            out.append(f'<g class="b b{layer}"><rect x="{x}" y="{y}" width="{w}" height="{bh}" fill="{fill}"/>')
            if rnd.random() < .35 and w > 60:
                out.append(f'<rect x="{x + w // 2 - 2}" y="{y - rnd.randint(10, 26)}" width="4" height="30" fill="{fill}"/>')
            if layer > 0 and not mini:
                cols = max(2, (w - 14) // 13); rows = max(2, (bh - 18) // 17)
                for r in range(rows):
                    for c in range(cols):
                        if rnd.random() < .5:
                            out.append(f'<rect class="w" x="{x + 8 + c * 13}" y="{y + 10 + r * 17}" width="6" height="9" rx="1"/>')
            out.append('</g>')
            x += w + rnd.randint(-6, 10)
    out.append('</svg>')
    return "".join(out)



def nextcard():
    g = DATED_SOON[0]
    d = days_left(g)
    return f"""<a class="dep" href="grants.html"><span class="dep-k">Next departure</span><span class="dep-t">{esc(g['name'])}</span><span class="dep-m"><b>{d}</b> days<i></i>{money(g.get('amountMax') or 0) if g.get('amountMax') else ''}</span></a><div class="loc"><svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg><span class="loc-d">Mott Street, Manhattan</span><span class="loc-n">Mott Street, Manhattan · night</span></div>"""


def home():
    """Nav, headline + one line + one button on the left, one photograph on the right, footer."""
    body = f"""
<div class="split">
  <div class="stxt">
    {label('Equity · Economics · Ethnicity')}
    <h1>{TAGLINE}<span>.</span></h1>
    <p>Student-led research on who builds local economies, who gets credit and who gets left out.</p>
    <div class="cta"><a class="btn" href="articles.html">Read the research</a></div>
  </div>
  <div class="spic rise">
    <img class="p-day" src="../shared/img/web/fire.jpg" alt="Brick tenements with fire escapes and shop signs on a Chinatown street in Manhattan" fetchpriority="high">
    <img class="p-night" src="../shared/img/web/night.jpg" alt="Mott Street in Manhattan at night, strung with lights">
    <div class="grade"></div>{nextcard()}
  </div>
</div>
"""
    return shell("index", body)

def pimg(p):
    return "../shared/img/" + ("web/rail.jpg" if "workers" in p["img"] else "web/street.jpg" if "street" in p["img"] else "web/lanterns.jpg")


def pub_list(page, kicker, title, lede, items, extra=""):
    """Header and a grid of photo cards."""
    cards = "".join(f"""<a class="pcard rise" href="{p['slug']}.html"><div class="pimg"><img src="{pimg(p)}" alt="{esc(p['alt'])}" loading="lazy"></div>
      <div class="pmeta"><span class="chip">{p['kind']}</span><span class="mono">{p['short'][:6]} · {p['min']} min</span></div><h3>{esc(p['title'])}</h3><p class="muted">{esc(p['author'])}</p></a>""" for p in items)
    return shell(page, ph(kicker, title, lede) + f'<div class="pgrid">{cards}</div>' + extra)

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
    body.append(f'<p class="muted" style="font-size:14px;margin-top:2em"><a href="../../{cite}">Citations and sources →</a></p>')
    body_html = f"""
<style>.topbar{{position:fixed;left:0;right:0;top:0;height:3px;background:transparent;z-index:40}}.topbar b{{display:block;height:100%;width:0;background:var(--accent)}}</style>
<div class="topbar"><b id="rb"></b></div>
<article class="tile atile rise" style="max-width:820px;margin:0 auto">
  {label(f"{p['kind']} · {p['date']} · {p['min']} min")}
  <h1>{esc(p['title'])}</h1>
  <div class="mono muted" style="font-size:12px">{esc(a['byline'] or 'By ' + p['author'])}</div>
  <div class="banner"><img src="{pimg(p)}" alt="{esc(p["alt"])}"></div><div class="capt">{esc(a["caption"] or p["alt"])}</div>
  <div class="prose" id="prose">{''.join(body)}</div>
</article>"""
    js = """<script>
const pr = $('#prose');
function upd() { const r = pr.getBoundingClientRect(), k = Math.max(0, Math.min(1, (innerHeight * .4 - r.top) / r.height)); $('#rb').style.width = k * 100 + '%'; }
addEventListener('scroll', upd, { passive: true }); upd();
</script>"""
    return shell(p["slug"], body_html, js)

def about():
    """Header, a photograph beside one statement, three people."""
    team = "".join(crow(f"0{i+1}", n, f"{r}. {b}", "") for i, (n, r, b) in enumerate(ABOUT["team"]))
    body = ph("About", "About e3 Initiative") + f"""
<div class="abt"><div class="abimg rise"><img src="../shared/img/web/bakery.jpg" alt="Customers outside a bakery and produce stand in Chinatown" loading="lazy"></div>
<div class="abtx"><p style="font-weight:400;font-size:28px;line-height:1.25;letter-spacing:-.7px">{ABOUT['who']}</p><p class="muted" style="font-size:15px;line-height:1.6;margin-top:18px;max-width:60ch">{ABOUT['what']}</p></div></div>
<section style="margin-top:20px"><div class="tile rows rise">{team}</div></section>"""
    return shell("about", body)

def journals():
    t, logo = JOURNAL
    body = ph("Publications", "Journals", "Browse our academic journals and long-form publications.") + f"""
<div class="tile pad rise" style="display:flex;gap:30px;align-items:center;flex-wrap:wrap"><img src="{IMG}{logo}" alt="{esc(t)}" width="160" height="160" style="border-radius:20px">
<div>{label('Journal')}<div class="serif-l" style="font-size:var(--s3);line-height:1.08;margin-top:14px;max-width:18ch">{t}</div><p class="muted" style="margin-top:10px;font-size:14px">Entries coming soon.</p></div></div>"""
    return shell("journals", body)

def grants():
    """Header, one search row, results. Other filters are folded away."""
    cats = "".join(f'<button data-v="{k}">{v}</button>' for k, v in CAT_LABEL.items())
    lists = " · ".join(f'<a href="{s}.html" style="color:var(--ink)">{CAT_LABEL[c]}</a>' for s, (c, _, _) in CATEGORY_PAGES.items())
    body = ph("Grants", "Grant Finder", f"Funding for small businesses and nonprofits. Ready-made lists: {lists}.", '<a class="btn ghost" href="grant-help.html">Help & tips →</a>') + f"""
<div class="tile pad rise" style="margin-bottom:20px">
  <div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap">
    <div class="search" style="flex:1;min-width:240px">{icon('search')}<input class="inp" id="q" type="search" placeholder="Women-owned bakery…" aria-label="Search grants"></div>
    <div class="seg" data-f="status"><button class="on" data-v="live">Open + rolling</button><button data-v="">All</button></div>
    <span class="thin" style="font-size:var(--s3)" id="gcount">0</span>
  </div>
  <details style="margin-top:16px"><summary class="label" style="cursor:pointer">More filters</summary>
    <div class="fl">{label('Who qualifies')}<div class="seg" data-f="elig"><button class="on" data-v="">Anyone</button><button data-v="small_business">Business</button><button data-v="nonprofit">Nonprofit</button></div></div>
    <div class="fl">{label('Award up to at least')}<div class="seg" data-f="amt"><button class="on" data-v="0">Any</button><button data-v="10000">$10k</button><button data-v="50000">$50k</button><button data-v="250000">$250k</button></div></div>
    <div class="fl">{label('Category')}<div class="seg" data-f="cat" data-multi><button class="on" data-v="">All</button>{cats}</div></div></details>
</div>
<div class="tile gres rise" id="gres" aria-live="polite"></div>"""
    js = """<script src="../shared/grants-data.js"></script><script>
const F = { q: '', elig: '', status: 'live', amt: 0, cat: new Set() };
$$('.seg[data-f]').forEach(seg => seg.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; const f = seg.dataset.f;
  if (seg.hasAttribute('data-multi')) { if (!b.dataset.v) { F.cat.clear(); $$('button', seg).forEach(x => x.classList.toggle('on', !x.dataset.v)); }
    else { F.cat.has(b.dataset.v) ? F.cat.delete(b.dataset.v) : F.cat.add(b.dataset.v); b.classList.toggle('on'); $('button[data-v=""]', seg).classList.toggle('on', !F.cat.size); } }
  else { $$('button', seg).forEach(x => x.classList.toggle('on', x === b)); F[f] = f === 'amt' ? +b.dataset.v : b.dataset.v; } render(); }));
$('#q').addEventListener('input', e => { F.q = e.target.value.toLowerCase(); render(); });
function render() {
  const rs = GRANTS.filter(g => (!F.q || (g.name + g.funder + g.desc + CAT_LABEL[g.cat]).toLowerCase().includes(F.q))
    && (!F.elig || g.elig === F.elig || g.elig === 'both') && (F.status === '' || g.status !== 'closed')
    && (!F.amt || g.max >= F.amt) && (!F.cat.size || F.cat.has(g.cat)))
    .sort((a, b) => ({ open: 0, rolling: 1, closed: 2 }[a.status] - { open: 0, rolling: 1, closed: 2 }[b.status]) || (a.days ?? 999) - (b.days ?? 999));
  $('#gcount').textContent = rs.length;
  $('#gres').innerHTML = rs.length ? rs.map(g => { const dt = g.days != null ? g.dl.split(' ') : null;
    return `<div class="grow ${g.status}" tabindex="0"><div class="dd">${dt ? `<b>${+dt[1]}</b><span>${dt[0]}</span>` : `<b style="font-size:24px">∞</b><span>${g.dl}</span>`}</div>
      <div><div class="n">${g.name}</div><div class="f">${g.funder}</div></div><div class="amt">${g.max ? 'up to $' + g.max.toLocaleString() : 'Varies'}</div>
      <div class="st">${g.status === 'open' ? `<span class="chip a">${g.days != null ? 'in ' + g.days + 'd' : 'Open'}</span>` : `<span class="chip">${g.status === 'rolling' ? 'Rolling' : 'Closed'}</span>`}</div>
      <div class="gdetail">${g.desc}<br><a class="btn sm" href="${g.link}" target="_blank" rel="noopener">Funder's page →</a></div></div>`; }).join('')
    : '<div style="padding:40px 0;text-align:center" class="muted">No grants match these filters. Try widening them.</div>';
}
$('#gres').addEventListener('click', e => { const r = e.target.closest('.grow'); if (r && !e.target.closest('a')) r.classList.toggle('x'); });
$('#gres').addEventListener('keydown', e => { if (e.key === 'Enter' && e.target.classList.contains('grow')) e.target.classList.toggle('x'); });
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
    body = ph("Grant list", title, intro) + f'<div class="tile rows rise">{rows}</div><p class="muted" style="margin-top:22px;font-size:14px">More lists: {others} · <a href="grants.html" style="color:var(--ink)">Search all {len(GRANTS)}</a></p>'
    return shell(slug, body)

def grant_help():
    """Header, one checklist. The directory is folded away."""
    tips = "".join(f'<button class="check" data-i="{i}"><span class="bx">{icon("check", 14)}</span><div><b>{a}</b><p>{b}</p></div></button>' for i, (a, b) in enumerate(HELP["tips"]))
    orgs = "".join(crow("→", n, d, u, f'<span class="chip">{l}</span>') for n, d, l, u in HELP["orgs"])
    body = ph("Grants", "Grant Help & Tips", HELP["intro"], '<a class="btn" href="grants.html">Search grants →</a>') + f"""
<div class="tile rows rise" style="padding-top:18px">{label('How to write a strong application · <span id="hcount">0/8</span>')}<div style="margin-top:6px">{tips}</div>
  <details style="padding:16px 0;border-top:1px solid var(--line)"><summary class="label" style="cursor:pointer">Common mistakes to avoid</summary><ul style="margin:12px 0 0 18px;color:var(--muted);font-size:14px;line-height:1.7">{''.join(f'<li>{m}</li>' for m in HELP['mistakes'])}</ul></details>
  <details style="padding:16px 0;border-top:1px solid var(--line)"><summary class="label" style="cursor:pointer">Where to get free help</summary><div style="margin-top:8px">{orgs}</div><p class="muted" style="font-size:12px;line-height:1.6;margin-top:14px;max-width:80ch">{HELP['disclaimer']}</p></details></div>"""
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
          <div>{label(t)}<p class="serif-l" style="font-size:var(--s2);line-height:1.22;margin-top:22px">{p1}</p><p class="muted" style="margin-top:16px;font-size:14px;line-height:1.55">{p2}</p></div>
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
    write(f"{D}/theme.css", CSS + NOB + CITY)
    write(f"{D}/theme.js", JS + CITYJS)
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
"""


CITY = r"""
/* city: transit-line nav, skyline, signage type */
.pill-nav{background:none;box-shadow:none;padding:0 0 0;gap:2px;position:relative}
.pill-nav::before{content:"";position:absolute;left:30px;right:30px;top:6px;height:4px;border-radius:2px;background:var(--accent)}
.pill-nav a{background:none!important;padding:22px 14px 4px;position:relative;color:var(--muted);font-weight:500}
.pill-nav a::before{content:"";position:absolute;left:50%;top:0;width:16px;height:16px;margin-left:-8px;border-radius:50%;background:var(--bg);box-shadow:0 0 0 4px var(--accent);transition:background .2s,transform .2s}
.pill-nav a:hover::before{transform:scale(1.15)}
.pill-nav a.on{color:var(--ink)}.pill-nav a.on::before{background:var(--ink);box-shadow:0 0 0 4px var(--accent)}
.pill-nav.open{background:var(--tile);box-shadow:var(--shadow);padding:8px}.pill-nav.open::before,.pill-nav.open a::before{display:none}.pill-nav.open a{padding:10px 16px}
.brand i{border-radius:7px;background:var(--accent)}.brand i::after{background:var(--peach);border-radius:2px;width:8px;height:8px;right:3px;top:3px}
h1,.ph h1,.hero h1{font-weight:600;letter-spacing:-.04em}
.label{text-transform:uppercase;font:600 11.5px var(--mono);letter-spacing:.1em}
.label i{border-radius:2px;width:8px;height:8px}
.btn{font-weight:600}
.chome{display:grid;gap:34px;align-content:start;grid-auto-rows:min-content}
.chero{display:grid;grid-template-columns:1.25fr 1fr;gap:20px 56px;align-items:end}
.chero .label{grid-column:1/-1}
.chero h1{font-size:76px;line-height:.96}.chero h1 span{color:var(--accent)}
.cside p{font-size:15px;line-height:1.55;color:var(--muted);max-width:42ch;margin-bottom:18px}
.city{position:relative;border-radius:22px;overflow:hidden;background:var(--sky);transition:background .5s}
#sky{height:380px}
.sky-svg{position:absolute;inset:0;width:100%;height:100%}
.sky-svg .w{fill:var(--win);opacity:0;transition:opacity 1.4s}
.sky-svg .w.on{opacity:.95}
html:not(.night) .sky-svg .w.on{opacity:.55}
.route{position:absolute;left:0;right:0;bottom:22px;height:4px}
.route i{position:absolute;inset:0;background:var(--accent);border-radius:2px}
.route b{position:absolute;top:-6px;width:16px;height:16px;margin-left:-8px;border-radius:50%;background:var(--front);box-shadow:0 0 0 4px var(--accent)}
.route em{position:absolute;top:-7px;left:-60px;width:56px;height:18px;border-radius:9px;background:var(--peach);box-shadow:0 0 18px var(--peach)}
.city.mini{height:96px;margin-top:80px;border-radius:0;background:none;opacity:.9}
.city.mini{max-width:100%;contain:paint}.city.mini .sky-svg{position:static;display:block;width:100%;height:96px}
@media(max-width:900px){.chero{grid-template-columns:1fr}.chero h1{font-size:54px}#sky{height:260px}}
@media(prefers-reduced-motion:reduce){.route em{display:none}}
"""

CITY += r"""
/* photo pass */
.phero{position:relative;border-radius:22px;overflow:hidden;height:min(76vh,700px);min-height:480px;background:#111}
.phero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .7s}
.phero .p-day{object-position:50% 40%}.phero .p-night{opacity:0}
html.night .phero .p-night{opacity:1}html.night .phero .p-day{opacity:0}
.phero .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,9,13,.25) 0%,rgba(6,9,13,0) 28%,rgba(6,9,13,.78) 100%)}
.ptxt{position:absolute;left:48px;right:48px;bottom:44px;color:#fff;display:grid;gap:18px}
.ptxt .label{color:rgba(255,255,255,.85)}.ptxt .label i{background:var(--peach)}
.ptxt h1{font-size:92px;line-height:.94;max-width:11ch;color:#fff}.ptxt h1 span{color:var(--peach)}
.prow{display:flex;justify-content:space-between;align-items:flex-end;gap:28px}
.prow p{font-size:16px;line-height:1.5;color:rgba(255,255,255,.82);max-width:40ch}
.phero .btn{background:#fff;color:#101318}
.cover.photo{border-radius:20px}.cover.photo img,.banner img{filter:none}
.banner{border-radius:22px}
@media(max-width:900px){.phero{height:84vh;min-height:520px}.ptxt{left:24px;right:24px;bottom:28px}.ptxt h1{font-size:54px}.prow{flex-direction:column;align-items:flex-start}}
"""

CITY += r"""
/* split layout */
.split{display:grid;grid-template-columns:5fr 7fr;gap:48px;align-items:stretch;min-height:640px}
.stxt{display:flex;flex-direction:column;justify-content:flex-end;gap:22px;padding-bottom:6px}
.stxt h1{font-size:88px;line-height:.94;max-width:9ch}.stxt h1 span{color:var(--accent)}
.stxt p{font-size:16px;line-height:1.55;color:var(--muted);max-width:38ch}
.spic{position:relative;border-radius:22px;overflow:hidden;min-height:560px;background:#111}
.spic img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .7s}
.spic .p-night{opacity:0}html.night .spic .p-night{opacity:1}html.night .spic .p-day{opacity:0}
.pgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.pcard{display:block}
.pimg{border-radius:20px;overflow:hidden;aspect-ratio:4/3;background:var(--wash)}
.pimg img{width:100%;height:100%;object-fit:cover;transition:transform .6s cubic-bezier(.33,1,.68,1)}
.pcard:hover .pimg img{transform:scale(1.04)}
.pmeta{display:flex;align-items:center;gap:10px;margin:16px 0 8px;color:var(--muted);font-size:12px}
.pcard h3{font-weight:600;font-size:21px;line-height:1.2;letter-spacing:-.02em}
.pcard p{margin-top:8px;font-size:14px}
.abt > *{min-width:0}.abt{display:grid;grid-template-columns:5fr 6fr;gap:44px;align-items:center}
.abimg{border-radius:22px;overflow:hidden;height:540px}.abimg img{width:100%;height:100%;object-fit:cover}
@media(max-width:900px){.split,.abt{grid-template-columns:1fr;gap:28px;min-height:0}.stxt h1{font-size:56px}.spic{min-height:340px}.pgrid{grid-template-columns:1fr}.abimg{height:300px}}
@media(min-width:901px) and (max-width:1200px){.pgrid{grid-template-columns:repeat(2,1fr)}}
"""

CITY += r"""
/* ===== D type system (loaded last, sets every role explicitly) =====
   Archivo (wdth 62-125): condensed 700 uppercase = wayfinding display; normal width = UI and body.
   Newsreader: editorial serif for reading, ledes and statements. IBM Plex Mono: departures-board data. */
:root{
  --disp:"Archivo","Arial Narrow",system-ui,sans-serif; --read:"Newsreader",Georgia,"Times New Roman",serif; --mono:"IBM Plex Mono",ui-monospace,monospace;
  --sans:"Archivo",system-ui,sans-serif; --label-font:600 12px/1.2 "Archivo",system-ui,sans-serif;
  --t-hero:clamp(3rem,.8rem + 5.6vw,6rem);
  --t-h1:clamp(2.6rem,1.4rem + 4.2vw,4.75rem);
  --t-h2:clamp(2.1rem,1.4rem + 2.4vw,3.25rem);
  --t-h3:clamp(1.3rem,1.15rem + .6vw,1.6rem);
  --t-lede:clamp(1.15rem,1.05rem + .4vw,1.35rem);
  --t-body:1rem; --t-small:.875rem; --t-label:.75rem;
}
html{font-optical-sizing:auto;text-size-adjust:100%;-webkit-text-size-adjust:100%}
body{font:400 var(--t-body)/1.55 var(--sans);font-stretch:100%;font-feature-settings:"kern","liga","tnum","lnum";font-variant-numeric:lining-nums tabular-nums;letter-spacing:0;text-rendering:optimizeLegibility}
p,li,.n,.d,.f{text-wrap:pretty}
h1,h2,h3,.ph h1,.shead h2,.pcard h3{text-wrap:balance}

/* display: condensed signage */
h1,h2,.ph h1,.shead h2,.stxt h1,.chero h1,.ptxt h1{font-family:var(--disp);font-stretch:68%;font-weight:700;text-transform:uppercase;letter-spacing:-.012em;word-spacing:.08em;line-height:.9;font-feature-settings:"kern","lnum"}
.stxt h1{font-size:var(--t-hero);line-height:.88;max-width:8.5ch;letter-spacing:-.018em;hyphens:manual}
.ph h1{font-size:var(--t-h1);line-height:.92;margin-top:16px}
.shead h2{font-size:var(--t-h2);line-height:.95}
.ph p{font:400 var(--t-lede)/1.42 var(--read);letter-spacing:-.003em;max-width:52ch;color:var(--muted);margin-top:18px}
.stxt p{font:400 var(--t-lede)/1.42 var(--read);max-width:34ch;color:var(--muted)}
h3,.pcard h3{font-family:var(--disp);font-stretch:82%;font-weight:700;font-size:var(--t-h3);line-height:1.08;letter-spacing:-.008em;text-transform:none}

/* wayfinding: nav, labels, brand, buttons */
.brand{font:800 1.2rem/1 var(--disp);font-stretch:74%;text-transform:uppercase;letter-spacing:.015em}
.pill-nav a{font:600 .8125rem/1.1 var(--disp);font-stretch:88%;text-transform:uppercase;letter-spacing:.07em;padding-left:12px;padding-right:12px}
.pill-nav.open a{font-size:.9rem}
.label,summary.label,.field span,.fl > .label{font:600 var(--t-label)/1.2 var(--disp);font-stretch:100%;text-transform:uppercase;letter-spacing:.14em}
.shead a,footer .links,footer .links a{font:500 .8125rem/1.3 var(--disp);font-stretch:92%;text-transform:uppercase;letter-spacing:.08em}
.btn{font:700 .8125rem/1 var(--disp);font-stretch:92%;text-transform:uppercase;letter-spacing:.1em}
.btn.sm{font:600 .6875rem/1 var(--mono);letter-spacing:.04em}
.seg button{font:600 .8125rem/1 var(--disp);font-stretch:92%;letter-spacing:.03em}
.skip{font:600 .875rem var(--disp)}

/* data: departures board */
.mono,.chip,.crow .t,.tr,.capt,.yrs,.pmeta .mono,.grow .amt,.grow .dd span,.row .t,.cover .mk,.ind .yrs,footer .mono{font-family:var(--mono);font-variant-numeric:tabular-nums slashed-zero;font-feature-settings:"zero","tnum"}
.chip{font:500 .6875rem/1 var(--mono);text-transform:uppercase;letter-spacing:.06em;padding:6px 9px}
.crow .t{font:500 .75rem/1.2 var(--mono);letter-spacing:.02em}
.crow .n{font:600 1.0625rem/1.25 var(--disp);font-stretch:96%;letter-spacing:-.003em}
.crow .d{font:400 .875rem/1.4 var(--sans);color:var(--muted)}
.pmeta{font:500 .75rem/1.2 var(--mono);letter-spacing:.02em}
.pcard p{font:400 .9375rem/1.4 var(--sans)}
.grow .dd b{font:700 2rem/.9 var(--disp);font-stretch:70%;letter-spacing:-.01em;font-variant-numeric:lining-nums tabular-nums}
.grow .dd span{font:600 .625rem/1 var(--mono);letter-spacing:.12em;margin-top:4px}
.grow .n{font:600 1.0625rem/1.2 var(--disp);font-stretch:96%;letter-spacing:-.003em}
.grow .f{font:400 .8125rem/1.35 var(--sans)}
.grow{grid-template-columns:62px 1fr 150px 88px}
.grow .amt{font:500 .875rem/1 var(--mono);letter-spacing:-.01em;white-space:nowrap}
.gdetail{font:400 .9375rem/1.55 var(--sans);max-width:62ch}
.ind .val{font:700 clamp(3.4rem,2.6rem + 2.4vw,4.4rem)/.9 var(--disp);font-stretch:68%;letter-spacing:-.01em}
.ind .val small{font:500 1rem var(--mono);letter-spacing:0}
.ind .desc{font:400 .875rem/1.5 var(--sans);max-width:46ch}
.tr{font-size:.75rem}
.note{font:400 .875rem/1.45 var(--sans)}
.check b{font:600 1rem/1.3 var(--disp);font-stretch:96%;letter-spacing:0}
.check p{font:400 .875rem/1.5 var(--sans)}
.capt{font-size:.75rem;line-height:1.4;letter-spacing:.01em}

/* forms */
.inp,input,select,textarea{font:400 1rem/1.4 var(--sans);font-stretch:100%;letter-spacing:0}
.inp::placeholder{color:var(--muted);opacity:.85}
textarea.inp{line-height:1.5}

/* reading: article pages are editorial */
.atile h1{font:500 clamp(2.4rem,1.5rem + 3.4vw,4.25rem)/1.02 var(--read);font-stretch:100%;text-transform:none;letter-spacing:-.022em;max-width:20ch;text-wrap:balance;font-feature-settings:"kern","liga","lnum"}
.prose{font:400 clamp(1.125rem,1.05rem + .3vw,1.25rem)/1.62 var(--read);max-width:66ch;letter-spacing:0;hyphens:auto;-webkit-hyphens:auto;font-variant-numeric:lining-nums;font-feature-settings:"kern","liga","onum" 0}
.prose p{margin:0 0 1.1em;text-wrap:pretty}
.prose h2{font:700 clamp(1.7rem,1.4rem + 1vw,2.2rem)/1 var(--disp);font-stretch:70%;text-transform:uppercase;letter-spacing:-.005em;word-spacing:.1em;margin:1.7em 0 .55em}
.prose h3{font:700 1.35rem/1.15 var(--disp);font-stretch:84%;text-transform:none;letter-spacing:0;margin:1.5em 0 .4em}
.prose li{margin:0 0 .55em 1.1em;padding-left:.2em}
.prose a{text-decoration-thickness:1.5px;text-underline-offset:.2em}
.prose blockquote{font-style:italic}
.prose em,.prose i{font-style:italic}
.prose strong,.prose b{font-weight:600}
.read .side,.gside,.toc{font-family:var(--sans)}
.toc .crow .n{font:500 .9375rem/1.3 var(--sans)}

/* inline-styled elements from the page templates */
[style*="font-size:200px"]{font:800 clamp(9rem,5rem + 20vw,17rem)/.8 var(--disp)!important;font-stretch:62%;letter-spacing:-.02em!important;text-transform:none}
.thin{font-family:var(--disp);font-weight:700;font-stretch:68%;letter-spacing:-.01em;line-height:.9}
p[style*="font-weight:400;font-size:28px"],p[style*="font-weight:300;font-size:26px"]{font:400 clamp(1.5rem,1.2rem + 1.1vw,2.1rem)/1.22 var(--read)!important;letter-spacing:-.012em!important;text-wrap:balance}
div[style*="font-weight:300;font-size:36px"],div[style*="font-weight:300"]{font:700 clamp(1.8rem,1.4rem + 1.2vw,2.4rem)/1 var(--disp)!important;font-stretch:72%;text-transform:uppercase;letter-spacing:-.005em!important}
[style*="font-weight:300"] .mono,.mono[style]{font-family:var(--mono)}
.muted[style*="font-size:14px"],.muted[style*="font-size:15px"]{font-family:var(--sans)}
span.mono[style*="font-size:11px"],div.mono[style*="font-size:12px"]{font-family:var(--mono);letter-spacing:.02em}
.btn,.chip,.label{-webkit-font-smoothing:antialiased}

@media(max-width:900px){
  .stxt h1{max-width:none;line-height:.9}
  .grow{grid-template-columns:52px 1fr 78px}
  .ph h1{font-size:var(--t-h1)}
}
@media(max-width:700px){
  :root{--t-hero:clamp(3.2rem,15vw,4.4rem)}
  .ph h1{font-size:clamp(2.6rem,13vw,3.4rem)}
  .shead h2{font-size:clamp(2.1rem,10vw,2.6rem)}
  .atile h1{font-size:clamp(2.1rem,9.5vw,2.7rem)}
  .prose{font-size:1.125rem;line-height:1.6}
  .grow .dd b{font-size:1.75rem}
}
"""

CITY += r"""
/* aesthetic pass */
body{background:var(--bg);position:relative}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background:radial-gradient(900px 520px at 88% -8%,rgba(0,160,106,.16),transparent 60%),radial-gradient(760px 480px at -8% 38%,rgba(255,196,46,.10),transparent 62%)}
html.night body::before{background:radial-gradient(900px 560px at 88% -10%,rgba(0,190,125,.20),transparent 60%),radial-gradient(800px 520px at -10% 40%,rgba(255,196,46,.12),transparent 62%),radial-gradient(600px 400px at 60% 110%,rgba(80,90,200,.14),transparent 60%)}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:50;opacity:.06;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.wrap{position:relative;z-index:1}

/* frosted sticky nav with a glowing line */
.nav{position:sticky;top:0;z-index:30;margin-inline:calc(50% - 50vw);padding:18px calc(50vw - 50%) 18px;backdrop-filter:blur(18px) saturate(1.4);-webkit-backdrop-filter:blur(18px) saturate(1.4);
  background:linear-gradient(180deg,color-mix(in srgb,var(--bg) 94%,transparent),color-mix(in srgb,var(--bg) 62%,transparent))}
.pill-nav::before{box-shadow:0 0 14px rgba(0,160,106,.55)}
html.night .pill-nav::before{box-shadow:0 0 18px rgba(0,210,140,.7)}
.pill-nav a.on::before{box-shadow:0 0 0 4px var(--accent),0 0 18px rgba(0,190,125,.8)}
.brand i{box-shadow:0 6px 18px -4px rgba(0,160,106,.7)}

/* hero */
.stxt h1{font-size:clamp(3rem,5.6vw,5.4rem)!important;max-width:none}
.split{gap:56px;min-height:0;align-items:center;margin-top:8px}
.spic{border-radius:30px;min-height:min(72vh,680px);box-shadow:0 50px 90px -40px rgba(10,20,30,.55),0 0 0 1px rgba(255,255,255,.05);transform:rotate(0.0001deg)}
html.night .spic{box-shadow:0 60px 120px -40px rgba(0,190,125,.25),0 0 0 1px rgba(255,255,255,.07)}
.spic img{transform:scale(1.08);will-change:transform}
.spic .grade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,12,16,0) 45%,rgba(8,12,16,.62) 100%),linear-gradient(135deg,rgba(0,160,106,.22),rgba(255,196,46,.12) 70%);mix-blend-mode:normal;pointer-events:none}
.stxt .cta .btn{box-shadow:0 14px 30px -12px rgba(16,19,24,.6);transition:transform .3s cubic-bezier(.33,1,.68,1),box-shadow .3s}
.stxt .cta .btn:hover{transform:translateY(-3px);box-shadow:0 22px 36px -14px rgba(16,19,24,.7)}
html.night .stxt .cta .btn{box-shadow:0 14px 40px -12px rgba(0,210,140,.45)}
.dep{position:absolute;left:22px;bottom:22px;display:grid;gap:3px;padding:16px 20px 15px;min-width:250px;max-width:70%;border-radius:20px;color:#fff;
  background:rgba(14,18,24,.46);backdrop-filter:blur(20px) saturate(1.5);-webkit-backdrop-filter:blur(20px) saturate(1.5);box-shadow:inset 0 1px 0 rgba(255,255,255,.18);transition:transform .35s cubic-bezier(.33,1,.68,1),background .3s}
.dep:hover{transform:translateY(-4px);background:rgba(14,18,24,.6)}
.dep-k{font:600 .68rem var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--peach)}
.dep-t{font-weight:600;font-size:1.05rem;line-height:1.2;letter-spacing:-.01em}
.dep-m{display:flex;align-items:center;gap:8px;font:500 .8rem var(--mono);color:rgba(255,255,255,.78)}
.dep-m b{font:700 1.4rem var(--sans);color:#fff;letter-spacing:-.02em}.dep-m i{width:4px;height:4px;border-radius:50%;background:currentColor;opacity:.6}
.loc{position:absolute;right:20px;top:20px;display:flex;align-items:center;gap:7px;padding:8px 13px;border-radius:99px;font:500 .72rem var(--mono);letter-spacing:.04em;color:#fff;background:rgba(14,18,24,.4);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}
.loc-n{display:none}html.night .loc-d{display:none}html.night .loc-n{display:inline}

/* cards and rows */
.pimg{border-radius:24px;box-shadow:0 30px 50px -30px rgba(10,20,30,.5);position:relative}
.pimg::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(8,12,16,.38));opacity:.7;transition:opacity .4s}
.pcard:hover .pimg::after{opacity:.2}
.pcard{transition:transform .5s cubic-bezier(.33,1,.68,1)}.pcard:hover{transform:translateY(-6px)}
html.night .pimg{box-shadow:0 30px 60px -30px rgba(0,190,125,.22)}
.abimg{border-radius:28px;box-shadow:0 50px 80px -40px rgba(10,20,30,.55)}
.tile{box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 30px 60px -40px rgba(20,30,40,.35)!important}
html.night .tile{box-shadow:0 1px 0 rgba(255,255,255,.05) inset,0 30px 70px -40px rgba(0,0,0,.9)!important;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,0) 40%),var(--tile)}
.grow:hover,.crow:hover{background:color-mix(in srgb,var(--accent) 7%,transparent)}

/* footer: route line with stations, then a giant wordmark */
footer{position:relative;padding-top:56px;margin-top:70px}
footer .links{position:relative;display:flex;gap:6px 28px}
footer .links a{position:relative;padding-top:20px;color:var(--muted);transition:color .2s}
footer .links a::before{content:"";position:absolute;left:0;top:3px;width:9px;height:9px;border-radius:50%;background:var(--bg);box-shadow:0 0 0 2px var(--accent);transition:transform .2s,background .2s}
footer .links a:hover{color:var(--ink)}footer .links a:hover::before{background:var(--accent);transform:scale(1.35)}
footer .links::before{content:"";position:absolute;left:4px;right:20px;top:7px;height:2px;border-radius:1px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 0%,transparent))}
.mega{position:relative;z-index:0;margin:22px 0 -.06em;text-align:center;white-space:nowrap;font:800 18.6vw/.84 var(--sans);font-stretch:62%;font-variation-settings:'wdth' 62;letter-spacing:-.02em;text-transform:uppercase;color:transparent;background:linear-gradient(180deg,color-mix(in srgb,var(--ink) 22%,transparent),color-mix(in srgb,var(--ink) 3%,transparent) 85%);-webkit-background-clip:text;background-clip:text;pointer-events:none;user-select:none;overflow:hidden;max-width:100vw}
  background:linear-gradient(180deg,color-mix(in srgb,var(--ink) 14%,transparent),transparent 78%);-webkit-background-clip:text;background-clip:text;pointer-events:none;user-select:none;overflow:hidden;height:.62em}

@media(max-width:900px){.nav{padding-block:14px}.spic{min-height:380px}.dep{min-width:0;max-width:calc(100% - 44px)}.loc{display:none}footer .links{flex-wrap:wrap}}
@media(prefers-reduced-motion:reduce){.pcard,.dep,.stxt .cta .btn{transition:none}}
"""

CITYJS = r"""
(function () {
  const img = document.querySelectorAll('.spic img'); if (!img.length || matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  let y = 0, ticking = false;
  const upd = () => { img.forEach(i => i.style.transform = `translateY(${y * -.06}px) scale(1.1)`); ticking = false; };
  addEventListener('scroll', () => { y = scrollY; if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true }); upd();
})();

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
"""
