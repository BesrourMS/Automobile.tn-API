import requests
from bs4 import BeautifulSoup
import json

# Set the headers for CORS
headers = {'Access-Control-Allow-Origin': '*'}

# Make the initial request
url = 'https://www.automobile.tn/fr/neuf/recherche'
response = requests.get(url, headers=headers)
page = BeautifulSoup(response.text, 'html.parser')

# Get the total count
t = page.select('#facets fieldset div:nth-of-type(1) button')
total = t[0].get_text(strip=True)
count = total.split(" ")
limit = 0

# Count the number of elements
for a in page.select('#w0 div:nth-of-type(4) > span'):
    limit += 1

# Calculate the number of pages
pager = (int(count[1]) // limit) + 1 if int(count[1]) % limit != 0 else int(count[1]) // limit

j = 1
arrayclassement = []

# Loop through each page
while j <= pager:
    url = f'https://www.automobile.tn/fr/neuf/recherche/s=sort%21price?sort=price&page={j}'
    response = requests.get(url, headers=headers)
    html = BeautifulSoup(response.text, 'html.parser')
    i = 1

    # Loop through each element on the page
    while i <= limit:
        id = html.select(f'#w0 div:nth-of-type(4) > span:nth-of-type({i})')
        v = html.select(f'#w0 div:nth-of-type(4) > span:nth-of-type({i}) div a h2')
        x = html.select(f'#w0 div:nth-of-type(4) > span:nth-of-type({i}) div a div span')
        img = html.select(f'#w0 div:nth-of-type(4) > span:nth-of-type({i}) div a img')
        l = html.select(f'#w0 div:nth-of-type(4) > span:nth-of-type({i}) div a')

        d = id[0]['data-key'].strip() if id else ''
        voiture = v[0].get_text(strip=True) if v else ''
        prix = x[0].get_text(strip=True) if x else ''
        lien = l[0]['href'].strip() if l else ''
        logo = img[0]['src'].strip() if img else ''

        arrayclassement.append({
            'ID': d,
            'Voiture': voiture,
            'Image': logo,
            'Prix': prix,
            'Lien': 'https://www.automobile.tn' + lien,
        })
        i += 1

    j += 1

# Trim the array to the specified count
arrayclassement = arrayclassement[:int(count[1])]

# Print the result as JSON
print(json.dumps(arrayclassement, ensure_ascii=False))
