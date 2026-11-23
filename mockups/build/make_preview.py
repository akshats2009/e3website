"""Builds the D homepage preview into /d-preview (ruled on by the Cage Match council).
Rulings: solid nav; one photo per mode with click-only city tabs (others load on click); next-closing-grant card below the hero;
two font families (Archivo + IBM Plex Mono, self-hosted); no wordmark, grain, parallax or glow; credits page; noindex."""
import json, os, re
from PIL import Image

ROOT = "/home/user/e3website"
SRC = f"{ROOT}/mockups/shared/img/cities"
OUT = f"{ROOT}/d-preview"
os.makedirs(f"{OUT}/img", exist_ok=True)
CRED = json.load(open("/tmp/claude-0/-home-user-e3website/10fabba6-8466-5a4a-8a5e-76bc7c581094/scratchpad/credits.json"))

CITIES = [("ny", "New York", "Brooklyn Bridge and Lower Manhattan", "Times Square, Manhattan"),
          ("chi", "Chicago", "The Chicago skyline from Burnham Harbor", "The Chicago River at night"),
          ("sf", "San Francisco", "Downtown San Francisco and the Transamerica Pyramid", "The San Francisco skyline across the bay"),
          ("la", "Los Angeles", "Downtown Los Angeles towers", "Downtown Los Angeles towers at night")]
LIC = {"CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/", "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/",
       "CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/", "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/"}
ARTIST_FIX = {"chi-day": "Marie Miller"}

# images: 1200 and 640 wide WebP
sizes = {}
for k in CRED:
    im = Image.open(f"{SRC}/{k}.jpg").convert("RGB")
    for w, q in ((1200, 68), (640, 66)):
        t = im.copy(); t.thumbnail((w, w * 2))
        p = f"{OUT}/img/{k}-{w}.webp"; t.save(p, "WEBP", quality=q, method=6); sizes[(k, w)] = os.path.getsize(p)

def clean_title(k):
    return re.sub(r"\.jpe?g$", "", CRED[k]["title"].replace("File:", "")).replace("-", " ") if k == "chi-day" else re.sub(r"\.jpe?g$", "", CRED[k]["title"].replace("File:", ""))

PHOTOS = {}
for k in CRED:
    city = k.split("-")[0]; mode = k.split("-")[1]
    row = next(c for c in CITIES if c[0] == city)
    PHOTOS[k] = {"alt": (row[2] if mode == "day" else row[3]) + (", in daylight" if mode == "day" else ""),
                 "cap": row[2] if mode == "day" else row[3],
                 "who": ARTIST_FIX.get(k, CRED[k]["artist"]), "lic": CRED[k]["license"], "page": CRED[k]["url"]}

NAV = [("index.html", "Home"), ("about.html", "About"), ("articles.html", "Articles"), ("research.html", "Research"), ("journals.html", "Journals"), ("grants.html", "Grant Finder"), ("contact.html", "Contact")]
FOOT = [("articles.html", "Articles"), ("research.html", "Research"), ("journals.html", "Journals"), ("economic-indicators.html", "Economic Indicators"), ("grants.html", "Grant Finder"), ("grant-help.html", "Grant Help"), ("outreach.html", "Outreach"), ("privacy.html", "Privacy"), ("d-preview/credits.html", "Photo credits")]

