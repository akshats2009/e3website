"""Removes outlines, hairline dividers and heavy frames from all three themes by appending CSS overrides."""

A = r"""
/* no borders: surfaces separate by tone and space only */
:root{--r:22px}
.tile{box-shadow:none!important;border-radius:22px}
.pill-nav{box-shadow:none}
.crow,.grow,.check,.toc .crow{border-top:0!important}
.cal .div,.gdetail{border:0}
.cal .div{display:none}
details{border-top:0!important}
.btn.ghost{box-shadow:none;background:var(--wash)}
footer{border-top:0}
.tile.rows .crow + .crow,.gres .grow + .grow{box-shadow:none}
.menu-btn{box-shadow:none}
.knob,.mini-sw b{box-shadow:0 2px 6px rgba(0,0,0,.18)}
.inp:focus{box-shadow:none;background:rgb(var(--ink-rgb)/.08)}
.cover.photo,.banner{border-radius:16px}
"""

B = r"""
/* no borders */
:root{--r:22px}
.panel::after{display:none}
.panel::before{box-shadow:0 30px 60px -40px rgba(0,0,0,.85)}
.nav{border-bottom:0}
footer{border-top:0}
.rrow,.prow,.chk,.secs a,details{border-top:0!important}
.mrow{border:0!important}
.strip + .strip::before,.master::before,.vline + .vline::before,.lens + .lens::before{display:none}
.mbtn.ghost{box-shadow:none;background:rgba(255,255,255,.07)}
.key{box-shadow:0 4px 10px rgba(0,0,0,.5)}
.inp{box-shadow:none;background:#0b0b0d}
.inp:focus{box-shadow:none;background:#111114}
.tog{box-shadow:none}
.brand i,.fcap,.mbtn{box-shadow:0 6px 14px rgba(0,0,0,.5)}
.mbtn.ghost{box-shadow:none}
"""

C = r"""
/* no borders: type and space do the separating */
.nav,footer,.sh,.pub,.ph,.lede2,.lenses,.ind,.fgroup,.tip-row,.gt th,.gt td,.rule{border:0!important}
.ln + .ln{border:0!important}
.ph .baseguide,.pub::after{display:none}
.pill.o{box-shadow:none;background:rgba(20,19,18,.07)}
.inp{border:0!important;background:rgba(20,19,18,.05);padding:14px 16px;border-radius:10px;font-size:22px}
.inp:focus{background:rgba(20,19,18,.08)}
.bigsearch{border:0!important;background:transparent}
.menu-btn{box-shadow:none;background:rgba(20,19,18,.06)}
.nav ul a.on{text-decoration:none;font-variation-settings:'wght' 700}
.fgroup,.tip-row{padding-top:12px}
.knob{box-shadow:0 6px 14px -4px rgba(20,19,18,.3)}
.banner img,.pub img{border-radius:10px}
"""

def apply():
    for fn, key, css in [("theme_a.py", "A", A), ("theme_b.py", "B", B), ("theme_c.py", "C", C)]:
        s = open(fn).read()
        marker = "# NOBORDERS\n"
        if marker in s:
            s = s[:s.index(marker)]
        s = s.replace('write(f"{D}/theme.css", CSS)', 'write(f"{D}/theme.css", CSS + NOB)')
        s += "\n" + marker + 'NOB = r"""' + css + '"""\n'
        open(fn, "w").write(s)

if __name__ == "__main__":
    apply()
