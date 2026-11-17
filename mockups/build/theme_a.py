"""Variation A: Paper widgets. Warm paper, white tiles, thin Geist numerals, mono captions, one ultramarine accent.
Every page is built from the paper-widgets components: tiles with dot labels, calendar rows, tick dials, level bars,
the now-playing player and the focus switch (here: reading mode, saved across pages)."""
from common import *

D = "site-a"

CSS = r"""
:root{
  --bg:#e7e5e0; --tile:#f8f7f4; --ink:#141416; --ink-rgb:20 20 22; --muted:#8b887f; --accent:#2b36ff; --peach:#ffb48a;
  --line:rgba(20,20,22,.08); --wash:rgba(20,20,22,.05); --track:rgba(20,20,22,.07); --hair:rgba(20,20,22,.12);
  --marker:rgba(20,20,22,.14); --dotted:rgba(20,20,22,.16); --sun-glow:rgba(43,54,255,.14);
  --sans:"Geist",system-ui,sans-serif; --mono:"Geist Mono",monospace; --label-font:400 14px "Inter",system-ui,sans-serif;
  --r:38px; --cell:292px; --gap:20px;
  --shadow:0 0 0 1px rgba(20,20,22,.05), inset 0 1px 0 #fff, 0 28px 46px -30px rgba(40,34,20,.35), 0 2px 4px rgba(40,34,20,.04);
  --focus-dark:radial-gradient(260px 220px at 75% 15%, rgba(43,54,255,.55), transparent 70%), #121215;
}
html.night{--bg:#0d0d10;--tile:#17171b;--ink:#f4f3f0;--ink-rgb:244 243 240;--muted:#8a8780;--line:rgba(255,255,255,.07);--wash:rgba(255,255,255,.06);--track:rgba(255,255,255,.08);--hair:rgba(255,255,255,.14);--marker:rgba(255,255,255,.16);--dotted:rgba(255,255,255,.2);
  --shadow:0 0 0 1px rgba(255,255,255,.05), inset 0 1px 0 rgba(255,255,255,.06), 0 28px 46px -30px rgba(0,0,0,.8)}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased;font-variant-numeric:tabular-nums;transition:background .5s,color .5s}
a{color:inherit;text-decoration:none}
button,input,select,textarea{font:inherit;color:inherit}
button{background:none;border:0;cursor:pointer}
img{display:block;max-width:100%}
.wrap{max-width:calc(var(--cell)*4 + var(--gap)*3 + 64px);margin:0 auto;padding:0 32px}
.skip{position:absolute;left:-999px;top:8px;background:var(--ink);color:var(--tile);padding:8px 14px;border-radius:99px;z-index:99}
.skip:focus{left:12px}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}

/* nav */
.nav{display:flex;align-items:center;justify-content:space-between;padding:26px 0 34px;gap:16px}
.brand{display:flex;align-items:center;gap:10px;font-size:17px;letter-spacing:-.3px}
.brand i{width:26px;height:26px;border-radius:9px;background:var(--accent);position:relative;overflow:hidden;flex:none}
.brand i::after{content:"";position:absolute;right:-9px;top:-9px;width:20px;height:20px;border-radius:50%;background:var(--peach)}
.pill-nav{display:flex;list-style:none;background:var(--tile);border-radius:99px;padding:5px;box-shadow:var(--shadow);transition:background .5s}
.pill-nav a{display:block;padding:9px 15px;border-radius:99px;font:var(--label-font);color:var(--muted);white-space:nowrap;transition:color .2s}
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
.label{display:flex;align-items:center;gap:8px;font:var(--label-font);letter-spacing:-.1px;color:var(--muted)}
.label i{width:6px;height:6px;border-radius:50%;background:var(--accent);flex:none}
.tile > .label.abs{position:absolute;left:26px;top:22px}
.tr{position:absolute;right:26px;top:22px;font-size:13px;color:var(--muted)}
.mono{font-family:var(--mono)}
.muted{color:var(--muted)}
.thin{font-weight:300;letter-spacing:-.045em;line-height:1}
.chip{display:inline-flex;align-items:center;font:500 11px var(--mono);padding:5px 9px;border-radius:99px;background:var(--wash);color:var(--muted);white-space:nowrap}
.chip.a{background:var(--accent);color:#fff}
.chip.ink{background:var(--ink);color:var(--tile)}
.btn{display:inline-flex;align-items:center;gap:8px;height:46px;padding:0 20px;border-radius:99px;font-size:14px;background:var(--ink);color:var(--tile);transition:transform .15s;white-space:nowrap}
.btn.ghost{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 1px var(--hair)}
.btn.sm{height:34px;padding:0 14px;font:500 11px var(--mono)}
.btn:active{transform:scale(.96)}
.well{width:36px;height:36px;border-radius:11px;background:var(--wash);display:grid;place-items:center;flex:none}
.well.lg{width:64px;height:64px;border-radius:50%}

/* page header */
.ph{display:grid;grid-template-columns:1fr auto;gap:24px;align-items:end;margin:6px 0 30px}
.ph h1{font-weight:300;font-size:64px;line-height:1;letter-spacing:-.045em;margin-top:14px}
.ph p{color:var(--muted);font-size:15px;line-height:1.55;max-width:56ch;margin-top:14px}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:var(--gap)}
.c3{grid-column:span 3}.c4{grid-column:span 4}.c5{grid-column:span 5}.c6{grid-column:span 6}.c7{grid-column:span 7}.c8{grid-column:span 8}.c12{grid-column:span 12}
section{margin-top:72px}
.shead{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:20px;gap:16px}
.shead h2{font-weight:300;font-size:48px;letter-spacing:-.04em;line-height:1}
.shead a{font:var(--label-font);color:var(--muted)}.shead a:hover{color:var(--ink)}

/* calendar rows: the list primitive */
.rows{padding:8px 26px}
.crow{display:grid;grid-template-columns:74px 3px 1fr auto;gap:16px;align-items:center;padding:18px 0;border-top:1px solid var(--line)}
.crow:first-child{border-top:0}
.crow .t{font:500 12px var(--mono);color:var(--muted)}
.crow .m{height:36px;border-radius:2px;background:var(--marker);transition:background .2s}
.crow.next .m,.crow:hover .m{background:var(--accent)}
.crow .n{font-size:16px;letter-spacing:-.2px;line-height:1.3}
.crow .d{font-size:13px;color:var(--muted);margin-top:3px;line-height:1.4}

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
.field span{display:flex;align-items:center;gap:8px;font:var(--label-font);color:var(--muted);margin-bottom:8px}
.field span i{width:6px;height:6px;border-radius:50%;background:var(--accent)}
.inp{width:100%;height:52px;border-radius:16px;border:0;background:var(--wash);padding:0 16px;font-size:16px;outline:none;transition:box-shadow .2s,background .2s}
textarea.inp{height:150px;padding:14px 16px;resize:vertical;line-height:1.5}
.inp:focus{box-shadow:inset 0 0 0 1.5px var(--accent);background:transparent}
.seg{display:flex;flex-wrap:wrap;gap:6px}
.seg button{height:34px;padding:0 13px;border-radius:99px;background:var(--wash);font-size:13px;color:var(--muted);transition:background .2s,color .2s}
.seg button.on{background:var(--ink);color:var(--tile)}

/* prose */
.prose{font-size:18px;line-height:1.7;max-width:68ch}
.prose p{margin:0 0 1.15em}
.prose h2{font-weight:300;font-size:34px;letter-spacing:-.035em;line-height:1.1;margin:1.6em 0 .6em;scroll-margin-top:24px}
.prose h3{font-weight:400;font-size:20px;letter-spacing:-.3px;margin:1.4em 0 .4em}
.prose li{margin:0 0 .6em 1.1em}
.prose a{text-decoration:underline;text-decoration-color:var(--accent);text-underline-offset:3px}

footer{margin-top:96px;padding:28px 0 44px;border-top:1px solid var(--hair);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center}
footer .links{display:flex;gap:18px;flex-wrap:wrap;font:var(--label-font);color:var(--muted)}
footer .links a:hover{color:var(--ink)}

/* ——— home widgets ——— */
.home{display:grid;grid-template-columns:repeat(4,var(--cell));grid-auto-rows:var(--cell);gap:var(--gap)}
.home .tile{height:100%}
.w2{grid-column:span 2}
.hero{grid-column:span 2;display:flex;flex-direction:column;justify-content:space-between;padding:4px 8px 4px 0}
.hero h1{font-weight:300;font-size:62px;line-height:.98;letter-spacing:-.045em}
.hero h1 span{color:var(--accent)}
.hero p{font-size:14px;line-height:1.5;color:var(--muted);max-width:46ch;margin-bottom:16px}
.cta{display:flex;gap:8px;flex-wrap:wrap}
.player .pcov{position:absolute;left:24px;top:24px;width:248px;height:248px;border-radius:24px;overflow:hidden}
.player .art{position:absolute;inset:0;transition:transform .5s cubic-bezier(.65,0,.35,1),opacity .5s;border-radius:0}
.player .label.abs{left:300px}
.eq{position:absolute;left:426px;top:24px;width:30px;height:14px}
.eq b{position:absolute;bottom:0;width:3px;border-radius:2px;background:var(--accent);height:3px}
.ttl{position:absolute;left:300px;top:64px;right:26px;font-size:24px;letter-spacing:-.6px;line-height:1.12;transition:opacity .15s}
.by{position:absolute;left:301px;top:132px;font-size:14px;color:var(--muted);transition:opacity .15s}
.prog{position:absolute;left:300px;top:186px;width:288px;height:5px;border-radius:99px;background:var(--track);overflow:hidden}
.prog .f{position:absolute;inset:0 auto 0 0;border-radius:99px;background:var(--ink);width:0}
.knob{position:absolute;top:181px;width:15px;height:15px;margin-left:-7px;border-radius:50%;background:#fff;box-shadow:0 0 0 1px var(--hair),0 2px 6px rgba(0,0,0,.15);left:300px}
.times{position:absolute;top:202px;font:11px var(--mono);color:var(--muted)}
.ctl{position:absolute;top:232px;width:40px;height:40px;display:grid;place-items:center;border-radius:50%;transition:transform .15s,background .15s}
.ctl:active{transform:scale(.88);background:rgb(var(--ink-rgb)/.07)}
.play{position:absolute;left:420px;top:226px;width:52px;height:52px;display:grid;place-items:center;border-radius:50%;background:var(--ink);color:var(--tile)}
.cal .day{position:absolute;left:20px;top:64px;font-size:150px;font-weight:300;letter-spacing:-8px;line-height:1}
.cal .month{position:absolute;left:28px;top:222px;font-size:17px}
.cal .sum{position:absolute;left:28px;top:246px;font-size:13px;color:var(--muted)}
.cal .div{position:absolute;left:262px;top:28px;bottom:28px;width:1px;background:var(--line)}
.list{position:absolute;left:290px;top:34px;width:296px;height:232px;overflow:hidden}
.row{position:absolute;left:0;right:0;height:56px;display:flex;align-items:center;gap:14px;transition:top .6s cubic-bezier(.65,0,.35,1),opacity .6s}
.row .t{font:500 12px var(--mono);color:var(--muted);width:46px;flex:none}
.row .m{width:3px;height:30px;border-radius:2px;background:var(--marker);flex:none;transition:background .3s}
.row.next .m{background:var(--accent)}
.row .n,.row .d{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:126px}
.row .n{font-size:15px;letter-spacing:-.2px}
.row .d{font-size:12px;color:var(--muted);margin-top:2px}
.list .chip{position:absolute;right:0;top:16px;transition:opacity .2s}
.dialw{position:absolute;left:46px;top:56px}
.digits{position:absolute;left:46px;top:124px;width:200px;text-align:center;font-size:42px;font-weight:300;letter-spacing:-1.5px}
.digits small{font-size:18px;letter-spacing:0;color:var(--muted)}
.dcap{position:absolute;left:46px;top:178px;width:200px;text-align:center;font-size:13px;color:var(--muted)}
.focus .dark{position:absolute;inset:0;background:var(--focus-dark);opacity:0;transition:opacity .45s}
html.night .focus .dark{opacity:1}
html.night .focus{color:#f4f3f0}
.moon{position:absolute;left:24px;top:70px;transition:transform .45s,background .45s}
html.night .focus .moon{background:rgba(255,255,255,.1);transform:rotate(-40deg)}
.state{position:absolute;left:26px;top:160px;font-size:30px;font-weight:300;letter-spacing:-.8px}
.cap2{position:absolute;left:27px;top:200px;font-size:13px;color:var(--muted)}
.sw{position:absolute;left:26px;top:238px;width:60px;height:34px;border-radius:99px;background:var(--hair);transition:background .3s,transform .15s}
html.night .focus .sw{background:var(--accent)}
.sw b{position:absolute;left:3px;top:3px;width:28px;height:28px;border-radius:50%;background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.2);transition:transform .3s cubic-bezier(.33,1,.68,1)}
html.night .focus .sw b{transform:translateX(26px)}
.big{position:absolute;left:22px;top:58px;font-size:92px;font-weight:300;letter-spacing:-.04em;line-height:1}
.sky{position:absolute;left:27px;top:160px;font-size:15px}
.arcbox{position:absolute;left:24px;top:182px;overflow:visible}
.arcbox .dotted{fill:none;stroke:var(--dotted)}.arcbox .hz{stroke:var(--hair)}
.arcbox .lit{fill:none;stroke:var(--accent);stroke-linecap:round}.arcbox .pub{fill:var(--tile);stroke:var(--ink);stroke-width:1.5}
.tiny{position:absolute;top:268px;font:10.5px var(--mono);color:var(--muted)}
.cnt{position:absolute;left:24px;top:58px;font-size:54px;font-weight:300;letter-spacing:-.04em;line-height:1}
.goal{position:absolute;left:27px;top:118px;font-size:13px;color:var(--muted)}
.col{position:absolute;top:0}
.col .e,.col .b{position:absolute;left:0;top:166px;width:22px;height:90px;border-radius:7px}
.col .e{background:var(--wash)}
.col .b{background:var(--ink);opacity:.85;transform-origin:bottom;transform:scaleY(0);transition:transform .6s cubic-bezier(.34,1.56,.64,1)}
.col .b.hl{background:var(--accent);opacity:1}
.col .l{position:absolute;left:-6px;top:264px;width:34px;text-align:center;font:10.5px var(--mono);color:var(--muted)}
.devs{position:absolute;left:24px;right:26px;top:60px}
.share .h{position:absolute;left:26px;top:160px;font-size:30px;font-weight:300;letter-spacing:-.8px;line-height:1.05}
.share .s{position:absolute;left:27px;top:200px;font-size:13px;color:var(--muted);right:24px}
.share .go{position:absolute;left:26px;top:238px}
.share .well{position:absolute;left:24px;top:70px}
.mission{display:grid;grid-template-columns:var(--cell) 1fr;gap:var(--gap)}
.mission p{font-weight:300;font-size:40px;line-height:1.15;letter-spacing:-.035em}
.mission p span{color:var(--muted)}

/* publication cards */
.pubcard{display:grid;grid-template-columns:200px 1fr;gap:26px;padding:24px;align-items:center}
.pubcard h3{font-weight:400;font-size:24px;letter-spacing:-.6px;line-height:1.15;margin:10px 0 8px}
.pubcard p{color:var(--muted);font-size:14px;line-height:1.5}
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
.toc .crow{grid-template-columns:3px 1fr;padding:12px 0}
.toc .crow .m{height:26px}
.toc .crow .n{font-size:14px}
.atile{padding:30px 44px 50px}
.atile h1{font-weight:300;font-size:50px;line-height:1.02;letter-spacing:-.045em;margin:18px 0 18px;max-width:20ch}
.banner{border-radius:24px;overflow:hidden;margin:26px 0 8px}
.banner img{width:100%;max-height:440px;object-fit:cover;filter:grayscale(1) contrast(1.05)}
.capt{font-size:12px;color:var(--muted);margin-bottom:30px}

/* grants */
.gfind{display:grid;grid-template-columns:320px 1fr;gap:var(--gap);align-items:start}
.gside{display:grid;gap:var(--gap);position:sticky;top:20px}
.search{position:relative}
.search .inp{padding-left:44px}
.search svg{position:absolute;left:16px;top:17px;color:var(--muted)}
.fl{margin-top:18px}.fl > .label{margin-bottom:10px}
.gres{padding:6px 26px}
.grow{display:grid;grid-template-columns:62px 1fr 110px 88px;gap:18px;align-items:center;padding:16px 0;border-top:1px solid var(--line);cursor:pointer}
.grow:first-child{border-top:0}
.grow .dd{text-align:center}
.grow .dd b{display:block;font-weight:300;font-size:30px;letter-spacing:-1px;line-height:1}
.grow .dd span{font:10.5px var(--mono);color:var(--muted);text-transform:uppercase}
.grow .n{font-size:16px;letter-spacing:-.2px;line-height:1.3}
.grow .f{font-size:13px;color:var(--muted);margin-top:2px}
.grow .amt{font:13px var(--mono);text-align:right}
.grow .st{text-align:right}
.grow.closed{opacity:.55}
.gdetail{grid-column:1/-1;display:none;padding:4px 0 6px 80px;color:var(--muted);font-size:14px;line-height:1.55}
.grow.x .gdetail{display:block}
.gdetail .btn{margin-top:12px}
.count-num{font-weight:300;font-size:64px;letter-spacing:-.05em;line-height:1;margin-top:20px}

/* indicators */
.ind{padding:22px 26px 22px;min-height:292px;position:relative}
.ind .val{font-weight:300;font-size:64px;letter-spacing:-.045em;line-height:1;margin-top:26px}
.ind .val small{font-size:18px;letter-spacing:0;color:var(--muted);margin-left:6px}
.ind .desc{font-size:13px;color:var(--muted);line-height:1.5;margin-top:10px;max-width:46ch}
.ind svg{display:block;width:100%;height:96px;margin-top:16px;overflow:visible}
.ind .yrs{display:flex;justify-content:space-between;font:10.5px var(--mono);color:var(--muted);margin-top:6px}
.note{display:flex;gap:10px;align-items:center;padding:14px 18px;border-radius:18px;background:var(--wash);font-size:13px;color:var(--muted);margin-bottom:var(--gap)}

/* checklist (grant help) */
.check{display:grid;grid-template-columns:28px 1fr;gap:14px;padding:16px 0;border-top:1px solid var(--line);cursor:pointer;text-align:left;width:100%}
.check:first-child{border-top:0}
.check .bx{width:24px;height:24px;border-radius:8px;box-shadow:inset 0 0 0 1.5px var(--hair);display:grid;place-items:center;transition:background .2s,box-shadow .2s;color:#fff}
.check.done .bx{background:var(--accent);box-shadow:none}
.check b{font-weight:400;font-size:16px;letter-spacing:-.2px}
.check p{font-size:14px;color:var(--muted);line-height:1.5;margin-top:4px}
.check.done b{text-decoration:line-through;text-decoration-color:var(--accent)}

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
  .w2,.hero{grid-column:auto}.hero{grid-row:span 2}.hero h1{font-size:54px}
  .player,.cal{grid-row:span 2}
  .player .pcov{width:calc(100% - 48px);height:230px}
  .player .label.abs{left:26px;top:272px}.eq{left:auto;right:26px;top:272px}
  .ttl{left:26px;top:304px;font-size:22px}.by{left:27px;top:366px}
  .prog{left:26px;top:420px;width:calc(100% - 52px)}.knob{top:415px}.times{top:436px}
  #el{left:26px!important}#len{left:auto!important;right:26px}
  .ctl,.play{top:476px}.play{top:470px;left:calc(50% - 26px)}#prev{left:calc(50% - 90px)!important}#next{left:calc(50% + 50px)!important}
  .cal .div{display:none}.list{left:26px;top:300px;width:calc(100% - 52px)}.row .n,.row .d{max-width:60vw}
  .ph{grid-template-columns:1fr}.ph h1{font-size:44px}
  .pubcard{grid-template-columns:1fr}.pubcard .cover{max-width:160px}
  .atile{padding:24px 22px 36px}.atile h1{font-size:36px}
  .prose{font-size:17px}
  .grow{grid-template-columns:52px 1fr 78px}.grow .amt{display:none}.gdetail{padding-left:0}
  .crow{grid-template-columns:3px 1fr}.crow .t,.crow > .chip{display:none}
  .mission p{font-size:30px}.shead h2{font-size:38px}
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

HEAD_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400&family=Geist+Mono:wght@400;500&family=Inter:wght@400&display=swap" rel="stylesheet">'

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
      <button class="mini-sw" role="switch" aria-checked="false" aria-label="Reading mode" data-night><b>{icon('moon', 12)}</b></button>
      <button class="menu-btn" aria-label="Menu" aria-controls="nav" aria-expanded="false">{icon('menu')}</button>
    </div>
  </header>
  <main id="main">
{body}
  </main>
  <footer>
    <span class="mono" style="font-size:11px;color:var(--muted)">© 2026 e3 Initiative</span>
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
    soon = DATED_SOON[:6]
    nxt = soon[0]
    rows_js = [{"t": deadline_label(g), "n": g["name"], "d": f'{g["funder"].split(" (")[0]} · {money(g.get("amountMax"))}', "chip": f"in {days_left(g)} days"} for g in soon]
    cats = {}
    for g in OPEN:
        cats[g["category"]] = cats.get(g["category"], 0) + 1
    top = sorted(cats.items(), key=lambda x: -x[1])[:7]
    grp = lambda c: (sum(1 for g in GRANTS if g["category"] == c and status(g) != "closed"), sum(1 for g in GRANTS if g["category"] == c))
    mi, wo, ve = grp("minority_owned"), grp("women_owned"), grp("veteran_owned")
    pieces = [{"t": p["title"].split(":")[0], "by": f'{p["author"]} · {p["kind"]}', "len": p["min"], "href": p["slug"] + ".html"} for p in PUBS]
    import json as _j
    body = f"""
