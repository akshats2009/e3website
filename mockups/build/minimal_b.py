"""Minimal pass for theme B: about seven blocks per page."""
from common import replace_func

HOME = r'''
def home():
    """Seven blocks: nav, hero, a three-channel mixer, its top matches, the latest piece, mission, footer."""
    three = [("minority_owned", "Minority", "#f1f1f3"), ("women_owned", "Women", "#c6c6cb"), ("veteran_owned", "Veteran", "#8a8a90")]
    G = [[g["category"], g["name"], g["funder"].split(" (")[0], g.get("amountMax") or 0, days_left(g)] for g in OPEN if g["category"] in [a for a, _, _ in three]]
    p0 = PUBS[0]
    body = ph("Equity · Economics · Ethnicity", f"{TAGLINE}<span>, and the money to build them.</span>", LEDE,
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
      <div style="margin-top:22px"><div class="mrow cap">Closing soon<b id="mC" style="color:rgb(var(--led-near))">—</b></div><div class="mrow cap">Rolling<b id="mR">—</b></div></div>
    </div>
  </div>
  <div id="results" style="margin-top:6px" aria-live="polite"></div>""", "desk") + f"""
<section><div class="shead"><div><div class="cap">Latest</div><h2>Publications</h2></div><a href="articles.html">All publications →</a></div>
  {panel(f'<img src="{IMG}{p0["img"]}" alt="{esc(p0["alt"])}"><div class="txt"><div><div class="cap">{p0["kind"]} · {p0["short"]} · {p0["author"]}</div><h3>{esc(p0["title"].split(":")[0])}</h3></div><div><p>{esc(p0["summary"])}</p><div style="display:flex;gap:12px;align-items:center;margin-top:20px">{meter(12, p0["min"])}<span class="cap">{p0["min"]} min</span></div></div></div>', "feat", "a", f'href="{p0["slug"]}.html"')}
</section>
<section><div class="cap">Mission</div><p style="font-weight:300;font-size:40px;line-height:1.15;letter-spacing:-.03em;max-width:28ch;margin-top:18px">{MISSION.replace(', fostering', ',<span class=dim> fostering').replace('backgrounds.', 'backgrounds.</span>')}</p></section>"""
    js = f"""<script>
const G = {json.dumps(G, ensure_ascii=False)}, CH = {json.dumps([{"id": a, "name": b, "shade": c} for a, b, c in three])};
const WIN = [[14, '14 days', '14D'], [30, '30 days', '30D'], [60, '60 days', '60D'], [Infinity, 'Any time', 'ANY']];
const money = v => v >= 1e6 ? '$' + (v / 1e6).toFixed(v % 1e6 ? 1 : 0) + 'M' : v >= 1000 ? '$' + Math.round(v / 1000) + 'k' : '$' + Math.round(v);
const valAt = p => p < .08 ? 0 : Math.pow(10, 3 + 3 * (p - .08) / .92), posOf = v => v <= 0 ? 0 : .08 + .92 * (Math.log10(v) - 3) / 3;
const mins = {{}}, faders = {{}}; let win = 3;
CH.forEach(c => {{ mins[c.id] = 0; const s = document.createElement('div'); s.className = 'strip vline';
  const tk = [[1, '1M'], [posOf(1e5), '100k'], [posOf(1e4), '10k'], [0, '0']].map(([p, l]) => `<span style="top:${{(1 - p) * 100}}%">${{l}}</span>`).join('');
  s.innerHTML = `<div class="nm cap"><i style="background:${{c.shade}}"></i>${{c.name}}-owned</div>
    <div class="fader"><div class="fticks">${{tk}}</div><div class="trk"><div class="fill"></div></div><div class="fcap" tabindex="0" role="slider" aria-label="Minimum award, ${{c.name}}-owned"></div></div>
    <div class="lm">${{Array.from({{ length: 10 }}, (_, k) => `<i style="top:${{300 - (k + 1) * 30 + 3}}px"></i>`).join('')}}</div><div class="tag"></div>
    <div class="val"></div><div class="share cap"></div>`;
  $('#board').insertBefore(s, $('.master')); c.el = s;
  faders[c.id] = makeFader($('.fader', s), 0, p => {{ mins[c.id] = valAt(p); render(); }}); }});
const knob = makeKnob($('#win'), WIN.map(w => w[2]), 3, i => {{ win = i; render(); }});
function render() {{ const W = WIN[win][0]; let M = 0, Cl = 0, R = 0; const shown = [];
  CH.forEach(c => {{ const hit = G.filter(g => g[0] === c.id && (!g[3] || g[3] >= mins[c.id]) && (g[4] === null || g[4] <= W)), dated = hit.filter(g => g[4] !== null).sort((a, b) => a[4] - b[4]);
    M += hit.length; Cl += dated.length; R += hit.length - dated.length; shown.push(...hit);
    const lit = hit.length * 2, amber = dated.length * 2, s = c.el;
    $$('.lm i', s).forEach((m, k) => m.className = k < lit ? (k >= lit - amber ? 'near' : 'on') : '');
    const tag = $('.tag', s); tag.style.opacity = dated.length ? 1 : 0; tag.textContent = dated.length ? dated[0][4] + 'd' : ''; tag.style.top = 84 + 300 - Math.max(lit, 1) * 30 - 30 + 'px';
    $('.val', s).textContent = mins[c.id] ? '≥' + money(mins[c.id]) : 'Any amount'; $('.share', s).textContent = hit.length + ' match'; }});
  $('#wl').textContent = WIN[win][1]; $('#tot').textContent = M; $('#mC').textContent = Cl || '—'; $('#mR').textContent = R;
  shown.sort((a, b) => (a[4] ?? 999) - (b[4] ?? 999) || b[3] - a[3]);
  $('#results').innerHTML = shown.slice(0, 3).map(g => `<a class="rrow" href="grants.html" style="grid-template-columns:14px 1fr 120px 90px"><span class="led ${{g[4] !== null ? 'near' : 'on'}}"></span><div><div class="n">${{g[1]}}</div><div class="f">${{g[2]}}</div></div><span class="a">${{g[3] ? 'up to ' + money(g[3]) : 'varies'}}</span><span class="d ${{g[4] !== null ? 'near' : ''}}">${{g[4] !== null ? 'in ' + g[4] + 'd' : 'rolling'}}</span></a>`).join('')
    + `<a class="empty" href="grants.html" style="display:block">${{shown.length > 3 ? '+ ' + (shown.length - 3) + ' more · ' : ''}}open the full grant finder →</a>`; }}
render();
if (!reduce) setTimeout(() => knob.set(2), 900);
</script>"""
    return shell("index", body, js)
'''

