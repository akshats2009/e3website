"""Page-by-page minimal pass: every inner page is a header, one block of content, and the footer.
Applies to theme_a.py, theme_b.py, theme_c.py by replacing functions."""
import re
from common import replace_func

# ───────────────────────── A: Paper widgets ─────────────────────────
A = {}
A["about"] = r'''
def about():
    """Header, one statement, three people."""
    team = "".join(crow(f"0{i+1}", n, f"{r}. {b}", "") for i, (n, r, b) in enumerate(ABOUT["team"]))
    body = ph("About", "About e3 Initiative") + f"""
<div class="tile pad rise"><p style="font-weight:300;font-size:28px;line-height:1.25;letter-spacing:-.7px;max-width:44ch">{ABOUT['who']}</p><p class="muted" style="font-size:15px;line-height:1.6;margin-top:18px;max-width:70ch">{ABOUT['what']}</p></div>
<section style="margin-top:20px"><div class="tile rows rise">{team}</div>
<p class="muted" style="font-size:14px;margin-top:20px;max-width:70ch">We believe in community voices, cross-sector collaboration, and turning findings into stories of economic resilience.</p></section>"""
    return shell("about", body)
'''
A["pub_list"] = r'''
def pub_list(page, kicker, title, lede, items, extra=""):
    """Header and one list."""
    rows = "".join(crow(p['short'][:6], esc(p['title']), f"{p['kind']} · {p['min']} min · {p['author']}", p['slug'] + '.html') for p in items)
    return shell(page, ph(kicker, title, lede) + f'<div class="tile rows rise">{rows}</div>')
'''
A["article"] = r'''
def article(p):
    """Title, banner, text. A thin bar at the top shows reading progress."""
    a = p["data"]
    body = []
    for i, (t, txt) in enumerate(a["blocks"]):
        if t == "h2":
            body.append(f'<h2 id="s{i}">{txt}</h2>')
        elif t == "li":
            body.append(f"<ul><li>{txt}</li></ul>")
        else:
            body.append(f"<{t}>{txt}</{t}>")
    cite = {"article-railroad": "articles/chinese-labor-transcontinental-railroad-citations.html", "article-chinatown": "articles/chinatown-citations.html", "research-chinatown": "research/chinatown-solidarity-paper-citations.html"}[p["slug"]]
    body.append(f'<p class="muted" style="font-size:14px;margin-top:2em"><a href="../../{cite}">Citations and sources →</a></p>')
    body_html = f"""
<style>.topbar{{position:fixed;left:0;right:0;top:0;height:3px;background:transparent;z-index:40}}.topbar b{{display:block;height:100%;width:0;background:var(--accent)}}</style>
<div class="topbar"><b id="rb"></b></div>
<article class="tile atile rise" style="max-width:820px;margin:0 auto">
  {label(f"{p['kind']} · {p['date']} · {p['min']} min")}
  <h1>{esc(p['title'])}</h1>
  <div class="mono muted" style="font-size:12px">{esc(a['byline'] or 'By ' + p['author'])}</div>
  <div class="banner"><img src="{IMG}{p["img"].replace("-640", "")}" alt="{esc(p["alt"])}"></div><div class="capt">{esc(a["caption"] or p["alt"])}</div>
  <div class="prose" id="prose">{''.join(body)}</div>
</article>"""
    js = """<script>
const pr = $('#prose');
function upd() { const r = pr.getBoundingClientRect(), k = Math.max(0, Math.min(1, (innerHeight * .4 - r.top) / r.height)); $('#rb').style.width = k * 100 + '%'; }
addEventListener('scroll', upd, { passive: true }); upd();
</script>"""
    return shell(p["slug"], body_html, js)
'''
A["grants"] = r'''
def grants():
    """Header, one search row, results. Other filters are folded away."""
    cats = "".join(f'<button data-v="{k}">{v}</button>' for k, v in CAT_LABEL.items())
    lists = " · ".join(f'<a href="{s}.html" style="color:var(--ink)">{CAT_LABEL[c]}</a>' for s, (c, _, _) in CATEGORY_PAGES.items())
    body = ph("Grants", "Grant Finder", f"Funding for small businesses and nonprofits. Ready-made lists: {lists}.", '<a class="btn ghost" href="grant-help.html">Help & tips →</a>') + f"""
<div class="tile pad rise" style="margin-bottom:20px">
  <div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap">
    <div class="search" style="flex:1;min-width:240px">{icon('search')}<input class="inp" id="q" type="search" placeholder="Women-owned bakery…" aria-label="Search grants"></div>
    <div class="seg" data-f="status"><button class="on" data-v="live">Open + rolling</button><button data-v="">All</button></div>
    <span class="thin" style="font-size:40px" id="gcount">0</span>
  </div>
  <details style="margin-top:16px"><summary class="label" style="cursor:pointer">More filters</summary>
    <div class="fl">{label('Who qualifies')}<div class="seg" data-f="elig"><button class="on" data-v="">Anyone</button><button data-v="small_business">Business</button><button data-v="nonprofit">Nonprofit</button></div></div>
    <div class="fl">{label('Award up to at least')}<div class="seg" data-f="amt"><button class="on" data-v="0">Any</button><button data-v="10000">$10k</button><button data-v="50000">$50k</button><button data-v="250000">$250k</button></div></div>
    <div class="fl">{label('Category')}<div class="seg" data-f="cat" data-multi><button class="on" data-v="">All</button>{cats}</div></div></details>
</div>
<div class="tile gres rise" id="gres" aria-live="polite"></div>"""
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
A["grant_help"] = r'''
def grant_help():
    """Header, one checklist. The directory is folded away."""
    tips = "".join(f'<button class="check" data-i="{i}"><span class="bx">{icon("check", 14)}</span><div><b>{a}</b><p>{b}</p></div></button>' for i, (a, b) in enumerate(HELP["tips"]))
    orgs = "".join(crow("→", n, d, u, f'<span class="chip">{l}</span>') for n, d, l, u in HELP["orgs"])
    body = ph("Grants", "Grant Help & Tips", HELP["intro"], '<a class="btn" href="grants.html">Search grants →</a>') + f"""
<div class="tile rows rise" style="padding-top:18px">{label('How to write a strong application · <span id="hcount">0/8</span>')}<div style="margin-top:6px">{tips}</div>
  <details style="padding:16px 0;border-top:1px solid var(--line)"><summary class="label" style="cursor:pointer">Common mistakes to avoid</summary><ul style="margin:12px 0 0 18px;color:var(--muted);font-size:14px;line-height:1.7">{''.join(f'<li>{m}</li>' for m in HELP['mistakes'])}</ul></details>
  <details style="padding:16px 0;border-top:1px solid var(--line)"><summary class="label" style="cursor:pointer">Where to get free help</summary><div style="margin-top:8px">{orgs}</div><p class="muted" style="font-size:12px;line-height:1.6;margin-top:14px;max-width:80ch">{HELP['disclaimer']}</p></details></div>"""
    js = """<script>
const done = new Set(JSON.parse(localStorage.getItem('e3-help') || '[]'));
function upd() { $$('.check[data-i]').forEach(c => c.classList.toggle('done', done.has(+c.dataset.i))); $('#hcount').textContent = done.size + '/8'; localStorage.setItem('e3-help', JSON.stringify([...done])); }
$$('.check[data-i]').forEach(c => c.addEventListener('click', () => { const i = +c.dataset.i; done.has(i) ? done.delete(i) : done.add(i); upd(); })); upd();
</script>"""
    return shell("grant-help", body, js)
