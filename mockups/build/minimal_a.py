"""Minimal pass for theme A: about seven blocks per page. Applied by rewriting functions in theme_a.py."""
from common import replace_func

HOME = r'''
def home():
    """Seven blocks: nav, hero, now reading, deadlines, publications, mission, footer."""
    soon = DATED_SOON[:6]
    rows_js = [{"t": deadline_label(g), "n": g["name"], "d": f'{g["funder"].split(" (")[0]} · {money(g.get("amountMax"))}', "chip": f"in {days_left(g)} days"} for g in soon]
    pieces = [{"t": p["title"].split(":")[0], "by": f'{p["author"]} · {p["kind"]}', "len": p["min"], "href": p["slug"] + ".html"} for p in PUBS]
    import json as _j
    body = f"""
<div class="home">
  <div class="hero">
    {label('Equity · Economics · Ethnicity')}
    <h1>{TAGLINE}<span>.</span></h1>
    <div><p>{LEDE}</p><div class="cta"><a class="btn" href="articles.html">Read the research</a></div></div>
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
    <div class="sum">{len(OPEN)} grants open · find yours →</div>
    <div class="div"></div><div class="list" id="list"><span class="chip a" id="chip"></span></div>
  </a>
  <div class="tile w2 rows rise" style="padding-top:20px">{label('Latest publications')}{''.join(crow(p['short'][:6], esc(p['title'].split(':')[0]), p['kind'], p['slug'] + '.html') for p in PUBS)}</div>
</div>
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
</script>"""
    return shell("index", body, js)
'''

PUBLIST = r'''
def pub_list(page, kicker, title, lede, items, extra=""):
    """Header, one list, a single line of related links."""
    rows = "".join(crow(p['short'][:6], esc(p['title']), f"{p['kind']} · {p['min']} min · {p['author']}", p['slug'] + '.html') for p in items)
    links = '<p class="muted" style="margin-top:22px;font-size:14px">Also: <a href="journals.html" style="color:var(--ink)">Journals</a> · <a href="economic-indicators.html" style="color:var(--ink)">Economic indicators</a></p>'
    return shell(page, ph(kicker, title, lede) + f'<div class="tile rows rise">{rows}</div>' + links)
'''

ARTICLE = r'''
def article(p):
    """Nav, title, banner, text, one side tile (progress and contents), footer."""
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
    cite = {"article-railroad": "articles/chinese-labor-transcontinental-railroad-citations.html", "article-chinatown": "articles/chinatown-citations.html", "research-chinatown": "research/chinatown-solidarity-paper-citations.html"}[p["slug"]]
    body.append(f'<p class="muted" style="font-size:14px;margin-top:2em"><a href="../../{cite}">Citations and sources →</a></p>')
    toc_html = "".join(f'<a class="crow" href="#{i}" data-sec="{i}"><span class="m"></span><div><div class="n">{esc(n)}</div></div></a>' for i, n in toc)
    body_html = f"""
<div class="read">
  <aside class="side"><div class="tile pad rise">
    {label('Now reading')}
    <div class="rprog"><b id="rb"></b><i id="rk"></i></div>
    <div style="display:flex;justify-content:space-between" class="mono muted"><span style="font-size:11px" id="rl">0 min</span><span style="font-size:11px">{p['min']} min</span></div>
    {f'<nav class="toc" aria-label="Contents" style="margin-top:12px">{toc_html}</nav>' if toc else ''}
  </div></aside>
  <article class="tile atile rise">
    {label(f"{p['kind']} · {p['date']}")}
    <h1>{esc(p['title'])}</h1>
    <div class="mono muted" style="font-size:12px">{esc(a['byline'] or 'By ' + p['author'])}</div>
    <div class="banner"><img src="{IMG}{p["img"].replace("-640", "")}" alt="{esc(p["alt"])}"></div><div class="capt">{esc(a["caption"] or p["alt"])}</div>
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
'''