PUBLIST = r'''
def pub_list(page, title, lede, items, extra=""):
    """Header, one index panel, one line of related links."""
    rows = panel('<div class="rows">' + "".join(prow(p) for p in items) + "</div>")
    links = '<p class="cap" style="margin-top:22px">Also · <a href="journals.html" style="color:var(--text)">Journals</a> · <a href="economic-indicators.html" style="color:var(--text)">Economic indicators</a></p>'
    return shell(page, ph("Publications", title, lede) + rows + links)
'''

ARTICLE = r'''
def article(p):
    """Nav, article (title, banner, text), one side panel: progress and sections."""
    a = p["data"]
    secs, body = [], []
    for i, (t, txt) in enumerate(a["blocks"]):
        if t == "h2":
            secs.append((f"s{i}", re.sub(r"<[^>]+>", "", txt)))
            body.append(f'<h2 id="s{i}">{txt}</h2>')
        elif t == "li":
            body.append(f"<ul><li>{txt}</li></ul>")
        else:
            body.append(f"<{t}>{txt}</{t}>")
    cite = {"article-railroad": "articles/chinese-labor-transcontinental-railroad-citations.html", "article-chinatown": "articles/chinatown-citations.html", "research-chinatown": "research/chinatown-solidarity-paper-citations.html"}[p["slug"]]
    body.append(f'<p><a href="../../{cite}">Citations and sources →</a></p>')
    side = panel(f"""<div class="cap">Progress</div><div style="display:flex;gap:22px;align-items:flex-end;margin-top:18px">
      <span class="meter v" id="pm">{"<i></i>" * 24}</span><div><div class="mono" style="font-size:34px;letter-spacing:-.02em" id="pp">0%</div><div class="cap" style="margin-top:6px" id="pl">{p["min"]} min left</div></div></div>
      {('<nav class="secs" style="margin-top:22px">' + "".join(f'<a href="#{i}" data-s="{i}"><span class="led"></span>{esc(n)}</a>' for i, n in secs) + '</nav>') if secs else ''}""", "pad")
    body_html = f"""<div class="read" style="margin-top:40px">
  {panel(f"""<div class="cap">{p["kind"]} · {p["date"]}</div><h1>{esc(p["title"])}</h1><div class="cap" style="letter-spacing:.1em">{esc(a["byline"] or "By " + p["author"])}</div>
    <div class="banner"><img src="{IMG}{p["img"].replace("-640", "")}" alt="{esc(p["alt"])}"></div><div class="capt">{esc(a["caption"] or p["alt"])}</div>
    <div class="prose" id="prose">{"".join(body)}</div>""", "atile", "article")}
  <aside class="rside">{side}</aside></div>"""
    js = f"""<script>
const pr = $('#prose'), segs = $$('#pm i');
function upd() {{ const r = pr.getBoundingClientRect(), k = Math.max(0, Math.min(1, (innerHeight * .4 - r.top) / r.height));
  segs.forEach((s, i) => s.className = i < Math.round(k * 24) ? (i >= 20 ? 'near' : 'on') : '');
  $('#pp').textContent = Math.round(k * 100) + '%'; $('#pl').textContent = Math.max(0, Math.round((1 - k) * {p['min']})) + ' min left';
  let cur = null; $$('#prose h2').forEach(h => {{ if (h.getBoundingClientRect().top < innerHeight * .35) cur = h.id; }}); $$('.secs a').forEach(a => a.classList.toggle('on', a.dataset.s === cur)); }}
addEventListener('scroll', upd, {{ passive: true }}); upd();
</script>"""
    return shell(p["slug"], body_html, js)
'''

