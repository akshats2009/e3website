"""Photo pass for D: real photographs from the site's own archive replace the drawn skyline and covers."""
from common import replace_func
s = open("theme_d.py").read()

HOME = r'''
def home():
    """Nav, one full-bleed photograph with the headline, one line, one button, footer."""
    body = f"""
<div class="phero rise">
  <img class="p-day" src="../shared/img/street.jpg" alt="A Chinatown street with hanging lanterns and shopfront signs" fetchpriority="high">
  <img class="p-night" src="../shared/img/lanterns.jpg" alt="A lantern-lit Chinatown gate at night">
  <div class="shade"></div>
  <div class="ptxt">
    {label('Equity · Economics · Ethnicity')}
    <h1>{TAGLINE}<span>.</span></h1>
    <div class="prow"><p>Student-led research on who builds local economies, who gets credit and who gets left out.</p><div class="cta"><a class="btn" href="articles.html">Read the research</a></div></div>
  </div>
</div>
"""
    return shell("index", body)
'''
s = replace_func(s, "home", HOME)

# photo covers instead of drawn ones
s = s.replace('''def cover(i, mk=None):
    return f'<div class="cover {COVERS[i % 3]}"><span class="mk">{mk or f"E3—0{i+1}"}</span></div>\'''', '''PHOTOS = ["web/street.jpg", "web/lanterns.jpg", "web/shop.jpg", "web/skyline.jpg", "web/rail.jpg"]


def cover(i, mk=None):
    return f'<div class="cover photo"><img src="../shared/img/{PHOTOS[i % 5]}" alt="" loading="lazy"></div>\'''')
# no drawn skyline in the footer
import re
s = re.sub(r'  <div class=\\?"city mini\\?"[^\n]*\n', '', s)

PHOTO_CSS = r"""
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
s = s.replace('CITYJS = r"""', 'CITY += r"""' + PHOTO_CSS + '"""\n\nCITYJS = r"""', 1)
open("theme_d.py", "w").write(s)