<div class="home">
  <div class="hero">
    {label('Equity · Economics · Ethnicity')}
    <h1>{TAGLINE}<span>.</span></h1>
    <div><p>{LEDE}</p><div class="cta"><a class="btn" href="research.html">Read the research</a><a class="btn ghost" href="grants.html">Find a grant</a></div></div>
  </div>
  <div class="tile w2 player rise">
    <div class="pcov">
      <div class="art cover cv-a"><span class="mk">E3—01</span></div>
      <div class="art cover cv-b" style="transform:translateX(110%)"><span class="mk">E3—02</span></div>
      <div class="art cover cv-c" style="transform:translateX(110%)"><span class="mk">E3—03</span></div>
    </div>
    {label('Now reading', 'abs')}
    <div class="eq" aria-hidden="true">{''.join(f'<b style="left:{i*6}px"></b>' for i in range(5))}</div>
    <a class="ttl" id="ttl" href="#"></a><div class="by" id="by"></div>
    <div class="prog"><div class="f" id="pf"></div></div><div class="knob" id="pk"></div>
    <div class="times" id="el" style="left:300px">0:00</div><div class="times" id="len" style="left:540px"></div>
    <button class="ctl" style="left:348px" id="prev" aria-label="Previous piece"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M7 6h2v12H7zM20 6v12l-9-6z"/></svg></button>
    <button class="play" id="play" aria-label="Pause"><svg id="pi" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg></button>
    <button class="ctl" style="left:504px" id="next" aria-label="Next piece"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M15 6h2v12h-2zM4 6v12l9-6z"/></svg></button>
  </div>
  <a class="tile w2 cal rise" href="grants.html">
    {label(TODAY.strftime('%A'), 'abs')}
    <div class="day">{TODAY.day}</div><div class="month">{TODAY.strftime('%B')}</div>
    <div class="sum">{sum(1 for g in DATED_SOON if days_left(g) <= 30)} grant deadlines in 30 days</div>
    <div class="div"></div><div class="list" id="list"><span class="chip a" id="chip"></span></div>
  </a>
  <div class="tile rise">
    {label('Next deadline', 'abs')}
    <svg class="dial dialw" data-lit="{days_left(nxt)}" width="200" height="200" viewBox="0 0 200 200" aria-hidden="true"></svg>
    <div class="digits"><span data-count="{days_left(nxt)}">0</span><small> days</small></div>
    <div class="dcap">{esc(nxt['name'])}</div>
  </div>
  <div class="tile focus rise">
    <div class="dark"></div>
    {label('Reading mode', 'abs')}
    <div class="well lg moon">{icon('moon', 26)}</div>
    <div class="state" data-night-state>Off</div><div class="cap2" data-night-cap>Paper, for daytime</div>
    <button class="sw" role="switch" aria-checked="false" aria-label="Reading mode" data-night><b></b></button>
  </div>
  <div class="tile rise">
    {label(f'{TODAY.year} so far', 'abs')}<div class="tr">Feb · Mar · Oct</div>
    <div class="big" data-count="{len(PUBS)}">0</div><div class="sky">Pieces published</div>
    <svg class="arcbox" width="248" height="86" viewBox="0 0 248 86" aria-hidden="true">
      <path id="arcd" class="dotted" d="M8 76 C 60 -14, 188 -14, 240 76" stroke-width="1.2" stroke-dasharray="2 4"/>
      <line class="hz" x1="0" x2="248" y1="76" y2="76"/>
      <path id="arcl" class="lit" d="M8 76 C 60 -14, 188 -14, 240 76" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
      <g id="stops"></g><circle id="glow" r="14" fill="var(--sun-glow)" opacity="0"/><circle id="sun" r="6" fill="var(--accent)" opacity="0"/>
    </svg>
    <div class="tiny" style="left:26px">Jan</div><div class="tiny" style="right:26px">Dec</div>
  </div>
  <a class="tile rise" href="grants.html">
    {label('Open grants', 'abs')}
    <div class="cnt" data-count="{len(OPEN)}">0</div><div class="goal">of {len(GRANTS)} tracked · {round(len(OPEN)/len(GRANTS)*100)}%</div>
    <div id="cols">{''.join(f'<div class="col" style="left:{26+i*35}px"><div class="e"></div><div class="b{" hl" if i==0 else ""}" data-h="{n/top[0][1]:.2f}"></div><div class="l">{CAT_LABEL[c][:2]}</div></div>' for i,(c,n) in enumerate(top))}</div>
  </a>
  <div class="tile rise">
    {label("Who it's for", 'abs')}
    <div class="devs">
      <a href="minority-owned-business-grants.html">{lvl('people', 'Minority-owned', mi[0]/mi[1]*100, True)}</a>
      <a href="women-owned-business-grants.html">{lvl('person', 'Women-owned', wo[0]/wo[1]*100)}</a>
      <a href="veteran-owned-business-grants.html">{lvl('shield', 'Veteran-owned', ve[0]/ve[1]*100)}</a>
    </div>
  </div>
  <a class="tile share rise" href="outreach.html">
    {label('Outreach', 'abs')}<div class="well lg">{icon('mic', 24)}</div>
    <div class="h">Share your story</div><div class="s">An interview, on your terms.</div><span class="btn sm go">Book a time →</span>
  </a>