ABOUT_ = r'''
def about():
    """Header, one statement, team, approach."""
    team = panel('<div class="grid" style="gap:0">' + "".join(f"""<div class="vline c4 pad">
      <div style="height:44px;margin-bottom:20px;border-radius:12px;background:var(--metal);box-shadow:var(--metal-shadow);display:flex;align-items:center;padding:0 16px;color:#111;font:500 12px var(--mono);letter-spacing:.08em;text-transform:uppercase">{n}</div>
      <div class="cap" style="color:var(--text)">{r}</div><p class="dim" style="font-size:14px;line-height:1.6;margin-top:12px">{b}</p></div>""" for n, r, b in ABOUT["team"]) + "</div>")
    appr = panel('<div class="rows">' + "".join(f'<div class="mrow" style="border:0;border-top:1px solid var(--row-line);padding:18px 0;justify-content:flex-start;gap:24px"><span class="cap">0{i+1}</span><span style="font-size:17px;min-width:220px">{t}</span><span class="dim" style="font-size:14px">{d}</span></div>' for i, (t, d) in enumerate(ABOUT["approach"])) + "</div>")
    body = ph("About", "About e3 Initiative", ABOUT["what"]) + f"""
{panel(f'<p style="font-weight:300;font-size:26px;line-height:1.35;letter-spacing:-.02em;max-width:48ch">{ABOUT["who"]}</p>', "pad")}
<section><div class="shead"><div><div class="cap">On the desk</div><h2>Our team</h2></div></div>{team}</section>
<section><div class="shead"><div><div class="cap">We believe in</div><h2>Our approach</h2></div></div>{appr}</section>"""
    return shell("about", body)
'''