'''
A["category"] = r'''
def category(slug):
    """Header and one list."""
    cat, title, what = CATEGORY_PAGES[slug]
    intro, gs = category_intro(cat, what)
    gs = sorted(gs, key=lambda g: ({"open": 0, "rolling": 1, "closed": 2}[status(g)], days_left(g) if days_left(g) is not None else 999))
    rows = "".join(crow(deadline_label(g), esc(g["name"]), esc(g["funder"]) + " · " + esc(g["amount"]), g["link"], status_chip(status(g), days_left(g)), status(g) == "open") for g in gs)
    others = " · ".join(f'<a href="{s}.html" style="color:var(--ink)">{CAT_LABEL[v[0]]}</a>' for s, v in CATEGORY_PAGES.items() if s != slug)
    body = ph("Grant list", title, intro) + f'<div class="tile rows rise">{rows}</div><p class="muted" style="margin-top:22px;font-size:14px">More lists: {others} · <a href="grants.html" style="color:var(--ink)">Search all {len(GRANTS)}</a></p>'
    return shell(slug, body)
'''
A["contact"] = r'''
def contact():
    """Header and the form."""
    body = ph("Contact", "Let's connect", "Have questions about our research or want to collaborate? Send a message and we will respond within two business days. We use your details only to reply.") + """
<form class="tile pad rise" onsubmit="event.preventDefault();this.querySelector('[data-sent]').hidden=false" style="padding:30px;max-width:760px">
  <div class="grid" style="gap:0 16px"><label class="field c6"><span><i></i>Name *</span><input class="inp" required autocomplete="name"></label>
  <label class="field c6"><span><i></i>Email *</span><input class="inp" type="email" required autocomplete="email"></label></div>
  <label class="field"><span><i></i>Subject *</span><input class="inp" required></label>
  <label class="field"><span><i></i>Message *</span><textarea class="inp" required></textarea></label>
  <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap"><button class="btn" type="submit">Send message →</button><span class="chip a" data-sent hidden>Mockup: nothing was sent</span></div>
</form>"""
    return shell("contact", body)
