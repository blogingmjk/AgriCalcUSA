#!/usr/bin/env python3
"""AgriCalc USA static site generator.  Run:  python3 build.py
Edit the CONFIG block, re-run, and upload the contents of ./dist"""
import os, re, json, html, shutil, datetime
from content import ARTICLES

# ============================ CONFIG (edit these) ============================
SITE_NAME   = "AgriCalc USA"
SITE_URL    = "https://www.agricalcusa.com"      # your real domain, no trailing slash
ADSENSE     = "ca-pub-XXXXXXXXXXXXXXXX"          # your AdSense publisher ID
AD_SLOTS    = dict(top="1111111111", mid="2222222222", end="3333333333")  # your ad unit IDs
EMAIL       = "contact@agricalcusa.com"          # contact email shown on site
TODAY       = "2026-10-22"
DISPLAY_DATE= "October 22, 2026"
# ============================================================================
OUT = "dist"
PUB = ADSENSE.replace("ca-", "")
esc = html.escape

def num(n, label, val, hint="", full=False, step="any", mn="0"):
    return f'<div class="{"full" if full else ""}"><label for="{n}">{label}</label><input id="{n}" name="{n}" type="number" inputmode="decimal" step="{step}" min="{mn}" value="{val}">{f"<div class=hint>{hint}</div>" if hint else ""}</div>'
def sel(n, label, opts, full=False, hint=""):
    o = "".join(f'<option value="{v}" {x}>{t}</option>' for v, t, x in opts)
    return f'<div class="{"full" if full else ""}"><label for="{n}">{label}</label><select id="{n}" name="{n}">{o}</select>{f"<div class=hint>{hint}</div>" if hint else ""}</div>'
O = lambda v, t, x="": (v, t, x)

CROPS_W = [O("corn", "Corn (56 lb/bu)"), O("soybeans", "Soybeans (60 lb/bu)"), O("wheat", "Wheat (60 lb/bu)"), O("barley", "Barley (48 lb/bu)"), O("oats", "Oats (32 lb/bu)"), O("sorghum", "Sorghum (56 lb/bu)"), O("rye", "Rye (56 lb/bu)")]