GRANTS = r'''
def grants():
    """Header, a compact desk (search, who, status, window; categories folded), results."""
    cats = "".join(f'<button class="key" data-v="{k}">{v}</button>' for k, v in CAT_LABEL.items())
    lists = " · ".join(f'<a href="{s}.html" style="color:var(--text)">{CAT_LABEL[c]}</a>' for s, (c, _, _) in CATEGORY_PAGES.items())
    body = ph("Grants", "Grant Finder", f"Funding for small businesses and nonprofits. Ready-made lists: {lists}.", '<a class="mbtn ghost" href="grant-help.html" style="margin-top:20px">Help & tips →</a>') + panel(f"""
  <div style="display:grid;grid-template-columns:1fr 200px;gap:34px" class="gdesk">
    <div>
      <label class="field"><span class="cap">Search</span><input class="inp" id="q" type="search" placeholder="WOMEN-OWNED BAKERY…" aria-label="Search grants"></label>
      <div style="display:flex;gap:30px;flex-wrap:wrap">
        <div><div class="cap" style="margin:6px 0 10px">Who qualifies</div><div class="keys" data-group="elig"><button class="key on" data-v="">Anyone</button><button class="key" data-v="small_business">Business</button><button class="key" data-v="nonprofit">Nonprofit</button></div></div>
        <div><div class="cap" style="margin:6px 0 10px">Status</div><div class="keys" data-group="status"><button class="key on" data-v="live">Open + rolling</button><button class="key" data-v="">Include closed</button></div></div>
      </div>
      <details style="margin-top:18px"><summary class="cap" style="cursor:pointer">+ Categories</summary><div class="keys" data-group="cat" data-multi style="margin-top:12px">{cats}</div></details>
    </div>
    <div class="vline" style="padding-left:24px"><div class="cap">Deadline window</div><div class="knob" id="win" data-label="Deadline window" style="margin:14px auto 0"></div>
      <div class="mrow cap" style="margin-top:14px">Matching<b id="mM">—</b></div></div>
  </div>""", "desk") + panel('<div class="rows" id="gres" aria-live="polite"></div>', "", attrs='style="margin-top:20px"')
    js = """<script src="../shared/grants-data.js"></script><script>
const F = { q: '', elig: '', status: 'live', cat: new Set(), win: 3 }, WIN = [[14, '14D'], [30, '30D'], [90, '90D'], [Infinity, 'ANY']];
makeKnob($('#win'), WIN.map(w => w[1]), 3, i => { F.win = i; render(); });
$$('.keys[data-group]').forEach(g => g.addEventListener('change', () => { const on = $$('.key.on', g).map(k => k.dataset.v);
  if (g.dataset.group === 'cat') F.cat = new Set(on); else F[g.dataset.group] = on[0] ?? ''; render(); }));
$('#q').addEventListener('input', e => { F.q = e.target.value.toLowerCase(); render(); });
function render() { const W = WIN[F.win][0];
  const rs = GRANTS.filter(g => (!F.q || (g.name + g.funder + g.desc + CAT_LABEL[g.cat]).toLowerCase().includes(F.q)) && (!F.elig || g.elig === F.elig || g.elig === 'both')
    && (F.status === '' || g.status !== 'closed') && (!F.cat.size || F.cat.has(g.cat)) && (W === Infinity || (g.days != null && g.days <= W && g.days >= 0)))
    .sort((a, b) => ({ open: 0, rolling: 1, closed: 2 }[a.status] - { open: 0, rolling: 1, closed: 2 }[b.status]) || (a.days ?? 999) - (b.days ?? 999));
  $('#mM').textContent = rs.length;
  $('#gres').innerHTML = rs.length ? rs.map(g => { const c = g.status === 'closed' ? 'over' : g.days != null ? 'near' : 'on';
    return `<div class="rrow ${g.status === 'closed' ? 'closed' : ''}" tabindex="0" style="cursor:pointer;grid-template-columns:14px 1fr 130px 90px"><span class="led ${c}"></span><div><div class="n">${g.name}</div><div class="f">${g.funder}</div></div>
      <span class="a">${g.max ? '$' + g.max.toLocaleString() : 'varies'}</span><span class="d ${c}">${g.status === 'closed' ? 'closed' : g.days != null ? 'in ' + g.days + 'd' : g.dl.toLowerCase()}</span>
      <div class="x">${g.desc}<br><a class="mbtn sm" href="${g.link}" target="_blank" rel="noopener">Funder's page →</a></div></div>`; }).join('')
    : '<div class="empty">Nothing matches. Widen the window or clear the search.</div>'; }
$('#gres').addEventListener('click', e => { const r = e.target.closest('.rrow'); if (r && !e.target.closest('a')) r.classList.toggle('xo'); });
$('#gres').addEventListener('keydown', e => { if (e.key === 'Enter' && e.target.classList.contains('rrow')) e.target.classList.toggle('xo'); });
render();
</script>"""
    return shell("grants", body, js)
'''

