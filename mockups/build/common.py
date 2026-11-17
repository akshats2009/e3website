"""Shared content for the three site-wide mockups. Every theme renders the same pages from this data,
so the variations differ only in design. Text is taken from the live pages; grants from data/grants.json."""
import datetime
import html
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "mockups")
TODAY = datetime.date(2026, 11, 17)
IMG = "../../image/"

esc = html.escape

# ——— Navigation ———
NAV = [
    ("about.html", "About"),
    ("articles.html", "Publications"),
    ("grants.html", "Grants"),
    ("contact.html", "Contact"),
]
FOOT = [
    ("articles.html", "Publications"), ("grants.html", "Grant Finder"), ("grant-help.html", "Grant Help"),
    ("economic-indicators.html", "Indicators"), ("outreach.html", "Outreach"), ("privacy.html", "Privacy"),
]
# which nav item a page lights up
SECTION = {
    "index": "index.html", "about": "about.html", "articles": "articles.html", "article-railroad": "articles.html",
    "article-chinatown": "articles.html", "research": "articles.html", "research-chinatown": "articles.html",
    "journals": "articles.html", "grants": "grants.html", "grant-help": "grants.html",
    "minority-owned-business-grants": "grants.html", "women-owned-business-grants": "grants.html",
    "veteran-owned-business-grants": "grants.html", "economic-indicators": "articles.html",
    "outreach": "about.html", "contact": "contact.html", "privacy": "", "404": "",
}

# ——— Grants ———
GRANTS = json.load(open(os.path.join(ROOT, "data", "grants.json")))
CAT_LABEL = {
    "minority_owned": "Minority-owned", "women_owned": "Women-owned", "veteran_owned": "Veteran-owned",
    "arts_culture": "Arts & culture", "research": "Research", "technology": "Technology",
    "community_development": "Community", "food_agriculture": "Food & farming", "health": "Health",
    "environment": "Environment", "general": "General",
}
ELIG_LABEL = {"small_business": "Small business", "nonprofit": "Nonprofit", "both": "Business or nonprofit"}


def days_left(g):
    try:
        return (datetime.date.fromisoformat(g["deadline"]) - TODAY).days
    except ValueError:
        return None


def status(g):
    """The status a visitor should see. A dated deadline in the past is closed, whatever the file says."""
    d = days_left(g)
    if d is not None and d < 0:
        return "closed"
    return g["status"]


def deadline_label(g):
    d = days_left(g)
    if d is not None:
        return datetime.date.fromisoformat(g["deadline"]).strftime("%b %d")
    return {"rolling": "Rolling", "annual": "Annual"}.get(g["deadline"], g["deadline"].title())


def money(v):
    if not v:
        return "Varies"
    if v >= 1_000_000:
        return "$" + (f"{v/1e6:.1f}".rstrip("0").rstrip(".")) + "M"
    if v >= 1000:
        return f"${round(v/1000):,}k"
    return f"${v:,}"


OPEN = [g for g in GRANTS if status(g) != "closed"]
DATED_SOON = sorted([g for g in OPEN if days_left(g) is not None], key=days_left)

CATEGORY_PAGES = {
    "minority-owned-business-grants": ("minority_owned", "Grants for Minority-Owned Businesses",
        "for founders and organizations from communities that have historically had less access to capital, including Black, Native American, Hispanic/Latino, and LGBTQ+ business owners"),
    "women-owned-business-grants": ("women_owned", "Grants for Women-Owned Businesses",
        "for women entrepreneurs and women-led organizations, from monthly micro-grants to awards of up to $100,000"),
    "veteran-owned-business-grants": ("veteran_owned", "Grants for Veteran-Owned Businesses",
        "for veteran and military-spouse entrepreneurs, plus nonprofits that serve veterans and their families"),
}


def category_intro(cat, what):
    gs = [g for g in GRANTS if g["category"] == cat]
    c = {s: sum(1 for g in gs if status(g) == s) for s in ("open", "rolling", "closed")}
    parts = []
    if c["open"]:
        parts.append(f"{c['open']} {'is' if c['open'] == 1 else 'are'} open now")
    if c["rolling"]:
        parts.append(f"{c['rolling']} accept applications on a rolling basis")
    if c["closed"]:
        parts.append(f"{c['closed']} {'is' if c['closed'] == 1 else 'are'} closed for now")
    lst = ", ".join(parts[:-1]) + (", and " if len(parts) > 1 else "") + parts[-1]
    return (f"This list gathers {len(gs)} grants {what}. {lst[0].upper() + lst[1:]}. "
            "Many of the closed programs run every year, so they are worth tracking."), gs