</div>
<section>
  <div class="shead"><h2>Publications</h2><a href="articles.html">All articles →</a></div>
  <div class="tile rows">{''.join(crow(p['short'][:6], p['title'], p['summary'], p['slug'] + '.html', f'<span class="chip">{p["kind"]}</span>') for p in PUBS)}</div>
</section>
<section class="mission">{label('Mission')}<p>{MISSION.replace(', fostering', ', <span>fostering').replace('backgrounds.', 'backgrounds.</span>')}</p></section>
"""
    js = f"""<script>
const PIECES = {_j.dumps(pieces)}, EVENTS = {_j.dumps(rows_js)};
let cur = 0, pos = 0.4, playing = !reduce; const arts = $$('.art');
function setText() {{ $('#ttl').textContent = PIECES[cur].t; $('#ttl').href = PIECES[cur].href; $('#by').textContent = PIECES[cur].by; $('#len').textContent = PIECES[cur].len + ' min'; }}
function show(i, dir) {{ const old = arts[cur]; cur = (i + 3) % 3; const nu = arts[cur];
  nu.style.transition = 'none'; nu.style.transform = `translateX(${{dir * 110}}%)`; nu.style.opacity = 1; nu.style.zIndex = 2; old.style.zIndex = 1;
  requestAnimationFrame(() => requestAnimationFrame(() => {{ nu.style.transition = ''; nu.style.transform = 'none'; old.style.transform = `translateX(${{-dir * 40}}px) scale(.94)`; old.style.opacity = .1; }}));
  ['#ttl', '#by'].forEach(s => $(s).style.opacity = 0); setTimeout(() => {{ setText(); ['#ttl', '#by'].forEach(s => $(s).style.opacity = 1); }}, 150); pos = 0; }}
