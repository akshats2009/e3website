import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from make_preview2 import build
def gf(*fams): return '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' + "".join(f'<link href="https://fonts.googleapis.com/css2?family={f}&display=swap" rel="stylesheet">' for f in fams)
def pal(bg, surface, ink, muted, accent, onaccent, accent2, onaccent2, tint, dbg, dsurface, dink, dmuted, daccent, donaccent, daccent2, donaccent2, dtint):
    L = dict(bg=bg, surface=surface, ink=ink, muted=muted, accent=accent, onaccent=onaccent, accent2=accent2, onaccent2=onaccent2, wash=f"color-mix(in srgb,{ink} 8%,transparent)", tint1=tint)
    D = dict(bg=dbg, surface=dsurface, ink=dink, muted=dmuted, accent=daccent, onaccent=donaccent, accent2=daccent2, onaccent2=donaccent2, wash="rgba(255,255,255,.09)", tint1=dtint)
    return L, D
T = {}
L, D = pal("#faf3ea", "#fffaf3", "#2a1f1a", "#65544b", "#b4472b", "#ffffff", "#1f6360", "#ffffff", "rgba(180,71,43,.28)", "#1a1311", "#251b18", "#f6ece2", "#c9b8ab", "#e87a57", "#1a0d08", "#63bdb7", "#0d1f1e", "rgba(232,122,87,.3)")
T["t1-terracotta"] = dict(light=L, dark=D, serif="'Fraunces',Georgia,serif", sans="'DM Sans',system-ui,sans-serif", h1w="600", brandw="600", links=gf("Fraunces:opsz,wght@9..144,400..700", "DM+Sans:wght@400;500;600;700"))
L, D = pal("#f7f4ec", "#ffffff", "#14213d", "#4a5568", "#1d3a8a", "#ffffff", "#f2b01e", "#14213d", "rgba(29,58,138,.22)", "#0e1526", "#172036", "#f3efe4", "#b6bfd0", "#8fa8ff", "#0e1526", "#f2b01e", "#14213d", "rgba(143,168,255,.25)")
T["t2-ink-marigold"] = dict(light=L, dark=D, serif="'Source Serif 4',Georgia,serif", sans="'Source Sans 3',system-ui,sans-serif", h1w="600", brandw="600", links=gf("Source+Serif+4:opsz,wght@8..60,400..700", "Source+Sans+3:wght@400..700"))
L, D = pal("#f3eee3", "#fbf8f0", "#17261f", "#52625a", "#2b6a4d", "#ffffff", "#d27d2d", "#1a1006", "rgba(43,106,77,.25)", "#0f1a15", "#18261f", "#eef0e6", "#b3c2b8", "#6fcf9d", "#07140d", "#e8a35a", "#1a1006", "rgba(111,207,157,.22)")
T["t3-forest-sand"] = dict(light=L, dark=D, serif="'Literata',Georgia,serif", sans="'Figtree',system-ui,sans-serif", h1w="600", brandw="600", links=gf("Literata:opsz,wght@7..72,400..700", "Figtree:wght@400;500;600;700"))
L, D = pal("#fbf1ee", "#fff8f5", "#2b1730", "#66506b", "#7a2e6e", "#ffffff", "#f08a5d", "#2b1730", "rgba(122,46,110,.22)", "#1a0f1d", "#25172a", "#f8ecf2", "#c9b3cf", "#d98ccb", "#1a0f1d", "#f59a72", "#2b1730", "rgba(217,140,203,.25)")
T["t4-plum-peach"] = dict(light=L, dark=D, serif="'Young Serif',Georgia,serif", sans="'Inter',system-ui,sans-serif", h1w="400", brandw="400", links=gf("Young+Serif", "Inter:wght@400;500;600;700"))
L, D = pal("#f7f6f2", "#ffffff", "#101828", "#4a5565", "#b3122b", "#ffffff", "#1f3a93", "#ffffff", "rgba(31,58,147,.2)", "#0c1220", "#151c2e", "#f3f1ea", "#b8c0cf", "#ff6b7e", "#1a0509", "#8aa4ff", "#0c1220", "rgba(138,164,255,.22)")
T["t5-civic-red-blue"] = dict(light=L, dark=D, serif="'Spectral',Georgia,serif", sans="'Public Sans',system-ui,sans-serif", h1w="600", brandw="600", links=gf("Spectral:wght@400;500;600;700", "Public+Sans:wght@400;500;600;700"))
L, D = pal("#fff8ec", "#fffdf7", "#1f2937", "#4b5563", "#0f6b64", "#ffffff", "#f2a30f", "#1f2937", "rgba(15,107,100,.22)", "#10201f", "#172a29", "#f4f1e6", "#b6c7c4", "#4fd1c5", "#04201d", "#f6b73c", "#1f2937", "rgba(79,209,197,.22)")
T["t6-sunrise-teal"] = dict(light=L, dark=D, serif="'Lora',Georgia,serif", sans="'Work Sans',system-ui,sans-serif", h1w="600", brandw="600", links=gf("Lora:wght@400..700", "Work+Sans:wght@400;500;600;700"))
if __name__ == "__main__":
    for name, t in T.items():
        build(t, f"/home/user/e3website/mockups/lab/{name}.html", fontlinks=t["links"])
        print(name)