def grants_js():
    """The grant data as a JS file every theme's finder reads."""
    rows = []
    for g in GRANTS:
        rows.append({
            "name": g["name"], "funder": g["funder"], "elig": g["eligibility"], "cat": g["category"],
            "amount": g["amount"], "max": g.get("amountMax") or 0, "deadline": g["deadline"],
            "days": days_left(g), "status": status(g), "desc": g["description"], "link": g["link"],
            "dl": deadline_label(g),
        })
    return ("/* Generated from data/grants.json for the mockups. Status is recomputed: a past dated deadline is closed. */\n"
            "window.GRANTS = " + json.dumps(rows, ensure_ascii=False) + ";\n"
            "window.CAT_LABEL = " + json.dumps(CAT_LABEL) + ";\n"
            "window.ELIG_LABEL = " + json.dumps(ELIG_LABEL) + ";\n")


# ——— Publications ———
def _clean(fragment):
    """Keep <em>, <strong>, <i>, <b>; drop every other tag."""
    fragment = re.sub(r"(?is)<(?!/?(em|strong|i|b)\b)[^>]+>", "", fragment)
    return " ".join(fragment.split())


def extract(path):
    s = open(os.path.join(ROOT, path)).read()
    s = re.sub(r"(?s)<(script|style|head|nav|footer)[^>]*>.*?</\1>", "", s)
    blocks, title, byline, caption = [], "", "", ""
    for m in re.finditer(r"(?s)<(h1|h2|h3|p|blockquote|li)[^>]*>(.*?)</\1>", s):
        tag, text = m.group(1), _clean(m.group(2))
        plain = html.unescape(re.sub(r"<[^>]+>", "", text))
        if not plain or plain.startswith(("Skip to", "←", "View Citations")):
            continue
        if tag == "h1":
            title = plain
        elif plain.startswith("By "):
            byline = plain
        elif plain.startswith("Banner:"):
            caption = plain.replace("Banner: ", "")
        else:
            blocks.append((tag, text))
    return {"title": title, "byline": byline, "caption": caption, "blocks": blocks}


def minutes(blocks):
    words = sum(len(re.sub(r"<[^>]+>", "", t).split()) for _, t in blocks)
    return max(1, round(words / 230))


RAIL = extract("articles/chinese-labor-transcontinental-railroad.html")
PAPER = extract("research/chinatown-solidarity-paper.html")
CHINA = extract("articles/chinatown-solidarity.html")

PUBS = [
    {"slug": "article-railroad", "kind": "Article", "date": "October 4, 2026", "short": "Oct 04 2026",
     "title": RAIL["title"], "author": "Minghao Gu", "img": "chinese-workers-summit-tunnel.jpg",
     "alt": "Chinese railroad workers among rocks near the opening of Summit Tunnel, 1865–1867",
     "summary": "Minghao Gu examines the dangerous labor, resistance, and overlooked legacy of Chinese immigrants who helped build the Transcontinental Railroad.",
     "min": minutes(RAIL["blocks"]), "data": RAIL},
    {"slug": "research-chinatown", "kind": "Research paper", "date": "March 11, 2026", "short": "Mar 11 2026",
     "title": PAPER["title"], "author": "Minghao Gu", "img": "chinatown-street-640.jpg",
     "alt": "Chinatown street with colorful lanterns and signs",
     "summary": "Full research paper examining the historical origins, cultural preservation, and modern resilience of Chinatown as an ethnic economy built on solidarity, identity, and community.",
     "min": minutes(PAPER["blocks"]), "data": PAPER},
    {"slug": "article-chinatown", "kind": "Article", "date": "February 2, 2026", "short": "Feb 02 2026",
     "title": CHINA["title"] or "Beyond Restaurants, Boba Cafes, and Souvenir Shops: The Historical and Modern Economic Solidarity of Chinatown",
     "author": "Minghao Gu", "img": "chinatown-banner-640.jpg", "alt": "Chinatown temple decorated with lanterns at night",
     "summary": "A historical and contemporary look at how Chinatowns foster economic solidarity, cultural preservation, and community resilience across generations.",
     "min": minutes(CHINA["blocks"]), "data": CHINA},
]
ARTICLES = [p for p in PUBS if p["kind"] == "Article"]
RESEARCH = [p for p in PUBS if p["kind"] != "Article"]