setText(); $('#next').onclick = () => show(cur + 1, 1); $('#prev').onclick = () => show(cur - 1, -1);
$('#play').onclick = () => {{ playing = !playing; $('#play').setAttribute('aria-label', playing ? 'Pause' : 'Play'); $('#pi').innerHTML = playing ? '<path d="M7 5h4v14H7zM13 5h4v14h-4z"/>' : '<path d="M8 5v14l11-7z"/>'; }};
const bars = $$('.eq b'); let last = performance.now();
(function loop(now) {{ const dt = (now - last) / 1000; last = now; if (playing) pos += dt * 0.05;
  const f = Math.min(1, pos / PIECES[cur].len), w = $('.prog').offsetWidth; $('#pf').style.width = w * f + 'px'; $('#pk').style.left = $('.prog').offsetLeft + w * f + 'px';
  $('#el').textContent = Math.floor(pos) + ':' + String(Math.floor((pos % 1) * 60)).padStart(2, '0');
  bars.forEach((b, i) => b.style.height = (playing ? 4 + 10 * Math.abs(Math.sin(now / 1000 * (5 + i * 1.7) + i)) : 3) + 'px'); requestAnimationFrame(loop); }})(last);
const rows = EVENTS.map(e => {{ const r = document.createElement('div'); r.className = 'row'; r.innerHTML = `<span class="t">${{e.t}}</span><span class="m"></span><div><div class="n">${{e.n}}</div><div class="d">${{e.d}}</div></div>`; $('#list').insertBefore(r, $('#chip')); return r; }});
let top0 = 0; function place() {{ rows.forEach((r, i) => {{ const k = i - top0; r.style.top = k * 76 + 'px'; r.style.opacity = k >= 0 && k < 3 ? 1 : 0; r.classList.toggle('next', k === 0); }});
  $('#chip').style.opacity = 0; setTimeout(() => {{ $('#chip').textContent = EVENTS[top0].chip; $('#chip').style.opacity = 1; }}, 300); }}
