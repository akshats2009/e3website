"""Final D preview: council-picked terracotta + cream with Fraunces + DM Sans, self-hosted. Writes /d-preview."""
import os, re, shutil, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from make_preview2 import build, PHOTO, WHO, LIC, CITY_NAMES
from lab_themes import pal
ROOT = "/home/user/e3website"; OUT = f"{ROOT}/d-preview"
SC = "/tmp/claude-0/-home-user-e3website/10fabba6-8466-5a4a-8a5e-76bc7c581094/scratchpad/ff"
for src, dst in (("fraunces-opsz.woff2", "fraunces.woff2"), ("dmsans.woff2", "dmsans.woff2")):
    shutil.copy(f"{SC}/{src}", f"{OUT}/fonts/{dst}")
for old in ("sourceserif.woff2", "sourcesans.woff2"):
    p = f"{OUT}/fonts/{old}"
    if os.path.exists(p): os.remove(p)
L, D = pal("#f6ecdf", "#fffaf3", "#2a1f1a", "#65544b", "#b4472b", "#ffffff", "#1f6360", "#ffffff", "rgba(180,71,43,.22)",
           "#1a1311", "#2b201c", "#f6ece2", "#cbbaad", "#e87a57", "#1a0d08", "#63bdb7", "#0d1f1e", "rgba(232,122,87,.26)")
T = dict(light=L, dark=D, serif="Fraunces,Georgia,'Times New Roman',serif", sans="'DM Sans',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif", h1w="600", brandw="600")
FACE = "@font-face{font-family:Fraunces;src:url(/d-preview/fonts/fraunces.woff2) format('woff2');font-weight:400 700;font-display:swap}@font-face{font-family:'DM Sans';src:url(/d-preview/fonts/dmsans.woff2) format('woff2');font-weight:400 700;font-display:swap}"
PRE = '<link rel="preload" href="/d-preview/fonts/fraunces.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/d-preview/fonts/dmsans.woff2" as="font" type="font/woff2" crossorigin>'
build(T, f"{OUT}/index.html", fontlinks=PRE, fontface=FACE)
html = open(f"{OUT}/index.html").read()
# credits page = same shell, different main and a small script
rows = ""
for k, v in PHOTO.items():
    city = CITY_NAMES[k.split("-")[0]]; mode = k.split("-")[1]
    title = re.sub(r"\.jpe?g$", "", v["title"].replace("File:", "")).replace("Chicago-skyline-lake-burnham", "Chicago skyline, Lake Burnham")
    rows += f'<tr><td>{city}, {mode}</td><td><a href="{v["url"]}">{title}</a></td><td>{WHO[k]}</td><td><a href="{LIC.get(v["license"], v["url"])}">{v["license"]}</a></td></tr>'
main = f"""<main id="main" class="wrap"><div class="prose"><h1>Photo credits</h1>
<p>The city photographs on the homepage come from Wikimedia Commons and are used under the licenses below. We resized and compressed each photo for the web and cropped it to fit the layout; we made no other changes. Photos licensed CC BY-SA remain under CC BY-SA, and so does any adaptation of them.</p>
<table><thead><tr><th scope="col">Photo</th><th scope="col">Title (source)</th><th scope="col">Creator</th><th scope="col">License</th></tr></thead><tbody>{rows}</tbody></table>
<p>The article thumbnails come from the e3 Initiative archive.</p></div></main>"""
mini = "<script>(function(){var r=document.documentElement,m=document.getElementById('mode'),mn=document.getElementById('menu'),n=document.getElementById('nav');m.setAttribute('aria-pressed',r.classList.contains('night'));m.addEventListener('click',function(){var on=r.classList.toggle('night');try{localStorage.setItem('e3-night',on?'1':'0')}catch(e){}m.setAttribute('aria-pressed',on)});mn.addEventListener('click',function(){var o=n.classList.toggle('open');mn.setAttribute('aria-expanded',o)})})();</script></body></html>"
extra = "<style>.prose{max-width:820px;padding:44px 0}.prose h1{margin-bottom:18px}.prose p{margin:0 0 14px;color:var(--muted);max-width:68ch}table{width:100%;border-collapse:collapse;margin:22px 0;font-size:1rem}th,td{text-align:left;padding:12px 14px;vertical-align:top}th{font:700 .8125rem var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}tbody tr:nth-child(odd){background:var(--wash)}@media(max-width:700px){thead{display:none}table,tbody,tr,td{display:block;width:100%}tr{padding:12px 14px;border-radius:14px}td{padding:2px 0}td:first-child{font-weight:700}}</style>"
c = re.sub(r'<main id="main" class="wrap">.*?</main>', lambda m: main, html, flags=re.S)
c = re.sub(r'<script>\n\(function\(\)\{var r=document.documentElement,m=.*</script></body></html>', lambda m: mini, c, flags=re.S)
c = c.replace("</style></head>", extra.replace("<style>", "").replace("</style>", "") + "</style></head>", 1)
c = c.replace("Research on Equity, Economics, and Ethnicity (design preview)", "Photo credits").replace('aria-current=page', '')
open(f"{OUT}/credits.html", "w").write(c)
print("built", os.path.getsize(f"{OUT}/index.html") // 1024, "KB index;", sorted(os.listdir(f"{OUT}/fonts")))