# ——— Page copy ———
TAGLINE = "Research for equitable communities"
LEDE = ("A student-led initiative studying equity, economics and ethnicity: who builds local economies, "
        "who gets credit and who gets left out. We publish what we find and track the grants that can change it.")
MISSION = ("To provide rigorous, community-centered research that bridges the gap between lived experiences and policy "
           "decisions, fostering a more equitable world for all ethnicities and economic backgrounds.")
PILLARS = [
    ("Equity", "Promoting fairness and justice in economic systems and social policy."),
    ("Economics", "Analyzing wealth distribution, labor markets, and community investment models."),
    ("Ethnicity", "Understanding the unique experiences and cultural wealth of diverse communities."),
]
ABOUT = {
    "who": "The e3 initiative is a student-led initiative committed to advancing understanding at the critical intersection of equity, economics, and ethnicity. We aim to amplify minority voices, highlight overlooked local and historical experiences, and bridge academic research with community storytelling.",
    "what": "We conduct rigorous, interdisciplinary research that examines how economic systems, policies, and practices affect the economic experience of ethnic communities. Our work includes interviews, research papers, articles, and community projects aimed towards building greater equity in the future.",
    "team": [
        ("Akshat Sawner", "Cofounder", "Bio coming soon."),
        ("Minghao Gu", "Cofounder", "Minghao is a junior at Solon High School. He plans to double major in ethnic studies/anthropology and economics in college. He was a former intern at Pasquines writing articles before leaving to start the e3 initiative."),
        ("Vikram Sakthi Manikandan", "Outreach director", "Vikram Sakthi Manikandan is a junior at Solon High School with an interest in finance and data science. He has developed his analytical skills through rigorous coursework and extracurriculars. As an experienced volunteer coordinator and intern at Cleveland Clinic, Vikram is now looking to utilize his background to drive meaningful community impact through this initiative."),
    ],
    "approach": [
        ("Community voices", "We elevate lived experiences through interviews and personal storytelling."),
        ("Cross-sector collaboration", "We work with local leaders, nonprofits, and businesses."),
        ("Findings", "We translate findings into meaningful stories that highlight economic resilience."),
    ],
}
OUTREACH = {
    "interview": ("Interview", "Community voices and personal stories.",
        "Through our interview program, we connect with community members to capture lived experiences and elevate voices often unheard in policy discussions. These conversations inform our research and help us understand the real-world impact of economic and social systems.",
        "Interested in sharing your story? Contact our outreach team to learn more about participating in our interview program."),
    "partnerships": ("Partnerships", "Collaborating for greater impact.",
        "We partner with local organizations, community leaders, academic institutions, and businesses to expand our reach and deepen our impact. These collaborations help us access diverse perspectives and ensure our research serves real community needs.",
        "If your organization is interested in partnering with e3 Initiative, please reach out through our contact page."),
}
HELP = {
    "intro": "Grants are free money you don't pay back, but they're competitive, and the application process trips a lot of people up. Use these tips to put together a strong application, and the directory below to get free, expert help when you need a real person.",
    "tips": [
        ("Confirm you're eligible first.", "Read the eligibility rules carefully before spending time on an application. Check business type (for-profit vs. 501(c)(3) nonprofit), location, size, revenue, time in operation, and any owner requirements. Applying when you don't qualify is the #1 wasted effort."),
        ("Read the full guidelines, twice.", "Funders publish exactly what they fund, what they won't fund, and how they score applications. Mirror their language and priorities in your answers."),
        ("Tell a clear, specific story.", "Explain who you are, the problem you're solving, who benefits, and what you'll do with the money. Concrete details and real numbers beat buzzwords."),
        ("Build a realistic budget.", "Show exactly how the funds will be used and tie each line item back to your goals. If a match is required, plan for it early."),
        ("Gather your documents ahead of time.", "Common asks: EIN, business registration, financial statements, a 501(c)(3) determination letter (nonprofits), a SAM.gov / UEI number (federal grants), and owner ID. Keep a folder ready so deadlines don't sneak up on you."),
        ("Tailor every application.", "Don't copy-paste one essay everywhere. Reuse your core story, but answer each funder's actual questions in their words."),
        ("Never miss the deadline.", "Submit a day or two early: portals get slow and crash near cutoffs. Note whether rolling grants review monthly or quarterly."),
        ("Proofread, then have someone else read it.", "Typos and unclear answers cost real points. A fresh set of eyes catches what you can't."),
    ],
    "mistakes": [
        "Applying when you don't meet the stated eligibility criteria.",
        "Missing the deadline, or submitting at the last minute.",
        "Ignoring the funder's priorities and writing what you wish they funded.",
        "A vague or unrealistic budget with no detail.",
        "Reusing a generic application instead of answering the actual questions.",
        "Forgetting required attachments (financials, tax status, registrations).",
        "Skipping the proofread and final review.",
        "Applying to only one grant. Apply to several to improve your odds.",
    ],
    "orgs": [
        ("SBA Local Assistance & SBDCs", "Small Business Development Centers offer free advising on funding, business plans, and grant readiness, in every state.", "Find your local office", "https://www.sba.gov/counseling/local-assistance/"),
        ("SCORE", "Free, confidential mentoring from experienced business volunteers, including help reviewing grant applications. Online or in person.", "Get a free mentor", "https://www.score.org/find-mentor"),
        ("Women's Business Centers", "SBA-funded centers that help women entrepreneurs with funding, training, and counseling at low or no cost.", "Find a center", "https://www.sba.gov/counseling/local-assistance/resource-partners/#womens-centers"),
        ("Veterans Business Outreach Centers", "Free business and funding help for veterans, service members, and military spouses starting or growing a business.", "Find a VBOC", "https://www.sba.gov/counseling/local-assistance/resource-partners/#veterans-business-outreach-centers"),
        ("MBDA Business Centers", "The Minority Business Development Agency helps minority-owned businesses access capital, contracts, and grant opportunities.", "Find an MBDA center", "https://www.mbda.gov/businesscenters"),
        ("Grants.gov Support", "The federal grants portal. Its support desk answers questions about applying for federal grants: call 1-800-518-4726 or email support@grants.gov.", "Grants.gov help", "https://www.grants.gov/support"),
        ("Candid (Foundation Directory)", "The go-to research tool for nonprofit grants and foundations. Use it free at a nearby Funding Information Network library.", "Find free access", "https://candid.org/find-us"),
        ("Dial 211 (United Way)", "A free, confidential helpline that connects you to local programs, financial assistance, and community resources. Call or text 211.", "Visit 211.org", "https://211.org/"),
    ],
    "disclaimer": "The information on this page is general guidance, not professional, legal, or financial advice. Program details and contact information change: confirm specifics with each organization directly before relying on them.",
}
BEFORE_APPLY = [
    ("Check the funder's page.", "Deadlines, award amounts, and rules change often. Treat this list as a starting point."),
    ("Read the eligibility details closely.", "Ownership share, years in business, revenue range, and location differ a lot between grants."),
    ("Plan for the next cycle.", "Many closed programs recur annually, so note their usual timing and prepare early."),
]
INDICATORS = [
    ("cpi", "Inflation", "CPI", "index", "CPI tracks the prices people pay for common items like groceries, rent, and transportation. If CPI rises quickly, your paycheck usually buys less."),
    ("core_cpi", "Inflation", "Core CPI", "index", "Core CPI removes food and energy, which jump around a lot. It shows whether inflation pressure is broad and persistent, not just a temporary shock."),
    ("ppi", "Inflation", "PPI", "index", "PPI measures what businesses pay for materials and production. When it rises, companies often pass those costs to consumers later."),
    ("core_pce", "Inflation", "Core PCE", "index", "Core PCE is the inflation measure the Fed watches most closely. It can influence interest-rate decisions that affect loans, mortgages, and credit cards."),
    ("fed_funds", "Rates", "Fed Funds", "%", "This is the benchmark short-term interest rate set through Fed policy. Higher rates usually mean more expensive borrowing and slower spending."),
    ("unemployment", "Labor", "Unemployment", "%", "The unemployment rate shows the share of people who want a job but cannot find one. Rising unemployment usually signals stress in the economy."),
    ("payrolls", "Labor", "Nonfarm Payrolls", "M jobs", "Payrolls count how many jobs employers added or lost. Strong payroll growth often means more hiring and healthier household income."),
    ("ten_year", "Growth / Rates", "10Y Yield", "%", "The 10-year Treasury yield reflects long-term growth and inflation expectations. It influences mortgage rates and can signal how confident markets are about the future."),
]
PRIVACY = [
    ("h2", "Information we collect"),
    ("h3", "Contact form"),
    ("p", 'If you send us a message, we receive the name, email address, subject and message you enter. We use them only to reply to you. The form is delivered by <a href="https://formsubmit.co/">FormSubmit</a>, a third-party service, which processes your submission in order to email it to us.'),
    ("h3", "Analytics"),
    ("p", "We use two analytics tools to understand which pages are read and how people find us:"),
    ("li", 'Google Analytics 4, which sets cookies and records page views, approximate location, device and browser information. See <a href="https://policies.google.com/privacy">Google\'s privacy policy</a>.'),
    ("li", "Umami, a privacy-focused analytics tool we host ourselves. It records page views and basic device information without tracking you across other websites."),
    ("p", "We do not use analytics data to identify individual visitors, and we do not sell it."),
    ("h3", "Settings saved in your browser"),
    ("p", "When you change the theme or text size, your choice is saved in your browser's local storage so it persists between visits. It stays on your device and is never sent to us."),
    ("h3", "Hosting logs"),
    ("p", "The site is hosted on Vercel, which keeps standard server logs (such as IP address, requested page and time) for security and operations."),
    ("h2", "Third-party content"),
    ("p", "Pages load fonts from Google Fonts and some images from Unsplash. Your browser contacts those services directly when it loads those files, so they may receive your IP address and browser details."),
    ("h2", "Your choices"),
    ("li", 'You can block or delete cookies in your browser settings, or install the <a href="https://tools.google.com/dlpage/gaoptout">Google Analytics opt-out add-on</a>. The site works normally either way.'),
    ("li", "You can ask us to delete any message you sent through the contact form."),
    ("h2", "Children"),
    ("p", "This site is not directed at children under 13, and we do not knowingly collect their personal information."),
    ("h2", "Changes to this policy"),
    ("p", "If we change how the site handles data, we will update this page and the date above."),
    ("h2", "Questions"),
    ("p", 'For privacy questions or deletion requests, please use our <a href="contact.html">contact form</a>.'),
]
JOURNAL = ("Critical Debates in Humanities, Science and Global Justice", "critical-debates-logo-340.png")