CSS = """
@font-face{font-family:Archivo;src:url(fonts/archivo.woff2) format('woff2');font-weight:100 900;font-stretch:62% 125%;font-display:swap}
@font-face{font-family:'IBM Plex Mono';src:url(fonts/plexmono.woff2) format('woff2');font-weight:500;font-display:swap}
:root{--bg:#eef0f2;--surface:#fff;--ink:#101318;--muted:#4a5360;--accent:#00704b;--wash:rgba(16,19,24,.07);--on-accent:#fff;--shadow:0 30px 60px -40px rgba(20,30,40,.35);
 --sans:Archivo,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace}
html.night{--bg:#090c11;--surface:#121820;--ink:#f1f3f5;--muted:#a9b2be;--accent:#37d9a0;--wash:rgba(255,255,255,.08);--on-accent:#06130d;--shadow:0 30px 70px -40px rgba(0,0,0,.9)}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--ink);font:400 1rem/1.55 var(--sans);-webkit-font-smoothing:antialiased}
a{color:inherit}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:4px}
.skip{position:absolute;left:-999px;top:8px;background:var(--ink);color:var(--bg);padding:10px 14px;border-radius:8px;z-index:10}.skip:focus{left:12px}
.wrap{max-width:1200px;margin:0 auto;padding:0 28px}
header{position:sticky;top:0;z-index:20;background:var(--bg)}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 0}
.brand{display:flex;align-items:center;gap:10px;font-weight:700;font-stretch:80%;letter-spacing:.02em;text-transform:uppercase;text-decoration:none}
.brand i{width:24px;height:24px;border-radius:7px;background:var(--accent);display:block}
.right{display:flex;align-items:center;gap:10px}
nav ul{display:flex;list-style:none;position:relative;gap:0}
nav ul::before{content:"";position:absolute;left:28px;right:28px;top:10px;height:3px;border-radius:2px;background:var(--accent)}
nav a{position:relative;display:block;padding:26px 11px 6px;font:600 .8rem var(--sans);font-stretch:85%;letter-spacing:.07em;text-transform:uppercase;text-decoration:none;color:var(--muted);min-height:44px}
nav a::before{content:"";position:absolute;left:50%;top:3px;width:16px;height:16px;margin-left:-8px;border-radius:50%;background:var(--bg);box-shadow:0 0 0 3px var(--accent)}
nav a:hover{color:var(--ink)}nav a[aria-current=page]{color:var(--ink)}nav a[aria-current=page]::before{background:var(--ink)}
.icon-btn{width:44px;height:44px;border-radius:50%;background:var(--wash);display:grid;place-items:center;border:0;color:var(--ink);cursor:pointer}
.icon-btn svg{grid-area:1/1}.menu{display:none}
.sun{display:none}html.night .sun{display:block}html.night .moon{display:none}
.hero{display:grid;grid-template-columns:5fr 7fr;gap:48px;align-items:center;padding:28px 0 20px}
.eyebrow{font:500 .75rem var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:18px}
h1{font-weight:760;font-stretch:72%;text-transform:uppercase;letter-spacing:-.015em;line-height:.95;font-size:clamp(2.9rem,6vw,5.4rem);text-wrap:balance}
h1 span{color:var(--accent)}
.lede{margin:22px 0 28px;font-size:1.125rem;max-width:36ch;color:var(--muted)}
.btns{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-flex;align-items:center;min-height:48px;padding:0 24px;border-radius:99px;font:700 .85rem var(--sans);font-stretch:90%;letter-spacing:.08em;text-transform:uppercase;text-decoration:none;background:var(--ink);color:var(--bg)}
.btn.alt{background:var(--wash);color:var(--ink)}.btn:hover{opacity:.88}
figure{margin:0}
.photo{position:relative;border-radius:26px;overflow:hidden;aspect-ratio:6/5;background:var(--wash);box-shadow:var(--shadow)}
.photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.tabs{position:absolute;left:16px;top:16px;display:flex;flex-wrap:wrap;gap:4px;padding:4px;border-radius:99px;background:rgba(10,14,20,.82)}
.tabs button{min-height:36px;padding:0 14px;border-radius:99px;border:0;background:none;color:#fff;font:700 .72rem var(--sans);letter-spacing:.07em;text-transform:uppercase;cursor:pointer}
.tabs button[aria-pressed=true]{background:#fff;color:#101318}
figcaption{margin-top:12px;font:500 .72rem/1.5 var(--mono);color:var(--muted)}
figcaption a{color:var(--ink)}
.closes{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:18px 32px;margin:26px 0 0;padding:26px 30px;border-radius:24px;background:var(--surface);box-shadow:var(--shadow)}
.closes h2{font:500 .75rem var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.closes .name{font-weight:700;font-size:1.4rem;line-height:1.2}.closes .name a{text-decoration:none}.closes .name a:hover{text-decoration:underline}
.closes .meta{color:var(--muted);margin-top:4px}
.closes .when{font:500 .95rem var(--mono);text-align:right}.closes .when b{display:block;font:760 2.2rem/1 var(--sans);font-stretch:75%;letter-spacing:-.01em;color:var(--accent);margin-bottom:4px}
section.latest{padding:56px 0 8px}
section.latest h2{font-weight:760;font-stretch:72%;text-transform:uppercase;font-size:clamp(1.8rem,3.4vw,2.6rem);letter-spacing:-.01em;margin-bottom:22px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;list-style:none}
.card a{display:block;text-decoration:none}.card img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:18px;background:var(--wash)}
.card h3{font-weight:700;font-size:1.1rem;line-height:1.25;margin:14px 0 6px}.card a:hover h3{text-decoration:underline}
.card span{font:500 .8rem var(--mono);color:var(--muted)}
footer{padding:56px 0 40px;margin-top:40px}
footer ul{display:flex;flex-wrap:wrap;gap:6px 24px;list-style:none;margin-bottom:18px}
footer a{display:inline-block;padding:8px 0;color:var(--muted);text-decoration:none;font-weight:500}footer a:hover{color:var(--ink);text-decoration:underline}
footer p{font:500 .75rem var(--mono);color:var(--muted)}
.prose{max-width:760px;padding:40px 0}.prose h1{font-size:clamp(2.4rem,5vw,3.6rem);margin-bottom:18px}.prose p{margin:0 0 14px;color:var(--muted)}
table{width:100%;border-collapse:collapse;margin:22px 0;font-size:.95rem}th,td{text-align:left;padding:12px 14px 12px 0;vertical-align:top}th{font:500 .72rem var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
tbody tr:nth-child(odd){background:var(--wash)}td,th{padding-left:12px}
@media(max-width:900px){.hero{grid-template-columns:1fr;gap:28px}.lede{max-width:none}.cards{grid-template-columns:1fr}.photo{aspect-ratio:4/3}
 .menu{display:grid}nav{display:none;position:absolute;left:0;right:0;top:100%;background:var(--bg);padding:6px 28px 16px}nav.open{display:block}nav ul{flex-direction:column}nav ul::before,nav a::before{display:none}nav a{padding:12px 0;min-height:44px}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

HEAD_JS = "<script>(function(){try{var s=localStorage.getItem('e3-night');if(s==='1'||(s===null&&matchMedia('(prefers-color-scheme:dark)').matches))document.documentElement.classList.add('night')}catch(e){}})()</script>"
SUN = '<svg class="sun" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
MOON = '<svg class="moon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/></svg>'

def shell(title, desc, body, current, scripts="", path="d-preview/"):
    nav = "".join(f'<li><a href="/{h}"{" aria-current=page" if h == current else ""}>{t}</a></li>' for h, t in NAV)
    foot = "".join(f'<li><a href="/{h}">{t}</a></li>' for h, t in FOOT)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="noindex">
{HEAD_JS}
<link rel="preload" href="/d-preview/fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS.replace('url(fonts/', 'url(/d-preview/fonts/')}</style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header><div class="wrap nav">
  <a class="brand" href="/index.html"><i aria-hidden="true"></i>e3 Initiative</a>
  <div class="right">
    <nav id="nav" aria-label="Main"><ul>{nav}</ul></nav>
    <button class="icon-btn" id="mode" aria-pressed="false" aria-label="Dark mode">{MOON}{SUN}</button>
    <button class="icon-btn menu" id="menu" aria-expanded="false" aria-controls="nav" aria-label="Menu"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
</div></header>
<main id="main" class="wrap">
{body}
</main>
<footer><div class="wrap"><ul>{foot}</ul><p>© 2026 e3 Initiative. This is a design preview and is not indexed.</p></div></footer>
<script>
(function(){{var r=document.documentElement,m=document.getElementById('mode'),mn=document.getElementById('menu'),n=document.getElementById('nav');
m.setAttribute('aria-pressed',r.classList.contains('night'));
m.addEventListener('click',function(){{var on=r.classList.toggle('night');try{{localStorage.setItem('e3-night',on?'1':'0')}}catch(e){{}}m.setAttribute('aria-pressed',on);if(window.e3Photo)window.e3Photo()}});
mn.addEventListener('click',function(){{var o=n.classList.toggle('open');mn.setAttribute('aria-expanded',o)}});}})();
</script>
{scripts}
</body></html>
"""

