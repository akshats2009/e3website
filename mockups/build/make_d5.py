"""Cities pass for D: hero cycles New York / Chicago / San Francisco / Los Angeles; day photo in light mode, night photo in dark mode; live local time."""
import re
s = open("theme_d.py").read()

CITIES = [("New York", "America/New_York", "ny", "Times Square, Manhattan", "Brooklyn Bridge and Lower Manhattan"),
          ("Chicago", "America/Chicago", "chi", "The Chicago River and Marina City", "The Chicago skyline from the lakefront harbor"),
          ("San Francisco", "America/Los_Angeles", "sf", "The San Francisco skyline across the bay", "Downtown San Francisco and the Transamerica Pyramid"),
          ("Los Angeles", "America/Los_Angeles", "la", "Downtown Los Angeles towers", "Downtown Los Angeles towers")]

FN = '''
CITIES = %r


def citybox():
    imgs = "".join(
        f'<img class="c d{" on" if i == 0 else ""}" data-i="{i}" src="../shared/img/cities/{k}-day.jpg" alt="{dd}, in daylight">'
        f'<img class="c n{" on" if i == 0 else ""}" data-i="{i}" src="../shared/img/cities/{k}-night.jpg" alt="{nn}, at night">'
        for i, (nm, tz, k, nn, dd) in enumerate(CITIES))
    tabs = "".join(f'<button class="ct{" on" if i == 0 else ""}" data-i="{i}" data-tz="{tz}">{nm}</button>' for i, (nm, tz, k, nn, dd) in enumerate(CITIES))
    return f"""{imgs}<div class="grade"></div><div class="cts" role="tablist" aria-label="Choose a city">{tabs}</div>
<div class="loc"><svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg><span id="cname">New York</span><i></i><span id="ctime">--:--</span></div>
{dep()}"""

''' % (CITIES,)

# split nextcard() into dep() (card only)
s = re.sub(r'def nextcard\(\):.*?\n\n', lambda m: '', s, count=1, flags=re.S)
DEP = '''
def dep():
    g = DATED_SOON[0]
    d = days_left(g)
    return f"""<a class="dep" href="grants.html"><span class="dep-k">Next departure</span><span class="dep-t">{esc(g['name'])}</span><span class="dep-m"><b>{d}</b> days<i></i>{money(g.get('amountMax') or 0) if g.get('amountMax') else ''}</span></a>"""

'''
s = s.replace("def home():", DEP + FN + "\ndef home():", 1)
s = re.sub(r'<div class="spic rise">.*?\{nextcard\(\)\}\n  </div>', '<div class="spic rise" id="cities">{citybox()}</div>', s, count=1, flags=re.S)

CSS = r"""
/* cities */
.spic img.c{opacity:0;transition:opacity 1.1s ease;transform:scale(1.08)}
html:not(.night) .spic img.c.d.on{opacity:1}
html.night .spic img.c.n.on{opacity:1}
.spic .p-day,.spic .p-night{display:none}
.cts{position:absolute;left:20px;top:20px;display:flex;gap:4px;padding:4px;border-radius:99px;background:rgba(14,18,24,.42);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);z-index:3}
.ct{padding:8px 15px;border-radius:99px;font:600 .74rem var(--sans);letter-spacing:.06em;text-transform:uppercase;color:rgba(255,255,255,.78);transition:background .25s,color .25s}
.ct:hover{color:#fff}.ct.on{background:#fff;color:#101318}
.loc{z-index:3;gap:8px;top:auto;bottom:22px;right:20px}.dep{max-width:60%}.loc i{width:3px;height:3px;border-radius:50%;background:currentColor;opacity:.6}
.dep{z-index:3}
@media(max-width:900px){.loc{display:flex;top:auto;bottom:22px;right:20px;left:auto}.dep{max-width:calc(100% - 190px)}.ct{padding:7px 11px}}
"""
s = s.replace('CITYJS = r"""', 'CITY += r"""' + CSS + '"""\n\nCITYJS = r"""', 1)

JS = r"""
(function () {
  const box = document.getElementById('cities'); if (!box) return;
  const imgs = [...box.querySelectorAll('img.c')], tabs = [...box.querySelectorAll('.ct')], cname = document.getElementById('cname'), ctime = document.getElementById('ctime');
  let cur = 0, timer;
  const clock = () => { const t = tabs[cur]; ctime.textContent = new Date().toLocaleTimeString('en-US', { timeZone: t.dataset.tz, hour: 'numeric', minute: '2-digit' }); };
  function go(i) { cur = i; imgs.forEach(m => m.classList.toggle('on', +m.dataset.i === i)); tabs.forEach(t => t.classList.toggle('on', +t.dataset.i === i)); cname.textContent = tabs[i].textContent; clock(); }
  tabs.forEach(t => t.addEventListener('click', () => { go(+t.dataset.i); clearInterval(timer); }));
  clock(); setInterval(clock, 15000);
  if (!matchMedia('(prefers-reduced-motion:reduce)').matches) timer = setInterval(() => go((cur + 1) % tabs.length), 7000);
})();
"""
s = s.replace('CITYJS = r"""', 'CITYJS = r"""' + JS, 1)
# parallax should target the new images too (already selects .spic img)
open("theme_d.py", "w").write(s)
