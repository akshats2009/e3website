"""Minimal pass for theme C: about seven blocks per page."""
from common import replace_func

HOME_SECTIONS_OLD_START = '<section><div class="sh"><h2>Three lenses</h2>'

GRANTS = r'''
def grants():
    """Header, the big search, two filter rows (more folded), count + table."""
    cats = "".join(f'<button data-v="{k}">{v}</button>' for k, v in CAT_LABEL.items())
    lists = " · ".join(f'<a href="{s}.html" style="text-decoration:underline dashed var(--guide);text-underline-offset:4px;color:var(--ink)">{CAT_LABEL[c]}</a>' for s, (c, _, _) in CATEGORY_PAGES.items())
    body = ph("Grants", "Grant Finder", f"Set by urgency: the closer a deadline, the heavier it is. Closed grants drop to Thin. Ready-made lists: {lists}.", '<a class="pill o" href="grant-help.html">Help & tips →</a>') + f"""
<div style="margin-top:40px"><label class="lab" for="q">Search</label><input class="bigsearch" id="q" type="search" placeholder="women-owned bakery…" autocomplete="off"></div>
<div style="margin-top:20px">
  <div class="fgroup"><span class="lab">Who qualifies</span><div class="ftabs" data-f="elig"><button class="on" data-v="">Anyone</button><button data-v="small_business">Small business</button><button data-v="nonprofit">Nonprofit</button></div></div>
  <div class="fgroup"><span class="lab">Status</span><div class="ftabs" data-f="status"><button class="on" data-v="live">Open + rolling</button><button data-v="">Everything</button></div></div>
  <details class="fgroup" style="display:block"><summary class="lab" style="cursor:pointer">+ More filters</summary>
    <div class="fgroup" style="margin-top:12px"><span class="lab">Award up to</span><div class="ftabs" data-f="amt"><button class="on" data-v="0">Any</button><button data-v="10000">$10k+</button><button data-v="50000">$50k+</button><button data-v="250000">$250k+</button></div></div>
    <div class="fgroup"><span class="lab">Category</span><div class="ftabs" data-f="cat" data-multi><button class="on" data-v="">All</button>{cats}</div></div></details>
</div>
<div style="display:flex;align-items:baseline;margin-top:40px;gap:14px"><span class="big-num" id="cnt" style="font-variation-settings:'wght' 200">0</span><span class="lab">of {len(GRANTS)} grants</span></div>
<table class="gt"><thead><tr><th>Grant</th><th>Max award</th><th style="text-align:right">Deadline</th></tr></thead><tbody id="gt" aria-live="polite"></tbody></table>"""
    js = """<script src="../shared/grants-data.js"></script><script>
const F = { q: '', elig: '', status: 'live', amt: 0, cat: new Set() };
$$('.ftabs[data-f]').forEach(t => t.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
  if (t.hasAttribute('data-multi')) { if (!b.dataset.v) { F.cat.clear(); $$('button', t).forEach(x => x.classList.toggle('on', !x.dataset.v)); } else { F.cat.has(b.dataset.v) ? F.cat.delete(b.dataset.v) : F.cat.add(b.dataset.v); b.classList.toggle('on'); $('button[data-v=""]', t).classList.toggle('on', !F.cat.size); } }
  else { $$('button', t).forEach(x => x.classList.toggle('on', x === b)); F[t.dataset.f] = t.dataset.f === 'amt' ? +b.dataset.v : b.dataset.v; } render(); }));
$('#q').addEventListener('input', e => { F.q = e.target.value.toLowerCase(); $('#q').style.fontVariationSettings = `'wght' ${200 + Math.min(500, e.target.value.length * 30)}`; render(); });
function render() {
  const rs = GRANTS.filter(g => (!F.q || (g.name + g.funder + g.desc + CAT_LABEL[g.cat]).toLowerCase().includes(F.q)) && (!F.elig || g.elig === F.elig || g.elig === 'both')
    && (F.status === '' || g.status !== 'closed') && (!F.amt || g.max >= F.amt) && (!F.cat.size || F.cat.has(g.cat)))
    .sort((a, b) => ({ open: 0, rolling: 1, closed: 2 }[a.status] - { open: 0, rolling: 1, closed: 2 }[b.status]) || (a.days ?? 999) - (b.days ?? 999));
  $('#cnt').textContent = rs.length; $('#cnt').style.fontVariationSettings = `'wght' ${Math.round(100 + rs.length / GRANTS.length * 800)}`;
  $('#gt').innerHTML = rs.length ? rs.map((g, i) => { const w = g.status === 'closed' ? 100 : urg(g.days), hot = g.days != null && g.days <= 14 && g.status !== 'closed';
    return `<tr class="${hot ? 'hot' : ''} ${g.status === 'closed' ? 'closed' : ''}" data-i="${i}" tabindex="0"><td><div class="n">${g.name}</div><div class="f">${g.funder}</div></td>
      <td class="a">${g.max ? '$' + g.max.toLocaleString() : 'Varies'}</td><td class="d" style="font-variation-settings:'wght' ${w}">${g.dl}<small>${g.status === 'closed' ? 'closed' : g.days != null ? 'in ' + g.days + ' days' : g.status}</small></td></tr>
      <tr class="xr" hidden><td colspan="3">${g.desc} <a class="pill sm o" href="${g.link}" target="_blank" rel="noopener" style="margin-left:8px">Funder's page →</a></td></tr>`; }).join('')
    : '<tr><td colspan="3" class="lab" style="padding:40px 0">No grants match these filters. Try widening them.</td></tr>'; }
$('#gt').addEventListener('click', e => { const r = e.target.closest('tr[data-i]'); if (r && !e.target.closest('a')) r.nextElementSibling.hidden = !r.nextElementSibling.hidden; });
$('#gt').addEventListener('keydown', e => { if (e.key === 'Enter' && e.target.matches('tr[data-i]')) e.target.nextElementSibling.hidden = !e.target.nextElementSibling.hidden; });
render();
</script>"""
    return shell("grants", body, js)
'''