place(); if (!reduce) setInterval(() => {{ top0 = (top0 + 1) % (EVENTS.length - 2); place(); }}, 3600);
const arcd = $('#arcd'), AL = arcd.getTotalLength();
[0.09, 0.19, 0.76].forEach(k => {{ const p = arcd.getPointAtLength(AL * k), c = document.createElementNS(SVG, 'circle'); c.setAttribute('cx', p.x); c.setAttribute('cy', p.y); c.setAttribute('r', 3.5); c.setAttribute('class', 'pub'); $('#stops').appendChild(c); }});
const SUN = ({TODAY.timetuple().tm_yday} / 365);
setTimeout(() => {{ ['#sun', '#glow'].forEach(s => $(s).setAttribute('opacity', 1)); const t0 = performance.now();
  (function s(now) {{ const k = reduce ? 1 : Math.min(1, (now - t0) / 1600), p = arcd.getPointAtLength(AL * SUN * inOut(k));
    ['#sun', '#glow'].forEach(x => {{ $(x).setAttribute('cx', p.x); $(x).setAttribute('cy', p.y); }}); $('#arcl').setAttribute('stroke-dashoffset', 1 - SUN * inOut(k)); $('#glow').setAttribute('r', 12 + 3 * Math.sin(now / 333)); if (!reduce) requestAnimationFrame(s); }})(t0); }}, 1000);
$$('.col .b').forEach((b, i) => setTimeout(() => b.style.transform = `scaleY(${{b.dataset.h}})`, 1100 + i * 80));
</script>"""
    return shell("index", body, js)


def pub_list(page, kicker, title, lede, items, extra=""):
    cards = "".join(f"""<a class="tile pubcard rise c12" href="{p['slug']}.html">
      <div class="cover photo"><img src="{IMG}{p['img']}" alt="{esc(p['alt'])}" loading="lazy"></div>
      <div>{label(f"{p['kind']} · {p['date']}")}<h3>{esc(p['title'])}</h3><p>{esc(p['summary'])}</p>
        <div class="meta"><span class="playb">{icon('play', 16)}</span><span class="pbar"><b style="width:0"></b></span><span class="mono muted" style="font-size:11px">{p['min']} min · {p['author']}</span></div></div></a>"""
        for p in items)
    return shell(page, ph(kicker, title, lede) + f'<div class="grid">{cards}</div>{extra}')


def article(p):
    a = p["data"]
    toc, body = [], []
    for i, (t, txt) in enumerate(a["blocks"]):
        if t == "h2":
            toc.append((f"s{i}", re.sub(r"<[^>]+>", "", txt)))
            body.append(f'<h2 id="s{i}">{txt}</h2>')
        elif t == "li":
            body.append(f"<ul><li>{txt}</li></ul>")
        else:
            body.append(f"<{t}>{txt}</{t}>")
    toc_html = "".join(f'<a class="crow" href="#{i}" data-sec="{i}"><span class="m"></span><div><div class="n">{esc(n)}</div></div></a>' for i, n in toc)
    banner = f'<div class="banner"><img src="{IMG}{p["img"].replace("-640", "")}" alt="{esc(p["alt"])}"></div><div class="capt">{esc(a["caption"] or p["alt"])}</div>'
    cite = {"article-railroad": "chinese-labor-transcontinental-railroad-citations.html", "article-chinatown": "chinatown-citations.html", "research-chinatown": "chinatown-solidarity-paper-citations.html"}[p["slug"]]
    folder = "articles" if p["kind"] == "Article" else "research"
    body_html = f"""
<div class="read">
  <aside class="side">
    <div class="tile pad rise">
      {label('Now reading')}
      <div style="font-size:18px;letter-spacing:-.3px;line-height:1.25;margin-top:14px">{esc(p['title'].split(':')[0])}</div>
      <div class="rprog"><b id="rb"></b><i id="rk"></i></div>
      <div style="display:flex;justify-content:space-between" class="mono muted"><span style="font-size:11px" id="rl">0 min</span><span style="font-size:11px">{p['min']} min</span></div>
    </div>
    {f'<nav class="tile rows toc rise" aria-label="Contents">{toc_html}</nav>' if toc else ''}
    <a class="tile pad rise" href="../../{folder}/{cite}" style="display:flex;align-items:center;gap:14px"><span class="well">{icon('doc')}</span><span><b style="font-weight:400">Citations and sources</b><br><span class="muted" style="font-size:13px">On the live site</span></span></a>
  </aside>
  <article class="tile atile rise">
    {label(f"{p['kind']} · {p['date']}")}
    <h1>{esc(p['title'])}</h1>
    <div class="mono muted" style="font-size:12px">{esc(a['byline'] or 'By ' + p['author'])}</div>
    {banner}
    <div class="prose" id="prose">{''.join(body)}</div>
  </article>
</div>"""
    js = f"""<script>
const pr = $('#prose'), total = {p['min']};
function upd() {{ const r = pr.getBoundingClientRect(), k = Math.max(0, Math.min(1, (innerHeight * .4 - r.top) / r.height));
  $('#rb').style.width = k * 100 + '%'; $('#rk').style.left = k * 100 + '%'; $('#rl').textContent = Math.round(k * total) + ' min';
  let cur = null; $$('#prose h2').forEach(h => {{ if (h.getBoundingClientRect().top < innerHeight * .35) cur = h.id; }});
  $$('[data-sec]').forEach(a => a.classList.toggle('next', a.dataset.sec === cur)); }}
