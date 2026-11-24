"""D preview v2: richer homepage with swappable colour/type themes. build(theme, out_html, selfhost)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
ROOT = "/home/user/e3website"
CITIES = ["ny", "chi", "sf", "la"]
CITY_NAMES = {"ny": "New York", "chi": "Chicago", "sf": "San Francisco", "la": "Los Angeles"}
PHOTO = json.load(open("/tmp/claude-0/-home-user-e3website/10fabba6-8466-5a4a-8a5e-76bc7c581094/scratchpad/credits.json"))
LIC = {"CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/", "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/", "CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/"}
ALT = {"ny-day": "Brooklyn Bridge and Lower Manhattan, in daylight", "ny-night": "Times Square, Manhattan, at night", "chi-day": "The Chicago skyline from Burnham Harbor, in daylight", "chi-night": "The Chicago River at night",
       "sf-day": "Downtown San Francisco and the Transamerica Pyramid, in daylight", "sf-night": "The San Francisco skyline across the bay at night", "la-day": "Downtown Los Angeles towers, in daylight", "la-night": "Downtown Los Angeles towers at night"}
WHO = {k: ("Marie Miller" if k == "chi-day" else v["artist"]) for k, v in PHOTO.items()}

def vars_css(t):
    L, D = t["light"], t["dark"]
    f = lambda d: ";".join(f"--{k}:{v}" for k, v in d.items())
    return f":root{{{f(L)}}}html.night{{{f(D)}}}"

CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font:400 1.125rem/1.6 var(--sans);font-variant-numeric:lining-nums;-webkit-font-smoothing:antialiased}
a{color:inherit}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:4px}
.skip{position:absolute;left:-999px;top:8px;background:var(--ink);color:var(--bg);padding:10px 14px;border-radius:8px;z-index:10}.skip:focus{left:12px}
.wrap{max-width:1200px;margin:0 auto;padding:0 28px}
header{position:sticky;top:0;z-index:20;background:var(--bg)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px 0}
.brand{display:flex;align-items:center;gap:10px;font:var(--brandw) 1.3rem var(--serif);text-decoration:none;letter-spacing:-.005em}
.brand i{width:26px;height:26px;border-radius:8px;background:var(--accent);display:block;position:relative}
.brand i::after{content:"";position:absolute;right:4px;top:4px;width:9px;height:9px;border-radius:50%;background:var(--accent2)}
.right{display:flex;align-items:center;gap:6px}
nav ul{display:flex;list-style:none;gap:2px}
nav a{display:block;padding:10px 14px;border-radius:99px;font:600 1rem var(--sans);text-decoration:none;color:var(--muted);min-height:44px;display:flex;align-items:center}
nav a:hover{color:var(--ink);background:var(--wash)}nav a[aria-current=page]{color:var(--ink);background:var(--wash)}
.icon-btn{width:44px;height:44px;border-radius:50%;background:var(--wash);display:grid;place-items:center;border:0;color:var(--ink);cursor:pointer}
.icon-btn svg{grid-area:1/1}.menu{display:none}.sun{display:none}html.night .sun{display:block}html.night .moon{display:none}
.hero{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;padding:36px 0 28px}
.eyebrow{display:inline-block;font:700 .8125rem var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:16px}
h1{font:var(--h1w) clamp(2.5rem,4.8vw,4.2rem)/1.06 var(--serif);letter-spacing:-.015em;text-wrap:balance}
.lede{margin:22px 0 30px;font-size:1.3rem;line-height:1.5;max-width:36ch;color:var(--muted)}
.btns{display:flex;flex-wrap:wrap;gap:12px}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.hero>*{min-width:0}.search{display:flex;gap:8px;max-width:520px;width:100%;background:var(--surface);border-radius:99px;padding:6px;box-shadow:0 10px 30px -18px rgba(60,30,10,.45)}
.search input{flex:1;min-width:0;border:0;background:none;color:var(--ink);font:400 1.0625rem var(--sans);padding:0 18px;min-height:48px;border-radius:99px}.search input::placeholder{color:var(--muted)}
.search input:focus-visible{outline:none}.search:focus-within{box-shadow:0 0 0 3px var(--accent)}
.chips{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:center;margin-top:16px;font-size:1rem;color:var(--muted)}
.chips a{padding:6px 14px;border-radius:99px;background:var(--wash);text-decoration:none;color:var(--ink);font-weight:600;min-height:36px;display:inline-flex;align-items:center}.chips a:hover{background:var(--accent);color:var(--onaccent)}
.more{display:flex;gap:22px;margin-top:18px}.more a{font-weight:700;color:var(--accent);text-underline-offset:4px;padding:8px 0}
.btn{display:inline-flex;align-items:center;min-height:52px;padding:0 28px;border-radius:99px;font:700 1.0625rem var(--sans);text-decoration:none;background:var(--accent);color:var(--onaccent);transition:transform .15s,filter .15s}
.btn:hover{filter:brightness(1.08);transform:translateY(-1px)}.btn.alt{background:transparent;color:var(--ink);box-shadow:inset 0 0 0 2px var(--ink)}
figure{margin:0}.photo{position:relative;border-radius:28px;overflow:hidden;aspect-ratio:6/5;background:var(--wash)}
.photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.photo::after{content:"";position:absolute;inset:0;background:linear-gradient(135deg,var(--tint1),transparent 55%);mix-blend-mode:multiply;opacity:.9;pointer-events:none}
html.night .photo::after{mix-blend-mode:soft-light}
figcaption{margin-top:12px;font:400 .9375rem/1.5 var(--sans);color:var(--muted)}figcaption a{color:var(--ink)}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:26px 0 0}
.stat{background:var(--surface);border-radius:22px;padding:22px 26px}
.stat b{display:block;font:var(--h1w) 3rem/1 var(--serif);color:var(--ink);letter-spacing:-.02em;font-variant-numeric:lining-nums tabular-nums}.stat span{display:block;margin-top:6px;color:var(--muted);font-size:1.0625rem}
section{padding:60px 0 0}
.sub{margin-top:4px;color:var(--muted)}
.sh{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:22px}
h2{font:var(--h1w) clamp(1.8rem,3.2vw,2.5rem)/1.12 var(--serif);letter-spacing:-.01em}
.link{font:700 1rem var(--sans);color:var(--accent);text-underline-offset:4px}
.closing{list-style:none;background:var(--surface);border-radius:26px;padding:8px 10px}
.closing li a{display:grid;grid-template-columns:76px 1fr auto auto;gap:6px 22px;align-items:center;padding:16px 18px;border-radius:18px;text-decoration:none}
.closing li a:hover{background:var(--wash)}
.dt{text-align:center;font:var(--h1w) 1.9rem/1 var(--serif);color:var(--ink)}.dt small{display:block;font:700 .75rem var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-top:3px}
.gn{font:600 1.1875rem/1.3 var(--sans)}.gf{display:block;color:var(--muted);font-size:1rem;font-weight:400}
.amt{font:700 1.125rem var(--sans);font-variant-numeric:tabular-nums;text-align:right}
.chip{display:inline-block;padding:5px 14px;border-radius:99px;font:700 .875rem var(--sans);background:var(--wash);color:var(--ink);white-space:nowrap}.chip.soon{background:var(--accent);color:var(--onaccent)}
.cards3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.fcard{display:flex!important;flex-direction:column}.fbody{flex:1;display:flex;flex-direction:column}.by{margin-top:auto;padding-top:14px;font-size:.9375rem;color:var(--muted)}
.fcard{display:block;text-decoration:none;background:var(--surface);border-radius:28px;overflow:hidden}
.fcard img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover}
.fbody{padding:24px 28px 30px}.tag{font:700 .8125rem var(--sans);letter-spacing:.09em;text-transform:uppercase;color:var(--accent)}
.fcard h3{font:var(--h1w) 1.45rem/1.22 var(--serif);margin:8px 0 10px;letter-spacing:-.008em}.fcard:hover h3{text-decoration:underline;text-underline-offset:4px}
.fcard p{color:var(--muted)}
.stack{display:grid;gap:22px}.stack .fcard{display:grid;grid-template-columns:140px 1fr}.stack .fcard img{height:100%;aspect-ratio:auto}.stack .fbody{padding:18px 20px}.stack h3{font-size:1.2rem;margin:6px 0 0}
.band{margin-top:60px;background:var(--accent);color:var(--onaccent);border-radius:32px;padding:48px 52px;display:flex;flex-wrap:wrap;gap:24px 40px;align-items:center;justify-content:space-between}
.band h2{max-width:20ch}.band p{margin-top:8px;max-width:46ch;opacity:.92}
.band .btn{background:var(--onaccent);color:var(--accent)}.band .btn.alt{background:transparent;color:var(--onaccent);box-shadow:inset 0 0 0 2px var(--onaccent)}
footer{padding:64px 0 44px;margin-top:20px}footer ul{display:flex;flex-wrap:wrap;gap:6px 24px;list-style:none;margin-bottom:18px}
footer a{display:inline-block;padding:8px 0;color:var(--muted);text-decoration:none;font-weight:600}footer a:hover{color:var(--ink);text-decoration:underline}footer p{font-size:.9375rem;color:var(--muted)}
@media(max-width:900px){.hero,.cards3{grid-template-columns:1fr;gap:28px}.stats{grid-template-columns:1fr}.photo{aspect-ratio:4/3}.menu{display:grid}
 nav{display:none;position:absolute;left:0;right:0;top:100%;background:var(--bg);padding:6px 28px 16px}nav.open{display:block}nav ul{flex-direction:column}
 .closing li a{grid-template-columns:60px 1fr auto}.closing .amt{display:none}.band{padding:34px 28px}.stack .fcard{grid-template-columns:110px 1fr}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""
SUN = '<svg class="sun" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
MOON = '<svg class="moon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/></svg>'
NAV = [("index.html", "Home"), ("about.html", "About"), ("articles.html", "Articles"), ("research.html", "Research"), ("journals.html", "Journals"), ("grants.html", "Grant Finder"), ("contact.html", "Contact")]
FOOT = [("articles.html", "Articles"), ("research.html", "Research"), ("journals.html", "Journals"), ("economic-indicators.html", "Economic Indicators"), ("grants.html", "Grant Finder"), ("grant-help.html", "Grant Help"), ("outreach.html", "Outreach"), ("privacy.html", "Privacy"), ("d-preview/credits.html", "Photo credits")]

from common import PUBS
def _cards3():
    imgs={"article-railroad":("card-rail.webp","Chinese railroad workers among rocks near the opening of Summit Tunnel, 1865 to 1867","/articles/chinese-labor-transcontinental-railroad.html"),
          "research-chinatown":("card-research.webp","Chinatown street with colorful lanterns and signs","/research/chinatown-solidarity-paper.html"),
          "article-chinatown":("card-article.webp","Chinatown temple decorated with lanterns at night","/articles/chinatown-solidarity.html")}
    out=""
    for p in PUBS:
        im,alt,href=imgs[p["slug"]]
        out+=f'<a class="fcard" href="{href}"><img src="/d-preview/img/{im}" width="720" height="480" alt="{alt}" loading="lazy" decoding="async"><div class="fbody"><span class="tag">{p["kind"]}</span><h3>{p["title"].split(": ")[0]}</h3><p>{p["summary"]}</p><span class="by">{p["author"]} · {p["min"]} min read · {p["short"][:6]}, {p["short"][-4:]}</span></div></a>'
    return out

def build(t, out, fontlinks="", fontface="", base=""):
    nav = "".join(f'<li><a href="/{h}"{" aria-current=page" if h == "index.html" else ""}>{n}</a></li>' for h, n in NAV)
    foot = "".join(f'<li><a href="/{h}">{n}</a></li>' for h, n in FOOT)
    P = json.dumps({k: {"a": ALT[k], "w": WHO[k], "l": PHOTO[k]["license"], "u": LIC.get(PHOTO[k]["license"], PHOTO[k]["url"]), "p": PHOTO[k]["url"]} for k in PHOTO}, ensure_ascii=False)
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>e3 Initiative | Research on Equity, Economics, and Ethnicity (design preview)</title>
<meta name="description" content="The e3 Initiative conducts research at the intersection of equity, economics, and ethnicity to inform policy and empower local change."><meta name="robots" content="noindex">
<script>(function(){{try{{var s=localStorage.getItem('e3-night');if(s==='1'||(s===null&&matchMedia('(prefers-color-scheme:dark)').matches))document.documentElement.classList.add('night')}}catch(e){{}}}})()</script>
{fontlinks}<style>{fontface}{vars_css(t)}:root{{--serif:{t['serif']};--sans:{t['sans']};--h1w:{t['h1w']};--brandw:{t['brandw']}}}{CSS}</style></head>
<body><a class="skip" href="#main">Skip to main content</a>
<header><div class="wrap nav"><a class="brand" href="/index.html"><i aria-hidden="true"></i>e3 Initiative</a>
<div class="right"><nav id="nav" aria-label="Main"><ul>{nav}</ul></nav>
<button class="icon-btn" id="mode" aria-pressed="false" aria-label="Dark mode">{MOON}{SUN}</button>
<button class="icon-btn menu" id="menu" aria-expanded="false" aria-controls="nav" aria-label="Menu"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button></div></div></header>
<main id="main" class="wrap">
<div class="hero"><div>
<span class="eyebrow">Equity · Economics · Ethnicity</span>
<h1>Research for equitable communities.</h1>
<p class="lede">We study the intersection of equity, economics, and ethnicity to inform policy and empower local change.</p>
<form class="search" action="/grants.html" role="search"><label for="q" class="vh">Search grants</label><input id="q" name="q" type="search" placeholder="Search grants: arts, women-owned" autocomplete="off"><button class="btn" type="submit">Search</button></form>
<p class="chips"><span>Try:</span><a href="/grants.html?q=women-owned">Women-owned</a><a href="/grants.html?q=veteran">Veteran-owned</a><a href="/grants.html?q=arts">Arts</a><a href="/grants.html?q=nonprofit">Nonprofit</a></p>
<p class="more"><a href="/grants.html">Browse all grants</a><a href="/research.html">Explore our research</a></p></div>
<figure><div class="photo"><img id="hero" width="1200" height="1000" alt="" fetchpriority="high" decoding="async"></div><figcaption id="cap"></figcaption></figure></div>
<div class="stats" id="stats"><div class="stat"><b id="s1">87</b><span>grants open or rolling you can apply for now</span></div><div class="stat"><b id="s2">4</b><span>deadlines closing in the next 30 days</span></div><div class="stat"><b id="s3">3</b><span>articles and papers on Chinatown economies</span></div></div>
<section aria-labelledby="c-h"><div class="sh"><div><h2 id="c-h">Closing soon</h2><p class="sub" id="ctotal">The next grant deadlines, soonest first.</p></div><a class="link" href="/grants.html">All grants</a></div><ul class="closing" id="closing"><li><a href="/grants.html"><span class="dt">Open</span><span class="gn">Browse every open grant in the Grant Finder</span></a></li></ul></section>
<section aria-labelledby="r-h"><div class="sh"><h2 id="r-h">Latest research</h2><a class="link" href="/articles.html">View all</a></div>
<div class="cards3">{_cards3()}</div></section>
<div class="band"><div><h2>Have a story, or want to work with us?</h2><p>Our research depends on the people it describes. Share your experience, or partner with the team.</p></div><div class="btns"><a class="btn" href="/outreach.html">Share your story</a><a class="btn alt" href="/contact.html">Contact us</a></div></div>
</main>
<footer><div class="wrap"><ul>{foot}</ul><p>© 2026 e3 Initiative</p></div></footer>
<script>
(function(){{var r=document.documentElement,m=document.getElementById('mode'),mn=document.getElementById('menu'),n=document.getElementById('nav');
m.setAttribute('aria-pressed',r.classList.contains('night'));
m.addEventListener('click',function(){{var on=r.classList.toggle('night');try{{localStorage.setItem('e3-night',on?'1':'0')}}catch(e){{}}m.setAttribute('aria-pressed',on);show()}});
mn.addEventListener('click',function(){{var o=n.classList.toggle('open');mn.setAttribute('aria-expanded',o)}});
var P={P},C=['ny','chi','sf','la'],NM={json.dumps(CITY_NAMES)},B='{base}/d-preview/img/',city=null;
try{{city=sessionStorage.getItem('e3-city')}}catch(e){{}}if(!city||C.indexOf(city)<0){{city=C[Math.floor(Math.random()*4)];try{{sessionStorage.setItem('e3-city',city)}}catch(e){{}}}}
var img=document.getElementById('hero'),cap=document.getElementById('cap');
function show(){{var k=city+'-'+(r.classList.contains('night')?'night':'day'),p=P[k],b=B+k;img.alt=p.a;img.srcset=b+'-640.webp 640w, '+b+'-1200.webp 1200w';img.sizes='(max-width:900px) 100vw, 50vw';img.src=b+'-1200.webp';
 cap.innerHTML=NM[city]+'. Photo: '+p.w.replace(/</g,'&lt;')+', <a href="'+p.u+'">'+p.l+'</a> (<a href="'+p.p+'">source</a>). Resized and compressed. <a href="/d-preview/credits.html">All credits</a>.'}}
show();
fetch('{base}/data/grants.json').then(function(x){{return x.json()}}).then(function(g){{
 var today=new Date();today.setHours(0,0,0,0);
 var open=g.filter(function(x){{return x.status!=='closed'&&(x.deadline==='rolling'||x.deadline==='annual'||new Date(x.deadline+'T23:59:59')>=today)}});
 document.getElementById('s1').textContent=open.length;
 var up=g.filter(function(x){{return /^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(x.deadline)&&x.status!=='closed'&&new Date(x.deadline+'T23:59:59')>=today}}).sort(function(a,b){{return a.deadline<b.deadline?-1:1}}).slice(0,4);
 if(!up.length)return;var ul=document.getElementById('closing');ul.textContent='';var tot=up.reduce(function(a,x){{return a+(x.amountMax||0)}},0);if(tot)document.getElementById('ctotal').textContent='Up to $'+tot.toLocaleString('en-US')+' across the next '+up.length+' deadlines.';var in30=g.filter(function(x){{return /^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(x.deadline)&&x.status!=='closed'&&(new Date(x.deadline+'T00:00:00')-today)/864e5<=30&&new Date(x.deadline+'T23:59:59')>=today}}).length;document.getElementById('s2').textContent=in30;
 up.forEach(function(x){{var d=new Date(x.deadline+'T12:00:00'),days=Math.round((new Date(x.deadline+'T00:00:00')-today)/864e5);
  var li=document.createElement('li'),a=document.createElement('a');a.href='/grants.html';
  var dt=document.createElement('span');dt.className='dt';dt.textContent=d.getDate();var sm=document.createElement('small');sm.textContent=d.toLocaleDateString('en-US',{{month:'short'}});dt.appendChild(sm);
  var gn=document.createElement('span');gn.className='gn';gn.textContent=x.name;var gf=document.createElement('span');gf.className='gf';gf.textContent=x.funder;gn.appendChild(gf);
  var am=document.createElement('span');am.className='amt';am.textContent=x.amountMax?'Up to $'+x.amountMax.toLocaleString('en-US'):'';
  var ch=document.createElement('span');ch.className='chip'+(days<=7?' soon':'');ch.textContent=days===0?'Closes today':days===1?'1 day left':days+' days left';
  a.appendChild(dt);a.appendChild(gn);a.appendChild(am);a.appendChild(ch);li.appendChild(a);ul.appendChild(li)}})
}}).catch(function(){{}});
}})();
</script></body></html>"""
    open(out, "w").write(html)