ABOUT_ = r'''
def about():
    """Header, one statement, team, approach."""
    team = "".join(f"""<div class="tile pad rise c4"><div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div class="cover {COVERS[i]}" style="width:72px;border-radius:20px"></div><span class="chip">{r}</span></div>
        <div style="font-weight:300;font-size:28px;letter-spacing:-.8px;line-height:1.05;margin:24px 0 10px">{n}</div><p class="muted" style="font-size:14px;line-height:1.55">{b}</p></div>"""
        for i, (n, r, b) in enumerate(ABOUT["team"]))
    appr = "".join(crow(f"0{i+1}", t, d, "") for i, (t, d) in enumerate(ABOUT["approach"]))
    body = ph("About", "About e3 Initiative") + f"""
<div class="tile pad rise"><p style="font-weight:300;font-size:28px;line-height:1.25;letter-spacing:-.7px;max-width:44ch">{ABOUT['who']}</p><p class="muted" style="font-size:15px;line-height:1.6;margin-top:18px;max-width:70ch">{ABOUT['what']}</p></div>
<section><div class="shead"><h2>Our team</h2></div><div class="grid">{team}</div></section>
<section><div class="shead"><h2>Our approach</h2></div><div class="tile rows rise">{appr}</div></section>"""
    return shell("about", body)
'''

GRANTS = r'''
def grants():
    """Header, one filter tile (search, who, status; more filters folded away), results."""
    cats = "".join(f'<button data-v="{k}">{v}</button>' for k, v in CAT_LABEL.items())
    lists = " · ".join(f'<a href="{s}.html" style="color:var(--ink)">{CAT_LABEL[c]}</a>' for s, (c, _, _) in CATEGORY_PAGES.items())
    body = ph("Grants", "Grant Finder", f"Funding for small businesses and nonprofits. Ready-made lists: {lists}.", '<a class="btn ghost" href="grant-help.html">Help & tips →</a>') + f"""
<div class="gfind">
  <aside class="gside"><div class="tile pad rise">
    <div style="display:flex;justify-content:space-between;align-items:baseline">{label('Matching')}<span class="thin" style="font-size:40px" id="gcount">0</span></div>
    <div class="search" style="margin-top:16px">{icon('search')}<input class="inp" id="q" type="search" placeholder="Women-owned bakery…" aria-label="Search grants"></div>
    <div class="fl">{label('Who qualifies')}<div class="seg" data-f="elig"><button class="on" data-v="">Anyone</button><button data-v="small_business">Business</button><button data-v="nonprofit">Nonprofit</button></div></div>
    <div class="fl">{label('Status')}<div class="seg" data-f="status"><button class="on" data-v="live">Open + rolling</button><button data-v="">All</button></div></div>
    <details class="fl"><summary class="label" style="cursor:pointer">More filters</summary>
      <div class="fl">{label('Award up to at least')}<div class="seg" data-f="amt"><button class="on" data-v="0">Any</button><button data-v="10000">$10k</button><button data-v="50000">$50k</button><button data-v="250000">$250k</button></div></div>
      <div class="fl">{label('Category')}<div class="seg" data-f="cat" data-multi><button class="on" data-v="">All</button>{cats}</div></div></details>
  </div></aside>
  <div class="tile gres rise" id="gres" aria-live="polite"></div>
</div>"""
    js = """<script src="../shared/grants-data.js"></script><script>
const F = { q: '', elig: '', status: 'live', amt: 0, cat: new Set() };
$$('.seg[data-f]').forEach(seg => seg.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; const f = seg.dataset.f;
  if (seg.hasAttribute('data-multi')) { if (!b.dataset.v) { F.cat.clear(); $$('button', seg).forEach(x => x.classList.toggle('on', !x.dataset.v)); }
    else { F.cat.has(b.dataset.v) ? F.cat.delete(b.dataset.v) : F.cat.add(b.dataset.v); b.classList.toggle('on'); $('button[data-v=""]', seg).classList.toggle('on', !F.cat.size); } }
  else { $$('button', seg).forEach(x => x.classList.toggle('on', x === b)); F[f] = f === 'amt' ? +b.dataset.v : b.dataset.v; } render(); }));
$('#q').addEventListener('input', e => { F.q = e.target.value.toLowerCase(); render(); });
function render() {
  const rs = GRANTS.filter(g => (!F.q || (g.name + g.funder + g.desc + CAT_LABEL[g.cat]).toLowerCase().includes(F.q))
    && (!F.elig || g.elig === F.elig || g.elig === 'both') && (F.status === '' || g.status !== 'closed')
    && (!F.amt || g.max >= F.amt) && (!F.cat.size || F.cat.has(g.cat)))
    .sort((a, b) => ({ open: 0, rolling: 1, closed: 2 }[a.status] - { open: 0, rolling: 1, closed: 2 }[b.status]) || (a.days ?? 999) - (b.days ?? 999));
  $('#gcount').textContent = rs.length;
  $('#gres').innerHTML = rs.length ? rs.map(g => { const dt = g.days != null ? g.dl.split(' ') : null;
    return `<div class="grow ${g.status}" tabindex="0"><div class="dd">${dt ? `<b>${+dt[1]}</b><span>${dt[0]}</span>` : `<b style="font-size:20px">∞</b><span>${g.dl}</span>`}</div>
      <div><div class="n">${g.name}</div><div class="f">${g.funder}</div></div><div class="amt">${g.max ? 'up to $' + g.max.toLocaleString() : 'Varies'}</div>
      <div class="st">${g.status === 'open' ? `<span class="chip a">${g.days != null ? 'in ' + g.days + 'd' : 'Open'}</span>` : `<span class="chip">${g.status === 'rolling' ? 'Rolling' : 'Closed'}</span>`}</div>
      <div class="gdetail">${g.desc}<br><a class="btn sm" href="${g.link}" target="_blank" rel="noopener">Funder's page →</a></div></div>`; }).join('')
    : '<div style="padding:40px 0;text-align:center" class="muted">No grants match these filters. Try widening them.</div>';
}
$('#gres').addEventListener('click', e => { const r = e.target.closest('.grow'); if (r && !e.target.closest('a')) r.classList.toggle('x'); });
$('#gres').addEventListener('keydown', e => { if (e.key === 'Enter' && e.target.classList.contains('grow')) e.target.classList.toggle('x'); });
render();
</script>"""
    return shell("grants", body, js)
'''

