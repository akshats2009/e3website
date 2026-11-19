"""Aesthetic pass for D: glass nav, graded photography, floating departure card, station footer, giant wordmark, parallax."""
s = open("theme_d.py").read()

# floating "next departure" card on the hero photo (real data: the next closing grant)
NEXT = r'''
def nextcard():
    g = DATED_SOON[0]
    d = days_left(g)
    return f"""<a class="dep" href="grants.html"><span class="dep-k">Next departure</span><span class="dep-t">{esc(g['name'])}</span><span class="dep-m"><b>{d}</b> days<i></i>{money(g.get('amountMax') or 0) if g.get('amountMax') else ''}</span></a><div class="loc"><svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg><span class="loc-d">Mott Street, Manhattan</span><span class="loc-n">Mott Street, Manhattan · night</span></div>"""

'''
s = s.replace("def home():", NEXT + "\ndef home():", 1)
s = s.replace('alt="Mott Street in Manhattan at night, strung with lights">', 'alt="Mott Street in Manhattan at night, strung with lights">\n    <div class="grade"></div>{nextcard()}', 1)

# footer: stations + giant wordmark
s = s.replace("  </footer>\n</div>", '  </footer>\n  <div class="mega" aria-hidden="true">e3 Initiative</div>\n</div>', 1)