TOOLS = [
 dict(slug="land-area-converter", key="area", icon="📐", name="Land Area Converter", short="Convert acres, hectares, square feet, square yards and square miles.",
  desc="Free land area converter for farmers. Convert acres to hectares, square feet, square miles and more instantly.",
  fields=num("value", "Area", "40", full=True) + sel("unit", "Convert from", [O(k, k.capitalize(), "selected" if k == "acres" else "") for k in ["acres","hectares","square feet","square yards","square meters","square miles"]], full=True),
  about="Land is bought, rented and reported in different units. Deeds and USDA programs use **acres**, engineering plans use **square feet**, and international buyers and research papers use **hectares**. This tool converts any of the six common units to all the others at once.",
  formula="1 acre = 43,560 sq ft = 4,840 sq yd = 4,046.86 sq m = 0.4047 ha\n1 section (1 sq mile) = 640 acres",
  faqs=[("How many acres is a section?","A standard U.S. survey section is one square mile, which is 640 acres."),("How many square feet are in an acre?","An acre is 43,560 square feet. A square lot about 208.7 feet on each side is one acre."),("How do I convert acres to hectares?","Multiply acres by 0.4047. For example, 100 acres is about 40.47 hectares.")]),
 dict(slug="seed-rate-calculator", key="seed", icon="🌱", name="Seed Rate Calculator", short="Work out seeds per acre, total seed, bags and cost for corn, soybeans and wheat.",
  desc="Free seeding rate calculator for corn, soybeans and wheat. Adjust for germination and emergence and get bags, pounds and seed cost.",
  fields=sel("crop","Crop preset",[O("corn","Corn","selected"),O("soybeans","Soybeans"),O("wheat","Wheat (drilled)"),O("custom","Custom")],full=True,hint="Presets fill typical values. You can edit every field.")
   + num("acres","Acres","100") + num("pop","Target plants per acre","34000") + num("germ","Germination % (seed tag)","95") + num("emerg","Expected emergence %","92")
   + num("spl","Seeds per pound","1600") + num("bag","Seeds per bag (0 if sold by weight)","80000") + num("price","Seed price ($ per bag, or per lb if bag size is 0)","300",full=True),
  about="This calculator works backward from the plant population you want at harvest. It adjusts for seed germination and field emergence, then converts the answer into total seeds, pounds, bags and cost. Presets for corn, soybeans and wheat are **typical** values; replace them with the numbers from your seed tag and local recommendations.",
  formula="Seeds per acre = Target plants per acre ÷ (Germination % × Emergence %)",
  faqs=[("What germination rate should I use?","Use the germination percentage printed on the seed tag for your lot."),("What is a good emergence rate?","Many growers assume about 90 to 95 percent in good seedbeds and less in cold, wet or crusted soils."),("Why are my results different from my seed dealer's?","Dealers may use different population targets, seeds-per-bag sizes or emergence assumptions. Compare each input.")]),
 dict(slug="fertilizer-calculator", key="fert", icon="🧪", name="Fertilizer Rate Calculator", short="Convert N, P2O5 and K2O targets into pounds of product, tons and cost.",
  desc="Free fertilizer calculator. Convert nitrogen, phosphate and potash targets into pounds of urea, DAP, MAP, UAN, anhydrous and potash with cost.",
  fields=num("acres","Acres","100",full=True) + num("n","Nitrogen target (lb N/ac)","150") + num("p2o5","Phosphate target (lb P2O5/ac)","60") + num("k2o","Potash target (lb K2O/ac)","60")
   + sel("nsrc","Nitrogen source",[O("46-0-0","Urea (46-0-0)","selected"),O("34-0-0","Ammonium nitrate (34-0-0)"),O("82-0-0","Anhydrous ammonia (82-0-0)"),O("32-0-0","UAN 32 (32-0-0)"),O("28-0-0","UAN 28 (28-0-0)"),O("21-0-0","Ammonium sulfate (21-0-0)")])
   + sel("psrc","Phosphate source",[O("18-46-0","DAP (18-46-0)","selected"),O("11-52-0","MAP (11-52-0)"),O("0-0-0","None")])
   + sel("ksrc","Potash source",[O("0-0-60","Potash (0-0-60)","selected"),O("0-0-0","None")],full=True)
   + num("nprice","N product price ($/ton)","0") + num("pprice","P product price ($/ton)","0") + num("kprice","K product price ($/ton)","0",full=True,hint="Leave prices at 0 to skip the cost estimate."),
  about="Enter the nutrient amounts recommended by your soil test or extension service and pick the products you plan to use. The calculator converts nutrient pounds into pounds of product per acre, credits the nitrogen contained in DAP or MAP, and totals tons and cost for your acres.",
  formula="Product lb/ac = Nutrient lb/ac ÷ (Grade % ÷ 100)\nN credit from DAP/MAP = Product lb × (N % ÷ 100)",
  faqs=[("Does DAP count toward my nitrogen?","Yes. DAP is 18% N and MAP is 11% N. This calculator subtracts that nitrogen from your N target before sizing the N product."),("What is the difference between P and P2O5?","Labels and recommendations use P2O5. Elemental P is about 43.6% of P2O5."),("Is this a fertilizer recommendation?","No. It converts targets into product. Set targets from soil tests and local extension guidance.")]),
 dict(slug="crop-profit-calculator", key="profit", icon="💵", name="Crop Profit & Break-Even Calculator", short="Estimate net return per acre, break-even price and break-even yield.",
  desc="Free crop profit calculator with break-even price and yield. Enter yield, price and per-acre costs to see net return for corn, soybeans, wheat and more.",
  fields=num("acres","Acres","100") + num("yield","Expected yield (bu/ac)","200") + num("price","Expected price ($/bu)","4.50",full=True)
   + num("seed","Seed ($/ac)","110") + num("fert","Fertilizer ($/ac)","150") + num("chem","Crop protection ($/ac)","70") + num("ins","Insurance ($/ac)","30")
   + num("mach","Fuel & machinery ($/ac)","80") + num("labor","Labor ($/ac)","30") + num("rent","Land rent / ownership ($/ac)","250") + num("other","Drying, hauling, other ($/ac)","60"),
  about="Build a quick budget for any grain crop. Enter expected yield and price, then your costs per acre. The calculator shows revenue, total cost, net return, **break-even price** and **break-even yield**. The default numbers are illustrations only; replace them with your own records.",
  formula="Net per acre = (Yield × Price) − Total cost per acre\nBreak-even price = Total cost ÷ Yield\nBreak-even yield = Total cost ÷ Price",
  faqs=[("What is a break-even price?","It is the price per bushel you need to cover all listed costs at your expected yield."),("Should I include land rent?","Yes, if you rent or want to include a charge for owned land. Otherwise your result shows return to land and management."),("Where can I find cost estimates?","USDA ERS Commodity Costs and Returns and your state extension enterprise budgets are good checks.")]),
 dict(slug="irrigation-water-calculator", key="irrigation", icon="💧", name="Irrigation Water Calculator", short="Calculate acre-inches, gallons, acre-feet and pumping hours.",
  desc="Free irrigation calculator. Convert depth and acres to acre-inches, gallons, acre-feet and pumping time, with system efficiency.",
  fields=num("acres","Acres irrigated","80") + num("depth","Net depth to apply (inches)","1") + num("eff","System efficiency %","85") + num("gpm","Pump flow (GPM, optional)","800"),
  about="Enter how much water your crop needs, your irrigated area and the efficiency of your system. You get the gross depth you must pump, total water in acre-inches, acre-feet and gallons, plus the pumping time at your flow rate.",
  formula="Gross depth = Net depth ÷ Efficiency\nGallons = Acres × Gross depth (in) × 27,154\n1 acre-foot = 325,851 gallons",
  faqs=[("How many gallons are in an acre-inch?","One acre-inch is 27,154 gallons."),("What efficiency should I use?","Well-managed center pivots are often roughly 75 to 90 percent. Use your system's tested value when available."),("How much water does my crop need?","That depends on crop, growth stage, weather and soil. Use ET data from your state extension service.")]),
 dict(slug="grain-bushel-converter", key="grain", icon="🌽", name="Grain Bushel Converter", short="Convert bushels, pounds, tons and cwt, and bu/ac to kg/ha.",
  desc="Free grain bushel converter for corn, soybeans, wheat, barley, oats, sorghum and rye. Convert bushels to pounds, tons and metric tonnes.",
  fields=sel("crop","Grain",CROPS_W,full=True) + num("amount","Amount","1000") + sel("unit","Unit",[O(k,k.capitalize() if k!="hundredweight (cwt)" else k,"selected" if k=="bushels" else "") for k in ["bushels","pounds","short tons","metric tonnes","hundredweight (cwt)"]])
   + num("yield","Yield in bu/ac (optional)","200",full=True,hint="Converts to lb/ac, kg/ha and tonnes/ha."),
  about="Convert any amount of grain between bushels, pounds, short tons, metric tonnes and hundredweight using official standard test weights. Add a yield in bushels per acre to see metric yield for reports and international comparisons.",
  formula="Bushels = Pounds ÷ Test weight (lb/bu)\n1 lb/ac = 1.12085 kg/ha",
  faqs=[("How many pounds are in a bushel of corn?","Shelled corn is 56 pounds per bushel."),("How many bushels are in a ton of soybeans?","A short ton (2,000 lb) of soybeans is about 33.3 bushels at 60 lb per bushel."),("Do test weights change with moisture?","Actual test weight varies by lot. The standard weights here are for pricing and general conversion.")]),
 dict(slug="grain-bin-capacity-calculator", key="bin", icon="🛢️", name="Grain Bin Capacity Calculator", short="Estimate bushels and tons in a round grain bin, with peak.",
  desc="Free grain bin capacity calculator. Estimate bushels in a round bin from diameter, grain depth and peak height for corn, soybeans, wheat and more.",
  fields=sel("crop","Grain",CROPS_W,full=True) + num("dia","Bin diameter (ft)","30") + num("depth","Grain depth at wall (ft)","24") + num("peak","Peak height above wall (ft)","5",full=True,hint="Use 0 for a level fill."),
  about="Estimate how much grain a round bin holds before harvest or when planning deliveries. Enter diameter, grain depth at the sidewall and any peak height. The calculator adds a cone for the peak and converts bushels to tons for your selected grain.",
  formula="Cylinder bu = π × (D/2)² × depth × 0.8036\nCone bu = π × (D/2)² × peak ÷ 3 × 0.8036",
  faqs=[("How accurate is this?","It is a good planning estimate. Deep grain packs, so actual capacity may be a few percent higher. Confirm with your bin manufacturer."),("Why 0.8036?","One bushel is 1.2445 cubic feet, so one cubic foot holds 0.8036 bushels."),("Does it work for hopper-bottom bins?","Not directly. Add the hopper volume separately or use the manufacturer's chart.")]),
 dict(slug="sprayer-calibration-calculator", key="sprayer", icon="🚜", name="Sprayer Calibration Calculator", short="Calculate GPA, acres per tank and product per tank.",
  desc="Free sprayer calibration calculator. Find gallons per acre (GPA) from nozzle flow, speed and spacing, plus acres per tank and product per tank.",
  fields=num("gpm","Flow per nozzle (GPM)","0.4") + num("mph","Travel speed (mph)","10") + num("space","Nozzle spacing (inches)","20") + num("tank","Tank size (gallons)","500")
   + num("rate","Product rate per acre (label units)","32",hint="oz, pt, qt, whatever your label uses") + num("acres","Acres to spray (optional)","200"),
  about="Calibration confirms how many gallons per acre your sprayer really applies. Enter the nozzle flow from your catch test, your measured travel speed and the nozzle spacing. The tool returns GPA, acres covered per tank and the product to add to each tank.",
  formula="GPA = (GPM × 5,940) ÷ (MPH × Nozzle spacing in inches)\nAcres per tank = Tank gallons ÷ GPA",
  faqs=[("How do I measure travel speed?","Time a known distance, such as 200 feet, at spray speed. Speed in mph = feet ÷ seconds × 0.682."),("What flow rate should I enter?","Use the measured output per nozzle in gallons per minute from a one-minute catch test."),("Can I use this for any product?","Yes for the math, but always follow the label for rate, volume and nozzle type.")]),
 dict(slug="growing-degree-days-calculator", key="gdd", icon="🌡️", name="Growing Degree Days Calculator", short="Accumulate GDD from daily highs and lows using the 86/50 method.",
  desc="Free growing degree days (GDD) calculator. Paste daily high and low temperatures to accumulate corn heat units with the 86/50 method.",
  fields=sel("method","Method",[O("corn","Corn / soybeans / sorghum (86/50)",'selected data-base="50" data-cap="86" data-floor="1"'),O("wheat","Small grains (base 32°F, no cap)",'data-base="32" data-cap="0" data-floor="0"'),O("custom","Custom")],full=True)
   + num("base","Base temperature (°F)","50") + num("cap","Upper limit (°F, 0 for none)","86") + '<div class="full"><label><input type="checkbox" name="floor" checked style="width:auto;min-height:0;margin-right:.5rem">Raise lows below the base up to the base</label></div>'
   + '<div class="full"><label for="days">Daily temperatures (one line per day: high, low)</label><textarea id="days" name="days">85, 62\n90, 66\n78, 55\n72, 45\n68, 48</textarea></div>',
  about="Paste one line per day with the high and low temperature in °F. The calculator applies your base temperature and upper limit, then shows each day's GDD and the running total. Compare the total with your hybrid's GDD rating to plan maturity.",
  formula="GDD = (High + Low) ÷ 2 − Base\n86/50 method: cap highs at 86°F, raise lows below 50°F to 50°F",
  faqs=[("What is the 86/50 method?","It caps daily highs at 86°F and raises lows below 50°F to 50°F, then subtracts a 50°F base."),("Where do I get daily temperatures?","Use your local weather station, a state climate office or a university ag weather network."),("Can GDD be negative?","No. Days that fall below the base count as zero.")]),
]
TBY = {t["slug"]: t for t in TOOLS}
ABY = {a["slug"]: a for a in ARTICLES}
for a in ARTICLES:
    a["words"] = len(a["body"].split()); a["mins"] = max(3, round(a["words"] / 220))

