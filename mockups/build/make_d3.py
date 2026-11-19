"""Layout pass for D: split hero (type left, photograph right), photo cards for publications, photo on About."""
from common import replace_func
s = open("theme_d.py").read()

HOME = r'''
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
  </div>
</div>
"""
    return shell("index", body)
'''
s = replace_func(s, "home", HOME)

PUBS_FN = r'''
def pimg(p):
    return "../shared/img/" + ("web/rail.jpg" if "workers" in p["img"] else "web/street.jpg" if "street" in p["img"] else "web/lanterns.jpg")


def pub_list(page, kicker, title, lede, items, extra=""):
    """Header and a grid of photo cards."""
    cards = "".join(f"""<a class="pcard rise" href="{p['slug']}.html"><div class="pimg"><img src="{pimg(p)}" alt="{esc(p['alt'])}" loading="lazy"></div>
      <div class="pmeta"><span class="chip">{p['kind']}</span><span class="mono">{p['short'][:6]} · {p['min']} min</span></div><h3>{esc(p['title'])}</h3><p class="muted">{esc(p['author'])}</p></a>""" for p in items)
    return shell(page, ph(kicker, title, lede) + f'<div class="pgrid">{cards}</div>' + extra)
'''
s = replace_func(s, "pub_list", PUBS_FN)

ABOUT_FN = r'''
def about():
    """Header, a photograph beside one statement, three people."""
    team = "".join(crow(f"0{i+1}", n, f"{r}. {b}", "") for i, (n, r, b) in enumerate(ABOUT["team"]))
    body = ph("About", "About e3 Initiative") + f"""
<div class="abt"><div class="abimg rise"><img src="../shared/img/web/bakery.jpg" alt="Customers outside a bakery and produce stand in Chinatown" loading="lazy"></div>
<div class="abtx"><p style="font-weight:400;font-size:28px;line-height:1.25;letter-spacing:-.7px">{ABOUT['who']}</p><p class="muted" style="font-size:15px;line-height:1.6;margin-top:18px;max-width:60ch">{ABOUT['what']}</p></div></div>
<section style="margin-top:20px"><div class="tile rows rise">{team}</div></section>"""
    return shell("about", body)
'''
s = replace_func(s, "about", ABOUT_FN)

CSS = r"""
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
s = s.replace('CITYJS = r"""', 'CITY += r"""' + CSS + '"""\n\nCITYJS = r"""', 1)
s = s.replace("© 2026 e3 Initiative</span>", "© 2026 e3 Initiative · Photos: Wikimedia Commons, Flickr (CC)</span>")
s = s.replace('{IMG}{p["img"].replace("-640", "")}', '{pimg(p)}')

TYPE = r"""
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
s = s.replace('CITYJS = r"""', 'CITY += r"""' + TYPE + '"""\n\nCITYJS = r"""', 1)
open("theme_d.py", "w").write(s)