PAGES = ["index", "about", "articles", "article-railroad", "article-chinatown", "research", "research-chinatown",
         "journals", "grants", "grant-help", "minority-owned-business-grants", "women-owned-business-grants",
         "veteran-owned-business-grants", "economic-indicators", "outreach", "contact", "privacy", "404"]
TITLES = {
    "index": "Home", "about": "About", "articles": "Publications", "research": "Research", "journals": "Journals",
    "grants": "Grant Finder", "grant-help": "Grant Help & Tips", "economic-indicators": "Economic Indicators",
    "outreach": "Outreach", "contact": "Contact", "privacy": "Privacy Policy", "404": "Page not found",
    "article-railroad": RAIL["title"], "article-chinatown": PUBS[2]["title"], "research-chinatown": PAPER["title"],
    **{k: v[1] for k, v in CATEGORY_PAGES.items()},
}

# Shared runtime: indicator data (live from the site's API, a labelled placeholder otherwise)
INDICATORS_JS = r"""/* Loads /api/economic-indicators (live FRED data on the deployed site). Without it, returns a smooth
   placeholder shape flagged live:false, so themes can label it and show no numbers. */
window.loadIndicators = async function () {
  try {
    const r = await fetch('/api/economic-indicators', { cache: 'no-store' });
    if (!r.ok) throw new Error(r.status);
    const d = await r.json();
    if (!d.series) throw new Error('no series');
    return { live: true, years: d.years, series: d.series, asOf: d.asOfDate };
  } catch (e) {
    const years = Array.from({ length: 27 }, (_, i) => 2000 + i);
    const shape = (seed) => years.map((_, i) => 1 + 0.35 * Math.sin(i / 4 + seed) + i * 0.03 + 0.12 * Math.sin(i * 1.7 + seed * 2));
    const series = {};
    ['cpi', 'core_cpi', 'ppi', 'core_pce', 'fed_funds', 'unemployment', 'payrolls', 'ten_year'].forEach((k, j) => series[k] = shape(j));
    return { live: false, years, series, asOf: null };
  }
};
window.fmtIndicator = (v, unit) => unit === '%' ? v.toFixed(2) + '%' : unit === 'M jobs' ? v.toFixed(1) + 'M' : v.toFixed(1);
"""


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)

KEY_INDICATORS = ["cpi", "unemployment", "fed_funds", "payrolls"]


def replace_func(src, name, new):
    """Swap one top-level function in a theme module's source for a new version."""
    a = src.index(f"\ndef {name}(")
    b = src.find("\ndef ", a + 1)
    return src[:a + 1] + new.strip("\n") + "\n\n" + (src[b + 1:] if b != -1 else "")