# home
PH = json.dumps({k: {"a": v["alt"], "c": v["cap"], "w": v["who"], "l": v["lic"], "u": LIC.get(v["lic"], v["page"]), "p": v["page"], "s1": sizes[(k, 1200)], "s2": sizes[(k, 640)]} for k, v in PHOTOS.items()}, ensure_ascii=False)
tabs = "".join(f'<button type="button" data-c="{c}" aria-pressed="{"true" if i == 0 else "false"}">{n}</button>' for i, (c, n, _, _) in enumerate(CITIES))
cards = [("articles/chinese-labor-transcontinental-railroad.html", "Chinese Labor and the Transcontinental Railroad: The Uncredited Contributions and Lost Legacy", "image/chinese-workers-summit-tunnel.jpg", "Chinese railroad workers among rocks near the opening of Summit Tunnel, 1865 to 1867", "Article"),
         ("research/chinatown-solidarity-paper.html", "Beyond Restaurants and Boba Cafes: The Historical and Modern Economic Solidarity of Chinatown", "image/chinatown-street-640.jpg", "Chinatown street with colorful lanterns and signs", "Research paper"),
         ("articles/chinatown-solidarity.html", "Beyond Restaurants, Boba Cafes, and Souvenir Shops: The Historical and Modern Economic Solidarity of Chinatown", "image/chinatown-banner-640.jpg", "Chinatown temple decorated with lanterns at night", "Article")]