'''
A["privacy"] = r'''
def privacy():
    """Header and the policy."""
    out, ul = [], False
    for i, (t, txt) in enumerate(PRIVACY):
        if t == "li":
            if not ul:
                out.append("<ul>"); ul = True
            out.append(f"<li>{txt}</li>"); continue
        if ul:
            out.append("</ul>"); ul = False
        out.append(f"<{t}>{txt}</{t}>")
    if ul:
        out.append("</ul>")
    body = ph("Legal", "Privacy Policy", "The e3 Initiative is a small research organization. This page explains what information this website collects, why, and the choices you have.", '<span class="chip">Updated Nov 12, 2026</span>') + f'<article class="tile atile rise" style="max-width:820px"><div class="prose">{"".join(out)}</div></article>'
    return shell("privacy", body)
'''
A["notfound"] = r'''
def notfound():
    body = f"""<div class="tile rise" style="padding:26px 34px 36px;max-width:760px;margin-top:20px">{label('Page not found')}
    <div class="thin" style="font-size:200px;letter-spacing:-12px;margin:30px 0 10px">404</div>
    <p class="muted" style="max-width:40ch;margin-bottom:24px">Sorry, we couldn't find that page. It may have moved, or the link may be mistyped.</p>
    <div class="cta"><a class="btn" href="index.html">Go home</a><a class="btn ghost" href="articles.html">Publications</a></div></div>"""
    return shell("404", body)
'''
A["journals"] = r'''
def journals():
    t, logo = JOURNAL
    body = ph("Publications", "Journals", "Browse our academic journals and long-form publications.") + f"""
<div class="tile pad rise" style="display:flex;gap:30px;align-items:center;flex-wrap:wrap"><img src="{IMG}{logo}" alt="{esc(t)}" width="160" height="160" style="border-radius:20px">
<div>{label('Journal')}<div style="font-weight:300;font-size:36px;letter-spacing:-1px;line-height:1.1;margin-top:14px;max-width:18ch">{t}</div><p class="muted" style="margin-top:10px;font-size:14px">Entries coming soon.</p></div></div>"""
    return shell("journals", body)
