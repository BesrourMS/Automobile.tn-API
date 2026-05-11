from scrapling.fetchers import StealthyFetcher
from scrapling import Selector
import json

BASE_URL = "https://www.automobile.tn"

FETCH_OPTS = dict(
    block_webrtc=True,
    hide_canvas=True,
    network_idle=True,
    retries=2,
    solve_cloudflare=True,
)

# --- Step 1: Get first page to determine total count and items per page ---
first_page = StealthyFetcher.fetch(
    f"{BASE_URL}/fr/neuf/electrique/",
    real_chrome=False,
    **FETCH_OPTS,
)

# Total count from facets button
total_btn = first_page.css('#facets fieldset div:nth-of-type(1) button').first
total_text = total_btn.text.strip() if total_btn else "0 0"
count_parts = total_text.split(" ")
total_count = int(count_parts[1]) if len(count_parts) > 1 else 0

# Items per page
items_on_page = len(first_page.css('#w0 div:nth-of-type(4) > span'))
limit = items_on_page if items_on_page > 0 else 1

# Number of pages
pager = (total_count // limit) + (1 if total_count % limit != 0 else 0)

print(f"Total: {total_count} | Per page: {limit} | Pages: {pager}")

# --- Step 2: Scrape all pages ---
arrayclassement = []

for j in range(1, pager + 1):
    url = f"{BASE_URL}/fr/neuf/electrique/s=sort%21price?sort=price&page={j}"
    page = StealthyFetcher.fetch(url, real_chrome=False, **FETCH_OPTS)

    spans = page.css('#w0 div:nth-of-type(4) > span')
    print(f"Page {j}/{pager} — {len(spans)} items")

    for span in spans:
        # data-key on the span itself
        d       = span.attrib.get('data-key', '').strip()

        # Car name
        h2      = span.css('div a h2')
        voiture = h2.first.text.strip() if h2 else ''

        # Price
        price_el = span.css('div a div span')
        prix     = price_el.first.text.strip() if price_el else ''

        # Link
        a_el = span.css('div a')
        href = a_el.first.attrib.get('href', '').strip() if a_el else ''
        lien = BASE_URL + href if href else ''

        # Image
        img_el = span.css('div a img')
        logo   = img_el.first.attrib.get('src', '').strip() if img_el else ''

        arrayclassement.append({
            'ID':      d,
            'Voiture': voiture,
            'Image':   logo,
            'Prix':    prix,
            'Lien':    lien,
        })

    if len(arrayclassement) >= total_count:
        break

# Trim to exact total
arrayclassement = arrayclassement[:total_count]

with open('ev.json', 'w', encoding='utf-8') as f:
    json.dump(arrayclassement, f, indent=2, ensure_ascii=False)

print(f"Saved {len(arrayclassement)} cars to ev.json")