CATEGORY = r'''
def category(slug):
    """Header, counts, the list, one line of other lists."""
    cat, title, what = CATEGORY_PAGES[slug]
    intro, gs = category_intro(cat, what)
    gs = sorted(gs, key=lambda g: ({"open": 0, "rolling": 1, "closed": 2}[status(g)], days_left(g) if days_left(g) is not None else 999))
    c = {s: sum(1 for g in gs if status(g) == s) for s in ("open", "rolling", "closed")}
    rows = "".join(crow(deadline_label(g), esc(g["name"]), esc(g["funder"]) + " · " + esc(g["amount"]), g["link"], status_chip(status(g), days_left(g)), status(g) == "open") for g in gs)
    others = " · ".join(f'<a href="{s}.html" style="color:var(--ink)">{CAT_LABEL[v[0]]}</a>' for s, v in CATEGORY_PAGES.items() if s != slug)
    body = ph("Grant list", title, intro) + f"""
<div class="grid">
  <div class="tile pad rise c4" style="align-self:start">{label('In this list')}<div class="count-num" data-count="{len(gs)}">0</div>
    <div style="margin-top:14px">{lvl('spark', 'Open now', c['open']/len(gs)*100, True)}{lvl('link', 'Rolling', c['rolling']/len(gs)*100)}{lvl('doc', 'Closed for now', c['closed']/len(gs)*100)}</div></div>
  <div class="tile rows rise c8">{rows}</div>
</div>
<p class="muted" style="margin-top:22px;font-size:14px">More lists: {others} · <a href="grants.html" style="color:var(--ink)">Search all {len(GRANTS)}</a></p>"""
    return shell(slug, body)
'''