'''
A["outreach"] = r'''
def outreach():
    cards = "".join(f"""<div class="tile pad rise c6" id="{k}" style="min-height:360px;display:flex;flex-direction:column;justify-content:space-between">
          <div>{label(t)}<p style="font-weight:300;font-size:26px;line-height:1.25;letter-spacing:-.6px;margin-top:22px">{p1}</p><p class="muted" style="margin-top:16px;font-size:14px;line-height:1.55">{p2}</p></div>
          <a class="btn" href="contact.html" style="align-self:flex-start;margin-top:24px">{'Share your story' if k == 'interview' else 'Partner with us'} →</a></div>"""
        for k, (t, s, p1, p2) in OUTREACH.items())
    return shell("outreach", ph("Outreach", "Outreach", "Interviews and partnerships: how community knowledge gets into our research.") + f'<div class="grid">{cards}</div>')
'''

# ───────────────────────── B: Graphite desk ─────────────────────────
B = {}
B["about"] = r'''
def about():
    """Header, one statement, three people."""
    team = panel('<div class="rows">' + "".join(f'<div class="mrow" style="display:block;border:0;border-top:1px solid var(--row-line);padding:22px 0"><div style="display:flex;gap:18px;align-items:baseline;flex-wrap:wrap"><span class="cap">0{i+1}</span><b style="font:20px var(--sans);letter-spacing:-.01em">{n}</b><span class="cap" style="margin-left:auto">{r}</span></div><p class="dim" style="font-size:14px;line-height:1.6;margin:8px 0 0 40px;max-width:70ch">{b}</p></div>' for i, (n, r, b) in enumerate(ABOUT["team"])) + "</div>", "", attrs='style="margin-top:20px"')
    body = ph("About", "About e3 Initiative", ABOUT["what"]) + panel(f'<p style="font-weight:300;font-size:26px;line-height:1.35;letter-spacing:-.02em;max-width:48ch">{ABOUT["who"]}</p>', "pad") + team + '<p class="cap" style="margin-top:22px;line-height:1.8;max-width:80ch">We believe in community voices, cross-sector collaboration, and turning findings into stories of economic resilience.</p>'
    return shell("about", body)
'''
B["pub_list"] = r'''
def pub_list(page, title, lede, items, extra=""):
    """Header and one index panel."""
    return shell(page, ph("Publications", title, lede) + panel('<div class="rows">' + "".join(prow(p) for p in items) + "</div>"))
'''
B["article"] = r'''
def article(p):
    """Title, banner, text. A thin bar at the top shows reading progress."""
    a = p["data"]
    body = []
    for i, (t, txt) in enumerate(a["blocks"]):
        if t == "h2":
            body.append(f'<h2 id="s{i}">{txt}</h2>')
        elif t == "li":
            body.append(f"<ul><li>{txt}</li></ul>")
        else:
            body.append(f"<{t}>{txt}</{t}>")
    cite = {"article-railroad": "articles/chinese-labor-transcontinental-railroad-citations.html", "article-chinatown": "articles/chinatown-citations.html", "research-chinatown": "research/chinatown-solidarity-paper-citations.html"}[p["slug"]]
    body.append(f'<p><a href="../../{cite}">Citations and sources →</a></p>')
    inner = f"""<div class="cap">{p["kind"]} · {p["date"]} · {p["min"]} min</div><h1>{esc(p["title"])}</h1><div class="cap" style="letter-spacing:.1em">{esc(a["byline"] or "By " + p["author"])}</div>
    <div class="banner"><img src="{IMG}{p["img"].replace("-640", "")}" alt="{esc(p["alt"])}"></div><div class="capt">{esc(a["caption"] or p["alt"])}</div>
    <div class="prose" id="prose">{"".join(body)}</div>"""
    body_html = f"""<style>.topbar{{position:fixed;left:0;right:0;top:0;height:3px;z-index:70}}.topbar b{{display:block;height:100%;width:0;background:rgb(var(--led-fine));box-shadow:0 0 8px rgb(var(--led-fine)/.6)}}</style>
<div class="topbar"><b id="rb"></b></div>
<div style="margin-top:40px;max-width:860px;margin-left:auto;margin-right:auto">{panel(inner, "atile", "article")}</div>"""
    js = """<script>
const pr = $('#prose');
function upd() { const r = pr.getBoundingClientRect(), k = Math.max(0, Math.min(1, (innerHeight * .4 - r.top) / r.height)); $('#rb').style.width = k * 100 + '%'; }
addEventListener('scroll', upd, { passive: true }); upd();
</script>"""
    return shell(p["slug"], body_html, js)