PUBLIST = r'''
def pub_list(page, title, lede, items, extra=""):
    """Header, index rows, one line of related links."""
    links = '<p class="lab" style="margin-top:24px">Also: <a href="journals.html" style="color:var(--ink)">Journals</a> · <a href="economic-indicators.html" style="color:var(--ink)">Economic indicators</a></p>'
    return shell(page, ph("Publications", title, lede) + "".join(pub_row(i, p, False) for i, p in enumerate(items)) + links)
'''

CATEGORY = r'''
def category(slug):
    """Header, three numerals, the table, one line of links."""
    cat, title, what = CATEGORY_PAGES[slug]
    intro, gs = category_intro(cat, what)
    gs = sorted(gs, key=lambda g: ({"open": 0, "rolling": 1, "closed": 2}[status(g)], days_left(g) if days_left(g) is not None else 999))
    c = {s: sum(1 for g in gs if status(g) == s) for s in ("open", "rolling", "closed")}
    nums = "".join(f'<div class="c4"><div class="big-num" style="font-variation-settings:{chr(39)}wght{chr(39)} {w};font-size:110px">{n}</div><div class="lab" style="margin-top:12px">{lab}</div></div>' for n, lab, w in [(c["open"], "open now", 800), (c["rolling"], "rolling", 450), (c["closed"], "closed for now", 100)])
    others = " · ".join(f'<a href="{s}.html" style="color:var(--ink)">{CAT_LABEL[v[0]]}</a>' for s, v in CATEGORY_PAGES.items() if s != slug)
    body = ph("Grant list", title, intro) + f"""
<div class="grid" style="margin-top:50px">{nums}</div>
<table class="gt" style="margin-top:50px"><thead><tr><th>Grant</th><th>Award</th><th style="text-align:right">Deadline</th></tr></thead><tbody>{''.join(grant_tr(g) for g in gs)}</tbody></table>
<p class="lab" style="margin-top:24px">More lists: {others} · <a href="grants.html" style="color:var(--ink)">Search all {len(GRANTS)}</a></p>"""
    return shell(slug, body)
'''

