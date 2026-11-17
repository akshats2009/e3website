"""Homepage-only minimal pass: headline, one line, one button, one signature element."""
from common import replace_func

HOME_A = r'''
def home():
    """Nav, hero, one player tile, footer."""
    pieces = [{"t": p["title"].split(":")[0], "by": f'{p["author"]} · {p["kind"]}', "len": p["min"], "href": p["slug"] + ".html"} for p in PUBS]
    import json as _j
    body = f"""
<div class="home">
  <div class="hero">
    {label('Equity · Economics · Ethnicity')}
    <h1>{TAGLINE}<span>.</span></h1>
    <div><p>Student-led research on who builds local economies, who gets credit and who gets left out.</p><div class="cta"><a class="btn" href="articles.html">Read the research</a></div></div>
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
</div>
"""
    js = f"""<script>
const PIECES = {_j.dumps(pieces)};
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
</script>"""
    return shell("index", body, js)
'''

HOME_B = r'''
def home():
    """Nav, hero, one three-channel mixer, footer."""
    three = [("minority_owned", "Minority", "#f1f1f3"), ("women_owned", "Women", "#c6c6cb"), ("veteran_owned", "Veteran", "#8a8a90")]
    G = [[g["category"], g["name"], g["funder"].split(" (")[0], g.get("amountMax") or 0, days_left(g)] for g in OPEN if g["category"] in [a for a, _, _ in three]]
    body = ph("Equity · Economics · Ethnicity", f"{TAGLINE}<span>.</span>", "Student-led research on who builds local economies, who gets credit and who gets left out.",
              '<div style="margin-top:26px"><a class="mbtn" href="articles.html">Read the research</a></div>') + panel(f"""
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
    <div><div class="cap">Grant mixer</div><div style="font-size:30px;letter-spacing:-.02em;margin-top:10px">Find funding in seconds</div></div>
    <div style="text-align:right"><div class="cap">Matching</div><div class="mono" style="font-size:30px;letter-spacing:-.02em;margin-top:10px" id="tot">0</div></div>
  </div>
  <div class="board mini3" id="board">
    <div class="master vline">
      <div class="cap">Deadline window</div>
      <div class="knob" id="win" data-label="Deadline window" style="margin:22px auto 0"></div>
      <div style="text-align:center;margin-top:8px"><div style="font-size:24px;letter-spacing:-.02em" id="wl">Any time</div></div>
      <a class="mbtn" href="grants.html" style="margin-top:26px;width:100%;justify-content:center">See the grants</a>
    </div>
  </div>""", "desk")
    js = f"""<script>
const G = {json.dumps(G, ensure_ascii=False)}, CH = {json.dumps([{"id": a, "name": b, "shade": c} for a, b, c in three])};
const WIN = [[14, '14 days', '14D'], [30, '30 days', '30D'], [60, '60 days', '60D'], [Infinity, 'Any time', 'ANY']];
const money = v => v >= 1e6 ? '$' + (v / 1e6).toFixed(v % 1e6 ? 1 : 0) + 'M' : v >= 1000 ? '$' + Math.round(v / 1000) + 'k' : '$' + Math.round(v);
const valAt = p => p < .08 ? 0 : Math.pow(10, 3 + 3 * (p - .08) / .92), posOf = v => v <= 0 ? 0 : .08 + .92 * (Math.log10(v) - 3) / 3;
const mins = {{}}; let win = 3;
CH.forEach(c => {{ mins[c.id] = 0; const s = document.createElement('div'); s.className = 'strip vline';
  const tk = [[1, '1M'], [posOf(1e5), '100k'], [posOf(1e4), '10k'], [0, '0']].map(([p, l]) => `<span style="top:${{(1 - p) * 100}}%">${{l}}</span>`).join('');
  s.innerHTML = `<div class="nm cap"><i style="background:${{c.shade}}"></i>${{c.name}}-owned</div>
    <div class="fader"><div class="fticks">${{tk}}</div><div class="trk"><div class="fill"></div></div><div class="fcap" tabindex="0" role="slider" aria-label="Minimum award, ${{c.name}}-owned"></div></div>
    <div class="lm">${{Array.from({{ length: 10 }}, (_, k) => `<i style="top:${{300 - (k + 1) * 30 + 3}}px"></i>`).join('')}}</div><div class="tag"></div>
    <div class="val"></div><div class="share cap"></div>`;
  $('#board').insertBefore(s, $('.master')); c.el = s;
  makeFader($('.fader', s), 0, p => {{ mins[c.id] = valAt(p); render(); }}); }});
const knob = makeKnob($('#win'), WIN.map(w => w[2]), 3, i => {{ win = i; render(); }});
function render() {{ const W = WIN[win][0]; let M = 0;
  CH.forEach(c => {{ const hit = G.filter(g => g[0] === c.id && (!g[3] || g[3] >= mins[c.id]) && (g[4] === null || g[4] <= W)), dated = hit.filter(g => g[4] !== null).sort((a, b) => a[4] - b[4]);
    M += hit.length; const lit = hit.length * 2, amber = dated.length * 2, s = c.el;
    $$('.lm i', s).forEach((m, k) => m.className = k < lit ? (k >= lit - amber ? 'near' : 'on') : '');
    const tag = $('.tag', s); tag.style.opacity = dated.length ? 1 : 0; tag.textContent = dated.length ? dated[0][4] + 'd' : ''; tag.style.top = 84 + 300 - Math.max(lit, 1) * 30 - 30 + 'px';
    $('.val', s).textContent = mins[c.id] ? '≥' + money(mins[c.id]) : 'Any amount'; $('.share', s).textContent = hit.length + ' match'; }});
  $('#wl').textContent = WIN[win][1]; $('#tot').textContent = M; }}
render();
if (!reduce) setTimeout(() => knob.set(2), 900);
</script>"""
    return shell("index", body, js)
'''


def apply():
    for fn, name, src in [("theme_a.py", "home", HOME_A), ("theme_b.py", "home", HOME_B)]:
        s = open(fn).read()
        open(fn, "w").write(replace_func(s, name, src))
    # C: keep the specimen and the lede; drop the index and the closing-soon table
    s = open("theme_c.py").read()
    a = s.index('<section><div class="sh"><h2>Index</h2>')
    b = s.index('</table></section>"""', a) + len('</table></section>')
    s = s[:a] + s[b:]
    s = s.replace('<div><p>{LEDE}</p><div class="btns"><a class="pill" href="articles.html">Read the research</a></div></div>',
                  '<div><p>Student-led research on who builds local economies, who gets credit and who gets left out.</p><div class="btns"><a class="pill" href="articles.html">Read the research</a></div></div>')
    open("theme_c.py", "w").write(s)


if __name__ == "__main__":
    apply()