addEventListener('scroll', upd, {{ passive: true }}); upd();
</script>"""
    return shell(p["slug"], body_html, js)


def about():
    team = "".join(f"""<div class="tile pad rise c4"><div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div class="cover {COVERS[i]}" style="width:88px;border-radius:22px"></div><span class="chip{' a' if i < 2 else ''}">{r}</span></div>
        <div style="font-weight:300;font-size:30px;letter-spacing:-.8px;line-height:1.05;margin:26px 0 10px">{n}</div><p class="muted" style="font-size:14px;line-height:1.55">{b}</p></div>"""
        for i, (n, r, b) in enumerate(ABOUT["team"]))
    appr = "".join(f'<div class="tile pad rise c4"><div class="well lg">{icon(ic, 24)}</div><div style="font-weight:300;font-size:26px;letter-spacing:-.6px;margin:22px 0 8px">{t}</div><p class="muted" style="font-size:14px;line-height:1.5">{d}</p></div>'
        for (t, d), ic in zip(ABOUT["approach"], ["mic", "hands", "spark"]))
    body = ph("About", "About e3 Initiative", "", f'<div class="seg"><a class="btn ghost" href="contact.html">Get in touch</a></div>') + f"""
<div class="grid">
  <div class="tile pad rise c6">{label('Who we are')}<p style="font-weight:300;font-size:26px;line-height:1.25;letter-spacing:-.6px;margin-top:18px">{ABOUT['who']}</p></div>
  <div class="tile pad rise c6">{label('What we do')}<p style="font-weight:300;font-size:26px;line-height:1.25;letter-spacing:-.6px;margin-top:18px">{ABOUT['what']}</p></div>
</div>
<section><div class="shead"><h2>Our team</h2></div><div class="grid">{team}</div></section>
<section><div class="shead"><h2>Our approach</h2><span class="muted" style="font:var(--label-font)">We believe in</span></div><div class="grid">{appr}</div></section>"""
    return shell("about", body)


def journals():
    t, logo = JOURNAL
    body = ph("Publications", "Journals", "Browse our academic journals and long-form publications. Each journal entry includes comprehensive analysis and scholarly insights.") + f"""
<div class="grid">
  <div class="tile pad rise c5" style="display:grid;place-items:center;min-height:360px"><img src="{IMG}{logo}" alt="{esc(t)}" width="240" height="240" style="border-radius:24px"></div>
  <div class="tile pad rise c7" style="display:flex;flex-direction:column;justify-content:space-between;min-height:360px">
    <div>{label('Journal')}<div style="font-weight:300;font-size:40px;letter-spacing:-1.2px;line-height:1.05;margin-top:18px">{t}</div></div>
    <div class="tile" style="box-shadow:none;background:var(--wash);border-radius:24px;padding:20px;display:flex;gap:16px;align-items:center">
      <svg class="dial" data-lit="0" width="64" height="64" viewBox="0 0 200 200" aria-hidden="true"></svg>
      <div><b style="font-weight:400">Entries coming soon</b><div class="muted" style="font-size:13px;margin-top:2px">New long-form work will appear here first.</div></div></div>
  </div>
</div>"""
    return shell("journals", body)


def grants():
    groups = "".join(f'<a href="{slug}.html">{lvl(ic, CAT_LABEL[cat], sum(1 for g in GRANTS if g["category"]==cat and status(g)!="closed")/sum(1 for g in GRANTS if g["category"]==cat)*100, i==0)}</a>'
        for i, ((slug, (cat, _, _)), ic) in enumerate(zip(CATEGORY_PAGES.items(), ["people", "person", "shield"])))
    cats = "".join(f'<button data-v="{k}">{v}</button>' for k, v in CAT_LABEL.items())
    body = ph("Grants", "Grant Finder", "Funding for small businesses and nonprofits. Search by keyword, or filter by who qualifies, category, award size and deadline.",
        f'<a class="btn ghost" href="grant-help.html">Help & tips →</a>') + f"""
<div class="gfind">
  <aside class="gside">
    <div class="tile pad rise">
      {label('Search')}
      <div class="search" style="margin-top:12px">{icon('search')}<input class="inp" id="q" type="search" placeholder="Women-owned bakery…" aria-label="Search grants"></div>
      <div class="fl">{label('Who qualifies')}<div class="seg" data-f="elig"><button class="on" data-v="">Anyone</button><button data-v="small_business">Business</button><button data-v="nonprofit">Nonprofit</button></div></div>
      <div class="fl">{label('Status')}<div class="seg" data-f="status"><button class="on" data-v="live">Open + rolling</button><button data-v="open">Open</button><button data-v="">All</button></div></div>
      <div class="fl">{label('Award up to at least')}<div class="seg" data-f="amt"><button class="on" data-v="0">Any</button><button data-v="10000">$10k</button><button data-v="50000">$50k</button><button data-v="250000">$250k</button></div></div>
      <div class="fl">{label('Category')}<div class="seg" data-f="cat" data-multi><button class="on" data-v="">All</button>{cats}</div></div>
    </div>
    <div class="tile pad rise" style="display:flex;gap:18px;align-items:center">
      <svg class="dial" id="gdial" width="96" height="96" viewBox="0 0 200 200" aria-hidden="true"></svg>
      <div>{label('Matching')}<div class="count-num" id="gcount" style="margin-top:6px;font-size:48px">0</div><div class="muted" style="font-size:13px">of {len(GRANTS)} grants</div></div>
    </div>
    <div class="tile pad rise">{label('Browse by group')}<div style="margin-top:6px">{groups}</div></div>
  </aside>
  <div class="tile gres rise" id="gres" aria-live="polite"></div>
</div>"""
    js = """<script src="../shared/grants-data.js"></script><script>
const F = { q: '', elig: '', status: 'live', amt: 0, cat: new Set() };
const setDial = buildDial($('#gdial'), 0, 200);
$$('.seg[data-f]').forEach(seg => seg.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; const f = seg.dataset.f;
  if (seg.hasAttribute('data-multi')) { if (!b.dataset.v) { F.cat.clear(); $$('button', seg).forEach(x => x.classList.toggle('on', !x.dataset.v)); }
    else { F.cat.has(b.dataset.v) ? F.cat.delete(b.dataset.v) : F.cat.add(b.dataset.v); b.classList.toggle('on'); $('button[data-v=""]', seg).classList.toggle('on', !F.cat.size); } }
  else { $$('button', seg).forEach(x => x.classList.toggle('on', x === b)); F[f] = f === 'amt' ? +b.dataset.v : b.dataset.v; } render(); }));