HELP_ = r'''
def grant_help():
    """Header, checklist (mistakes folded in), free-help index, one-line disclaimer."""
    tips = "".join(f'<button class="tip-row" data-i="{i}"><span class="no">0{i+1}</span><div><b>{a}</b><p>{b}</p></div><span class="bx">✓</span></button>' for i, (a, b) in enumerate(HELP["tips"]))
    orgs = "".join(f'<a class="pub" href="{u}" target="_blank" rel="noopener" style="padding:24px 0"><div class="no" style="font-size:44px">{chr(65+i)}</div><div><h3 style="font-size:24px">{n}</h3><p>{d}</p></div><div class="meta"><b>{l} →</b></div></a>' for i, (n, d, l, u) in enumerate(HELP["orgs"]))
    body = ph("Grants", "Grant Help & Tips", HELP["intro"], '<a class="pill" href="grants.html">Search grants →</a>') + f"""
<section style="margin-top:60px"><div class="sh"><h2>How to write a strong application</h2><span class="lab">Ready: <span id="rd" style="font-size:22px;color:var(--ink);font-family:var(--sans);font-variation-settings:'wght' 100">0 of 8</span></span></div>
<p class="lab" style="margin:14px 0 0">Tick a step when it's done: it gains weight.</p>{tips}
<details style="padding:20px 0;border-bottom:1px solid var(--rule)"><summary class="lab" style="cursor:pointer">+ Common mistakes to avoid</summary>{''.join(f'<p style="padding:10px 0;font-size:16px;line-height:1.5"><span class="g lab" style="margin-right:12px">✕</span>{m}</p>' for m in HELP['mistakes'])}</details></section>
<section><div class="sh"><h2>Where to get free help</h2></div>{orgs}<p class="lab" style="margin-top:20px;line-height:1.7;max-width:90ch">{HELP['disclaimer']}</p></section>"""
    js = """<script>
const done = new Set(JSON.parse(localStorage.getItem('e3-help') || '[]'));
function upd() { $$('.tip-row[data-i]').forEach(c => c.classList.toggle('on', done.has(+c.dataset.i))); $('#rd').textContent = done.size + ' of 8';
  $('#rd').style.fontVariationSettings = `'wght' ${100 + done.size * 100}`; localStorage.setItem('e3-help', JSON.stringify([...done])); }
$$('.tip-row[data-i]').forEach(c => c.addEventListener('click', () => { const i = +c.dataset.i; done.has(i) ? done.delete(i) : done.add(i); upd(); })); upd();
</script>"""
    return shell("grant-help", body, js)
'''

ABOUT_ = r'''
def about():
    """Header, one statement, team, approach."""
    team = "".join(f'<div class="pub"><div class="no">0{i+1}</div><div><h3 data-lens="300" style="font-size:40px">{n}</h3><p style="font-size:15px">{b}</p></div><div class="meta"><b>{r}</b></div></div>' for i, (n, r, b) in enumerate(ABOUT["team"]))
    appr = "".join(f'<div class="ln"><span class="lab">0{i+1}</span><h3 class="w{w}" style="font-size:30px;margin:12px 0 8px">{t}</h3><p>{d}</p></div>' for i, ((t, d), w) in enumerate(zip(ABOUT["approach"], [3, 5, 7])))
    body = ph("About", "About e3 Initiative", ABOUT["what"]) + f"""
<p style="font-size:30px;line-height:1.25;letter-spacing:-.025em;font-variation-settings:'wght' 260;max-width:40ch;margin-top:50px">{ABOUT['who']}</p>
<section><div class="sh"><h2>Our team</h2></div>{team}</section>
<section><div class="sh"><h2>Our approach</h2></div><div class="lenses">{appr}</div></section>"""
    return shell("about", body)
'''

