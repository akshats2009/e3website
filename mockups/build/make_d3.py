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
    <img class="p-day" src="../shared/img/street.jpg" alt="A Chinatown street with hanging lanterns and shopfront signs" fetchpriority="high">
    <img class="p-night" src="../shared/img/lanterns.jpg" alt="A lantern-lit Chinatown gate at night">
  </div>
</div>
"""
    return shell("index", body)
'''
s = replace_func(s, "home", HOME)

PUBS_FN = r'''
def pimg(p):
    return "../shared/img/" + ("workers.jpg" if "workers" in p["img"] else "street.jpg" if "street" in p["img"] else "lanterns.jpg")


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
<div class="abt"><div class="abimg rise"><img src="../shared/img/gate.jpg" alt="A decorated Chinatown gate at dusk" loading="lazy"></div>
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
s = s.replace('{IMG}{p["img"].replace("-640", "")}', '{pimg(p)}')
open("theme_d.py", "w").write(s)