'''
B["grants"] = r'''
def grants():
    """Header, one desk (search, status, knob; the rest folded), results."""
    cats = "".join(f'<button class="key" data-v="{k}">{v}</button>' for k, v in CAT_LABEL.items())
    lists = " · ".join(f'<a href="{s}.html" style="color:var(--text)">{CAT_LABEL[c]}</a>' for s, (c, _, _) in CATEGORY_PAGES.items())
    body = ph("Grants", "Grant Finder", f"Funding for small businesses and nonprofits. Ready-made lists: {lists}.", '<a class="mbtn ghost" href="grant-help.html" style="margin-top:20px">Help & tips →</a>') + panel(f"""
  <div style="display:grid;grid-template-columns:1fr 190px;gap:34px" class="gdesk">
    <div>
      <label class="field"><span class="cap">Search</span><input class="inp" id="q" type="search" placeholder="WOMEN-OWNED BAKERY…" aria-label="Search grants"></label>
      <div class="keys" data-group="status"><button class="key on" data-v="live">Open + rolling</button><button class="key" data-v="">Include closed</button></div>
      <details style="margin-top:18px"><summary class="cap" style="cursor:pointer">+ More filters</summary>
        <div class="cap" style="margin:14px 0 10px">Who qualifies</div><div class="keys" data-group="elig"><button class="key on" data-v="">Anyone</button><button class="key" data-v="small_business">Business</button><button class="key" data-v="nonprofit">Nonprofit</button></div>
        <div class="cap" style="margin:14px 0 10px">Category</div><div class="keys" data-group="cat" data-multi>{cats}</div></details>
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
B["grant_help"] = r'''
def grant_help():
    """Header, one checklist. Mistakes and the directory are folded away."""
    tips = "".join(f'<button class="chk" data-i="{i}"><span class="no">0{i+1}</span><div><b>{a}</b><p>{b}</p></div><span class="tog"></span></button>' for i, (a, b) in enumerate(HELP["tips"]))
    mistakes = '<details style="padding:18px 0 0;border-top:1px solid var(--row-line)"><summary class="cap" style="cursor:pointer">+ Common mistakes to avoid</summary>' + "".join(f'<div class="mrow" style="justify-content:flex-start;gap:14px;align-items:flex-start;border:0;padding:8px 0"><span class="led over" style="margin-top:6px"></span><span style="font-size:14px;line-height:1.5;color:var(--body)">{m}</span></div>' for m in HELP["mistakes"]) + "</details>"
    orgs = "".join(f'<a class="rrow" href="{u}" target="_blank" rel="noopener" style="grid-template-columns:14px 1fr 170px"><span class="led on"></span><div><div class="n">{n}</div><div class="f" style="font-family:var(--sans);font-size:13px;line-height:1.5">{d}</div></div><span class="cap" style="text-align:right">{l} →</span></a>' for n, d, l, u in HELP["orgs"])
    directory = f'<details style="padding:18px 0 0;border-top:1px solid var(--row-line);margin-top:14px"><summary class="cap" style="cursor:pointer">+ Where to get free help</summary><div style="margin-top:8px">{orgs}</div><p class="dim mono" style="font-size:11px;line-height:1.7;margin-top:14px;max-width:90ch">{HELP["disclaimer"]}</p></details>'
    body = ph("Grants", "Grant Help & Tips", HELP["intro"], '<a class="mbtn" href="grants.html" style="margin-top:20px">Search grants →</a>') + panel('<div class="cap" style="margin-bottom:6px">How to write a strong application · <span id="hc">0/8</span> done</div>' + tips + mistakes + directory, "pad")
    js = """<script>
const done = new Set(JSON.parse(localStorage.getItem('e3-help') || '[]'));
function upd() { $$('.chk').forEach(c => c.classList.toggle('on', done.has(+c.dataset.i))); $('#hc').textContent = done.size + '/8'; localStorage.setItem('e3-help', JSON.stringify([...done])); }
$$('.chk').forEach(c => c.addEventListener('click', () => { const i = +c.dataset.i; done.has(i) ? done.delete(i) : done.add(i); upd(); })); upd();
</script>"""
    return shell("grant-help", body, js)
'''
B["category"] = r'''
def category(slug):
    """Header and one list."""
    cat, title, what = CATEGORY_PAGES[slug]
    intro, gs = category_intro(cat, what)
    gs = sorted(gs, key=lambda g: ({"open": 0, "rolling": 1, "closed": 2}[status(g)], days_left(g) if days_left(g) is not None else 999))
    others = " · ".join(f'<a href="{s}.html" style="color:var(--text)">{CAT_LABEL[v[0]]}</a>' for s, v in CATEGORY_PAGES.items() if s != slug)
    body = ph("Grant list", title, intro) + panel('<div class="rows">' + "".join(grow(g) for g in gs) + "</div>") + f'<p class="cap" style="margin-top:22px">More lists · {others} · <a href="grants.html" style="color:var(--text)">Search all {len(GRANTS)}</a></p>'
    return shell(slug, body)
'''
B["contact"] = r'''
def contact():
    """Header and the form."""
    form = """<form onsubmit="event.preventDefault();this.querySelector('[data-sent]').hidden=false" id="cf">
      <div class="grid" style="gap:0 18px"><label class="field c6"><span><span class="led" data-for="n"></span><span class="cap">Name *</span></span><input class="inp" id="n" required autocomplete="name"></label>
      <label class="field c6"><span><span class="led" data-for="e"></span><span class="cap">Email *</span></span><input class="inp" id="e" type="email" required autocomplete="email"></label></div>
      <label class="field"><span><span class="led" data-for="s"></span><span class="cap">Subject *</span></span><input class="inp" id="s" required></label>
      <label class="field"><span><span class="led" data-for="m"></span><span class="cap">Message *</span></span><textarea class="inp" id="m" required></textarea></label>
      <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap"><button class="mbtn" type="submit">Send message</button><span class="cap" data-sent hidden style="color:rgb(var(--led-near))">Mockup: nothing was sent</span></div></form>"""
    body = ph("Contact", "Let's connect", "Have questions about our research or want to collaborate? Send a message and we will respond within two business days. We use your details only to reply.") + f'<div style="max-width:780px">{panel(form, "pad")}</div>'
    js = """<script>
function chk() { ['n', 'e', 's', 'm'].forEach(id => { const v = $('#' + id).checkValidity() && $('#' + id).value; $(`[data-for=${id}]`).className = 'led' + (v ? ' on' : ''); }); }
$('#cf').addEventListener('input', chk);
</script>"""
    return shell("contact", body, js)
'''
B["privacy"] = r'''
def privacy():
    """Header and the policy."""
    out, ul = [], False
    for i, (t, txt) in enumerate(PRIVACY):
        if t == "li":
            if not ul:
                out.append("<ul>"); ul = True
            out.append(f"<li>{txt}</li>"); continue
        if ul:
            out.append("</ul>"); ul = False
        out.append(f"<{t}>{txt}</{t}>")
    if ul:
        out.append("</ul>")
    body = ph("Legal", "Privacy Policy", "The e3 Initiative is a small research organization. This page explains what information this website collects, why, and the choices you have.", '<div class="cap" style="margin-top:14px">Last updated · Nov 12 2026</div>') + f'<div style="max-width:860px">{panel("<div class=prose>" + "".join(out) + "</div>", "atile", "article")}</div>'
    return shell("privacy", body)
'''
B["journals"] = r'''
def journals():
    t, logo = JOURNAL
    body = ph("Publications", "Journals", "Browse our academic journals and long-form publications.") + panel(f"""
  <div style="display:flex;gap:34px;align-items:center;flex-wrap:wrap"><div style="border-radius:20px;background:var(--well);box-shadow:var(--well-shadow);padding:22px"><img src="{IMG}{logo}" alt="{esc(t)}" width="150" height="150" style="border-radius:12px"></div>
  <div><div class="cap">Journal</div><div style="font-weight:300;font-size:34px;letter-spacing:-.03em;line-height:1.1;margin-top:12px;max-width:20ch">{t}</div><div class="cap" style="margin-top:14px">Entries coming soon</div></div></div>""", "pad")
    return shell("journals", body)
'''
B["outreach"] = r'''
def outreach():
    cards = "".join(panel(f"""<div class="cap">{t}</div>
      <p style="font-weight:300;font-size:26px;line-height:1.3;letter-spacing:-.02em;margin:22px 0 16px">{p1}</p><p class="dim" style="font-size:14px;line-height:1.6">{p2}</p>
      <a class="mbtn" href="contact.html" style="margin-top:26px">{'Share your story' if k == 'interview' else 'Partner with us'} →</a>""", "pad c6", attrs=f'id="{k}"') for k, (t, s, p1, p2) in OUTREACH.items())
    return shell("outreach", ph("Outreach", "Outreach", "Interviews and partnerships: how community knowledge gets into our research.") + f'<div class="grid">{cards}</div>')
'''


def apply_funcs(fn, funcs, mapping):
    s = open(fn).read()
    for key, name in mapping.items():
        s = replace_func(s, name, funcs[key])
    open(fn, "w").write(s)


def apply():
    apply_funcs("theme_a.py", A, {k: {"notfound": "notfound"}.get(k, k) for k in A})
    apply_funcs("theme_b.py", B, {k: k for k in B})

    # ───── C: type specimen — string edits on the existing functions ─────
    s = open("theme_c.py").read()
    # about: statement, three names, one line of approach
    s = replace_func(s, "about", r'''
def about():
    """Header, one statement, three people."""
    team = "".join(f'<div class="pub"><div class="no">0{i+1}</div><div><h3 data-lens="300" style="font-size:40px">{n}</h3><p style="font-size:15px">{b}</p></div><div class="meta"><b>{r}</b></div></div>' for i, (n, r, b) in enumerate(ABOUT["team"]))
    body = ph("About", "About e3 Initiative", ABOUT["what"]) + f"""
<p style="font-size:30px;line-height:1.25;letter-spacing:-.025em;font-variation-settings:'wght' 260;max-width:40ch;margin-top:50px">{ABOUT['who']}</p>
<section style="margin-top:60px">{team}<p class="lab" style="margin-top:28px;line-height:1.7;max-width:80ch">We believe in community voices, cross-sector collaboration, and turning findings into stories of economic resilience.</p></section>"""
    return shell("about", body)
''')
    # publications: header and rows only
    s = s.replace('''    links = '<p class="lab" style="margin-top:24px">Also: <a href="journals.html" style="color:var(--ink)">Journals</a> · <a href="economic-indicators.html" style="color:var(--ink)">Economic indicators</a></p>'
    return shell(page, ph("Publications", title, lede) + "".join(pub_row(i, p, False) for i, p in enumerate(items)) + links)''',
                  '''    return shell(page, ph("Publications", title, lede) + "".join(pub_row(i, p, False) for i, p in enumerate(items)))''')
    # article: single column, no margin asides
    s = re.sub(r'<div class="read">\s*<aside class="margin">.*?</aside>\s*<article class="prose" id="prose">\{\'\'\.join\(body\)\}</article>\s*<aside></aside>\s*</div>',
               '<div class="read" style="grid-template-columns:1fr;max-width:700px;margin-left:auto;margin-right:auto"><article class="prose" id="prose">{\'\'.join(body)}</article></div>', s, flags=re.S)
    s = s.replace("""  let cur = null; $$('#prose h2').forEach(h => { if (h.getBoundingClientRect().top < innerHeight * .35) cur = h.id; }); $$('.margin a[data-s]').forEach(a => a.classList.toggle('on', a.dataset.s === cur)); }""", " }")
    s = s.replace("""<span class="lab" id="rw">reading gives it weight · wght 100</span>""", """<span class="lab" id="rw">wght 100</span>""")
    s = s.replace("$('#rw').textContent = 'reading gives it weight · wght ' + w;", "$('#rw').textContent = 'wght ' + w;")
    s = s.replace("""  <div class="lab" style="margin-top:22px">{esc(a['byline'] or 'By ' + p['author'])} · {p['min']} min</div></div>""",
                  """  <div class="lab" style="margin-top:22px">{esc(a['byline'] or 'By ' + p['author'])} · {p['min']} min · <a href="../../{cite}" style="text-decoration:underline dashed var(--guide);text-underline-offset:4px">citations</a></div></div>""")
    # grants: who-qualifies moves into the folded filters
    s = s.replace("""  <div class="fgroup"><span class="lab">Who qualifies</span><div class="ftabs" data-f="elig"><button class="on" data-v="">Anyone</button><button data-v="small_business">Small business</button><button data-v="nonprofit">Nonprofit</button></div></div>
  <div class="fgroup"><span class="lab">Status</span>""", """  <div class="fgroup"><span class="lab">Status</span>""")
    s = s.replace("""<details class="fgroup" style="display:block"><summary class="lab" style="cursor:pointer">+ More filters</summary>
""", """<details class="fgroup" style="display:block"><summary class="lab" style="cursor:pointer">+ More filters</summary>
    <div class="fgroup" style="margin-top:12px"><span class="lab">Who qualifies</span><div class="ftabs" data-f="elig"><button class="on" data-v="">Anyone</button><button data-v="small_business">Small business</button><button data-v="nonprofit">Nonprofit</button></div></div>
""")
    # grant help: directory folded
    s = s.replace("""<section><div class="sh"><h2>Where to get free help</h2></div>{orgs}<p class="lab" style="margin-top:20px;line-height:1.7;max-width:90ch">{HELP['disclaimer']}</p></section>\"\"\"""",
                  """<section><details><summary class="sh" style="cursor:pointer"><h2>Where to get free help</h2><span class="lab">+ show</span></summary>{orgs}<p class="lab" style="margin-top:20px;line-height:1.7;max-width:90ch">{HELP['disclaimer']}</p></details></section>\"\"\"""")
    # category: drop the three numerals
    s = s.replace("""<div class="grid" style="margin-top:50px">{nums}</div>
<table class="gt" style="margin-top:50px">""", """<table class="gt" style="margin-top:40px">""")
    # contact: form only
    s = re.sub(r'\n<aside class="c4"><div class="big-num w8".*?</aside></div>"""', '\n</div>"""', s, flags=re.S)
    # privacy: header and prose only
    s = re.sub(r'<div class="read"><aside class="margin">.*?</aside><article class="prose" style="--bw:400">\{\'\'\.join\(out\)\.replace\(.*?\)\}</article><aside></aside></div>',
               '<div class="read" style="grid-template-columns:1fr;max-width:700px"><article class="prose" style="--bw:400">{\'\'.join(out)}</article></div>', s, flags=re.S)
    open("theme_c.py", "w").write(s)


if __name__ == "__main__":
    apply()
