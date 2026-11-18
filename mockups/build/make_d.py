"""Generates theme_d.py ("Night city") from theme_a.py: new palette, transit-line nav, skyline hero and footer."""
import re
from common import replace_func

s = open("theme_a.py").read()
s = s.replace('D = "site-a"', 'D = "site-d"')
s = s.replace("wght@300;400&family=Geist+Mono", "wght@300;400;600;700&family=Geist+Mono")

# palette: day = concrete + transit green, night = navy asphalt + lit windows
a = s.index(":root{\n  --bg:")
b = s.index("*,*::before,*::after{box-sizing")
PAL = r""":root{
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
"""
s = s[:a] + PAL + s[b:]
s = s.replace("html.night .mini-sw{background:var(--accent)}", "html.night .mini-sw{background:var(--accent)}")

# skyline generator (deterministic) + new homepage
SKY = r'''
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


def home():
    """Nav, headline, one line, one button, one skyline, footer."""
    body = f"""
<div class="chome">
  <div class="chero">
    {label('Equity · Economics · Ethnicity')}
    <h1>{TAGLINE}<span>.</span></h1>
    <div class="cside"><p>Student-led research on who builds local economies, who gets credit and who gets left out.</p><div class="cta"><a class="btn" href="articles.html">Read the research</a></div></div>
  </div>
  <div class="city rise" id="sky">{skyline(340)}
    <div class="route" aria-hidden="true"><i></i><b style="left:12%"></b><b style="left:38%"></b><b style="left:64%"></b><b style="left:88%"></b><em id="train"></em></div>
  </div>
</div>
"""
    return shell("index", body)
'''
s = replace_func(s, "home", SKY.split("\n\n\ndef home")[0] + "\n\n\ndef home" + SKY.split("\n\n\ndef home")[1])

# skyline silhouette above the footer on every inner page
s = s.replace("  <footer>\n    <span class=\"mono\"", "  <div class=\"city mini\" aria-hidden=\"true\">{skyline(110, True, 3)}</div>\n  <footer>\n    <span class=\"mono\"", 1)

# build() writes extra CSS and JS
s = s.replace("CSS + NOB)", "CSS + NOB + CITY)").replace('write(f"{D}/theme.js", JS)', 'write(f"{D}/theme.js", JS + CITYJS)')

s += r'''

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

CITYJS = r"""
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
'''
open("theme_d.py", "w").write(s)

# register in the gallery
b = open("build.py").read()
if '"d"' not in b:
    b = b.replace('''    ("c", "Type specimen",''', '''    ("d", "Night city", "A skyline with lit windows, a transit-line nav with stations, signage type, light and dark. Built on the paper-widgets tiles."),
    ("c", "Type specimen",''')
    b = b.replace("three site-wide directions", "four site-wide directions").replace("three designs", "four designs")
    open("build.py", "w").write(b)