HELP_ = r'''
def grant_help():
    """Header, checklist (mistakes folded inside), progress, free-help directory."""
    tips = "".join(f'<button class="check" data-i="{i}"><span class="bx">{icon("check", 14)}</span><div><b>{a}</b><p>{b}</p></div></button>' for i, (a, b) in enumerate(HELP["tips"]))
    orgs = "".join(crow("→", n, d, u, f'<span class="chip">{l}</span>') for n, d, l, u in HELP["orgs"])
    body = ph("Grants", "Grant Help & Tips", HELP["intro"], '<a class="btn" href="grants.html">Search grants →</a>') + f"""
<div class="grid">
  <div class="tile rows rise c8" style="padding-top:18px">{label('How to write a strong application')}<div style="margin-top:6px">{tips}</div>
    <details style="padding:16px 0;border-top:1px solid var(--line)"><summary class="label" style="cursor:pointer">Common mistakes to avoid</summary><ul style="margin:12px 0 0 18px;color:var(--muted);font-size:14px;line-height:1.7">{''.join(f'<li>{m}</li>' for m in HELP['mistakes'])}</ul></details></div>
  <div class="tile pad rise c4" style="text-align:center;align-self:start">{label('Your progress')}
    <div style="position:relative;width:200px;height:200px;margin:14px auto 0"><svg class="dial" id="hdial" width="200" height="200" viewBox="0 0 200 200" aria-hidden="true"></svg>
    <div style="position:absolute;inset:0;display:grid;place-items:center"><div><div class="thin" style="font-size:44px" id="hcount">0/8</div><div class="muted" style="font-size:13px;margin-top:4px">steps done</div></div></div></div></div>
</div>
<section><div class="shead"><h2>Where to get free help</h2></div><div class="tile rows rise">{orgs}</div><p class="muted" style="font-size:12px;line-height:1.6;margin-top:16px;max-width:80ch">{HELP['disclaimer']}</p></section>"""
    js = """<script>
const setH = buildDial($('#hdial'), 0, 200), done = new Set(JSON.parse(localStorage.getItem('e3-help') || '[]'));
function upd() { $$('.check[data-i]').forEach(c => c.classList.toggle('done', done.has(+c.dataset.i))); $('#hcount').textContent = done.size + '/8'; setH(Math.round(done.size / 8 * 60)); localStorage.setItem('e3-help', JSON.stringify([...done])); }
$$('.check[data-i]').forEach(c => c.addEventListener('click', () => { const i = +c.dataset.i; done.has(i) ? done.delete(i) : done.add(i); upd(); })); setTimeout(upd, 900);
</script>"""
    return shell("grant-help", body, js)
'''

CONTACT = r'''
def contact():
    """Header, form, one side tile."""
    body = ph("Contact", "Let's connect", "Have questions about our research or want to collaborate? Send a message and we will respond within two business days.") + f"""
<div class="grid">
  <form class="tile pad rise c8" onsubmit="event.preventDefault();this.querySelector('[data-sent]').hidden=false" style="padding:30px">
    <div class="grid" style="gap:0 16px"><label class="field c6"><span><i></i>Name *</span><input class="inp" required autocomplete="name"></label>
    <label class="field c6"><span><i></i>Email *</span><input class="inp" type="email" required autocomplete="email"></label></div>
    <label class="field"><span><i></i>Subject *</span><input class="inp" required></label>
    <label class="field"><span><i></i>Message *</span><textarea class="inp" required></textarea></label>
    <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap"><button class="btn" type="submit">Send message →</button><span class="chip a" data-sent hidden>Mockup: nothing was sent</span></div>
  </form>
  <div class="tile pad rise c4" style="align-self:start"><div style="display:flex;gap:16px;align-items:center"><svg class="dial" data-lit="10" width="88" height="88" viewBox="0 0 200 200" aria-hidden="true"></svg><div>{label('Reply within')}<div class="thin" style="font-size:36px;margin-top:6px">2 days</div></div></div>
    <p class="muted" style="font-size:14px;line-height:1.55;margin-top:18px">Want to be interviewed? Say so in your message. We use your details only to reply (<a href="privacy.html" style="color:var(--ink)">privacy</a>).</p></div>
</div>"""
    return shell("contact", body)
'''