# ------------------------------- helpers ------------------------------------
def md(text, R):
    lines = text.strip().split("\n"); out = []; toc = []; i = 0
    def inl(s):
        s = esc(s, quote=False)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
        return s
    while i < len(lines):
        L = lines[i]
        if not L.strip(): i += 1; continue
        if L.startswith("## "):
            t = L[3:]; sid = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-"); toc.append((sid, t)); out.append(f'<h2 id="{sid}">{inl(t)}</h2>')
        elif L.startswith("### "): out.append(f"<h3>{inl(L[4:])}</h3>")
        elif L.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "): buf.append(inl(lines[i][2:])); i += 1
            out.append('<div class="callout"><p>' + "<br>".join(buf) + "</p></div>"); continue
        elif L.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "): items.append(f"<li>{inl(lines[i][2:])}</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>"); continue
        elif re.match(r"\d+\. ", L):
            items = []
            while i < len(lines) and re.match(r"\d+\. ", lines[i]): items.append(f"<li>{inl(re.sub(r'^\d+\. ', '', lines[i]))}</li>"); i += 1
            out.append("<ol>" + "".join(items) + "</ol>"); continue
        elif L.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[\s\-|]+\|?$", lines[i]): rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            h = "<tr>" + "".join(f"<th>{inl(c)}</th>" for c in rows[0]) + "</tr>"
            b = "".join("<tr>" + "".join(f"<td>{inl(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="table-wrap"><table><thead>{h}</thead><tbody>{b}</tbody></table></div>'); continue
        else: out.append(f"<p>{inl(L)}</p>")
        i += 1
    return "\n".join(out).replace("{R}", R), toc

def ad(kind, R=""):
    return (f'<div class="ad-wrap" aria-label="Advertisement"><span class="ad-label">Advertisement</span>'
            f'<!-- AdSense unit: replace data-ad-slot with your ad unit ID -->'
            f'<ins class="adsbygoogle" style="display:block" data-ad-client="{ADSENSE}" data-ad-slot="{AD_SLOTS[kind]}" data-ad-format="auto" data-full-width-responsive="true"></ins></div>')

LOGO = '<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#256d3a"/><path d="M24 40V16" stroke="#f6d98a" stroke-width="2.6" stroke-linecap="round"/><g fill="#e0a82e"><ellipse cx="24" cy="10" rx="3.2" ry="5.5"/><ellipse cx="17" cy="17" rx="3" ry="5.2" transform="rotate(-35 17 17)"/><ellipse cx="31" cy="17" rx="3" ry="5.2" transform="rotate(35 31 17)"/><ellipse cx="17" cy="26" rx="3" ry="5.2" transform="rotate(-35 17 26)"/><ellipse cx="31" cy="26" rx="3" ry="5.2" transform="rotate(35 31 26)"/></g></svg>'

pages = []  # (path, priority, changefreq)

def layout(path, title, desc, body, schema=None, og_type="website", nav="", robots="index,follow,max-image-preview:large", extra_head=""):
    depth = path.count("/"); R = "../" * depth
    url = SITE_URL + "/" + ("" if path == "index.html" else path)
    t = title if title.endswith(SITE_NAME) else f"{title} | {SITE_NAME}"
    if len(t) > 62 and not title.endswith(SITE_NAME): t = title
    sch = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    def nv(k, label, href): return f'<li><a href="{R}{href}"{" aria-current=page" if nav == k else ""}>{label}</a></li>'
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(t)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{SITE_NAME}"><meta property="og:title" content="{esc(t)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE_URL}/assets/images/og-image.png"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(t)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{SITE_URL}/assets/images/og-image.png">
<meta name="theme-color" content="#256d3a">
<link rel="icon" href="{R}assets/images/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{R}assets/images/apple-touch-icon.png"><link rel="manifest" href="{R}manifest.webmanifest">
<link rel="stylesheet" href="{R}assets/css/style.css">
<!-- ===== GOOGLE ADSENSE: replace ca-pub-XXXXXXXXXXXXXXXX with your publisher ID (or re-run build.py) ===== -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE}" crossorigin="anonymous"></script>
<!-- ===== Optional: paste Google Analytics 4 / Search Console verification tags below ===== -->
{extra_head}{sch}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="header"><div class="container nav">
<a class="brand" href="{R}index.html">{LOGO}<span>{SITE_NAME}<small>Farm calculators &amp; guides</small></span></a>
<button class="toggle" aria-expanded="false" aria-controls="menu">Menu</button>
<ul class="menu" id="menu">{nv("home","Home","index.html")}{nv("tools","Calculators","tools/index.html")}{nv("guides","Guides","blog/index.html")}{nv("about","About","about.html")}<li><a class="cta" href="{R}contact.html">Contact</a></li></ul>
</div></header>
<main id="main">
{body.replace("{R}", R)}
</main>
<footer class="footer"><div class="container">
<div class="fgrid">
<div><a class="brand" href="{R}index.html">{LOGO}<span>{SITE_NAME}</span></a><p style="margin-top:1rem;font-size:.94rem">Free farm calculators and practical, research-based guides for American growers and ranchers.</p></div>
<div><h4>Calculators</h4><ul>{"".join(f'<li><a href="{R}tools/{t["slug"]}.html">{t["name"]}</a></li>' for t in TOOLS[:5])}<li><a href="{R}tools/index.html">All calculators →</a></li></ul></div>
<div><h4>Popular Guides</h4><ul>{"".join(f'<li><a href="{R}blog/{a["slug"]}.html">{esc(a["title"].split(":")[0])}</a></li>' for a in ARTICLES[:5])}<li><a href="{R}blog/index.html">All guides →</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="{R}about.html">About</a></li><li><a href="{R}editorial-policy.html">Editorial Policy</a></li><li><a href="{R}contact.html">Contact</a></li><li><a href="{R}privacy-policy.html">Privacy Policy</a></li><li><a href="{R}terms.html">Terms of Use</a></li><li><a href="{R}disclaimer.html">Disclaimer</a></li><li><a href="{R}sitemap.html">Sitemap</a></li></ul></div>
</div>
<small class="d">© {TODAY[:4]} {SITE_NAME}. Educational information only; not professional agronomic, legal, tax or financial advice. Always follow product labels and consult your local Extension office or a certified crop advisor.</small>
</div></footer>
<div class="cookie" id="cookie" role="dialog" aria-label="Privacy notice"><p>We use cookies and similar technologies for site functionality and to show ads through Google AdSense. See our <a href="{R}privacy-policy.html">Privacy Policy</a> for details and choices.</p><button class="btn btn-green" id="cookie-ok" type="button">Got it</button></div>
<script src="{R}assets/js/app.js" defer></script>
{"<script src='"+R+"assets/js/tools.js' defer></script>" if path.startswith("tools/") and path!="tools/index.html" else ""}
</body></html>"""

def write(path, content, pri="0.5", freq="monthly", listed=True):
    fp = os.path.join(OUT, path); os.makedirs(os.path.dirname(fp) or OUT, exist_ok=True)
    open(fp, "w", encoding="utf-8").write(content)
    if listed: pages.append((path, pri, freq))

def crumbs(items):
    h = '<nav class="crumbs container" aria-label="Breadcrumb">' + " <span>›</span> ".join(f'<a href="{{R}}{u}">{esc(n)}</a>' if u else esc(n) for n, u in items) + "</nav>"
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, **({"item": SITE_URL + "/" + (u if u != "index.html" else "")} if u else {})} for i, (n, u) in enumerate(items)]}
    return h, ld

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": SITE_NAME, "url": SITE_URL, "logo": SITE_URL + "/assets/images/apple-touch-icon.png", "email": EMAIL}

def card_tool(t): return f'<a class="card" href="{{R}}tools/{t["slug"]}.html"><div class="ico">{t["icon"]}</div><h3>{t["name"]}</h3><p>{t["short"]}</p><span class="more">Open calculator →</span></a>'
def card_art(a): return f'<a class="card" href="{{R}}blog/{a["slug"]}.html"><span class="tag">{a["cat"]}</span><h3>{esc(a["title"])}</h3><p>{esc(a["desc"])}</p><span class="meta">{a["mins"]} min read</span></a>'

# ------------------------------- HOME ---------------------------------------
home = f"""
<section class="hero"><div class="container">
<span class="eyebrow">For U.S. farmers, ranchers &amp; growers</span>
<h1>Farm calculators that do the math. Guides that get it right.</h1>
<p>Plan seed, fertilizer, water, grain storage and profit with free calculators built on standard U.S. units, plus plain-English guides grounded in USDA and land-grant extension research.</p>
<div class="row"><a class="btn btn-gold" href="{{R}}tools/index.html">Browse calculators</a><a class="btn btn-ghost" href="{{R}}blog/index.html">Read the guides</a></div>
<div class="stats"><div><b>{len(TOOLS)}</b><span>Free calculators</span></div><div><b>{len(ARTICLES)}</b><span>In-depth guides</span></div><div><b>0</b><span>Sign-ups required</span></div><div><b>100%</b><span>Works on phone &amp; tablet</span></div></div>
</div></section>
<section class="s"><div class="container"><div class="s-head"><h2>Free farm calculators</h2><p>Every tool uses U.S. units (acres, bushels, pounds, gallons, dollars) and shows the formula so you can check the work.</p></div>
<div class="grid">{"".join(card_tool(t) for t in TOOLS)}</div></div></section>
<div class="container">{ad("top")}</div>
<section class="s alt"><div class="container"><div class="s-head"><h2>Latest farming guides</h2><p>Practical how-to articles with worked examples and links to official USDA sources.</p></div>
<div class="grid">{"".join(card_art(a) for a in ARTICLES[:6])}</div><p class="mt"><a class="btn btn-green" href="{{R}}blog/index.html">See all guides</a></p></div></section>
<section class="s"><div class="container"><div class="s-head"><h2>Why farmers use {SITE_NAME}</h2></div>
<div class="trust"><div><b>Standard U.S. units</b><span>Acres, bushels, lb/ac, GPA, °F and USD, with no unit juggling.</span></div><div><b>Formulas shown</b><span>Each tool explains its math so you can verify it.</span></div><div><b>Official sources</b><span>Guides cite USDA agencies and point you to your state extension.</span></div><div><b>Private by design</b><span>Calculators run in your browser. Your numbers are not uploaded.</span></div></div></div></section>
<div class="container">{ad("end")}</div>
"""
write("index.html", layout("index.html", "Free Farm Calculators & Guides for U.S. Farmers", "Free farm calculators and guides for U.S. farmers: seed rate, fertilizer, irrigation, grain bin capacity, sprayer calibration, growing degree days and crop profit.", home, nav="home",
 schema=[ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": SITE_URL, "inLanguage": "en-US"}]), "1.0", "weekly")

# ------------------------------- TOOLS --------------------------------------
cb, cl = crumbs([("Home", "index.html"), ("Calculators", None)])
write("tools/index.html", layout("tools/index.html", "Free Farm Calculators for U.S. Farmers", "Free online farm calculators: seed rate, fertilizer, irrigation water, grain bin capacity, sprayer calibration, growing degree days, crop profit and unit converters.",
 cb + f'<div class="container page-head"><h1>Free farm calculators</h1><p class="lead">Nine tools for planning inputs, water, storage and profit. No sign-up, and everything runs in your browser.</p><div class="grid">{"".join(card_tool(t) for t in TOOLS)}</div>{ad("mid")}</div>', [cl, ORG], nav="tools"), "0.9", "weekly")

for t in TOOLS:
    cb, cl = crumbs([("Home", "index.html"), ("Calculators", "tools/index.html"), (t["name"], None)])
    rel_art = [a for a in ARTICLES if t["slug"] in a["tools"]][:3]
    others = [x for x in TOOLS if x["slug"] != t["slug"]][:3]
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in t["faqs"])
    about, _ = md(t["about"], "{R}")
    body = f"""{cb}<div class="container page-head"><h1>{t["name"]}</h1><p class="lead">{esc(t["short"])}</p></div>
<div class="container"><div class="tool-layout">
<form class="panel" id="tool-form" data-tool="{t["key"]}" novalidate><h2>Enter your numbers</h2><div class="fields">{t["fields"]}</div>
<div class="actions"><button class="btn btn-green" type="submit">Calculate</button><button class="btn btn-line" type="reset">Reset</button></div></form>
<div class="panel"><h2>Results</h2><div id="result" class="result" role="status" aria-live="polite">Press <strong>Calculate</strong> to see your results.</div></div></div>
{ad("top")}
<div class="narrow" style="margin-inline:0;width:min(820px,100%)"><h2>How this calculator works</h2>{about}<div class="formula">{esc(t["formula"]).replace(chr(10), "<br>")}</div>
<h2>Frequently asked questions</h2>{faq}
{ad("end")}
<h2>Related guides</h2><div class="related">{"".join(card_art(a) for a in rel_art)}</div>
<h2>More calculators</h2><div class="related">{"".join(card_tool(x) for x in others)}</div></div></div>"""
    schema = [cl, {"@context": "https://schema.org", "@type": "WebApplication", "name": t["name"], "url": f"{SITE_URL}/tools/{t['slug']}.html", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any", "description": t["desc"], "inLanguage": "en-US", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faqs"]]}]
    write(f"tools/{t['slug']}.html", layout(f"tools/{t['slug']}.html", f"{t['name']} (Free, U.S. Units)", t["desc"], body, schema, nav="tools"), "0.9", "monthly")

# ------------------------------- BLOG ---------------------------------------
cb, cl = crumbs([("Home", "index.html"), ("Guides", None)])
cats = sorted({a["cat"] for a in ARTICLES})
write("blog/index.html", layout("blog/index.html", "Farming Guides for U.S. Growers", "Practical farming guides for U.S. growers: seeding rates, fertilizer labels, hardiness zones, USDA programs, irrigation math, grain storage, soil testing and more.",
 cb + f'<div class="container page-head"><h1>Farming guides</h1><p class="lead">Clear, example-driven articles on planting, fertility, water, grain storage, equipment and farm business, with sources you can check.</p><p class="meta">Topics: {" · ".join(cats)}</p><div class="grid">{"".join(card_art(a) for a in ARTICLES)}</div>{ad("mid")}</div>', [cl, ORG], nav="guides"), "0.8", "weekly")

for a in ARTICLES:
    R = "{R}"; body_html, toc = md(a["body"], "{R}")
    parts = body_html.split("<h2")
    if len(parts) > 3: body_html = "<h2".join(parts[:3]) + ad("mid") + "<h2" + "<h2".join(parts[3:])
    toc_html = '<nav class="toc" aria-label="Table of contents"><b>In this guide</b><ol>' + "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc) + "</ol></nav>" if len(toc) > 2 else ""
    cb, cl = crumbs([("Home", "index.html"), ("Guides", "blog/index.html"), (a["title"], None)])
    tools_box = '<div class="callout"><p><strong>Try it:</strong> ' + " · ".join(f'<a href="{{R}}tools/{TBY[s]["slug"]}.html">{TBY[s]["name"]}</a>' for s in a["tools"]) + "</p></div>"
    src = '<h2>Sources and further reading</h2><ul class="sources">' + "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{esc(n)}</a></li>' for n, u in a["sources"]) + '<li>Your state land-grant university Extension service</li></ul>'
    rel = '<h2>Related guides</h2><div class="related">' + "".join(card_art(ABY[s]) for s in a["related"]) + "</div>"
    body = f"""{cb}<div class="narrow"><article class="article"><span class="tag">{a["cat"]}</span><h1 style="margin-top:.6rem">{esc(a["title"])}</h1>
<p class="meta">By the {SITE_NAME} editorial team · Updated {DISPLAY_DATE} · {a["mins"]} min read</p>
<p class="lead" style="font-size:1.12rem;color:var(--muted)">{esc(a["desc"])}</p>{toc_html}{body_html}{tools_box}{ad("end")}{src}
<p class="meta">This article is for general education and is not professional advice. See our <a href="{{R}}disclaimer.html">disclaimer</a> and <a href="{{R}}editorial-policy.html">editorial policy</a>.</p></article>{rel}</div>"""
    schema = [cl, {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "en-US", "mainEntityOfPage": f"{SITE_URL}/blog/{a['slug']}.html", "image": SITE_URL + "/assets/images/og-image.png", "author": {"@type": "Organization", "name": SITE_NAME}, "publisher": {"@type": "Organization", "name": SITE_NAME, "logo": {"@type": "ImageObject", "url": SITE_URL + "/assets/images/apple-touch-icon.png"}}}]
    write(f"blog/{a['slug']}.html", layout(f"blog/{a['slug']}.html", a["title"], a["desc"], body, schema, og_type="article", nav="guides"), "0.8", "monthly")

# ------------------------------ STATIC PAGES --------------------------------
def simple(path, title, desc, h1, content, nav="", pri="0.4"):
    cb, cl = crumbs([("Home", "index.html"), (h1, None)])
    c, _ = md(content, "{R}")
    write(path, layout(path, title, desc, cb + f'<div class="narrow"><article class="article"><h1>{h1}</h1><p class="meta">Last updated {DISPLAY_DATE}</p>{c}</article></div>', [cl], nav=nav), pri, "yearly")

simple("about.html", "About Us", f"About {SITE_NAME}: free farm calculators and research-based guides for U.S. farmers.", "About " + SITE_NAME, f"""
{SITE_NAME} is an independent educational website that gives American farmers, ranchers and gardeners free calculators and plain-English guides. Our goal is simple: make the everyday math of farming fast and transparent, and explain the reasoning behind it.

## What we publish
- **Calculators** for seed rate, fertilizer, irrigation water, grain storage, sprayer calibration, growing degree days, profit and unit conversion. Each tool shows its formula.
- **Guides** that explain concepts with worked examples and point to official USDA and land-grant university resources.

## How we work
We write in U.S. units, check formulas against standard references, and link to primary sources such as USDA agencies. Read our [editorial policy]({{R}}editorial-policy.html) for details on sourcing, updates and corrections.

## What we are not
We are not a certified crop advisor, lawyer or financial planner. Local soils, weather, labels and regulations vary, so use our content as a starting point and confirm decisions with your state Extension office or a qualified professional. See the [disclaimer]({{R}}disclaimer.html).

## How we are funded
This site is supported by advertising, including Google AdSense. Ads never decide what we write. Read the [privacy policy]({{R}}privacy-policy.html) to learn how ads and cookies work.

## Contact
Questions, corrections or suggestions for new tools? Visit the [contact page]({{R}}contact.html).
""", "about", "0.5")

simple("editorial-policy.html", "Editorial Policy", f"How {SITE_NAME} researches, writes, reviews and corrects its farming guides and calculators.", "Editorial Policy", """
## Accuracy and sourcing
Guides are based on public research and standard references, including USDA agencies (NRCS, NASS, ERS, FSA, RMA, ARS) and land-grant university Extension publications. We link to primary sources at the end of each article.

## Calculators
Calculators use published formulas and conversion constants. We show the formula on every tool page. Default values are illustrations; they are not recommendations for your farm.

## Examples and numbers
Prices, costs and yields in examples are illustrations, not forecasts. Agronomic ranges (such as plant populations or pH targets) are typical values and vary by region, crop and variety.

## Updates and corrections
We review content when standards, program rules or methods change. If you find an error, please [contact us]({R}contact.html). We correct verified errors promptly and update the "Updated" date.

## Independence and advertising
Advertising, including Google AdSense, supports this site. Advertisers do not influence our content, and we do not accept payment for product recommendations.

## No professional advice
Content is educational. For decisions about chemical use, finances, loans, insurance or legal compliance, consult a qualified professional and follow all product labels and local laws.
""", pri="0.3")

contact = f"""
<div class="narrow"><article class="article"><h1>Contact Us</h1><p>Have a question, correction or an idea for a new calculator? We read every message.</p>
<p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<form class="form-grid" action="mailto:{EMAIL}" method="post" enctype="text/plain">
<div><label for="n">Your name</label><input id="n" name="name" type="text" autocomplete="name" required></div>
<div><label for="e">Your email</label><input id="e" name="email" type="email" autocomplete="email" required></div>
<div><label for="m">Message</label><textarea id="m" name="message" required style="font-family:inherit"></textarea></div>
<div><button class="btn btn-green" type="submit">Send message</button></div>
<p class="form-note">This form opens your email app. We cannot give individual agronomic, legal or financial advice; for field-specific help, contact your local Extension office.</p></form></article></div>"""
cb, cl = crumbs([("Home", "index.html"), ("Contact", None)])
write("contact.html", layout("contact.html", "Contact Us", f"Contact the {SITE_NAME} team with questions, corrections or tool suggestions.", cb + contact, [cl]), "0.4", "yearly")

simple("privacy-policy.html", "Privacy Policy", f"Privacy policy for {SITE_NAME}: what data we collect, how cookies and Google AdSense work, and your choices.", "Privacy Policy", f"""
This Privacy Policy explains how {SITE_NAME} ("we", "us") handles information when you visit {SITE_URL}.

## Information we collect
- **Calculator inputs.** Numbers you enter in calculators are processed in your browser. We do not receive or store them.
- **Contact messages.** If you email us, we receive your name, email address and message and use them only to respond.
- **Automatically collected data.** Like most websites, our hosting provider and third-party services may collect IP address, browser type, device information, pages viewed and referring pages.

## Cookies and similar technologies
Cookies are small files stored on your device. We and our partners use them for basic site functions, to remember that you dismissed our privacy notice, to measure traffic and to serve and measure ads.

## Advertising and Google AdSense
We use Google AdSense to display ads. Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to our site and/or other sites on the Internet.
- You can opt out of personalized advertising by visiting [Google Ads Settings](https://adssettings.google.com).
- You can also opt out of some third-party vendors' use of cookies for personalized advertising at [www.aboutads.info](https://www.aboutads.info).
- Learn how Google uses data at [How Google uses information from sites or apps that use our services](https://policies.google.com/technologies/partner-sites).

## Your choices and U.S. state privacy rights
Residents of some states, including California, Colorado, Connecticut, Virginia and others, may have rights to access, delete or correct personal information and to opt out of its sale, sharing for cross-context behavioral advertising or targeted advertising. We do not knowingly sell personal information for money. To make a request, email {EMAIL}. You can also manage cookies in your browser settings.

## Children's privacy
This site is not directed to children under 13, and we do not knowingly collect their personal information.

## Third-party links
Our content links to other sites, such as USDA. We are not responsible for their privacy practices.

## Changes to this policy
We may update this policy and will post the new date above.

## Contact
Questions about privacy? Email {EMAIL}.
""", pri="0.3")

simple("terms.html", "Terms of Use", f"Terms of use for {SITE_NAME}: how you may use our free farm calculators and guides, and our limits of liability.", "Terms of Use", f"""
By using {SITE_NAME} you agree to these terms.

## Use of the site
You may use the site and its calculators for personal and business purposes. You agree not to misuse the site, attempt to disrupt it, or copy substantial portions of our content without permission.

## Educational purpose
Content and calculator results are provided for general information only. See the [disclaimer]({{R}}disclaimer.html).

## No warranties
The site is provided "as is" and "as available" without warranties of any kind, to the fullest extent permitted by law. We do not guarantee that calculations or content are error-free, complete or suitable for your particular situation.

## Limitation of liability
To the fullest extent permitted by law, {SITE_NAME} and its owners are not liable for any loss or damage arising from use of, or reliance on, the site or its calculators, including crop loss, financial loss or regulatory penalties.

## Intellectual property
Text, design, code and graphics are owned by {SITE_NAME} unless noted. You may link to our pages freely.

## Third-party content and ads
The site may display third-party advertising and link to third-party sites that we do not control.

## Changes
We may update these terms at any time. Continued use means you accept the updated terms.

## Contact
Email {EMAIL}.
""", pri="0.3")

simple("disclaimer.html", "Disclaimer", f"Disclaimer for {SITE_NAME}: educational information, not professional agronomic, legal or financial advice.", "Disclaimer", """
## Educational information only
Everything on this website, including calculators, examples and guides, is for general educational purposes. It is not professional agronomic, legal, tax, insurance or financial advice.

## Verify before you act
Soils, weather, crop varieties, pests, laws and program rules differ by location and change over time. Verify recommendations with your state land-grant university Extension service, a Certified Crop Adviser, or the relevant agency before making decisions.

## Pesticides and chemicals
The label is the law. Always read and follow the product label, including rates, safety equipment, re-entry intervals and restrictions. Nothing here replaces a label.

## Calculator results
Calculators provide estimates based on the inputs you enter and standard formulas. Results depend on input accuracy and may differ from real-world outcomes. Example numbers (prices, costs, yields) are illustrations, not forecasts.

## Government programs and links
Program descriptions are summaries and may be out of date. Rules, deadlines and eligibility are set by the administering agencies. Visit farmers.gov or your local USDA Service Center for current information. Links to outside websites do not imply endorsement.

## Advertising
This site displays ads, including Google AdSense. Advertisements are not endorsements of products or services.
""", pri="0.3")

# sitemap page + 404
cb, cl = crumbs([("Home", "index.html"), ("Sitemap", None)])
write("sitemap.html", layout("sitemap.html", "Sitemap", f"Browse every calculator, guide and policy page on {SITE_NAME} from one simple sitemap.", cb + f'<div class="narrow"><article class="article"><h1>Sitemap</h1><h2>Calculators</h2><ul>{"".join(f"<li><a href={{R}}tools/{t[chr(115)+chr(108)+chr(117)+chr(103)]}.html>{t[chr(110)+chr(97)+chr(109)+chr(101)]}</a></li>" for t in TOOLS)}</ul><h2>Guides</h2><ul>{"".join(f"<li><a href={{R}}blog/{a[chr(115)+chr(108)+chr(117)+chr(103)]}.html>{esc(a[chr(116)+chr(105)+chr(116)+chr(108)+chr(101)])}</a></li>" for a in ARTICLES)}</ul><h2>Company</h2><ul><li><a href={{R}}about.html>About</a></li><li><a href={{R}}editorial-policy.html>Editorial Policy</a></li><li><a href={{R}}contact.html>Contact</a></li><li><a href={{R}}privacy-policy.html>Privacy Policy</a></li><li><a href={{R}}terms.html>Terms of Use</a></li><li><a href={{R}}disclaimer.html>Disclaimer</a></li></ul></article></div>', [cl]), "0.3", "monthly")
write("404.html", layout("404.html", "Page Not Found", "The page you requested could not be found.", '<div class="container page-head center"><h1>Page not found</h1><p class="lead" style="margin-inline:auto">That page may have moved. Try a calculator or guide instead.</p><p><a class="btn btn-green" href="/index.html">Home</a> <a class="btn btn-line" href="/tools/index.html">Calculators</a> <a class="btn btn-line" href="/blog/index.html">Guides</a></p></div>', robots="noindex,follow"), listed=False)

# ------------------------------ ROOT FILES ----------------------------------
for d in ("assets/css", "assets/js"):
    os.makedirs(f"{OUT}/{d}", exist_ok=True)
    for f in os.listdir(d): shutil.copy(f"{d}/{f}", f"{OUT}/{d}/{f}")
os.makedirs(f"{OUT}/assets/images", exist_ok=True)
open(f"{OUT}/assets/images/favicon.svg", "w").write(LOGO.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '))
try:
    from PIL import Image, ImageDraw, ImageFont
    def font(sz, bold=False):
        for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",):
            if os.path.exists(p): return ImageFont.truetype(p, sz)
        return ImageFont.load_default()
    im = Image.new("RGB", (1200, 630), "#143823"); d = ImageDraw.Draw(im)
    for x in range(-200, 1400, 46): d.line([(x, 630), (x + 300, 0)], fill="#1b4a2e", width=3)
    d.ellipse((780, 260, 1300, 780), fill="#256d3a"); d.rounded_rectangle((70, 70, 150, 150), 20, fill="#e0a82e")
    d.text((70, 230), SITE_NAME, font=font(96, True), fill="#ffffff"); d.text((74, 370), "Free farm calculators & guides", font=font(44), fill="#f6d98a")
    d.text((74, 440), "for U.S. farmers, ranchers and growers", font=font(34), fill="#cfe3d4"); im.save(f"{OUT}/assets/images/og-image.png")
    ic = Image.new("RGB", (180, 180), "#256d3a"); di = ImageDraw.Draw(ic); di.line([(90, 150), (90, 60)], fill="#f6d98a", width=8)
    for cx, cy in [(90, 40), (62, 62), (118, 62), (62, 96), (118, 96)]: di.ellipse((cx - 13, cy - 20, cx + 13, cy + 20), fill="#e0a82e")
    ic.save(f"{OUT}/assets/images/apple-touch-icon.png")
except Exception as e: print("PIL skipped:", e)
open(f"{OUT}/manifest.webmanifest", "w").write(json.dumps({"name": SITE_NAME, "short_name": "AgriCalc", "start_url": "/index.html", "display": "standalone", "background_color": "#faf6ec", "theme_color": "#256d3a", "icons": [{"src": "/assets/images/apple-touch-icon.png", "sizes": "180x180", "type": "image/png"}]}))
open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
open(f"{OUT}/ads.txt", "w").write(f"google.com, {PUB}, DIRECT, f08c47fec0942fa0\n")
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.w3.org/2005/Atom">'.replace("http://www.w3.org/2005/Atom", "http://www.sitemaps.org/schemas/sitemap/0.9") + "\n"
for p, pri, fr in pages: sm += f"  <url><loc>{SITE_URL}/{'' if p=='index.html' else p}</loc><lastmod>{TODAY}</lastmod><changefreq>{fr}</changefreq><priority>{pri}</priority></url>\n"
open(f"{OUT}/sitemap.xml", "w").write(sm + "</urlset>\n")
print(f"Built {len(pages)} pages into ./{OUT}")