AES = r"""
/* aesthetic pass */
body{background:var(--bg);position:relative}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background:radial-gradient(900px 520px at 88% -8%,rgba(0,160,106,.16),transparent 60%),radial-gradient(760px 480px at -8% 38%,rgba(255,196,46,.10),transparent 62%)}
html.night body::before{background:radial-gradient(900px 560px at 88% -10%,rgba(0,190,125,.20),transparent 60%),radial-gradient(800px 520px at -10% 40%,rgba(255,196,46,.12),transparent 62%),radial-gradient(600px 400px at 60% 110%,rgba(80,90,200,.14),transparent 60%)}
body::after{content:"";position:fixed;inset:0;pointer-events:none;z-index:50;opacity:.06;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.wrap{position:relative;z-index:1}

/* frosted sticky nav with a glowing line */
.nav{position:sticky;top:0;z-index:30;margin-inline:calc(50% - 50vw);padding:18px calc(50vw - 50%) 18px;backdrop-filter:blur(18px) saturate(1.4);-webkit-backdrop-filter:blur(18px) saturate(1.4);
  background:linear-gradient(180deg,color-mix(in srgb,var(--bg) 94%,transparent),color-mix(in srgb,var(--bg) 62%,transparent))}
.pill-nav::before{box-shadow:0 0 14px rgba(0,160,106,.55)}
html.night .pill-nav::before{box-shadow:0 0 18px rgba(0,210,140,.7)}
.pill-nav a.on::before{box-shadow:0 0 0 4px var(--accent),0 0 18px rgba(0,190,125,.8)}
.brand i{box-shadow:0 6px 18px -4px rgba(0,160,106,.7)}

/* hero */
.stxt h1{font-size:clamp(3rem,5.6vw,5.4rem)!important;max-width:none}
.split{gap:56px;min-height:0;align-items:center;margin-top:8px}
.spic{border-radius:30px;min-height:min(72vh,680px);box-shadow:0 50px 90px -40px rgba(10,20,30,.55),0 0 0 1px rgba(255,255,255,.05);transform:rotate(0.0001deg)}
html.night .spic{box-shadow:0 60px 120px -40px rgba(0,190,125,.25),0 0 0 1px rgba(255,255,255,.07)}
.spic img{transform:scale(1.08);will-change:transform}
.spic .grade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,12,16,0) 45%,rgba(8,12,16,.62) 100%),linear-gradient(135deg,rgba(0,160,106,.22),rgba(255,196,46,.12) 70%);mix-blend-mode:normal;pointer-events:none}
.stxt .cta .btn{box-shadow:0 14px 30px -12px rgba(16,19,24,.6);transition:transform .3s cubic-bezier(.33,1,.68,1),box-shadow .3s}
.stxt .cta .btn:hover{transform:translateY(-3px);box-shadow:0 22px 36px -14px rgba(16,19,24,.7)}
html.night .stxt .cta .btn{box-shadow:0 14px 40px -12px rgba(0,210,140,.45)}
.dep{position:absolute;left:22px;bottom:22px;display:grid;gap:3px;padding:16px 20px 15px;min-width:250px;max-width:70%;border-radius:20px;color:#fff;
  background:rgba(14,18,24,.46);backdrop-filter:blur(20px) saturate(1.5);-webkit-backdrop-filter:blur(20px) saturate(1.5);box-shadow:inset 0 1px 0 rgba(255,255,255,.18);transition:transform .35s cubic-bezier(.33,1,.68,1),background .3s}
.dep:hover{transform:translateY(-4px);background:rgba(14,18,24,.6)}
.dep-k{font:600 .68rem var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--peach)}
.dep-t{font-weight:600;font-size:1.05rem;line-height:1.2;letter-spacing:-.01em}
.dep-m{display:flex;align-items:center;gap:8px;font:500 .8rem var(--mono);color:rgba(255,255,255,.78)}
.dep-m b{font:700 1.4rem var(--sans);color:#fff;letter-spacing:-.02em}.dep-m i{width:4px;height:4px;border-radius:50%;background:currentColor;opacity:.6}
.loc{position:absolute;right:20px;top:20px;display:flex;align-items:center;gap:7px;padding:8px 13px;border-radius:99px;font:500 .72rem var(--mono);letter-spacing:.04em;color:#fff;background:rgba(14,18,24,.4);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}
.loc-n{display:none}html.night .loc-d{display:none}html.night .loc-n{display:inline}

/* cards and rows */
.pimg{border-radius:24px;box-shadow:0 30px 50px -30px rgba(10,20,30,.5);position:relative}
.pimg::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,rgba(8,12,16,.38));opacity:.7;transition:opacity .4s}
.pcard:hover .pimg::after{opacity:.2}
.pcard{transition:transform .5s cubic-bezier(.33,1,.68,1)}.pcard:hover{transform:translateY(-6px)}
html.night .pimg{box-shadow:0 30px 60px -30px rgba(0,190,125,.22)}
.abimg{border-radius:28px;box-shadow:0 50px 80px -40px rgba(10,20,30,.55)}
.tile{box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 30px 60px -40px rgba(20,30,40,.35)!important}
html.night .tile{box-shadow:0 1px 0 rgba(255,255,255,.05) inset,0 30px 70px -40px rgba(0,0,0,.9)!important;background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,0) 40%),var(--tile)}
.grow:hover,.crow:hover{background:color-mix(in srgb,var(--accent) 7%,transparent)}

/* footer: route line with stations, then a giant wordmark */
footer{position:relative;padding-top:56px;margin-top:70px}
footer .links{position:relative;display:flex;gap:6px 28px}
footer .links a{position:relative;padding-top:20px;color:var(--muted);transition:color .2s}
footer .links a::before{content:"";position:absolute;left:0;top:3px;width:9px;height:9px;border-radius:50%;background:var(--bg);box-shadow:0 0 0 2px var(--accent);transition:transform .2s,background .2s}
footer .links a:hover{color:var(--ink)}footer .links a:hover::before{background:var(--accent);transform:scale(1.35)}
footer .links::before{content:"";position:absolute;left:4px;right:20px;top:7px;height:2px;border-radius:1px;background:linear-gradient(90deg,var(--accent),color-mix(in srgb,var(--accent) 0%,transparent))}
.mega{position:relative;z-index:0;margin:22px 0 -.06em;text-align:center;white-space:nowrap;font:800 18.6vw/.84 var(--sans);font-stretch:62%;font-variation-settings:'wdth' 62;letter-spacing:-.02em;text-transform:uppercase;color:transparent;background:linear-gradient(180deg,color-mix(in srgb,var(--ink) 22%,transparent),color-mix(in srgb,var(--ink) 3%,transparent) 85%);-webkit-background-clip:text;background-clip:text;pointer-events:none;user-select:none;overflow:hidden;max-width:100vw}
  background:linear-gradient(180deg,color-mix(in srgb,var(--ink) 14%,transparent),transparent 78%);-webkit-background-clip:text;background-clip:text;pointer-events:none;user-select:none;overflow:hidden;height:.62em}

@media(max-width:900px){.nav{padding-block:14px}.spic{min-height:380px}.dep{min-width:0;max-width:calc(100% - 44px)}.loc{display:none}footer .links{flex-wrap:wrap}}
@media(prefers-reduced-motion:reduce){.pcard,.dep,.stxt .cta .btn{transition:none}}
"""
s = s.replace('CITYJS = r"""', 'CITY += r"""' + AES + '"""\n\nCITYJS = r"""', 1)

# gentle parallax on the hero photo
PAR = r"""
(function () {
  const img = document.querySelectorAll('.spic img'); if (!img.length || matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  let y = 0, ticking = false;
  const upd = () => { img.forEach(i => i.style.transform = `translateY(${y * -.06}px) scale(1.1)`); ticking = false; };
  addEventListener('scroll', () => { y = scrollY; if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true }); upd();
})();
"""
s = s.replace('CITYJS = r"""', 'CITYJS = r"""' + PAR, 1)
open("theme_d.py", "w").write(s)