INDIC = r'''
def indicators():
    """Header, four key charts, the other four behind one button."""
    def tile(k, grp, name, u, d, extra):
        return f"""<div class="tile ind rise c6{extra}" data-key="{k}" data-unit="{u}">
      {label(f'{grp}: {name}')}<div class="tr mono" data-hl></div>
      <div class="val"><span data-v>—</span><small>{u if u != 'index' else 'index'}</small></div>
      <svg viewBox="0 0 500 96" preserveAspectRatio="none" aria-hidden="true"></svg>
      <div class="yrs"><span>2000</span><span data-end>today</span></div>
      <p class="desc">{d}</p></div>"""
    key = [i for i in INDICATORS if i[0] in KEY_INDICATORS]
    more = [i for i in INDICATORS if i[0] not in KEY_INDICATORS]
    body = ph("Data", "Economic Indicators", "Everyday costs, job security and borrowing rates since 2000. Hover a chart to read any year.") + f"""
<div class="note" id="note" hidden>{icon('spark')}<span>Preview: placeholder shapes. Live FRED data loads from <span class="mono">/api/economic-indicators</span> on the deployed site.</span></div>
<div class="grid">{''.join(tile(*i, '') for i in key)}{''.join(tile(*i, ' more') for i in more)}</div>
<div style="text-align:center;margin-top:24px"><button class="btn ghost" id="moreb" onclick="document.querySelectorAll('.ind.more').forEach(e=>e.hidden=false);this.remove()">Show all 8 indicators</button></div>"""
    js = """<script src="../shared/indicators.js"></script><script>
$$('.ind.more').forEach(e => e.hidden = true);
loadIndicators().then(D => {
  $('#note').hidden = D.live;
  $$('.ind').forEach(t => { const s = D.series[t.dataset.key]; if (!s) return; const svg = $('svg', t), n = s.length, lo = Math.min(...s), hi = Math.max(...s);
    const x = i => i / (n - 1) * 500, y = v => 86 - (v - lo) / (hi - lo || 1) * 76;
    const d = s.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1)).join(' ');
    svg.innerHTML = `<line x1="0" x2="500" y1="90" y2="90" stroke="var(--hair)"/><path d="${d}" fill="none" stroke="var(--dotted)" stroke-width="1.2" stroke-dasharray="2 4" vector-effect="non-scaling-stroke"/>
      <path class="ln" d="${d}" fill="none" stroke="var(--ink)" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" vector-effect="non-scaling-stroke" style="transition:stroke-dashoffset 1.4s cubic-bezier(.65,0,.35,1)"/>
      <circle class="dot" cx="${x(n - 1)}" cy="${y(s[n - 1])}" r="5" fill="var(--accent)"/>`;
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
'''


def apply():
    p = "theme_a.py"
    s = open(p).read()
    for name, src in [("home", HOME), ("pub_list", PUBLIST), ("article", ARTICLE), ("about", ABOUT_), ("grants", GRANTS),
                      ("category", CATEGORY), ("grant_help", HELP_), ("contact", CONTACT), ("indicators", INDIC)]:
        s = replace_func(s, name, src)
    # Publications = everything; research keeps its own filtered list; no extra blocks
    s = s.replace('"articles": pub_list("articles", "Publications", "Articles", "Perspectives and community insights from our team and partners, from grassroots organizing to systemic policy analysis.", ARTICLES)',
                  '"articles": pub_list("articles", "Publications", "Publications", "Articles and research papers from our team and partners, from grassroots history to systemic policy analysis.", PUBS)')
    s = s.replace('.home{display:grid;grid-template-columns:repeat(4,var(--cell));grid-auto-rows:var(--cell);gap:var(--gap)}',
                  '.home{display:grid;grid-template-columns:repeat(4,var(--cell));grid-auto-rows:var(--cell);gap:var(--gap)}\n.home .rows .crow{padding:13px 0}.home .rows .crow .m{height:28px}')
    s = s.replace('.toc .crow{grid-template-columns:3px 1fr;padding:12px 0}', '.toc .crow{grid-template-columns:3px 1fr;padding:10px 0;border-top:1px solid var(--line)}')
    s = s.replace('details summary::-webkit-details-marker{display:none}', '')
    s = s.replace('@media (max-width:1300px){', 'summary{list-style:none}summary::-webkit-details-marker{display:none}summary.label::after{content:"+";margin-left:6px}\n@media (max-width:1300px){', 1)
    open(p, "w").write(s)


if __name__ == "__main__":
    apply()