CATEGORY = r'''
def category(slug):
    """Header, three meters, the list, one line of links."""
    cat, title, what = CATEGORY_PAGES[slug]
    intro, gs = category_intro(cat, what)
    gs = sorted(gs, key=lambda g: ({"open": 0, "rolling": 1, "closed": 2}[status(g)], days_left(g) if days_left(g) is not None else 999))
    c = {s: sum(1 for g in gs if status(g) == s) for s in ("open", "rolling", "closed")}
    others = " · ".join(f'<a href="{s}.html" style="color:var(--text)">{CAT_LABEL[v[0]]}</a>' for s, v in CATEGORY_PAGES.items() if s != slug)
    meters = "".join(f'<div class="vline" style="padding:0 26px;display:flex;gap:18px;align-items:flex-end"><span class="meter v" data-n="12" data-lit="{n}" data-near="{n if k == "open" else 0}"></span><div><div class="mono" style="font-size:40px;letter-spacing:-.02em">{n}</div><div class="cap">{lab}</div></div></div>'
        for k, n, lab in [("open", c["open"], "Open now"), ("rolling", c["rolling"], "Rolling"), ("closed", c["closed"], "Closed for now")])
    body = ph("Grant list", title, intro) + panel(f'<div style="display:flex;flex-wrap:wrap;gap:20px 0;margin-left:-26px">{meters}</div>', "pad") + panel('<div class="rows">' + "".join(grow(g) for g in gs) + "</div>", "", attrs='style="margin-top:20px"') + f'<p class="cap" style="margin-top:22px">More lists · {others} · <a href="grants.html" style="color:var(--text)">Search all {len(GRANTS)}</a></p>'
    return shell(slug, body)
'''

HELP_ = r'''
def grant_help():
    """Header, checklist (mistakes folded inside), readiness meter, free-help directory."""
    tips = "".join(f'<button class="chk" data-i="{i}"><span class="no">0{i+1}</span><div><b>{a}</b><p>{b}</p></div><span class="tog"></span></button>' for i, (a, b) in enumerate(HELP["tips"]))
    mistakes = '<details style="padding:18px 0 0;border-top:1px solid var(--row-line)"><summary class="cap" style="cursor:pointer">+ Common mistakes to avoid</summary>' + "".join(f'<div class="mrow" style="justify-content:flex-start;gap:14px;align-items:flex-start;border:0;padding:8px 0"><span class="led over" style="margin-top:6px"></span><span style="font-size:14px;line-height:1.5;color:var(--body)">{m}</span></div>' for m in HELP["mistakes"]) + "</details>"
    orgs = "".join(f'<a class="rrow" href="{u}" target="_blank" rel="noopener" style="grid-template-columns:14px 1fr 170px"><span class="led on"></span><div><div class="n">{n}</div><div class="f" style="font-family:var(--sans);font-size:13px;line-height:1.5">{d}</div></div><span class="cap" style="text-align:right">{l} →</span></a>' for n, d, l, u in HELP["orgs"])
    body = ph("Grants", "Grant Help & Tips", HELP["intro"], '<a class="mbtn" href="grants.html" style="margin-top:20px">Search grants →</a>') + f"""
<div class="grid" style="align-items:start">
  {panel('<div class="cap" style="margin-bottom:6px">How to write a strong application · switch each on as you go</div>' + tips + mistakes, "pad c8")}
  {panel('<div class="cap">Readiness</div><div style="display:flex;gap:22px;align-items:flex-end;margin-top:18px"><span class="meter v" id="hm">' + '<i></i>' * 16 + '</span><div><div class="mono" style="font-size:40px;letter-spacing:-.02em" id="hc">0/8</div><div class="cap" style="margin-top:6px">steps done</div></div></div>', "pad c4")}
</div>
<section><div class="shead"><div><div class="cap">Directory</div><h2>Where to get free help</h2></div></div>{panel('<div class="rows">' + orgs + '</div>')}<p class="dim mono" style="font-size:11px;line-height:1.7;margin-top:16px;max-width:90ch">{HELP['disclaimer']}</p></section>"""
    js = """<script>
const done = new Set(JSON.parse(localStorage.getItem('e3-help') || '[]'));
function upd() { $$('.chk').forEach(c => c.classList.toggle('on', done.has(+c.dataset.i))); $('#hc').textContent = done.size + '/8';
  $$('#hm i').forEach((s, i) => s.className = i < done.size * 2 ? (done.size === 8 ? 'on' : 'near') : ''); localStorage.setItem('e3-help', JSON.stringify([...done])); }
$$('.chk').forEach(c => c.addEventListener('click', () => { const i = +c.dataset.i; done.has(i) ? done.delete(i) : done.add(i); upd(); })); upd();
</script>"""
    return shell("grant-help", body, js)
'''

