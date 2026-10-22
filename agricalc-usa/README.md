# AgriCalc USA

Static, fast, mobile-friendly farm calculator + guides website for U.S. farmers.
No backend, no database, no build tools required to host it.

## Folders
- `site/`   → upload-ready website (put the CONTENTS on your host: Cloudflare Pages, Netlify, GitHub Pages, any cPanel)
- `source/` → generator (`build.py`, `content.py`, `assets/`) if you want to edit and rebuild

## 1) Set your domain, email and AdSense (do this first)
Open `source/build.py` and edit the CONFIG block at the top:

    SITE_URL = "https://www.yourdomain.com"
    ADSENSE  = "ca-pub-XXXXXXXXXXXXXXXX"      # your publisher ID
    AD_SLOTS = dict(top="...", mid="...", end="...")   # your ad unit IDs (create 3 display units in AdSense)
    EMAIL    = "you@yourdomain.com"

Then run:  `cd source && python3 build.py`  → new site is written to `source/dist/` (upload that).

No Python? Search-and-replace in the `site/` folder instead:
- `https://www.agricalcusa.com` → your domain
- `ca-pub-XXXXXXXXXXXXXXXX` → your publisher ID (also in `ads.txt` as `pub-XXXXXXXXXXXXXXXX`)
- slots `1111111111`, `2222222222`, `3333333333` → your ad unit IDs
- `contact@agricalcusa.com` → your email

### How ads behave
Every page has `<ins class="adsbygoogle">` slots (top / middle / end of content) and the AdSense script in `<head>`.
Slots stay hidden until real IDs are set, so you never show empty boxes. To preview slot positions, open any page with `?adpreview=1`.

## 2) Deploy
Upload the contents of `site/` to the web root. Make sure `ads.txt` is at `https://yourdomain.com/ads.txt`.

## 3) After launch
1. Add the site to Google Search Console and submit `https://yourdomain.com/sitemap.xml`.
2. Apply for AdSense once the site is live on your own domain.
3. Optional: paste Google Analytics 4 code in the marked spot in `<head>` (in `build.py`, `layout()`), then rebuild.
4. If you expect visitors from the EEA/UK, enable a Google-certified consent message (AdSense > Privacy & messaging).

## Adding content
Open `source/content.py`, copy an article block, change slug/title/body, rebuild. Sitemap, related links, schema and table of contents are generated automatically.

## What's included
- 9 working calculators (land area, seed rate, fertilizer, crop profit/break-even, irrigation, grain converter, grain bin capacity, sprayer calibration, growing degree days)
- 11 guides with sources, worked examples, table of contents
- About, Editorial Policy, Contact, Privacy Policy (AdSense/CCPA language), Terms, Disclaimer, Sitemap, 404
- SEO: unique titles/descriptions, canonical URLs, Open Graph/Twitter, JSON-LD (Organization, WebSite, Article, WebApplication, FAQPage, BreadcrumbList), sitemap.xml, robots.txt
