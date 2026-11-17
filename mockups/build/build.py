"""Builds the three site-wide mockups into mockups/site-a, site-b, site-c, plus the shared data and a gallery page.
Run from anywhere: python3 mockups/build/build.py"""
import importlib
import sys

from common import PAGES, TITLES, grants_js, INDICATORS_JS, write

THEMES = [
    ("a", "Paper widgets", "Warm paper, white tiles, thin numerals, one ultramarine accent. Built from paper-widgets."),
    ("b", "Graphite desk", "Dark graphite hardware: metal faders, a stepped knob, LED meters. Built from budget-mixer."),
    ("c", "Type specimen", "Warm paper and a variable font: weight carries meaning, orange type guides. Built from weight-axis."),
]


def main(only=None):
    write("shared/grants-data.js", grants_js())
    write("shared/indicators.js", INDICATORS_JS)
    built = {}
    for key, name, _ in THEMES:
        if only and key not in only:
            continue
        mod = importlib.import_module(f"theme_{key}")
        built[key] = mod.build()
        print(f"site-{key}: {len(built[key])} pages")
    rows = "".join(
        f'<li><a href="{p}.html">{TITLES[p]}</a></li>' for p in PAGES
    )
    cards = "".join(f"""
  <section>
    <h2><span>{k.upper()}</span>{n}</h2><p>{d}</p>
    <ul>{rows.replace('href="', f'href="site-{k}/')}</ul>
  </section>""" for k, n, d in THEMES)
    write("index.html", f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>e3 Initiative · site-wide mockups</title>
<style>
body{{font:15px/1.5 system-ui,sans-serif;margin:0;padding:48px 32px;background:#f4f3f0;color:#141416}}
h1{{font-weight:400;font-size:40px;letter-spacing:-.03em;margin:0 0 8px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin-top:32px}}
section{{background:#fff;border-radius:20px;padding:24px;box-shadow:0 1px 0 rgba(0,0,0,.05)}}
h2{{font-weight:500;font-size:22px;margin:0;display:flex;gap:10px;align-items:center}}
h2 span{{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:8px;background:#141416;color:#fff;font-size:14px}}
p{{color:#6b6862;margin:8px 0 14px}} ul{{margin:0;padding:0;list-style:none;columns:2;column-gap:20px}} li{{margin:4px 0;break-inside:avoid}}
a{{color:#2b36ff;text-decoration:none}} a:hover{{text-decoration:underline}}
</style></head><body>
<h1>e3 Initiative: three site-wide directions</h1>
<p>Same pages, same content, three designs. Open the pages over a local server (for example <code>python3 -m http.server</code> from the repo root) so the shared data loads.</p>
<div class="grid">{cards}</div>
</body></html>
""")


if __name__ == "__main__":
    sys.path.insert(0, __import__("os").path.dirname(__file__))
    main(sys.argv[1:] or None)