CONTACT = r'''
def contact():
    """Header, form, one side panel."""
    form = f"""<form onsubmit="event.preventDefault();this.querySelector('[data-sent]').hidden=false" id="cf">
      <div class="grid" style="gap:0 18px"><label class="field c6"><span><span class="led" data-for="n"></span><span class="cap">Name *</span></span><input class="inp" id="n" required autocomplete="name"></label>
      <label class="field c6"><span><span class="led" data-for="e"></span><span class="cap">Email *</span></span><input class="inp" id="e" type="email" required autocomplete="email"></label></div>
      <label class="field"><span><span class="led" data-for="s"></span><span class="cap">Subject *</span></span><input class="inp" id="s" required></label>
      <label class="field"><span><span class="led" data-for="m"></span><span class="cap">Message *</span></span><textarea class="inp" id="m" required></textarea></label>
      <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap"><button class="mbtn" type="submit">Send message</button><span class="cap" data-sent hidden style="color:rgb(var(--led-near))">Mockup: nothing was sent</span></div></form>"""
    body = ph("Contact", "Let's connect", "Have questions about our research or want to collaborate? Send a message and we will respond within two business days.") + f"""
<div class="grid" style="align-items:start">{panel(form, "pad c8")}
  {panel('<div class="mrow cap">Reply within<b>2 business days</b></div><div class="mrow cap">Interviews<b><a href="outreach.html">Outreach →</a></b></div><div class="mrow cap">Your data<b><a href="privacy.html">Privacy →</a></b></div>', "pad c4")}</div>"""
    js = """<script>
function chk() { ['n', 'e', 's', 'm'].forEach(id => { const v = $('#' + id).checkValidity() && $('#' + id).value; $(`[data-for=${id}]`).className = 'led' + (v ? ' on' : ''); }); }
$('#cf').addEventListener('input', chk);
</script>"""
    return shell("contact", body, js)
'''

