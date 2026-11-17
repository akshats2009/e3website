"""Add a separate light/dark mode toggle to all themes (idempotent)."""
SUN = '<svg class="sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
MOON = '<svg class="moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/></svg>'

def snippet(key, non, default):
    head = f"<script>try{{if(localStorage.getItem('{key}')==='{non}')document.documentElement.classList.add('{non}')}}catch(e){{}}</script>"
    js = ("<script>(function(){var r=document.documentElement;document.querySelectorAll('[data-mode]').forEach(function(b){"
          f"b.setAttribute('aria-pressed',r.classList.contains('{non}'));"
          "b.onclick=function(){"
          f"var on=r.classList.toggle('{non}');try{{localStorage.setItem('{key}',on?'{non}':'{default}')}}catch(e){{}}"
          "document.querySelectorAll('[data-mode]').forEach(function(x){x.setAttribute('aria-pressed',on)})}})})();</script>")
    return head, js

BASE = ".nav-end{display:flex;align-items:center;gap:10px}.mode{width:40px;height:40px;border-radius:50%%;display:grid;place-items:center;flex:none;background:color-mix(in srgb,%s 8%%,transparent);color:%s;transition:background .2s}.mode:hover{background:color-mix(in srgb,%s 14%%,transparent)}.mode svg{grid-area:1/1}"

B_CSS = BASE % ("var(--text)", "var(--text)", "var(--text)") + r"""
.mode .moon{display:none}html.light .mode .sun{display:none}html.light .mode .moon{display:block}
html.light{--page:#e5e5e8;--text:#141416;--text-rgb:20 20 22;--label:rgba(20,20,22,.5);--strong:rgba(20,20,22,.88);--body:rgba(20,20,22,.76);
 --panel-top:#fcfcfd;--panel-mid:#f4f4f6;--panel-bottom:#ececef;--divider:rgba(0,0,0,.06);--row-line:rgba(0,0,0,.07);--track:#d6d6db;--tick:rgba(0,0,0,.22);--tick-label:rgba(0,0,0,.42);--led-off:rgba(0,0,0,.09);
 --well:#e3e3e7;--well-shadow:inset 0 1px 2px rgba(0,0,0,.14)}
html.light body{background:radial-gradient(1400px 900px at 50% 300px,#f4f4f6 0%,#e9e9ec 60%,var(--page) 100%) no-repeat}
html.light .grain{opacity:.035}html.light .sheen{display:none}
html.light .panel::before{box-shadow:inset 0 1px 0 #fff,0 40px 70px -44px rgba(0,0,0,.3)}
html.light .mbtn:not(.ghost){background:#141416;color:#f4f4f6;box-shadow:0 10px 18px -8px rgba(0,0,0,.45)}
html.light .mbtn.ghost{background:rgba(0,0,0,.06)}
html.light .menu-btn{box-shadow:none;background:rgba(0,0,0,.06)}
html.light .inp{background:#e3e3e7}html.light .inp:focus{background:#dadade}
html.light .knob .tr{stroke:rgba(0,0,0,.1)}html.light .knob .pg{stroke:#141416}
html.light .fader .fill{background:linear-gradient(0deg,rgba(0,0,0,.1),rgba(0,0,0,.5))}
html.light .prow:hover h3{color:#000}
html.light .nav ul.open{background:#f4f4f6}
html.light .key{color:rgba(244,244,246,.55)}html.light .key.on{color:#f4f4f6}html.light .key::before{background:rgba(255,255,255,.14)}
"""
C_CSS = BASE % ("var(--ink)", "var(--ink)", "var(--ink)") + r"""
.mode .sun{display:none}html.dark .mode .sun{display:block}html.dark .mode .moon{display:none}
html.dark{--page:#10100f;--paper-light:#1b1a18;--ink:#f2efe8;--label-ink:rgba(242,239,232,.45);--soft:rgba(242,239,232,.62);--track:rgba(242,239,232,.12);--tick:rgba(242,239,232,.26);--rule:rgba(242,239,232,.12);--wash:rgba(242,239,232,.05)}
html.dark body::after{mix-blend-mode:screen;opacity:.1}
html.dark .tkl{color:rgba(242,239,232,.4)}
html.dark .inp::placeholder,html.dark .bigsearch::placeholder{color:rgba(242,239,232,.25)}
html.dark .pill.o{background:rgba(242,239,232,.09);color:var(--ink)}
html.dark .inp{background:rgba(242,239,232,.06)}html.dark .inp:focus{background:rgba(242,239,232,.1)}
html.dark .menu-btn{background:rgba(242,239,232,.08)}
html.dark .knob{background:#f2efe8}
"""

def patch(fn, key, non, default, css, icons_first):
    s = open(fn).read()
    if "MODE_HEAD" in s: return
    head, js = snippet(key, non, default)
    s = s.replace('def shell(', f'MODE_HEAD = {head!r}\nMODE_JS = {js!r}\nMODE_CSS = {css!r}\nMODE_BTN = \'<button class="mode" data-mode aria-label="Toggle dark mode" aria-pressed="false">{SUN}{MOON}</button>\'\n\n\ndef shell(', 1)
    s = s.replace('{FONTS}<link rel="stylesheet" href="theme.css"></head>', '{MODE_HEAD}{FONTS}<link rel="stylesheet" href="theme.css"></head>', 1)
    s = s.replace('<script src="theme.js"></script>\n{scripts}', '<script src="theme.js"></script>\n{MODE_JS}\n{scripts}', 1)
    s = s.replace('CSS + NOB', 'CSS + NOB + MODE_CSS')
    open(fn, 'w').write(s)

patch("theme_b.py", "e3-mode-b", "light", "dark", B_CSS, 0)
patch("theme_c.py", "e3-mode-c", "dark", "light", C_CSS, 0)