for _src, _n in (("chinese-workers-summit-tunnel", "card-rail"), ("chinatown-street-640", "card-research"), ("chinatown-banner-640", "card-article")):
    _im = Image.open(f"{ROOT}/image/{_src}.jpg").convert("RGB"); _w, _h = _im.size; _t = min(_w, int(_h * 4 / 3)); _hh = int(_t * 3 / 4)
    _im = _im.crop(((_w - _t) // 2, (_h - _hh) // 2, (_w - _t) // 2 + _t, (_h - _hh) // 2 + _hh)); _im.thumbnail((480, 360)); _im.save(f"{OUT}/img/{_n}.webp", "WEBP", quality=70, method=6)
CARDIMG = ["img/card-rail.webp", "img/card-research.webp", "img/card-article.webp"]
cards = [(h, t, CARDIMG[i], a, k) for i, (h, t, _i, a, k) in enumerate(cards)]
cardhtml = "".join(f'<li class="card"><a href="/{h}"><img src="/d-preview/{i}" alt="{a}" width="480" height="360" loading="lazy" decoding="async"><h3>{t}</h3><span>{k}</span></a></li>' for h, t, i, a, k in cards)
body = f"""
<div class="hero">
  <div>
    <p class="eyebrow">Equity · Economics · Ethnicity</p>
    <h1>Research for equitable communities<span>.</span></h1>
    <p class="lede">We study the intersection of equity, economics, and ethnicity to inform policy and empower local change.</p>
    <div class="btns"><a class="btn" href="/research.html">Explore research</a><a class="btn alt" href="/grants.html">Find a grant</a></div>
  </div>
  <figure>
    <div class="photo" id="photo">
      <img id="hero" width="1200" height="1000" alt="" fetchpriority="high" decoding="async">
      <script>(function(){{var n=document.documentElement.classList.contains('night'),i=document.getElementById('hero');i.src='/d-preview/img/ny-'+(n?'night':'day')+'-1200.webp';i.srcset='/d-preview/img/ny-'+(n?'night':'day')+'-640.webp 640w, /d-preview/img/ny-'+(n?'night':'day')+'-1200.webp 1200w';i.sizes='(max-width:900px) 100vw, 58vw'}})()</script>
      <noscript><img src="/d-preview/img/ny-day-1200.webp" width="1200" height="1000" alt="Brooklyn Bridge and Lower Manhattan, in daylight"></noscript>
      <div class="tabs" role="group" aria-label="Choose a city photo">{tabs}</div>
    </div>
    <figcaption id="cap"></figcaption>
  </figure>
</div>
<section class="closes" aria-labelledby="closes-h" id="closes">
  <div><h2 id="closes-h">Next grant to close</h2><p class="name"><a href="/grants.html">Browse open grants in the Grant Finder</a></p><p class="meta">Deadlines, amounts and eligibility for small businesses and nonprofits.</p></div>
  <a class="btn alt" href="/grants.html">Open Grant Finder</a>
</section>
<section class="latest" aria-labelledby="latest-h"><h2 id="latest-h">Latest research</h2><ul class="cards">{cardhtml}</ul><p style="margin-top:20px"><a class="btn alt" href="/articles.html">View all articles</a></p></section>
"""
SCRIPT = f"""<script>
(function(){{
var P={PH},C={json.dumps([c for c,_,_,_ in CITIES])},NM={json.dumps({c: n for c, n, _, _ in CITIES})};
var city='ny',img=document.getElementById('hero'),cap=document.getElementById('cap'),tabs=document.querySelectorAll('.tabs button');
function mode(){{return document.documentElement.classList.contains('night')?'night':'day'}}
function show(){{var k=city+'-'+mode(),p=P[k],b='/d-preview/img/'+k;
  img.alt=p.a;img.srcset=b+'-640.webp 640w, '+b+'-1200.webp 1200w';img.src=b+'-1200.webp';
  cap.innerHTML=NM[city]+': '+p.c.replace(/&/g,'&amp;')+'. Photo: '+p.w.replace(/</g,'&lt;')+', <a href="'+p.u+'">'+p.l+'</a> (<a href="'+p.p+'">source</a>). Resized and compressed. <a href="/d-preview/credits.html">All credits</a>.';
  tabs.forEach(function(t){{t.setAttribute('aria-pressed',t.dataset.c===city)}})}}
tabs.forEach(function(t){{t.addEventListener('click',function(){{city=t.dataset.c;show()}})}});
window.e3Photo=show;show();
fetch('/data/grants.json').then(function(r){{return r.json()}}).then(function(g){{
  var today=new Date();today.setHours(0,0,0,0);
  var up=g.filter(function(x){{return /^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(x.deadline)&&x.status!=='closed'&&new Date(x.deadline+'T23:59:59')>=today}}).sort(function(a,b){{return a.deadline<b.deadline?-1:1}});
  if(!up.length)return;var x=up[0],d=new Date(x.deadline+'T12:00:00'),days=Math.round((new Date(x.deadline+'T00:00:00')-today)/864e5);
  var el=document.getElementById('closes'),f=d.toLocaleDateString('en-US',{{month:'long',day:'numeric',year:'numeric'}});
  var nm=document.createElement('a');nm.href='/grants.html';nm.textContent=x.name;
  var h=el.querySelector('.name');h.textContent='';h.appendChild(nm);
  el.querySelector('.meta').textContent=x.funder+(x.amount?' · '+x.amount:'');
  var w=document.createElement('p');w.className='when';var b=document.createElement('b');b.textContent=days===0?'Today':days===1?'1 day':days+' days';
  w.appendChild(b);w.appendChild(document.createTextNode('Closes '+f));el.insertBefore(w,el.querySelector('a.btn'));
}}).catch(function(){{}});
}})();
</script>"""
open(f"{OUT}/index.html", "w").write(shell("e3 Initiative | Research on Equity, Economics, and Ethnicity (design preview)", "The e3 Initiative conducts research at the intersection of equity, economics, and ethnicity to inform policy and empower local change.", body, "index.html", SCRIPT))

# credits
rows = ""
for k, v in PHOTOS.items():
    city = next(c[1] for c in CITIES if c[0] == k.split("-")[0])
    rows += f'<tr><td>{city}, {k.split("-")[1]}</td><td><a href="{v["page"]}">{clean_title(k)}</a></td><td>{v["who"]}</td><td><a href="{LIC.get(v["lic"], v["page"])}">{v["lic"]}</a></td></tr>'
cred = f"""<div class="prose"><h1>Photo credits</h1>
<p>The city photographs on the homepage come from Wikimedia Commons and are used under the licenses below. We resized and compressed each photo for the web and cropped it to fit the layout; we made no other changes. Photos licensed CC BY-SA remain under CC BY-SA, and so does any adaptation of them.</p>
<table><thead><tr><th scope="col">Photo</th><th scope="col">Title (source)</th><th scope="col">Creator</th><th scope="col">License</th></tr></thead><tbody>{rows}</tbody></table>
<p>The article thumbnails come from the e3 Initiative archive. Their credits are on the pages that use them.</p></div>"""
open(f"{OUT}/credits.html", "w").write(shell("Photo credits | e3 Initiative (design preview)", "Credits and licenses for the photographs used on the e3 Initiative homepage preview.", cred, "d-preview/credits.html"))
tot = sum(v for (k, w), v in sizes.items() if w == 1200)
print("images: 1200px total", tot // 1024, "KB; per-image max", max(v for (k, w), v in sizes.items() if w == 1200) // 1024, "KB")
