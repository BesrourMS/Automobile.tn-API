from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
import asyncio
from bs4 import BeautifulSoup

app = FastAPI()

async def fetch_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return BeautifulSoup(response.text, 'html.parser')

@app.get("/")
async def scrape_and_response():
    # Set the headers for CORS
    headers = {'Access-Control-Allow-Origin': '*'}

    # Make the initial request
    url = 'https://www.automobile.tn/fr/neuf/recherche'
    page = await fetch_data(url)

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

    # Loop through each page asynchronously
    async with httpx.AsyncClient() as client:
        tasks = []
        while j <= pager:
            url = f'https://www.automobile.tn/fr/neuf/recherche/s=sort%21price?sort=price&page={j}'
            tasks.append(fetch_data(url))
            j += 1

        pages = await asyncio.gather(*tasks)

    # Loop through each element on each page
    for html in pages:
        i = 1
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

    # Trim the array to the specified count
    arrayclassement = arrayclassement[:int(count[1])]

    # Create a FastAPI JSONResponse with additional headers
    response_data = JSONResponse(content=arrayclassement)

    # Add additional headers to the response
    response_data.headers['Content-type'] = 'application/json; charset=utf-8'
    response_data.headers['X-Total-Pages'] = str(pager)
    response_data.headers['X-Total-Cars'] = str(count[1])
    response_data.headers['X-Powered-By'] = 'Mohamed Safouan Besrour'

    return response_data