$('#q').addEventListener('input', e => { F.q = e.target.value.toLowerCase(); render(); });
function render() {
  const rs = GRANTS.filter(g => (!F.q || (g.name + g.funder + g.desc + CAT_LABEL[g.cat]).toLowerCase().includes(F.q))
    && (!F.elig || g.elig === F.elig || g.elig === 'both') && (F.status === '' || (F.status === 'live' ? g.status !== 'closed' : g.status === F.status))
    && (!F.amt || g.max >= F.amt) && (!F.cat.size || F.cat.has(g.cat)))
    .sort((a, b) => ({ open: 0, rolling: 1, closed: 2 }[a.status] - { open: 0, rolling: 1, closed: 2 }[b.status]) || (a.days ?? 999) - (b.days ?? 999));
  $('#gcount').textContent = rs.length; setDial(Math.round(rs.length / GRANTS.length * 60));
  $('#gres').innerHTML = rs.length ? rs.map(g => { const dt = g.days != null ? g.dl.split(' ') : null;
    return `<div class="grow ${g.status}" tabindex="0"><div class="dd">${dt ? `<b>${+dt[1]}</b><span>${dt[0]}</span>` : `<b style="font-size:20px">∞</b><span>${g.dl}</span>`}</div>
      <div><div class="n">${g.name}</div><div class="f">${g.funder} · ${CAT_LABEL[g.cat]}</div></div><div class="amt">${g.max ? 'up to $' + g.max.toLocaleString() : 'Varies'}</div>
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
    cat, title, what = CATEGORY_PAGES[slug]
    intro, gs = category_intro(cat, what)
    gs = sorted(gs, key=lambda g: ({"open": 0, "rolling": 1, "closed": 2}[status(g)], days_left(g) if days_left(g) is not None else 999))
    c = {s: sum(1 for g in gs if status(g) == s) for s in ("open", "rolling", "closed")}
    rows = "".join(crow(deadline_label(g), esc(g["name"]), esc(g["funder"]) + " · " + esc(g["amount"]), g["link"], status_chip(status(g), days_left(g)), status(g) == "open") for g in gs)
    others = "".join(f'<a class="btn ghost" href="{s}.html">{CAT_LABEL[v[0]]}</a>' for s, v in CATEGORY_PAGES.items() if s != slug)
    body = ph("Grant list", title, intro) + f"""
<div class="grid">
  <div class="tile pad rise c4">{label('In this list')}<div class="count-num" data-count="{len(gs)}">0</div>
    <div style="margin-top:14px">{lvl('spark', 'Open now', c['open']/len(gs)*100, True)}{lvl('link', 'Rolling', c['rolling']/len(gs)*100)}{lvl('doc', 'Closed for now', c['closed']/len(gs)*100)}</div></div>
  <div class="tile rows rise c8">{rows}</div>
  <div class="tile pad rise c6">{label('Before you apply')}{''.join(f'<div class="check done" style="cursor:default"><span class="bx">{icon("check", 14)}</span><div><b style="text-decoration:none">{a}</b><p>{b}</p></div></div>' for a, b in BEFORE_APPLY)}</div>
  <div class="tile pad rise c6">{label('More grant lists')}<div class="seg" style="margin-top:16px;gap:10px">{others}<a class="btn" href="grants.html">Search all {len(GRANTS)}</a><a class="btn ghost" href="grant-help.html">Tips & free help</a></div></div>
</div>"""
    return shell(slug, body)


def grant_help():
    tips = "".join(f'<button class="check" data-i="{i}"><span class="bx">{icon("check", 14)}</span><div><b>{a}</b><p>{b}</p></div></button>' for i, (a, b) in enumerate(HELP["tips"]))
    orgs = "".join(f'<a class="tile pad rise c3" href="{u}" target="_blank" rel="noopener" style="display:flex;flex-direction:column;justify-content:space-between;min-height:250px"><div><span class="well">{icon("link")}</span><div style="font-size:18px;letter-spacing:-.3px;line-height:1.2;margin:16px 0 8px">{n}</div><p class="muted" style="font-size:13px;line-height:1.5">{d}</p></div><span class="btn sm" style="align-self:flex-start;margin-top:16px">{l} →</span></a>' for n, d, l, u in HELP["orgs"])
    body = ph("Grants", "Grant Help & Tips", HELP["intro"], '<a class="btn" href="grants.html">Search grants →</a>') + f"""
<div class="grid">
  <div class="tile rows rise c8" style="padding-top:18px">{label('How to write a strong application · tick them off')}<div style="margin-top:6px">{tips}</div></div>
  <div style="display:grid;gap:var(--gap);align-content:start" class="c4">
    <div class="tile pad rise" style="text-align:center">{label('Your progress')}
      <div style="position:relative;width:200px;height:200px;margin:14px auto 0"><svg class="dial" id="hdial" width="200" height="200" viewBox="0 0 200 200" aria-hidden="true"></svg>
      <div style="position:absolute;inset:0;display:grid;place-items:center"><div><div class="thin" style="font-size:44px" id="hcount">0/8</div><div class="muted" style="font-size:13px;margin-top:4px">steps done</div></div></div></div></div>
    <div class="tile rows rise" style="padding-top:18px">{label('Common mistakes')}{''.join(f'<div class="crow" style="grid-template-columns:3px 1fr;padding:12px 0"><span class="m" style="height:22px"></span><div class="d" style="margin:0;font-size:14px">{m}</div></div>' for m in HELP['mistakes'])}</div>
  </div>
</div>
<section><div class="shead"><h2>Where to get free help</h2></div><p class="muted" style="margin:-8px 0 20px;max-width:60ch">You don't have to do this alone. These organizations offer free, expert help finding funding and preparing applications. Most are government-funded or nonprofit.</p><div class="grid">{orgs}</div></section>
<section class="grid"><div class="tile pad rise c8" style="display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap"><div>{label('Still have questions?')}<p style="font-weight:300;font-size:26px;letter-spacing:-.6px;margin-top:12px">We're happy to point you in the right direction.</p></div><a class="btn" href="contact.html">Contact the team →</a></div>
<div class="tile pad rise c4"><p class="muted" style="font-size:13px;line-height:1.55">{HELP['disclaimer']}</p></div></section>"""
    js = """<script>
const setH = buildDial($('#hdial'), 0, 200), done = new Set(JSON.parse(localStorage.getItem('e3-help') || '[]'));
function upd() { $$('.check[data-i]').forEach(c => c.classList.toggle('done', done.has(+c.dataset.i))); $('#hcount').textContent = done.size + '/8'; setH(Math.round(done.size / 8 * 60)); localStorage.setItem('e3-help', JSON.stringify([...done])); }
$$('.check[data-i]').forEach(c => c.addEventListener('click', () => { const i = +c.dataset.i; done.has(i) ? done.delete(i) : done.add(i); upd(); })); setTimeout(upd, 900);
</script>"""
    return shell("grant-help", body, js)


def indicators():
    tiles = "".join(f"""<div class="tile ind rise c6" data-key="{k}" data-unit="{u}">
      {label(f'{grp}: {name}')}<div class="tr mono" data-hl></div>
      <div class="val"><span data-v>—</span><small>{u if u != 'index' else 'index'}</small></div>
      <svg viewBox="0 0 500 96" preserveAspectRatio="none" aria-hidden="true"></svg>
      <div class="yrs"><span>2000</span><span data-end>today</span></div>
      <p class="desc">{d}</p></div>""" for k, grp, name, u, d in INDICATORS)
    body = ph("Data", "Economic Indicators", "These charts help explain everyday costs, job security, and borrowing rates. Hover a chart to read any year since 2000.") + f"""
<div class="note" id="note" hidden>{icon('spark')}<span>Preview: these lines are placeholder shapes. Live FRED data loads from <span class="mono">/api/economic-indicators</span> on the deployed site, and no numbers are shown until then.</span></div>
<div class="grid">{tiles}</div>"""
    js = """<script src="../shared/indicators.js"></script><script>
loadIndicators().then(D => {
  $('#note').hidden = D.live;
  $$('.ind').forEach(t => { const s = D.series[t.dataset.key]; if (!s) return; const svg = $('svg', t), n = s.length, lo = Math.min(...s), hi = Math.max(...s);
    const x = i => i / (n - 1) * 500, y = v => 86 - (v - lo) / (hi - lo || 1) * 76;
    const d = s.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1)).join(' ');
    svg.innerHTML = `<line x1="0" x2="500" y1="90" y2="90" stroke="var(--hair)"/><path d="${d}" fill="none" stroke="var(--dotted)" stroke-width="1.2" stroke-dasharray="2 4" vector-effect="non-scaling-stroke"/>
      <path class="ln" d="${d}" fill="none" stroke="var(--ink)" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" vector-effect="non-scaling-stroke" style="transition:stroke-dashoffset 1.4s cubic-bezier(.65,0,.35,1)"/>
      <circle cx="${x(n - 1)}" cy="${y(s[n - 1])}" r="12" fill="var(--sun-glow)"/><circle class="dot" cx="${x(n - 1)}" cy="${y(s[n - 1])}" r="5" fill="var(--accent)"/>`;
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
    body = ph("Outreach", "Outreach", "Interviews and partnerships: how community knowledge gets into our research.") + '<div class="grid">' + "".join(
        f"""<div class="tile pad rise c6" id="{k}" style="min-height:420px;display:flex;flex-direction:column;justify-content:space-between">
          <div style="display:flex;justify-content:space-between">{label(t)}<span class="chip">{s}</span></div>
          <div><div class="well lg" style="margin:30px 0 22px">{icon(ic, 26)}</div><p style="font-weight:300;font-size:24px;line-height:1.3;letter-spacing:-.5px">{p1}</p><p class="muted" style="margin-top:16px;font-size:14px;line-height:1.55">{p2}</p></div>
          <a class="btn" href="contact.html" style="align-self:flex-start;margin-top:24px">{'Share your story' if k == 'interview' else 'Partner with us'} →</a></div>"""
        for (k, (t, s, p1, p2)), ic in zip(OUTREACH.items(), ["mic", "hands"])) + "</div>"
    return shell("outreach", body)


def contact():
    body = ph("Contact", "Let's connect", "Have questions about our research or want to collaborate? Send a message and we will respond within two business days.") + f"""
<div class="grid">
  <form class="tile pad rise c8" id="cf" onsubmit="event.preventDefault();this.querySelector('[data-sent]').hidden=false" style="padding:30px">
    <div class="grid" style="gap:0 16px"><label class="field c6"><span><i></i>Name *</span><input class="inp" required autocomplete="name"></label>
    <label class="field c6"><span><i></i>Email *</span><input class="inp" type="email" required autocomplete="email"></label></div>
    <label class="field"><span><i></i>Subject *</span><input class="inp" required></label>
    <label class="field"><span><i></i>Message *</span><textarea class="inp" required></textarea></label>
    <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap"><button class="btn" type="submit">Send message →</button><span class="chip a" data-sent hidden>Mockup: nothing was sent</span></div>
  </form>
  <div class="c4" style="display:grid;gap:var(--gap);align-content:start">
    <div class="tile pad rise" style="display:flex;gap:16px;align-items:center"><svg class="dial" data-lit="10" width="88" height="88" viewBox="0 0 200 200" aria-hidden="true"></svg><div>{label('Reply within')}<div class="thin" style="font-size:36px;margin-top:6px">2 days</div><div class="muted" style="font-size:13px">business days</div></div></div>
    <a class="tile pad rise" href="outreach.html">{label('Want to be interviewed?')}<p class="muted" style="font-size:14px;margin-top:10px;line-height:1.5">Say so in your message and our outreach team will follow up.</p></a>
    <a class="tile pad rise" href="privacy.html">{label('Privacy')}<p class="muted" style="font-size:14px;margin-top:10px;line-height:1.5">We use your details only to reply. Read the policy →</p></a>
  </div>
</div>"""
    return shell("contact", body)


def privacy():
    out, toc, ul = [], [], False
    for i, (t, txt) in enumerate(PRIVACY):
        if t == "li":
            if not ul:
                out.append("<ul>"); ul = True
            out.append(f"<li>{txt}</li>"); continue
        if ul:
            out.append("</ul>"); ul = False
        if t == "h2":
            toc.append((f"p{i}", txt)); out.append(f'<h2 id="p{i}">{txt}</h2>')
        else:
            out.append(f"<{t}>{txt}</{t}>")
    if ul:
        out.append("</ul>")
    body = ph("Legal", "Privacy Policy", "The e3 Initiative is a small research organization. This page explains what information this website collects, why, and the choices you have.", '<span class="chip">Updated Nov 12, 2026</span>') + f"""
<div class="read"><nav class="side tile rows toc rise" aria-label="Contents">{''.join(f'<a class="crow" href="#{i}"><span class="m"></span><div><div class="n">{n}</div></div></a>' for i, n in toc)}</nav>
<article class="tile atile rise"><div class="prose">{''.join(out)}</div></article></div>"""
    return shell("privacy", body)


def notfound():
    body = f"""<div class="grid" style="margin-top:20px">
  <div class="tile rise c7" style="min-height:420px;position:relative;padding:26px">{label('Page not found')}
    <div class="thin" style="font-size:220px;letter-spacing:-12px;margin-top:40px">404</div>
    <p class="muted" style="max-width:40ch">Sorry, we couldn't find that page. It may have moved, or the link may be mistyped.</p></div>
  <div class="tile rows rise c5">{''.join(crow('→', t, '', h) for h, t in [('index.html', 'Go to the homepage'), ('articles.html', 'Browse articles'), ('research.html', 'Browse research'), ('grants.html', 'Search grants'), ('contact.html', 'Contact us')])}</div>
</div>"""
    return shell("404", body)


def build():
    write(f"{D}/theme.css", CSS)
    write(f"{D}/theme.js", JS)
    pages = {
        "index": home(), "about": about(), "journals": journals(), "grants": grants(), "grant-help": grant_help(),
        "economic-indicators": indicators(), "outreach": outreach(), "contact": contact(), "privacy": privacy(), "404": notfound(),
        "articles": pub_list("articles", "Publications", "Articles", "Perspectives and community insights from our team and partners, from grassroots organizing to systemic policy analysis.", ARTICLES),
        "research": pub_list("research", "Publications", "Research", "Research papers, reports, and briefs. Each publication includes clear summaries and next steps for community leaders and decision-makers.", RESEARCH,
            '<section><div class="shead"><h2>Also in Publications</h2></div><div class="grid"><a class="tile pad rise c6" href="journals.html">' + label("Journals") + '<p style="font-weight:300;font-size:24px;letter-spacing:-.5px;margin-top:12px">Critical Debates in Humanities, Science and Global Justice →</p></a><a class="tile pad rise c6" href="economic-indicators.html">' + label("Data") + '<p style="font-weight:300;font-size:24px;letter-spacing:-.5px;margin-top:12px">Economic indicators since 2000 →</p></a></div></section>'),
    }
    for p in PUBS:
        pages[p["slug"]] = article(p)
    for s in CATEGORY_PAGES:
        pages[s] = category(s)
    for k, v in pages.items():
        write(f"{D}/{k}.html", v)
    return sorted(pages)