INDIC = r'''
def indicators():
    """Header with range knob, four key scopes, the other four behind one button."""
    def scope(k, grp, name, u, d, extra):
        return panel(f"""<div style="display:flex;justify-content:space-between;align-items:center"><span class="cap">{grp} · {name}</span><span class="led" data-led></span></div>
      <div class="screen"><svg viewBox="0 0 500 130" preserveAspectRatio="none" aria-hidden="true"></svg></div>
      <div style="display:flex;justify-content:space-between;align-items:baseline;gap:12px"><div class="readout"><span data-v>— —</span><small>{u}</small></div><span class="cap" data-yr></span></div>
      <p style="margin-top:10px">{d}</p>""", f"scope c6{extra}", attrs=f'data-key="{k}" data-unit="{u}"')
    key = [i for i in INDICATORS if i[0] in KEY_INDICATORS]
    more = [i for i in INDICATORS if i[0] not in KEY_INDICATORS]
    body = ph("Data", "Economic Indicators", "Everyday costs, job security and borrowing rates. Turn the knob to change the range; hover a screen to read any year.",
              '<div style="display:flex;align-items:center;gap:24px;margin-top:18px"><div class="knob" id="rng" data-label="Time range"></div><div class="mono" style="font-size:22px" id="rngl">2000 →</div></div>') + f"""
{panel('<span class="led near"></span><span>Preview: placeholder traces. Live FRED data loads from /api/economic-indicators on the deployed site.</span>', "notice", attrs='id="note" hidden')}
<div class="grid">{''.join(scope(*i, '') for i in key)}{''.join(scope(*i, ' more') for i in more)}</div>
<div style="text-align:center;margin-top:24px"><button class="mbtn ghost" onclick="document.querySelectorAll('.scope.more').forEach(e=>e.hidden=false);this.remove()">Show all 8 indicators</button></div>"""
    js = """<script src="../shared/indicators.js"></script><script>
$$('.scope.more').forEach(e => e.hidden = true);
let D, from = 0; const STARTS = [2000, 2008, 2016, 2020];
makeKnob($('#rng'), STARTS.map(String), 0, i => { from = i; draw(); });
function draw() { if (!D) return; const y0 = STARTS[from]; $('#rngl').textContent = y0 + ' →';
  $$('.scope').forEach(t => { const all = D.series[t.dataset.key]; if (!all) return; const i0 = Math.max(0, D.years.indexOf(y0)), s = all.slice(i0), yrs = D.years.slice(i0), n = s.length;
    const lo = Math.min(...s), hi = Math.max(...s), x = i => i / (n - 1) * 500, y = v => 120 - (v - lo) / (hi - lo || 1) * 110, svg = $('svg', t);
    const d = s.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1)).join(' ');
    svg.innerHTML = `<path d="${d}" fill="none" stroke="rgba(214,236,226,.25)" stroke-width="6" vector-effect="non-scaling-stroke" style="filter:blur(3px)"/>
      <path d="${d}" fill="none" stroke="rgb(214,236,226)" stroke-width="1.6" vector-effect="non-scaling-stroke" ${D.live ? '' : 'stroke-dasharray="4 4"'}/>
      <line class="cur" x1="${x(n - 1)}" x2="${x(n - 1)}" y1="0" y2="130" stroke="rgba(255,181,71,.6)" vector-effect="non-scaling-stroke"/>`;
    const u = t.dataset.unit, show = i => { $('[data-v]', t).textContent = D.live ? fmtIndicator(s[i], u).replace(/[%M]/g, '') : '— —'; $('[data-yr]', t).textContent = yrs[i]; $('.cur', svg).setAttribute('x1', x(i)); $('.cur', svg).setAttribute('x2', x(i)); };
    show(n - 1); $('[data-led]', t).className = 'led ' + (D.live ? 'on' : 'near');
    svg.onpointermove = e => { const r = svg.getBoundingClientRect(); show(Math.round((e.clientX - r.left) / r.width * (n - 1))); }; svg.onpointerleave = () => show(n - 1); }); }
loadIndicators().then(d => { D = d; $('#note').hidden = d.live; draw(); });
</script>"""
    return shell("economic-indicators", body, js)
'''


def apply():
    p = "theme_b.py"
    s = open(p).read()
    for name, src in [("home", HOME), ("pub_list", PUBLIST), ("article", ARTICLE), ("about", ABOUT_), ("grants", GRANTS),
                      ("category", CATEGORY), ("grant_help", HELP_), ("contact", CONTACT), ("indicators", INDIC)]:
        s = replace_func(s, name, src)
    s = s.replace('"articles": pub_list("articles", "Articles", "Perspectives and community insights from our team and partners, from grassroots organizing to systemic policy analysis.", ARTICLES)',
                  '"articles": pub_list("articles", "Publications", "Articles and research papers from our team and partners, from grassroots history to systemic policy analysis.", PUBS)')
    s = s.replace(".board{display:grid;grid-template-columns:repeat(6,1fr) 200px;margin-top:8px}",
                  ".board{display:grid;grid-template-columns:repeat(6,1fr) 200px;margin-top:8px}\n.board.mini3{grid-template-columns:repeat(3,1fr) 240px;margin-top:20px}\n.board.mini3 .strip{height:480px}\nsummary{list-style:none}summary::-webkit-details-marker{display:none}\n[hidden]{display:none!important}")
    s = s.replace("  .board{grid-template-columns:repeat(2,1fr)}", "  .board,.board.mini3{grid-template-columns:repeat(2,1fr)}")
    s = s.replace("  .board{grid-template-columns:repeat(3,1fr)}.master{grid-column:1/-1}", "  .board,.board.mini3{grid-template-columns:repeat(3,1fr)}.master{grid-column:1/-1}")
    open(p, "w").write(s)


if __name__ == "__main__":
    apply()