INDIC = r'''
def indicators():
    """Header, four key charts, the rest behind one button."""
    def row(k, grp, name, u, d, extra):
        return f"""<div class="ind c6{extra}" data-key="{k}" data-unit="{u}"><div class="row1"><span class="lab">{grp} · {name}</span><span class="lab" data-yr></span></div>
      <div class="val" style="margin-top:16px;font-variation-settings:'wght' 200"><span data-v>—</span><small>{u}</small></div>
      <svg viewBox="0 0 500 110" preserveAspectRatio="none" aria-hidden="true"></svg><p>{d}</p></div>"""
    key = [i for i in INDICATORS if i[0] in KEY_INDICATORS]
    more = [i for i in INDICATORS if i[0] not in KEY_INDICATORS]
    body = ph("Data", "Economic Indicators", "Everyday costs, job security and borrowing rates since 2000. Each value's weight shows where it sits in its own history: a record high is Black, a record low is Thin.") + f"""
<div class="notice" id="note" hidden>Preview: placeholder shapes. Live FRED data loads from /api/economic-indicators on the deployed site.</div>
<div class="grid" style="gap:0 48px">{''.join(row(*i, '') for i in key)}{''.join(row(*i, ' more') for i in more)}</div>
<div style="margin-top:28px"><button class="pill o" onclick="document.querySelectorAll('.ind.more').forEach(e=>e.hidden=false);this.remove()">Show all 8 indicators</button></div>"""
    js = """<script src="../shared/indicators.js"></script><script>
$$('.ind.more').forEach(e => e.hidden = true);
loadIndicators().then(D => { $('#note').hidden = D.live;
  $$('.ind').forEach(t => { const s = D.series[t.dataset.key]; if (!s) return; const n = s.length, lo = Math.min(...s), hi = Math.max(...s), x = i => i / (n - 1) * 500, y = v => 100 - (v - lo) / (hi - lo || 1) * 90, u = t.dataset.unit, svg = $('svg', t);
    const d = s.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1)).join(' ');
    svg.innerHTML = `<line x1="0" x2="500" y1="${y(hi)}" y2="${y(hi)}" stroke="var(--guide)" stroke-dasharray="3 5" opacity=".6" vector-effect="non-scaling-stroke"/><line x1="0" x2="500" y1="${y(lo)}" y2="${y(lo)}" stroke="var(--guide)" stroke-dasharray="3 5" opacity=".6" vector-effect="non-scaling-stroke"/>
      <path d="${d}" fill="none" stroke="var(--ink)" stroke-width="1.6" vector-effect="non-scaling-stroke" ${D.live ? '' : 'stroke-dasharray="2 4"'}/><line class="cur" y1="0" y2="110" stroke="var(--guide)" stroke-width="1.5" vector-effect="non-scaling-stroke"/>`;
    const show = i => { const k = (s[i] - lo) / (hi - lo || 1), w = Math.round(100 + k * 800); $('.val', t).style.fontVariationSettings = `'wght' ${w}`;
      $('[data-v]', t).textContent = D.live ? fmtIndicator(s[i], u).replace(/[%M]/g, '') : '—'; $('[data-yr]', t).textContent = D.years[i]; $('.cur', svg).setAttribute('x1', x(i)); $('.cur', svg).setAttribute('x2', x(i)); };
    show(n - 1); svg.onpointermove = e => { const r = svg.getBoundingClientRect(); show(Math.round((e.clientX - r.left) / r.width * (n - 1))); }; svg.onpointerleave = () => show(n - 1); }); });
</script>"""
    return shell("economic-indicators", body, js)
'''


def apply():
    p = "theme_c.py"
    s = open(p).read()
    for name, src in [("grants", GRANTS), ("pub_list", PUBLIST), ("category", CATEGORY), ("grant_help", HELP_), ("about", ABOUT_), ("indicators", INDIC)]:
        s = replace_func(s, name, src)
    # Home: drop the three-lenses block and the mission; index without the photo; grants table to four rows
    a = s.index(HOME_SECTIONS_OLD_START)
    b = s.index('</p></section>"""', a) + len('</p></section>')
    s = s[:a] + s[b:]
    s = s.replace("{''.join(pub_row(i, p, i == 0) for i, p in enumerate(PUBS))}", "{''.join(pub_row(i, p, False) for i, p in enumerate(PUBS))}")
    s = s.replace("soon = sorted(OPEN, key=lambda g: days_left(g) if days_left(g) is not None else 999)[:7]", "soon = sorted(OPEN, key=lambda g: days_left(g) if days_left(g) is not None else 999)[:4]")
    s = s.replace('<section><div class="sh"><h2>Grants, weighted by urgency</h2><a href="grants.html">Search all {len(GRANTS)} →</a></div>{LEGEND}',
                  '<section><div class="sh"><h2>Closing soon</h2><a href="grants.html">All {len(OPEN)} open grants →</a></div>')
    s = s.replace('<div><p>{LEDE}</p><div class="btns"><a class="pill" href="research.html">Read the research</a><a class="pill o" href="grants.html">Find a grant</a></div></div>',
                  '<div><p>{LEDE}</p><div class="btns"><a class="pill" href="articles.html">Read the research</a></div></div>')
    # Article: no weight slider in the margin
    s = s.replace('<aside class="margin"><div class="lab">Text weight</div><div class="slider mini" id="bw" data-label="Body"></div></aside>', '<aside></aside>')
    s = s.replace("makeSlider($('#bw'), 380, w => pr.style.setProperty('--bw', w.toFixed(0)));\n", "")
    s = s.replace('"articles": pub_list("articles", "Articles", "Perspectives and community insights from our team and partners, from grassroots organizing to systemic policy analysis.", ARTICLES)',
                  '"articles": pub_list("articles", "Publications", "Articles and research papers from our team and partners, from grassroots history to systemic policy analysis.", PUBS)')
    s = s.replace(".rule{border-top:1px solid var(--rule)}", ".rule{border-top:1px solid var(--rule)}\nsummary{list-style:none}summary::-webkit-details-marker{display:none}\n[hidden]{display:none!important}")
    open(p, "w").write(s)


if __name__ == "__main__":
    apply()
